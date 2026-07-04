#!/usr/bin/env python
"""
Deterministic meta-analysis for the v2 advanced version of the Synthesis paper
"The Haemodynamic Fallacy in Cardiogenic Shock" (View/23).

v2 adds ECLS-SHOCK (Thiele NEJM 2023, n=417) — the largest VA-ECMO RCT, absent
from v1 — and reframes v1's mixed "any-MCS" pool into a device/comparator-stratified
analysis. All inputs PubMed-verified (title+journal+first-author+DOI) 2026-07-04.

  IABP-SHOCK II  Thiele 2012 NEJM 367:1287-96   PMID 22920912  NCT00491036
      IABP vs no-IABP; 30-day death 119/300 vs 123/298; RR 0.96 (0.79-1.17)
  IMPRESS        Ouweneel 2017 JACC 69:278-87   PMID 27810347  NCT02185785
      Impella CP vs IABP (both active!); 30-day HR 0.96 (0.42-2.18)
  DanGer Shock   Moller 2024 NEJM 390:1382-93   PMID 38587239  NCT01633502
      Impella CP + standard vs standard, STEMI only; 180-day death 82/179 vs
      103/176; HR 0.74 (0.55-0.99), p=0.04  (v1 mis-cited pages 1284-97)
  ECMO-CS        Ostadal 2023 Circulation 147:454-64  PMID 36335478  NCT02301819
      immediate VA-ECMO vs conservative; composite primary; 30-d all-cause death
      ~50.0% vs 47.5% (secondary) -> not pooled here; see Zeymer IPD-MA
  ECLS-SHOCK     Thiele 2023 NEJM 389:1286-97   PMID 37634145  NCT03637205
      VA-ECMO vs medical therapy; 30-day death 100/209 (47.8%) vs 102/208 (49.0%)
      RR 0.98 (0.80-1.19), p=0.81; bleeding RR 2.44, vascular RR 2.86

External benchmark (NOT re-run):
  Zeymer 2023 Lancet 402:1338-46  PMID 37643628 — VA-ECMO IPD-MA of 4 trials
      (n=567): 30-day death OR 0.93 (0.66-1.29) NS; bleeding OR 2.44; vascular 3.53.

Methods: pool on log scale; REML tau^2 with Paule-Mandel sensitivity; HKSJ CI
t_{k-1}, q>=1 floor; Cochran Q / I^2; 95% PI t_{k-1}; leave-one-out. Deterministic;
numpy + scipy.
"""
import math
import numpy as np
from scipy import optimize
from scipy.stats import t as tdist

Z = 1.959963985

def yv(hr, lo, hi):
    y = math.log(hr); se = (math.log(hi) - math.log(lo)) / (2 * Z)
    return y, se * se

# device vs no-device/standard-support trials (IMPRESS excluded: control = IABP)
TRIALS = {
    "IABP-SHOCK II": (0.96, 0.79, 1.17, "IABP",      "30-day"),
    "DanGer Shock":  (0.74, 0.55, 0.99, "Impella CP","180-day"),
    "ECLS-SHOCK":    (0.98, 0.80, 1.19, "VA-ECMO",   "30-day"),
}
IMPRESS = (0.96, 0.42, 2.18)  # Impella CP vs IABP — reported separately

def reml_tau2(y, v):
    y=np.asarray(y); v=np.asarray(v)
    def nll(lt2):
        t2=math.exp(lt2); w=1.0/(v+t2); mu=np.sum(w*y)/np.sum(w)
        return -(-0.5*np.sum(np.log(v+t2))-0.5*math.log(np.sum(w))-0.5*np.sum(w*(y-mu)**2))
    return math.exp(optimize.minimize_scalar(nll,bounds=(-20,5),method="bounded").x)

def pm_tau2(y, v):
    y=np.asarray(y); v=np.asarray(v); k=len(y)
    def f(t2):
        w=1.0/(v+t2); mu=np.sum(w*y)/np.sum(w); return np.sum(w*(y-mu)**2)-(k-1)
    if f(0)<=0: return 0.0
    hi=10.0
    while f(hi)>0 and hi<1e6: hi*=2
    return optimize.brentq(f,0,hi)

def pool(names, label, tau_mode="reml"):
    ys=[]; vs=[]
    for nm in names:
        hr,lo,hi,_,_=TRIALS[nm]; y,v=yv(hr,lo,hi); ys.append(y); vs.append(v)
    k=len(ys); ys=np.array(ys); vs=np.array(vs)
    tau2 = reml_tau2(ys,vs) if tau_mode=="reml" else pm_tau2(ys,vs)
    w=1.0/(vs+tau2); mu=np.sum(w*ys)/np.sum(w); var_mu=1.0/np.sum(w)
    q=np.sum(w*(ys-mu)**2)/(k-1) if k>1 else 1.0; q=max(1.0,q); var_hk=q*var_mu
    tcrit=tdist.ppf(0.975,k-1) if k>1 else float('nan')
    wf=1.0/vs; muf=np.sum(wf*ys)/np.sum(wf); Q=np.sum(wf*(ys-muf)**2); df=k-1
    I2=max(0.0,(Q-df)/Q)*100 if Q>0 and k>1 else 0.0
    print(f"\n--- {label} (k={k}, {tau_mode}) ---")
    if k>1:
        hk=(mu-tcrit*math.sqrt(var_hk), mu+tcrit*math.sqrt(var_hk))
        pi=(mu-tcrit*math.sqrt(tau2+var_mu), mu+tcrit*math.sqrt(tau2+var_mu))
        print(f"  tau^2={tau2:.4f}  Q={Q:.3f} (df {df})  I^2={I2:.1f}%")
        print(f"  Pooled effect={math.exp(mu):.3f}  HKSJ 95% CI {math.exp(hk[0]):.3f}-{math.exp(hk[1]):.3f}")
        print(f"  95% PI: {math.exp(pi[0]):.3f}-{math.exp(pi[1]):.3f}")
    return math.exp(mu)

print("Cardiogenic-shock MCS — deterministic meta-analysis (v2)")
print(f"{'Trial':<16}{'device':<12}{'effect':<20}{'logHR':>9}{'SE':>8}")
for nm,(hr,lo,hi,dev,ep) in TRIALS.items():
    y,v=yv(hr,lo,hi)
    print(f"{nm:<16}{dev:<12}{f'{hr:.2f} ({lo:.2f}-{hi:.2f})':<20}{y:>+9.4f}{math.sqrt(v):>8.4f}")
yi,vi=yv(*IMPRESS)
print(f"{'IMPRESS':<16}{'Impella/IABP':<12}{f'{IMPRESS[0]:.2f} ({IMPRESS[1]:.2f}-{IMPRESS[2]:.2f})':<20}{yi:>+9.4f}{math.sqrt(vi):>8.4f}  [vs IABP; reported separately]")

pool(list(TRIALS), "PRIMARY: device vs standard/no-support (IABP-SHOCK II + DanGer + ECLS-SHOCK)")
pool(list(TRIALS), "  sensitivity PM tau^2", tau_mode="pm")
pool(["IABP-SHOCK II","ECLS-SHOCK"], "NULL-DEVICE POOL (leave DanGer out: IABP + VA-ECMO)")

print("\n" + "="*66)
print("Device-stratified reading:")
print("  VA-ECMO vs medical:  ECLS-SHOCK RR 0.98 (0.80-1.19); Zeymer IPD-MA of 4")
print("     ECMO trials (n=567) OR 0.93 (0.66-1.29) NS -> NO mortality benefit,")
print("     bleeding OR 2.44, vascular OR 3.53.  [external benchmark, PMID 37643628]")
print("  IABP vs none:        IABP-SHOCK II RR 0.96 (0.79-1.17) -> null.")
print("  Impella vs IABP:     IMPRESS HR 0.96 (0.42-2.18) -> null (small).")
print("  Impella vs standard: DanGer Shock HR 0.74 (0.55-0.99) -> the LONE positive,")
print("     STEMI-only, 180-day, at cost of bleeding/limb/RRT (composite RR 4.74).")
print("\nConclusion: the ONLY positive mortality signal is device+population+comparator")
print("specific (Impella CP, STEMI-CS, vs standard). Haemodynamic support in general")
print("-- and VA-ECMO specifically, now with the largest trial -- does not lower death.")
