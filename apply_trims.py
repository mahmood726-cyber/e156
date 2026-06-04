#!/usr/bin/env python
"""Apply manually-authored trimmed bodies (outputs/trimmed_bodies.json: marker ->
new_body) back into the workbook, with strict verification per entry:
  - new word count <= 156
  - exactly 7 sentences
  - the ordered list of numeric tokens is IDENTICAL to the original body
A trim failing any check is rejected (not written) and reported.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
WB = os.path.join(ROOT, "rewrite-workbook.txt")
TRIMS = os.path.join(ROOT, "outputs", "trimmed_bodies.json")
ORIG = os.path.join(ROOT, "outputs", "overlimit_bodies.json")

NUMS = re.compile(r"\d[\d.,]*")
SENT = re.compile(r"[.?!](?:\s|$)")


def main():
    trims = json.load(open(TRIMS, encoding="utf-8"))
    orig = json.load(open(ORIG, encoding="utf-8"))
    t = open(WB, "rb").read().decode("utf-8", "replace")  # binary: preserve LF
    parts = re.split(r"(\n\[\d+/\d+\]\s)", t)
    applied, rejected = [], []
    marker_idx = {parts[i - 1].strip(): i for i in range(2, len(parts), 2)}

    for marker, nb in trims.items():
        nb = nb.strip()
        ob = orig[marker]["body"]
        wc = len(nb.split())
        problems = []
        if wc > 156:
            problems.append(f"{wc} words")
        if len(SENT.findall(nb)) != 7:
            problems.append(f"{len(SENT.findall(nb))} sentences")
        if NUMS.findall(nb) != NUMS.findall(ob):
            problems.append("numbers differ: "
                            f"{set(NUMS.findall(ob)) ^ set(NUMS.findall(nb))}")
        if problems:
            rejected.append((marker, problems))
            continue
        i = marker_idx[marker]
        e = parts[i]
        m = re.search(r"(CURRENT BODY \()\d+( words\):\n)(.+?)(\n\n)", e, re.S)
        assert m and m.group(3) == ob, f"{marker}: body mismatch vs original"
        parts[i] = e[:m.start()] + m.group(1) + str(wc) + m.group(2) + nb + m.group(4) + e[m.end():]
        applied.append((marker, orig[marker]["wc"], wc))

    if rejected:
        print(f"REJECTED {len(rejected)} (NOT written):")
        for mk, pr in rejected:
            print(f"  {mk}: {pr}")
    if applied and not rejected:
        open(WB, "wb").write("".join(parts).encode("utf-8"))
        print(f"APPLIED {len(applied)} trims.")
        for mk, a, b in applied:
            print(f"  {mk}: {a} -> {b}")
    elif rejected:
        print("\nNothing written (fix rejected entries first).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
