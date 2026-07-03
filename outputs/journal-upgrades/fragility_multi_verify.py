#!/usr/bin/env python
"""
Reusable exact Fragility Index (FI) calculator for 2x2 trial outcomes, used by
several Synthesis fragility papers (View/10 revascularisation, /13, /27 PLATO ...).

FI = minimum number of patients in ONE arm whose status changes (non-event ->
event) to make a two-sided Fisher exact test non-significant (p >= 0.05), per
Walsh 2014. Events are added to the arm with FEWER events (narrows the gap).
Fragility Quotient FQ = FI / N_total (Bakal 2015).

Each trial is (label, ev1, n1, ev2, n2). Counts must be crude cumulative event
counts from the primary binary outcome; for time-to-event outcomes this binary
approximation ignores censoring and is a LOWER bound on the true (log-rank) FI —
flagged per trial. Provide only counts verified against the primary publication.

Deterministic; requires scipy. No external data.
"""
import platform
if hasattr(platform, "_wmi_query"):
    platform._wmi_query = lambda *a, **k: (_ for _ in ()).throw(OSError("disabled"))
from scipy.stats import fisher_exact

def frag(ev1, n1, ev2, n2):
    """Return (baseline_p, FI, FQ, p_at_FI). Adds events to the lower-event arm."""
    ne1, ne2 = n1 - ev1, n2 - ev2
    p0 = fisher_exact([[ev1, ne1], [ev2, ne2]], alternative="two-sided")[1]
    # choose arm with fewer events to receive added events
    if ev1 <= ev2:
        a, b, c, d = ev1, ne1, ev2, ne2
        def step(k): return fisher_exact([[a+k, b-k], [c, d]], "two-sided")[1]
        cap = b
    else:
        a, b, c, d = ev2, ne2, ev1, ne1
        def step(k): return fisher_exact([[a+k, b-k], [c, d]], "two-sided")[1]
        cap = b
    if p0 >= 0.05:
        return p0, None, None, p0  # already non-significant
    fi = 0; p = p0
    while p < 0.05 and fi < cap:
        fi += 1
        p = step(fi)
    return p0, fi, fi / (n1 + n2), p

# --- trials with counts VERIFIED against the primary publication ---
# FAME-3 (Fearon et al., NEJM 2022;386:128-137): 1-yr primary composite
#   FFR-PCI 80/757 (10.6%) vs CABG 51/743 (6.9%). NCT02100722.
TRIALS = [
    ("FAME-3 (1-yr MACE, PCI vs CABG)", 80, 757, 51, 743, "verified vs Fearon 2022"),
]

print("=" * 74)
print("Exact Fragility Index (two-sided Fisher) — revascularisation trials")
print("=" * 74)
print(f"{'trial':<40}{'p0':>10}{'FI':>6}{'FQ%':>8}{'p@FI':>9}")
for label, e1, n1, e2, n2, note in TRIALS:
    p0, fi, fq, pfi = frag(e1, n1, e2, n2)
    fqs = f"{100*fq:.2f}" if fq is not None else "-"
    fis = str(fi) if fi is not None else "NS"
    print(f"{label:<40}{p0:>10.4f}{fis:>6}{fqs:>8}{pfi:>9.4f}   [{note}]")
print("=" * 74)
print("Note: FAME-3 primary composite (death/MI/stroke/repeat-revasc at 1 yr) is a")
print("binary count outcome as reported; FI is exact. Time-to-event trials (SYNTAX,")
print("FREEDOM, EXCEL, ISCHEMIA) require IPD for an exact log-rank FI and are not")
print("computed here to avoid asserting counts not verified against the source.")
