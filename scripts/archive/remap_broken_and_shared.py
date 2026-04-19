"""Track 4 continued — rewrite workbook Dashboard URLs that are broken
(404) or shared (multiple papers pointing to the same URL) to the new
per-paper pages at e156/paper/<num>.html.

Skips papers already remapped to specific rapidmeta-finerenone review
files in Track 3 (since those are real per-therapy tools, not generic).

Safety: never touch a Dashboard URL that currently 200s AND isn't shared.
Those are genuine working per-paper dashboards and must be preserved.
"""
from __future__ import annotations
import datetime as dt
import io
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
WORKBOOK_BAK = E156 / "rewrite-workbook.txt.bak.phase-d"
VERIFY_JSON = E156 / "audit_output" / f"board_verify_{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.json"
LOG = E156 / "audit_output" / "dashboard_final_remap_log.json"

SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
NEW_BASE = "https://mahmood726-cyber.github.io/e156/paper"

# Papers handled by Track 3 (Finrenone remap to specific per-therapy pages) —
# leave their Dashboard URL alone; it now points to the right file.
FINRENONE_TRACK3_NUMS = {57, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424,
                         430, 439, 441, 442, 443}


def load_shared_and_404_nums() -> set[int]:
    """Every paper num whose Dashboard URL is either 404 or shared."""
    r = json.loads(VERIFY_JSON.read_text(encoding="utf-8"))
    # 404 pages
    nums_404 = {e["num"] for e in r["per_entry"] if e["pages"].get("status") == 404}

    # Shared dashboards
    pages_to_nums = defaultdict(list)
    for e in r["per_entry"]:
        url = e["pages"].get("url")
        if url:
            pages_to_nums[url].append(e["num"])
    shared_nums: set[int] = set()
    for url, nums in pages_to_nums.items():
        if len(nums) > 1:
            shared_nums.update(nums)

    return nums_404 | shared_nums


def main() -> int:
    shutil.copy2(WORKBOOK, WORKBOOK_BAK)
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)

    block_of: dict[int, int] = {}
    for idx, block in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(block)
        if m:
            num = int(m.group(1))
            if num not in block_of:
                block_of[num] = idx

    targets = load_shared_and_404_nums() - FINRENONE_TRACK3_NUMS
    print(f"Target nums: {len(targets)} (excludes Finrenone Track 3 remaps)")

    log: dict[str, list] = {"remapped": [], "no_block": [], "no_dashboard_line": [],
                            "finrenone_excluded": sorted(FINRENONE_TRACK3_NUMS)}
    remapped_count = 0
    for num in sorted(targets):
        if num not in block_of:
            log["no_block"].append(num)
            continue
        idx = block_of[num]
        block = blocks[idx]
        m = re.search(r"(Dashboard:\s+)(\S+)", block)
        if not m:
            log["no_dashboard_line"].append(num)
            continue
        old_url = m.group(2)
        new_url = f"{NEW_BASE}/{num}.html"
        if old_url == new_url:
            continue
        blocks[idx] = re.sub(
            r"(Dashboard:\s+)(\S+)",
            lambda mm: mm.group(1) + new_url,
            block,
            count=1,
        )
        log["remapped"].append({"num": num, "from": old_url, "to": new_url})
        remapped_count += 1

    WORKBOOK.write_text(SEP.join(blocks), encoding="utf-8")
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Remapped: {remapped_count}")
    print(f"No workbook block: {len(log['no_block'])}")
    print(f"No Dashboard line: {len(log['no_dashboard_line'])}")
    print(f"Workbook backup: {WORKBOOK_BAK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
