import argparse
import json
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"(https?://|www\.|doi\.org/)", re.IGNORECASE)
HEADING_RE = re.compile(r"^\s*#+\s+", re.MULTILINE)
INTERVAL_RE = re.compile(
    r"\b(?:(?:9[059]|99)%?\s*(?:CI|CrI|PI|confidence interval|credible interval|prediction interval)"
    r"|CI|IQR|prediction interval|credible interval"
    r"|(?:CI|IQR|range|interval)\s+\d+[\u2013\u2014.-]+\d+"
    r"|within\s+[\d.]+|tolerance|parity|matched.*within"
    r"|\d+\.?\d*\s*(?:percent|%)(?:\s|[.,;:])|(?:pass|passed)\s+(?:\d+|all)"
    r"|\d+\s*(?:of|/)\s*\d+)\b",
    re.IGNORECASE,
)
ESTIMATE_RE = re.compile(
    r"\b(?:RR|OR|HR|MD|SMD|RD|AUC|IRR|NNT|WMD"
    r"|sensitivity|specificity|mean difference|risk ratio|odds ratio|hazard ratio"
    r"|relative risk|risk difference|rate ratio|fragility index|median|prevalence"
    r"|calibration slope|proportion|correlation|r-squared|eta.squared"
    r"|number needed to treat|incidence rate|concordance|accuracy"
    r"|RMST|restricted mean survival|replication probability"
    r"|coverage|parity|tolerance|pass rate|matched|deviation"
    r"|error|bias|reduction|compliance|concordance rate"
    r"|scenarios?\s+passed|percent|tau.squared|I.squared"
    r"|pooled\s+estimates?|validation|coefficient"
    r"|optimism|classification|convincing|credibility"
    r"|count|counts|stock|backlog|share|records?|studies?|family|families)\b",
    re.IGNORECASE,
)
QUANT_RE = re.compile(
    r"\b(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\s*"
    r"(?:percent|%|studies?|records?|trials?|patients?|events?|rate|share|stock|backlog|counts?)\b"
    r"|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b"
    r"|\b\d{3,}(?:\.\d+)?\b"
    r"|\b\d+\s*(?:of|/)\s*\d+\b",
    re.IGNORECASE,
)


def load_text(args: argparse.Namespace) -> str:
    if args.stdin:
        return sys.stdin.read().strip()

    if not args.file:
        raise SystemExit("Provide --file or --stdin.")

    path = Path(args.file)
    raw = path.read_text(encoding="utf-8")

    if args.json_field:
        data = json.loads(raw)
        value = data.get(args.json_field)
        if value is None:
            raise SystemExit(f"JSON field '{args.json_field}' not found.")
        return str(value).strip()

    return raw.strip()


_ABBREVIATIONS = sorted([
    "et al.", "e.g.", "i.e.", "U.S.", "U.K.",
    "Dr.", "Mr.", "Ms.", "vs.", "al.", "No.", "St.", "Prof.", "Fig.", "Vol.",
    "Eq.", "Jr.", "Sr.", "Ltd.", "Inc.", "Dept.", "Surg.", "Suppl.", "Ref.",
    "M.D.",
    "Jan.", "Feb.", "Mar.", "Apr.", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec.",
], key=len, reverse=True)  # longest first to avoid partial matches
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")


def split_sentences(text: str) -> list[str]:
    protected = text
    for abbr in _ABBREVIATIONS:
        protected = protected.replace(abbr, abbr.replace(".", "\x00"))
    parts = _SENT_SPLIT_RE.split(protected.strip())
    return [p.replace("\x00", ".").strip() for p in parts if p.strip()]


def count_words(text: str) -> int:
    return len(text.split())


def coerce_sentences(structured_sentences) -> list[str]:
    coerced = []
    for entry in structured_sentences or []:
        if isinstance(entry, dict):
            text = str(entry.get("text", "")).strip()
        else:
            text = str(entry).strip()
        if text:
            coerced.append(text)
    return coerced


def validate(text: str, strict_words: bool = True, structured_sentences=None) -> dict:
    sentences = coerce_sentences(structured_sentences) or split_sentences(text)
    words = count_words(text)
    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("single paragraph", "\n\n" not in text, "Body must not contain blank-line paragraph breaks.")
    add("sentence count", len(sentences) == 7, f"Found {len(sentences)} sentences.")
    add("word count", words <= 156 if strict_words else words <= 170, f"Found {words} words.")
    add("no headings", not HEADING_RE.search(text), "No markdown headings allowed in body.")
    add("no links", not LINK_RE.search(text), "No links or DOI links allowed in body.")
    add(
        "result sentence has interval",
        len(sentences) >= 4 and bool(INTERVAL_RE.search(sentences[3]) or QUANT_RE.search(sentences[3])),
        "Sentence 4 should include a quantitative result such as a percentage, count, or interval.",
    )
    add(
        "result sentence has estimand",
        len(sentences) >= 4 and bool(ESTIMATE_RE.search(sentences[3])),
        "Sentence 4 should name an effect measure or test metric.",
    )
    add(
        "boundary sentence present",
        len(sentences) >= 7
        and any(kw in sentences[6].lower() for kw in [
            "is limited", "are limited", "limited by", "limited to", "limitation",
            "cannot", "may not", "could not", "does not", "do not extend",
            "unclear", "uncertain", "caution", "warrant",
            "scope", "boundary", "harm", "restrict", "constrain",
            "exclude", "generali", "not generali",
        ]),
        "Sentence 7 should express a limitation, harm, or scope boundary.",
    )

    return {
        "word_count": words,
        "sentence_count": len(sentences),
        "checks": checks,
        "ok": all(check["ok"] for check in checks),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an E156 body.")
    parser.add_argument("--file", help="Path to text or JSON file.")
    parser.add_argument("--json-field", help="Read body from a field inside a JSON file.")
    parser.add_argument("--stdin", action="store_true", help="Read body text from stdin.")
    parser.add_argument("--max-156", action="store_true", help="Allow up to 156 words instead of exactly 156.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    text = load_text(args)
    result = validate(text, strict_words=not args.max_156)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"word_count: {result['word_count']}")
    print(f"sentence_count: {result['sentence_count']}")
    print(f"overall: {'PASS' if result['ok'] else 'FAIL'}")
    for check in result["checks"]:
        status = "PASS" if check["ok"] else "FAIL"
        print(f"- {status}: {check['name']} | {check['detail']}")


if __name__ == "__main__":
    main()
