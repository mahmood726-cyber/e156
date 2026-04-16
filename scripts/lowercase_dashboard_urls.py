"""Lowercase the repo-name portion of every Dashboard URL in the workbook.

GitHub Pages at `<user>.github.io/<repo>/` normalises the repo path to
lowercase. The workbook's Dashboard URLs used whatever case the entry
name had (often CamelCase or PascalCase). This caused hundreds of
false-404s in the link audit.

This script finds every `mahmood726-cyber.github.io/<anything>/` URL
and lowercases the `<anything>` segment, leaving the rest of the URL
and all other workbook text untouched.

Only modifies SUBMISSION METADATA `Dashboard:` lines — we do NOT
touch Code or Protocol URLs (those live at github.com which IS case-
sensitive).

Run:
  python lowercase_dashboard_urls.py            # dry-run + count
  python lowercase_dashboard_urls.py --apply    # write the workbook
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

WORKBOOK = Path(__file__).resolve().parents[1] / "rewrite-workbook.txt"

# Match a Dashboard: line that points at github.io. We only want to
# lowercase the path segment AFTER the user subdomain.
DASH_RE = re.compile(
    r"(Dashboard:\s*https://mahmood726-cyber\.github\.io/)([^/\s]+)(/?)",
    re.IGNORECASE,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = WORKBOOK.read_text(encoding="utf-8")
    matches = list(DASH_RE.finditer(text))
    to_change = [m for m in matches if m.group(2) != m.group(2).lower()]
    unchanged = len(matches) - len(to_change)

    print(f"[lowercase] {len(matches)} Dashboard URLs total")
    print(f"  {len(to_change)} have uppercase letters -> will be lowercased")
    print(f"  {unchanged} already lowercase -> leave alone")

    if not to_change:
        print("Nothing to do.")
        return 0

    # Show first 8 examples
    print("\nFirst 8 changes:")
    for m in to_change[:8]:
        print(f"  {m.group(2)} -> {m.group(2).lower()}")

    if not args.apply:
        print("\n[dry-run] Re-run with --apply to write the workbook.")
        return 0

    def _lower(m: re.Match) -> str:
        return m.group(1) + m.group(2).lower() + m.group(3)

    new_text = DASH_RE.sub(_lower, text)
    WORKBOOK.write_text(new_text, encoding="utf-8")
    print(f"\n[apply] wrote {WORKBOOK} — {len(to_change)} URLs lowercased.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
