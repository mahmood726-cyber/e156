#!/usr/bin/env python
"""Inject agent-produced screening decisions into a capsule.

The AI auto-screening step is performed by the host agentic CLI itself (Claude
Code / Gemini CLI) — the orchestrating agent IS the model, so no separate API
key is needed. The agent reads each record's live abstract / registry summary,
applies the pre-registered eligibility criteria, and writes a decisions JSON
(data/screening-decisions.json). This injector validates that file and writes
the decisions into the capsule as SCREEN_LIVE, between the markers
  /*SCREEN_START*/ ... /*SCREEN_END*/
so the capsule prefers the genuine decision over its illustrative placeholder.

Decisions file shape:
  { "_meta": {...}, "decisions": { "<recordId>": {"decision":"include|exclude",
     "reason": "...", "confidence": 0.0-1.0 }, ... } }

Fail-closed: missing file/markers or an invalid decision stops the run.

Usage:
  python scripts/inject_screening.py --decisions data/screening-decisions.json \
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

START, END = "/*SCREEN_START*/", "/*SCREEN_END*/"


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Inject agent screening decisions (SCREEN_LIVE) into a capsule.")
    ap.add_argument("--decisions", required=True)
    ap.add_argument("--capsule", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.decisions):
        die("decisions file not found: %s" % args.decisions)
    if not os.path.isfile(args.capsule):
        die("capsule not found: %s" % args.capsule)
    try:
        doc = json.load(open(args.decisions, encoding="utf-8"))
    except Exception as e:
        die("decisions file is not valid JSON: %s" % e)
    dec = doc.get("decisions", doc)
    if not isinstance(dec, dict) or not dec:
        die("no 'decisions' object found in %s" % args.decisions)

    inc = exc = 0
    for rid, d in dec.items():
        if not isinstance(d, dict) or d.get("decision") not in ("include", "exclude"):
            die("invalid decision for %r (need decision include|exclude)" % rid)
        if not d.get("reason"):
            die("missing reason for %r" % rid)
        c = d.get("confidence")
        if not isinstance(c, (int, float)) or not (0 <= c <= 1):
            die("confidence for %r must be 0-1" % rid)
        inc += d["decision"] == "include"
        exc += d["decision"] == "exclude"

    obj = json.dumps(dec, ensure_ascii=False, separators=(",", ":"))
    html = open(args.capsule, encoding="utf-8").read()
    if START not in html or END not in html:
        die("capsule missing %s ... %s markers (add: const SCREEN_LIVE=%s{}%s;)" % (START, END, START, END))
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), START + obj + END, html, flags=re.S)

    meta = doc.get("_meta", {})
    print("Decisions: %d records (%d include, %d exclude) — screened_by: %s" % (
        len(dec), inc, exc, meta.get("screened_by", "—")))
    if args.dry_run:
        print("[dry-run] would inject SCREEN_LIVE into %s" % args.capsule)
        return
    with open(args.capsule, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("Injected SCREEN_LIVE into %s" % args.capsule)


if __name__ == "__main__":
    main()
