#!/usr/bin/env python
"""
Deterministic verification for the v2 (truth-first rebuild) of View/98
(Effectiveness of differentiated service delivery [DSD] models for ART).

The v1 draft carried placeholder pooled estimates ([n], [x], [author required])
and a fabricated per-model subgroup table with no underlying study data, plus a
reference list in which several citations' volume/page coordinates belong to
unrelated papers. This rebuild discards all of that and anchors ONLY on two
independent, PubMed-verified RCT-only meta-analyses, whose reported estimates are
hard-coded here from their published abstracts:

  Bwire 2023  (Rev Med Virol 33(6):e2479; PMID 37655428) -- 16 RCTs, 13,886 pts
     Any DSD vs standard of care:
        Retention in care  RR 1.09 (95% CI 1.08-1.11), I2 = 0%
        Viral suppression  RR 1.01 (95% CI 1.00-1.02), I2 = 0%
     Adherence-clubs vs SoC (a single DSD model):
        Retention in care  RR 1.01 (95% CI 0.96-1.07), I2 = 84%
        Viral suppression  RR 1.02 (95% CI 0.98-1.07), I2 = 77%

  Nega 2026  (AIDS Res Ther 23(1):21; PMID 41582132) -- RCT-only MA
        Viral NON-suppression RR 0.89 (95% CI 0.74-1.07), I2 = 7.47%
        NON-retention in care RR 1.03 (95% CI 0.68-1.57), I2 = 90.37%
        Loss to follow-up     RR 0.80 (95% CI 0.31-2.06)

This script does NOT pool the two MAs (they share included trials -> double count).
It performs three reproducible checks:
  (1) non-inferiority logic on viral suppression against a 0.95 margin;
  (2) cross-MA concordance -- Nega's non-suppression side re-expressed on the
      suppression side and compared with Bwire (qualitative, overlap-flagged);
  (3) absolute-benefit (NNT) framing of the verified any-DSD retention RR with an
      explicitly stated baseline, plus an honest heterogeneity statement.
Requires only the standard library. Read-only.
"""
import math

Z = 1.959963985

def logci(rr, lo, hi):
    y = math.log(rr)
    se = (math.log(hi) - math.log(lo)) / (2 * Z)
    return y, se

print("=== (1) Non-inferiority on viral suppression (margin RR >= 0.95) ===")
for name, rr, lo, hi in [
    ("Bwire any-DSD VS", 1.01, 1.00, 1.02),
    ("Bwire adherence-club VS", 1.02, 0.98, 1.07),
]:
    verdict = "NON-INFERIOR (lower CI >= 0.95)" if lo >= 0.95 else "inconclusive"
    print(f"  {name:28} RR {rr:.2f} ({lo:.2f}-{hi:.2f})  -> {verdict}")
print("  Bwire any-DSD lower CI (1.00) exceeds the margin AND exceeds 1.0 ->")
print("  suppression is at least equivalent (point estimate marginally favours DSD).")

print("\n=== (2) Cross-MA concordance on viral suppression (NOT pooled) ===")
# Nega reports NON-suppression RR 0.89. On the suppression side this is protective
# for DSD (fewer non-suppressed). Express as an approximate suppression-side RR
# using a plausible baseline non-suppression risk p0 (sensitivity band).
for p0 in (0.08, 0.12, 0.16):
    rr_ns = 0.89
    # suppression RR = (1 - rr_ns*p0) / (1 - p0)
    rr_supp = (1 - rr_ns * p0) / (1 - p0)
    print(f"  Nega non-suppression RR 0.89, baseline non-suppression {p0*100:.0f}%"
          f"  -> implied suppression RR ~ {rr_supp:.3f}")
print("  All lie at/above 1.00 -> concordant with Bwire's VS RR 1.01. The two")
print("  RCT-only MAs AGREE that DSD is non-inferior on suppression.")
print("  (Overlap in included trials -> reported as corroboration, not pooled.)")

print("\n=== (3) Absolute retention benefit (any-DSD RR 1.09) + heterogeneity honesty ===")
rr, lo, hi = 1.09, 1.08, 1.11
for base in (0.75, 0.80, 0.85):
    dsd = rr * base
    arr = dsd - base
    nnt = 1 / arr if arr > 0 else float("inf")
    print(f"  Baseline SoC 12-mo retention {base*100:.0f}%  -> DSD {dsd*100:.1f}%"
          f"  (ARR {arr*100:.1f} pp, NNT {nnt:.0f})")
print("  Bwire any-DSD retention pool: I2 = 0% (tight). BUT the single-model")
print("  adherence-club pool is I2 = 84%, and Nega's non-retention pool is I2 = 90%")
print("  with CI 0.68-1.57 (spans benefit AND harm). HONEST READ: the average")
print("  retention benefit is real, but it is MODEL- and SETTING-dependent, not")
print("  uniform -- the v1's fabricated uniformly-low I2 hid this heterogeneity.")

print("\n=== Provenance ===")
print("  Evidence base is RCT-only (Bwire 16 RCTs; Nega RCT-only) -> GRADE starts")
print("  HIGH, downgraded for heterogeneity/indirectness, NOT the v1's premise of")
print("  'predominantly observational, VERY LOW'. This is a substantive correction.")
