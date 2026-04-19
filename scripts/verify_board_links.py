"""End-to-end claim-board verifier.

For each of the visible entries on students.html, checks that every link
works AND that each paper's dashboard is unique-and-topical. Writes a
structured report so we know exactly what's broken or semantically off.

Checks performed:
  1. Parse students.html's embedded JSON -> list of visible entries.
  2. For each entry, HEAD-check code_url, protocol_url, pages_url.
     (HEAD with fallback to GET, follow redirects, 5s timeout, 10 workers.)
  3. Group entries by pages_url -> flag shared dashboards (one dashboard
     serving N different papers is almost always a topic-mismatch bug).
  4. Group entries by code_url -> flag legitimate shared-repo clusters
     (intentional for some living-MA engines, wrong for others).
  5. For a sample of pages_urls (up to 60), download and check whether
     the page's <title> / <h1> mentions a keyword from the paper topic
     / body. Mismatches go to review list.

Writes audit_output/board_verify_<date>.json  (full machine-readable)
       audit_output/board_verify_<date>.md    (human summary)
"""
from __future__ import annotations
import argparse
import concurrent.futures as cf
import datetime as dt
import io
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from collections import defaultdict

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
STUDENTS_HTML = E156 / "students.html"
LOG_DIR = E156 / "audit_output"

TIMEOUT = 8.0
WORKERS = 12
USER_AGENT = "Mozilla/5.0 (E156-board-verifier)"


def parse_entries_from_html() -> list[dict]:
    """Pull the embedded ENTRIES JSON out of students.html."""
    text = STUDENTS_HTML.read_text(encoding="utf-8")
    m = re.search(r"const ENTRIES = (\[.*?\]);\s*$", text, re.DOTALL | re.MULTILINE)
    if not m:
        # Try alternate pattern
        m = re.search(r"const ENTRIES\s*=\s*(\[.*?\]);", text, re.DOTALL)
    if not m:
        raise RuntimeError("couldn't find `const ENTRIES = [...]` in students.html")
    return json.loads(m.group(1))


def check_url(url: str) -> dict:
    """HEAD check with GET fallback. Returns {status, final_url, error}."""
    if not url:
        return {"status": None, "note": "no_url"}
    rec = {"url": url}
    try:
        req = urllib.request.Request(
            url, method="HEAD",
            headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            rec["status"] = resp.status
            rec["final_url"] = resp.url
            return rec
    except urllib.error.HTTPError as e:
        # 405 Method Not Allowed on HEAD -> fall through to GET
        if e.code != 405:
            rec["status"] = e.code
            rec["error"] = f"HTTP {e.code}"
            return rec
    except (urllib.error.URLError, TimeoutError) as e:
        rec["status"] = None
        rec["error"] = f"network: {e}"
        return rec
    except Exception as e:
        rec["status"] = None
        rec["error"] = f"unexpected: {e}"
        return rec

    # HEAD -> 405: retry with GET
    try:
        req = urllib.request.Request(
            url, method="GET",
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            rec["status"] = resp.status
            rec["final_url"] = resp.url
            return rec
    except urllib.error.HTTPError as e:
        rec["status"] = e.code
        rec["error"] = f"HTTP {e.code}"
        return rec
    except (urllib.error.URLError, TimeoutError) as e:
        rec["status"] = None
        rec["error"] = f"network: {e}"
        return rec
    except Exception as e:
        rec["status"] = None
        rec["error"] = f"unexpected: {e}"
        return rec


def bulk_check(urls: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = {ex.submit(check_url, u): u for u in urls}
        for i, f in enumerate(cf.as_completed(futures), 1):
            u = futures[f]
            out[u] = f.result()
            if i % 50 == 0:
                print(f"  ... {i}/{len(urls)} checked")
    return out


def fetch_text(url: str, max_bytes: int = 8192) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read(max_bytes).decode("utf-8", errors="replace")
    except Exception:
        return ""


def extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return ""


def topic_keywords(entry: dict) -> list[str]:
    """Heuristic: pull therapy/method keywords from title."""
    title = (entry.get("title") or "").lower()
    # Pull 4+ char words, drop stopwords
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "into", "upon",
        "across", "living", "meta", "analysis", "methods", "study", "review",
        "using", "paper", "effect", "synthesis", "evidence", "trial", "trials",
        "pooled", "data", "dataset", "models", "model", "random", "effects",
    }
    words = re.findall(r"\b[a-z][a-z0-9-]{3,}\b", title)
    return [w for w in words if w not in stop][:6]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-dashboards", type=int, default=0,
                    help="Download up to N unique dashboards and check topic match (0 = skip)")
    args = ap.parse_args()

    entries = parse_entries_from_html()
    print(f"Visible entries on board: {len(entries)}")

    # Gather all URLs (deduplicated)
    all_urls: set[str] = set()
    per_entry_urls: list[tuple[int, str, str, str]] = []
    for e in entries:
        per_entry_urls.append((e["num"], e.get("code_url", ""),
                               e.get("protocol_url", ""), e.get("pages_url", "")))
        for u in (e.get("code_url", ""), e.get("protocol_url", ""), e.get("pages_url", "")):
            if u:
                all_urls.add(u)
    print(f"Unique URLs to check: {len(all_urls)}")

    print("Checking URLs...")
    url_results = bulk_check(sorted(all_urls))

    # Per-entry summary
    per_entry = []
    for num, code, proto, pages in per_entry_urls:
        rec = {"num": num}
        for label, url in (("code", code), ("protocol", proto), ("pages", pages)):
            if not url:
                rec[label] = {"status": None, "note": "no_url"}
            else:
                rec[label] = {"url": url, **url_results[url]}
        per_entry.append(rec)

    # Dashboard-sharing analysis
    pages_to_nums = defaultdict(list)
    code_to_nums = defaultdict(list)
    for e in entries:
        if e.get("pages_url"):
            pages_to_nums[e["pages_url"]].append(e["num"])
        if e.get("code_url"):
            code_to_nums[e["code_url"]].append(e["num"])

    shared_dashboards = {u: nums for u, nums in pages_to_nums.items() if len(nums) > 1}
    shared_code = {u: nums for u, nums in code_to_nums.items() if len(nums) > 1}

    # Dashboard content sample
    dashboard_samples = []
    if args.sample_dashboards > 0:
        # Pick the shared ones first (most at-risk), then random unique
        priority_urls = list(shared_dashboards.keys())
        other_urls = [u for u in pages_to_nums if u not in shared_dashboards]
        sample_urls = priority_urls[:args.sample_dashboards]
        if len(sample_urls) < args.sample_dashboards:
            sample_urls.extend(other_urls[:args.sample_dashboards - len(sample_urls)])
        print(f"Fetching content for {len(sample_urls)} dashboards...")
        for u in sample_urls:
            if url_results.get(u, {}).get("status") != 200:
                dashboard_samples.append({"url": u, "skipped": True, "reason": "not_200"})
                continue
            html = fetch_text(u)
            title = extract_title(html)
            # Build keyword match report
            num_list = pages_to_nums[u]
            shared = len(num_list) > 1
            per_paper_match = []
            for num in num_list:
                entry = next((e for e in entries if e["num"] == num), None)
                if not entry:
                    continue
                kws = topic_keywords(entry)
                hits = [k for k in kws if k in title.lower()]
                per_paper_match.append({
                    "num": num,
                    "paper_title": entry.get("title", ""),
                    "keywords": kws,
                    "keyword_hits_in_dashboard_title": hits,
                    "topic_match_score": len(hits) / max(len(kws), 1),
                })
            dashboard_samples.append({
                "url": u,
                "dashboard_title": title,
                "shared_by_n_papers": len(num_list),
                "is_shared": shared,
                "per_paper_match": per_paper_match,
            })

    # Aggregate counts
    def count_by_status(label: str) -> dict[str, int]:
        c: dict[str, int] = defaultdict(int)
        for rec in per_entry:
            s = rec[label].get("status")
            key = str(s) if s is not None else "NONE"
            c[key] += 1
        return dict(c)

    summary = {
        "entries_checked": len(entries),
        "unique_urls_checked": len(all_urls),
        "code_url_status_dist": count_by_status("code"),
        "protocol_url_status_dist": count_by_status("protocol"),
        "pages_url_status_dist": count_by_status("pages"),
        "shared_dashboards_count": len(shared_dashboards),
        "shared_code_repos_count": len(shared_code),
        "entries_affected_by_shared_dashboards": sum(len(v) for v in shared_dashboards.values()),
        "entries_affected_by_shared_code": sum(len(v) for v in shared_code.values()),
    }

    date_tag = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    out_json = LOG_DIR / f"board_verify_{date_tag}.json"
    out_md = LOG_DIR / f"board_verify_{date_tag}.md"

    report = {
        "summary": summary,
        "per_entry": per_entry,
        "shared_dashboards": shared_dashboards,
        "shared_code": shared_code,
        "dashboard_samples": dashboard_samples,
    }
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out_json}")
    print()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
