#!/usr/bin/env python
"""Sync the approved E156 format-paper body (workbook entry [351], CURRENT BODY,
142 words, 7 sentences) into the e156-submission page data + render. This only
propagates the EXISTING authoritative workbook text; it does not author new
content and does not touch the (empty) YOUR REWRITE.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SUB = os.path.join(ROOT, "e156-submission")

TITLE = ("E156: A Compact Evidence-Synthesis Micro-Paper Format for "
         "Standardized Reporting of Meta-Analytic Results")
ESTIMAND = ("Format compliance rate (proportion meeting the 7-sentence, "
            "156-word constraint)")
SENTENCES = [
    "Can a fixed 7-sentence, 156-word micro-paper format standardize the reporting "
    "of meta-analytic results while preserving essential information for clinical "
    "decision-making?",
    "We developed the E156 specification requiring exactly seven sentences covering "
    "question, dataset, method, result, robustness, interpretation, and limitation "
    "within a maximum of 156 words.",
    "The format was applied to 339 meta-analysis projects spanning pairwise, network, "
    "diagnostic accuracy, and prevalence synthesis types.",
    "All 339 entries achieved full compliance with the 7-sentence constraint, and mean "
    "word count was 152.4 (range 138 to 156) demonstrating the format accommodates "
    "diverse study designs.",
    "An interactive library dashboard and batch validation pipeline enforce compliance "
    "automatically, with scripts for workbook management, GitHub deployment, and "
    "protocol timestamping.",
    "The E156 format enables rapid editorial triage, systematic comparison across "
    "evidence syntheses, and machine-readable extraction of key results.",
    "The format cannot capture nuanced subgroup analyses or complex network geometries "
    "that require extended narrative.",
]
BODY = " ".join(SENTENCES)
SUMMARY = ("A fixed 7-sentence, 156-word reporting format for evidence syntheses, "
           "applied to 339 meta-analyses with full compliance.")
WORDS = len(BODY.split())


def patch_index():
    p = os.path.join(SUB, "index.html")
    t = open(p, "rb").read().decode("utf-8", "replace")
    reps = [
        ('"title": "Untitled E156",',
         '"title": ' + json.dumps(TITLE) + ',\n  "sentences": ' + json.dumps(SENTENCES) + ','),
        ('"summary": "",', '"summary": ' + json.dumps(SUMMARY) + ','),
        ('"primary_estimand": "",', '"primary_estimand": ' + json.dumps(ESTIMAND) + ','),
        ('"study_count": null,', '"study_count": 339,'),
        ('"body": "",', '"body": ' + json.dumps(BODY) + ','),
    ]
    for old, new in reps:
        assert t.count(old) == 1, f"index.html anchor not unique: {old[:40]!r} ({t.count(old)})"
        t = t.replace(old, new, 1)
    open(p, "wb").write(t.encode("utf-8"))
    print("index.html: D object populated (title, sentences, body, estimand, n=339)")


def patch_paper_json():
    p = os.path.join(SUB, "paper.json")
    d = json.load(open(p, encoding="utf-8"))
    d["title"] = TITLE
    d["body"] = BODY
    d["sentences"] = SENTENCES
    d["summary"] = SUMMARY
    d["word_count"] = WORDS
    d["sentence_count"] = len(SENTENCES)
    d["primary_estimand"] = ESTIMAND
    d["type"] = "methods"
    d["study_count"] = 339
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"paper.json: title + body ({WORDS} words, {len(SENTENCES)} sentences)")


def patch_paper_md():
    p = os.path.join(SUB, "paper.md")
    t = open(p, encoding="utf-8", errors="replace").read()
    assert t.count("Untitled E156") == 1, "paper.md title anchor not unique"
    # replace the title line and append the body beneath it
    t = t.replace("Untitled E156", TITLE + "\n\n" + BODY, 1)
    open(p, "w", encoding="utf-8").write(t)
    print("paper.md: title + body inserted")


def main():
    print(f"syncing format paper #351 ({WORDS} words):")
    patch_index()
    patch_paper_json()
    patch_paper_md()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
