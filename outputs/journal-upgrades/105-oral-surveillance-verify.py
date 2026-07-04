#!/usr/bin/env python
"""
Deterministic benefit-risk verification for the v2 advanced version of the
Synthesis paper "JAK Inhibitors in RA ... ORAL Surveillance" (View/105).

Verified primary source (PubMed metadata matched 2026-07-04):
  Ytterberg SR et al. "Cardiovascular and Cancer Risk with Tofacitinib in
  Rheumatoid Arthritis." N Engl J Med 2022;386(4):316-326. PMID 35081280.
  doi 10.1056/NEJMoa2109927. NCT02092467 (ORAL Surveillance).

Design: randomized, open-label, non-inferiority POST-authorization safety trial.
RA patients >=50 y with >=1 additional CV risk factor, on methotrexate.
Arms (1:1:1): tofacitinib 5 mg BID (n=1455), tofacitinib 10 mg BID (n=1456),
TNF inhibitor (n=1451). Coprimary endpoints: adjudicated MACE and cancers
(excluding non-melanoma skin cancer). Median follow-up 4.0 y.
Non-inferiority shown only if the UPPER bound of the two-sided 95% CI for the HR
(combined tofacitinib vs TNFi) is < 1.8.

VERIFIED primary results (combined tofacitinib doses vs TNFi):
  MACE   : tofa 98/2911 (3.4%)  vs TNFi 37/1451 (2.5%)   HR 1.33 (0.91-1.94)
  cancer : tofa 122/2911 (4.2%) vs TNFi 42/1451 (2.9%)   HR 1.48 (1.04-2.09)

NOTE: v1 draft asserted MACE HR 1.33 (1.00-1.76) and VTE HR 1.96 (1.30-2.97) and
dose-specific HRs (1.43 / 2.55) that do NOT match the NEJM primary abstract
(MACE CI is 0.91-1.94). Those figures are NOT reproduced here; VTE and dose-
stratified estimates require the full text / secondary analyses and are flagged,
not asserted. This script uses ONLY the verified coprimary results.
"""
import math

NI_MARGIN = 1.8
N_TOFA = 1455 + 1456   # 2911 combined
N_TNFI = 1451

def analyse(name, e_tofa, e_tnfi, hr, lo, hi):
    p_t = e_tofa / N_TOFA
    p_c = e_tnfi / N_TNFI
    rd = p_t - p_c
    rr = p_t / p_c
    nnh = 1.0 / rd if rd > 0 else float('inf')
    ni_met = hi < NI_MARGIN
    sig_harm = lo > 1.0
    print(f"\n{name}")
    print(f"  tofacitinib {e_tofa}/{N_TOFA} = {p_t*100:.2f}%   TNFi {e_tnfi}/{N_TNFI} = {p_c*100:.2f}%")
    print(f"  crude RR (reconstruction) = {rr:.3f}  vs published HR {hr:.2f} ({lo:.2f}-{hi:.2f})"
          f"  -> {'consistent' if abs(rr-hr)<0.1 else 'CHECK'}")
    print(f"  absolute risk difference = {rd*100:+.2f} pp over median 4.0 y")
    print(f"  number-needed-to-HARM (NNH) = {nnh:.0f}")
    print(f"  non-inferiority (upper CI {hi:.2f} < {NI_MARGIN}?): {'MET' if ni_met else 'NOT MET'}")
    print(f"  significantly increased (lower CI {lo:.2f} > 1.0?): {'YES' if sig_harm else 'no'}")

print("ORAL Surveillance — deterministic benefit-risk verification (v2)")
print(f"Combined tofacitinib N={N_TOFA}  TNFi N={N_TNFI}  (total {N_TOFA+N_TNFI})")
analyse("MACE (adjudicated)",   98, 37, 1.33, 0.91, 1.94)
analyse("Cancer excl. NMSC",   122, 42, 1.48, 1.04, 2.09)

print("\n" + "="*66)
print("Interpretation (verified):")
print("  - Neither coprimary endpoint met non-inferiority (both upper CIs > 1.8).")
print("  - Cancer risk was significantly INCREASED (HR 1.48, lower CI 1.04 > 1).")
print("  - MACE point estimate elevated (HR 1.33) but CI includes 1 (0.91-1.94):")
print("    directionally consistent with harm, not individually 'significant', yet")
print("    non-inferiority is REFUTED -- the correct read for a NI trial.")
print("  - NNH ~122 (MACE) and ~77 (cancer) over 4 years contextualise absolute harm.")
print("  - Crude RR reconstructions (1.32, 1.45) closely match the adjudicated Cox")
print("    HRs (1.33, 1.48), validating the published estimates.")
print("  - VTE and 5mg-vs-10mg dose-stratified HRs are NOT in the primary abstract;")
print("    they require full-text/secondary-analysis verification and are flagged.")
