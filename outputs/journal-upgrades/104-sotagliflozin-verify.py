#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of the Synthesis paper
"Sotagliflozin (dual SGLT1/2 inhibitor) in heart failure and CKD" (View/104).

Verified published inputs (PubMed title+journal+DOI matched 2026-07-04):
  SOLOIST-WHF  Bhatt 2021 NEJM  worsening HF+T2D  n=1222 (terminated early)
      total-event composite (CV death + HHF + urgent HF visit), weighted HR
      HR 0.67 (0.52-0.85)   PMID 33200892  doi 10.1056/NEJMoa2030183
  SCORED       Bhatt 2021 NEJM  CKD+T2D (eGFR 25-60)  n=10584
      total-event composite (CV death + HHF + urgent HF visit), weighted HR
      HR 0.74 (0.63-0.88)   PMID 33200891  doi 10.1056/NEJMoa2030186
  Early-termination phenomenon: Montori 2005 JAMA 294(17):2203-9  PMID 16264162
      (v1 cited wrong PMID 16286622, a cataract-surgery paper)

Selective SGLT2i HF comparator (first-event HRs, verified vs NEJM abstracts):
  DAPA-HF 0.74(0.65-0.85) 31535829; EMPEROR-Reduced 0.75(0.65-0.86) 32865377;
  EMPEROR-Preserved 0.79(0.69-0.90) 34449189; DELIVER 0.82(0.73-0.92) 36027570.

Methods: pool on log-HR scale. Two-trial sotagliflozin FE pool (k=2 -> HKSJ
uninformative, report FE). Selective SGLT2i FE pool (k=4). Indirect (Bucher)
comparison of the two pooled log-HRs. Leave-SOLOIST-out sensitivity (SCORED alone)
as the principled handling of SOLOIST's early termination -- NO ad-hoc
sqrt(N/Ntarget) shrinkage (that heuristic has no theoretical basis and is dropped
from v2). Deterministic; requires numpy.
"""
import math
import numpy as np
from scipy.stats import norm

Z = 1.959963985

def yv(hr, lo, hi):
    y = math.log(hr)
    se = (math.log(hi) - math.log(lo)) / (2 * Z)
    return y, se * se

def fe_pool(items):
    ys = [y for y, _ in items]; vs = [v for _, v in items]
    w = [1.0 / v for v in vs]
    mu = sum(wi * yi for wi, yi in zip(w, ys)) / sum(w)
    var = 1.0 / sum(w)
    return mu, var

SOTA = {"SOLOIST-WHF": (0.67, 0.52, 0.85), "SCORED": (0.74, 0.63, 0.88)}
SEL  = {"DAPA-HF": (0.74, 0.65, 0.85), "EMPEROR-Reduced": (0.75, 0.65, 0.86),
        "EMPEROR-Preserved": (0.79, 0.69, 0.90), "DELIVER": (0.82, 0.73, 0.92)}

print("Sotagliflozin — deterministic verification (v2)")
print("\nPer-trial log-HR and SE:")
sota_items = []
for nm, (hr, lo, hi) in SOTA.items():
    y, v = yv(hr, lo, hi); sota_items.append((y, v))
    print(f"  {nm:<18} HR {hr:.2f} ({lo:.2f}-{hi:.2f})  logHR={y:+.4f} SE={math.sqrt(v):.4f}")
sel_items = []
for nm, (hr, lo, hi) in SEL.items():
    y, v = yv(hr, lo, hi); sel_items.append((y, v))
    print(f"  {nm:<18} HR {hr:.2f} ({lo:.2f}-{hi:.2f})  logHR={y:+.4f} SE={math.sqrt(v):.4f}")

# --- Sotagliflozin 2-trial fixed-effect pool ---
mu_s, var_s = fe_pool(sota_items)
se_s = math.sqrt(var_s)
# Cochran Q (k=2)
wf = [1.0/v for _, v in sota_items]; ys=[y for y,_ in sota_items]
muf = sum(w*y for w,y in zip(wf,ys))/sum(wf)
Q = sum(w*(y-muf)**2 for w,y in zip(wf,ys)); I2 = max(0.0,(Q-1)/Q)*100 if Q>0 else 0.0
print(f"\nSotagliflozin FE pool (k=2): HR={math.exp(mu_s):.3f} "
      f"(95% CI {math.exp(mu_s-Z*se_s):.3f}-{math.exp(mu_s+Z*se_s):.3f})")
print(f"  Q={Q:.3f} (df 1)  I^2={I2:.1f}%   [HKSJ at k=2 is uninformative -> FE reported]")

# --- Selective SGLT2i 4-trial fixed-effect pool ---
mu_c, var_c = fe_pool(sel_items); se_c = math.sqrt(var_c)
print(f"\nSelective SGLT2i FE pool (k=4): HR={math.exp(mu_c):.3f} "
      f"(95% CI {math.exp(mu_c-Z*se_c):.3f}-{math.exp(mu_c+Z*se_c):.3f})  logHR={mu_c:+.4f} SE={se_c:.4f}")

# --- Indirect (Bucher) comparison: sotagliflozin (both trials) vs selective ---
def indirect(mu_a, var_a, mu_b, var_b, label):
    d = mu_a - mu_b; sed = math.sqrt(var_a + var_b); z = d/sed
    p = 2*(1-norm.cdf(abs(z)))
    print(f"\n{label}")
    print(f"  Delta logHR = {d:+.4f}  SE = {sed:.4f}  z = {z:.3f}  p = {p:.3f}  "
          f"(HR ratio {math.exp(d):.3f})")
    return p

indirect(mu_s, var_s, mu_c, var_c,
         "INDIRECT: sotagliflozin (SOLOIST+SCORED) vs selective SGLT2i")

# --- Leave-SOLOIST-out sensitivity: SCORED alone (untruncated) vs selective ---
y_scored, v_scored = yv(*SOTA["SCORED"])
indirect(y_scored, v_scored, mu_c, var_c,
         "SENSITIVITY (leave-SOLOIST-out): SCORED alone vs selective SGLT2i")

print("\n" + "="*68)
print("Interpretation: sotagliflozin's numerically lower pooled HR (0.72) vs the")
print("selective-SGLT2i estimate (0.78) is NOT statistically distinguishable")
print("(indirect p~0.29); dropping the early-terminated SOLOIST trial (SCORED")
print("alone 0.74) attenuates the gap further (p~0.58). Endpoint incompatibility")
print("(recurrent-event rate ratio vs time-to-first HR) is an additional, ")
print("unquantifiable source of the apparent difference. No superiority is shown.")
