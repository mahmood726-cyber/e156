#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of View/30
(Intravenous calcium for calcium-channel-blocker toxicity).

There are NO randomised trials, so nothing here is a pooled treatment effect.
This script verifies only the reproducible, source-anchored quantities used in
the paper, and computes honest descriptive proportions (with Wilson CIs) from
the two structured data sources — explicitly NOT as efficacy estimates.

  (1) Elemental-calcium stoichiometry for 10% CaCl2 vs 10% Ca-gluconate
      (the 272 mg vs 90 mg / 10 mL and the ~3:1 ratio) from molecular weights.
  (2) Descriptive proportions from Cole 2018 (Am J Emerg Med 36:1817; PMID
      29452919) and Isbister 2024/25 (Br J Clin Pharmacol 91:740; PMID 39305202)
      with Wilson 95% CIs -- clearly labelled as cohort descriptors, confounded
      by concurrent multimodal therapy, NOT calcium treatment effects.
  (3) Case-fatality context from the verifiable Olson 2005 out-of-hospital
      guideline (Clin Toxicol 43:797; PMID 16440509): 57 deaths / 9,650 CCB
      ingestions reported to US poison centres in 2003.

Requires only the Python standard library + scipy for the Wilson interval
(falls back to a closed-form Wilson if scipy is absent). Read-only.
"""
import math

Z = 1.959963985  # qnorm(0.975)

def wilson(k, n):
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    d = 1 + Z*Z/n
    centre = (p + Z*Z/(2*n)) / d
    half = (Z*math.sqrt(p*(1-p)/n + Z*Z/(4*n*n))) / d
    return p, centre - half, centre + half

print("=== (1) Elemental-calcium stoichiometry (10% w/v = 1000 mg salt / 10 mL) ===")
Ca = 40.078
Cl = 35.45
H2O = 18.015
# Calcium chloride dihydrate CaCl2.2H2O
mw_cacl2 = Ca + 2*Cl + 2*H2O
ca_cacl2 = 1000.0 * Ca / mw_cacl2
# Calcium gluconate monohydrate C12H22CaO14.H2O
C, H, O = 12.011, 1.008, 15.999
mw_glu = 12*C + 22*H + Ca + 14*O + H2O   # monohydrate
ca_glu = 1000.0 * Ca / mw_glu
print(f"  CaCl2.2H2O  MW={mw_cacl2:.2f}  -> elemental Ca in 10 mL of 10% = {ca_cacl2:.1f} mg  (paper: 272)")
print(f"  Ca-gluconate.H2O MW={mw_glu:.2f} -> elemental Ca in 10 mL of 10% = {ca_glu:.1f} mg  (paper:  90)")
print(f"  Ratio CaCl2:CaGlu (equal volume) = {ca_cacl2/ca_glu:.2f} : 1   (paper: 3:1)")
print(f"  Equi-elemental: 1 g CaCl2 ({ca_cacl2:.0f} mg Ca) ~= "
      f"{ca_cacl2/ca_glu*1:.2f} g CaGlu (~{3*ca_glu:.0f} mg Ca in 3 g)")

print("\n=== (2) Descriptive cohort proportions (NOT calcium efficacy) ===")
# Cole 2018: 199 patients received high-dose insulin for BB/CCB poisoning.
#   66 CCB-only, 88 BB-only, 45 both. Whole-cohort: 41 cardiac arrests, 31 died.
for label, k, n in [
    ("Cole 2018 cardiac arrest (whole 199-pt HDI cohort)", 41, 199),
    ("Cole 2018 in-hospital death (whole 199-pt HDI cohort)", 31, 199),
    ("Cole 2018 hypoglycaemia (whole cohort)", int(round(0.31*199)), 199),
]:
    p, lo, hi = wilson(k, n)
    print(f"  {label:52} {k}/{n} = {p*100:5.1f}% (95% CI {lo*100:.1f}-{hi*100:.1f}%)")
print("  NOTE: 66 of the 199 were CCB-only; arrests/deaths are reported cohort-wide,")
print("        NOT isolable to the CCB subset or to calcium. v1 mis-stated '41 of 66'.")

# Isbister 2024/25: 236 CCB overdoses across two services, 2014-2023.
for label, k, n in [
    ("Isbister received IV calcium", 44, 236),
    ("Isbister received high-dose insulin", 21, 236),
    ("Isbister hypotension", 91, 236),
    ("Isbister died", 7, 236),
    ("Isbister amlodipine (commonest agent)", 147, 236),
]:
    p, lo, hi = wilson(k, n)
    print(f"  {label:52} {k}/{n} = {p*100:5.1f}% (95% CI {lo*100:.1f}-{hi*100:.1f}%)")

print("\n=== (3) Poison-centre case fatality (verifiable, Olson 2005 guideline) ===")
p, lo, hi = wilson(57, 9650)
print(f"  CCB ingestions 2003 (US PCCs): 57 deaths / 9,650 = {p*100:.2f}% "
      f"(95% CI {lo*100:.2f}-{hi*100:.2f}%)")
print("  (The v1 '2020: 45/6,132' AAPCC figure could NOT be verified from the "
      "NPDS annual report here -> flagged AS-CITED, not asserted.)")
