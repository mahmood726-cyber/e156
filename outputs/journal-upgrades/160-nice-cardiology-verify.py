#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of View/160
(NICECardiology: SGLT2-inhibitor class effect + guideline-adoption critique).

Reproduces the pooled class effect on the composite of cardiovascular death or
heart-failure hospitalisation (CV-death/HHF) across the eight pivotal
SGLT2-inhibitor trials, and adds NEW analyses not in v1:

  * REML (primary) + Paule-Mandel + DerSimonian-Laird tau^2, each with a
    Hartung-Knapp-Sidik-Jonkman (HKSJ) t_{k-1} CI (q>=1 floor) AND the
    DL+z CI that v1 reported (for a like-for-like reproduction of "0.74-0.84").
  * Cochran Q, I^2, and the Q p-value (reproduces v1's Q=7.61, p=0.37).
  * 95% prediction interval (t_{k-1}).
  * Leave-one-out influence analysis.
  * Trial-type subgroup + interaction test: 4 dedicated HF trials vs
    4 diabetes cardiovascular-outcome trials (CVOTs) -- NEW.
  * Monte-Carlo reversal probability P(HR>=1) from the fitted RE distribution
    (seeded, deterministic).
  * E-value for the point estimate and the CI bound closest to the null.

Every composite HR is the CV-death/HHF endpoint as reported in each trial's
primary publication (PMIDs listed). No AACT or external data required.
Requires numpy + scipy. Read-only; prints the numbers pasted into the paper.
"""
import math
import numpy as np
from scipy import optimize
from scipy.stats import t as tdist, norm, chi2

Z = 1.959963985  # qnorm(0.975)

# name, HR, lo, hi, agent, class ("HF"=dedicated HF trial, "CVOT"=diabetes CVOT), PMID
TRIALS = [
    ("EMPA-REG OUTCOME",  0.66, 0.55, 0.79, "Empagliflozin",  "CVOT", "26378978"),
    ("CANVAS",            0.78, 0.67, 0.91, "Canagliflozin",  "CVOT", "28605608"),
    ("DECLARE-TIMI 58",   0.83, 0.73, 0.95, "Dapagliflozin",  "CVOT", "30415602"),
    ("DAPA-HF",           0.75, 0.65, 0.85, "Dapagliflozin",  "HF",   "31535829"),
    ("EMPEROR-Reduced",   0.75, 0.65, 0.86, "Empagliflozin",  "HF",   "32865377"),
    ("VERTIS CV",         0.88, 0.75, 1.03, "Ertugliflozin",  "CVOT", "32966714"),
    ("EMPEROR-Preserved", 0.79, 0.69, 0.90, "Empagliflozin",  "HF",   "34449189"),
    ("DELIVER",           0.82, 0.73, 0.92, "Dapagliflozin",  "HF",   "36027570"),
]

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
    if f(0.0) <= 0:
        return 0.0
    hi = 10.0
    while f(hi) > 0 and hi < 1e6:
        hi *= 2
    return optimize.brentq(f, 0.0, hi)

def dl_tau2(y, v):
    y = np.asarray(y); v = np.asarray(v); k = len(y)
    w = 1.0 / v
    mu = np.sum(w * y) / np.sum(w)
    Q = np.sum(w * (y - mu) ** 2)
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    return max(0.0, (Q - (k - 1)) / c)

def het(y, v):
    y = np.asarray(y); v = np.asarray(v); k = len(y)
    w = 1.0 / v
    mu = np.sum(w * y) / np.sum(w)
    Q = float(np.sum(w * (y - mu) ** 2))
    df = k - 1
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    p = 1.0 - chi2.cdf(Q, df)
    return Q, df, I2, p

def pool(y, v, tau2):
    y = np.asarray(y); v = np.asarray(v); k = len(y)
    w = 1.0 / (v + tau2)
    mu = float(np.sum(w * y) / np.sum(w))
    var_mu = 1.0 / np.sum(w)
    # HKSJ (q>=1 floor, t_{k-1})
    q = np.sum(w * (y - mu) ** 2) / (k - 1)
    q = max(1.0, q)
    se_hk = math.sqrt(q * var_mu)
    tc = tdist.ppf(0.975, k - 1)
    hk = (mu - tc * se_hk, mu + tc * se_hk)
    # DL/RE + z (v1-style)
    se = math.sqrt(var_mu)
    zc = (mu - Z * se, mu + Z * se)
    # 95% PI t_{k-1}
    se_pi = math.sqrt(tau2 + var_mu)
    pi = (mu - tc * se_pi, mu + tc * se_pi)
    return mu, var_mu, hk, zc, pi

def show(label, y, v, tau2):
    mu, var_mu, hk, zc, pi = pool(y, v, tau2)
    print(f"  [{label}] tau^2={tau2:.5f}  HR={math.exp(mu):.4f}")
    print(f"       HKSJ 95% CI {math.exp(hk[0]):.4f}-{math.exp(hk[1]):.4f}"
          f"   RE+z 95% CI {math.exp(zc[0]):.4f}-{math.exp(zc[1]):.4f}")
    print(f"       95% PI {math.exp(pi[0]):.4f}-{math.exp(pi[1]):.4f}")
    return mu, var_mu

ys, vs = [], []
print("SGLT2-inhibitor class effect on CV-death/HHF -- 8 pivotal trials\n")
for name, hr, lo, hi, agent, cls, pmid in TRIALS:
    y, v = yv(hr, lo, hi); ys.append(y); vs.append(v)
    print(f"  {name:<18} {agent:<14} {cls:<4} HR {hr:.2f} ({lo:.2f}-{hi:.2f})"
          f"  logHR={y:+.4f} SE={math.sqrt(v):.4f}  PMID {pmid}")

tR, tP, tD = reml_tau2(ys, vs), pm_tau2(ys, vs), dl_tau2(ys, vs)
Q, df, I2, pQ = het(ys, vs)
print(f"\nHeterogeneity: Q={Q:.2f} (df={df}), I^2={I2:.1f}%, p={pQ:.3f}")
print(f"tau^2: REML={tR:.5f}  PM={tP:.5f}  DL={tD:.5f}\n")
print("Pooled class effect (8 trials):")
muR, var_muR = show("REML", ys, vs, tR)
show("PM", ys, vs, tP)
muD, var_muD = show("DL ", ys, vs, tD)

# Leave-one-out (REML)
print("\nLeave-one-out (REML + HKSJ):")
for i in range(len(TRIALS)):
    yy = [ys[j] for j in range(len(ys)) if j != i]
    vv = [vs[j] for j in range(len(vs)) if j != i]
    t2 = reml_tau2(yy, vv)
    mu, _, hk, _, _ = pool(yy, vv, t2)
    print(f"  -{TRIALS[i][0]:<18} HR={math.exp(mu):.4f} "
          f"({math.exp(hk[0]):.4f}-{math.exp(hk[1]):.4f})")

# NEW: trial-type subgroup + interaction (fixed-effect within subgroup)
def fe(idx):
    yy = np.array([ys[i] for i in idx]); vv = np.array([vs[i] for i in idx])
    w = 1.0 / vv
    mu = float(np.sum(w * yy) / np.sum(w))
    se = math.sqrt(1.0 / np.sum(w))
    return mu, se
hf_idx  = [i for i, t in enumerate(TRIALS) if t[5] == "HF"]
cvot_idx = [i for i, t in enumerate(TRIALS) if t[5] == "CVOT"]
mh, seh = fe(hf_idx); mc, sec = fe(cvot_idx)
diff = mh - mc; sed = math.sqrt(seh**2 + sec**2); zi = diff / sed
pint = 2 * (1 - norm.cdf(abs(zi)))
print("\nNEW -- trial-type subgroup (fixed-effect within group):")
print(f"  Dedicated HF trials (k=4)  HR={math.exp(mh):.4f} "
      f"({math.exp(mh-Z*seh):.4f}-{math.exp(mh+Z*seh):.4f})")
print(f"  Diabetes CVOTs      (k=4)  HR={math.exp(mc):.4f} "
      f"({math.exp(mc-Z*sec):.4f}-{math.exp(mc+Z*sec):.4f})")
print(f"  Interaction HR-ratio={math.exp(diff):.4f}  z={zi:.2f}  p_interaction={pint:.3f}")

# Monte-Carlo reversal probability from fitted RE (REML mu, tau^2 + var_mu)
rng = np.random.default_rng(20260709)
sd_total = math.sqrt(tR + var_muR)
draws = rng.normal(muR, sd_total, 200000)
p_rev = float(np.mean(draws >= 0.0))
# analytic check
p_rev_analytic = 1 - norm.cdf((0 - muR) / sd_total)
print(f"\nMonte-Carlo reversal P(HR>=1): {p_rev:.5f} "
      f"(analytic {p_rev_analytic:.5f}); seed=20260709, n=200000")

# E-value (VanderWeele & Ding 2017) for a rate/hazard ratio < 1
def evalue(rr):
    rr = 1.0 / rr if rr < 1 else rr  # map protective to >1
    return rr + math.sqrt(rr * (rr - 1))
hr_pt = math.exp(muR)
hr_hi = math.exp(pool(ys, vs, tR)[3][1])  # RE+z upper bound (closest to null)
print(f"\nE-value: point HR {hr_pt:.3f} -> {evalue(hr_pt):.2f};"
      f" CI bound {hr_hi:.3f} -> {evalue(hr_hi):.2f}")

# NNT from a representative dedicated-HF control event rate
# DAPA-HF placebo CV-death/HHF ~ 21.2 per 100 pt-yr (McMurray 2019). ARR = CER*(1-HR).
cer = 0.212
arr = cer * (1 - hr_pt)
print(f"\nNNT (per patient-year; CER={cer:.3f} from DAPA-HF placebo arm, HR={hr_pt:.3f}):"
      f" ARR={arr:.4f}, NNT={1/arr:.1f}")
