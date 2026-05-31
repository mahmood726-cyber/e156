#!/usr/bin/env python
"""Fetch REAL OpenAlex metadata (DOI, citation count, open-access status) for the
included trials and inject it into a capsule.

Third 'demo -> live data' source (companion to fetch_ctgov.py / fetch_pubmed.py).
OpenAlex is queried by PMID (no auth). It supplies the genuine DOI — which the
capsule otherwise could not assert without fabricating it — so references link
directly to the paper, plus the citation count and open-access status.

Writes provenance (data/openalex-records.json) and injects OPENALEX_LIVE between
  /*OPENALEX_START*/ ... /*OPENALEX_END*/
Fail-closed on any network/HTTP/parse error; never fabricates a DOI.

Usage:
  python scripts/fetch_openalex.py --capsule flagship/sglt2-hf-capsule.html \
      --map NCT03036124=31535829 ... [--mailto you@example.com] [--dry-run]
"""
import argparse
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

API = "https://api.openalex.org/works/pmid:"
START, END = "/*OPENALEX_START*/", "/*OPENALEX_END*/"


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def fetch(pmid, mailto):
    url = API + str(pmid) + ("?mailto=" + urllib.parse.quote(mailto) if mailto else "")
    req = urllib.request.Request(url, headers={"User-Agent": "e156-capsule/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
    except Exception as e:
        die("OpenAlex fetch failed for PMID %s: %s" % (pmid, e))
    doi = (d.get("doi") or "").replace("https://doi.org/", "")
    oa = d.get("open_access", {}) or {}
    return {
        "doi": doi,
        "citedBy": d.get("cited_by_count"),
        "oa": bool(oa.get("is_oa")),
        "oaStatus": oa.get("oa_status") or "",
        "year": d.get("publication_year"),
        "openalexId": (d.get("id") or "").replace("https://openalex.org/", ""),
        "title": (d.get("title") or "").strip(),
        "source": "OpenAlex",
    }


def main():
    ap = argparse.ArgumentParser(description="Fetch real OpenAlex DOIs/citations and inject OPENALEX_LIVE.")
    ap.add_argument("--capsule", required=True)
    ap.add_argument("--map", action="append", required=True, metavar="NCT=PMID")
    ap.add_argument("--mailto", default=None, help="email for the OpenAlex polite pool (optional)")
    ap.add_argument("--data-out", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.capsule):
        die("capsule not found: %s" % args.capsule)
    pairs = {}
    for m in args.map:
        if "=" not in m:
            die("--map must be NCT=PMID, got %r" % m)
        nct, pmid = m.split("=", 1)
        if not re.fullmatch(r"NCT\d{8}", nct) or not re.fullmatch(r"\d+", pmid):
            die("bad --map entry %r" % m)
        pairs[nct] = pmid

    records = {}
    for i, (nct, pmid) in enumerate(pairs.items()):
        if i:
            time.sleep(0.2)
        rec = fetch(pmid, args.mailto)
        if not rec["doi"]:
            die("no DOI returned for %s (PMID %s)" % (nct, pmid))
        records[nct] = rec
        print("  %s  DOI %-26s cited_by=%-6s OA=%s  %s" % (
            nct, rec["doi"], rec["citedBy"], rec["oaStatus"] or "no", rec["title"][:42]))

    obj = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    html = open(args.capsule, encoding="utf-8").read()
    if START not in html or END not in html:
        die("capsule missing %s ... %s markers (add: const OPENALEX_LIVE=%s{}%s;)" % (START, END, START, END))
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), START + obj + END, html, flags=re.S)

    data_out = args.data_out or os.path.join(os.path.dirname(os.path.abspath(args.capsule)), "..", "data", "openalex-records.json")
    if args.dry_run:
        print("[dry-run] would inject %d OpenAlex records into %s" % (len(records), args.capsule))
        return
    os.makedirs(os.path.dirname(data_out), exist_ok=True)
    with open(data_out, "w", encoding="utf-8", newline="") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    with open(args.capsule, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("Injected %d live OpenAlex records into %s" % (len(records), args.capsule))
    print("Provenance written to %s" % os.path.normpath(data_out))


if __name__ == "__main__":
    main()
