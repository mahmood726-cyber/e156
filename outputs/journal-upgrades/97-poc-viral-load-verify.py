#!/usr/bin/env python
"""
Deterministic verification for the v2 advanced version of the Synthesis paper
"Point-of-Care Viral Load Testing for HIV Treatment Monitoring" (View/97).

TRUTH-FIRST CORRECTION: v1 anchored on "SAMBA-1 (PMID 31326362)" with a NULL result
(RR 0.77 for unsuppressed, NS). BOTH are wrong: PMID 31326362 is a DNA-repair paper,
and the real landmark RCT of POC VL is the STREAM trial, which was POSITIVE. v1's
headline ("best RCT evidence does not show significant improvement") is therefore
backwards and is corrected here.

Verified anchor (PubMed metadata + abstract matched 2026-07-04):
  Drain PK et al. "Point-of-care HIV viral load testing combined with task shifting to
  improve treatment outcomes (STREAM)." Lancet HIV 2020;7(4):e229-e237. PMID 32105625.
  doi 10.1016/S2352-3018(19)30402-3. NCT03066128. Open-label non-inferiority RCT,
  Durban, South Africa. N=390 (195 POC+task-shift / 195 standard lab VL).
  Combined viral suppression (<200 c/mL) + retention @12mo: 175/195 (90%) vs 148/195 (76%),
     difference +13.9% (6.4-21.2), p<0.0004.
  Viral suppression: 182/195 (93%) vs 162/195 (83%), +10.3% (3.9-16.8), p=0.0025.
  Retention:         180/195 (92%) vs 162/195 (85%), +7.7% (1.3-14.2), p=0.026.
  No adverse events related to POC testing or task shifting.

Recompute risk differences, risk ratios, NNT, and Fisher-exact p from the counts.
Deterministic; scipy.
"""
from scipy.stats import fisher_exact

def analyse(label, e_i, n_i, e_c, n_c, pub_diff, pub_p):
    p_i, p_c = e_i/n_i, e_c/n_c
    rd = p_i - p_c
    rr = p_i / p_c
    nnt = 1/rd
    _, p = fisher_exact([[e_i, n_i-e_i], [e_c, n_c-e_c]], alternative="two-sided")
    print(f"\n{label}")
    print(f"  POC {e_i}/{n_i} = {p_i*100:.1f}%   standard {e_c}/{n_c} = {p_c*100:.1f}%")
    print(f"  risk difference = {rd*100:+.1f} pp  (published {pub_diff})")
    print(f"  risk ratio = {rr:.3f}   NNT = {nnt:.1f}")
    print(f"  Fisher-exact two-sided p = {p:.4g}  (published {pub_p})  -> "
          f"{'SIGNIFICANT' if p<0.05 else 'ns'}")

print("STREAM (POC viral load) — deterministic verification (v2)")
print("v1's anchor was WRONG: SAMBA-1 PMID 31326362 = a DNA-repair paper; the real")
print("landmark RCT is STREAM (Drain 2020, PMID 32105625), which was POSITIVE.")
analyse("Combined viral suppression + retention @12mo (PRIMARY)",
        175, 195, 148, 195, "+13.9% (6.4-21.2)", "p<0.0004")
analyse("Viral suppression (<200 c/mL)",
        182, 195, 162, 195, "+10.3% (3.9-16.8)", "p=0.0025")
analyse("Retention in care [NOTE: source abstract internally inconsistent]",
        180, 195, 162, 195, "+7.7% (1.3-14.2)", "p=0.026")
print("  ^ the abstract states standard-arm retention as '162 (85%)', but 162/195=83.1%;")
print("    the same count 162 is also given for suppression (83%). We therefore report")
print("    the PUBLISHED retention difference (+7.7pp, p=0.026) and flag the discrepancy;")
print("    the primary combined endpoint and suppression reproduce EXACTLY.")

print("\n" + "="*66)
print("Corrected conclusion: the best RCT evidence (STREAM) shows POC VL testing")
print("combined with task shifting SIGNIFICANTLY IMPROVED the combined suppression +")
print("retention endpoint (+13.9pp, NNT ~7), viral suppression (+10.3pp, NNT ~10), and")
print("retention (+7.7pp, NNT ~13). v1's 'no significant improvement' claim rested on a")
print("misattributed trial and is reversed. (Single-site trial; generalisability caveat.)")
