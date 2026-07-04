# HIV Testing in Adolescent Girls and Young Women: Separating a Verified General Effect from an Unverified AGYW-Specific Claim

**Published (base article):** Synthēsis · View/91
**Authors:** Christine Muhumuza et al.
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `91-hiv-testing-agyw-verify.py` (deterministic)
**Evidence tier:** MODERATE for the general HIVST effect; the AGYW-specific ranking is NOT established.
**Standard:** PRISMA 2020 · GRADE · verified anchor · reproduce-or-flag.

---

## Upgrade note (what changed from v1)

The v1 draft was placeholder-driven and shared a fabricated citation with the HIV
self-testing paper (View/95). Specifically: its abstract carried live placeholders
("[Author: insert n trials]", "[author verify from meta-analysis dataset]", cascade
counts "[author required]"); its AGYW-specific modality ranking (HIVST > mobile/outreach
> PITC) had no verified source; and it cited the **same wrong Ortblad PMID (28926628)**
— a Raman-spectroscopy diabetes paper, not an HIV self-testing trial — that v2 already
removed from paper 95. v2 (i) anchors the one claim that can be verified (HIVST doubles
testing uptake in the general evidence base; Johnson 2017), (ii) states plainly that this
anchor is **not AGYW-specific**, and (iii) withdraws the placeholder AGYW modality ranking
and cascade rather than shipping invented numbers. The honest result is a clear separation
of what is established from what is not.

---

## Abstract

**Background.** Adolescent girls and young women (AGYW, 15–24) bear a disproportionate share
of new HIV infections in sub-Saharan Africa and test at lower rates than adult women.
Achieving the UNAIDS first-95 (status awareness) requires closing this gap.

**Methods.** We assessed which testing-intervention claims for AGYW are supported by verified
randomised evidence, anchoring on the WHO-commissioned HIV self-testing meta-analysis
(Johnson 2017) and distinguishing general from AGYW-specific effects. Verified inputs;
deterministic provenance script.

**Results.** HIV self-testing (HIVST) reliably **increases testing uptake** in the general
randomised evidence base: **RR 2.12 (95% CI 1.51–2.98)** for uptake and rate ratio **1.88**
for frequency, with no social harm (Johnson 2017). **However, this evidence is among men,
not AGYW**, and provides no AGYW-specific pooled uptake estimate. The v1 draft's AGYW modality
ranking (HIVST > mobile > provider-initiated testing) and its per-1,000-AGYW cascade were
**placeholders without a verified source and are withdrawn.**

**Conclusion.** The verified, transferable message is that HIVST substantially increases
testing uptake and should be offered to AGYW as an additional approach, paired with
facilitated linkage. A quantitative AGYW-specific effectiveness ranking and cascade are **not
established** by verified data and require AGYW-specific trials or an individual-participant-
data analysis — they should not be asserted with invented numbers.

---

## 1. Introduction

AGYW are a WHO and PEPFAR priority population: in high-burden sub-Saharan settings they
account for a large share of new infections among young people, and they face
age-and-gender-specific barriers to facility-based testing (school hours, stigma,
provider judgement, confidentiality concerns). The policy hope is that alternative testing
modalities — self-testing, mobile/outreach, demand-creation — raise uptake in this group.
This paper does something narrower and more honest than v1 attempted: it establishes what the
verified randomised evidence supports, and it refuses to convert that into an AGYW-specific
quantitative ranking the evidence cannot bear.

## 2. Methods

We anchored on the WHO-commissioned systematic review and meta-analysis of HIV self-testing
(Johnson 2017, JIAS 20:21594; PMID 28530049), reporting its verified pooled estimates and
assessing their applicability to AGYW. We then evaluated whether v1's AGYW-specific
modality ranking and cascade could be traced to any verified source. Where they could not,
we withdrew them. The provenance of every claim is recorded in
`91-hiv-testing-agyw-verify.py`.

## 3. Results

### 3.1 What is verified (general HIVST effect)

| Outcome | Population | Estimate (95% CI) |
|---|---|---|
| HIVST increases testing **uptake** | men | **RR 2.12 (1.51–2.98)** |
| HIVST increases testing **frequency** | MSM | rate ratio 1.88 (1.17–3.01) |
| Social harm | all | none observed |

This is robust (5 RCTs, 4,145 participants) and directly supports offering HIVST as an
additional testing approach. Its limitation for this paper is explicit: the trial base is
**among men**, so it establishes the *mechanism* (removing facility-attendance and privacy
barriers roughly doubles uptake) but not an *AGYW-specific magnitude*.

### 3.2 What is NOT established (AGYW-specific claims)

The v1 draft asserted, for AGYW specifically: an overall pooled uptake RR (left as
"[author verify]"), a modality ranking (HIVST highest, mobile/outreach intermediate, PITC
minimal), and a cascade ("per 1,000 AGYW eligible, HIVST yields [author required] additional
testers, of whom [author required] are newly positive and [author required] link to care").
**None of these has a verified source; all are withdrawn.** An AGYW-specific effectiveness
ranking would require trials enrolling AGYW with head-to-head or common-comparator modality
arms, or an individual-participant-data meta-analysis harmonising AGYW subgroups across
trials — neither of which the v1 draft cited.

### 3.3 The transferable, honest conclusion

Two things are simultaneously true and must not be conflated: (i) HIVST reliably increases
testing uptake and is safe (general evidence), so it is a sound component of AGYW testing
programmes; and (ii) the specific *magnitude* of benefit and the *ranking* of modalities *in
AGYW* are not quantified by verified evidence. The correct posture is to deploy HIVST (and
other low-barrier modalities) for AGYW on the strength of the general effect and the strong
mechanistic rationale, while treating any AGYW-specific effect size as an open empirical
question — and, as in the general HIVST literature, to pair testing with **facilitated
linkage**, since unsupervised testing shifts the bottleneck from diagnosis to linkage.

### 3.4 GRADE

| Claim | Certainty |
|---|---|
| HIVST increases testing uptake (general) | **MODERATE** |
| HIVST is safe (no social harm) | **MODERATE** |
| Applicability of the uptake effect to AGYW | **LOW** (indirect: trials among men) |
| AGYW-specific modality ranking / cascade | **INSUFFICIENT** (no verified source) |

## 4. Discussion

This paper is a corrective more than a synthesis, because the v1 draft's central deliverable
— an AGYW-specific modality ranking and cascade — was built from placeholders and a
fabricated citation. Removing them leaves less, but what remains is true: HIV self-testing
roughly doubles testing uptake without harm, and AGYW are a population for whom the barriers
HIVST removes (facility attendance, privacy, provider judgement) are especially salient. That
is a sufficient basis to include HIVST in AGYW programming. It is not a sufficient basis to
publish a numerical ranking of modalities or a quantified cascade *specific to AGYW*, and
doing so would substitute false precision for the honest statement that the AGYW-specific
evidence is thin.

The research implication is specific: the field needs AGYW-enrolled trials designed for
modality comparison, and an individual-participant-data meta-analysis that can isolate the
AGYW subgroup across existing trials, before an AGYW effectiveness ranking can be asserted.
The programmatic implication is that facilitated linkage — not testing uptake — is likely the
binding constraint, consistent with the general HIVST literature in which the post-test
cascade, not the test itself, limits population impact. Investing in supported linkage for
AGYW who test reactive is the action most likely to convert increased testing into reduced
transmission.

## 5. Limitations

The anchoring evidence is among men and searched to 2016; it establishes the general HIVST
effect but not an AGYW-specific magnitude, and more recent AGYW-relevant trials should be
incorporated as their identities and results are verified. The withdrawal of v1's AGYW
ranking and cascade leaves those questions open rather than answered — which is the truthful
state of the evidence. The epidemiological framing (AGYW share of new infections) is drawn
from UNAIDS reporting and should be cited to the specific report and year at copy-edit rather
than asserted as a fixed figure.

## 6. Conclusion

HIV self-testing reliably increases testing uptake without social harm (RR 2.12) and should be
offered to AGYW, paired with facilitated linkage. An AGYW-specific modality ranking and
cascade are **not established** by verified evidence and were withdrawn from this version, along
with a fabricated trial citation. The priority is AGYW-specific trials and supported linkage —
not the assertion of invented AGYW-specific numbers.

---

## References

1. Johnson CC, Kennedy C, Fonner V, et al. Examining the effects of HIV self-testing compared to standard HIV testing services: a systematic review and meta-analysis. *J Int AIDS Soc.* 2017;20(1):21594. PMID: 28530049. doi:10.7448/IAS.20.1.21594.
2. World Health Organization. *Consolidated Guidelines on HIV Testing Services.* Geneva: WHO; 2019.
3. UNAIDS. *Global AIDS Update 2023: The Path That Ends AIDS.* Geneva: UNAIDS; 2023.

---

*Data-integrity note.* The verified anchor (Johnson 2017, PMID 28530049; HIVST uptake RR 2.12
[1.51–2.98], frequency rate ratio 1.88, no social harm) was confirmed by PubMed metadata +
abstract match on 2026-07-04 (the same verified source used in paper 95). This anchor is
**general (among men), not AGYW-specific**, and is labelled as such. v1's abstract placeholders,
its AGYW-specific modality ranking and per-1,000 cascade (all unsourced), and the **wrong Ortblad
PMID 28926628** (a Raman-spectroscopy diabetes paper — the same fabrication removed from paper
95) were **withdrawn**, not carried forward. The provenance of each claim is recorded in
`91-hiv-testing-agyw-verify.py`. **Build target:** `.docx` via the E156 host build
(`outputs/journal-upgrades/build/91-hiv-testing-agyw-v2/`); render the verified-vs-withdrawn
claims table (§3.1–3.2).
