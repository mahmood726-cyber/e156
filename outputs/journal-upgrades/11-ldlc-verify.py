#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of the Synthesis paper
"Residual Cardiovascular Risk After LDL-C Lowering" (View/11).

Verified inputs (PubMed metadata matched 2026-07-04):
  CTT 2010 (Baigent et al.) Lancet 376:1670-81  PMID 21067804
     RR 0.78 (0.76-0.80) in major vascular events per 1.0 mmol/L LDL-C reduction
     (~22% RRR/mmol/L); all-cause mortality RR 0.90/mmol/L; NO threshold observed.
  FOURIER (Sabatine 2017) NEJM 376:1713-22  PMID 28304224  NCT01764633
     evolocumab vs placebo on statin; LDL 92 -> 30 mg/dL (-59%, -62 mg/dL);
     primary composite 1344/13784 (9.8%) vs 1563/13780 (11.3%),
     HR 0.85 (0.79-0.92); key secondary (CVD/MI/stroke) HR 0.80 (0.73-0.88);
     median follow-up 2.2 y.
  ODYSSEY OUTCOMES (Schwartz 2018) NEJM 379:2097-2107  PMID 30403574
     alirocumab after ACS; HR 0.85 (0.78-0.93). (v1 cited WRONG PMID 29957120,
     a nanomedicine cancer-drug paper.)

Analyses: (1) CTT log-linear prediction for FOURIER's LDL reduction; (2) fraction of
the CTT steady-state effect realized in FOURIER's 2.2-y window (delayed-benefit /
time-course reconciliation); (3) FOURIER NNT; (4) LDL-C measurement-variability
misclassification at the 70 mg/dL threshold. Deterministic; scipy.stats.norm.
"""
import math
from scipy.stats import norm

MMOL_PER_MGDL = 1 / 38.67  # 1 mmol/L = 38.67 mg/dL for LDL-C

# --- 1. CTT log-linear prediction for FOURIER's LDL reduction ---
ctt_rr_per_mmol = 0.78
fourier_ldl_drop_mgdl = 92 - 30            # 62 mg/dL
fourier_ldl_drop_mmol = fourier_ldl_drop_mgdl * MMOL_PER_MGDL
ctt_pred_rr = ctt_rr_per_mmol ** fourier_ldl_drop_mmol
print("LDL-C residual-risk verification (deterministic, v2)")
print(f"\n1) CTT log-linear prediction:")
print(f"   FOURIER LDL reduction = {fourier_ldl_drop_mgdl} mg/dL = {fourier_ldl_drop_mmol:.2f} mmol/L")
print(f"   CTT steady-state predicted RR = 0.78^{fourier_ldl_drop_mmol:.2f} = {ctt_pred_rr:.3f} "
      f"({(1-ctt_pred_rr)*100:.1f}% RRR)")

# --- 2. Fraction of CTT effect realized in 2.2 years ---
fourier_hr = 0.85
frac = (1 - fourier_hr) / (1 - ctt_pred_rr)
print(f"\n2) Time-course reconciliation:")
print(f"   FOURIER OBSERVED 2.2-y HR = {fourier_hr} ({(1-fourier_hr)*100:.0f}% RRR)")
print(f"   fraction of CTT steady-state effect realized in 2.2 y = "
      f"{(1-fourier_hr)*100:.0f}/{(1-ctt_pred_rr)*100:.0f} = {frac*100:.0f}%")
print("   -> PCSK9i 'underperformance' vs CTT is a delayed-benefit artifact of a")
print("      short trial, NOT a threshold or mechanism failure (CTT shows no floor).")

# --- 3. FOURIER NNT ---
p_pbo, p_evo = 0.113, 0.098
arr = p_pbo - p_evo
print(f"\n3) FOURIER absolute benefit:")
print(f"   primary event 11.3% vs 9.8%  ARR = {arr*100:.1f} pp over 2.2 y  "
      f"NNT = {1/arr:.0f}")

# --- 4. LDL-C measurement misclassification at 70 mg/dL ---
print(f"\n4) LDL measurement variability at the 70 mg/dL threshold:")
for cv in (0.08, 0.10, 0.12):
    sd = 70 * cv
    band = 1.959963985 * sd
    # patient whose TRUE LDL sits exactly at 70: P(measured on 'wrong' side) = 50%,
    # but for true LDL 5 mg/dL below (65) the P(measured >=70 -> mis-'above-target'):
    p_cross_at65 = 1 - norm.cdf((70 - 65) / sd)
    p_cross_at75 = norm.cdf((70 - 75) / sd)
    print(f"   CV={cv*100:.0f}% -> SD={sd:.1f} mg/dL, 95% band +-{band:.0f} mg/dL; "
          f"true 65 mis>=70: {p_cross_at65*100:.0f}%; true 75 mis<70: {p_cross_at75*100:.0f}%")
print("   -> A single fasting LDL near 70 mg/dL misclassifies a large minority of")
print("      borderline patients; confirm with a repeat measurement before intensifying.")

print("\n" + "="*66)
print("Bottom line: LDL-lowering benefit is log-linear with NO threshold (CTT);")
print("PCSK9i add-on delivers HR ~0.85 in ~2 y (NNT ~67), which is ~45% of the")
print("CTT-predicted steady-state effect for its 1.6 mmol/L drop -- the rest accrues")
print("with longer exposure. Decision noise at the 70 mg/dL target is measurement-,")
print("not mechanism-, driven.")
