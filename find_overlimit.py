#!/usr/bin/env python
"""List E156 workbook entries whose CURRENT BODY exceeds 156 words, with the
overage, type, and SUBMITTED status (frozen entries must not be edited)."""
import re
import os

WB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rewrite-workbook.txt")


def entries(t):
    # split keeping the [n/m] marker
    parts = re.split(r"(\n\[\d+/\d+\]\s)", t)
    out = []
    for i in range(1, len(parts), 2):
        marker = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        out.append((marker, body))
    return out


def main():
    t = open(WB, encoding="utf-8", errors="replace").read()
    over = []
    for marker, e in entries(t):
        mw = re.search(r"CURRENT BODY \((\d+) words\):\n(.+?)\n\n", e, re.S)
        if not mw:
            continue
        declared = int(mw.group(1))
        body = mw.group(2)
        actual = len(body.split())
        if actual <= 156:
            continue
        ty = (re.search(r"TYPE:\s*([^|\n]+)", e) or [None, "?"])
        ty = ty.group(1).strip() if hasattr(ty, "group") else "?"
        submitted = "[x]" in (re.search(r"SUBMITTED:\s*(\[[ xX]\])", e) or [None, "[ ]"]).group(1) \
            if re.search(r"SUBMITTED:\s*(\[[ xX]\])", e) else False
        title = (re.search(r"TITLE:\s*([^\n]+)", e) or [None, "?"])
        title = title.group(1).strip()[:50] if hasattr(title, "group") else "?"
        over.append((marker, actual, actual - 156, ty, submitted, title))
    over.sort(key=lambda r: -r[2])
    sub = sum(1 for r in over if r[4])
    print(f"{len(over)} entries > 156 words  ({sub} SUBMITTED/frozen, {len(over)-sub} editable)\n")
    print(f"{'marker':12} {'words':>5} {'over':>4} {'subm':>4}  type / title")
    for m, w, o, ty, s, title in over:
        print(f"{m:12} {w:>5} {o:>4} {'FRZ' if s else '':>4}  {ty[:14]:14} {title}")
    import statistics as st
    overs = [r[2] for r in over]
    print(f"\noverage: max={max(overs)} mean={st.mean(overs):.1f} "
          f">10 over: {sum(1 for o in overs if o>10)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
