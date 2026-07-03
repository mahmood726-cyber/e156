#!/usr/bin/env python
"""
Deterministic random-effects meta-analysis of the primary composite endpoint
(cardiovascular death or worsening/hospitalised heart failure) across the pivotal
SGLT2-inhibitor heart-failure trials, for the v2 advanced versions of the
Synthesis SGLT2-HF living-meta-analysis papers (View/88, /94, /102).

Trial primary-composite hazard ratios (verified against the NEJM abstracts):
  DAPA-HF          McMurray 2019  HFrEF    HR 0.74 (0.65-0.85)  PMID 31535829
  EMPEROR-Reduced  Packer 2020    HFrEF    HR 0.75 (0.65-0.86)  PMID 32865377
  EMPEROR-Preserved Anker 2021    HFpEF    HR 0.79 (0.69-0.90)  PMID 34449189
  DELIVER          Solomon 2022   HFmrEF/pEF HR 0.82 (0.73-0.92) PMID 36027570
  SOLOIST-WHF      Bhatt 2021     recent WHF HR 0.67 (0.52-0.85) PMID 33200892
    (SOLOIST primary = total [recurrent] events -> rate ratio, not a first-event
     HR; included only in a sensitivity pool and flagged.)

Methods (per small-k meta-analysis rules): pool on the log-HR scale; REML tau^2
(primary) with Paule-Mandel as sensitivity (DerSimonian-Laird shown for contrast
only, not used for inference at k<10); Hartung-Knapp-Sidik-Jonkman (HKSJ) CI using
t_{k-1} with the q>=1 floor; I^2 and Cochran Q; 95% prediction interval with
t_{k-1}. Deterministic; requires numpy + scipy.
"""
import math
import numpy as np
from scipy import optimize
from scipy.stats import t as tdist, norm, chi2

TRIALS = [
    ("DAPA-HF",          0.74, 0.65, 0.85, "HFrEF"),
    ("EMPEROR-Reduced",  0.75, 0.65, 0.86, "HFrEF"),
    ("EMPEROR-Preserved",0.79, 0.69, 0.90, "HFpEF"),
    ("DELIVER",          0.82, 0.73, 0.92, "HFmrEF/HFpEF"),
    ("SOLOIST-WHF",      0.67, 0.52, 0.85, "recent WHF (rate ratio)"),
]

def yv(hr, lo, hi):
    y = math.log(hr)
    se = (math.log(hi) - math.log(lo)) / (2 * 1.959963985)
    return y, se * se  # log-HR and its variance

def reml_tau2(y, v):
    y = np.asarray(y); v = np.asarray(v); k = len(y)
    def neg_ll(lt2):
        t2 = math.exp(lt2)
        w = 1.0 / (v + t2)
        mu = np.sum(w * y) / np.sum(w)
        ll = (-0.5 * np.sum(np.log(v + t2))
              - 0.5 * math.log(np.sum(w))
              - 0.5 * np.sum(w * (y - mu) ** 2))
        return -ll
    r = optimize.minimize_scalar(neg_ll, bounds=(-20, 5), method="bounded")
    return math.exp(r.x)

def pm_tau2(y, v):
    y = np.asarray(y); v = np.asarray(v); k = len(y)
    def f(t2):
        w = 1.0 / (v + t2)
        mu = np.sum(w * y) / np.sum(w)
        return np.sum(w * (y - mu) ** 2) - (k - 1)
    if f(0) <= 0:
        return 0.0
    hi = 10.0
    while f(hi) > 0 and hi < 1e6:
        hi *= 2
    return optimize.brentq(f, 0, hi)

def pool(y, v, tau2, label):
    y = np.asarray(y); v = np.asarray(v); k = len(y)
    w = 1.0 / (v + tau2)
    mu = np.sum(w * y) / np.sum(w)
    var_mu = 1.0 / np.sum(w)
    # HKSJ variance with q>=1 floor
    q = np.sum(w * (y - mu) ** 2) / (k - 1)
    q = max(1.0, q)
    var_hk = q * var_mu
    tcrit = tdist.ppf(0.975, k - 1)
    hk_lo, hk_hi = mu - tcrit * math.sqrt(var_hk), mu + tcrit * math.sqrt(var_hk)
    # Cochran Q, I^2 (fixed-effect weights)
    wf = 1.0 / v
    muf = np.sum(wf * y) / np.sum(wf)
    Q = np.sum(wf * (y - muf) ** 2)
    df = k - 1
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    # prediction interval t_{k-1}
    pi_lo = mu - tdist.ppf(0.975, k - 1) * math.sqrt(tau2 + var_mu)
    pi_hi = mu + tdist.ppf(0.975, k - 1) * math.sqrt(tau2 + var_mu)
    print(f"\n--- {label} (k={k}) ---")
    print(f"  tau^2 = {tau2:.5f}   Q = {Q:.3f} (df {df})   I^2 = {I2:.1f}%")
    print(f"  Pooled HR = {math.exp(mu):.3f}  (HKSJ 95% CI {math.exp(hk_lo):.3f}-{math.exp(hk_hi):.3f}; q-floored={q>1.0})")
    z_lo, z_hi = mu - 1.96*math.sqrt(var_mu), mu + 1.96*math.sqrt(var_mu)
    print(f"    (normal 95% CI for contrast: {math.exp(z_lo):.3f}-{math.exp(z_hi):.3f})")
    print(f"  95% prediction interval HR: {math.exp(pi_lo):.3f}-{math.exp(pi_hi):.3f}")

def run(subset, label):
    ys, vs = [], []
    for name, hr, lo, hi, ef in subset:
        y, v = yv(hr, lo, hi); ys.append(y); vs.append(v)
    tR = reml_tau2(ys, vs); tP = pm_tau2(ys, vs)
    print(f"\n{'='*66}\n{label}\n  trials: {', '.join(t[0] for t in subset)}")
    print(f"  REML tau^2={tR:.5f} | Paule-Mandel tau^2={tP:.5f}")
    pool(ys, vs, tR, "REML + HKSJ")
    pool(ys, vs, tP, "Paule-Mandel + HKSJ (sensitivity)")

print("SGLT2-inhibitor heart-failure meta-analysis — deterministic verification")
for name, hr, lo, hi, ef in TRIALS:
    y, v = yv(hr, lo, hi)
    print(f"  {name:<18} {ef:<24} HR {hr:.2f} ({lo:.2f}-{hi:.2f})  logHR={y:+.4f} SE={math.sqrt(v):.4f}")
run(TRIALS[:4], "PRIMARY POOL — 4 first-event-HR trials (SOLOIST excluded)")
run(TRIALS, "SENSITIVITY — all 5 trials (SOLOIST rate-ratio included)")
run(TRIALS[:2], "HFrEF-only (DAPA-HF + EMPEROR-Reduced)")

# --- EF-spectrum subgroup analysis + interaction (for paper 94) ---
def fe(items):
    ws = [1.0 / v for _, v in items]
    ys = [y for y, _ in items]
    mu = sum(w * y for w, (y, _) in zip(ws, items)) / sum(ws)
    se = math.sqrt(1.0 / sum(ws))
    return mu, se
rEF = [yv(*t[1:4]) for t in TRIALS[:2]]                 # DAPA-HF, EMPEROR-Reduced
pEF = [yv(TRIALS[2][1], TRIALS[2][2], TRIALS[2][3]),
       yv(TRIALS[3][1], TRIALS[3][2], TRIALS[3][3])]     # EMPEROR-Preserved, DELIVER
# yv returns (y, v); fe expects (y, v) with v=variance -> adapt
def yv2(hr, lo, hi):
    y = math.log(hr); se = (math.log(hi) - math.log(lo)) / (2 * 1.959963985)
    return y, se * se
rEF = [yv2(t[1], t[2], t[3]) for t in TRIALS[:2]]
pEF = [yv2(t[1], t[2], t[3]) for t in TRIALS[2:4]]
mr, ser = fe(rEF); mp, sep = fe(pEF)
diff = mr - mp; sed = math.sqrt(ser**2 + sep**2); z = diff / sed
p_int = 2 * (1 - norm.cdf(abs(z)))
print(f"\n{'='*66}\nEF-SPECTRUM SUBGROUP ANALYSIS (paper 94)")
print(f"  HFrEF (DAPA-HF+EMPEROR-Reduced)  HR={math.exp(mr):.3f} "
      f"({math.exp(mr-1.96*ser):.3f}-{math.exp(mr+1.96*ser):.3f})")
print(f"  HFmrEF/HFpEF (EMP-Pres+DELIVER)  HR={math.exp(mp):.3f} "
      f"({math.exp(mp-1.96*sep):.3f}-{math.exp(mp+1.96*sep):.3f})")
print(f"  Interaction: HR-ratio={math.exp(diff):.3f}, z={z:.2f}, p_interaction={p_int:.3f}")
