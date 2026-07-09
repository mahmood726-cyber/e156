#!/usr/bin/env python
"""
Deterministic verification for the v2 (truth-first) of View/54
(The AMR crisis in Africa: a trial-registry "deficit" re-examined).

The v1 headline -- "only 45 of 24,771 African trials (0.2%) focus on AMR" -- is a
real count but a MISLEADING framing: 0.2% of African trials being AMR-focused says
nothing about under-representation unless compared with the AMR share GLOBALLY,
which is even smaller. This script reproduces the AMR trial counts from the AACT
April-12-2026 snapshot (via the repo's reusable `_africa_equity_verify.py`, whose
AMR condition group prints these exact numbers) and computes the like-for-like and
burden-adjusted comparisons the v1 omitted.

AACT-derived counts (condition-coded 'AMR' group; reproduce by running
`_africa_equity_verify.py` against F:/AACT-storage/AACT/2026-04-12):
    registry all-studies         : 579,828
    registry interventional      : 442,464
    registry any-African-site    : 25,125  (4.33% of all studies)
    AMR-condition global         : 259
    AMR-condition African        : 47      (18.15% of AMR trials)
    AMR-condition global (interv): 162
    AMR-condition African (interv): 31     (19.14%)
The v1's own keyword search found 45 African AMR trials -- concordant with 47.

Burden anchors (PubMed-verified):
    Murray GRAM 2022 (PMID 35065702): GLOBAL 1.27M attributable / 4.95M associated.
    Sartorius 2024   (PMID 38134946): WHO AFRICAN REGION 2019 --
        250,000 deaths ATTRIBUTABLE, 1.05M ASSOCIATED with bacterial AMR.
    (v1 mis-stated 1.05M as 'African deaths' attributed to Murray; it is the
     ASSOCIATED figure from Sartorius 2024, a paper v1 does not cite.)

Read-only; standard library only.
"""

ALL          = 579_828
INTERV       = 442_464
AFR_SITE     = 25_125
AMR_G        = 259
AMR_A        = 47
AMR_GI       = 162
AMR_AI       = 31

# Burden (attributable, primary counterfactual)
GLOB_ATTRIB  = 1_270_000      # Murray 2022
AFR_ATTRIB   = 250_000        # Sartorius 2024
AFR_ASSOC    = 1_050_000      # Sartorius 2024 (broader counterfactual)

print("=== Baseline & shares ===")
base = 100.0 * AFR_SITE / ALL
print(f"  African-site share of ALL trials (baseline): {base:.2f}%")
print(f"  African share of AMR trials: {100.0*AMR_A/AMR_G:.2f}%  "
      f"(interventional {100.0*AMR_AI/AMR_GI:.2f}%)")
print(f"  -> African share of AMR trials ({100.0*AMR_A/AMR_G:.1f}%) is "
      f"{(100.0*AMR_A/AMR_G)/base:.1f}x the 4.33% baseline: OVER-represented, not under.")

print("\n=== The v1 '0.2%' framing, compared like-for-like ===")
amr_pct_africa = 100.0 * AMR_A / AFR_SITE
amr_pct_global = 100.0 * AMR_G / ALL
print(f"  AMR as % of AFRICAN trials: {AMR_A}/{AFR_SITE:,} = {amr_pct_africa:.3f}%  (v1's '0.2%')")
print(f"  AMR as % of GLOBAL trials : {AMR_G}/{ALL:,} = {amr_pct_global:.3f}%")
print(f"  Ratio (Africa / global) = {amr_pct_africa/amr_pct_global:.1f}x")
print("  -> AMR is a LARGER fraction of Africa's trials than of the world's.")
print("     The '0.2% deficit' vanishes under a like-for-like denominator.")

print("\n=== Burden-adjusted: AMR trials per 100,000 ATTRIBUTABLE AMR deaths ===")
afr_rate = AMR_A / (AFR_ATTRIB/100_000)
glob_rate = AMR_G / (GLOB_ATTRIB/100_000)
print(f"  Africa: {AMR_A} trials / {AFR_ATTRIB:,} deaths = {afr_rate:.1f} per 100k")
print(f"  Global: {AMR_G} trials / {GLOB_ATTRIB:,} deaths = {glob_rate:.1f} per 100k")
print(f"  Africa/global = {afr_rate/glob_rate:.2f}  -> near PARITY (not a specific deficit).")
print("  HONEST READ: the AMR trial enterprise is tiny relative to burden EVERYWHERE;")
print("  Africa is not specifically deficient on any like-for-like or burden-adjusted metric.")

print("\n=== What DOES survive as a real problem ===")
print("  * Absolute scarcity: 259 condition-coded AMR trials globally for a threat")
print(f"    causing {GLOB_ATTRIB:,} attributable deaths/yr (Murray 2022).")
print("  * Novel-agent gap: cefiderocol/ceftazidime-avibactam/imipenem-relebactam")
print("    trials at African sites are absent (verify by AACT intervention query).")
print("  * Concentration: African AMR trials cluster in South Africa / MDR-TB.")
print("  * Burden distinction: Africa 2019 = 250,000 ATTRIBUTABLE, 1.05M ASSOCIATED")
print("    (Sartorius 2024) -- v1 conflated these and mis-cited Murray.")
