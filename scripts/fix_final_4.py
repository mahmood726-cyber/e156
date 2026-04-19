"""Fix the last 4 remaining issues from the final re-verification.

- #339 Pairwise70        lowercase URL typo   -> Pairwise70 (real repo case)
- #351 DCB_PAD_LivingMeta lowercase URL typo  -> DCB_PAD_LivingMeta
- #352 Orforglipron_LivingMeta lowercase URL typo -> Orforglipron_LivingMeta
- #415 Finerenone clinical MA shares FINERENONE_REVIEW.html with #57
        (software article) — remap #415 to its per-paper info page so
        every dashboard URL on the board is unique.
"""
from __future__ import annotations
import io
import re
import shutil
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
BAK = E156 / "rewrite-workbook.txt.bak.phase-final"
SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)

# Per-num fix: (old-substring-in-block, new-substring)
FIXES = {
    339: ("https://mahmood726-cyber.github.io/pairwise70/",
          "https://mahmood726-cyber.github.io/Pairwise70/"),
    351: ("https://mahmood726-cyber.github.io/dcb_pad_livingmeta/",
          "https://mahmood726-cyber.github.io/DCB_PAD_LivingMeta/"),
    352: ("https://mahmood726-cyber.github.io/orforglipron_livingmeta/",
          "https://mahmood726-cyber.github.io/Orforglipron_LivingMeta/"),
    415: ("https://mahmood726-cyber.github.io/rapidmeta-finerenone/FINERENONE_REVIEW.html",
          "https://mahmood726-cyber.github.io/e156/paper/415.html"),
}


def main() -> int:
    shutil.copy2(WORKBOOK, BAK)
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)

    block_of: dict[int, int] = {}
    for idx, block in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(block)
        if m:
            num = int(m.group(1))
            if num not in block_of:
                block_of[num] = idx

    changed = 0
    for num, (old, new) in FIXES.items():
        if num not in block_of:
            print(f"  #{num}: SKIP (block not found)")
            continue
        idx = block_of[num]
        if old not in blocks[idx]:
            print(f"  #{num}: SKIP (old URL not present)")
            continue
        blocks[idx] = blocks[idx].replace(old, new, 1)
        print(f"  #{num}: {old} -> {new}")
        changed += 1

    WORKBOOK.write_text(SEP.join(blocks), encoding="utf-8")
    print(f"Changed {changed}/4. Backup: {BAK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
