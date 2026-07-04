#!/usr/bin/env python
"""
Deterministic worked-example verification for the v2 advanced version of the Synthesis
paper "Cochrane in the Modern RE Era: REML, HKSJ, Prediction Intervals" (View/cochrane-modern-re).

Demonstrates the modern random-effects toolkit on a VERIFIED clinical dataset -- the four
pivotal SGLT2-inhibitor heart-failure trials (same PubMed-verified HRs used across the
Synthesis SGLT2-HF v2 papers 88/94/102): DAPA-HF 0.74(0.65-0.85), EMPEROR-Reduced
0.75(0.65-0.86), EMPEROR-Preserved 0.79(0.69-0.90), DELIVER 0.82(0.73-0.92).

Shows why, at small k: (1) DerSimonian-Laird under-covers vs REML/Paule-Mandel;
(2) the HKSJ correction with the q>=1 floor matters; (3) the prediction interval, not
the CI, answers "what will the next trial show". Deterministic; numpy + scipy.
"""
import math
import numpy as np
from scipy import optimize
from scipy.stats import t as tdist, norm

Z = 1.959963985
TRIALS = [("DAPA-HF",0.74,0.65,0.85),("EMPEROR-Reduced",0.75,0.65,0.86),
          ("EMPEROR-Preserved",0.79,0.69,0.90),("DELIVER",0.82,0.73,0.92)]

def yv(hr,lo,hi):
    y=math.log(hr); se=(math.log(hi)-math.log(lo))/(2*Z); return y, se*se

ys=np.array([yv(h,l,u)[0] for _,h,l,u in TRIALS])
vs=np.array([yv(h,l,u)[1] for _,h,l,u in TRIALS])
k=len(ys)

def dl_tau2(y,v):
    w=1/v; mu=np.sum(w*y)/np.sum(w); Q=np.sum(w*(y-mu)**2)
    c=np.sum(w)-np.sum(w**2)/np.sum(w); return max(0.0,(Q-(k-1))/c), Q
def reml_tau2(y,v):
    def nll(lt2):
        t2=math.exp(lt2); w=1/(v+t2); mu=np.sum(w*y)/np.sum(w)
        return -(-0.5*np.sum(np.log(v+t2))-0.5*math.log(np.sum(w))-0.5*np.sum(w*(y-mu)**2))
    return math.exp(optimize.minimize_scalar(nll,bounds=(-20,5),method="bounded").x)
def pm_tau2(y,v):
    def f(t2):
        w=1/(v+t2); mu=np.sum(w*y)/np.sum(w); return np.sum(w*(y-mu)**2)-(k-1)
    if f(0)<=0: return 0.0
    hi=10.0
    while f(hi)>0 and hi<1e6: hi*=2
    return optimize.brentq(f,0,hi)

tDL,Q = dl_tau2(ys,vs); tRE=reml_tau2(ys,vs); tPM=pm_tau2(ys,vs)
I2=max(0.0,(Q-(k-1))/Q)*100

def pooled(tau2,hksj):
    w=1/(vs+tau2); mu=np.sum(w*ys)/np.sum(w); var=1/np.sum(w)
    if hksj:
        q=max(1.0,np.sum(w*(ys-mu)**2)/(k-1)); var=q*var
        tc=tdist.ppf(0.975,k-1); lo,hi=mu-tc*math.sqrt(var),mu+tc*math.sqrt(var)
    else:
        lo,hi=mu-Z*math.sqrt(var),mu+Z*math.sqrt(var)
    return math.exp(mu),math.exp(lo),math.exp(hi)

print("Modern random-effects toolkit — worked example on verified SGLT2-HF data")
print(f"\nCochran Q={Q:.3f} (df {k-1})  I^2={I2:.1f}%")
print(f"tau^2 estimators:  DL={tDL:.5f}   REML={tRE:.5f}   Paule-Mandel={tPM:.5f}")
print("  (all ~0 here; DL's downward bias is masked when true tau^2 is genuinely ~0,")
print("   but DL would under-estimate under real heterogeneity at k=4 -> use REML/PM.)")

for label,tau2,hksj in [("DL + normal z-CI (old Cochrane default)",tDL,False),
                        ("REML + normal z-CI",tRE,False),
                        ("REML + HKSJ t_{k-1} (modern default)",tRE,True)]:
    hr,lo,hi=pooled(tau2,hksj)
    print(f"\n{label}:")
    print(f"  pooled HR={hr:.3f}  95% CI {lo:.3f}-{hi:.3f}  (width {hi-lo:.3f})")

# prediction interval (REML, t_{k-1})
w=1/(vs+tRE); mu=np.sum(w*ys)/np.sum(w); var=1/np.sum(w)
tc=tdist.ppf(0.975,k-1)
pi=(math.exp(mu-tc*math.sqrt(tRE+var)), math.exp(mu+tc*math.sqrt(tRE+var)))
print(f"\n95% PREDICTION INTERVAL (REML, t_{{k-1}}): {pi[0]:.3f}-{pi[1]:.3f}")
print("  -> excludes 1: a future same-design trial is expected to show benefit.")
print("\nLesson: at k<10, REML/PM (not DL) + HKSJ t_{k-1} with the q>=1 floor + a")
print("prediction interval are the modern minimum. Here they agree (I^2=0) but the")
print("HKSJ interval is appropriately WIDER than the naive z-interval.")
