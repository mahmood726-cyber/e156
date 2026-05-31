#!/usr/bin/env python
"""Run a whole e156 capsule pipeline end-to-end from one config file.

Chains the single-purpose CLIs in order:
  1. register_protocol.py  — commit the protocol (timestamp) + inject the permalink
  2. fetch_ctgov.py        — live ClinicalTrials.gov registry summaries
  3. fetch_pubmed.py       — live PubMed abstracts
  4. fetch_openalex.py     — live OpenAlex DOIs / citations / OA status
  5. inject_screening.py   — agent-produced screening decisions (if present)
  6. inject_extraction.py  — agent-produced data extraction (if present)

The AI steps (screening, extraction) are done by the HOST agentic CLI itself
(Claude Code / Gemini) — the orchestrating agent is the model, no API key. So
the flow is: run steps 1-4 to acquire data; the agent reads the fetched records
and writes the screening/extraction JSONs; re-run (or run 5-6) to inject them.
If those files are absent, the runner does steps 1-4 and tells you what the agent
should produce next.

Config (JSON), e.g. pipelines/sglt2-hf.json:
  {
    "capsule":   "flagship/sglt2-hf-capsule.html",
    "protocol":  "protocols/sglt2-hf-protocol.md",
    "author":    {"name": "...", "email": "..."},
    "ncts":      ["NCT03036124", ...],                 // CT.gov fetch
    "pmid_map":  {"NCT03036124": "31535829", ...},     // PubMed + OpenAlex
    "mailto":    "you@example.com",                     // optional (OpenAlex)
    "screening": "data/screening-decisions.json",      // optional (agent-made)
    "extraction":"data/extraction-live.json"           // optional (agent-made)
  }

Usage:
  python scripts/run_pipeline.py --config pipelines/sglt2-hf.json
  python scripts/run_pipeline.py --config ... --only ctgov,pubmed
  python scripts/run_pipeline.py --config ... --skip protocol --dry-run
"""
import argparse
import io
import json
import os
import subprocess
import sys

if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STEPS = ["protocol", "ctgov", "pubmed", "openalex", "screening", "extraction"]


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def run(script, argv, dry):
    cmd = [sys.executable, os.path.join(HERE, script)] + argv + (["--dry-run"] if dry else [])
    print("\n$ %s %s" % (script, " ".join(argv) + (" --dry-run" if dry else "")))
    sys.stdout.flush()
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        die("step failed: %s (exit %d)" % (script, r.returncode))


def main():
    ap = argparse.ArgumentParser(description="Run an e156 capsule pipeline from a config file.")
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", default=None, help="comma list of steps to run (%s)" % "/".join(STEPS))
    ap.add_argument("--skip", default=None, help="comma list of steps to skip")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.config):
        die("config not found: %s" % args.config)
    cfg = json.load(open(args.config, encoding="utf-8"))
    for req in ("capsule",):
        if req not in cfg:
            die("config missing required key: %s" % req)
    capsule = cfg["capsule"]

    want = set(s.strip() for s in args.only.split(",")) if args.only else set(STEPS)
    skip = set(s.strip() for s in args.skip.split(",")) if args.skip else set()
    bad = (want | skip) - set(STEPS)
    if bad:
        die("unknown step(s): %s" % ", ".join(sorted(bad)))
    plan = [s for s in STEPS if s in want and s not in skip]
    print("Pipeline: %s  (config: %s)" % (" -> ".join(plan), os.path.basename(args.config)))

    pmid_map = cfg.get("pmid_map", {})
    map_args = []
    for nct, pmid in pmid_map.items():
        map_args += ["--map", "%s=%s" % (nct, pmid)]

    for step in plan:
        if step == "protocol":
            if not cfg.get("protocol"):
                print("\n(skip protocol: no 'protocol' in config)"); continue
            a = ["--protocol", cfg["protocol"], "--capsule", capsule]
            au = cfg.get("author", {})
            if au.get("name") and au.get("email"):
                a += ["--author-name", au["name"], "--author-email", au["email"]]
            run("register_protocol.py", a, args.dry_run)
        elif step == "ctgov":
            ncts = cfg.get("ncts", [])
            if not ncts:
                print("\n(skip ctgov: no 'ncts' in config)"); continue
            a = ["--capsule", capsule]
            for n in ncts:
                a += ["--nct", n]
            run("fetch_ctgov.py", a, args.dry_run)
        elif step == "pubmed":
            if not pmid_map:
                print("\n(skip pubmed: no 'pmid_map' in config)"); continue
            run("fetch_pubmed.py", ["--capsule", capsule] + map_args, args.dry_run)
        elif step == "openalex":
            if not pmid_map:
                print("\n(skip openalex: no 'pmid_map' in config)"); continue
            a = ["--capsule", capsule] + map_args
            if cfg.get("mailto"):
                a += ["--mailto", cfg["mailto"]]
            run("fetch_openalex.py", a, args.dry_run)
        elif step == "screening":
            f = cfg.get("screening")
            if not f or not os.path.isfile(os.path.join(ROOT, f)):
                print("\n(screening: no agent decisions yet — have the host agent read the fetched\n"
                      " records + protocol criteria and write %s, then re-run --only screening)"
                      % (f or "data/<review>-screening.json"))
                continue
            run("inject_screening.py", ["--decisions", f, "--capsule", capsule], args.dry_run)
        elif step == "extraction":
            f = cfg.get("extraction")
            if not f or not os.path.isfile(os.path.join(ROOT, f)):
                print("\n(extraction: no agent extraction yet — have the host agent extract from the\n"
                      " fetched abstracts and write %s, then re-run --only extraction)"
                      % (f or "data/<review>-extraction.json"))
                continue
            run("inject_extraction.py", ["--extraction", f, "--capsule", capsule], args.dry_run)

    print("\nPipeline complete%s." % (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
