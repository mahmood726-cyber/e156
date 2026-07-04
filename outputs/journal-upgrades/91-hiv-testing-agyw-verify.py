#!/usr/bin/env python
"""
Provenance/verification record for the v2 advanced version of the Synthesis paper
"HIV Testing Services Uptake Among Adolescent Girls and Young Women" (View/91).

Like paper 95, this v1 draft is placeholder-driven and shares a FABRICATED PMID.
v2 contribution is reference-integrity + honest reframing. Verified 2026-07-04.

Verified evidence anchor (NOT AGYW-specific): Johnson CC et al. J Int AIDS Soc
2017;20(1):21594, PMID 28530049 -- HIVST doubles testing uptake among men
RR 2.12 (1.51-2.98); frequency rate ratio 1.88 (1.17-3.01); no social harm.
This trial base is among MEN, not AGYW; it establishes the HIVST effect in general
but does NOT provide an AGYW-specific pooled uptake estimate.
"""
VERIFIED = {
    "HIVST uptake (general, men), RR":      ("2.12", "1.51-2.98", "Johnson 2017 PMID 28530049"),
    "HIVST frequency (general, MSM), RR":   ("1.88", "1.17-3.01", "Johnson 2017"),
    "social harm":                          ("none", "-",         "Johnson 2017"),
}
V1_WITHDRAWN = {
    "abstract '[author verify]'/'[author required]' placeholders": "removed (uptake RR, cascade counts)",
    "Ortblad PMID 28926628": "WRONG (a Raman-spectroscopy diabetes paper; same error as paper 95) -> removed",
    "AGYW-specific modality ranking (HIVST>mobile>PITC) with implied RRs": "no verified AGYW-specific source -> WITHDRAWN",
    "cascade 'per 1000 AGYW' additional testers / positives / linked": "all placeholders -> WITHDRAWN",
}
print("HIV testing in AGYW (View/91) — verification & provenance record (v2)")
print("\nVERIFIED (general HIVST effect, NOT AGYW-specific):")
for k,(e,ci,src) in VERIFIED.items():
    print(f"  {k:<38} {e:>5} (95% CI {ci}) [{src}]")
print("\nWITHDRAWN from v1 (placeholder / fabricated / unsourced):")
for k,v in V1_WITHDRAWN.items():
    print(f"  - {k}\n      -> {v}")
print("\nHonest state: HIVST reliably increases testing uptake in the general evidence")
print("base (RR 2.12), and AGYW are a WHO priority population, but an AGYW-SPECIFIC")
print("pooled uptake estimate and cascade are NOT established by verified data here.")
print("The AGYW modality ranking and cascade in v1 were placeholders and are withdrawn.")
