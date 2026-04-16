"""Verify every entry on the live student board has complete SUBMISSION
METADATA — per-paper body, references, GitHub code + dashboard URLs,
data availability, ethics, funding, COI, CRediT, AI disclosure.

Parses the ENTRIES JSON inlined in students.html and counts how many
of 485 entries carry each field. Flags any entry that's missing any
of the required fields so the workbook can be repaired.

Run:
  python verify_student_board.py                # stdout summary
  python verify_student_board.py --detail       # list every missing-field entry
"""
from __future__ import annotations
import argparse
import io
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

STUDENTS_HTML = Path(__file__).resolve().parents[1] / "students.html"

REQUIRED = [
    ("body",                 "156-word body"),
    ("code_url",             "Source code URL"),
    ("protocol_url",         "Protocol URL"),
    ("pages_url",            "Dashboard URL"),
    ("references",           "References (≥2)"),
    ("data_availability",    "Data availability statement"),
    ("ethics",               "Ethics statement"),
    ("funding",              "Funding statement"),
    ("competing_interests",  "Competing interests (COI)"),
    ("credit",               "CRediT authorship"),
    ("ai_disclosure",        "AI disclosure"),
    ("target_journal",       "Target journal line"),
    ("corresponding_author", "Corresponding author"),
    ("orcid",                "ORCID"),
    ("affiliation",          "Affiliation"),
    ("reporting_checklist",  "Reporting checklist"),
]


def load_entries() -> list[dict]:
    text = STUDENTS_HTML.read_text(encoding="utf-8")
    m = re.search(r"const ENTRIES = (\[.+?\]);", text, re.DOTALL)
    if not m:
        raise SystemExit("Could not find `const ENTRIES = [...]` in students.html")
    return json.loads(m.group(1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--detail", action="store_true")
    args = ap.parse_args()

    entries = load_entries()
    total = len(entries)
    print(f"Entries in students.html: {total}")
    print()

    # Count presence per field
    stats: dict[str, dict] = {}
    for key, label in REQUIRED:
        present = 0
        missing_nums: list[tuple[int, str]] = []
        for e in entries:
            v = e.get(key, "")
            ok = False
            if key == "references":
                ok = isinstance(v, list) and len(v) >= 2
            elif isinstance(v, str):
                ok = bool(v.strip())
            if ok:
                present += 1
            else:
                missing_nums.append((e.get("num", "?"), e.get("name", "?")))
        pct = 100.0 * present / total if total else 0
        stats[key] = {"label": label, "present": present, "missing": missing_nums, "pct": pct}

    # Summary
    print(f"{'Field':<28}  Present / Total   %    Status")
    print("-" * 70)
    all_clean = True
    for key, label in REQUIRED:
        s = stats[key]
        status = "PASS" if s["present"] == total else "FAIL"
        if status == "FAIL":
            all_clean = False
        print(f"{label:<28}  {s['present']:>5} / {total:<5}  {s['pct']:>5.1f}%  {status}")

    # Entries missing one or more required fields
    print()
    per_entry_issues: dict[int, list[str]] = {}
    for key, label in REQUIRED:
        for num, _name in stats[key]["missing"]:
            per_entry_issues.setdefault(num, []).append(key)
    clean_count = total - len(per_entry_issues)
    print(f"Entries with every required field populated: {clean_count} / {total}")
    print(f"Entries missing ≥1 required field: {len(per_entry_issues)}")

    if args.detail and per_entry_issues:
        print()
        print("Detail (first 40):")
        by_num = {e.get("num"): e for e in entries}
        for num in sorted(per_entry_issues)[:40]:
            e = by_num.get(num, {})
            print(f"  [{num}] {e.get('name', '?'):<30} missing: {', '.join(per_entry_issues[num])}")

    return 0 if all_clean else 1


if __name__ == "__main__":
    sys.exit(main())
