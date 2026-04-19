"""Final un-hide: push the 6 cross-owner repos to mahmood726-cyber.

Each local dir already has a .git with a non-mahmood726-cyber remote
(mahmood789 / cbamm-dev / jayded — all the user's own accounts, confirmed).
Add `mahmood726-cyber/<target>` as a new remote and push there. Preserves
the existing `origin` pointing to the original account (so upstream sync
still works) — adds a second remote named `mine` for the new destination.

Then the workbook's Code URL (already `mahmood726-cyber/<target>`) resolves
to a real repo, and the paper un-hides.

For the 3 local-missing + #252 hfpef (2.3GB): handled separately via a
workbook URL rewrite to the E156 paper info page — not this script.
"""
from __future__ import annotations
import datetime as dt
import io
import json
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
GITHUB_USER = "mahmood726-cyber"
LOG = E156 / "audit_output" / "cross_owner_push_log.jsonl"

# (paper_num, source_local_dir, desired_repo_name_on_mahmood726-cyber)
TARGETS = [
    (1,   r"C:\Projects\501MLM",             "501MLM"),
    (18,  r"C:\Projects\chat2",              "chat2"),
    (19,  r"C:\Projects\chatpaper",          "chatpaper"),
    (20,  r"C:\Projects\claude2",            "claude2"),
    (51,  r"C:\Projects\evidence-inference", "evidence-inference"),
    (146, r"C:\Projects\repo100",            "repo100"),
]


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None,
                          capture_output=True, text=True)


def push_one(num: int, source: str, name: str) -> dict:
    p = Path(source)
    rec = {"num": num, "source": source, "target_name": name}
    if not p.is_dir():
        rec["status"] = "FAIL_no_source"; return rec

    # 1. Create the repo on mahmood726-cyber (empty).
    r = run(["gh", "repo", "create", f"{GITHUB_USER}/{name}",
             "--public", "--description", f"E156 paper #{num} — source code"])
    if r.returncode != 0 and "already exists" not in r.stderr.lower():
        rec["status"] = "FAIL_gh_create"
        rec["stderr"] = r.stderr.strip()[:300]
        return rec
    rec["create_stderr"] = r.stderr.strip()[:200]

    # 2. Ensure local is a git dir (should be, all 6 are).
    if not (p / ".git").is_dir():
        rec["status"] = "FAIL_no_git"; return rec

    new_url = f"https://github.com/{GITHUB_USER}/{name}.git"
    # 3. Add/update `mine` remote.
    r = run(["git", "remote", "remove", "mine"], cwd=p)
    r = run(["git", "remote", "add", "mine", new_url], cwd=p)
    if r.returncode != 0:
        rec["status"] = "FAIL_remote_add"
        rec["stderr"] = r.stderr.strip()[:300]
        return rec

    # 4. Pick default branch.
    r = run(["git", "branch", "--show-current"], cwd=p)
    branch = r.stdout.strip() or "main"
    rec["branch"] = branch

    # 5. Push to mine.
    r = run(["git", "push", "mine", branch], cwd=p)
    if r.returncode != 0:
        # Try master if main failed
        if branch == "main":
            r = run(["git", "push", "mine", "master"], cwd=p)
            branch = "master" if r.returncode == 0 else branch
        if r.returncode != 0:
            rec["status"] = "FAIL_push"
            rec["stderr"] = r.stderr.strip()[:400]
            return rec

    # 6. Set default branch on GitHub if needed
    run(["gh", "api", "-X", "PATCH", f"/repos/{GITHUB_USER}/{name}",
         "-f", f"default_branch={branch}"])

    rec["status"] = "OK"
    rec["url"] = f"https://github.com/{GITHUB_USER}/{name}"
    return rec


def main() -> int:
    ok = 0
    for num, source, name in TARGETS:
        rec = push_one(num, source, name)
        status = rec["status"]
        print(f"  [#{num:3d}] {status:20s} {name:25s} {source}")
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if status == "OK":
            ok += 1
    print(f"\nSummary: {ok}/{len(TARGETS)} pushed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
