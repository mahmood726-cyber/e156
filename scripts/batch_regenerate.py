"""
batch_regenerate.py — Regenerate E156 artifacts for ALL projects that have config.json.

Creates/updates: index.html, paper.md, paper.json, protocol.md
Also ensures: author info, submitted status, references, slug, GitHub URL

Usage:
    python batch_regenerate.py              # Dry run (count only)
    python batch_regenerate.py --apply      # Regenerate all
    python batch_regenerate.py --apply --push  # Regenerate + push
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from generate_submission import generate_submission, TEMPLATE_PATH
from validate_e156 import split_sentences

GH_USER = "mahmood726-cyber"

# All directories to scan
SCAN_DIRS = [
    "C:/Models",
    "C:/Projects",
    "C:/HTML apps",
    "C:/AdaptSim", "C:/AlBurhan", "C:/AlMizan", "C:/BenfordMA",
    "C:/BiasForensics", "C:/CausalSynth", "C:/E156",
    "C:/EvidenceHalfLife", "C:/EvidenceQuality", "C:/FragilityAtlas",
    "C:/MetaAudit", "C:/MetaFolio", "C:/MetaReproducer",
    "C:/MetaShift", "C:/OutcomeReportingBias", "C:/OverlapDetector",
    "C:/PredictionGap", "C:/RMSTmeta", "C:/ubcma",
    "C:/AfricaRCT", "C:/overmind", "C:/meta_transport_engine",
]


def find_all_configs():
    """Find all e156-submission/config.json files."""
    configs = []
    for scan_dir in SCAN_DIRS:
        p = Path(scan_dir)
        if not p.is_dir():
            continue
        # Check if this dir itself has e156-submission
        cfg = p / "e156-submission" / "config.json"
        if cfg.exists():
            configs.append(cfg)
        # Check immediate children
        for child in sorted(p.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            cfg = child / "e156-submission" / "config.json"
            if cfg.exists():
                configs.append(cfg)
    return configs


def ensure_protocol(project_dir, config):
    """Create protocol.md if it doesn't exist."""
    proto_path = project_dir / "e156-submission" / "protocol.md"
    if proto_path.exists():
        return False

    title = config.get("title", project_dir.name)
    body = config.get("body", "")
    notes = config.get("notes", {})
    proj_type = config.get("type", "methods")

    lines = [
        f"# Protocol: {title}",
        "",
        f"**Type:** {proj_type}",
        f"**Primary Estimand:** {config.get('primary_estimand', 'Not specified')}",
        f"**Certainty:** {config.get('certainty', 'Not assessed')}",
        "",
        "## Search Strategy",
        "",
        config.get("search_strategy", {}).get("description", "Systematic search of relevant databases."),
        "",
        "## Inclusion Criteria",
        "",
        "- Studies matching the primary research question",
        "- Published in peer-reviewed journals or registered on ClinicalTrials.gov",
        "",
        "## Analysis Plan",
        "",
        f"- Tool: {notes.get('app', 'Custom implementation')}",
        f"- Data source: {notes.get('data', 'As described in the paper')}",
        f"- Code: {notes.get('code', 'Available on GitHub')}",
        "",
        "## Reporting",
        "",
        "Results reported following E156 micro-paper format (7 sentences, <=156 words).",
        "",
        "## AI Disclosure",
        "",
        "AI was used as a constrained synthesis engine operating on structured inputs.",
        "All results were reviewed and verified by the author.",
        "",
        f"*Protocol generated: {datetime.now().strftime('%Y-%m-%d')}*",
    ]

    proto_path.write_text("\n".join(lines), encoding="utf-8")
    return True


def enrich_config(config, project_dir):
    """Ensure config has author info, slug, references, GitHub URL."""
    changed = False
    name = project_dir.name

    # Author info
    if config.get("author") != "Mahmood Ahmad":
        config["author"] = "Mahmood Ahmad"
        changed = True
    if config.get("affiliation") != "Tahir Heart Institute":
        config["affiliation"] = "Tahir Heart Institute"
        changed = True
    if config.get("email") != "mahmood.ahmad2@nhs.net":
        config["email"] = "mahmood.ahmad2@nhs.net"
        changed = True

    # Slug
    if not config.get("slug"):
        config["slug"] = name.lower().replace("_", "-").replace(" ", "-")
        changed = True

    # GitHub URL
    if "notes" not in config:
        config["notes"] = {}
    if not config["notes"].get("code"):
        slug = config["slug"]
        config["notes"]["code"] = f"https://github.com/{GH_USER}/{slug}"
        changed = True

    # References (ensure at least empty list)
    if "references" not in config:
        config["references"] = []
        changed = True

    # Submitted status
    if "submitted" not in config:
        config["submitted"] = False
        changed = True

    return changed


def main():
    do_apply = "--apply" in sys.argv
    do_push = "--push" in sys.argv

    print("Scanning for e156-submission/config.json files...")
    configs = find_all_configs()
    print(f"Found {len(configs)} projects with config.json\n")

    if not do_apply:
        # Dry run - count what needs work
        need_index = 0
        need_paper = 0
        need_protocol = 0
        need_enrich = 0

        for cfg_path in configs:
            sub_dir = cfg_path.parent
            if not (sub_dir / "index.html").exists():
                need_index += 1
            if not (sub_dir / "paper.md").exists():
                need_paper += 1
            if not (sub_dir / "protocol.md").exists():
                need_protocol += 1
            try:
                c = json.loads(cfg_path.read_text(encoding="utf-8"))
                if c.get("author") != "Mahmood Ahmad" or not c.get("slug"):
                    need_enrich += 1
            except Exception:
                pass

        print(f"Need index.html:  {need_index}")
        print(f"Need paper.md:    {need_paper}")
        print(f"Need protocol.md: {need_protocol}")
        print(f"Need enrichment:  {need_enrich}")
        print(f"\nRun with --apply to generate all missing artifacts.")
        return

    # Apply mode
    generated = 0
    protocols = 0
    enriched = 0
    errors = 0

    for i, cfg_path in enumerate(configs, 1):
        project_dir = cfg_path.parent.parent
        sub_dir = cfg_path.parent

        try:
            config = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ERROR reading {cfg_path}: {e}")
            errors += 1
            continue

        # Enrich config
        if enrich_config(config, project_dir):
            enriched += 1

        # Set path for generate_submission
        config["path"] = str(project_dir)

        # Save enriched config
        cfg_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

        # Generate submission artifacts (index.html, paper.md, paper.json)
        try:
            generate_submission(config)
            generated += 1
        except Exception as e:
            print(f"  ERROR generating {project_dir.name}: {e}")
            errors += 1
            continue

        # Generate protocol if missing
        if ensure_protocol(project_dir, config):
            protocols += 1

        if i % 50 == 0:
            print(f"  Progress: {i}/{len(configs)}...")

    print(f"\n{'=' * 60}")
    print(f"BATCH REGENERATION COMPLETE")
    print(f"  Generated: {generated}")
    print(f"  Protocols created: {protocols}")
    print(f"  Configs enriched: {enriched}")
    print(f"  Errors: {errors}")
    print(f"{'=' * 60}")

    if do_push:
        print(f"\nPushing updated projects...")
        pushed = 0
        for cfg_path in configs:
            project_dir = cfg_path.parent.parent
            if not (project_dir / ".git").is_dir():
                continue
            subprocess.run(
                ["git", "add", "e156-submission/", "index.html", ".nojekyll"],
                cwd=str(project_dir), capture_output=True, timeout=10
            )
            rc = subprocess.run(
                ["git", "commit", "-m", "E156: regenerate artifacts + author info"],
                cwd=str(project_dir), capture_output=True, timeout=10
            ).returncode
            if rc != 0:
                continue  # nothing to commit
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=str(project_dir), capture_output=True, text=True, timeout=5
            )
            branch = branch_result.stdout.strip() or "master"
            rc = subprocess.run(
                ["git", "push", "origin", branch],
                cwd=str(project_dir), capture_output=True, timeout=30
            ).returncode
            if rc == 0:
                pushed += 1
        print(f"  Pushed: {pushed}")


if __name__ == "__main__":
    main()
