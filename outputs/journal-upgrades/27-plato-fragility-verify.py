#!/usr/bin/env python
"""
Deterministic Fragility Index (FI) computation for the PLATO primary composite
endpoint (CV death / MI / stroke at 12 months), for the v2 advanced version of
Synthesis View/27 ("The PLATO Trial — Was It Too Good to Be True?").

Published PLATO figures (Wallentin et al., NEJM 2009;361:1045-1057, PMID 19717846):
  Ticagrelor : 864 events / 9,333 randomised  (9.26%)
  Clopidogrel: 1,014 events / 9,291 randomised (10.91%)
  Reported HR 0.84 (95% CI 0.77-0.92), p < 0.001.

Fragility Index (Walsh 2014 method, PMID 24508144): the minimum number of
patients in ONE arm whose status must change (non-event -> event) to render the
2x2 result non-significant by a two-sided Fisher exact test (p >= 0.05). Per
standard practice and to reduce the event gap, events are ADDED to the arm with
FEWER events (ticagrelor), holding that arm's total fixed. Only ONE arm is
modified (fragility-index rule).

Fully deterministic. No external data. Requires scipy.
"""
import platform
# Python 3.13 WMI deadlock guard: neutralise platform._wmi_query before scipy import
if hasattr(platform, "_wmi_query"):
    platform._wmi_query = lambda *a, **k: (_ for _ in ()).throw(OSError("disabled"))

from scipy.stats import fisher_exact

# --- published PLATO 2x2 ---
tica_ev, tica_n = 864, 9333
clop_ev, clop_n = 1014, 9291
tica_ne = tica_n - tica_ev
clop_ne = clop_n - clop_ev

def p_two_sided(a, b, c, d):
    # table [[event_tica, nonevent_tica],[event_clop, nonevent_clop]]
    return fisher_exact([[a, b], [c, d]], alternative="two-sided")[1]

p0 = p_two_sided(tica_ev, tica_ne, clop_ev, clop_ne)
odds = (tica_ev/tica_ne)/(clop_ev/clop_ne)

# --- fragility: add events to ticagrelor arm (event++, nonevent--) ---
fi = 0
a, b = tica_ev, tica_ne
p = p0
while p < 0.05 and b > 0:
    a += 1
    b -= 1
    fi += 1
    p = p_two_sided(a, b, clop_ev, clop_ne)

fq = 100.0 * fi / (tica_n + clop_n)

# --- also report the sensitivity direction: remove events from clopidogrel ---
fi2 = 0
c, d = clop_ev, clop_ne
p2 = p0
while p2 < 0.05 and c > 0:
    c -= 1
    d += 1
    fi2 += 1
    p2 = p_two_sided(tica_ev, tica_ne, c, d)

# --- NNT (12-month event proportions) ---
r_c = clop_ev / clop_n
r_t = tica_ev / tica_n
arr = r_c - r_t
nnt = 1.0 / arr

print("=" * 62)
print("PAPER 27  PLATO Fragility Index — deterministic verification")
print("=" * 62)
print(f"Ticagrelor : {tica_ev} / {tica_n}  ({100*r_t:.2f}%)")
print(f"Clopidogrel: {clop_ev} / {clop_n}  ({100*r_c:.2f}%)")
print(f"Sample odds ratio (event): {odds:.3f}")
print(f"Baseline two-sided Fisher exact p = {p0:.3e}")
print("-" * 62)
print(f"Fragility Index (add events to ticagrelor arm) : {fi}")
print(f"  -> Fisher p at FI reaches {p:.4f} (>= 0.05)")
print(f"Fragility Quotient = FI / N_total = {fi}/{tica_n+clop_n} = {fq:.3f}%")
print(f"(cross-check: remove events from clopidogrel arm : {fi2})")
print("-" * 62)
print(f"Absolute risk reduction = {100*arr:.2f}% ; NNT = {nnt:.1f} (~{round(nnt)})")
print("=" * 62)
print("Note: total losses to follow-up in PLATO primary composite were far")
print(f"fewer than nothing relevant here; FI={fi} vs a modification quotient of")
print(f"{fq:.2f}% indicates a statistically robust primary result (FI >> 10).")
