"""Two cleanups in one pass.

A. Fix #129 and #413 broken URLs and un-hide them.
   - #129 Pairwise70: workbook Code URL `pairwiseai70` doesn't exist; real
     repo is `Pairwise70`. Rewrite Code/Protocol/Dashboard URLs.
   - #413 ARNIHFLivingMA: workbook treats `ARNI_HF_REVIEW.html` as a repo
     name. The HTML actually lives inside `rapidmeta-finerenone`. Fix to
     code=rapidmeta-finerenone, dashboard=.../ARNI_HF_REVIEW.html.

B. Renumber duplicate [N/T] headers to unique high numbers 486-496.
   The workbook has 11 entries whose `[N/485]` number collides with a
   previous one — the build script dedupes by taking the first, so the
   second block's paper silently vanishes from the board. Rather than
   delete those entries, give them new unique numbers so they re-enter
   as distinct papers with their own /e156/paper/<num>.html dashboards.
"""
from __future__ import annotations
import io
import json
import re
import shutil
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
HIDE_LIST = E156 / "audit_output" / "hide_repo_404.json"
BAK = E156 / "rewrite-workbook.txt.bak.cleanup"
LOG = E156 / "audit_output" / "workbook_cleanup_log.json"

SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)

# Part A — URL fixes to un-hide
URL_FIXES = {
    129: [
        ("https://github.com/mahmood726-cyber/pairwiseai70",
         "https://github.com/mahmood726-cyber/Pairwise70"),
        ("https://mahmood726-cyber.github.io/pairwise70/",
         "https://mahmood726-cyber.github.io/Pairwise70/"),
    ],
    413: [
        # Bizarrely, workbook uses `ARNI_HF_REVIEW.html` as a repo name.
        # The real review HTML lives inside rapidmeta-finerenone.
        ("https://github.com/mahmood726-cyber/ARNI_HF_REVIEW.html/blob/main/E156-PROTOCOL.md",
         "https://github.com/mahmood726-cyber/rapidmeta-finerenone/blob/main/E156-PROTOCOL.md"),
        ("https://github.com/mahmood726-cyber/ARNI_HF_REVIEW.html",
         "https://github.com/mahmood726-cyber/rapidmeta-finerenone"),
        ("https://mahmood726-cyber.github.io/arni_hf_review.html/",
         "https://mahmood726-cyber.github.io/rapidmeta-finerenone/ARNI_HF_REVIEW.html"),
    ],
}

# Part B — renumber the SECOND occurrence of each duplicate number
#   Keep first block's number unchanged; assign a fresh number to the second.
RENUMBER_MAP = {
    # (original_num, occurrence_index_starting_at_0) -> new_num
    # Occurrence 1 (second block) gets a new number.
    (338, 1): 486,
    (339, 1): 487,
    (351, 1): 488,
    (352, 1): 489,
    (376, 1): 490,
    (377, 1): 491,
    (378, 1): 492,
    (389, 1): 493,
    (390, 1): 494,
    (391, 1): 495,
    (392, 1): 496,
}


def main() -> int:
    shutil.copy2(WORKBOOK, BAK)
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)

    log: dict[str, list] = {"url_fixes": [], "renumbered": [], "hide_list_changes": []}

    # Part A — URL fixes
    # Build num -> first block index
    block_of: dict[int, int] = {}
    for idx, b in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(b)
        if m:
            num = int(m.group(1))
            if num not in block_of:
                block_of[num] = idx

    for num, fixes in URL_FIXES.items():
        if num not in block_of:
            log["url_fixes"].append({"num": num, "status": "SKIP_no_block"})
            continue
        idx = block_of[num]
        applied = 0
        for old, new in fixes:
            if old in blocks[idx]:
                blocks[idx] = blocks[idx].replace(old, new, 1)
                applied += 1
        log["url_fixes"].append({"num": num, "applied": applied, "total": len(fixes)})
        print(f"  URL fix #{num}: {applied}/{len(fixes)} substitutions applied")

    # Part B — renumber second occurrences
    occurrences: dict[int, int] = {}
    for idx, b in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(b)
        if not m:
            continue
        num = int(m.group(1))
        occ = occurrences.setdefault(num, 0)
        occurrences[num] += 1
        if (num, occ) not in RENUMBER_MAP:
            continue
        new_num = RENUMBER_MAP[(num, occ)]
        # Rewrite the `[N/T]` line in this block only
        pattern = re.compile(rf"^\[{num}/(\d+)\]", re.MULTILINE)
        blocks[idx], n_subs = pattern.subn(f"[{new_num}/\\1]", blocks[idx], count=1)
        if n_subs:
            name_m = re.search(rf"^\[{new_num}/\d+\]\s*(.+)", blocks[idx], re.MULTILINE)
            log["renumbered"].append({
                "old_num": num, "new_num": new_num,
                "name": name_m.group(1).strip() if name_m else "?",
            })
            print(f"  Renumbered: #{num} (2nd) -> #{new_num} ({name_m.group(1).strip() if name_m else '?'})")

    # Write workbook
    WORKBOOK.write_text(SEP.join(blocks), encoding="utf-8")

    # Part A continued — un-hide #129 and #413
    hide = set(json.loads(HIDE_LIST.read_text(encoding="utf-8")))
    before = len(hide)
    for num in URL_FIXES:
        hide.discard(num)
    if len(hide) != before:
        HIDE_LIST.write_text(json.dumps(sorted(hide)) + "\n", encoding="utf-8")
        log["hide_list_changes"].append({
            "before": before, "after": len(hide),
            "unhidden": sorted({129, 413} - set(hide))
        })
        print(f"  Hide list: {before} -> {len(hide)} ({before - len(hide)} un-hidden)")

    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Backup: {BAK}")
    print(f"Log: {LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
