"""Audit every workbook entry's Code / Protocol / Dashboard URLs.

For each of the 483 entries, we HEAD-check three URLs:
  - Code:      the GitHub repo (should 200 or 301→200)
  - Protocol:  the E156-PROTOCOL.md in the repo
  - Dashboard: the GitHub Pages URL

Output:
  - audit_links_<date>.csv     full per-entry report
  - audit_links_<date>.json    structured version for downstream scripts
  - audit_links_<date>.md      human-readable summary

A GitHub 404 on the Pages URL doesn't necessarily mean Pages is broken
— it can also mean Pages was never enabled for that repo. We
distinguish:
  - repo_ok + dashboard_ok      → fully shipped
  - repo_ok + dashboard_404     → Pages not enabled (fixable)
  - repo_404                    → repo doesn't exist (unfixable here —
                                   the student board shouldn't list it)
  - repo_ok + protocol_404      → protocol file missing from repo

Uses concurrent.futures to parallelise HEAD requests (~20 in flight)
so 1449 URL checks finish in a few minutes instead of ~1 hr serial.

Respects GitHub rate limits (60 unauthenticated req/hr, 5000 with a
token) by reading GITHUB_TOKEN from env if set.

Usage:
  python audit_links.py
  python audit_links.py --workers 10   # throttle down on slow internet
  python audit_links.py --skip-protocol  # only check Code + Dashboard
"""
from __future__ import annotations
import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

WORKBOOK = Path(__file__).resolve().parents[1] / "rewrite-workbook.txt"
OUT_DIR = Path(__file__).resolve().parents[1] / "audit_output"

# Per-entry extractor. The SUBMISSION METADATA block has this shape:
#
#   [N/M] ProjectName
#   TITLE: ...
#   ...
#   Links:
#     Code:      https://github.com/...
#     Protocol:  https://github.com/.../blob/main/E156-PROTOCOL.md
#     Dashboard: https://....github.io/...
#
# We capture (number, name, code_url, protocol_url, dashboard_url).

ENTRY_HEADER_RE = re.compile(r"\[(\d+)/\d+\]\s+(\S+)")
LINKS_BLOCK_RE = re.compile(
    r"Links:\s*\n"
    r"\s*Code:\s*(\S+)\s*\n"
    r"\s*Protocol:\s*(\S+)\s*\n"
    r"\s*Dashboard:\s*(\S+)",
    re.MULTILINE,
)


def parse_workbook() -> list[dict]:
    text = WORKBOOK.read_text(encoding="utf-8")
    entries = []
    # Split on the 70-char `=` separator that brackets each entry.
    blocks = text.split("\n======================================================================\n")
    for block in blocks:
        hdr = ENTRY_HEADER_RE.search(block)
        links = LINKS_BLOCK_RE.search(block)
        if hdr and links:
            entries.append({
                "num": int(hdr.group(1)),
                "name": hdr.group(2),
                "code": links.group(1).strip(),
                "protocol": links.group(2).strip(),
                "dashboard": links.group(3).strip(),
            })
    return entries


def head_check(url: str, timeout: float = 12.0, token: str | None = None,
               max_retries: int = 3) -> dict:
    """GET the URL with retries and exponential backoff.

    Uses GET not HEAD because GitHub occasionally rate-limits HEAD harder,
    and Pages URLs don't always answer HEAD cleanly. Retries on 403, 429,
    5xx, and connection errors. Returns final status after retries.

    Return {'url', 'status', 'final_url', 'elapsed_ms', 'error', 'retries'}.
    """
    start = time.time()
    headers = {
        "User-Agent": "e156-link-audit/1.0",
        "Accept": "*/*",
        # Only ask for minimal bytes — we just need the status code.
        "Range": "bytes=0-0",
    }
    if token and "github.com" in url:
        headers["Authorization"] = f"Bearer {token}"

    last_err = ""
    last_status = 0
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, method="GET", headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return {
                    "url": url, "status": resp.status, "final_url": resp.url,
                    "elapsed_ms": int((time.time() - start) * 1000),
                    "error": "", "retries": attempt,
                }
        except urllib.error.HTTPError as e:
            last_status = e.code
            last_err = f"HTTP {e.code}"
            # 404 / 410 are definitive — don't retry
            if e.code in (404, 410):
                return {
                    "url": url, "status": e.code, "final_url": url,
                    "elapsed_ms": int((time.time() - start) * 1000),
                    "error": last_err, "retries": attempt,
                }
            # 416 (range not satisfiable) — url exists, we just asked wrong
            if e.code == 416:
                return {
                    "url": url, "status": 200, "final_url": url,
                    "elapsed_ms": int((time.time() - start) * 1000),
                    "error": "416→treated as 200 (range)", "retries": attempt,
                }
            # 403/429/5xx → retry with backoff
        except urllib.error.URLError as e:
            last_err = f"URLError: {e.reason}"
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"

        if attempt < max_retries - 1:
            # Exponential backoff: 1s, 2s, 4s…
            time.sleep(1.5 ** attempt + 0.5)

    return {
        "url": url, "status": last_status, "final_url": url,
        "elapsed_ms": int((time.time() - start) * 1000),
        "error": last_err, "retries": max_retries,
    }


def classify(entry: dict, results: dict) -> str:
    """Return a status tag summarising the entry's link health."""
    c = results["code"]["status"]
    p = results["protocol"]["status"]
    d = results["dashboard"]["status"]

    if c >= 400:
        return "repo_404"
    if d >= 400:
        if p >= 400:
            return "repo_ok_but_protocol_and_dashboard_404"
        return "repo_ok_pages_missing"
    if p >= 400:
        return "repo_ok_protocol_404"
    return "ok"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--skip-protocol", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="cap at N entries (debug)")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    date = dt.date.today().isoformat()

    token = os.environ.get("GITHUB_TOKEN", "").strip() or None
    if token:
        print(f"[audit] using GITHUB_TOKEN (higher rate limit)", file=sys.stderr)

    entries = parse_workbook()
    if args.limit:
        entries = entries[: args.limit]
    print(f"[audit] {len(entries)} entries parsed from workbook", file=sys.stderr)

    # Flatten to a list of (entry_idx, url_kind, url) tuples for the pool
    jobs = []
    for idx, e in enumerate(entries):
        jobs.append((idx, "code", e["code"]))
        if not args.skip_protocol:
            jobs.append((idx, "protocol", e["protocol"]))
        jobs.append((idx, "dashboard", e["dashboard"]))

    # Results: entry_results[idx][kind] = head_check dict
    entry_results: list[dict] = [dict() for _ in entries]

    start = time.time()
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(head_check, url, 8.0, token): (idx, kind)
                for idx, kind, url in jobs}
        done = 0
        for fut in cf.as_completed(futs):
            idx, kind = futs[fut]
            entry_results[idx][kind] = fut.result()
            done += 1
            if done % 50 == 0:
                print(f"[audit] {done}/{len(jobs)} checks done "
                      f"({(time.time() - start):.0f}s elapsed)", file=sys.stderr)

    # Fill in skipped protocol slot as "skipped"
    if args.skip_protocol:
        for r in entry_results:
            r["protocol"] = {"url": "", "status": 200, "final_url": "",
                             "elapsed_ms": 0, "error": "skipped"}

    # Classify each entry
    tally: dict[str, int] = {}
    per_entry = []
    for e, r in zip(entries, entry_results):
        tag = classify(e, r)
        tally[tag] = tally.get(tag, 0) + 1
        per_entry.append({**e, **{f"{k}_status": v["status"] for k, v in r.items()}, "tag": tag})

    # Write CSV + JSON
    csv_path = OUT_DIR / f"audit_links_{date}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(per_entry[0].keys()))
        w.writeheader()
        w.writerows(per_entry)

    json_path = OUT_DIR / f"audit_links_{date}.json"
    json_path.write_text(json.dumps({"entries": per_entry, "tally": tally}, indent=2), encoding="utf-8")

    # Write MD summary
    md = [f"# E156 link audit — {date}", "", f"{len(entries)} entries, {len(jobs)} URL checks", ""]
    md.append("## Tally")
    for k, v in sorted(tally.items(), key=lambda x: -x[1]):
        md.append(f"- **{k}**: {v}")
    md.append("")

    needs_dashboard = [e for e in per_entry if e["tag"] == "repo_ok_pages_missing"]
    if needs_dashboard:
        md.append(f"## Needs dashboard ({len(needs_dashboard)})")
        md.append("")
        md.append("| # | Project | Repo |")
        md.append("|---|---------|------|")
        for e in needs_dashboard[:100]:
            md.append(f"| {e['num']} | {e['name']} | {e['code']} |")
        md.append("")

    broken_repos = [e for e in per_entry if e["tag"] == "repo_404"]
    if broken_repos:
        md.append(f"## Repo 404 (unfixable — remove from student board) ({len(broken_repos)})")
        md.append("")
        for e in broken_repos[:30]:
            md.append(f"- [{e['num']}] {e['name']} — {e['code']}")
        md.append("")

    md_path = OUT_DIR / f"audit_links_{date}.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    # Stdout summary
    print()
    print("=" * 60)
    print(f"E156 link audit — {date}")
    print("=" * 60)
    for k, v in sorted(tally.items(), key=lambda x: -x[1]):
        print(f"  {k:<45} {v:>4}")
    print()
    print(f"CSV:  {csv_path}")
    print(f"JSON: {json_path}")
    print(f"MD:   {md_path}")
    print(f"Elapsed: {time.time() - start:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
