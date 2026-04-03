import argparse
import csv
import json
import re
from pathlib import Path

from validate_e156 import validate


HTML_TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "e156_interactive_template.html"
ROLE_SEQUENCE = [
    "Question",
    "Dataset",
    "Method",
    "Primary result",
    "Robustness",
    "Interpretation",
    "Boundary",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "untitled"


def parse_json_field(value: str):
    value = (value or "").strip()
    if not value:
        return None
    return json.loads(value)


def parse_int(value: str):
    value = (value or "").strip().replace(",", "")
    if not value:
        return None
    return int(value)


def derive_sentences(body: str) -> list[dict[str, str]]:
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', body.strip())
    parts = [part.strip() for part in parts if part.strip()]
    if len(parts) != len(ROLE_SEQUENCE):
        return []
    return [{"role": role, "text": text} for role, text in zip(ROLE_SEQUENCE, parts)]


def build_article(row: dict[str, str], validation_result: dict) -> dict:
    body = row.get("body", "").strip()
    article = {
        "title": row.get("title", "").strip(),
        "summary": row.get("summary", "").strip(),
        "type": row.get("type", "").strip(),
        "primary_estimand": row.get("primary_estimand", "").strip(),
        "study_count": parse_int(row.get("study_count", "")),
        "participant_count": parse_int(row.get("participant_count", "")),
        "version": row.get("version", "").strip(),
        "date": row.get("date", "").strip(),
        "certainty": row.get("certainty", "").strip(),
        "app": row.get("app", "").strip(),
        "data": row.get("data", "").strip(),
        "code": row.get("code", "").strip(),
        "doi": row.get("doi", "").strip(),
        "protocol": row.get("protocol", "").strip(),
        "source_article": row.get("source_article", "").strip(),
        "body": body,
        "validation": {
            "status": "pass" if validation_result["ok"] else "fail",
            "checks": validation_result["checks"],
        },
        "primary_plot": parse_json_field(row.get("primary_plot", "")) or {},
        "studies": parse_json_field(row.get("studies", "")) or [],
    }

    extra = parse_json_field(row.get("extra_fields", ""))
    if isinstance(extra, dict):
        article.update(extra)

    if "sentences" not in article:
        derived_sentences = derive_sentences(body)
        if derived_sentences:
            article["sentences"] = derived_sentences

    return article


def render_html(article: dict, template_text: str) -> str:
    return template_text.replace("__E156_JSON__", json.dumps(article, indent=2))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build validated E156 JSON and HTML bundles from a CSV file.")
    parser.add_argument("--input", required=True, help="CSV file with one article per row.")
    parser.add_argument(
        "--output-root",
        default=str(Path(__file__).resolve().parents[1] / "output"),
        help="Root directory for batch outputs.",
    )
    parser.add_argument(
        "--template",
        default=str(HTML_TEMPLATE),
        help="HTML template path.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_root = Path(args.output_root)
    template_text = Path(args.template).read_text(encoding="utf-8")

    json_dir = output_root / "json"
    html_dir = output_root / "html"
    validation_dir = output_root / "validation"
    json_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    validation_dir.mkdir(parents=True, exist_ok=True)

    manifest = []

    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=1):
            title = (row.get("title") or "").strip() or f"article-{index}"
            slug = (row.get("slug") or "").strip() or slugify(title)
            body = (row.get("body") or "").strip()
            validation_result = validate(body, strict_words=True)
            article = build_article(row, validation_result)

            json_path = json_dir / f"{slug}.json"
            html_path = html_dir / f"{slug}.html"
            validation_path = validation_dir / f"{slug}.validation.json"

            write_json(json_path, article)
            write_json(validation_path, validation_result)
            html_path.write_text(render_html(article, template_text), encoding="utf-8")

            manifest.append(
                {
                    "slug": slug,
                    "title": title,
                    "json": str(json_path),
                    "html": str(html_path),
                    "validation": str(validation_path),
                    "ok": validation_result["ok"],
                    "word_count": validation_result["word_count"],
                    "sentence_count": validation_result["sentence_count"],
                }
            )

    manifest_path = output_root / "manifest.json"
    write_json(manifest_path, {"input": str(input_path), "records": manifest})
    print(f"Wrote manifest {manifest_path}")
    print(f"JSON bundles: {json_dir}")
    print(f"HTML bundles: {html_dir}")
    print(f"Validation reports: {validation_dir}")


if __name__ == "__main__":
    main()
