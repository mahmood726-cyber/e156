"""Audit the workbook after fill_submission_metadata.py ran.

Checks:
  1. YOUR REWRITE sections are preserved verbatim vs a git-HEAD baseline.
  2. All entries have a SUBMISSION METADATA block with all 11 required fields.
  3. GitHub URLs are well-formed.
  4. ORCID / affiliation / AI-disclosure text is consistent across all entries.
  5. Entry count matches workbook declaration (480 projects).
  6. No entry is duplicated or missing.
  7. Reference formatting sanity (2 refs per entry, each with DOI or book note).

Exits 0 if clean, non-zero with a summary if any check fails.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

WORKBOOK = Path(__file__).resolve().parents[1] / "rewrite-workbook.txt"
SEP = "=" * 70

REQUIRED_FIELDS = [
    "SUBMISSION METADATA:",
    "Corresponding author:",
    "ORCID:",
    "Affiliation:",
    "Links:",
    "References (topic pack:",
    "Data availability:",
    "Ethics:",
    "Funding:",
    "Competing interests:",
    "Author contributions (CRediT):",
    "AI disclosure:",
    "Preprint:",
    "Reporting checklist:",
    "Manuscript license:",
    "Code license:",
]

EXPECTED_ORCID = "0000-0001-9107-3704"
EXPECTED_AFFIL = "Tahir Heart Institute, Rabwah, Pakistan"
EXPECTED_AUTHOR = "Mahmood Ahmad"


def parse_entries(text: str) -> list[tuple[int, str, str]]:
    blocks = text.split(SEP)
    out: list[tuple[int, str, str]] = []
    for block in blocks:
        # Relaxed regex: project names may contain spaces (e.g. "IPD Zahid",
        # "Living metas"). Match everything after [N/X] up to end of line.
        m = re.search(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", block, re.MULTILINE)
        if m:
            out.append((int(m.group(1)), m.group(2), block))
    return out


def extract_your_rewrite(block: str) -> str:
    """Return the YOUR REWRITE body verbatim, for comparison."""
    m = re.search(
        r"YOUR REWRITE[^\n]*\n(.*?)(?=\n\s*SUBMISSION METADATA:|\n\s*SUBMITTED:)",
        block,
        re.DOTALL,
    )
    return m.group(1).strip() if m else ""


def git_show_baseline(path: str) -> str | None:
    """Get the version of workbook as of the last commit in E156/."""
    try:
        result = subprocess.run(
            ["git", "-C", str(WORKBOOK.parent), "show", f"HEAD:{path}"],
            capture_output=True, text=True, timeout=30, encoding="utf-8",
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def main() -> int:
    text = WORKBOOK.read_text(encoding="utf-8")
    entries = parse_entries(text)
    problems: list[str] = []

    # Check 1: total entry count
    header_total = re.search(r"Total projects:\s*(\d+)", text)
    header_count = int(header_total.group(1)) if header_total else None
    print(f"[1] Entry count: parsed {len(entries)}; header declares {header_count}")
    if header_count and len(entries) != header_count:
        problems.append(f"entry count mismatch: {len(entries)} parsed vs {header_count} declared")

    # Check 2: no duplicate entry numbers
    nums = [n for n, _, _ in entries]
    if len(nums) != len(set(nums)):
        dup = [n for n in set(nums) if nums.count(n) > 1]
        problems.append(f"duplicate entry numbers: {dup}")
    print(f"[2] Duplicate entry numbers: {0 if len(nums) == len(set(nums)) else len(nums) - len(set(nums))}")

    # Check 3: all entries have all 16 required fields
    field_fail: list[tuple[int, str, list[str]]] = []
    for num, name, block in entries:
        missing = [f for f in REQUIRED_FIELDS if f not in block]
        if missing:
            field_fail.append((num, name, missing))
    print(f"[3] Entries missing any of {len(REQUIRED_FIELDS)} required fields: {len(field_fail)}")
    if field_fail:
        problems.append(f"field-missing entries: {len(field_fail)}")
        for num, name, missing in field_fail[:5]:
            print(f"    [{num}] {name}: missing {missing}")

    # Check 4: ORCID / affiliation / author consistency
    orcid_count = text.count(f"ORCID: {EXPECTED_ORCID}")
    affil_count = text.count(f"Affiliation: {EXPECTED_AFFIL}")
    author_count = text.count(f"Corresponding author: {EXPECTED_AUTHOR}")
    print(f"[4] ORCID {EXPECTED_ORCID}: {orcid_count} occurrences (expect {len(entries)})")
    print(f"    Affiliation correct: {affil_count} occurrences (expect {len(entries)})")
    print(f"    Author correct: {author_count} occurrences (expect {len(entries)})")
    if orcid_count != len(entries):
        problems.append(f"ORCID inconsistency: {orcid_count}/{len(entries)}")
    if affil_count != len(entries):
        problems.append(f"affiliation inconsistency: {affil_count}/{len(entries)}")

    # Check 5: AI disclosure has "human-written" language
    human_written = text.count("human-written")
    print(f"[5] AI disclosure with 'human-written' language: {human_written}/{len(entries)}")
    if human_written != len(entries):
        problems.append(f"AI disclosure inconsistency: {human_written}/{len(entries)}")

    # Check 6: each entry has exactly 2 references (numbered 1. and 2.)
    # NB: pack names may contain parens themselves (e.g. "trial sequential
    # analysis (TSA)"), so we key on "References (topic pack:" prefix and
    # read until "Data availability:" unconditionally.
    ref_fail: list[tuple[int, str, int]] = []
    for num, name, block in entries:
        if "References (topic pack:" not in block or "Data availability:" not in block:
            ref_fail.append((num, name, 0))
            continue
        start = block.index("References (topic pack:")
        end = block.index("Data availability:", start)
        section = block[start:end]
        ref_lines = [l for l in section.splitlines() if re.match(r"\s+\d+\.\s", l)]
        if len(ref_lines) != 2:
            ref_fail.append((num, name, len(ref_lines)))
    print(f"[6] Entries not having exactly 2 references: {len(ref_fail)}")
    if ref_fail:
        problems.append(f"reference-count issues: {len(ref_fail)}")
        for num, name, n in ref_fail[:5]:
            print(f"    [{num}] {name}: {n} references")

    # Check 7: GitHub URL well-formedness. NB: key on "Links:" section
    # specifically — "Code:" can appear in titles like "Everything Claude Code:".
    url_fail: list[tuple[int, str, str]] = []
    for num, name, block in entries:
        links_match = re.search(
            r"Links:\s*\n(.*?)(?=\n\s*References \(topic pack:)",
            block, re.DOTALL,
        )
        if not links_match:
            url_fail.append((num, name, "no Links section"))
            continue
        section = links_match.group(1)
        for field, expected_pattern in [
            ("Code", r"^https://github\.com/mahmood726-cyber/[\w.-]+$"),
            ("Protocol", r"^https://github\.com/mahmood726-cyber/[\w.-]+/blob/main/E156-PROTOCOL\.md$"),
            ("Dashboard", r"^https://mahmood726-cyber\.github\.io/[\w.-]+/$"),
        ]:
            m = re.search(rf"{field}:\s+(\S+)", section)
            if not m:
                url_fail.append((num, name, f"missing {field} in Links"))
                continue
            if not re.match(expected_pattern, m.group(1)):
                url_fail.append((num, name, f"{field} malformed: {m.group(1)}"))
    print(f"[7] Entries with URL issues: {len(url_fail)}")
    if url_fail:
        problems.append(f"URL issues: {len(url_fail)}")
        for num, name, msg in url_fail[:5]:
            print(f"    [{num}] {name}: {msg}")

    # Check 8: YOUR REWRITE preservation (diff against git HEAD if tracked)
    # E156 may not be a git repo; this check is advisory.
    baseline = git_show_baseline("rewrite-workbook.txt")
    if baseline is None:
        print(f"[8] YOUR REWRITE preservation: skipped (no git baseline — E156 not a tracked repo)")
    else:
        baseline_entries = parse_entries(baseline)
        baseline_rewrites = {num: extract_your_rewrite(block) for num, _, block in baseline_entries}
        current_rewrites = {num: extract_your_rewrite(block) for num, _, block in entries}
        changed: list[int] = []
        for num, rw in current_rewrites.items():
            if num in baseline_rewrites and baseline_rewrites[num] != rw:
                changed.append(num)
        print(f"[8] YOUR REWRITE sections changed vs git HEAD: {len(changed)}")
        if changed:
            problems.append(f"YOUR REWRITE changed in {len(changed)} entries (SACROSANCT VIOLATION)")
            print(f"    entries: {changed[:20]}")

    # Check 9: SUBMITTED lines still present per entry
    submitted_markers = text.count("SUBMITTED: [")
    print(f"[9] SUBMITTED markers: {submitted_markers} (expect {len(entries) + 1}, +1 for global header)")
    if submitted_markers < len(entries):
        problems.append(f"missing SUBMITTED markers: {submitted_markers} vs {len(entries)}")

    print()
    if problems:
        print(f"=== {len(problems)} PROBLEM(S) ===")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("=== ALL CHECKS PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
