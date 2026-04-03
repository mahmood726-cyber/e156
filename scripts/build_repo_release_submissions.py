"""
Build repo-local e156-submission folders for the tracked E156 release set and
run the protocol/disclosure pass on each submission.
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_SLUGS = [
    "clinical-ma",
    "fragility-atlas",
    "metarep",
    "reduced-dose-doacs-vte-demo",
]

sys.path.insert(0, str(SCRIPT_DIR))

from add_protocols_and_disclosure import process as add_protocol_and_disclosure
from finalize_all import AFFILIATION, AUTHOR, EMAIL, pick_refs
from generate_submission import generate_submission


def load_article(slug: str) -> dict:
    article_path = REPO_ROOT / "output" / "json" / f"{slug}.json"
    if not article_path.exists():
        raise FileNotFoundError(f"Missing article JSON for slug '{slug}': {article_path}")
    return json.loads(article_path.read_text(encoding="utf-8"))


def build_config(slug: str, article: dict) -> dict:
    project_dir = REPO_ROOT / "releases" / slug
    refs = pick_refs(article.get("title", ""), article.get("body", ""), article.get("type", "methods"))
    validation_status = article.get("validation", {}).get("status", "")
    notes = {
        "app": article.get("app", ""),
        "data": article.get("data", ""),
        "code": article.get("code", ""),
        "doi": article.get("doi", ""),
        "version": article.get("version", "1.0"),
        "date": article.get("date", ""),
        "certainty": article.get("certainty", ""),
        "validation": validation_status.upper() if validation_status else "DRAFT",
        "protocol": article.get("protocol", ""),
        "source_article": article.get("source_article", ""),
    }
    config = {
        "title": article.get("title", ""),
        "slug": slug,
        "author": AUTHOR,
        "affiliation": AFFILIATION,
        "email": EMAIL,
        "date": article.get("date", ""),
        "path": str(project_dir),
        "type": article.get("type", "methods"),
        "primary_estimand": article.get("primary_estimand", ""),
        "certainty": article.get("certainty", ""),
        "summary": article.get("summary", ""),
        "body": article.get("body", ""),
        "sentences": article.get("sentences", []),
        "notes": notes,
        "study_count": article.get("study_count"),
        "participant_count": article.get("participant_count"),
        "studies": article.get("studies", []),
        "primary_plot": article.get("primary_plot", {}),
        "references": refs,
    }
    for key in ("search_strategy", "prisma", "included_papers", "analysis_modules", "journal_wrapper"):
        if key in article:
            config[key] = article[key]
    return config


def build_submission(slug: str) -> Path:
    article = load_article(slug)
    config = build_config(slug, article)
    ok = generate_submission(config)
    if not ok:
        raise RuntimeError(f"Submission generation failed validation for '{slug}'")
    submission_dir = Path(config["path"]) / "e156-submission"
    add_protocol_and_disclosure(submission_dir)
    return submission_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Build repo-local release submissions and run protocol/disclosure.")
    parser.add_argument(
        "--slugs",
        nargs="*",
        default=DEFAULT_SLUGS,
        help="Optional subset of release slugs to materialize.",
    )
    args = parser.parse_args()

    built = []
    for slug in args.slugs:
        submission_dir = build_submission(slug)
        built.append({"slug": slug, "submission_dir": str(submission_dir)})

    print(json.dumps({"built": built}, indent=2))


if __name__ == "__main__":
    main()
