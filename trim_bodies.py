#!/usr/bin/env python
"""Safe word-trimmer for over-156-word E156 bodies in the workbook.

Only applies a whitelist of meaning-preserving filler contractions + removal of
leading discourse markers. It NEVER edits a number: a trim is accepted for an
entry only if, after trimming, (a) word count <= 156, (b) sentence count is
unchanged (still 7), and (c) the ordered list of numeric tokens is identical to
the original. Anything it can't safely bring to <=156 is left for manual edit
and reported. Workbook entries only; YOUR REWRITE / SUBMITTED untouched.

Usage: python trim_bodies.py [--apply]
"""
import argparse
import os
import re

WB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rewrite-workbook.txt")

# mid-sentence contractions (space-bounded, never touch digits)
SUBS = [
    (" in order to ", " to "),
    (" due to the fact that ", " because "),
    (" a total of ", " "),
    (" was found to be ", " was "),
    (" were found to be ", " were "),
    (" has been shown to ", " "),
    (" have been shown to ", " "),
    (" in the setting of ", " in "),
    (" with respect to ", " for "),
    (" in comparison with ", " versus "),
    (" in comparison to ", " versus "),
    (" compared with ", " versus "),
    (" compared to ", " versus "),
    (" as well as ", " and "),
    (" the majority of ", " most "),
    (" a number of ", " several "),
    (" in spite of ", " despite "),
    (" for the purpose of ", " to "),
    (" in the context of ", " in "),
    (" it is important to note that ", " "),
    (" it should be noted that ", " "),
    (" there is evidence that ", " "),
    (" a variety of ", " various "),
    (" on the basis of ", " from "),
    (" in terms of ", " for "),
    (" with the exception of ", " except "),
    (" prior to ", " before "),
    (" subsequent to ", " after "),
]
# leading discourse markers (start of body or after . ? !)
LEAD = re.compile(r"(^|[.?!]\s)(Notably|Importantly|Furthermore|Moreover|"
                  r"Additionally|Crucially|Indeed|Remarkably|Strikingly|"
                  r"Of note,|Critically|Significantly),?\s+([a-z])")

NUMS = re.compile(r"\d[\d.,]*")
SENT = re.compile(r"[.?!](?:\s|$)")


def nums(s):
    return NUMS.findall(s)


def sentences(s):
    return len(SENT.findall(s))


def trim(body):
    b = body
    for _ in range(8):  # iterate; some subs expose others
        prev = b
        for old, new in SUBS:
            b = b.replace(old, new)
        b = LEAD.sub(lambda m: m.group(1) + m.group(3).upper(), b)
        b = re.sub(r"  +", " ", b)
        if b == prev:
            break
    return b.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    t = open(WB, encoding="utf-8", errors="replace").read()
    parts = re.split(r"(\n\[\d+/\d+\]\s)", t)
    fixed, residual, skipped = [], [], []
    for i in range(2, len(parts), 2):
        e = parts[i]
        m = re.search(r"(CURRENT BODY \()(\d+)( words\):\n)(.+?)(\n\n)", e, re.S)
        if not m:
            continue
        body = m.group(4)
        if len(body.split()) <= 156:
            continue
        marker = parts[i - 1].strip()
        if sentences(body) != 7:
            skipped.append((marker, "not 7 sentences"))
            continue
        nb = trim(body)
        wc = len(nb.split())
        safe = nums(nb) == nums(body) and sentences(nb) == 7
        if wc <= 156 and safe:
            new_e = e[:m.start()] + m.group(1) + str(wc) + m.group(3) + nb + m.group(5) + e[m.end():]
            parts[i] = new_e
            fixed.append((marker, len(body.split()), wc))
        else:
            reason = "numbers/sentences changed" if not safe else f"still {wc} words"
            residual.append((marker, len(body.split()), wc, reason))

    print(f"FIXED by safe trim: {len(fixed)}")
    print(f"RESIDUAL (need manual): {len(residual)}")
    if skipped:
        print(f"SKIPPED (malformed): {len(skipped)} {skipped[:3]}")
    print("\nresidual list (marker, orig, after-safe-trim, why):")
    for r in residual:
        print(f"  {r[0]:12} {r[1]} -> {r[2]}  ({r[3]})")

    if args.apply and fixed:
        open(WB, "w", encoding="utf-8").write("".join(parts))
        print(f"\nAPPLIED {len(fixed)} safe trims to workbook.")
    elif not args.apply:
        print("\n(dry-run; pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
