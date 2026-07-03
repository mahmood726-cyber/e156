#!/usr/bin/env python
"""
Deterministic verification script for the world-class (v2) advanced version of
"CT.gov Structural Missingness" (Synthesis View/165).

Computes, from the raw AACT flat-file snapshot (no sampling, full registry):
  1. Total study denominator.
  2. Four field-level missingness rates:
       - publication links (study_references presence)
       - IPD sharing statement (studies.plan_to_share_ipd)
       - detailed description (present row AND non-empty content)
       - study locations (facilities presence)
  3. Full sponsor-class (source_class) breakdown for all seven AACT classes,
     with a composite hiddenness score (mean of the four binary indicators).

Robustness: AACT pipe-delimited flat files embed newlines inside long text
fields (official_title, detailed description, plan_to_share_ipd_description).
Naive line splitting misaligns high-index columns, so we reassemble each
logical record by its start signature before splitting on '|'.

  - studies.txt record start:  ^NCT\\d{8}\\|
  - child-table record start:  ^\\d+\\|NCT\\d{8}\\|

Output is fully deterministic (no randomness, no sampling). Reads the snapshot
read-only. AACT root is taken from $AACT_DIR or discovered among candidate
roots; the script fails closed if no snapshot is found.
"""
import os
import re
import sys

SNAP = "2026-04-12"
CANDIDATES = [
    os.environ.get("AACT_DIR", ""),
    rf"F:\AACT-storage\AACT\{SNAP}",
    rf"C:\AACT-storage\AACT\{SNAP}",
    rf"D:\AACT-storage\AACT\{SNAP}",
    f"/f/AACT-storage/AACT/{SNAP}",
]

def find_aact():
    for c in CANDIDATES:
        if c and os.path.isfile(os.path.join(c, "studies.txt")):
            return c
    sys.exit("FAIL-CLOSED: no AACT snapshot found. Set $AACT_DIR to the folder "
             "containing studies.txt (AACT " + SNAP + " flat files).")

AACT = find_aact()

STUDY_START = re.compile(rb"^NCT\d{8}\|")
CHILD_START = re.compile(rb"^\d+\|NCT\d{8}\|")
NCT_FIELD2 = re.compile(rb"^\d+\|(NCT\d{8})\|")

def iter_study_records(path):
    """Yield fully-reassembled studies.txt records (bytes), skipping header."""
    buf = None
    with open(path, "rb") as fh:
        fh.readline()  # header
        for line in fh:
            if STUDY_START.match(line):
                if buf is not None:
                    yield buf
                buf = line
            else:
                if buf is not None:
                    buf += line
        if buf is not None:
            yield buf

def child_nct_set(path, require_content_field=None):
    """Distinct nct_ids in a child table. If require_content_field (0-based
    index) is given, only count rows whose that field has non-empty content."""
    ids = set()
    buf = None
    def flush(b):
        m = NCT_FIELD2.match(b)
        if not m:
            return
        nct = m.group(1).decode()
        if require_content_field is None:
            ids.add(nct)
        else:
            parts = b.rstrip(b"\n").split(b"|")
            if len(parts) > require_content_field:
                val = parts[require_content_field].strip()
                if val and val != rb"\N".strip():
                    ids.add(nct)
    with open(path, "rb") as fh:
        fh.readline()
        for line in fh:
            if CHILD_START.match(line):
                if buf is not None:
                    flush(buf)
                buf = line
            else:
                if buf is not None:
                    buf += line
        if buf is not None:
            flush(buf)
    return ids

def is_empty(v):
    return (v is None) or (v.strip() in (b"", rb"\N".strip(), b"\\N"))

# ---- studies: total, source_class (idx 64), plan_to_share_ipd (idx 60) ----
N_FIELDS = 71
IDX_SOURCE_CLASS = 64
IDX_IPD = 60

studies = {}          # nct -> (source_class, ipd_missing_bool)
bad_fieldcount = 0
total = 0
for rec in iter_study_records(os.path.join(AACT, "studies.txt")):
    total += 1
    parts = rec.rstrip(b"\n").split(b"|")
    if len(parts) != N_FIELDS:
        bad_fieldcount += 1
        # still salvage nct + best-effort; skip class/ipd if misaligned
        nct = parts[0].decode()
        studies[nct] = (b"__MISALIGNED__", None)
        continue
    nct = parts[0].decode()
    sc = parts[IDX_SOURCE_CLASS].strip() or b"__BLANK__"
    ipd_missing = is_empty(parts[IDX_IPD])
    studies[nct] = (sc, ipd_missing)

all_ncts = set(studies)

# ---- child-table presence sets ----
ref_ncts = child_nct_set(os.path.join(AACT, "study_references.txt"))
fac_ncts = child_nct_set(os.path.join(AACT, "facilities.txt"))
# detailed_descriptions: field3 = description (0-based idx 2); require content
dd_ncts = child_nct_set(os.path.join(AACT, "detailed_descriptions.txt"),
                        require_content_field=2)

def pct(n, d):
    return 100.0 * n / d if d else float("nan")

# ---- overall rates ----
miss_pub = sum(1 for n in all_ncts if n not in ref_ncts)
miss_loc = sum(1 for n in all_ncts if n not in fac_ncts)
miss_dd = sum(1 for n in all_ncts if n not in dd_ncts)
miss_ipd = sum(1 for n, (_, im) in studies.items() if im)

print("=" * 68)
print("PAPER 165  CT.gov Structural Missingness — deterministic verification")
print("AACT snapshot:", AACT)
print("=" * 68)
print(f"Total studies (denominator)          : {total:,}")
print(f"studies rows with != {N_FIELDS} fields (misaligned): {bad_fieldcount:,}")
print("-" * 68)
print(f"Publication links MISSING : {miss_pub:>7,}  ({pct(miss_pub,total):5.2f}%)")
print(f"IPD statement    MISSING : {miss_ipd:>7,}  ({pct(miss_ipd,total):5.2f}%)")
print(f"Detailed descr.  MISSING : {miss_dd:>7,}  ({pct(miss_dd,total):5.2f}%)")
print(f"Study locations  MISSING : {miss_loc:>7,}  ({pct(miss_loc,total):5.2f}%)")
print("-" * 68)

# ---- sponsor-class breakdown ----
from collections import defaultdict
cls_tot = defaultdict(int)
cls_pub = defaultdict(int)
cls_ipd = defaultdict(int)
cls_dd = defaultdict(int)
cls_loc = defaultdict(int)
for nct, (sc, im) in studies.items():
    key = sc.decode(errors="replace")
    cls_tot[key] += 1
    if nct not in ref_ncts: cls_pub[key] += 1
    if im: cls_ipd[key] += 1
    if nct not in dd_ncts: cls_dd[key] += 1
    if nct not in fac_ncts: cls_loc[key] += 1

print(f"{'source_class':<14}{'n':>9}{'pub%':>8}{'ipd%':>8}{'dd%':>8}{'loc%':>8}{'composite':>11}")
for key in sorted(cls_tot, key=lambda k: -cls_tot[k]):
    n = cls_tot[key]
    p = pct(cls_pub[key], n); i = pct(cls_ipd[key], n)
    d = pct(cls_dd[key], n); l = pct(cls_loc[key], n)
    comp = (p + i + d + l) / 400.0
    print(f"{key:<14}{n:>9,}{p:>8.1f}{i:>8.1f}{d:>8.1f}{l:>8.1f}{comp:>11.3f}")
print("=" * 68)
