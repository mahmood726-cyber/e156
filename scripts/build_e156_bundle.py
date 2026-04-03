import argparse
import json
from pathlib import Path


INTERNAL_KEYS = {
    "review",
    "review_summary",
    "validation",
    "outsideNote",
    "meta",
    "sentences",
    "wordCount",
    "sentenceCount",
}


def sanitize_for_publication(value):
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            if key in INTERNAL_KEYS:
                continue
            cleaned[key] = sanitize_for_publication(item)
        return cleaned
    if isinstance(value, list):
        return [sanitize_for_publication(item) for item in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a self-contained E156 HTML bundle.")
    parser.add_argument("--input", required=True, help="Path to article JSON.")
    parser.add_argument("--output", required=True, help="Output HTML path.")
    parser.add_argument(
        "--template",
        default=str(Path(__file__).resolve().parents[1] / "templates" / "e156_interactive_template.html"),
        help="HTML template path.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    template_path = Path(args.template)

    article = json.loads(input_path.read_text(encoding="utf-8"))
    public_article = sanitize_for_publication(article)
    template = template_path.read_text(encoding="utf-8")
    html = template.replace("__E156_JSON__", json.dumps(public_article, indent=2))

    output_path.write_text(html, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
