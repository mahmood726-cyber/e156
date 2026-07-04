#!/usr/bin/env python
"""
Deterministic meta-analysis of EARLY INTERVENTION vs CONSERVATIVE / SURVEILLANCE
in asymptomatic severe aortic stenosis, for the v2 advanced version of the
Synthesis paper "AS-Logic: The Tipping Point in Asymptomatic Severe Aortic
Stenosis" (View/14).

All inputs are taken verbatim from the PUBLISHED trial abstracts (PubMed metadata
verified 2026-07-04; title + journal + DOI matched before use):

  RECOVERY   Kang 2020    NEJM   n=145  PMID 31733181  NCT01161732
     very severe AS (AVA<=0.75 + Vmax>=4.5 or MG>=50); surgical AVR
     PRIMARY (operative mortality OR CV death): 1/73 vs 11/72
        HR 0.09 (0.01-0.67), p=0.003
     all-cause death (major secondary): 5/73 vs 15/72  HR 0.33 (0.12-0.90)
  AVATAR     Banovic 2022 Circulation n=157 PMID 34779220 NCT02436655
     standard severe AS (AVA<=1.0 + Vmax>4 or MG>=40), neg. exercise test; SAVR
     PRIMARY (all-cause death/AMI/stroke/unplanned HF hosp): 13/78 vs 26/79
        HR 0.46 (0.23-0.90), p=0.02
  EARLY TAVR Genereux 2024 NEJM n=901 PMID 39466903 NCT03042104
     asymptomatic severe AS, preserved EF; balloon-expandable TAVR vs surveillance
     PRIMARY (death/stroke/unplanned CV hosp): 122/455 (26.8%) vs 202/446 (45.3%)
        HR 0.50 (0.40-0.63), P<0.001;  death 8.4% vs 9.2%
  EVOLVED    2024         JAMA   n=224  PMID 39466640  NCT03094143
     severe AS + midwall myocardial fibrosis (CMR); TAVR or SAVR vs GDC
     PRIMARY (all-cause death OR unplanned AS hosp): 20/113 (18%) vs 25/111 (23%)
        HR 0.79 (0.44-1.43), p=0.44
        all-cause death 16/113 vs 14/111  HR 1.22 (0.59-2.51)
        unplanned AS hosp 7/113 vs 19/111  HR 0.37 (0.16-0.88)

Published comparator meta-analysis used ONLY as an external benchmark (not re-run):
  Genereux/Lindman-era study-level MA, JACC 2024, PMID 39641732 (4 RCTs, N=1,427):
     unplanned CV/HF hosp   HR 0.40 (0.30-0.53)  I2=4%
     stroke                 HR 0.62 (0.40-0.97)  I2=0%
     all-cause mortality    HR 0.68 (0.40-1.17)  I2=61%
     cardiovascular mortality HR 0.67 (0.35-1.29) I2=50%

Methods (per small-k rules): pool on log-HR scale; REML tau^2 (primary) with
Paule-Mandel sensitivity; Hartung-Knapp-Sidik-Jonkman CI using t_{k-1} with the
q>=1 floor; Cochran Q and I^2 from fixed-effect weights; 95% prediction interval
with t_{k-1}. Deterministic. Requires numpy + scipy.
"""
import math
import numpy as np
from scipy import optimize
from scipy.stats import t as tdist, norm

Z = 1.959963985

# name, HR, lo, hi, endpoint label, population
TRIALS = {
    "RECOVERY":   (0.09, 0.01, 0.67, "op.mort/CV death", "very severe AS"),
    "AVATAR":     (0.46, 0.23, 0.90, "death/AMI/stroke/HFhosp", "standard severe AS"),
    "EARLY TAVR": (0.50, 0.40, 0.63, "death/stroke/CV hosp", "severe AS, preserved EF"),
    "EVOLVED":    (0.79, 0.44, 1.43, "death/AS hosp", "severe AS + fibrosis"),
}

def yv(hr, lo, hi):
    y = math.log(hr)
    se = (math.log(hi) - math.log(lo)) / (2 * Z)
    return y, se * se

def reml_tau2(y, v):
    y = np.asarray(y); v = np.asarray(v)
    def neg_ll(lt2):
        t2 = math.exp(lt2)
        w = 1.0 / (v + t2)
        mu = np.sum(w * y) / np.sum(w)
        return -(-0.5 * np.sum(np.log(v + t2))
                 - 0.5 * math.log(np.sum(w))
                 - 0.5 * np.sum(w * (y - mu) ** 2))
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
    q = np.sum(w * (y - mu) ** 2) / (k - 1)
    q = max(1.0, q)
    var_hk = q * var_mu
    tcrit = tdist.ppf(0.975, k - 1)
    hk_lo, hk_hi = mu - tcrit * math.sqrt(var_hk), mu + tcrit * math.sqrt(var_hk)
    wf = 1.0 / v
    muf = np.sum(wf * y) / np.sum(wf)
    Q = np.sum(wf * (y - muf) ** 2)
    df = k - 1
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    pi_lo = mu - tcrit * math.sqrt(tau2 + var_mu)
    pi_hi = mu + tcrit * math.sqrt(tau2 + var_mu)
    z_lo, z_hi = mu - Z * math.sqrt(var_mu), mu + Z * math.sqrt(var_mu)
    print(f"\n--- {label} (k={k}) ---")
    print(f"  tau^2={tau2:.5f}  Q={Q:.3f} (df {df})  I^2={I2:.1f}%")
    print(f"  Pooled HR = {math.exp(mu):.3f}  "
          f"(HKSJ 95% CI {math.exp(hk_lo):.3f}-{math.exp(hk_hi):.3f}; q-floored={q<=1.0})")
    print(f"    normal-approx 95% CI: {math.exp(z_lo):.3f}-{math.exp(z_hi):.3f}")
    print(f"  95% prediction interval HR: {math.exp(pi_lo):.3f}-{math.exp(pi_hi):.3f}")
    return math.exp(mu)

def run(names, label):
    ys, vs = [], []
    for nm in names:
        hr, lo, hi, *_ = TRIALS[nm]
        y, v = yv(hr, lo, hi); ys.append(y); vs.append(v)
    tR = reml_tau2(ys, vs); tP = pm_tau2(ys, vs)
    print(f"\n{'='*70}\n{label}\n  trials: {', '.join(names)}")
    print(f"  REML tau^2={tR:.5f} | Paule-Mandel tau^2={tP:.5f}")
    pool(ys, vs, tR, "REML + HKSJ (primary)")
    pool(ys, vs, tP, "Paule-Mandel + HKSJ (sensitivity)")

print("Asymptomatic severe AS — early intervention meta-analysis (deterministic)")
print(f"{'Trial':<12}{'endpoint':<26}{'HR (95% CI)':<20}{'logHR':>8} {'SE':>7}")
for nm, (hr, lo, hi, ep, pop) in TRIALS.items():
    y, v = yv(hr, lo, hi)
    print(f"{nm:<12}{ep:<26}{f'{hr:.2f} ({lo:.2f}-{hi:.2f})':<20}{y:>+8.4f} {math.sqrt(v):>7.4f}")

# Primary pool: three standard-population, broad-composite trials (incl. hospitalisation)
run(["AVATAR", "EARLY TAVR", "EVOLVED"],
    "MODEL 1 (PRIMARY) — standard severe AS, composite incl. hospitalisation")
# Sensitivity: add RECOVERY (very severe AS, CV-death-only endpoint -> expected outlier)
run(["RECOVERY", "AVATAR", "EARLY TAVR", "EVOLVED"],
    "MODEL 2 (SENSITIVITY) — all four trials incl. RECOVERY")

# --- NNT from each trial's own primary event rates (verified counts) ---
def nnt(ctrl_e, ctrl_n, exp_e, exp_n, label, horizon):
    arr = ctrl_e/ctrl_n - exp_e/exp_n
    print(f"  {label:<12} conservative {ctrl_e}/{ctrl_n}={ctrl_e/ctrl_n*100:.1f}%  "
          f"early {exp_e}/{exp_n}={exp_e/exp_n*100:.1f}%  "
          f"ARR={arr*100:.1f}pp  NNT={1/arr:.1f}  ({horizon})")

print(f"\n{'='*70}\nABSOLUTE BENEFIT — NNT from published primary-endpoint counts")
nnt(26, 79, 13, 78, "AVATAR",     "median 32 mo")
nnt(202, 446, 122, 455, "EARLY TAVR", "median ~2 yr")
nnt(11, 72, 1, 73, "RECOVERY",   "median ~6 yr, CV-death endpoint")
nnt(25, 111, 20, 113, "EVOLVED",  "median ~4 yr, fibrosis subgroup, NS")

# --- EVOLVED component dissociation (mortality up, hospitalisation down) ---
print(f"\n{'='*70}\nEVOLVED component dissociation (why the composite is null):")
print("  all-cause death   16/113 (14%) vs 14/111 (13%)  HR 1.22 (0.59-2.51)  -> no mortality benefit")
print("  unplanned AS hosp  7/113 (6%)  vs 19/111 (17%)  HR 0.37 (0.16-0.88)  -> hospitalisation reduced")
print("  NYHA II-IV @12mo  19.7% vs 37.9%  OR 0.37 (0.20-0.70)               -> symptom benefit")

print(f"\n{'='*70}\nEXTERNAL BENCHMARK (JACC 2024 study-level MA, PMID 39641732; not re-run):")
print("  unplanned CV/HF hosp  HR 0.40 (0.30-0.53) I2=4%   <- concordant, robust")
print("  stroke                HR 0.62 (0.40-0.97) I2=0%   <- concordant, robust")
print("  all-cause mortality   HR 0.68 (0.40-1.17) I2=61%  <- NOT significant, high heterogeneity")
print("  cardiovascular mort.  HR 0.67 (0.35-1.29) I2=50%  <- NOT significant")
print("\nInterpretation: early intervention robustly reduces HOSPITALISATION and")
print("STROKE across trials; a MORTALITY benefit is not established (CIs cross 1,")
print("driven by RECOVERY's outlier effect vs neutral EVOLVED/EARLY-TAVR mortality).")
