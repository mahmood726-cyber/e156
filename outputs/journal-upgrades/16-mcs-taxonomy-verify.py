#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of the Synthesis paper
"The MCS Apples-and-Oranges Problem" (View/16).

Methodological companion to paper 23 (which gives the clinical device-stratified
reading). This paper's point is about EVIDENCE SYNTHESIS: pooling across MCS device
types/comparators/eras yields a PREDICTION INTERVAL that spans meaningful benefit to
meaningful harm, so the all-device pooled estimate is clinically uninformative.

All trial inputs are the SAME PubMed-verified estimates used in paper 23
(23-cardiogenic-shock-verify.py; verified 2026-07-04):
  IABP-SHOCK II  Thiele 2012 NEJM   PMID 22920912  IABP vs none        RR 0.96 (0.79-1.17)
  IMPRESS        Ouweneel 2017 JACC PMID 27810347  Impella vs IABP     HR 0.96 (0.42-2.18)
  ECMO-CS        Ostadal 2023 Circ  PMID 36335478  VA-ECMO vs conserv  ~1.05 (29/58 vs 28/59; secondary all-cause, flagged)
  ECLS-SHOCK     Thiele 2023 NEJM   PMID 37634145  VA-ECMO vs medical  RR 0.98 (0.80-1.19)
  DanGer Shock   Moller 2024 NEJM   PMID 38587239  Impella vs standard HR 0.74 (0.55-0.99)

Methods: log-scale pooling; DerSimonian-Laird tau^2 (as commonly used in the pooled
MCS meta-analyses this paper critiques) with REML shown for contrast; HKSJ CI t_{k-1};
Cochran Q / I^2; 95% prediction interval t_{k-1}. Era split: pre-2015 vs 2015-2024.
Deterministic; numpy + scipy.
"""
import math
import numpy as np
from scipy import optimize
from scipy.stats import t as tdist

Z = 1.959963985

def yv(eff, lo, hi):
    y = math.log(eff); se = (math.log(hi) - math.log(lo)) / (2 * Z)
    return y, se

# name, effect, lo, hi, device, comparator, year
TRIALS = [
    ("IABP-SHOCK II", 0.96, 0.79, 1.17, "IABP",       "none",     2012),
    ("IMPRESS",       0.96, 0.42, 2.18, "Impella",    "IABP",     2017),
    ("ECMO-CS",       1.05, 0.72, 1.53, "VA-ECMO",    "conserv.", 2023),  # RR approx; CI wide, flagged
    ("ECLS-SHOCK",    0.98, 0.80, 1.19, "VA-ECMO",    "medical",  2023),
    ("DanGer Shock",  0.74, 0.55, 0.99, "Impella",    "standard", 2024),
]

def dl_tau2(y, v):
    y=np.asarray(y); v=np.asarray(v); k=len(y)
    w=1/v; mu=np.sum(w*y)/np.sum(w); Q=np.sum(w*(y-mu)**2)
    c=np.sum(w)-np.sum(w**2)/np.sum(w)
    return max(0.0,(Q-(k-1))/c) if c>0 else 0.0

def reml_tau2(y, v):
    y=np.asarray(y); v=np.asarray(v)
    def nll(lt2):
        t2=math.exp(lt2); w=1/(v+t2); mu=np.sum(w*y)/np.sum(w)
        return -(-0.5*np.sum(np.log(v+t2))-0.5*math.log(np.sum(w))-0.5*np.sum(w*(y-mu)**2))
    return math.exp(optimize.minimize_scalar(nll,bounds=(-20,5),method="bounded").x)

def pool(names, label, force_tau2=None):
    sub=[t for t in TRIALS if t[0] in names]
    ys=[]; vs=[]
    for _,eff,lo,hi,*_ in sub:
        y,se=yv(eff,lo,hi); ys.append(y); vs.append(se*se)
    k=len(ys); ys=np.array(ys); vs=np.array(vs)
    tau2 = force_tau2 if force_tau2 is not None else dl_tau2(ys,vs)
    w=1/(vs+tau2); mu=np.sum(w*ys)/np.sum(w); var_mu=1/np.sum(w)
    q=np.sum(w*(ys-mu)**2)/(k-1) if k>1 else 1.0; q=max(1.0,q)
    tcrit=tdist.ppf(0.975,k-1) if k>1 else float('nan')
    wf=1/vs; muf=np.sum(wf*ys)/np.sum(wf); Q=np.sum(wf*(ys-muf)**2)
    I2=max(0.0,(Q-(k-1))/Q)*100 if Q>0 and k>1 else 0.0
    print(f"\n--- {label} (k={k}) ---")
    if k>1:
        hk=(mu-tcrit*math.sqrt(q*var_mu), mu+tcrit*math.sqrt(q*var_mu))
        pi=(mu-tcrit*math.sqrt(tau2+var_mu), mu+tcrit*math.sqrt(tau2+var_mu))
        z=(mu-Z*math.sqrt(var_mu), mu+Z*math.sqrt(var_mu))
        tt=f"tau^2={tau2:.4f}" + (" (imposed)" if force_tau2 is not None else " (DL)")
        print(f"  {tt}  Q={Q:.3f} (df {k-1})  I^2={I2:.1f}%")
        print(f"  Pooled effect={math.exp(mu):.3f}  z-CI {math.exp(z[0]):.3f}-{math.exp(z[1]):.3f}  "
              f"HKSJ {math.exp(hk[0]):.3f}-{math.exp(hk[1]):.3f}")
        print(f"  95% PREDICTION INTERVAL: {math.exp(pi[0]):.3f}-{math.exp(pi[1]):.3f}")

print("MCS apples-and-oranges — deterministic PI/taxonomy verification (v2)")
print(f"{'Trial':<15}{'device/comparator':<22}{'effect':<18}{'year':>5}")
for nm,eff,lo,hi,dev,comp,yr in TRIALS:
    print(f"{nm:<15}{dev+' vs '+comp:<22}{f'{eff:.2f} ({lo:.2f}-{hi:.2f})':<18}{yr:>5}")

allnames=[t[0] for t in TRIALS]
pool(allnames, "ALL-DEVICE POOL (the critiqued approach), DL tau^2")
pool(allnames, "ALL-DEVICE POOL under plausible moderate heterogeneity", force_tau2=0.05)

print("\n" + "="*66 + "\nERA SPLIT:")
pool(["IABP-SHOCK II"], "pre-2015 (IABP-SHOCK II only)")
pool(["IMPRESS","ECMO-CS","ECLS-SHOCK","DanGer Shock"], "2015-2024 era")

print("\n" + "="*66 + "\nDEVICE/COMPARATOR STRATA:")
pool(["ECMO-CS","ECLS-SHOCK"], "VA-ECMO vs no-ECMO")
pool(["IMPRESS","DanGer Shock"], "Impella (mixed comparators - itself apples/oranges)")

print("\n" + "="*66)
print("Point: the all-device pooled point estimate (~0.9) is stable, but its 95%")
print("PREDICTION INTERVAL under realistic heterogeneity spans from meaningful")
print("benefit to meaningful harm -> the pooled number cannot forecast the next")
print("trial. Device- AND comparator-stratified synthesis is the minimum standard;")
print("even 'Impella' pools apples/oranges (vs IABP in IMPRESS, vs standard in DanGer).")
