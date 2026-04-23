# sentinel:skip-file  (P0-hardcoded-local-path: portfolio-management script with intentional external project paths)
"""
auto_deploy.py — Automatic E156 deployment (runs on schedule).

Detects changes since last run, syncs configs, pushes to GitHub.
Designed to run unattended via Windows Task Scheduler.

Logs to C:\E156\scripts\deploy.log
"""

import json
import os
import subprocess
import sys
import io
import hashlib
from datetime import datetime
from pathlib import Path

# UTF-8 stdout for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from apply_rewrites import parse_workbook, apply_all_configs, validate_rewrite
from generate_submission import generate_submission
from e156_utils import find_all_submissions

GH_USER = "mahmood726-cyber"
WORKBOOK = Path("C:/E156/rewrite-workbook.txt")
STATE_FILE = Path("C:/E156/scripts/.deploy_state.json")
LOG_FILE = Path("C:/E156/scripts/deploy.log")
PUSH_SCRIPT = Path("C:/Users/user/push_all_repos.py")


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def rotate_log(max_lines=5000):
    """Keep log file from growing unbounded."""
    if LOG_FILE.exists():
        lines = LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) > max_lines:
            LOG_FILE.write_text("\n".join(lines[-max_lines:]) + "\n", encoding="utf-8")


def run(cmd, cwd=None, timeout=60):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "TIMEOUT"


def get_workbook_hash():
    """Get hash of workbook to detect changes."""
    if not WORKBOOK.exists():
        return ""
    return hashlib.md5(WORKBOOK.read_bytes()).hexdigest()


def load_state():
    """Load last deployment state."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"last_hash": "", "last_run": "", "deployed_count": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def find_new_repos():
    """Find git repos without GitHub remotes (new projects)."""
    new_repos = []
    scan_dirs = [
        "C:/Models", "C:/Projects", "C:/HTML apps",
        "C:/Projects/ctgov-analyses", "C:/Projects/evidence-intelligence"
    ]
    for scan_dir in scan_dirs:
        if not os.path.isdir(scan_dir):
            continue
        for name in os.listdir(scan_dir):
            full = os.path.join(scan_dir, name)
            if not os.path.isdir(full) or name.startswith("."):
                continue
            git_dir = os.path.join(full, ".git")
            if not os.path.isdir(git_dir):
                continue
            rc, out, _ = run("git remote get-url origin", cwd=full)
            if rc != 0 or not out:
                new_repos.append(full)
    return new_repos


def push_changed_projects(entries):
    """Push projects that have uncommitted changes in e156-submission/."""
    pushed = 0
    for e in entries:
        p = Path(e["path"])
        if not p.is_dir() or not (p / ".git").is_dir():
            continue

        # Check for changes
        rc, out, _ = run("git status --porcelain e156-submission/ index.html .nojekyll", cwd=str(p))
        if rc != 0 or not out:
            continue

        # Stage, commit, push
        run("git add e156-submission/ index.html .nojekyll", cwd=str(p))
        rc, _, _ = run('git commit -m "E156 auto-deploy: sync status"', cwd=str(p))
        if rc != 0:
            continue

        # Detect branch
        _, branch, _ = run("git rev-parse --abbrev-ref HEAD", cwd=str(p))
        branch = branch or "master"

        rc, _, err = run(f"git push origin {branch}", cwd=str(p), timeout=30)
        if rc == 0:
            pushed += 1
            log(f"  Pushed: {e['name']}")
        else:
            log(f"  Push failed: {e['name']} - {err[:60]}")

    return pushed


def main():
    rotate_log()
    log("=" * 50)
    log("AUTO-DEPLOY START")

    state = load_state()
    current_hash = get_workbook_hash()
    workbook_changed = current_hash != state["last_hash"]

    if workbook_changed:
        log(f"Workbook changed (hash: {current_hash[:8]})")
    else:
        log("Workbook unchanged since last run")

    # Parse workbook
    entries = parse_workbook(str(WORKBOOK))
    submitted = [e for e in entries if e["submitted"]]
    log(f"Entries: {len(entries)}, FINAL: {len(submitted)}, DRAFT: {len(entries) - len(submitted)}")

    # Step 1: Sync all configs (author + DRAFT/FINAL)
    synced = apply_all_configs(entries)
    if synced > 0:
        log(f"Synced {synced} configs (author info + status)")

    # Step 2: Find and create new repos
    new_repos = find_new_repos()
    if new_repos:
        log(f"Found {len(new_repos)} new repos without remotes")
        rc, out, _ = run(f'"{sys.executable}" {PUSH_SCRIPT} --new-only', timeout=300)
        if rc == 0:
            log("New repos created and pushed")
        else:
            log(f"New repo push had issues: {out[:100]}")

    # Step 3: Push changed projects
    pushed = push_changed_projects(entries)
    if pushed > 0:
        log(f"Pushed {pushed} updated projects")
    else:
        log("No projects needed pushing")

    # Step 4: Push E156 repo itself if changed
    e156_dir = "C:/E156"
    rc, out, _ = run("git status --porcelain", cwd=e156_dir)
    if out:
        run("git add scripts/ templates/ rewrite-workbook.txt e156-library.html index.html", cwd=e156_dir)
        run('git commit -m "E156 auto-deploy: library + configs"', cwd=e156_dir)
        run("git push origin master", cwd=e156_dir, timeout=30)
        log("Pushed E156 repo")

    # Step 5: Push portfolio site if changed
    portfolio_dir = f"C:/{GH_USER}.github.io"
    if os.path.isdir(portfolio_dir):
        rc, out, _ = run("git status --porcelain", cwd=portfolio_dir)
        if out:
            run("git add -A", cwd=portfolio_dir)
            run('git commit -m "Portfolio auto-update"', cwd=portfolio_dir)
            run("git push origin master --force-with-lease", cwd=portfolio_dir, timeout=30)
            log("Pushed portfolio site")

    # Save state
    state["last_hash"] = current_hash
    state["last_run"] = datetime.now().isoformat()
    state["deployed_count"] = state.get("deployed_count", 0) + (1 if synced > 0 or pushed > 0 else 0)
    save_state(state)

    log(f"AUTO-DEPLOY COMPLETE (synced={synced}, pushed={pushed}, new={len(new_repos)})")
    log("=" * 50)


if __name__ == "__main__":
    main()
