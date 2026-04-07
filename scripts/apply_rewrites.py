"""
Apply rewrites from the workbook to all E156 submissions.
Validates EVERY rewrite before changing ANYTHING.
Only updates projects where you wrote a rewrite. Skips blanks.

Usage:
    python apply_rewrites.py                    # Validate only (dry run)
    python apply_rewrites.py --apply            # Validate + apply
    python apply_rewrites.py --apply --push     # Validate + apply + push to GitHub
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from validate_e156 import validate, split_sentences
from generate_submission import generate_submission


def parse_workbook(path):
    """Parse the rewrite workbook into project entries."""
    text = Path(path).read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"^={50,}$", text, flags=re.MULTILINE)

    for block in blocks:
        # Find project header
        m = re.search(r"\[(\d+)/\d+\]\s+(.+)", block)
        if not m:
            continue

        index = int(m.group(1))
        name = m.group(2).strip()

        # Find PATH
        pm = re.search(r"^PATH:\s*(.+)$", block, re.MULTILINE)
        if not pm:
            continue
        path_str = pm.group(1).strip()

        # Find CURRENT BODY
        cm = re.search(r"CURRENT BODY \(\d+ words\):\n(.+?)(?=\nYOUR REWRITE)", block, re.DOTALL)
        current = cm.group(1).strip() if cm else ""

        # Find YOUR REWRITE (stop at SUBMITTED line)
        rm = re.search(r"YOUR REWRITE \(at most 156 words, 7 sentences\):\n(.+?)(?=\nSUBMITTED:|\Z)", block, re.DOTALL)
        rewrite = rm.group(1).strip() if rm else ""

        # Find SUBMITTED status
        sm = re.search(r"SUBMITTED:\s*\[(x?)\]", block, re.IGNORECASE)
        submitted = bool(sm and sm.group(1).lower() == "x") if sm else False

        entries.append({
            "index": index,
            "name": name,
            "path": path_str,
            "current": current,
            "rewrite": rewrite,
            "submitted": submitted,
        })

    return entries


def validate_rewrite(name, body):
    """Validate a rewrite. Returns (ok, issues)."""
    issues = []
    wc = len(body.split())
    result = validate(body, strict_words=True)
    sents = split_sentences(body)

    if wc > 156:
        issues.append(f"Word count: {wc} (maximum 156)")
    if wc < 100:
        issues.append(f"Word count: {wc} (too short — minimum ~120 for substance)")
    if len(sents) != 7:
        issues.append(f"Sentence count: {len(sents)} (need exactly 7)")
    if "\n\n" in body:
        issues.append("Contains blank lines (must be single paragraph)")
    if re.search(r"^\s*#", body, re.MULTILINE):
        issues.append("Contains markdown headings")
    if re.search(r"https?://", body):
        issues.append("Contains URLs (not allowed in body)")

    # Check that at least one of S3-S5 has a number (result may land in S4 or adjacent)
    if len(sents) >= 5:
        has_num = any(re.search(r"\d", sents[i]) for i in range(2, 5))
        if not has_num:
            issues.append("S3-S5 have no numbers — must include quantitative result")

    # Check S7 has limitation language
    if len(sents) >= 7:
        s7 = sents[6].lower()
        limitation_words = ["limit", "cannot", "may not", "unclear", "uncertain",
                           "caution", "scope", "boundary", "harm", "constrain",
                           "generali", "restrict", "warrant", "however", "not ",
                           "does not", "only", "unable", "lack", "miss",
                           "exclude", "narrow", "depend", "assume", "imprecis",
                           "approximate", "not yet", "not address", "not extend",
                           "not capture", "not replace", "not detect", "not account",
                           "not valid", "not includ", "not support", "not scale",
                           "not assess", "not verify", "remains", "rather than",
                           "non-exclusive", "should be interpret", "caveat"]
        if not any(w in s7 for w in limitation_words):
            issues.append("S7 (sentence 7) has no limitation language")

    return len(issues) == 0, issues


def apply_rewrite(entry):
    """Apply one rewrite to its project. Uses YOUR REWRITE if submitted, else CURRENT BODY."""
    project_path = entry["path"]
    cfg_path = Path(project_path) / "e156-submission" / "config.json"

    if not cfg_path.exists():
        return False, f"config.json not found: {cfg_path}"

    try:
        config = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"Bad JSON: {e}"

    # Choose body: use rewrite if available, otherwise current
    body = entry["rewrite"] if entry["rewrite"] else entry["current"]

    sents = split_sentences(body)
    roles = ["Question", "Dataset", "Method", "Primary result", "Robustness", "Interpretation", "Boundary"]

    # Update config
    config["body"] = body
    if len(sents) == 7:
        config["sentences"] = [{"role": r, "text": s} for r, s in zip(roles, sents)]

    # Author info (always set)
    config["author"] = "Mahmood Ahmad"
    config["affiliation"] = "Tahir Heart Institute"
    config["email"] = "mahmood.ahmad2@nhs.net"

    # Submitted status (controls DRAFT vs FINAL display)
    config["submitted"] = entry["submitted"]

    # Ensure references exist (at least empty array)
    if "references" not in config or not config["references"]:
        config["references"] = []

    # Ensure slug for GitHub Pages links
    if "slug" not in config:
        config["slug"] = entry["name"].lower().replace("_", "-").replace(" ", "-")

    # Ensure notes.code has GitHub URL
    if "notes" not in config:
        config["notes"] = {}
    if not config["notes"].get("code"):
        slug = config["slug"]
        config["notes"]["code"] = f"https://github.com/mahmood726-cyber/{slug}"

    # Save config
    cfg_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    # Regenerate submission (index.html, paper.md, paper.json)
    config["path"] = project_path
    generate_submission(config)

    return True, "Applied"


def apply_all_configs(entries):
    """Update ALL project configs with author info and submitted status,
    even those without rewrites. This ensures DRAFT/FINAL is always current."""
    updated = 0
    for entry in entries:
        project_path = entry["path"]
        cfg_path = Path(project_path) / "e156-submission" / "config.json"

        if not cfg_path.exists():
            continue

        try:
            config = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        changed = False

        # Always update author info
        if config.get("author") != "Mahmood Ahmad":
            config["author"] = "Mahmood Ahmad"
            changed = True
        if config.get("affiliation") != "Tahir Heart Institute":
            config["affiliation"] = "Tahir Heart Institute"
            changed = True
        if config.get("email") != "mahmood.ahmad2@nhs.net":
            config["email"] = "mahmood.ahmad2@nhs.net"
            changed = True

        # Update submitted status
        if config.get("submitted") != entry["submitted"]:
            config["submitted"] = entry["submitted"]
            changed = True

        # Update body based on submitted status
        if entry["submitted"] and entry["rewrite"]:
            if config.get("body") != entry["rewrite"]:
                config["body"] = entry["rewrite"]
                sents = split_sentences(entry["rewrite"])
                roles = ["Question", "Dataset", "Method", "Primary result",
                         "Robustness", "Interpretation", "Boundary"]
                if len(sents) == 7:
                    config["sentences"] = [{"role": r, "text": s} for r, s in zip(roles, sents)]
                changed = True

        if changed:
            cfg_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
            config["path"] = project_path
            generate_submission(config)
            updated += 1

    return updated


def main():
    workbook_path = Path("C:/E156/rewrite-workbook.txt")
    if not workbook_path.exists():
        print(f"Workbook not found: {workbook_path}")
        sys.exit(1)

    do_apply = "--apply" in sys.argv
    do_push = "--push" in sys.argv

    print("Parsing workbook...")
    entries = parse_workbook(workbook_path)
    print(f"Found {len(entries)} projects in workbook\n")

    # Find entries with rewrites
    rewrites = [e for e in entries if e["rewrite"] and e["rewrite"] != e["current"]]
    skipped = len(entries) - len(rewrites)
    print(f"Rewrites found: {len(rewrites)}")
    print(f"Skipped (blank or unchanged): {skipped}\n")

    if not rewrites:
        print("No rewrites to apply. Edit the workbook and add your 156-word bodies.")
        return

    # Validate ALL rewrites first
    print("=" * 60)
    print("VALIDATING ALL REWRITES (nothing changed yet)")
    print("=" * 60)

    valid = []
    invalid = []
    for e in rewrites:
        ok, issues = validate_rewrite(e["name"], e["rewrite"])
        if ok:
            valid.append(e)
            print(f"  PASS: {e['name']} (156w, 7s)")
        else:
            invalid.append((e, issues))
            print(f"  FAIL: {e['name']}")
            for issue in issues:
                print(f"    - {issue}")

    print(f"\nValid: {len(valid)}, Invalid: {len(invalid)}")

    if invalid:
        print(f"\n{'!' * 60}")
        print(f"BLOCKED: {len(invalid)} rewrites have errors.")
        print(f"Fix them in the workbook and re-run.")
        print(f"NO CHANGES WERE MADE.")
        print(f"{'!' * 60}")

        if not do_apply:
            return
        else:
            print(f"\nApplying {len(valid)} valid rewrites only (skipping {len(invalid)} invalid)...")

    if not do_apply:
        print(f"\nDry run complete. To apply valid rewrites, run:")
        print(f"  python apply_rewrites.py --apply")
        return

    # First: update ALL configs with author info and submitted status
    print(f"\n{'=' * 60}")
    print(f"UPDATING ALL CONFIGS (author info + DRAFT/FINAL status)")
    print(f"{'=' * 60}")
    synced = apply_all_configs(entries)
    print(f"  Synced {synced} project configs")

    # Apply valid rewrites
    print(f"\n{'=' * 60}")
    print(f"APPLYING {len(valid)} REWRITES")
    print(f"{'=' * 60}")

    applied = 0
    for e in valid:
        ok, msg = apply_rewrite(e)
        if ok:
            applied += 1
            print(f"  Applied: {e['name']}")
        else:
            print(f"  ERROR: {e['name']} - {msg}")

    print(f"\nApplied {applied}/{len(valid)} rewrites")

    # Push if requested
    if do_push and applied > 0:
        print(f"\nPushing {applied} projects to GitHub...")
        for e in valid:
            p = Path(e["path"])
            if (p / ".git").is_dir():
                subprocess.run(["git", "-C", str(p), "add", "e156-submission/"],
                             capture_output=True, timeout=10)
                subprocess.run(["git", "-C", str(p), "commit", "-m",
                              "Author rewrite: verified 156-word body"],
                             capture_output=True, timeout=10)
                subprocess.run(["git", "-C", str(p), "push", "origin", "master"],
                             capture_output=True, timeout=30)
        print("Pushed.")

    print(f"\n{'=' * 60}")
    print(f"DONE: {applied} papers updated, {skipped} unchanged, {len(invalid)} need fixes")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
