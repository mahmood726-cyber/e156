"""Commit and push publication-managed changes for repos that contain E156 submissions."""

from __future__ import annotations

import os
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from e156_utils import find_all_submissions


MANAGED_PATHS = (
    "e156-submission",
    "E156-PROTOCOL.md",
    "push.sh",
    "LICENSE",
    "LICENSE.md",
    "LICENSE.txt",
    "CITATION.cff",
)

DASHBOARD_WINDOWS_REPO = r"C:\mahmood726-cyber.github.io"
GIT_NAME = os.environ.get("E156_GIT_NAME", "Mahmood Ahmad")
GIT_EMAIL = os.environ.get("E156_GIT_EMAIL", "mahmood726-cyber@users.noreply.github.com")
STAGE_TIMEOUT = int(os.environ.get("E156_GIT_STAGE_TIMEOUT", "45"))
COMMIT_TIMEOUT = int(os.environ.get("E156_GIT_COMMIT_TIMEOUT", "180"))
PUSH_TIMEOUT = int(os.environ.get("E156_GIT_PUSH_TIMEOUT", "90"))
GIT_BIN = os.environ.get("E156_GIT_BIN", "git")
POWERSHELL_EXE = Path("/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")


@dataclass
class SyncResult:
    path: Path
    state: str
    detail: str


def local_windows_path(path_str: str) -> Path:
    if os.name == "nt":
        return Path(path_str)
    drive = path_str[0].lower()
    suffix = path_str[2:].replace("\\", "/").lstrip("/")
    return Path(f"/mnt/{drive}/{suffix}")


def repo_path_for_git(path: Path) -> str:
    resolved = str(path.resolve())
    if os.name != "nt" and resolved.startswith("/mnt/") and len(resolved) > 6:
        drive = resolved[5].upper()
        suffix = resolved[6:].replace("/", "\\").lstrip("\\")
        return f"{drive}:\\{suffix}"
    return resolved


def powershell_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def run_git(path: Path, *args: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    if os.name != "nt" and POWERSHELL_EXE.exists():
        repo_dir = powershell_quote(repo_path_for_git(path))
        git_bin = powershell_quote(GIT_BIN)
        git_args = " ".join(powershell_quote(arg) for arg in args)
        command = f"Set-Location -LiteralPath {repo_dir}; & {git_bin}"
        if git_args:
            command += f" {git_args}"
        popen_args = [str(POWERSHELL_EXE), "-NoProfile", "-Command", command]
    else:
        popen_args = [GIT_BIN, "-C", repo_path_for_git(path), *args]
    process = subprocess.Popen(
        popen_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except OSError:
            pass
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                try:
                    stream.close()
                except OSError:
                    pass
        raise
    return subprocess.CompletedProcess(
        args=popen_args,
        returncode=process.returncode,
        stdout=stdout,
        stderr=stderr,
    )


def git_error(result: subprocess.CompletedProcess[str]) -> str:
    detail = (result.stderr or result.stdout or "").strip().splitlines()
    return detail[0] if detail else "git command failed"


def is_git_repo(path: Path) -> bool:
    if (path / ".git").exists():
        return True
    try:
        probe = run_git(path, "rev-parse", "--is-inside-work-tree", timeout=10)
    except subprocess.TimeoutExpired:
        return False
    return probe.returncode == 0 and probe.stdout.strip() == "true"


def current_branch(path: Path) -> str:
    try:
        probe = run_git(path, "rev-parse", "--abbrev-ref", "HEAD", timeout=10)
    except subprocess.TimeoutExpired:
        return ""
    branch = probe.stdout.strip()
    return branch if probe.returncode == 0 and branch and branch != "HEAD" else ""


def tracked_match_exists(path: Path, relative: str) -> bool:
    try:
        probe = run_git(path, "ls-files", "--", relative, timeout=10)
    except subprocess.TimeoutExpired:
        return False
    return probe.returncode == 0 and bool(probe.stdout.strip())


def normalize_repo_name(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def expected_repo_name(path: Path) -> str:
    config_path = path / "e156-submission" / "config.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            config = {}
        repo_url = str(config.get("repo_url", "")).rstrip("/")
        if repo_url:
            name = repo_url.rsplit("/", 1)[-1]
            return name[:-4] if name.endswith(".git") else name
        slug = str(config.get("slug", "")).strip()
        if slug:
            return slug
    return path.name.lower().replace(" ", "-").replace("_", "-")


def origin_repo_name(path: Path) -> str:
    try:
        probe = run_git(path, "remote", "get-url", "origin", timeout=10)
    except subprocess.TimeoutExpired:
        return ""
    if probe.returncode != 0:
        return ""
    remote = probe.stdout.strip().rstrip("/")
    if not remote:
        return ""
    if ":" in remote and not remote.startswith(("http://", "https://")):
        remote = remote.rsplit(":", 1)[-1]
    name = remote.rsplit("/", 1)[-1]
    return name[:-4] if name.endswith(".git") else name


def remote_matches_expected(path: Path) -> tuple[bool, str]:
    actual = origin_repo_name(path)
    if not actual:
        return True, ""
    expected = expected_repo_name(path)
    if normalize_repo_name(actual) == normalize_repo_name(expected):
        return True, ""
    return False, f"origin mismatch: expected {expected}, found {actual}"


def managed_paths_for(path: Path) -> list[str]:
    stage_paths: list[str] = []
    for relative in MANAGED_PATHS:
        candidate = path / relative
        if candidate.exists() or tracked_match_exists(path, relative):
            stage_paths.append(relative)
    return stage_paths


def has_preexisting_staged_changes(path: Path) -> tuple[bool, str]:
    try:
        probe = run_git(path, "diff", "--cached", "--name-only", timeout=15)
    except subprocess.TimeoutExpired:
        return False, "timed out checking staged changes"
    if probe.returncode != 0:
        return False, git_error(probe)
    staged = [line.strip() for line in probe.stdout.splitlines() if line.strip()]
    if staged:
        return True, ", ".join(staged[:5])
    return False, ""


def stage_managed_paths(path: Path) -> tuple[bool, str]:
    stage_paths = managed_paths_for(path)
    if not stage_paths:
        return False, "no managed publication paths"
    for relative in stage_paths:
        try:
            result = run_git(path, "add", "-A", "--", relative, timeout=STAGE_TIMEOUT)
        except subprocess.TimeoutExpired:
            return False, f"timed out staging {relative}"
        if result.returncode != 0:
            return False, f"{relative}: {git_error(result)}"
    return True, ", ".join(stage_paths)


def has_staged_changes(path: Path) -> tuple[bool, str]:
    try:
        probe = run_git(path, "diff", "--cached", "--quiet", "--exit-code", timeout=15)
    except subprocess.TimeoutExpired:
        return False, "timed out checking staged diff"
    if probe.returncode == 0:
        return False, ""
    if probe.returncode == 1:
        return True, ""
    return False, git_error(probe)


def commit_staged_changes(path: Path, message: str) -> tuple[bool, str]:
    try:
        result = run_git(
            path,
            "-c",
            f"user.name={GIT_NAME}",
            "-c",
            f"user.email={GIT_EMAIL}",
            "commit",
            "--no-verify",
            "--no-gpg-sign",
            "-m",
            message,
            timeout=COMMIT_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return False, "timed out during commit"
    if result.returncode != 0:
        detail = (result.stdout or result.stderr or "").strip()
        if "nothing to commit" in detail.lower():
            return True, "nothing to commit"
        return False, git_error(result)
    return True, "committed"


def push_repo(path: Path, message: str, stage_all: bool = False) -> SyncResult:
    if not is_git_repo(path):
        return SyncResult(path, "skipped", "not a git repo")

    if not stage_all:
        remote_ok, detail = remote_matches_expected(path)
        if not remote_ok:
            return SyncResult(path, "skipped", detail)

    pre_staged, detail = has_preexisting_staged_changes(path)
    if detail and not pre_staged:
        return SyncResult(path, "failed", detail)
    if pre_staged:
        return SyncResult(path, "skipped", f"pre-existing staged changes: {detail}")

    if stage_all:
        try:
            result = run_git(path, "add", "-A", timeout=STAGE_TIMEOUT)
        except subprocess.TimeoutExpired:
            return SyncResult(path, "failed", "timed out staging dashboard repo")
        if result.returncode != 0:
            return SyncResult(path, "failed", git_error(result))
    else:
        ok, detail = stage_managed_paths(path)
        if not ok:
            return SyncResult(path, "skipped", detail)

    staged, detail = has_staged_changes(path)
    if detail:
        return SyncResult(path, "failed", detail)
    if staged:
        committed, detail = commit_staged_changes(path, message)
        if not committed:
            return SyncResult(path, "failed", detail)

    branches: list[str] = []
    branch = current_branch(path)
    if branch:
        branches.append(branch)
    else:
        for candidate in ("master", "main"):
            if candidate not in branches:
                branches.append(candidate)

    last_error = ""
    for candidate in branches:
        try:
            result = run_git(path, "push", "origin", candidate, timeout=PUSH_TIMEOUT)
        except subprocess.TimeoutExpired:
            return SyncResult(path, "failed", f"timed out pushing {candidate}")
        if result.returncode == 0:
            return SyncResult(path, "synced", candidate)
        last_error = git_error(result)

    return SyncResult(path, "failed", last_error if last_error else "push failed")


FAILED_QUEUE_FILE = SCRIPT_DIR / ".push_failures.json"
MAX_RETRIES = 2


def load_failed_queue() -> list[dict]:
    if FAILED_QUEUE_FILE.exists():
        try:
            return json.loads(FAILED_QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def save_failed_queue(queue: list[dict]) -> None:
    FAILED_QUEUE_FILE.write_text(json.dumps(queue, indent=2, default=str), encoding="utf-8")


def main() -> None:
    dashboard_repo = local_windows_path(DASHBOARD_WINDOWS_REPO)
    repos = sorted({submission_dir.parent for submission_dir in find_all_submissions()} - {dashboard_repo})
    results: list[SyncResult] = []
    failed_queue = load_failed_queue()
    new_failures: list[dict] = []

    # Retry previously failed repos first
    retry_paths = {item["path"] for item in failed_queue if item.get("retries", 0) < MAX_RETRIES}
    if retry_paths:
        print(f"Retrying {len(retry_paths)} previously failed repos...", flush=True)

    for repo in repos:
        result = push_repo(repo, "Auto-sync E156 submission")
        results.append(result)
        if result.state == "synced":
            print(f"SYNCED {repo} [{result.detail}]", flush=True)
        elif result.state == "failed":
            print(f"FAILED {repo} [{result.detail}]", flush=True)
            # Track failure for retry
            prev = next((item for item in failed_queue if item["path"] == str(repo)), None)
            retries = (prev["retries"] + 1) if prev else 0
            new_failures.append({
                "path": str(repo),
                "error": result.detail,
                "retries": retries,
                "last_attempt": str(datetime.now()) if "datetime" in dir() else "",
            })

    dashboard = push_repo(dashboard_repo, "Auto-sync dashboard", stage_all=True)
    results.append(dashboard)
    if dashboard.state == "synced":
        print(f"SYNCED {dashboard_repo} [{dashboard.detail}]", flush=True)
    elif dashboard.state == "failed":
        print(f"FAILED {dashboard_repo} [{dashboard.detail}]", flush=True)

    synced = sum(1 for result in results if result.state == "synced")
    skipped = sum(1 for result in results if result.state == "skipped")
    failed = sum(1 for result in results if result.state == "failed")
    print(f"Processed {len(repos)} submission repos (+ dashboard).", flush=True)
    print(f"Synced {synced}, skipped {skipped}, failed {failed}.", flush=True)

    # Save failed queue (only repos that still fail after retries)
    save_failed_queue(new_failures)
    if new_failures:
        print(f"\n{len(new_failures)} repos queued for retry (max {MAX_RETRIES} retries):", flush=True)
        for item in new_failures:
            exceeded = " [MAX RETRIES - needs manual fix]" if item["retries"] >= MAX_RETRIES else ""
            print(f"  {item['path']}: {item['error']}{exceeded}", flush=True)


if __name__ == "__main__":
    from datetime import datetime
    main()
