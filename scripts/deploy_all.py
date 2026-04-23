# sentinel:skip-file  (P0-hardcoded-local-path: portfolio-management script with intentional external project paths)
"""
deploy_all.py — Master E156 deployment pipeline.

Reads the rewrite-workbook, syncs DRAFT/FINAL status, regenerates HTML,
pushes to GitHub, and enables Pages. One command to deploy everything.

Usage:
    python deploy_all.py                    # Dry run (validate only)
    python deploy_all.py --deploy           # Full deploy
    python deploy_all.py --deploy --push    # Deploy + push to GitHub
    python deploy_all.py --status           # Show DRAFT/FINAL counts
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from apply_rewrites import parse_workbook, validate_rewrite, apply_all_configs
from generate_submission import generate_submission
from build_library import build as build_library
from e156_utils import find_all_submissions

GH_USER = "mahmood726-cyber"
WORKBOOK = Path("C:/E156/rewrite-workbook.txt")
PUSH_SCRIPT = Path("C:/Users/user/push_all_repos.py")


def run(cmd, cwd=None, timeout=60):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "TIMEOUT"


def show_status(entries):
    """Show DRAFT vs FINAL status summary."""
    submitted = [e for e in entries if e["submitted"]]
    draft = [e for e in entries if not e["submitted"]]
    has_rewrite = [e for e in entries if e["rewrite"]]

    print(f"\n{'=' * 60}")
    print(f"E156 WORKBOOK STATUS — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'=' * 60}")
    print(f"  Total entries:     {len(entries)}")
    print(f"  With rewrites:     {len(has_rewrite)}")
    print(f"  SUBMITTED (FINAL): {len(submitted)}")
    print(f"  DRAFT:             {len(draft)}")
    print(f"{'=' * 60}")

    if submitted:
        print(f"\nFINAL papers ({len(submitted)}):")
        for e in submitted:
            print(f"  [x] {e['name']}")

    # Count projects with e156-submission/config.json
    configured = 0
    for e in entries:
        cfg = Path(e["path"]) / "e156-submission" / "config.json"
        if cfg.exists():
            configured += 1
    print(f"\n  With E156 config:  {configured}/{len(entries)}")


def validate_project_code(project_path):
    """Basic validation that project code works."""
    p = Path(project_path)

    # Check index.html exists and has content
    index = p / "e156-submission" / "index.html"
    if index.exists() and index.stat().st_size > 500:
        return True, "index.html OK"

    # Check for Python files - try to compile
    py_files = list(p.glob("*.py"))
    for pf in py_files[:3]:
        rc, _, err = run(f'python -m py_compile "{pf}"', cwd=str(p))
        if rc != 0:
            return False, f"Python syntax error in {pf.name}: {err[:80]}"

    # Check for HTML files - basic structure check
    html_files = list(p.glob("*.html"))
    for hf in html_files[:3]:
        content = hf.read_text(encoding="utf-8", errors="replace")
        if "<html" not in content.lower():
            return False, f"Bad HTML in {hf.name}"

    return True, "OK"


def push_project(project_path, branch="master"):
    """Commit and push a project to GitHub."""
    p = str(project_path)
    if not os.path.isdir(os.path.join(p, ".git")):
        return False, "No .git"

    # Add e156-submission and index.html
    run("git add e156-submission/ index.html .nojekyll", cwd=p)
    run('git commit -m "E156: sync DRAFT/FINAL status + author info"', cwd=p)

    # Push
    rc, _, err = run(f"git push origin {branch}", cwd=p, timeout=30)
    if rc != 0:
        # Try other branch
        rc, _, err = run("git push origin main", cwd=p, timeout=30)
    return rc == 0, err[:80] if rc != 0 else "Pushed"


def main():
    do_deploy = "--deploy" in sys.argv
    do_push = "--push" in sys.argv
    status_only = "--status" in sys.argv

    if not WORKBOOK.exists():
        print(f"Workbook not found: {WORKBOOK}")
        sys.exit(1)

    print("Parsing workbook...")
    entries = parse_workbook(str(WORKBOOK))
    print(f"Found {len(entries)} entries")

    if status_only:
        show_status(entries)
        return

    show_status(entries)

    if not do_deploy:
        print(f"\nDry run. To deploy: python deploy_all.py --deploy")
        print(f"To deploy + push:   python deploy_all.py --deploy --push")
        return

    # Step 1: Sync all configs (author info + DRAFT/FINAL)
    print(f"\n{'=' * 60}")
    print("STEP 1: Syncing all configs (author + DRAFT/FINAL)")
    print(f"{'=' * 60}")
    synced = apply_all_configs(entries)
    print(f"  Updated {synced} project configs")

    # Step 2: Create .nojekyll in all projects
    print(f"\n{'=' * 60}")
    print("STEP 2: Creating .nojekyll files")
    print(f"{'=' * 60}")
    nojekyll_count = 0
    for e in entries:
        nj = Path(e["path"]) / ".nojekyll"
        if not nj.exists() and Path(e["path"]).is_dir():
            nj.write_text("", encoding="utf-8")
            nojekyll_count += 1
    print(f"  Created {nojekyll_count} .nojekyll files")

    # Step 3: Validate code before push
    if do_push:
        print(f"\n{'=' * 60}")
        print("STEP 3: Validating project code")
        print(f"{'=' * 60}")
        valid_count = 0
        invalid_projects = []
        for e in entries:
            p = Path(e["path"])
            if not p.is_dir():
                continue
            ok, msg = validate_project_code(str(p))
            if ok:
                valid_count += 1
            else:
                invalid_projects.append((e["name"], msg))
                print(f"  FAIL: {e['name']} — {msg}")
        print(f"  Valid: {valid_count}, Invalid: {len(invalid_projects)}")

    # Step 4: Push to GitHub
    if do_push:
        print(f"\n{'=' * 60}")
        print("STEP 4: Pushing to GitHub")
        print(f"{'=' * 60}")
        pushed = 0
        failed = 0
        for e in entries:
            p = Path(e["path"])
            if not p.is_dir() or not (p / ".git").is_dir():
                continue
            # Skip projects that failed validation
            if any(name == e["name"] for name, _ in invalid_projects):
                print(f"  SKIP (invalid): {e['name']}")
                continue
            ok, msg = push_project(str(p))
            if ok:
                pushed += 1
            else:
                failed += 1
                if "TIMEOUT" not in msg and "up-to-date" not in msg:
                    print(f"  FAIL: {e['name']} — {msg}")
        print(f"  Pushed: {pushed}, Failed: {failed}")

    # Step 5: Rebuild library
    print(f"\n{'=' * 60}")
    print("STEP 5: Rebuilding E156 library")
    print(f"{'=' * 60}")
    try:
        build_library()
        print("  Library rebuilt: C:/E156/e156-library.html")
    except Exception as ex:
        print(f"  Library build failed: {ex}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"DEPLOY COMPLETE — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'=' * 60}")
    submitted = sum(1 for e in entries if e["submitted"])
    print(f"  FINAL papers: {submitted}")
    print(f"  DRAFT papers: {len(entries) - submitted}")
    print(f"  Configs synced: {synced}")
    if do_push:
        print(f"  Repos pushed: {pushed}")
    print(f"\nPortfolio: https://{GH_USER}.github.io/")
    print(f"Library:   C:/E156/e156-library.html")


if __name__ == "__main__":
    main()
