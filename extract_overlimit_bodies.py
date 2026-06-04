#!/usr/bin/env python
"""Extract over-156-word workbook bodies to outputs/overlimit_bodies.json
(marker -> {wc, drop, body}) for careful manual trimming."""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
WB = os.path.join(ROOT, "rewrite-workbook.txt")
OUT = os.path.join(ROOT, "outputs", "overlimit_bodies.json")

t = open(WB, encoding="utf-8", errors="replace").read()
parts = re.split(r"(\n\[\d+/\d+\]\s)", t)
data = {}
for i in range(2, len(parts), 2):
    e = parts[i]
    m = re.search(r"CURRENT BODY \(\d+ words\):\n(.+?)\n\n", e, re.S)
    if not m:
        continue
    body = m.group(1)
    wc = len(body.split())
    if wc <= 156:
        continue
    marker = parts[i - 1].strip()
    data[marker] = {"wc": wc, "drop": wc - 156, "body": body}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(data, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"extracted {len(data)} over-limit bodies -> {OUT}")
