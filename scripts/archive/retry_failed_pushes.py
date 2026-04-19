"""Retry push targets that failed on the first pass.

Picks failure records out of the current day's push_log, re-attempts each
one. For records whose status is FAIL_gh_create_push, the repo was already
created on GitHub — retry only the `git push -u origin main` step (don't
re-run gh repo create, which would fail with "name already exists").

For all other failures, re-run the full push_one pipeline.
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

from apply_fresh_pushes import push_one, run  # reuse pipeline

E156 = Path(__file__).resolve().parents[1]
LOG_DIR = E156 / "audit_output"


def retry_push_only(target: dict) -> dict:
    """gh repo create already succeeded; retry the push step."""
    source = Path(target["source_path"])
    rec = {
        "target": target["target_repo"],
        "source_path": str(source),
        "entry_nums": target["entry_nums"],
        "started": dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "mode": "push_only",
    }
    r = run(["git", "push", "-u", "origin", "main"], cwd=source, check=False)
    if r.returncode != 0:
        rec["status"] = "FAIL_git_push"
        rec["stderr"] = r.stderr.strip()[:600]
        return rec
    rec["status"] = "OK"
    rec["gh_url"] = f"https://github.com/mahmood726-cyber/{target['target_repo']}"
    return rec


def main() -> int:
    date_tag = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"push_log_{date_tag}.jsonl"
    retry_log = LOG_DIR / f"push_retry_log_{date_tag}.jsonl"

    # Collect all FAIL records, dedupe on target (keep the most recent fail
    # so that any earlier partial failures are overridden by the latest).
    failures: dict[str, dict] = {}
    for line in log_path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["status"].startswith("FAIL"):
            failures[r["target"]] = r

    print(f"Retrying {len(failures)} failed targets")
    print(f"Retry log: {retry_log}")
    print()

    for target_name, orig_rec in failures.items():
        fake_target = {
            "target_repo": orig_rec["target"],
            "source_path": orig_rec["source_path"],
            "entry_nums": orig_rec["entry_nums"],
        }
        if orig_rec["status"] == "FAIL_gh_create_push":
            rec = retry_push_only(fake_target)
        else:
            rec = push_one(fake_target, dry_run=False)
        status = rec["status"]
        marker = "OK  " if status == "OK" else "FAIL"
        print(f"  {marker}  {rec['target']:40s}  {status}")
        with retry_log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
