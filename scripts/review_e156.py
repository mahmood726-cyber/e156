import argparse
import json
import re
from pathlib import Path


REQUIRED_PERSONAS = ["clinician", "statistician", "methods_editor", "skeptic", "reader"]
ALLOWED_VERDICTS = {"pass", "revise", "block"}

# A real persona note must say something. Below this length, or matching a
# rubber-stamp placeholder, the review does not gate-pass.
MIN_NOTE_CHARS = 20
_PLACEHOLDER_NOTE_RE = re.compile(
    r"^(?:n/?a|tbd|todo|lgtm|ok(?:ay)?|fine|good|pass|approved|looks good|"
    r"starter\b.*|replace\b.*)$",
    re.IGNORECASE,
)


def _norm(value: str) -> str:
    return clean_text(value).strip().lower()


def _is_weak_note(note: str) -> bool:
    note = clean_text(note)
    return len(note) < MIN_NOTE_CHARS or bool(_PLACEHOLDER_NOTE_RE.match(note))
DEFAULT_REVIEWER_IDS = {
    "clinician": "clinical-desk",
    "statistician": "stats-desk",
    "methods_editor": "methods-desk",
    "skeptic": "skeptic-desk",
    "reader": "reader-desk",
}
# The seed desk labels are placeholders, not real reviewer identities. A
# completed review must replace them, and the 5 reviewer ids must be distinct
# (one person cannot fill all five desks).
DEFAULT_DESK_LABELS = frozenset(DEFAULT_REVIEWER_IDS.values())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def clean_text(value: object) -> str:
    return str(value or "").strip()


def summarize_review(review: dict, author: str | None = None) -> dict:
    personas = review.get("personas", {})
    missing = [name for name in REQUIRED_PERSONAS if name not in personas]
    invalid = []
    empty_notes = []
    weak_notes = []
    conflicted_reviewers = []
    placeholder_reviewers = []
    duplicate_reviewers = []
    seen_reviewer_norms: set[str] = set()
    missing_reviewer_ids = []
    missing_signed_at = []
    verdict_counts = {"pass": 0, "revise": 0, "block": 0}
    required_actions = []
    reviewer_signoffs = []
    reviewed_at = clean_text(review.get("reviewed_at"))
    author_norm = _norm(author) if author else ""

    for name in REQUIRED_PERSONAS:
        persona = personas.get(name, {})
        verdict = persona.get("verdict")
        if verdict not in ALLOWED_VERDICTS:
            invalid.append(name)
            continue
        verdict_counts[verdict] += 1
        note = clean_text(persona.get("notes"))
        if not note:
            empty_notes.append(name)
        elif _is_weak_note(note):
            weak_notes.append(name)
        reviewer_id = clean_text(persona.get("reviewer_id"))
        signed_at = clean_text(persona.get("signed_at"))
        if not reviewer_id:
            missing_reviewer_ids.append(name)
        else:
            rnorm = _norm(reviewer_id)
            if author_norm and rnorm == author_norm:
                conflicted_reviewers.append(name)  # author cannot review own paper
            if reviewer_id in DEFAULT_DESK_LABELS:
                placeholder_reviewers.append(name)  # seed desk label is not a real reviewer
            if rnorm in seen_reviewer_norms:
                duplicate_reviewers.append(name)    # one person filling multiple desks
            seen_reviewer_norms.add(rnorm)
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

    blocking = bool(
        missing or invalid or empty_notes or weak_notes or conflicted_reviewers
        or placeholder_reviewers or duplicate_reviewers
        or missing_reviewer_ids or missing_signed_at or not reviewed_at
    )
    if blocking:
        gate = "block"
    elif verdict_counts["block"] > 0:
        gate = "block"
    elif verdict_counts["revise"] > 0:
        gate = "revise"
    else:
        gate = "pass"

    return {
        "ok": not blocking,
        "gate": gate,
        "missing_personas": missing,
        "invalid_personas": invalid,
        "empty_notes": empty_notes,
        "weak_notes": weak_notes,
        "conflicted_reviewers": conflicted_reviewers,
        "placeholder_reviewers": placeholder_reviewers,
        "duplicate_reviewers": duplicate_reviewers,
        "missing_reviewer_ids": missing_reviewer_ids,
        "missing_signed_at": missing_signed_at,
        "missing_reviewed_at": not bool(reviewed_at),
        "reviewed_at": reviewed_at,
        "verdict_counts": verdict_counts,
        "required_actions": required_actions,
        "reviewer_signoffs": reviewer_signoffs,
    }


def build_persona_stub(name: str, starter_mode: bool, seed_reviewers: bool) -> dict:
    focus_map = {
        "clinician": "practical clarity",
        "statistician": "numerical honesty",
        "methods_editor": "structure discipline",
        "skeptic": "overclaim and causality check",
        "reader": "flow and readability",
    }
    stub = {
        "focus": focus_map[name],
        # --seed-reviewers prefills only the desk label. It must NOT stamp a
        # signoff date or a passing verdict — that would let one command forge a
        # completed review (2026-05-28 red-team #6).
        "reviewer_id": DEFAULT_REVIEWER_IDS[name] if seed_reviewers else "",
        "signed_at": "",
        # Default to "revise", never "pass": an un-completed template must not
        # read as approval.
        "verdict": "revise",
        "notes": "",
        "required_actions": [],
    }
    if starter_mode:
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
        "personas": {name: build_persona_stub(name, starter_mode, seed_reviewers) for name in REQUIRED_PERSONAS},
        "article_title": article.get("title", ""),
        "body": article.get("body", ""),
    }
    write_json(output_path, template)


def attach_review(article_path: Path, review_path: Path, output_path: Path, summary_path: Path | None) -> None:
    article = load_json(article_path)
    review = load_json(review_path)
    summary = summarize_review(review, author=article.get("corresponding_author") or article.get("author"))
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
    parser.add_argument("--author", default="", help="Corresponding author id; --check blocks if any reviewer_id matches (no self-review).")
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
        summary = summarize_review(review, author=args.author or None)
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
