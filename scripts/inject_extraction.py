#!/usr/bin/env python
"""Inject agent-produced data extraction into a capsule.

Companion to inject_screening.py. The auto-extraction step is performed by the
host agentic CLI (Claude Code / Gemini) — the agent reads each trial's live
PubMed abstract and extracts the fields the abstract supports, each with the
verbatim sentence it came from (data/extraction-live.json). This injector
validates that file and writes it into the capsule as EXTRACT_LIVE between
  /*EXTRACT_START*/ ... /*EXTRACT_END*/
so the extraction panel shows genuine, source-verified values.

Extraction file shape:
  { "_meta": {...}, "extractions": { "<nct>": { "fields": [
      {"k": "label", "v": "value", "snip": "verbatim source sentence", "c": 0.0-1.0}, ... ] } } }

Fail-closed: missing file/markers or a malformed field stops the run.

Usage:
  python scripts/inject_extraction.py --extraction data/extraction-live.json \
      --capsule flagship/sglt2-hf-capsule.html [--dry-run]
"""
import argparse
import io
import json
import os
import re
import sys

if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

START, END = "/*EXTRACT_START*/", "/*EXTRACT_END*/"


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Inject agent data extraction (EXTRACT_LIVE) into a capsule.")
    ap.add_argument("--extraction", required=True)
    ap.add_argument("--capsule", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.extraction):
        die("extraction file not found: %s" % args.extraction)
    if not os.path.isfile(args.capsule):
        die("capsule not found: %s" % args.capsule)
    try:
        doc = json.load(open(args.extraction, encoding="utf-8"))
    except Exception as e:
        die("extraction file is not valid JSON: %s" % e)
    ex = doc.get("extractions", doc)
    if not isinstance(ex, dict) or not ex:
        die("no 'extractions' object found in %s" % args.extraction)

    n_fields = 0
    for nct, rec in ex.items():
        fields = rec.get("fields") if isinstance(rec, dict) else None
        if not isinstance(fields, list) or not fields:
            die("no fields for %s" % nct)
        for f in fields:
            if not all(k in f for k in ("k", "v", "snip")):
                die("field for %s missing k/v/snip" % nct)
            c = f.get("c", 1)
            if not isinstance(c, (int, float)) or not (0 <= c <= 1):
                die("confidence for a %s field must be 0-1" % nct)
            n_fields += 1

    obj = json.dumps(ex, ensure_ascii=False, separators=(",", ":"))
    html = open(args.capsule, encoding="utf-8").read()
    if START not in html or END not in html:
        die("capsule missing %s ... %s markers (add: const EXTRACT_LIVE=%s{}%s;)" % (START, END, START, END))
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), START + obj + END, html, flags=re.S)

    meta = doc.get("_meta", {})
    print("Extraction: %d trials, %d fields — extracted_by: %s" % (
        len(ex), n_fields, meta.get("extracted_by", "—")))
    if args.dry_run:
        print("[dry-run] would inject EXTRACT_LIVE into %s" % args.capsule)
        return
    with open(args.capsule, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("Injected EXTRACT_LIVE into %s" % args.capsule)


if __name__ == "__main__":
    main()
