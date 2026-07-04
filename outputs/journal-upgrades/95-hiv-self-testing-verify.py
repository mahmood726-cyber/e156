#!/usr/bin/env python
"""
Deterministic provenance/verification record for the v2 advanced version of the
Synthesis paper "HIV Self-Testing" (View/95).

This paper's v2 contribution is reference-integrity + honest reframing rather than a
new pooled computation, so this script records (a) the VERIFIED anchor estimates and
(b) the provenance status of every v1 quantitative claim. All values verified against
PubMed metadata + abstract on 2026-07-04.

Anchor (verified): Johnson CC et al. "Examining the effects of HIV self-testing vs
standard HIV testing services: a systematic review and meta-analysis." J Int AIDS Soc
2017;20(1):21594. PMID 28530049. doi 10.7448/IAS.20.1.21594. (WHO-commissioned;
5 RCTs, 4,145 participants, 4 countries, free oral-fluid kits, among men.)
"""

VERIFIED = {
    "uptake (men), RR":            ("2.12", "1.51-2.98", "3 RCTs", "Johnson 2017"),
    "frequency (MSM), rate ratio": ("1.88", "1.17-3.01", "2 RCTs", "Johnson 2017"),
    "additional tests 12-15mo, MD":("2.13", "1.59-2.66", "2 RCTs", "Johnson 2017"),
    "HIV+ diagnosis, RR":          ("2.02", "0.37-10.76","2 RCTs", "Johnson 2017 (imprecise)"),
    "social harm":                 ("none", "-",         "5 RCTs", "Johnson 2017"),
}

V1_CLAIMS_WITHDRAWN = {
    "modality RR community 2.15":   "no verified source -> WITHDRAWN",
    "modality RR secondary 2.05":   "no verified source -> WITHDRAWN",
    "modality RR workplace 1.76":   "no verified source -> WITHDRAWN",
    "modality RR facility 1.35":    "no verified source -> WITHDRAWN",
    "linkage facility ~75% / secondary ~45%": "no verified source -> WITHDRAWN",
    "abstract '[author from MA]' placeholders": "removed",
    "Ortblad PMID 28926628":        "WRONG (a Raman-spectroscopy diabetes paper) -> removed",
}

print("HIV Self-Testing (View/95) — verification & provenance record (v2)")
print("\nVERIFIED anchor estimates (Johnson 2017, PMID 28530049):")
for k,(est,ci,kk,src) in VERIFIED.items():
    print(f"  {k:<30} {est:>6}  (95% CI {ci:<11}) {kk:<8} [{src}]")

print("\nv1 claims assessed and WITHDRAWN (untraceable / wrong):")
for k,v in V1_CLAIMS_WITHDRAWN.items():
    print(f"  - {k:<44} {v}")

print("\nConclusion: HIVST reliably ~doubles testing uptake (RR 2.12) and frequency")
print("(1.88) without social harm [MODERATE certainty]; a modality RANKING is NOT")
print("established (evidence is single-modality-dominant) [INSUFFICIENT]. Linkage to")
print("care after a reactive self-test is the decisive implementation gap.")
