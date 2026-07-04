#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of the Synthesis paper
"Pre-Exposure Prophylaxis Initiation and Adherence ... in Sub-Saharan Africa" (View/96).

Verified landmark PrEP trials (PubMed metadata + abstract matched 2026-07-04):
  iPrEx     Grant 2010 NEJM 363:2587-99  PMID 21091279  oral TDF/FTC vs PLACEBO, MSM
     36 vs 64 incident infections -> 44% reduction in HIV incidence.
  HPTN 083  Landovitz 2021 NEJM 385:595-608  PMID 34379922  CAB-LA vs oral TDF-FTC,
     cisgender men + transgender women: 13 (0.41/100 PY) vs 39 (1.22/100 PY).
  HPTN 084  Delany-Moretlwe 2022 Lancet 399:1779-89  PMID 35378077  CAB-LA vs oral
     TDF-FTC, WOMEN (7 SSA countries, N=3224): 4 (0.2/100 PY) vs 36 (1.85/100 PY),
     HR 0.12 (0.05-0.31); only 42.1% of TDF-FTC samples had tenofovir consistent
     with daily use (adherence marker).
     (v1 cited a WRONG HPTN 084 PMID 35298832 = a Covid ICU-cost model paper.)

This script recomputes incidence-rate ratios (CAB-LA vs oral) from the published
person-time incidence rates, contrasts the CAB-LA advantage in men vs women, and links
it to the adherence gap. Deterministic; numpy.
"""
import math

def irr(rate_cab, rate_oral, label, hr_pub):
    r = rate_cab / rate_oral
    print(f"\n{label}")
    print(f"  CAB-LA {rate_cab}/100 PY  vs oral TDF-FTC {rate_oral}/100 PY")
    print(f"  incidence-rate ratio = {r:.3f}  ({(1-r)*100:.0f}% fewer infections vs oral PrEP)")
    print(f"  published hazard ratio ~ {hr_pub}  -> {'consistent' if abs(r-hr_pub)<0.06 else 'CHECK'}")
    return r

print("PrEP formulation efficacy — deterministic verification (v2)")
print("\n1) Oral TDF/FTC vs PLACEBO (iPrEx, MSM): 36 vs 64 infections.")
print("   Published efficacy = 44% reduction in HIV incidence (intention-to-treat).")

print("\n2) Long-acting CAB-LA vs oral TDF/FTC (the modern, active-controlled question):")
r_men   = irr(0.41, 1.22, "HPTN 083 (men + transgender women)", 0.34)
r_women = irr(0.20, 1.85, "HPTN 084 (women)", 0.12)

print("\n" + "="*66)
print("Sex gap in the CAB-LA advantage:")
print(f"  men/TGW  IRR {r_men:.3f}  (~{(1-r_men)*100:.0f}% fewer than oral)")
print(f"  women    IRR {r_women:.3f}  (~{(1-r_women)*100:.0f}% fewer than oral)")
print(f"  women/men IRR ratio = {r_women/r_men:.2f}  -> CAB-LA's edge over oral PrEP is")
print("  LARGER in women, precisely where oral adherence is hardest.")
print("\nAdherence mechanism (HPTN 084): only 42.1% of oral-arm plasma samples had")
print("tenofovir consistent with daily use, vs 93% CAB injection coverage. The oral-")
print("PrEP 'failures' in women are ADHERENCE failures, not drug failures; the long-")
print("acting formulation converts efficacy into effectiveness by removing daily dosing.")
print("\nImplication: efficacy (does the drug work if taken) is settled for all")
print("formulations; EFFECTIVENESS (does it work as delivered) is an adherence problem,")
print("and CAB-LA's benefit is greatest in the populations with the lowest oral adherence.")
