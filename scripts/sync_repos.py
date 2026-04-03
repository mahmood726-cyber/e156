"""Commit and push all repos that contain E156 submissions, plus the dashboard repo."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from e156_utils import find_all_submissions


DASHBOARD_REPO = Path(r"C:\mahmood726-cyber.github.io")


def is_git_repo(path: Path) -> bool:
    if (path / ".git").exists():
        return True
    probe = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    return probe.returncode == 0 and probe.stdout.strip() == "true"


def current_branch(path: Path) -> str:
    probe = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    branch = probe.stdout.strip()
    return branch if probe.returncode == 0 and branch and branch != "HEAD" else ""


def push_repo(path: Path, message: str) -> tuple[bool, str]:
    if not is_git_repo(path):
        return False, "not a git repo"

    subprocess.run(["git", "-C", str(path), "add", "-A"], check=False, capture_output=True)
    status = subprocess.run(
        ["git", "-C", str(path), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if status.returncode != 0:
        return False, "git status failed"

    if status.stdout.strip():
        subprocess.run(
            ["git", "-C", str(path), "commit", "-m", message],
            check=False,
            capture_output=True,
            text=True,
        )

    branches = []
    branch = current_branch(path)
    if branch:
        branches.append(branch)
    for candidate in ("master", "main"):
        if candidate not in branches:
            branches.append(candidate)

    for candidate in branches:
        result = subprocess.run(
            ["git", "-C", str(path), "push", "origin", candidate],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return True, candidate

    return False, "push failed"


def main() -> None:
    repos = sorted({submission_dir.parent for submission_dir in find_all_submissions()})
    synced = 0

    for repo in repos:
        ok, detail = push_repo(repo, "Auto-sync E156 submission")
        if ok:
            synced += 1
            print(f"SYNCED {repo} [{detail}]")

    ok, detail = push_repo(DASHBOARD_REPO, "Auto-sync dashboard")
    if ok:
        print(f"SYNCED {DASHBOARD_REPO} [{detail}]")

    print(f"Processed {len(repos)} submission repos.")


if __name__ == "__main__":
    main()
