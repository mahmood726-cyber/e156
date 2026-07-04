# JAK Inhibitors in Rheumatoid Arthritis: A Truth-First Benefit–Risk Reconstruction of ORAL Surveillance

**Published (base article):** Synthēsis · View/105
**Authors:** Mahmood Ahmad (middle author); first/last authors per the original E156 submission.
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `105-oral-surveillance-verify.py` (deterministic)
**Evidence tier:** MODERATE (single large RCT, CV-risk-enriched population).
**Standard:** non-inferiority interpretation · absolute-risk / NNH · reproduce-or-flag.

---

## Upgrade note (what changed from v1, and why)

The v1 draft carried **incorrect confidence intervals** for the headline safety
endpoints. It stated MACE HR 1.33 (95% CI **1.00–1.76**) and VTE HR 1.96
(1.30–2.97), with dose-specific HRs (1.43, 2.55). The verified primary NEJM report
(Ytterberg 2022, PMID 35081280) gives the combined-tofacitinib-vs-TNFi MACE HR as
**1.33 (0.91–1.94)** and cancer HR as **1.48 (1.04–2.09)**. The v1 MACE interval
(1.00–1.76) does not match the published primary result and cannot be sourced to the
trial abstract; the VTE and dose-stratified figures are secondary-analysis quantities
that are **not** in the primary report. v2 therefore (i) anchors every quantitative
claim on the two **verified coprimary endpoints**, (ii) adds an absolute-risk /
number-needed-to-harm analysis and an explicit non-inferiority-margin interpretation,
(iii) validates the published HRs by independent risk-ratio reconstruction, and
(iv) **flags** VTE and dose-stratified estimates as requiring full-text verification
rather than asserting v1's numbers. Efficacy claims that v1 marked `[author verify]`
are not repeated as facts.

---

## Abstract

**Background.** JAK inhibitors (tofacitinib, baricitinib, upadacitinib) match biologic
DMARDs for rheumatoid-arthritis (RA) efficacy but carry a regulatory boxed warning
driven by ORAL Surveillance — the mandated post-authorisation safety trial of
tofacitinib versus a TNF inhibitor (TNFi).

**Methods.** We reconstructed the benefit–risk profile from the verified coprimary
results of ORAL Surveillance (n=4,362; median follow-up 4.0 y): adjudicated MACE and
cancers (excluding non-melanoma skin cancer, NMSC), combined tofacitinib (5+10 mg,
n=2,911) versus TNFi (n=1,451). We computed absolute risk differences, numbers-needed-
to-harm (NNH), independent risk-ratio reconstructions, and applied the trial's
pre-specified non-inferiority margin (upper 95% CI < 1.8). Deterministic script.

**Results.** MACE: 3.4% (98/2,911) vs 2.5% (37/1,451); HR **1.33 (0.91–1.94)**; ARD
**+0.82 pp**; **NNH ≈ 122**. Cancer: 4.2% (122/2,911) vs 2.9% (42/1,451); HR **1.48
(1.04–2.09)**; ARD **+1.30 pp**; **NNH ≈ 77**. **Neither** endpoint met non-inferiority
(both upper CIs exceed 1.8); cancer was significantly increased (lower CI 1.04 > 1).
Risk-ratio reconstructions (1.32, 1.45) closely match the adjudicated Cox HRs (1.33,
1.48), validating the published estimates.

**Conclusion.** In a CV-risk-enriched RA population, tofacitinib failed non-inferiority
to TNFi for both cardiovascular and cancer safety, with a significant excess of
malignancy. The absolute harms are modest (NNH 77–122 over four years) but real, and
justify the class-label restriction to patients who have failed a TNFi. The result is
a non-inferiority failure, not proof of a large hazard — a distinction with direct
prescribing implications.

---

## 1. Introduction

RA affects 0.5–1% of adults and, in the 30–40% with inadequate methotrexate response,
is treated with biologic DMARDs (principally TNF inhibitors) or oral JAK inhibitors.
JAK inhibitors block Janus-kinase/STAT cytokine signalling and offer oral administration
with efficacy broadly comparable to biologics. Their regulatory status was transformed
by **ORAL Surveillance** (NCT02092467), an FDA-mandated non-inferiority safety trial in
RA patients ≥50 years with ≥1 additional cardiovascular risk factor, randomised 1:1:1
to tofacitinib 5 mg BID, 10 mg BID, or a TNFi. The 2022 NEJM report showed that
tofacitinib did not meet the pre-specified safety non-inferiority bar for its coprimary
endpoints, triggering a January-2022 class-label change restricting all JAK inhibitors
to patients who have failed a TNFi. This v2 focuses on what the trial actually
established, quantifies the absolute harm, and interprets the non-inferiority logic
correctly — because the difference between "failed non-inferiority" and "significantly
harmful" is frequently blurred in secondary commentary.

## 2. Methods

We used the verified coprimary results of ORAL Surveillance (Ytterberg 2022, PMID
35081280): event counts and hazard ratios for adjudicated MACE and cancer (excluding
NMSC), combined tofacitinib doses versus TNFi. For each endpoint we computed the
observed proportions, absolute risk difference (ARD), number-needed-to-harm
(NNH = 1/ARD), and an independent crude risk-ratio reconstruction (as a consistency
check against the adjudicated time-to-event HR). We applied the trial's pre-specified
non-inferiority rule — non-inferiority is shown only if the **upper** bound of the
two-sided 95% CI for the combined-tofacitinib-vs-TNFi HR is **< 1.8** — and separately
flagged whether each endpoint was individually statistically increased (lower CI > 1).
All values are emitted by `105-oral-surveillance-verify.py`. VTE and dose-stratified
(5 mg vs 10 mg) estimates are **not** in the primary report and are flagged as requiring
full-text/secondary-analysis verification; they are not asserted.

## 3. Results

### 3.1 Verified benefit–risk table (combined tofacitinib vs TNFi)

| Coprimary endpoint | Tofacitinib | TNFi | HR (95% CI) | ARD | NNH | NI met (upper<1.8)? | Sig. increased? |
|---|---|---|---|---|---|---|---|
| **MACE** (adjudicated) | 98/2,911 (3.4%) | 37/1,451 (2.5%) | **1.33 (0.91–1.94)** | +0.82 pp | **122** | **No** | No (CI incl. 1) |
| **Cancer** (excl. NMSC) | 122/2,911 (4.2%) | 42/1,451 (2.9%) | **1.48 (1.04–2.09)** | +1.30 pp | **77** | **No** | **Yes** |

*Total N = 4,362 (tofacitinib 5 mg 1,455 + 10 mg 1,456 + TNFi 1,451). Median follow-up
4.0 years.*

### 3.2 Independent validation of the published HRs

Crude risk-ratio reconstructions from the event counts — MACE 3.37%/2.55% = **1.32**;
cancer 4.19%/2.89% = **1.45** — closely match the adjudicated Cox hazard ratios (1.33
and 1.48). The concordance confirms the published estimates are internally consistent
with the reported event counts and denominators (no transcription or reporting error).

### 3.3 Non-inferiority interpretation (the key nuance)

ORAL Surveillance was a **non-inferiority** trial with a margin of 1.8 on the upper
95% CI. The correct reading is asymmetric:

- **MACE**: HR 1.33, upper CI **1.94 > 1.8** → non-inferiority **not shown**. The CI
  also includes 1 (0.91), so MACE is *not* individually "significantly increased" — but
  in a non-inferiority framework, failing to exclude the margin is itself the adverse
  finding. Reporting this as "no significant MACE difference" (as if superiority testing
  applied) would misstate the trial.
- **Cancer**: HR 1.48, upper CI 2.09 > 1.8 → non-inferiority not shown; **and** lower CI
  1.04 > 1 → cancer is significantly increased on its own terms. This is the firmer of
  the two safety signals.

### 3.4 Absolute harm in context

Over four years, the excess events are ~0.82 percentage points (MACE) and ~1.30
percentage points (cancer), i.e. NNH ≈ 122 and ≈ 77. These are modest absolute
magnitudes in a deliberately CV-risk-enriched population (≥50 years, ≥1 CV risk factor),
and they should not be extrapolated to younger, lower-risk RA patients, in whom the
absolute hazard is expected to be smaller. Efficacy was similar across all three arms,
so the benefit side of the ledger is a wash between tofacitinib and TNFi — which is
precisely why a safety non-inferiority failure is decision-relevant.

### 3.5 GRADE

| Outcome | Basis | Certainty | Note |
|---|---|---|---|
| Cancer (excl. NMSC), tofacitinib vs TNFi | ORAL Surveillance | **MODERATE** | Significant; NI not met |
| MACE, tofacitinib vs TNFi | ORAL Surveillance | **MODERATE** | NI not met; CI includes 1 |
| MACE/cancer for baricitinib, upadacitinib vs TNFi | no dedicated safety RCT | **LOW** | class-labelled by extrapolation |

## 4. Discussion

ORAL Surveillance is a rare, well-powered head-to-head safety trial, and its verified
result is unambiguous on its own terms: tofacitinib did **not** meet non-inferiority to
a TNFi for either cardiovascular events or cancer in a CV-risk-enriched RA population,
and the malignancy signal was individually significant (HR 1.48, 1.04–2.09). The
absolute harms are modest — NNH of roughly 77 (cancer) and 122 (MACE) over four years —
but they are real and, crucially, arise against **equivalent efficacy**, so there is no
countervailing benefit to offset them within the tofacitinib-versus-TNFi choice.

Two interpretive errors recur in the secondary literature and are worth correcting.
First, treating the MACE CI (0.91–1.94) as "no significant difference" imports a
superiority framework into a non-inferiority trial; the correct statement is that
non-inferiority was refuted. Second, the whole-class label change rests on extrapolation:
only tofacitinib was tested head-to-head, and dedicated non-inferiority safety RCTs of
baricitinib and upadacitinib versus TNFi do not exist, so their MACE/cancer certainty
is LOW and rests on mechanism-and-registry inference rather than randomised evidence. A
selective-JAK1 agent may or may not share tofacitinib's pan-JAK safety profile; the data
to adjudicate this are not yet available.

The clinical translation is proportionate rather than prohibitive: in patients ≥50 with
cardiovascular risk factors, a TNFi is the preferred second-line agent, and a JAK
inhibitor is reserved for TNFi failure or specific indications — exactly the regulatory
position. In younger, lower-CV-risk patients the absolute excess is expected to shrink,
and shared decision-making that quantifies the four-year NNH (rather than citing a
hazard ratio alone) is the appropriate frame.

## 5. Limitations

Single trial; CV-risk-enriched, ≥50-year population limits generalisability to younger
RA patients. Open-label design (blinded endpoint adjudication mitigates but does not
eliminate ascertainment concerns). VTE and dose-stratified (5 mg vs 10 mg) safety
estimates — clinically important, and the original basis for the 2019 pulmonary-embolism
alert — are secondary-analysis quantities not in the primary abstract and were
deliberately **not** reconstructed here; they require full-text verification. Efficacy
comparisons across JAK inhibitors and biologics were not re-derived in this v2 and are
addressed only qualitatively.

## 6. Conclusion

In ORAL Surveillance, tofacitinib failed safety non-inferiority to a TNF inhibitor for
both coprimary endpoints in a CV-risk-enriched RA population: MACE HR 1.33 (0.91–1.94;
NNH ≈ 122) and cancer HR 1.48 (1.04–2.09; NNH ≈ 77, significantly increased).
Independent risk-ratio reconstruction validates the published hazard ratios. The finding
justifies restricting JAK inhibitors to TNFi-failure patients ≥50 with cardiovascular
risk, while acknowledging that the absolute harm is modest and that whole-class
extrapolation to baricitinib and upadacitinib rests on LOW-certainty evidence pending
dedicated head-to-head safety trials.

---

## References

1. Ytterberg SR, Bhatt DL, Mikuls TR, et al. Cardiovascular and Cancer Risk with Tofacitinib in Rheumatoid Arthritis (ORAL Surveillance). *N Engl J Med.* 2022;386(4):316–326. PMID: 35081280. doi:10.1056/NEJMoa2109927.
2. Smolen JS, Landewé RBM, Bergstra SA, et al. EULAR recommendations for the management of rheumatoid arthritis with synthetic and biological DMARDs: 2022 update. *Ann Rheum Dis.* 2023;82(1):3–18. PMID: 36357155.
3. US Food and Drug Administration. FDA requires warnings about increased risk of serious heart-related events, cancer, blood clots, and death for JAK inhibitors (Drug Safety Communication, 1 September 2021).

---

*Data-integrity note.* The ORAL Surveillance PMID (35081280), title, journal, first
author (Ytterberg), citation (NEJM 386(4):316–326), coprimary HRs, event counts, and
denominators were verified by PubMed metadata match on 2026-07-04. Absolute risk
differences, NNH, risk-ratio reconstructions, and the non-inferiority-margin logic are
computed by `105-oral-surveillance-verify.py`. Reference 2 (EULAR 2022 update, Smolen,
*Ann Rheum Dis* 2023;82(1):3–18, PMID 36357155, doi:10.1136/ard-2022-223356) was verified
by PubMed metadata match on 2026-07-04; reference 3 is the FDA Drug Safety Communication
(regulatory document, not a PMID). v1's efficacy network-meta-analysis figures (ACR50 head-to-head
CIs) were marked `[author verify]` in the source and are **not** carried into v2 as
verified claims. **Build target:** `.docx` via the E156 host build
(`outputs/journal-upgrades/build/105-oral-surveillance-v2/`); render the benefit-risk
table (§3.1) as a paired absolute-risk / NNH figure.
