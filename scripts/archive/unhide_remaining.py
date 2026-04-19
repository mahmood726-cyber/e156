"""Open-access final pass — un-hide the remaining 10 papers.

For 6 cross-owner papers (pushed by push_cross_owner.py to mahmood726-cyber):
  just remove from hide_repo_404.json.

For 4 no-code papers (#48 DTA_Pro_Review, #123 NMAhtml, #353
TrialDiversityAtlas, #252 hfpef_registry_calibration): rewrite the
workbook's Code / Protocol URLs to the E156 paper info page, since no
real code repo exists (dirs missing or too big). Students still get the
paper body + metadata; the "code ↗" button points to the info page
instead of a dead 404.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
HIDE_LIST = E156 / "audit_output" / "hide_repo_404.json"
SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)

CROSS_OWNER_NUMS = {1, 18, 19, 20, 51, 146}  # pushed separately
NO_CODE_NUMS = {48, 123, 252, 353}            # route URLs to paper page

NEW_BASE = "https://mahmood726-cyber.github.io/e156/paper"


def main() -> int:
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)
    block_of: dict[int, int] = {}
    for idx, b in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(b)
        if m:
            num = int(m.group(1))
            if num not in block_of:
                block_of[num] = idx

    # For the 4 no-code papers: rewrite Code and Protocol URLs to point
    # at the E156 paper info page.
    rewritten = 0
    for num in NO_CODE_NUMS:
        if num not in block_of:
            print(f"  SKIP #{num}: no workbook block")
            continue
        b = blocks[block_of[num]]
        new_url = f"{NEW_BASE}/{num}.html"
        new_b = re.sub(r"(Code:\s+)(\S+)", lambda m: m.group(1) + new_url, b, count=1)
        new_b = re.sub(r"(Protocol:\s+)(\S+)", lambda m: m.group(1) + new_url, new_b, count=1)
        # Dashboard already points to paper page from earlier pass, but ensure it
        new_b = re.sub(r"(Dashboard:\s+)(\S+)", lambda m: m.group(1) + new_url, new_b, count=1)
        if new_b != b:
            blocks[block_of[num]] = new_b
            rewritten += 1
            print(f"  #{num}: routed Code/Protocol/Dashboard -> {new_url}")

    WORKBOOK.write_text(SEP.join(blocks), encoding="utf-8")
    print(f"Rewrote {rewritten}/{len(NO_CODE_NUMS)} no-code blocks")

    # Un-hide ALL 10
    hide = set(json.loads(HIDE_LIST.read_text(encoding="utf-8")))
    before = len(hide)
    target_unhide = CROSS_OWNER_NUMS | NO_CODE_NUMS
    hide -= target_unhide
    HIDE_LIST.write_text(json.dumps(sorted(hide)) + "\n", encoding="utf-8")
    print(f"Hide list: {before} -> {len(hide)} ({before - len(hide)} un-hidden)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
