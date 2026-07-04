#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of the Synthesis paper
"The EF50 Decision Threshold: Measurement Uncertainty in HFmrEF" (View/9).

Two verified anchors (PubMed metadata matched 2026-07-04):
  Bozkurt 2021 Eur J Heart Fail 23:352-380 (Universal Definition of HF) PMID 33605000
     HFrEF <=40%, HFmrEF 41-49%, HFpEF >=50%  (the 9-point band)
  Thavendiranathan 2013 JACC 61:77-84 PMID 23199515
     temporal variability of EF: 2D methods >0.10 (i.e. >10 EF points);
     noncontrast 3D echo ~0.06.  -> justifies a measurement SD of ~5 EF units
     (2D) as a *conservative* value; 8 units is realistic for routine 2D.

Therapeutic-arbitrariness link uses ALREADY-VERIFIED SGLT2i EF-spectrum trials
(see 88-sglt2-hf-meta-verify.py): EMPEROR-Preserved HR 0.79 (0.69-0.90) PMID 34449189
and DELIVER HR 0.82 (0.73-0.92) PMID 36027570, benefit continuous across EF with no
significant EF-interaction (paper 94: p_interaction=0.23). => an HFmrEF<->HFpEF
misclassification does NOT change SGLT2i eligibility, but an HFmrEF<->HFrEF (<=40)
misclassification changes ARNI/MRA/beta-blocker/ICD Class-I eligibility.

Simulation: Gaussian measurement model. For true EF in the HFmrEF band and a range
of measurement SDs, compute P(measured <=40 -> HFrEF) and P(measured >=50 -> HFpEF)
and total misclassification. SEM/MDC from ICC. Deterministic; scipy.stats.norm.
"""
import math
from scipy.stats import norm

def misclass(true_ef, sd):
    p_low = norm.cdf((40.0 - true_ef) / sd)      # measured <=40 -> HFrEF
    p_high = 1.0 - norm.cdf((50.0 - true_ef) / sd)  # measured >=50 -> HFpEF
    return p_low, p_high, p_low + p_high

print("EF50 threshold — misclassification simulation (deterministic, v2)")
print("HFmrEF band = 41-49% (Universal Definition, PMID 33605000)")
print("\nP(misclassified) for true EF across the band, by measurement SD:")
print(f"{'true EF':>8}", end="")
for sd in (3, 5, 8):
    print(f"   SD={sd}: P(HFrEF)/P(HFpEF)/total", end="")
print()
for ef in (41, 43, 45, 47, 49):
    print(f"{ef:>7}%", end="")
    for sd in (3, 5, 8):
        lo, hi, tot = misclass(ef, sd)
        print(f"   {lo*100:4.1f}% / {hi*100:4.1f}% / {tot*100:4.1f}%", end="")
    print()

print("\nCentral case: true EF=45, SD=5  ->  P(HFrEF)=Phi(-1)=%.1f%%, "
      "P(HFpEF)=1-Phi(1)=%.1f%%, total=%.1f%%"
      % tuple(x*100 for x in misclass(45, 5)))

print("\nSEM and MDC as a function of ICC (SD_between = 10 EF units, typical):")
SD_BETWEEN = 10.0
print(f"{'ICC':>6}{'SEM (EF units)':>16}{'MDC (EF units)':>16}")
for icc in (0.70, 0.82, 0.90, 0.95):
    sem = SD_BETWEEN * math.sqrt(1 - icc)
    mdc = 1.959963985 * math.sqrt(2) * sem
    print(f"{icc:>6.2f}{sem:>16.2f}{mdc:>16.2f}")
print("  -> Even at ICC 0.90, MDC ~8.8 EF units ~ the entire 9-point HFmrEF band:")
print("     a within-patient EF change smaller than the band width cannot be")
print("     distinguished from measurement noise.")

print("\nTherapeutic consequence (verified SGLT2i EF-spectrum data):")
print("  EMPEROR-Preserved HR 0.79 (0.69-0.90); DELIVER HR 0.82 (0.73-0.92);")
print("  benefit continuous across EF, EF-interaction NS (paper 94 p=0.23).")
print("  => HFmrEF<->HFpEF misclassification: SAME SGLT2i eligibility (both benefit).")
print("     HFmrEF<->HFrEF (<=40) misclassification: CHANGES ARNI/MRA/beta-blocker")
print("     Class-I status and ICD/CRT (<=35%) eligibility -> the consequential edge.")
