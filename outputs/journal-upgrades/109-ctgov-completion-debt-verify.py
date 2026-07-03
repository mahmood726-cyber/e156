#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of
"CT.gov Completion-Delay Debt" (Synthesis View/109).

Fills the v1 placeholder delay-bucket table with real values computed from the
raw AACT flat-file snapshot. For every submission-to-completion delay bucket it
reports: n, two-year no-results rate, and independently-computed ghost-protocol
rate (no results AND no study_references AND no links).

Eligibility (matches v1 intent):
  study_type = Interventional
  overall_status in {COMPLETED, TERMINATED, SUSPENDED, WITHDRAWN}
  primary_completion_date <= (snapshot_date - 2 years)      [results now overdue]
  study_first_submitted_date and primary_completion_date both parseable,
  and completion year >= submission year (non-negative delay).

Delay bucket = year(primary_completion_date) - year(study_first_submitted_date).
Buckets: same-year(0), 1, 2, 3-5, 6-10, >10.

Deterministic, read-only. AACT root from $AACT_DIR or discovered; fail-closed.
Note: v1 used the 2026-03-29 snapshot (N=249,507); this runs on 2026-04-12, so
counts differ slightly by registry growth — reported transparently.
"""
import os, re, sys
from collections import defaultdict

SNAP = "2026-04-12"
SNAP_YEAR, SNAP_CUTOFF = 2026, "2024-04-12"   # pcd <= cutoff (2y before snapshot)
CANDS = [os.environ.get("AACT_DIR",""),
         rf"F:\AACT-storage\AACT\{SNAP}", rf"C:\AACT-storage\AACT\{SNAP}",
         rf"D:\AACT-storage\AACT\{SNAP}", f"/f/AACT-storage/AACT/{SNAP}"]
AACT = next((c for c in CANDS if c and os.path.isfile(os.path.join(c,"studies.txt"))), None)
if not AACT:
    sys.exit("FAIL-CLOSED: no AACT snapshot; set $AACT_DIR")

STUDY_START = re.compile(rb"^NCT\d{8}\|")
CHILD_START = re.compile(rb"^\d+\|NCT\d{8}\|")
NCT_F2 = re.compile(rb"^\d+\|(NCT\d{8})\|")

def study_records(path):
    buf=None
    with open(path,"rb") as fh:
        fh.readline()
        for ln in fh:
            if STUDY_START.match(ln):
                if buf is not None: yield buf
                buf=ln
            elif buf is not None: buf+=ln
        if buf is not None: yield buf

def child_map(path, val_idx=None):
    """Return set of nct (val_idx None) or dict nct->value (0-based val_idx)."""
    out = {} if val_idx is not None else set()
    buf=None
    def flush(b):
        m=NCT_F2.match(b)
        if not m: return
        nct=m.group(1).decode()
        if val_idx is None: out.add(nct)
        else:
            p=b.rstrip(b"\n").split(b"|")
            out[nct]= p[val_idx].strip().decode() if len(p)>val_idx else ""
    with open(path,"rb") as fh:
        fh.readline()
        for ln in fh:
            if CHILD_START.match(ln):
                if buf is not None: flush(buf)
                buf=ln
            elif buf is not None: buf+=ln
        if buf is not None: flush(buf)
    return out

# --- child tables ---
results_reported = child_map(os.path.join(AACT,"calculated_values.txt"), val_idx=8) # were_results_reported
ref_ncts = child_map(os.path.join(AACT,"study_references.txt"))
link_ncts = child_map(os.path.join(AACT,"links.txt"))
purpose = child_map(os.path.join(AACT,"designs.txt"), val_idx=5)  # primary_purpose

# --- studies ---
N=71
I_SUB, I_PCD, I_TYPE, I_STATUS = 2, 28, 30, 35
CLOSED = {"COMPLETED","TERMINATED","SUSPENDED","WITHDRAWN"}
def ybucket(d):
    if d<0: return None
    if d==0: return "same"
    if d==1: return "1"
    if d==2: return "2"
    if 3<=d<=5: return "3-5"
    if 6<=d<=10: return "6-10"
    return ">10"

order=["same","1","2","3-5","6-10",">10"]
tot=defaultdict(int); nores=defaultdict(int); ghost=defaultdict(int)
ttot=defaultdict(int); tnores=defaultdict(int); tghost=defaultdict(int)  # treatment purpose
elig=0; bad=0
for rec in study_records(os.path.join(AACT,"studies.txt")):
    p=rec.rstrip(b"\n").split(b"|")
    if len(p)!=N: bad+=1; continue
    stype=p[I_TYPE].strip().decode().upper()
    if stype!="INTERVENTIONAL": continue
    status=p[I_STATUS].strip().decode().upper()
    if status not in CLOSED: continue
    pcd=p[I_PCD].strip().decode(); sub=p[I_SUB].strip().decode()
    if len(pcd)<4 or len(sub)<4 or not pcd[:4].isdigit() or not sub[:4].isdigit(): continue
    if pcd > SNAP_CUTOFF: continue      # not yet 2y overdue
    d = int(pcd[:4]) - int(sub[:4])
    b = ybucket(d)
    if b is None: continue
    elig+=1
    nct=p[0].decode()
    no_res = results_reported.get(nct,"") != "t"
    is_ghost = no_res and (nct not in ref_ncts) and (nct not in link_ncts)
    tot[b]+=1
    if no_res: nores[b]+=1
    if is_ghost: ghost[b]+=1
    if purpose.get(nct,"").upper()=="TREATMENT":
        ttot[b]+=1
        if no_res: tnores[b]+=1
        if is_ghost: tghost[b]+=1

def pct(a,b): return 100.0*a/b if b else float("nan")
print("="*72)
print("PAPER 109  CT.gov Completion-Delay Debt — deterministic verification")
print("AACT snapshot:", AACT, "| pcd cutoff <=", SNAP_CUTOFF)
print("="*72)
print(f"Eligible closed interventional studies (>=2y overdue): {elig:,}")
print(f"studies rows skipped (field-count anomaly): {bad:,}")
print("-"*72)
print(f"{'bucket':<8}{'n':>9}{'no-results%':>13}{'ghost%':>10}")
for b in order:
    print(f"{b:<8}{tot[b]:>9,}{pct(nores[b],tot[b]):>13.1f}{pct(ghost[b],tot[b]):>10.1f}")
alln=sum(tot.values()); allnr=sum(nores.values()); allg=sum(ghost.values())
print("-"*72)
print(f"{'ALL':<8}{alln:>9,}{pct(allnr,alln):>13.1f}{pct(allg,alln):>10.1f}")
print("-"*72)
print("TREATMENT-purpose sub-group:")
print(f"{'bucket':<8}{'n':>9}{'no-results%':>13}{'ghost%':>10}")
for b in order:
    print(f"{b:<8}{ttot[b]:>9,}{pct(tnores[b],ttot[b]):>13.1f}{pct(tghost[b],ttot[b]):>10.1f}")
print("="*72)
