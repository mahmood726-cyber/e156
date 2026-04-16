"""Classify each workbook entry into its correct Synthēsis section.

Per the 2026-04-15 multi-persona review (P0-3): all 483 entries had been
hardcoded to `Section: Methods Note`, but Synthēsis offers three sections
and the corpus is mixed (empirical results, methods/tools, commentary).

Section policies (from journal author guidelines, verified 2026-04-15):
  - Methods Note      — innovations, analytical workflows, practical
                        lessons that improve transparency / reproducibility
                        of meta-analysis.
  - Short Meta-Analysis — concise empirical meta-analytic results.
  - Brief Update      — commentary, replication, or update on a prior
                        review.

Classification heuristic (transparent — students can override on the
SUBMISSION METADATA line if they prefer a different fit):

  1. If the entry's CURRENT BODY mentions explicit empirical pooled
     estimates with confidence intervals (e.g. "pooled OR 0.78 (95% CI ..."
     or "RR 0.81", "HR 0.92", "SMD 0.24") AND the project is positioned
     as reporting results, classify as `Short Meta-Analysis`.
  2. If the entry's TYPE field is `methods` OR the body emphasises tooling,
     workflows, software, packages, dashboards, or specifications,
     classify as `Methods Note`.
  3. If the body is a commentary / replication / response / update on
     prior work (keywords: "update", "replication", "commentary",
     "response", "reanalysis"), classify as `Brief Update`.
  4. Default fallback: `Short Meta-Analysis` for empirical-leaning
     entries, `Methods Note` for tool-leaning entries.

Run:
  python C:/E156/scripts/classify_journal_sections.py            # dry-run + counts
  python C:/E156/scripts/classify_journal_sections.py --apply    # rewrite workbook
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

WORKBOOK = Path(__file__).resolve().parents[1] / "rewrite-workbook.txt"

# Pattern that finds (1) the entry header so we can grab TITLE/TYPE/CURRENT
# BODY, and (2) the existing `Target journal: ◆ Synthēsis ... Section: X`
# block so we can rewrite it.
ENTRY_HEADER_RE = re.compile(
    r"\[(\d+)/\d+\]\s+(\S+)\s*\nTITLE:\s*(.+?)\s*\nTYPE:\s+(\S+)",
    re.MULTILINE,
)

CURRENT_BODY_RE = re.compile(
    r"CURRENT BODY \(\d+ words\):\s*\n(.+?)(?=\n\nYOUR REWRITE|\nYOUR REWRITE)",
    re.DOTALL,
)

SECTION_BLOCK_RE = re.compile(
    r"(Target journal: ◆ Synthēsis [^\n]+\n  Section: )(Methods Note|Short Meta-Analysis|Brief Update)"
    r"( \(≤400 words main text[^)]*\)\.)",
)

# Empirical effect-size patterns — strong signal for Short Meta-Analysis.
# We intentionally require a CI alongside the point estimate to avoid
# matching mention-only sentences.
EMPIRICAL_PATTERNS = [
    re.compile(r"\b(?:pooled\s+)?(?:OR|RR|HR|SMD|MD|aOR|aHR)\s*[=:]?\s*-?\d+\.\d+\s*(?:\([^)]*CI[^)]*\))", re.IGNORECASE),
    re.compile(r"\b\d+\.\d+\s*\(\s*95%\s*CI\s+\d+\.\d+", re.IGNORECASE),
    re.compile(r"\bprevalence\s+(?:was|of)\s+\d+\.?\d*\s*%", re.IGNORECASE),
    re.compile(r"\bpooled\s+(?:effect|estimate|proportion)\b", re.IGNORECASE),
]

# Tooling / methods signal.
METHODS_PATTERNS = [
    re.compile(r"\b(?:R\s+package|Python\s+package|tool|dashboard|pipeline|workflow|spec|specification|framework|library)\b", re.IGNORECASE),
    re.compile(r"\bwe\s+(?:built|developed|designed|implemented)\b.*\b(?:tool|package|engine|system|app|interface)\b", re.IGNORECASE),
    re.compile(r"\b(?:reproducibility|automation|standardiz|validation\s+harness)\b", re.IGNORECASE),
]

# Commentary / update signal.
UPDATE_PATTERNS = [
    re.compile(r"\b(?:replicat(?:e|ion|ed)|reanalys(?:is|ed)|response\s+to|commentary|update(?:d)?\s+(?:to|of))\b", re.IGNORECASE),
]


def classify(title: str, type_field: str, body: str) -> str:
    """Return one of: Methods Note / Short Meta-Analysis / Brief Update."""
    # Normalize for keyword search; titles often telegraph the kind.
    haystack = f"{title}\n{body}"

    # 1. Replication / commentary signal wins outright.
    if any(p.search(haystack) for p in UPDATE_PATTERNS):
        return "Brief Update"

    empirical_hits = sum(1 for p in EMPIRICAL_PATTERNS if p.search(haystack))
    methods_hits = sum(1 for p in METHODS_PATTERNS if p.search(haystack))

    # 2. TYPE field is the strongest authorial signal.
    type_lc = type_field.lower()
    if type_lc.startswith("methods"):
        return "Methods Note"
    if type_lc in {"empirical", "meta-analysis", "ma", "result"}:
        return "Short Meta-Analysis" if empirical_hits >= 1 else "Methods Note"

    # 3. Body-pattern majority.
    if empirical_hits > methods_hits:
        return "Short Meta-Analysis"
    if methods_hits > empirical_hits:
        return "Methods Note"

    # 4. Fallback — empirical is a safer default for the journal's
    # editorial triage than methods (a wrongly-routed methods note
    # gets reassigned faster than a wrongly-routed empirical paper).
    return "Short Meta-Analysis" if empirical_hits >= 1 else "Methods Note"


def split_entries(text: str) -> list[tuple[int, int, str]]:
    """Yield (start, end, entry_text) tuples, splitting on the
    `======================================================================`
    boundary that separates entries."""
    parts = text.split("\n======================================================================\n")
    out = []
    cursor = 0
    for i, part in enumerate(parts):
        end = cursor + len(part)
        if i > 0:
            cursor += len("\n======================================================================\n")
            end = cursor + len(part)
        out.append((cursor, end, part))
        cursor = end
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="Rewrite the workbook (default: dry-run + counts)")
    args = ap.parse_args()

    text = WORKBOOK.read_text(encoding="utf-8")
    counts = {"Methods Note": 0, "Short Meta-Analysis": 0, "Brief Update": 0, "unchanged": 0, "no_section_block": 0}
    rewrites: list[tuple[int, int, str]] = []  # (abs_start, abs_end, replacement)

    cursor = 0
    for entry in text.split("\n======================================================================\n"):
        # Skip the header preamble (no entry header) and trailing blanks.
        header_match = ENTRY_HEADER_RE.search(entry)
        if header_match:
            num = header_match.group(1)
            title = header_match.group(3)
            type_field = header_match.group(4)
            body_match = CURRENT_BODY_RE.search(entry)
            body = body_match.group(1).strip() if body_match else ""
            section = classify(title, type_field, body)

            section_match = SECTION_BLOCK_RE.search(entry)
            if not section_match:
                counts["no_section_block"] += 1
            else:
                if section_match.group(2) == section:
                    counts["unchanged"] += 1
                else:
                    counts[section] += 1
                    # Compute absolute offsets in the original text.
                    abs_start = text.find(entry, cursor)
                    if abs_start < 0:
                        # Defensive: should never happen since we split from text.
                        continue
                    seg_start = abs_start + section_match.start()
                    seg_end = abs_start + section_match.end()
                    replacement = section_match.group(1) + section + section_match.group(3)
                    rewrites.append((seg_start, seg_end, replacement))
        # Advance cursor past this segment + the boundary.
        cursor += len(entry) + len("\n======================================================================\n")

    print(f"[classify] {sum(counts[k] for k in ('Methods Note','Short Meta-Analysis','Brief Update'))} entries would be reclassified:")
    for k in ("Methods Note", "Short Meta-Analysis", "Brief Update"):
        print(f"  -> {k:<22}{counts[k]}")
    print(f"  unchanged (already correct): {counts['unchanged']}")
    if counts["no_section_block"]:
        print(f"  WARN: {counts['no_section_block']} entries have no Target-journal block (skipped)")

    if not args.apply:
        print("\n[dry-run] no files written. Re-run with --apply to write the workbook.")
        return 0

    # Apply rewrites in reverse so earlier offsets stay valid.
    rewrites.sort(reverse=True)
    new_text = text
    for start, end, replacement in rewrites:
        new_text = new_text[:start] + replacement + new_text[end:]

    WORKBOOK.write_text(new_text, encoding="utf-8")
    print(f"\n[apply] wrote {WORKBOOK} ({len(rewrites)} section lines updated)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
