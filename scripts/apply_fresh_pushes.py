"""Phase B: push 55 fresh targets to new GitHub repos.

For each target in push_plan.json where:
  - has_remote_already is NOT in flags (not an alias)
  - target_repo != 'hfpef_registry_calibration' (2.3 GB, hits 100MB limit)

Do:
  1. Merge a shared .gitignore into source_path (preserve existing patterns).
  2. `git init -b main` inside source_path.
  3. `git add .` then check staged size; skip if any single file > 95 MB
     (GitHub hard-fails at 100 MB and complains above 50 MB).
  4. `git commit -m "Initial commit — E156 paper #N"`.
  5. `gh repo create mahmood726-cyber/<target> --public --source=. --remote=origin --push`.
  6. Log result to audit_output/push_log_<date>.jsonl.

Batching: --limit N, stop on 3 consecutive failures.
Resume: --start-at IDX (0-indexed into the push list).
Dry-run: --dry-run prints planned actions only.

Removing pushed nums from hide_repo_404.json is done in a SEPARATE pass
(scripts/unhide_after_push.py) so a partial push run doesn't half-update
the hide list.
"""
from __future__ import annotations
import argparse
import datetime as dt
import io
import json
import subprocess
import sys
from pathlib import Path

def _ensure_utf8_stdout() -> None:
    """Idempotent UTF-8 stdout wrap. Called from main() only (NOT at import)
    so that importing this module from another script doesn't clobber the
    caller's stdout. (See lessons.md: module-level stdout reassignment
    breaks pytest capture and import-time prints elsewhere.)
    """
    if sys.platform == "win32" and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
PUSH_PLAN = E156 / "audit_output" / "push_plan.json"
LOG_DIR = E156 / "audit_output"
GITHUB_USER = "mahmood726-cyber"

DEFER_BY_NAME = {
    "hfpef_registry_calibration",  # 2.3 GB, hits 100MB file limit
}
MAX_FILE_BYTES = 95 * 1024 * 1024  # GitHub rejects > 100 MB per file

GITIGNORE_TEMPLATE = """# E156 shared baseline — merged by apply_fresh_pushes.py

# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.venv/
venv/
env/
.env

# Node
node_modules/
dist/
build/
.next/
.nuxt/
out/

# OS / IDE
.DS_Store
Thumbs.db
desktop.ini
.vscode/
.idea/
*.swp
*.swo

# Session checkpoints (see C:\\Users\\user\\.claude\\rules\\rules.md)
PROGRESS.md

# Local agent config
.claude/
CLAUDE.local.md
"""


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command, return CompletedProcess. Never raise on check=False."""
    return subprocess.run(
        cmd, cwd=str(cwd) if cwd else None,
        capture_output=True, text=True, check=check,
    )


def merge_gitignore(source: Path) -> str:
    """Write or merge .gitignore. Return 'created', 'merged', or 'unchanged'."""
    gi = source / ".gitignore"
    if not gi.exists():
        gi.write_text(GITIGNORE_TEMPLATE, encoding="utf-8")
        return "created"
    existing = gi.read_text(encoding="utf-8", errors="replace")
    needed = [
        "__pycache__/", "*.py[cod]", ".venv/", "node_modules/",
        "dist/", "build/", ".DS_Store", "Thumbs.db", "PROGRESS.md",
    ]
    missing = [p for p in needed if p not in existing]
    if not missing:
        return "unchanged"
    block = "\n# E156 baseline additions\n" + "\n".join(missing) + "\n"
    gi.write_text(existing.rstrip() + "\n" + block, encoding="utf-8")
    return "merged"


def check_oversize_files(source: Path) -> list[str]:
    """Return list of relative paths of files > MAX_FILE_BYTES.

    Skips unreadable entries (broken symlinks, WinError 1920 on venv
    junction points) rather than aborting the whole target.
    """
    big = []
    try:
        iterator = source.rglob("*")
    except OSError:
        return big
    while True:
        try:
            sub = next(iterator)
        except StopIteration:
            break
        except OSError:
            continue
        try:
            if ".git" in sub.parts:
                continue
            if sub.is_file():
                size = sub.stat().st_size
                if size > MAX_FILE_BYTES:
                    big.append(str(sub.relative_to(source)))
        except OSError:
            continue
    return big


def push_one(target: dict, dry_run: bool) -> dict:
    source = Path(target["source_path"])
    name = target["target_repo"]
    nums = target["entry_nums"]
    rec = {
        "target": name,
        "source_path": str(source),
        "entry_nums": nums,
        "started": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    if not source.is_dir():
        rec["status"] = "FAIL_source_missing"
        return rec

    # Check oversize files up front — saves us from a failed push late
    big_files = check_oversize_files(source)
    if big_files:
        rec["status"] = "SKIP_oversize_files"
        rec["big_files"] = big_files[:5]
        rec["big_files_truncated_at"] = 5 if len(big_files) > 5 else None
        return rec

    rec["gitignore"] = merge_gitignore(source)

    if dry_run:
        rec["status"] = "DRY_RUN"
        return rec

    # git init
    r = run(["git", "init", "-b", "main"], cwd=source, check=False)
    if r.returncode != 0:
        rec["status"] = "FAIL_git_init"
        rec["stderr"] = r.stderr.strip()
        return rec

    # git add
    r = run(["git", "add", "."], cwd=source, check=False)
    if r.returncode != 0:
        rec["status"] = "FAIL_git_add"
        rec["stderr"] = r.stderr.strip()
        return rec

    # Check if anything was staged
    r = run(["git", "diff", "--cached", "--stat"], cwd=source, check=False)
    if r.returncode != 0 or not r.stdout.strip():
        rec["status"] = "FAIL_nothing_staged"
        rec["stderr"] = r.stderr.strip() or "empty stage"
        return rec

    # commit
    msg = f"Initial commit — E156 paper #{','.join(map(str, nums))}"
    r = run(["git", "commit", "-m", msg], cwd=source, check=False)
    if r.returncode != 0:
        rec["status"] = "FAIL_git_commit"
        rec["stderr"] = r.stderr.strip()
        return rec

    # gh repo create + push
    r = run(
        ["gh", "repo", "create", f"{GITHUB_USER}/{name}",
         "--public", "--source=.", "--remote=origin", "--push"],
        cwd=source, check=False,
    )
    if r.returncode != 0:
        rec["status"] = "FAIL_gh_create_push"
        rec["stderr"] = r.stderr.strip()
        rec["stdout"] = r.stdout.strip()
        return rec

    rec["status"] = "OK"
    rec["gh_url"] = f"https://github.com/{GITHUB_USER}/{name}"
    rec["finished"] = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    return rec


def main() -> int:
    _ensure_utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--start-at", type=int, default=0,
                    help="0-indexed offset into the push list")
    ap.add_argument("--limit", type=int, default=None,
                    help="max number of targets to attempt this run")
    ap.add_argument("--stop-on-consecutive-failures", type=int, default=3)
    args = ap.parse_args()

    plan = json.loads(PUSH_PLAN.read_text(encoding="utf-8"))
    fresh = [
        t for t in plan["targets"]
        if "has_remote_already" not in t.get("flags", [])
        and t["target_repo"] not in DEFER_BY_NAME
    ]
    fresh.sort(key=lambda t: t["target_repo"].lower())

    todo = fresh[args.start_at:]
    if args.limit is not None:
        todo = todo[:args.limit]

    date_tag = dt.datetime.utcnow().strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"push_log_{date_tag}.jsonl"

    print(f"Fresh-push universe: {len(fresh)} targets")
    print(f"This run:            {len(todo)} (offset {args.start_at}, limit {args.limit})")
    print(f"Log:                 {log_path}")
    print(f"Dry run:             {args.dry_run}")
    print()

    results = []
    consecutive_fails = 0
    for i, t in enumerate(todo, start=args.start_at):
        rec = push_one(t, args.dry_run)
        results.append(rec)
        status = rec["status"]
        marker = "OK  " if status == "OK" or status == "DRY_RUN" else "FAIL"
        print(f"  [{i:3d}] {marker}  {rec['target']:35s}  {status}")
        # Append to log
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if status.startswith("FAIL"):
            consecutive_fails += 1
            if consecutive_fails >= args.stop_on_consecutive_failures:
                print(f"\nSTOPPED: {consecutive_fails} consecutive failures. Fix and resume.")
                break
        else:
            consecutive_fails = 0

    ok = sum(1 for r in results if r["status"] in ("OK", "DRY_RUN"))
    fail = sum(1 for r in results if r["status"].startswith("FAIL"))
    skip = sum(1 for r in results if r["status"].startswith("SKIP"))
    print(f"\nDone: {ok} ok, {fail} fail, {skip} skip, {len(results)} total")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
