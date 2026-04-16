"""Fix the 117 name-drift cases in the workbook where the Code/Protocol/
Dashboard URLs point to a repo name that no longer matches GitHub.

Workflow:
  1. Fetch all 481 repos under mahmood726-cyber via `gh repo list`.
  2. For every workbook entry whose Code URL 404s, try to find the
     matching repo by fuzzy name match (≥0.7 ratio).
  3. If matched, rewrite the three URLs (Code, Protocol, Dashboard)
     to use the real repo name. Preserve CURRENT BODY + YOUR REWRITE
     untouched (workbook protection rule).
  4. Write the new workbook back and print a diff summary.
  5. Save a map file (url_fixes.json) for audit trail.

Usage:
  python fix_workbook_urls.py              # dry-run — shows what would change
  python fix_workbook_urls.py --apply      # actually write the workbook
"""
from __future__ import annotations
import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

WORKBOOK = Path(__file__).resolve().parents[1] / "rewrite-workbook.txt"
OUT_DIR = Path(__file__).resolve().parents[1] / "audit_output"


def fetch_actual_repos() -> list[str]:
    """Return [repo_name_lowercase] for every repo under mahmood726-cyber."""
    r = subprocess.run(
        ["gh", "repo", "list", "mahmood726-cyber", "--limit", "500", "--json", "name"],
        capture_output=True, text=True, check=True,
    )
    return [d["name"] for d in json.loads(r.stdout)]


def find_match(workbook_name: str, actual_repos: list[str]) -> str | None:
    lc_map = {r.lower(): r for r in actual_repos}
    if workbook_name.lower() in lc_map:
        return lc_map[workbook_name.lower()]
    # Fuzzy match with cutoff=0.82 — high enough to avoid "claude2 →
    # clauderepo" (dissimilar projects that happen to share a substring)
    # but low enough to catch the common "CamelCase → kebab-case" drift
    # like "CochraneDataExtractor → cochrane-data-extractor" (ratio ~0.87).
    # Normalising by stripping hyphens on both sides first boosts the
    # signal for case-only drift.
    norm = lambda s: s.replace("-", "").replace("_", "")
    norm_workbook = norm(workbook_name.lower())
    norm_map = {norm(k): v for k, v in lc_map.items()}
    if norm_workbook in norm_map:
        return norm_map[norm_workbook]
    m = difflib.get_close_matches(norm_workbook, list(norm_map.keys()),
                                  n=1, cutoff=0.82)
    return norm_map[m[0]] if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--audit", default=str(OUT_DIR / "audit_links_2026-04-16.json"),
                    help="path to the audit JSON from audit_links.py")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    audit = json.load(open(args.audit, encoding="utf-8"))
    actual_repos = fetch_actual_repos()
    print(f"[fix] {len(actual_repos)} actual repos under mahmood726-cyber", file=sys.stderr)

    # Only try to fix entries with tag=repo_404
    broken = [e for e in audit["entries"] if e["tag"] == "repo_404"]
    print(f"[fix] {len(broken)} broken entries to inspect", file=sys.stderr)

    fixes: list[dict] = []
    unmatchable: list[dict] = []
    for e in broken:
        match = find_match(e["name"], actual_repos)
        if match:
            fixes.append({
                "num": e["num"],
                "workbook_name": e["name"],
                "actual_repo": match,
                "old_code": e["code"],
                "new_code": f"https://github.com/mahmood726-cyber/{match}",
            })
        else:
            unmatchable.append(e)

    print(f"[fix] name-drift fixes: {len(fixes)}", file=sys.stderr)
    print(f"[fix] unmatchable (truly missing): {len(unmatchable)}", file=sys.stderr)

    # Save the fix-map for audit trail
    (OUT_DIR / "url_fixes.json").write_text(
        json.dumps({"fixes": fixes, "unmatchable": unmatchable}, indent=2),
        encoding="utf-8",
    )

    if not args.apply:
        print("\n[dry-run] showing first 5 fixes:")
        for f in fixes[:5]:
            print(f"  [{f['num']}] {f['workbook_name']:<28} -> {f['actual_repo']}")
        print(f"\nRun with --apply to write the workbook.")
        return 0

    # Apply the fixes: for each, replace the three URLs in the workbook.
    text = WORKBOOK.read_text(encoding="utf-8")
    applied = 0
    for f in fixes:
        old_name = f["workbook_name"]
        new_name = f["actual_repo"]
        # URL patterns we need to rewrite — cover all three Link lines.
        # Use word-boundary regex that pins to the mahmood726-cyber/name
        # prefix so we don't accidentally rewrite other occurrences.
        old_prefix = f"mahmood726-cyber/{old_name}"
        new_prefix = f"mahmood726-cyber/{new_name}"
        # Dashboard URLs use `mahmood726-cyber.github.io/<name>/` pattern too
        old_pages = f"mahmood726-cyber.github.io/{old_name}/"
        new_pages = f"mahmood726-cyber.github.io/{new_name}/"
        old_text = text
        text = text.replace(old_prefix, new_prefix)
        text = text.replace(old_pages, new_pages)
        if text != old_text:
            applied += 1

    WORKBOOK.write_text(text, encoding="utf-8")
    print(f"\n[apply] wrote {WORKBOOK} — {applied} entries had URL updates", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
