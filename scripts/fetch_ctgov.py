#!/usr/bin/env python
"""Fetch REAL ClinicalTrials.gov records and inject them into a capsule.

This is the first 'demo -> live data' step of the pipeline: it pulls genuine
registry data from the public ClinicalTrials.gov API v2 (no auth) for a given
set of NCT identifiers, builds the structured summary each capsule shows for a
registry record, writes a committed provenance file (data/ctgov-records.json),
and injects a CTGOV_LIVE object into the capsule between the markers
  /*CTGOV_START*/ ... /*CTGOV_END*/
so the capsule prefers the live data over its illustrative placeholders.

Fail-closed: a network/HTTP/parse error for any NCT stops the run; it never
writes partial or fabricated data, and never invents an NCT.

Usage:
  python scripts/fetch_ctgov.py --capsule flagship/sglt2-hf-capsule.html \
      --nct NCT03036124 --nct NCT03057977 ... [--dry-run]
"""
import argparse
import io
import json
import os
import re
import sys
import urllib.request

if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

API = "https://clinicaltrials.gov/api/v2/studies/"
FIELDS = ",".join([
    "protocolSection.identificationModule.briefTitle",
    "protocolSection.identificationModule.acronym",
    "protocolSection.statusModule.overallStatus",
    "protocolSection.conditionsModule.conditions",
    "protocolSection.designModule",
    "protocolSection.armsInterventionsModule.interventions",
    "protocolSection.armsInterventionsModule.armGroups",
    "protocolSection.outcomesModule.primaryOutcomes",
])
START, END = "/*CTGOV_START*/", "/*CTGOV_END*/"


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def title_case(s):
    return s.replace("_", " ").title() if s else ""


def fetch(nct):
    url = "%s%s?fields=%s" % (API, nct, FIELDS)
    req = urllib.request.Request(url, headers={"User-Agent": "e156-capsule/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
    except Exception as e:  # network, HTTP, JSON
        die("fetch failed for %s: %s" % (nct, e))
    ps = data.get("protocolSection", {})
    ident = ps.get("identificationModule", {})
    design = ps.get("designModule", {})
    di = design.get("designInfo", {})
    interventions = ps.get("armsInterventionsModule", {}).get("interventions", []) or []
    arms = ps.get("armsInterventionsModule", {}).get("armGroups", []) or []
    primaries = ps.get("outcomesModule", {}).get("primaryOutcomes", []) or []
    conds = ps.get("conditionsModule", {}).get("conditions", []) or []

    drugs = [i.get("name", "") for i in interventions if i.get("type") in ("DRUG", "BIOLOGICAL")]
    placebo = any("placebo" in (i.get("name", "") or "").lower() for i in interventions) \
        or any("PLACEBO" in (a.get("type", "") or "") for a in arms)
    phases = "/".join(title_case(p) for p in design.get("phases", []) or [])
    masking = di.get("maskingInfo", {}).get("masking", "")
    design_str = " · ".join(filter(None, [
        title_case(design.get("studyType", "")),
        phases,
        title_case(di.get("allocation", "")),
        (title_case(masking) + "-blind") if masking and masking != "NONE" else "",
    ]))
    enr = design.get("enrollmentInfo", {})
    return {
        "title": ident.get("briefTitle", ""),
        "acronym": ident.get("acronym", ""),
        "condition": conds[0] if conds else "—",
        "intervention": ", ".join([d for d in drugs if "placebo" not in d.lower()]) or "—",
        "comparator": "Placebo" if placebo else "—",
        "design": design_str or "—",
        "primary": (primaries[0].get("measure", "") if primaries else "—"),
        "enrollment": enr.get("count"),
        "status": title_case(ps.get("statusModule", {}).get("overallStatus", "")),
        "live": True,
        "source": "ClinicalTrials.gov API v2",
    }


def main():
    ap = argparse.ArgumentParser(description="Fetch real CT.gov records and inject CTGOV_LIVE into a capsule.")
    ap.add_argument("--capsule", required=True)
    ap.add_argument("--nct", action="append", required=True, help="NCT id (repeatable)")
    ap.add_argument("--data-out", default=None, help="provenance JSON path (default: data/ctgov-records.json next to the repo)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.capsule):
        die("capsule not found: %s" % args.capsule)
    bad = [n for n in args.nct if not re.fullmatch(r"NCT\d{8}", n)]
    if bad:
        die("not valid NCT ids: %s" % ", ".join(bad))

    records = {}
    for nct in args.nct:
        rec = fetch(nct)
        if not rec["title"]:
            die("no record returned for %s" % nct)
        records[nct] = rec
        print("  fetched %-12s %-10s enrol=%s  %s" % (nct, rec["acronym"] or "—", rec["enrollment"], rec["title"][:48]))

    obj = json.dumps(records, ensure_ascii=False, separators=(",", ":"))

    html = open(args.capsule, encoding="utf-8").read()
    if START not in html or END not in html:
        die("capsule missing %s ... %s markers (add: const CTGOV_LIVE=%s{}%s;)" % (START, END, START, END))
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), START + obj + END, html, flags=re.S)

    data_out = args.data_out or os.path.join(os.path.dirname(os.path.abspath(args.capsule)), "..", "data", "ctgov-records.json")
    if args.dry_run:
        print("[dry-run] would inject %d live records into %s and write %s" % (len(records), args.capsule, os.path.normpath(data_out)))
        return
    os.makedirs(os.path.dirname(data_out), exist_ok=True)
    with open(data_out, "w", encoding="utf-8", newline="") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    with open(args.capsule, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("Injected %d live ClinicalTrials.gov records into %s" % (len(records), args.capsule))
    print("Provenance written to %s" % os.path.normpath(data_out))


if __name__ == "__main__":
    main()
