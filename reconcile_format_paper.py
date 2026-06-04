#!/usr/bin/env python
"""Reconcile the stale figures in the E156 format paper (#351) against the live
workbook. Synthesis/meta-analysis-type entries (the paper's stated scope:
pairwise, network, DTA, prevalence) computed from rewrite-workbook.txt:
  n = 1312, all <=156 words (100% compliant), mean 155.5, range 118-156.

Number updates (word count unchanged at 142):
  '339 meta-analysis projects' -> '1312 meta-analysis projects'
  'All 339 entries'            -> 'All 1312 entries'
  'mean word count was 152.4 (range 138 to 156)'
                              -> 'mean word count was 155.5 (range 118 to 156)'

'Full compliance' is retained -- it remains TRUE for synthesis-type papers.
Applied to the submission artifacts and the workbook CURRENT BODY for entry
[351] only (SUBMITTED:[ ], so editable); YOUR REWRITE untouched.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SUB = os.path.join(ROOT, "e156-submission")

PAIRS = [
    ("339 meta-analysis projects", "1312 meta-analysis projects"),
    ("All 339 entries", "All 1312 entries"),
    ("mean word count was 152.4 (range 138 to 156)",
     "mean word count was 155.5 (range 118 to 156)"),
]


def apply_pairs(text, scoped_label, expect_each=1):
    for old, new in PAIRS:
        c = text.count(old)
        assert c == expect_each, f"{scoped_label}: {old[:35]!r} found {c} (expected {expect_each})"
        text = text.replace(old, new)
    return text


def reconcile_submission():
    # paper.json
    pj = os.path.join(SUB, "paper.json")
    d = json.load(open(pj, encoding="utf-8"))
    d["body"] = apply_pairs(d["body"], "paper.json/body")

    def repl(s):
        for old, new in PAIRS:
            s = s.replace(old, new)
        return s
    d["sentences"] = [repl(s) for s in d["sentences"]]
    assert " ".join(d["sentences"]) == d["body"], "sentences must equal body after edit"
    d["study_count"] = 1312
    d["word_count"] = len(d["body"].split())
    json.dump(d, open(pj, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"paper.json reconciled (word_count={d['word_count']})")

    # paper.md
    pm = os.path.join(SUB, "paper.md")
    t = open(pm, encoding="utf-8", errors="replace").read()
    open(pm, "w", encoding="utf-8").write(apply_pairs(t, "paper.md"))
    print("paper.md reconciled")

    # index.html (D.body + D.sentences strings + study_count)
    ih = os.path.join(SUB, "index.html")
    t = open(ih, "rb").read().decode("utf-8", "replace")
    for old, new in PAIRS:
        # appears in both D.body and the matching D.sentences entry -> 2x
        c = t.count(old)
        assert c == 2, f"index.html: {old[:30]!r} found {c} (expected 2)"
        t = t.replace(old, new)
    assert t.count('"study_count": 339,') == 1
    t = t.replace('"study_count": 339,', '"study_count": 1312,', 1)
    open(ih, "wb").write(t.encode("utf-8"))
    print("index.html reconciled")


def reconcile_workbook():
    wb = os.path.join(ROOT, "rewrite-workbook.txt")
    t = open(wb, encoding="utf-8", errors="replace").read()
    a = t.find("[351/1873]")
    b = t.find("[352/1873]", a)
    assert a != -1 and b != -1 and b > a, "entry [351] boundaries not found"
    entry = t[a:b]
    entry2 = entry
    for old, new in PAIRS:
        entry2 = entry2.replace(old, new)   # plain replace-all within entry 351
    assert "339 meta-analysis projects" not in entry2 and "All 339 entries" not in entry2 \
        and "152.4" not in entry2, "stale figures remain in workbook entry"
    # word-count marker stays 142 (verify)
    body_m = re.search(r"CURRENT BODY \((\d+) words\):\n(.+?)\n\n", entry2, re.S)
    if body_m:
        actual = len(body_m.group(2).split())
        if str(actual) != body_m.group(1):
            entry2 = entry2.replace(f"CURRENT BODY ({body_m.group(1)} words)",
                                    f"CURRENT BODY ({actual} words)", 1)
    assert "YOUR REWRITE (at most 156 words, 7 sentences):\n\n" in entry2, "YOUR REWRITE must stay empty/intact"
    t = t[:a] + entry2 + t[b:]
    open(wb, "w", encoding="utf-8").write(t)
    print("rewrite-workbook.txt entry [351] reconciled (YOUR REWRITE untouched)")


def main():
    # submission artifacts already reconciled in the prior run; only the
    # workbook remains. Guard so this is safe to re-run.
    pj = json.load(open(os.path.join(SUB, "paper.json"), encoding="utf-8"))
    if "1312 meta" not in pj["body"]:
        reconcile_submission()
    else:
        print("submission already reconciled (skip)")
    reconcile_workbook()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
