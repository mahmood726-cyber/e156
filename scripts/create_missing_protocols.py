"""Track 1 — create missing E156-PROTOCOL.md files via GitHub API.

For each board entry whose protocol_url returned 404, build a protocol
document from the workbook's SUBMISSION METADATA block and PUT it into
the repo via `gh api -X PUT /repos/:owner/:repo/contents/E156-PROTOCOL.md`.

De-dupes by repo: if N papers all share one repo (e.g., 17 Finrenone
aliases share rapidmeta-finerenone), the protocol file references ALL N
paper nums and titles, and is created once.

Writes audit_output/protocol_create_log_<date>.jsonl with per-repo result.
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import io
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
STUDENTS_HTML = E156 / "students.html"
VERIFY_JSON = E156 / "audit_output" / f"board_verify_{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.json"
LOG_DIR = E156 / "audit_output"

SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
CODE_URL_RE = re.compile(r"https://github\.com/([^/]+)/([^/\s]+)")


def parse_workbook() -> dict[int, dict]:
    """Return {num: {title, name, body, metadata_block}} for every entry."""
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)
    out: dict[int, dict] = {}
    for block in blocks:
        m = ENTRY_HEAD_RE.search(block)
        if not m:
            continue
        num = int(m.group(1))
        if num in out:  # keep first
            continue
        name = m.group(2).strip()
        title_m = re.search(r"TITLE:\s*(.+)", block)
        type_m = re.search(r"TYPE:\s*(.+)", block)
        data_m = re.search(r"DATA:\s*(.+)", block)
        body_m = re.search(r"CURRENT BODY[^\n]*\n+(.+?)(?:\n\n|YOUR REWRITE)", block, re.DOTALL)
        code_m = re.search(r"Code:\s+(\S+)", block)
        # SUBMISSION METADATA block: from "SUBMISSION METADATA:" to end of block
        sub_m = re.search(r"SUBMISSION METADATA:\s*\n(.+)", block, re.DOTALL)
        out[num] = {
            "num": num,
            "name": name,
            "title": title_m.group(1).strip() if title_m else name,
            "type": type_m.group(1).strip() if type_m else "",
            "data": data_m.group(1).strip() if data_m else "",
            "body": body_m.group(1).strip() if body_m else "",
            "code_url": code_m.group(1).strip() if code_m else "",
            "submission_metadata": sub_m.group(1).strip() if sub_m else "",
        }
    return out


def load_404_entry_nums() -> list[int]:
    if not VERIFY_JSON.exists():
        raise RuntimeError(f"{VERIFY_JSON} not found — run verify_board_links.py first")
    r = json.loads(VERIFY_JSON.read_text(encoding="utf-8"))
    nums = [e["num"] for e in r["per_entry"] if e["protocol"].get("status") == 404]
    return nums


def build_protocol_md(repo: str, entries: list[dict]) -> str:
    """Compose a PROTOCOL.md that lists every paper sharing this repo,
    followed by the full SUBMISSION METADATA block of each.
    """
    header = [
        f"# E156 Protocol — `{repo}`",
        "",
        f"This repository is the source code and dashboard backing "
        f"{'an' if len(entries) == 1 else 'a cluster of'} E156 micro-paper"
        f"{'s' if len(entries) != 1 else ''} on the "
        "[E156 Student Board](https://mahmood726-cyber.github.io/e156/students.html).",
        "",
    ]
    if len(entries) > 1:
        header.append(
            f"**{len(entries)} papers share this repo.** Each is listed below "
            f"with its own title, estimand, dataset, 156-word body, and "
            f"submission metadata (authorship, ethics, references, target "
            f"journal, etc.). Students claiming any of these papers should "
            f"use the body + metadata for their specific paper number and "
            f"submit separately.",
        )
        header.append("")
        header.append("## Papers in this repo")
        header.append("")
        header.append("| Paper # | Title |")
        header.append("| ---: | :--- |")
        for e in entries:
            header.append(f"| `[{e['num']}]` | {e['title']} |")
        header.append("")
    sections = ["\n".join(header)]

    for e in entries:
        sections.append(f"---\n\n## `[{e['num']}]` {e['title']}\n")
        sections.append(f"**Type:** {e['type']}  \n**Data:** {e['data']}\n")
        if e["body"]:
            sections.append("### 156-word body\n")
            sections.append(e["body"])
            sections.append("")
        if e["submission_metadata"]:
            sections.append("### Submission metadata\n")
            sections.append("```")
            sections.append(e["submission_metadata"])
            sections.append("```")
            sections.append("")

    sections.append("\n---\n")
    sections.append(
        "_Auto-generated from the workbook by "
        "`C:/E156/scripts/create_missing_protocols.py`. If something is "
        "wrong, edit `rewrite-workbook.txt` and re-run the script — it "
        "will overwrite this file via the GitHub API._"
    )
    return "\n".join(sections)


def gh_default_branch(owner: str, repo: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["gh", "api", f"repos/{owner}/{repo}", "--jq", ".default_branch"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        return out or None
    except subprocess.CalledProcessError:
        return None


def gh_put_file(owner: str, repo: str, path: str, content: str,
                branch: str, message: str) -> dict:
    """PUT via stdin to dodge Windows' ~32k command-line limit on `-f content=...`."""
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    body = json.dumps({"message": message, "content": b64, "branch": branch})
    cmd = [
        "gh", "api", "-X", "PUT",
        f"/repos/{owner}/{repo}/contents/{path}",
        "--input", "-",
    ]
    r = subprocess.run(cmd, input=body, capture_output=True, text=True)
    if r.returncode != 0:
        return {"ok": False, "stderr": r.stderr.strip()[:400],
                "stdout": r.stdout.strip()[:400]}
    try:
        data = json.loads(r.stdout)
        return {"ok": True, "commit_sha": data.get("commit", {}).get("sha"),
                "html_url": data.get("content", {}).get("html_url")}
    except json.JSONDecodeError:
        return {"ok": False, "stderr": "unparseable response",
                "stdout": r.stdout[:400]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None,
                    help="Cap repos processed this run (for canary)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    workbook = parse_workbook()
    nums_404 = load_404_entry_nums()
    print(f"Missing-protocol entries: {len(nums_404)}")

    # Group entries by (owner, repo)
    by_repo: dict[tuple[str, str], list[dict]] = defaultdict(list)
    unroutable: list[int] = []
    for num in nums_404:
        entry = workbook.get(num)
        if not entry:
            unroutable.append(num)
            continue
        m = CODE_URL_RE.match(entry["code_url"])
        if not m:
            unroutable.append(num)
            continue
        owner, repo = m.group(1), m.group(2)
        by_repo[(owner, repo)].append(entry)
    print(f"Unique repos to write: {len(by_repo)}")
    print(f"Unroutable (no workbook entry or no code URL): {len(unroutable)}")

    # Sort each group's entries by paper num for stable output
    for k in by_repo:
        by_repo[k].sort(key=lambda e: e["num"])

    date_tag = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"protocol_create_log_{date_tag}.jsonl"

    # Resume support: skip repos already in the log (any status)
    done_keys: set[tuple[str, str]] = set()
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                done_keys.add((r["owner"], r["repo"]))
            except Exception:
                pass
    if done_keys:
        print(f"Resume: skipping {len(done_keys)} repos already in log")

    targets = [kv for kv in by_repo.items() if kv[0] not in done_keys]
    if args.limit is not None:
        targets = targets[:args.limit]

    ok = 0
    skipped = 0
    failed = 0
    consecutive_fails = 0
    for i, ((owner, repo), entries) in enumerate(targets, 1):
        rec = {
            "owner": owner, "repo": repo,
            "entry_nums": [e["num"] for e in entries],
            "started": dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        }
        if args.dry_run:
            rec["action"] = "dry_run"
            rec["protocol_preview_bytes"] = len(build_protocol_md(repo, entries))
            ok += 1
            print(f"  [{i:3d}/{len(targets)}] DRY  {owner}/{repo}  papers={[e['num'] for e in entries]}  bytes≈{rec['protocol_preview_bytes']}")
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            continue

        default_branch = gh_default_branch(owner, repo)
        if not default_branch:
            rec["status"] = "SKIP_no_default_branch"
            skipped += 1
            print(f"  [{i:3d}/{len(targets)}] SKIP {owner}/{repo}  (couldn't resolve default branch)")
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            continue
        rec["default_branch"] = default_branch

        md = build_protocol_md(repo, entries)
        result = gh_put_file(
            owner, repo, "E156-PROTOCOL.md", md, default_branch,
            message=f"Add E156 protocol for paper{'s' if len(entries) > 1 else ''} #"
                    + ",".join(str(e["num"]) for e in entries),
        )
        rec["api_result"] = result
        if result["ok"]:
            rec["status"] = "OK"
            ok += 1
            consecutive_fails = 0
            marker = "OK  "
        else:
            # Detect 'already exists' (422) and 409 — treat as skip not fail
            stderr = result.get("stderr", "")
            if "sha" in stderr or "already exists" in stderr.lower() or "422" in stderr:
                rec["status"] = "SKIP_already_exists"
                skipped += 1
                marker = "SKIP"
            else:
                rec["status"] = "FAIL"
                failed += 1
                consecutive_fails += 1
                marker = "FAIL"
        print(f"  [{i:3d}/{len(targets)}] {marker} {owner}/{repo}  papers={[e['num'] for e in entries]}")
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if consecutive_fails >= 5:
            print(f"\nSTOPPED: {consecutive_fails} consecutive failures. Investigate before resuming.")
            break

    print()
    print(f"Summary: {ok} ok, {skipped} skipped, {failed} failed, {len(targets)} attempted")
    print(f"Log: {log_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
