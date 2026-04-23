# sentinel:skip-file  (P0-hardcoded-local-path: portfolio-management script with intentional external project paths)
"""
fix_remotes.py — Fix repos pointing to wrong GitHub accounts.

Migrates remotes from mahmood789 -> mahmood726-cyber and fixes malformed URLs.
Run with --dry-run first to preview changes.

Usage:
    python fix_remotes.py --dry-run    # Preview
    python fix_remotes.py              # Apply fixes
"""

import subprocess
import sys
import io
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CORRECT_USER = "mahmood726-cyber"

# Map: local_path -> (old_remote, correct_repo_name)
# Based on deploy.log failures and NAME_OVERRIDES from push_all_repos.py
FIXES = {
    "C:/Projects/501MLM": ("https://github.com/mahmood789/MLM501.git", "mlm501"),
    "C:/Projects/MLM501": ("https://github.com/mahmood789/MLM501", "mlm501-submission"),
    "C:/Projects/Multipledatameta": ("https://github.com/mahmood789/Multipledatameta.git", "multipledatameta"),
    "C:/Projects/WorldIPD": ("https://github.com/mahmood789/-WorldIPD.git", "worldipd"),
    "C:/Projects/WorldIPD-private": ("https://github.com/mahmood789/-WorldIPD-private.git", "worldipd-private"),
    # cbamm-dev repos — leave as-is or migrate if desired
    # "C:/Projects/chat2": ("https://github.com/cbamm-dev/cbamm.git", "cbamm"),
    # "C:/Projects/chatpaper": ("https://github.com/cbamm-dev/chatpaper.git", "chatpaper"),
    # "C:/Projects/claude2": ("https://github.com/cbamm-dev/claude2.git", "claude2"),
}


def run(cmd, cwd=None, timeout=30):
    try:
        r = subprocess.run(cmd, shell=False, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "TIMEOUT"


def fix_remote(path, repo_name, dry_run=False):
    """Fix the origin remote for a repo."""
    new_url = f"https://github.com/{CORRECT_USER}/{repo_name}.git"

    # Check current remote
    rc, current, _ = run(["git", "remote", "get-url", "origin"], cwd=path)
    if rc != 0:
        print(f"  SKIP  {path} — no origin remote")
        return False

    if CORRECT_USER in current and repo_name in current.lower():
        print(f"  OK    {path} — already correct: {current}")
        return False

    if dry_run:
        print(f"  DRY   {path}")
        print(f"        FROM: {current}")
        print(f"          TO: {new_url}")
        return True

    # Create the repo on GitHub if it doesn't exist
    rc, _, err = run(["gh", "repo", "create", f"{CORRECT_USER}/{repo_name}",
                       "--public", "--description", f"Research tool: {repo_name}"],
                      cwd=path, timeout=30)
    if rc != 0 and "already exists" not in err:
        # Repo may already exist, that's fine
        pass

    # Set the new remote
    rc, _, err = run(["git", "remote", "set-url", "origin", new_url], cwd=path)
    if rc != 0:
        print(f"  FAIL  {path} — set-url failed: {err}")
        return False

    # Try pushing
    _, branch, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    branch = branch or "master"
    rc, _, err = run(["git", "push", "-u", "origin", branch], cwd=path, timeout=60)
    if rc == 0:
        print(f"  FIX   {path} -> {new_url} [pushed {branch}]")
        return True
    else:
        print(f"  FIX   {path} -> {new_url} [remote set, push failed: {err[:80]}]")
        return True


def main():
    parser = argparse.ArgumentParser(description="Fix repo remotes")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Fixing {len(FIXES)} repos (user: {CORRECT_USER})")
    if args.dry_run:
        print("DRY RUN — no changes will be made\n")

    fixed = 0
    for path, (old_remote, repo_name) in FIXES.items():
        if fix_remote(path, repo_name, dry_run=args.dry_run):
            fixed += 1

    print(f"\n{'Would fix' if args.dry_run else 'Fixed'}: {fixed}/{len(FIXES)} repos")


if __name__ == "__main__":
    main()
