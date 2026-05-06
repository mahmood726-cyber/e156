"""Pre-commit guard: refuse commits that bundle `[N/total]` denominator
sweeps with substantive `CURRENT BODY:` / `YOUR REWRITE:` / `SUBMITTED:`
content changes in the same diff.

Per the 8-persona blinded review (P0-2 Domain Expert + Red-Team double-flag):
commit `b94f34d` shipped a "denominator normalization" that also bundled
an end-to-end rewrite of entry 5's CURRENT BODY plus the insertion of
entry 678. Net diff was dominated by ~669 cosmetic `[N/549]→[N/678]`
swaps so the body change was invisible to skim review. For a journal
SUBMISSION HISTORY register this is an audit-trail integrity violation.

This guard inspects the staged diff of `rewrite-workbook.txt`. If both
of these are present in the same commit, it BLOCKs:
  - Any line matching `^[+-]\\[\\d+/\\d+\\] ` — denominator sweep marker
  - Any line matching `^[+-](TITLE:|TYPE:|ESTIMAND:|DATA:|PATH:)` outside
    a NEW entry block (i.e. mid-entry rewrites) OR any line touching
    `CURRENT BODY` / `YOUR REWRITE` / `SUBMITTED:` toggles.

Bypass: `E156_BUNDLED_OK=1 git commit ...` for an explicit operator override.

Exit code:
  0 — commit allowed
  1 — commit blocked (mixed denominator sweep + body change)
  2 — internal error (allowed, with stderr warning)
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

WORKBOOK = "rewrite-workbook.txt"


def _staged_diff(repo_root: Path) -> str | None:
    """Return staged diff for WORKBOOK, or None if not modified."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--unified=0", "--", WORKBOOK],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if out.returncode != 0:
            return None
        return out.stdout
    except Exception:
        return None


_RE_DENOM = re.compile(r"^[+-]\[\d+/\d+\]\s+\S")
_RE_BODY_FIELD = re.compile(
    r"^[+-](TITLE:|TYPE:|ESTIMAND:|DATA:|PATH:|CURRENT BODY|YOUR REWRITE|SUBMITTED:)"
)


def main() -> int:
    if os.environ.get("E156_BUNDLED_OK") == "1":
        return 0

    # Find repo root from this script's location.
    repo_root = Path(__file__).resolve().parents[1]
    diff = _staged_diff(repo_root)
    if diff is None or not diff:
        return 0

    denom_lines = [ln for ln in diff.splitlines() if _RE_DENOM.match(ln)]
    body_lines = [ln for ln in diff.splitlines() if _RE_BODY_FIELD.match(ln)]

    if not denom_lines:
        return 0  # not a denominator sweep
    if not body_lines:
        return 0  # pure denominator sweep

    # Allow body lines that are part of a brand-new entry (`+` only, no
    # corresponding `-`). A new entry's `+TITLE:` is OK; a mid-entry
    # rewrite shows BOTH `-TITLE:` and `+TITLE:`.
    minus_titles = sum(1 for ln in body_lines if ln.startswith("-"))
    plus_titles = sum(1 for ln in body_lines if ln.startswith("+"))
    if minus_titles == 0 and plus_titles >= 1:
        # All body changes are additions (a new entry block) — that's
        # OK alongside a denominator sweep iff the new entry is a
        # well-formed block. We don't deeply inspect; this is the
        # common safe case (new entry + sweep).
        return 0

    # Mixed: denominator sweep + body rewrite of an existing entry.
    print(
        "\n[E156 commit guard] BLOCK — this commit bundles a denominator\n"
        f"sweep ({len(denom_lines)} `[N/total]` line edits) with\n"
        f"{minus_titles} body-line removal(s) and {plus_titles} body-line\n"
        "addition(s) in existing entries.\n\n"
        "Per review-findings-session-2026-05-06.md P0-2: split the commit:\n"
        "  1. Stash body changes\n"
        "  2. Commit the denominator sweep alone\n"
        "  3. Pop the stash and commit body changes separately\n\n"
        "Bypass (only if the bundling is intentional):\n"
        "  E156_BUNDLED_OK=1 git commit -m '...'\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        # Don't block commits because the guard itself crashed.
        print(f"[E156 commit guard] internal error: {e!r}", file=sys.stderr)
        sys.exit(2)
