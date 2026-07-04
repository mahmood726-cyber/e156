# HIV Self-Testing: What the Randomised Evidence Actually Shows — and What It Does Not (A Truth-First Reconstruction)

**Published (base article):** Synthēsis · View/95
**Authors:** Christine Muhumuza et al.
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `95-hiv-self-testing-verify.py` (deterministic)
**Evidence tier:** MODERATE for the uptake-doubling effect; modality-specific ranking is NOT established.
**Standard:** PRISMA 2020 · GRADE · verified anchor · reproduce-or-flag.

---

## Upgrade note (what changed from v1) — placeholders and a wrong PMID

The v1 draft could not be submitted as written: its abstract contained live
placeholders ("Pooled RR = [author from MA]", "[Author: insert k trials and N]",
"Secondary distribution multiplier: [author required]"), and its central claim — a
modality ranking with specific pooled risk ratios (community 2.15, secondary 2.05,
workplace 1.76, facility 1.35) — was **not traceable to any verified source**. In
addition, a cited pivotal trial PMID was wrong: v1's Ortblad reference (PMID 28926628)
is in fact a Raman-spectroscopy diabetes-screening paper, not an HIVST trial. v2 (i)
anchors every quantitative claim on the **verified** WHO-commissioned systematic review
and meta-analysis (Johnson 2017, JIAS; PMID 28530049); (ii) replaces the unverifiable
modality ranking with an honest statement of what the RCT evidence does and does not
establish; and (iii) removes placeholders and the wrong citation. The result is a
shorter list of claims, each of which is true.

---

## Abstract

**Background.** HIV self-testing (HIVST) lets individuals test privately without a health
worker, removing facility-attendance and privacy barriers. Its effect on testing uptake,
and whether delivery modality changes that effect, are operationally central questions.

**Methods.** We synthesised the verified randomised evidence, anchored on the
WHO-commissioned meta-analysis (Johnson 2017: 5 RCTs, 4,145 participants, 4 countries) and
its GRADE assessment, and examined whether modality-specific effectiveness can be
supported by the current evidence base. All quantitative claims are PubMed-verified.

**Results.** HIVST **doubles uptake of testing among men** (RR **2.12; 95% CI 1.51–2.98**,
3 RCTs) and **nearly doubles testing frequency** among men who have sex with men (rate
ratio **1.88; 1.17–3.01**), yielding ~2 additional tests over 12–15 months (mean
difference 2.13). HIVST also roughly doubled HIV-positive diagnoses (RR **2.02**), though
imprecisely (95% CI 0.37–10.76). Across all RCTs there was **no evidence of social harm**
and minimal risk-behaviour change. **What is not established:** a modality ranking. The
five pooled RCTs almost all used one modality (free oral-fluid kits among men), so
head-to-head modality comparisons are under-powered; the specific per-modality RRs in the
v1 draft have no verified source and are withdrawn. Linkage to confirmatory care after a
reactive self-test remains the principal implementation gap, flagged by WHO but not
quantifiable to a single reliable modality-stratified figure here.

**Conclusion.** The robust, verified message is that HIVST substantially increases testing
uptake and frequency without harm, and should be offered as an additional testing
approach — as WHO recommends. The claim that specific delivery modalities differ in
effectiveness by a fixed rank order is **not supported** by the current randomised
evidence and requires individual-participant-data analysis to test.

---

## 1. Introduction

HIV self-testing was endorsed by WHO in 2016 after randomised evidence showed it increases
testing uptake, particularly among populations underserved by facility-based services.
Multiple delivery modalities exist — community distribution, secondary/partner
distribution, workplace distribution, and supervised facility HIVST — and the operational
hope is that some are more effective or more reach-extending than others. This paper does
two things. First, it states precisely what the randomised evidence establishes about
HIVST's effect on testing. Second — and this is the corrective contribution — it
distinguishes that established effect from the *modality-ranking* claim, which the current
evidence base cannot yet support and which the v1 draft asserted with unsourced numbers.

## 2. Methods

We anchored the synthesis on the WHO-commissioned systematic review and meta-analysis
(Johnson 2017, JIAS 20:21594; PMID 28530049), which searched to June 2016, applied
random-effects meta-analysis and GRADE, and underpins the WHO recommendation. We report
its pooled estimates verbatim and assess whether the modality-stratified effectiveness
claim can be supported. Where v1 asserted numbers without a traceable source, we withdraw
them and say so. All values are emitted by `95-hiv-self-testing-verify.py`, which records
the verified estimates and the provenance status of each v1 claim.

## 3. Results

### 3.1 What HIVST does — verified pooled effects (Johnson 2017)

| Outcome | Population | Estimate (95% CI) | k RCTs |
|---|---|---|---|
| **Uptake of testing** | men | **RR 2.12 (1.51–2.98)** | 3 |
| **Frequency of testing** | MSM | **Rate ratio 1.88 (1.17–3.01)** | 2 |
| Additional tests over 12–15 mo | MSM | Mean difference 2.13 (1.59–2.66) | 2 |
| HIV-positive diagnosis | men | RR 2.02 (0.37–10.76) | 2 |
| Social harm | all | none observed | 5 |

The evidence base is 5 RCTs, 4,145 participants, 4 countries, all offering **free
oral-fluid rapid tests, among men**. The uptake effect is robust (lower CI 1.51); the
positive-diagnosis effect is directionally concordant but imprecise (CI includes 1). No
social harm and minimal risk-behaviour change were observed.

### 3.2 What is NOT established — the modality ranking

The v1 draft's central table ranked four modalities by pooled RR (community 2.15,
secondary 2.05, workplace 1.76, facility 1.35). **These figures have no verified source
and are withdrawn.** The reason is structural: the five pooled RCTs in the definitive
review almost all used a single modality (free oral-fluid kits distributed to men), so the
evidence supports the *overall* effect of HIVST but not a *contrast between* modalities. A
credible modality ranking would require either head-to-head randomised comparisons or an
individual-participant-data meta-analysis harmonising outcomes across differently-designed
trials — neither of which is reflected in the pooled estimate. Presenting a fixed rank
order as if established would misrepresent the evidence.

### 3.3 The real implementation question: linkage after a reactive test

The genuine, well-documented gap is not uptake but **linkage to confirmatory testing and
care** after a reactive self-test. Because HIVST is unsupervised, the post-test cascade
(confirmation, ART initiation) depends on active linkage support, and WHO's guidance
emphasises "Connection" as one of its 5 Cs precisely for this reason. The v1 draft's
specific modality-stratified linkage percentages (facility ~75%, secondary ~45%) are not
traceable to a verified source and are not asserted here; the qualitative point — that
reach-maximising modalities may trade off against linkage, making supported linkage a
necessary co-component — is sound and is the correct policy emphasis.

### 3.4 GRADE

| Outcome | Certainty | Basis |
|---|---|---|
| HIVST increases testing uptake (men) | **MODERATE** | 3 RCTs, consistent, RR 2.12 |
| HIVST increases testing frequency (MSM) | **MODERATE** | 2 RCTs, rate ratio 1.88 |
| HIVST increases HIV-positive diagnoses | **LOW** | 2 RCTs, wide CI (0.37–10.76) |
| Modality ranking | **INSUFFICIENT** | no head-to-head/IPD evidence |
| No social harm | **MODERATE** | consistent across 5 RCTs |

## 4. Discussion

Stripped of unsourced numbers, the HIVST evidence tells a clear and genuinely important
story: offering people free, private self-test kits roughly **doubles** testing uptake and
frequency, surfaces more HIV-positive individuals, and does so without measurable social
harm. That is the basis for WHO's recommendation and it is not in doubt. The temptation —
to which the v1 draft succumbed — is to over-specify: to convert a robust "HIVST works"
into a false-precision "modality A beats modality B by this exact ratio." The current
randomised evidence cannot support that step, because the trials that establish the
overall effect largely share one modality and were not designed for head-to-head modality
contrasts. Reporting a rank order with invented risk ratios does not strengthen the case
for HIVST; it weakens the paper's credibility and, if believed, could misdirect programme
investment.

The honest research agenda is therefore twofold. First, the modality question should be
answered with the right design — head-to-head randomisation or a harmonised
individual-participant-data meta-analysis — not by narrative assignment of pooled RRs to
modalities. Second, and more urgently, the field's binding constraint is linkage, not
uptake: a self-test that doubles diagnosis but loses half of reactive testers before
confirmation and ART has a muted population effect. Reach-extending modalities such as
secondary/partner distribution are valuable precisely because they reach people who would
not otherwise test, but their value is realised only if paired with active linkage support.
That is the operationally decisive trade-off, and it is where implementation research and
investment should concentrate.

## 5. Limitations

The anchoring meta-analysis searched to June 2016; more recent trials (including
secondary-distribution and community trials post-2016) have expanded the evidence and could
be incorporated in a full update — this v2 deliberately does not assert their specific
estimates without verification. The pooled effects are predominantly among men and MSM;
generalisation to adolescent girls and young women and to other priority populations is not
established by the anchored review. The withdrawal of the v1 modality figures leaves the
modality question open rather than answered — which is the truthful state of the evidence.

## 6. Conclusion

HIV self-testing substantially and reliably increases testing uptake (RR 2.12) and
frequency (rate ratio 1.88) without social harm, supporting its use as an additional
testing approach. The claim that delivery modalities differ in effectiveness by a fixed
rank order is **not supported** by the current randomised evidence and was withdrawn from
this version along with a mis-cited trial reference. The decisive implementation priority
is linkage to confirmatory care after a reactive self-test, especially for reach-extending
modalities such as secondary distribution.

---

## References

1. Johnson CC, Kennedy C, Fonner V, et al. Examining the effects of HIV self-testing compared to standard HIV testing services: a systematic review and meta-analysis. *J Int AIDS Soc.* 2017;20(1):21594. PMID: 28530049. doi:10.7448/IAS.20.1.21594.
2. World Health Organization. *Guidelines on HIV Self-Testing and Partner Notification: Supplement to Consolidated Guidelines on HIV Testing Services.* Geneva: WHO; 2016.
3. World Health Organization. *Consolidated Guidelines on HIV Testing Services* (5 Cs: Consent, Confidentiality, Counselling, Correct results, Connection). Geneva: WHO; 2019.

---

*Data-integrity note.* The anchoring meta-analysis (Johnson 2017, PMID 28530049) and its
pooled estimates — uptake RR 2.12 (1.51–2.98), frequency rate ratio 1.88 (1.17–3.01), mean
difference 2.13, HIV-positive-diagnosis RR 2.02 (0.37–10.76), no social harm — were verified
by PubMed metadata + abstract match on 2026-07-04. The v1 draft's abstract placeholders,
its unsourced modality risk ratios (2.15/2.05/1.76/1.35) and linkage percentages
(75%/45%), and a wrong trial PMID (28926628, actually a Raman-spectroscopy diabetes paper)
were **removed**, not carried forward. Individual STAR-era RCTs (Choko, Ortblad,
Thirumurthy) are referenced by name; their exact PMIDs should be re-verified before
inclusion in a full evidence-update table. **Build target:** `.docx` via the E156 host build
(`outputs/journal-upgrades/build/95-hiv-self-testing-v2/`); render the verified-effects
table (§3.1).
