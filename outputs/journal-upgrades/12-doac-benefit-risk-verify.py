#!/usr/bin/env python
"""
Deterministic bivariate benefit-risk meta-analysis of the four pivotal DOAC-vs-
warfarin atrial-fibrillation trials, for the v2 advanced version of Synthesis
View/12 ("Rigorous Bivariate Synthesis of Benefit-Risk Profiles for DOACs in AF").

High-dose DOAC vs warfarin, verified against the primary publications:
  Efficacy — stroke or systemic embolism (ITT / as-randomised RR or HR):
    RE-LY  (dabigatran 150)  0.66 (0.53-0.82)  Connolly 2009  PMID 19717844
    ROCKET-AF (rivaroxaban)  0.88 (0.74-1.03)  Patel 2011     PMID 21830957 (ITT)
    ARISTOTLE (apixaban)     0.79 (0.66-0.95)  Granger 2011   PMID 21870978
    ENGAGE-AF (edoxaban HD)  0.87 (0.73-1.04)  Giugliano 2013 PMID 24251359 (ITT)
  Safety — major bleeding (HR vs warfarin):
    RE-LY  (dabigatran 150)  0.93 (0.81-1.07)
    ROCKET-AF                1.04 (0.90-1.20)
    ARISTOTLE                0.69 (0.60-0.80)
    ENGAGE-AF (HD)           0.80 (0.71-0.91)

Benchmark (Ruff et al., Lancet 2014, PMID 24315724): pooled stroke/SE RR 0.81
(0.73-0.91); major bleeding "similar" to warfarin (published 0.86, 0.73-1.00);
ICH 0.48; all-cause mortality 0.90.

Methods: pool log-effects by REML random effects with Hartung-Knapp CI (t_{k-1},
q>=1 floor); report Q, I², prediction interval. Deterministic; numpy + scipy.
"""
import math, numpy as np
from scipy import optimize
from scipy.stats import t as tdist, chi2

def yv(e, lo, hi):
    y = math.log(e); se = (math.log(hi) - math.log(lo)) / (2 * 1.959963985)
    return y, se * se

def reml_tau2(y, v):
    y = np.asarray(y); v = np.asarray(v)
    def nll(lt):
        t2 = math.exp(lt); w = 1.0 / (v + t2); mu = np.sum(w*y)/np.sum(w)
        return -(-0.5*np.sum(np.log(v+t2)) - 0.5*math.log(np.sum(w)) - 0.5*np.sum(w*(y-mu)**2))
    return math.exp(optimize.minimize_scalar(nll, bounds=(-20,5), method="bounded").x)

def pooled(name, rows):
    ys, vs = zip(*[yv(*r) for r in rows]); ys=list(ys); vs=list(vs); k=len(ys)
    t2 = reml_tau2(ys, vs)
    w = [1.0/(v+t2) for v in vs]; mu = sum(wi*yi for wi,yi in zip(w,ys))/sum(w)
    var = 1.0/sum(w)
    q = sum(wi*(yi-mu)**2 for wi,yi in zip(w,ys))/(k-1); q=max(1.0,q)
    tcr = tdist.ppf(0.975, k-1); hk = math.sqrt(q*var)
    wf=[1.0/v for v in vs]; muf=sum(wi*yi for wi,yi in zip(wf,ys))/sum(wf)
    Q=sum(wi*(yi-muf)**2 for wi,yi in zip(wf,ys)); I2=max(0.0,(Q-(k-1))/Q)*100 if Q>0 else 0
    pil=mu-tdist.ppf(0.975,k-1)*math.sqrt(t2+var); pih=mu+tdist.ppf(0.975,k-1)*math.sqrt(t2+var)
    print(f"\n{name} (k={k}): pooled={math.exp(mu):.3f} "
          f"(HKSJ 95% CI {math.exp(mu-tcr*hk):.3f}-{math.exp(mu+tcr*hk):.3f}) "
          f"| tau2={t2:.4f} I2={I2:.0f}% Q={Q:.2f} | PI {math.exp(pil):.3f}-{math.exp(pih):.3f}")
    zl,zh = mu-1.96*math.sqrt(var), mu+1.96*math.sqrt(var)
    print(f"    normal-CI (contrast): {math.exp(zl):.3f}-{math.exp(zh):.3f}")

STROKE = [(0.66,0.53,0.82),(0.88,0.74,1.03),(0.79,0.66,0.95),(0.87,0.73,1.04)]
BLEED  = [(0.93,0.81,1.07),(1.04,0.90,1.20),(0.69,0.60,0.80),(0.80,0.71,0.91)]

print("DOAC vs warfarin — bivariate benefit-risk meta-analysis (deterministic)")
pooled("EFFICACY: stroke/systemic embolism", STROKE)
pooled("SAFETY: major bleeding", BLEED)
print("\nBenchmark (Ruff 2014): stroke/SE 0.81 (0.73-0.91); major bleeding 0.86 (0.73-1.00).")

# --- illustrative absolute benefit-risk per 1000 patient-years ---
# baseline (warfarin) annual rates from the trials (approx, stated as assumptions)
base = {"stroke/SE": 0.016, "major bleeding": 0.033, "ICH": 0.007, "mortality": 0.041}
rr   = {"stroke/SE": 0.81, "major bleeding": 0.86, "ICH": 0.48, "mortality": 0.90}
print("\nIllustrative absolute effects per 1000 patient-years (baseline = warfarin trial rates):")
for k in base:
    ard = base[k]*(1-rr[k])*1000
    tag = "fewer" if ard>=0 else "more"
    nnt = 1000/abs(ard) if ard else float('inf')
    print(f"  {k:<15} baseline {base[k]*100:.1f}%/yr, RR {rr[k]:.2f} -> {abs(ard):.1f} {tag}/1000py (NNT/NNH {nnt:.0f})")
