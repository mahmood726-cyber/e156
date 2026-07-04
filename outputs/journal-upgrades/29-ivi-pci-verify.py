#!/usr/bin/env python
"""
Deterministic meta-analysis for the v2 advanced version of the Synthesis paper
"IVI-Guided PCI: Systematic Review and Meta-Analysis" (View/29).

Verified RCT inputs (PubMed title+journal+DOI matched 2026-07-04):
  IVUS-XPL     Hong 2015  JAMA          IVUS  HR 0.48 (0.28-0.83)  PMID 26556051
  ULTIMATE-3yr Gao 2021   JACC Interv   IVUS  events 47/714 vs 76/734 (no HR in
                                              abstract -> logRR from counts)  PMID 33541535
  OCTOBER      Holm 2023  NEJM          OCT   HR 0.70 (0.50-0.98)  PMID 37634149
  ILUMIEN IV   Ali 2023   NEJM          OCT   HR 0.90 (0.67-1.19)  PMID 37634188

Methods: pool on log-scale. REML random-effects (primary) with Paule-Mandel
sensitivity; HKSJ CI with t_{k-1} and q>=1 floor; Cochran Q / I^2 (fixed-effect
weights); 95% prediction interval t_{k-1}; leave-one-out; IVUS vs OCT subgroups
(k=2 each -> flagged uninformative). Small-study check: rank correlation of effect
vs SE (Begg-style) reported descriptively (k=4 -> underpowered, descriptive only).
Deterministic; requires numpy + scipy.
"""
import math
import numpy as np
from scipy import optimize
from scipy.stats import t as tdist, norm

Z = 1.959963985

def yv_from_ci(hr, lo, hi):
    y = math.log(hr); se = (math.log(hi) - math.log(lo)) / (2 * Z)
    return y, se * se

def yv_from_counts(a, n1, b, n2):
    # log risk ratio and its variance (large-sample)
    y = math.log(a / n1) - math.log(b / n2)
    v = 1.0/a - 1.0/n1 + 1.0/b - 1.0/n2
    return y, v

TRIALS = []
TRIALS.append(("IVUS-XPL", "IVUS") + yv_from_ci(0.48, 0.28, 0.83))
y, v = yv_from_counts(47, 714, 76, 734)
TRIALS.append(("ULTIMATE-3yr", "IVUS", y, v))
TRIALS.append(("OCTOBER", "OCT") + yv_from_ci(0.70, 0.50, 0.98))
TRIALS.append(("ILUMIEN IV", "OCT") + yv_from_ci(0.90, 0.67, 1.19))

def reml_tau2(y, v):
    y = np.asarray(y); v = np.asarray(v)
    def neg_ll(lt2):
        t2 = math.exp(lt2); w = 1.0/(v+t2); mu = np.sum(w*y)/np.sum(w)
        return -(-0.5*np.sum(np.log(v+t2)) - 0.5*math.log(np.sum(w)) - 0.5*np.sum(w*(y-mu)**2))
    r = optimize.minimize_scalar(neg_ll, bounds=(-20, 5), method="bounded")
    return math.exp(r.x)

def pm_tau2(y, v):
    y=np.asarray(y); v=np.asarray(v); k=len(y)
    def f(t2):
        w=1.0/(v+t2); mu=np.sum(w*y)/np.sum(w); return np.sum(w*(y-mu)**2)-(k-1)
    if f(0)<=0: return 0.0
    hi=10.0
    while f(hi)>0 and hi<1e6: hi*=2
    return optimize.brentq(f,0,hi)

def pool(y, v, tau2, label):
    y=np.asarray(y); v=np.asarray(v); k=len(y)
    w=1.0/(v+tau2); mu=np.sum(w*y)/np.sum(w); var_mu=1.0/np.sum(w)
    q=np.sum(w*(y-mu)**2)/(k-1); q=max(1.0,q); var_hk=q*var_mu
    tcrit=tdist.ppf(0.975,k-1)
    hk=(mu-tcrit*math.sqrt(var_hk), mu+tcrit*math.sqrt(var_hk))
    wf=1.0/v; muf=np.sum(wf*y)/np.sum(wf); Q=np.sum(wf*(y-muf)**2); df=k-1
    I2=max(0.0,(Q-df)/Q)*100 if Q>0 else 0.0
    pi=(mu-tcrit*math.sqrt(tau2+var_mu), mu+tcrit*math.sqrt(tau2+var_mu))
    print(f"\n--- {label} (k={k}) ---")
    print(f"  tau^2={tau2:.4f}  Q={Q:.3f} (df {df})  I^2={I2:.1f}%")
    print(f"  Pooled HR={math.exp(mu):.3f}  HKSJ 95% CI {math.exp(hk[0]):.3f}-{math.exp(hk[1]):.3f}  (q-floored={q<=1.0})")
    print(f"  95% PI HR: {math.exp(pi[0]):.3f}-{math.exp(pi[1]):.3f}")
    return math.exp(mu), math.exp(hk[0]), math.exp(hk[1]), I2

print("IVI-guided vs angiography-guided PCI — deterministic meta-analysis (v2)")
print(f"{'Trial':<14}{'mod':<6}{'logHR':>9}{'SE':>9}{'effect':>18}")
for nm, mod, y, v in TRIALS:
    print(f"{nm:<14}{mod:<6}{y:>+9.4f}{math.sqrt(v):>9.4f}{math.exp(y):>10.3f} (from data)")

ys=[t[2] for t in TRIALS]; vs=[t[3] for t in TRIALS]
tR=reml_tau2(ys,vs); tP=pm_tau2(ys,vs)
print(f"\nREML tau^2={tR:.4f} | Paule-Mandel tau^2={tP:.4f}")
pool(ys,vs,tR,"PRIMARY (REML + HKSJ)")
pool(ys,vs,tP,"SENSITIVITY (Paule-Mandel + HKSJ)")

print("\n" + "="*60 + "\nLEAVE-ONE-OUT (REML + HKSJ):")
for i in range(len(TRIALS)):
    sub=[t for j,t in enumerate(TRIALS) if j!=i]
    yy=[t[2] for t in sub]; vv=[t[3] for t in sub]
    tt=reml_tau2(yy,vv)
    hr,lo,hi,I2=pool(yy,vv,tt,f"omit {TRIALS[i][0]}")

print("\n" + "="*60 + "\nSUBGROUPS (k=2 each -> HKSJ uninformative, point est. only):")
for mod in ("IVUS","OCT"):
    sub=[t for t in TRIALS if t[1]==mod]
    yy=[t[2] for t in sub]; vv=[t[3] for t in sub]
    tt=reml_tau2(yy,vv)
    pool(yy,vv,tt,f"{mod} subgroup ({', '.join(t[0] for t in sub)})")

# Small-study check (descriptive; k=4 underpowered)
se=np.sqrt(vs); rho=np.corrcoef(ys, se)[0,1]
print("\n" + "="*60)
print(f"Small-study descriptive check: corr(logHR, SE) = {rho:+.3f} across k=4")
print("  (k=4 far below the k>=10 threshold for Egger/Begg; reported as descriptive")
print("   only. A positive corr would hint smaller trials show larger effects.)")
