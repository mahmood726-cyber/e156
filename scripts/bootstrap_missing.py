"""
bootstrap_missing.py — Create e156-submission dirs for workbook entries that lack them.

Reads the workbook, finds projects with valid PATHs that don't have e156-submission/,
and creates the minimal submission structure (config.json + paper.json).

Usage:
    python bootstrap_missing.py --dry-run   # Preview
    python bootstrap_missing.py             # Create missing submissions
    python bootstrap_missing.py --rebuild   # Also rebuild _batch_all.json after
"""

import argparse
import json
import re
import sys
import io
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WORKBOOK = Path("C:/E156/rewrite-workbook.txt")
GH_USER = "mahmood726-cyber"


def parse_workbook():
    """Parse rewrite-workbook.txt into structured entries."""
    content = WORKBOOK.read_text(encoding="utf-8")
    separator = "=" * 70
    blocks = content.split(separator)
    entries = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        header_match = re.match(r'\[(\d+)/\d+\]\s+(.+)', block)
        if not header_match:
            continue

        entry_num = int(header_match.group(1))
        name = header_match.group(2).strip()

        title = ""
        entry_type = ""
        estimand = ""
        data_desc = ""
        path = ""
        current_body = ""
        submitted = False

        for line in block.splitlines():
            line_s = line.strip()
            if line_s.startswith("TITLE:"):
                title = line_s[6:].strip()
            elif line_s.startswith("TYPE:"):
                parts = line_s[5:].split("|")
                entry_type = parts[0].strip()
                if len(parts) > 1 and "ESTIMAND:" in parts[1]:
                    estimand = parts[1].split("ESTIMAND:")[1].strip()
            elif line_s.startswith("DATA:"):
                data_desc = line_s[5:].strip()
            elif line_s.startswith("PATH:"):
                path = line_s[5:].strip()
            elif line_s.startswith("SUBMITTED: [x]"):
                submitted = True

        body_match = re.search(
            r'CURRENT BODY \(\d+ words\):\n(.+?)(?:\nYOUR REWRITE|\Z)',
            block, re.DOTALL
        )
        if body_match:
            current_body = body_match.group(1).strip()

        if path and current_body:
            entries.append({
                "num": entry_num,
                "name": name,
                "title": title,
                "type": entry_type,
                "estimand": estimand,
                "data": data_desc,
                "path": path,
                "body": current_body,
                "submitted": submitted,
            })

    return entries


def to_slug(name):
    return name.lower().replace("_", "-").replace(" ", "-")


def create_submission(entry, dry_run=False):
    """Create e156-submission/ directory with config.json and paper.json."""
    proj_path = Path(entry["path"])
    sub_dir = proj_path / "e156-submission"
    config_file = sub_dir / "config.json"
    paper_file = sub_dir / "paper.json"

    slug = to_slug(entry["name"])
    now = datetime.now().strftime("%Y-%m-%d")

    config = {
        "slug": slug,
        "repo_url": f"https://github.com/{GH_USER}/{slug}",
        "pages_url": f"https://{GH_USER}.github.io/{slug}/",
        "author": "Mahmood Ahmad",
        "affiliation": "Tahir Heart Institute",
        "status": "FINAL" if entry["submitted"] else "DRAFT",
        "created": now,
    }

    # Parse body into sentences
    sentences = [s.strip() for s in re.split(r'(?<=[.?!])\s+', entry["body"]) if s.strip()]

    paper = {
        "title": entry["title"],
        "slug": slug,
        "date": now,
        "type": entry["type"],
        "primary_estimand": entry["estimand"],
        "certainty": "",
        "summary": entry["data"],
        "body": entry["body"],
        "sentences": sentences,
        "study_count": "",
        "participant_count": "",
    }

    if dry_run:
        return True

    sub_dir.mkdir(parents=True, exist_ok=True)
    config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    paper_file.write_text(json.dumps(paper, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Bootstrap missing E156 submissions")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild manifest after")
    args = parser.parse_args()

    entries = parse_workbook()
    created = 0
    skipped = 0
    missing_path = 0

    for entry in entries:
        proj_path = Path(entry["path"])
        if not proj_path.is_dir():
            missing_path += 1
            continue

        sub_dir = proj_path / "e156-submission"
        if sub_dir.exists() and (sub_dir / "config.json").exists():
            skipped += 1
            continue

        if create_submission(entry, dry_run=args.dry_run):
            tag = "DRY" if args.dry_run else "NEW"
            print(f"  {tag}  {entry['name']:45s}  {entry['path']}")
            created += 1

    print(f"\n{'Would create' if args.dry_run else 'Created'}: {created}")
    print(f"Already exists: {skipped}")
    print(f"Path not found: {missing_path}")
    print(f"Total entries: {len(entries)}")

    if args.rebuild and not args.dry_run and created > 0:
        import subprocess
        print("\nRebuilding manifest...")
        subprocess.run([sys.executable, str(Path(__file__).parent / "build_batch_manifest.py")])


if __name__ == "__main__":
    main()
