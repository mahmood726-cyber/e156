#!/usr/bin/env python
"""Fetch REAL PubMed abstracts for the included trials' primary papers and inject
them into a capsule.

Second 'demo -> live data' step (companion to fetch_ctgov.py). Given a mapping of
NCT id -> primary-publication PMID, it fetches the genuine title, abstract,
journal, year and first author from NCBI E-utilities (efetch, no auth), writes a
committed provenance file (data/pubmed-records.json), and injects a PUBMED_LIVE
object into the capsule between
  /*PUBMED_START*/ ... /*PUBMED_END*/
so the capsule prefers the live abstract over its illustrative placeholder.

Why a PMID map rather than auto-pick: searching <NCT>[si] returns dozens of
linked papers (sub-analyses, protocols). To avoid attaching the wrong abstract,
the caller supplies the primary PMID; the CLI fetches it and PRINTS the title so
the mapping is verifiable. Fail-closed on any network/HTTP/parse error.

Usage:
  python scripts/fetch_pubmed.py --capsule flagship/sglt2-hf-capsule.html \
      --map NCT03036124=31535829 --map NCT03057977=32865377 ... [--dry-run]
"""
import argparse
import io
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
START, END = "/*PUBMED_START*/", "/*PUBMED_END*/"


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def fetch(pmid):
    url = "%s?db=pubmed&id=%s&rettype=abstract&retmode=xml" % (EFETCH, pmid)
    req = urllib.request.Request(url, headers={"User-Agent": "e156-capsule/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            root = ET.fromstring(r.read())
    except Exception as e:
        die("efetch failed for PMID %s: %s" % (pmid, e))
    art = root.find(".//Article")
    if art is None:
        die("no article for PMID %s (wrong id?)" % pmid)
    title = (art.findtext("ArticleTitle") or "").strip().rstrip(".")
    # abstract may be split into labelled sections
    parts = []
    for el in art.findall(".//Abstract/AbstractText"):
        lbl = el.get("Label")
        txt = "".join(el.itertext()).strip()
        parts.append(("%s: %s" % (lbl.title(), txt)) if lbl else txt)
    abstract = " ".join(p for p in parts if p)
    journal = art.findtext(".//Journal/ISOAbbreviation") or art.findtext(".//Journal/Title") or ""
    year = art.findtext(".//JournalIssue/PubDate/Year") or art.findtext(".//PubDate/Year") or ""
    auth = art.find(".//AuthorList/Author")
    author = ""
    if auth is not None:
        ln = auth.findtext("LastName") or ""
        ini = auth.findtext("Initials") or ""
        author = ("%s %s" % (ln, ini)).strip() + (" et al." if ln else "")
    return {"pmid": str(pmid), "title": title, "abstract": abstract, "journal": journal,
            "year": year, "author": author, "source": "PubMed (NCBI E-utilities)"}


def main():
    ap = argparse.ArgumentParser(description="Fetch real PubMed abstracts and inject PUBMED_LIVE into a capsule.")
    ap.add_argument("--capsule", required=True)
    ap.add_argument("--map", action="append", required=True, metavar="NCT=PMID",
                    help="map an NCT id to its primary-paper PMID (repeatable)")
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
            die("bad --map entry %r (need NCT########=digits)" % m)
        pairs[nct] = pmid

    records = {}
    for i, (nct, pmid) in enumerate(pairs.items()):
        if i:
            time.sleep(0.4)  # stay under the 3 req/s E-utilities limit
        rec = fetch(pmid)
        if not rec["abstract"]:
            die("PMID %s (%s) returned no abstract" % (pmid, nct))
        records[nct] = rec
        print("  %s  PMID %-9s %s, %s — %s" % (nct, pmid, rec["journal"], rec["year"], rec["title"][:60]))

    obj = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    html = open(args.capsule, encoding="utf-8").read()
    if START not in html or END not in html:
        die("capsule missing %s ... %s markers (add: const PUBMED_LIVE=%s{}%s;)" % (START, END, START, END))
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), START + obj + END, html, flags=re.S)

    data_out = args.data_out or os.path.join(os.path.dirname(os.path.abspath(args.capsule)), "..", "data", "pubmed-records.json")
    if args.dry_run:
        print("[dry-run] would inject %d live abstracts into %s" % (len(records), args.capsule))
        return
    os.makedirs(os.path.dirname(data_out), exist_ok=True)
    with open(data_out, "w", encoding="utf-8", newline="") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    with open(args.capsule, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("Injected %d live PubMed abstracts into %s" % (len(records), args.capsule))
    print("Provenance written to %s" % os.path.normpath(data_out))


if __name__ == "__main__":
    main()
