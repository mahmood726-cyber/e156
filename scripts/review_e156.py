import argparse
import json
from pathlib import Path


REQUIRED_PERSONAS = ["clinician", "statistician", "methods_editor", "skeptic", "reader"]
ALLOWED_VERDICTS = {"pass", "revise", "block"}
DEFAULT_REVIEWER_IDS = {
    "clinician": "clinical-desk",
    "statistician": "stats-desk",
    "methods_editor": "methods-desk",
    "skeptic": "skeptic-desk",
    "reader": "reader-desk",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def clean_text(value: object) -> str:
    return str(value or "").strip()


def summarize_review(review: dict) -> dict:
    personas = review.get("personas", {})
    missing = [name for name in REQUIRED_PERSONAS if name not in personas]
    invalid = []
    empty_notes = []
    missing_reviewer_ids = []
    missing_signed_at = []
    verdict_counts = {"pass": 0, "revise": 0, "block": 0}
    required_actions = []
    reviewer_signoffs = []
    reviewed_at = clean_text(review.get("reviewed_at"))

    for name in REQUIRED_PERSONAS:
        persona = personas.get(name, {})
        verdict = persona.get("verdict")
        if verdict not in ALLOWED_VERDICTS:
            invalid.append(name)
            continue
        verdict_counts[verdict] += 1
        if not clean_text(persona.get("notes")):
            empty_notes.append(name)
        reviewer_id = clean_text(persona.get("reviewer_id"))
        signed_at = clean_text(persona.get("signed_at"))
        if not reviewer_id:
            missing_reviewer_ids.append(name)
        if not signed_at:
            missing_signed_at.append(name)
        reviewer_signoffs.append(
            {
                "persona": name,
                "reviewer_id": reviewer_id,
                "signed_at": signed_at,
                "verdict": verdict,
            }
        )
        actions = persona.get("required_actions") or []
        for action in actions:
            required_actions.append({"persona": name, "action": action})

    if missing or invalid or empty_notes or missing_reviewer_ids or missing_signed_at or not reviewed_at:
        gate = "block"
    elif verdict_counts["block"] > 0:
        gate = "block"
    elif verdict_counts["revise"] > 0:
        gate = "revise"
    else:
        gate = "pass"

    return {
        "ok": (
            not missing
            and not invalid
            and not empty_notes
            and not missing_reviewer_ids
            and not missing_signed_at
            and bool(reviewed_at)
        ),
        "gate": gate,
        "missing_personas": missing,
        "invalid_personas": invalid,
        "empty_notes": empty_notes,
        "missing_reviewer_ids": missing_reviewer_ids,
        "missing_signed_at": missing_signed_at,
        "missing_reviewed_at": not bool(reviewed_at),
        "reviewed_at": reviewed_at,
        "verdict_counts": verdict_counts,
        "required_actions": required_actions,
        "reviewer_signoffs": reviewer_signoffs,
    }


def build_persona_stub(name: str, starter_mode: bool, seed_reviewers: bool, signed_at: str) -> dict:
    focus_map = {
        "clinician": "practical clarity",
        "statistician": "numerical honesty",
        "methods_editor": "structure discipline",
        "skeptic": "overclaim and causality check",
        "reader": "flow and readability",
    }
    stub = {
        "focus": focus_map[name],
        "reviewer_id": DEFAULT_REVIEWER_IDS[name] if seed_reviewers else "",
        "signed_at": signed_at if seed_reviewers and signed_at else "",
        "verdict": "pass",
        "notes": "",
        "required_actions": [],
    }
    if starter_mode:
        stub["verdict"] = "revise"
        stub["notes"] = "Starter only. Replace with completed persona review notes."
        stub["required_actions"] = ["Complete persona review and replace starter note."]
    return stub


def init_review(
    article_path: Path,
    output_path: Path,
    starter_mode: bool = False,
    seed_reviewers: bool = False,
    signed_at: str = "",
) -> None:
    article = load_json(article_path)
    template = {
        "article_slug": article_path.stem,
        "reviewed_at": signed_at if seed_reviewers and signed_at else "",
        "personas": {name: build_persona_stub(name, starter_mode, seed_reviewers, signed_at) for name in REQUIRED_PERSONAS},
        "article_title": article.get("title", ""),
        "body": article.get("body", ""),
    }
    write_json(output_path, template)


def attach_review(article_path: Path, review_path: Path, output_path: Path, summary_path: Path | None) -> None:
    article = load_json(article_path)
    review = load_json(review_path)
    summary = summarize_review(review)
    reviewed_article = dict(article)
    reviewed_article["review"] = review
    reviewed_article["review_summary"] = summary
    write_json(output_path, reviewed_article)
    if summary_path:
        write_json(summary_path, summary)


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize, check, or attach a multi-persona E156 review.")
    parser.add_argument("--article", help="Article JSON path.")
    parser.add_argument("--review", help="Review JSON path.")
    parser.add_argument("--output", help="Output JSON path.")
    parser.add_argument("--summary-out", help="Optional review summary output path.")
    parser.add_argument("--init", action="store_true", help="Create a blank review template from an article JSON file.")
    parser.add_argument("--check", action="store_true", help="Validate and summarize a review JSON file.")
    parser.add_argument("--attach", action="store_true", help="Attach review and summary to an article JSON file.")
    parser.add_argument("--starter-mode", action="store_true", help="Seed the review as a starter draft with revise verdicts and placeholder notes.")
    parser.add_argument("--seed-reviewers", action="store_true", help="Prefill default reviewer desk ids.")
    parser.add_argument("--signed-at", default="", help="Optional YYYY-MM-DD signoff date to prefill reviewed_at and persona signed_at fields.")
    args = parser.parse_args()

    if args.init:
        if not args.article or not args.output:
            raise SystemExit("--init requires --article and --output.")
        init_review(
            Path(args.article),
            Path(args.output),
            starter_mode=args.starter_mode,
            seed_reviewers=args.seed_reviewers,
            signed_at=args.signed_at,
        )
        print(f"Wrote review template {args.output}")
        return

    if args.check:
        if not args.review:
            raise SystemExit("--check requires --review.")
        review = load_json(Path(args.review))
        summary = summarize_review(review)
        if args.summary_out:
            write_json(Path(args.summary_out), summary)
        print(json.dumps(summary, indent=2))
        return

    if args.attach:
        if not args.article or not args.review or not args.output:
            raise SystemExit("--attach requires --article, --review, and --output.")
        summary_path = Path(args.summary_out) if args.summary_out else None
        attach_review(Path(args.article), Path(args.review), Path(args.output), summary_path)
        print(f"Wrote reviewed article {args.output}")
        if summary_path:
            print(f"Wrote review summary {summary_path}")
        return

    raise SystemExit("Choose one mode: --init, --check, or --attach.")


if __name__ == "__main__":
    main()
