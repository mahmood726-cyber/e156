"""Track 2 — enable GitHub Pages for the 182 repos whose Pages URL 404'd.

For each entry with pages_url 404:
  - Extract repo name from pages_url (github.io/<repo-lower>/)
  - Confirm the repo has something to serve (index.html or /docs/index.html
    on the default branch) — otherwise enabling Pages gives a 404 page.
  - `gh api -X POST /repos/:owner/:repo/pages` with source = main / root
    (or /docs if that's where index.html lives).

Idempotent: skips repos that already have Pages enabled (409 response).

Writes audit_output/pages_enable_log_<date>.jsonl.
"""
from __future__ import annotations
import datetime as dt
import io
import json
import re
import subprocess
import sys
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
VERIFY_JSON = E156 / "audit_output" / f"board_verify_{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.json"
STUDENTS_HTML = E156 / "students.html"
LOG_DIR = E156 / "audit_output"
OWNER = "mahmood726-cyber"

PAGES_URL_RE = re.compile(rf"https://{re.escape(OWNER)}\.github\.io/([^/]+)/?")


def load_repos_needing_pages() -> list[dict]:
    """Get the actual repo name from code_url for every entry with pages 404.

    pages_url's path segment is lowercase by convention; the real repo name
    (which the Pages API needs) comes from code_url.
    """
    r = json.loads(VERIFY_JSON.read_text(encoding="utf-8"))
    # Build num -> code_url map from students.html
    html = STUDENTS_HTML.read_text(encoding="utf-8")
    m = re.search(r"const ENTRIES\s*=\s*(\[.*?\]);", html, re.DOTALL)
    entries = {e["num"]: e for e in json.loads(m.group(1))}

    out: dict[str, list[int]] = {}
    for e in r["per_entry"]:
        if e["pages"].get("status") != 404:
            continue
        num = e["num"]
        entry = entries.get(num)
        if not entry or not entry.get("code_url"):
            continue
        m = re.match(r"https://github\.com/[^/]+/([^/\s]+)", entry["code_url"])
        if not m:
            continue
        repo = m.group(1)
        out.setdefault(repo, []).append(num)
    return [{"repo": r, "paper_nums": sorted(nums)} for r, nums in sorted(out.items())]


def repo_has_index(repo: str, default_branch: str) -> tuple[bool, str]:
    """Returns (has_index, source_path). source_path is '/' or '/docs'."""
    for path in ("/", "/docs"):
        lookup = "index.html" if path == "/" else "docs/index.html"
        r = subprocess.run(
            ["gh", "api", f"repos/{OWNER}/{repo}/contents/{lookup}",
             "--jq", ".type"],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and r.stdout.strip() == "file":
            return True, path
    return False, "/"


def get_default_branch(repo: str) -> str | None:
    r = subprocess.run(
        ["gh", "api", f"repos/{OWNER}/{repo}", "--jq", ".default_branch"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def enable_pages(repo: str, branch: str, path: str) -> dict:
    cmd = [
        "gh", "api", "-X", "POST",
        f"/repos/{OWNER}/{repo}/pages",
        "-f", f"source[branch]={branch}",
        "-f", f"source[path]={path}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        try:
            data = json.loads(r.stdout)
            return {"ok": True, "url": data.get("html_url"), "source": data.get("source")}
        except json.JSONDecodeError:
            return {"ok": True, "raw": r.stdout[:400]}
    stderr = r.stderr.strip()
    # 409 = already enabled; 422 = validation (e.g., no content)
    status_hint = None
    if "409" in stderr or "already" in stderr.lower():
        status_hint = "already_enabled"
    elif "422" in stderr:
        status_hint = "validation_error"
    return {"ok": False, "stderr": stderr[:400], "hint": status_hint}


def main() -> int:
    repos = load_repos_needing_pages()
    print(f"Repos needing Pages: {len(repos)}")

    date_tag = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"pages_enable_log_{date_tag}.jsonl"

    ok = 0
    already = 0
    no_content = 0
    failed = 0

    for i, item in enumerate(repos, 1):
        repo = item["repo"]
        rec = {"repo": repo, "paper_nums": item["paper_nums"],
               "started": dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")}
        branch = get_default_branch(repo)
        if not branch:
            rec["status"] = "FAIL_no_default_branch"
            failed += 1
            print(f"  [{i:3d}/{len(repos)}] FAIL {repo}  (no default branch)")
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            continue
        rec["default_branch"] = branch

        has_index, source_path = repo_has_index(repo, branch)
        rec["has_index"] = has_index
        rec["source_path"] = source_path
        if not has_index:
            rec["status"] = "SKIP_no_index_html"
            no_content += 1
            print(f"  [{i:3d}/{len(repos)}] SKIP {repo}  (no index.html in / or /docs)")
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            continue

        result = enable_pages(repo, branch, source_path)
        rec["api_result"] = result
        if result["ok"]:
            rec["status"] = "OK"
            ok += 1
            marker = "OK  "
        elif result.get("hint") == "already_enabled":
            rec["status"] = "ALREADY_ENABLED"
            already += 1
            marker = "ALR "
        else:
            rec["status"] = "FAIL"
            failed += 1
            marker = "FAIL"
        print(f"  [{i:3d}/{len(repos)}] {marker} {repo}  branch={branch} path={source_path} papers={item['paper_nums']}")
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        # Gentle throttle
        time.sleep(0.25)

    print()
    print(f"Summary: {ok} enabled, {already} already, {no_content} no_index, {failed} failed, {len(repos)} total")
    print(f"Log: {log_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
