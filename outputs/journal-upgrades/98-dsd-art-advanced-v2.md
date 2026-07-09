# Differentiated Service Delivery for ART: A Truth-First Synthesis Anchored on RCT-Only Meta-Analyses
## World-Class Advanced Version (v2) — Draft for Author Review

**Published:** Synthēsis Vol. 2 No. 4 (2026) · View/98
**Authors:** Christine Muhumuza et al. · Mahmood Ahmad (middle author; verification / software / data curation)
**Original body:** ~300 words · v1 advanced draft: ~1,000 words (placeholder-laden)
**This draft:** ~1,700 words
**Companion verification script:** `98-dsd-art-verify.py` (deterministic; stdlib)
**Evidence base:** two independent RCT-only meta-analyses (not observational, as v1 assumed)

> **Reproduce-or-remove upgrade note (major rebuild).** The v1 advanced draft was
> not verifiable: its PRISMA counts, per-model subgroup table, retention CIs and
> patient-satisfaction SMD were all **placeholders or fabrications** ([n], [x],
> [author required] throughout; a four-row "CAG/MMS/CDDP/FFT" table with no study
> data), and its reference list was unreliable — several citations' volume/DOI
> coordinates point to **entirely different papers** (e.g. the cited *J Int AIDS
> Soc* 24:e25665 is a men's HIV-testing RCT, not Pasipamire; 23:e25474 is an
> adolescent viral-load cohort, not Cassidy; 24:e25730 is a drug-users policy
> essay, not Wilkinson). Rather than polish unverifiable content, this version is
> **rebuilt from scratch** on two PubMed-verified **RCT-only** meta-analyses
> (Bwire 2023; Nega 2026). Three v1 claims are corrected: **(1)** the fabricated
> per-model subgroups and satisfaction SMD are **removed**; **(2)** the evidence
> base is **RCT-based, not "predominantly observational, VERY LOW"** — a material
> upgrade to the starting certainty; **(3)** the v1's uniformly low I² is replaced
> by the **real, model-dependent heterogeneity** (I² up to 84–90% within single
> models). Only PMIDs whose title/journal/pages matched on 2026-07-09 are cited.

---

## Abstract

**Background.** Differentiated service delivery (DSD) for antiretroviral therapy
(ART) tailors care intensity to clinically stable patients — community ART groups,
adherence clubs, multi-month dispensing, and community pickup points. We synthesise
the strongest available evidence (randomised trials) on whether DSD preserves viral
suppression and improves retention versus standard facility care.

**Methods.** Truth-first synthesis anchored on two independent RCT-only
meta-analyses in sub-Saharan Africa: Bwire 2023 (16 RCTs, 13,886 participants) and
Nega 2026. Estimates are taken verbatim from the published reports and cross-checked
by a deterministic script that (i) tests non-inferiority against a 0.95 margin,
(ii) re-expresses Nega's non-suppression estimate on the suppression side to test
concordance with Bwire (without pooling overlapping trials), and (iii) frames the
verified retention benefit in absolute terms with a stated baseline. GRADE for RCT
evidence.

**Results.** Across 16 RCTs, any DSD model versus standard care gave **viral
suppression RR 1.01 (95% CI 1.00–1.02, I²=0%)** and **retention RR 1.09 (1.08–1.11,
I²=0%)** (Bwire 2023). The independent Nega 2026 MA concurred: viral non-suppression
RR 0.89 (0.74–1.07) — implying a suppression-side RR ≈1.01–1.02 across plausible
baselines. Non-inferiority on suppression is met (lower CI ≥0.95). The retention
benefit corresponds to an absolute gain of ~7 percentage points (NNT ≈14 at 80%
baseline). Crucially, heterogeneity is **model- and setting-dependent**: single-model
pools reach I²=77–84% (adherence clubs; Bwire) and I²=90% (non-retention; Nega),
so the tight any-DSD pool must not be read as uniformity.

**Conclusion.** RCT evidence supports DSD scale-up for stable ART patients: viral
suppression is preserved and retention improves on average. But the benefit is not
uniform across models or settings, and program-level results can vary widely —
a nuance the original draft's fabricated low-heterogeneity table obscured.

---

## 1. Introduction

DSD was developed on the premise that stable, virologically-suppressed patients do
not need the clinical contact intensity of newly-initiated or unstable patients.
Conventional ART imposes monthly/quarterly facility visits with substantial
transport cost, lost income, and disclosure risk. Four models operate at scale:
community ART groups (CAG), adherence clubs, multi-month dispensing (MMS), and
community drug distribution points (CDDP). The policy question is whether reduced
facility contact preserves clinical outcomes. This synthesis answers it from
randomised evidence — the appropriate tier, and (contrary to the v1 draft's
assumption) the tier that actually exists for this question.

## 2. Methods

**Design.** Truth-first evidence synthesis. Because two RCT-only meta-analyses now
exist, we anchor on them rather than re-extract primary trials (which risks
introducing the very citation errors that plagued v1). Both were verified against
PubMed metadata:

- **Bwire 2023** (*Rev Med Virol* 33(6):e2479; PMID 37655428; PROSPERO
  CRD42023418988): 1,596 records screened → **16 RCTs, 13,886 participants**,
  adults and children, sub-Saharan Africa; random-effects RRs.
- **Nega 2026** (*AIDS Res Ther* 23(1):21; PMID 41582132): independent RCT-only MA
  of stable PLWH in Africa; Cochrane RoB 2; Cochran Q / forest-plot heterogeneity.

**Analysis (companion script).** (1) Non-inferiority of viral suppression against a
prespecified RR margin of 0.95. (2) Cross-MA concordance: Nega reports *non*-
suppression, so we re-express it on the suppression side across a baseline
sensitivity band (8–16% non-suppression) and compare with Bwire — **without pooling**
the two MAs, since they share included trials and pooling would double-count.
(3) Absolute retention benefit (NNT) at stated baselines. GRADE for RCT evidence
(start HIGH; downgrade for heterogeneity, indirectness, imprecision as warranted).

## 3. Results

### 3.1 Viral suppression: non-inferior, concordant across two MAs

Any DSD model versus standard care preserved viral suppression: **RR 1.01 (95% CI
1.00–1.02), I²=0%** across 16 RCTs (Bwire 2023). The lower confidence bound (1.00)
exceeds the 0.95 non-inferiority margin and touches the line of equivalence, so DSD
is at least non-inferior, with a point estimate marginally favouring DSD.

The independent Nega 2026 MA corroborates this. It reports viral **non**-suppression
RR 0.89 (0.74–1.07); re-expressed on the suppression side across plausible baseline
non-suppression risks (8%, 12%, 16%), the implied suppression RR is **1.01–1.02**
(companion script) — directly concordant with Bwire. Two independently conducted
RCT-only meta-analyses thus agree that DSD does not compromise viral suppression.
(Because their trial sets overlap, this is reported as corroboration, not a pooled
super-estimate.)

### 3.2 Retention: better on average, ~7 points absolute

Any DSD model improved retention in care: **RR 1.09 (95% CI 1.08–1.11), I²=0%**
(Bwire 2023). Framed absolutely (companion script): against a standard-care 12-month
retention of 80%, DSD retention is ~87% — an absolute gain of **7.2 percentage
points, NNT ≈14** to keep one additional patient in care per year; the gain is 6.8pp
(NNT 15) at a 75% baseline and 7.7pp (NNT 13) at 85%. Over a multi-year programme
horizon this compounds into materially fewer patients lost to follow-up.

### 3.3 Heterogeneity is real and model-dependent (the v1's key distortion)

The tight any-DSD pools (I²=0%) must not be mistaken for uniformity. When Bwire
restricts to a *single* model — adherence clubs — heterogeneity is high: retention
RR 1.01 (0.96–1.07, **I²=84%**) and suppression RR 1.02 (0.98–1.07, **I²=77%**).
Nega's non-retention pool reaches **I²=90%** with a CI of 0.68–1.57 that spans both
substantial benefit and substantial harm. The honest reading: the *average* DSD
effect is favourable and precisely estimated, but *which* model in *which* setting
delivers that average varies widely. The v1 draft's fabricated per-model table
(CAG 1.00, MMS 1.03, CDDP 1.02, FFT 1.00, all "I²=14%") invented a false uniformity;
it is removed.

### 3.4 GRADE

| Outcome | Certainty | Rationale |
|---------|-----------|-----------|
| Viral suppression (non-inferiority) | **HIGH** | 16 RCTs, I²=0% for any-DSD pool, concordant across two MAs, direct outcome |
| Retention in care | **MODERATE** | RCT evidence, large tight any-DSD effect; downgraded once for **model-level heterogeneity** (single-model I² up to 90%) |
| Patient satisfaction | **not assessed** | v1's SMD 0.42 had no verifiable source; **removed** rather than reported |

This is a substantive re-grading: the v1 started from "predominantly observational →
VERY LOW/MODERATE." The evidence is in fact RCT-based, so suppression reaches HIGH
certainty. Retention is held at MODERATE by genuine between-model heterogeneity, not
by observational bias.

## 4. Discussion

The randomised evidence delivers a clear, defensible message: for clinically stable
patients, DSD preserves viral suppression (HIGH certainty, two concordant RCT MAs)
and improves retention (MODERATE certainty, ~7 absolute points). The mechanism is
plausible — fewer facility visits lower the opportunity cost of staying in care —
and the direction is consistent across model families.

The important refinement over the original draft is honesty about heterogeneity.
"DSD works on average" and "every DSD model works everywhere" are different claims;
only the first is supported. Single-model pools with I² near 80–90% mean that a
programme adopting one model in one health system cannot assume the pooled average
will reproduce locally. This argues for **local monitoring of retention and
suppression during scale-up**, not blanket extrapolation — precisely the
implementation-science posture the DSD field has adopted. Head-to-head randomised
comparisons *between* DSD models remain scarce and are the key evidence gap.

## 5. Limitations

Both anchor MAs pool trials of differing models, durations, and populations
(adults and children), so their any-DSD estimates average over real clinical
heterogeneity. The two MAs share included trials, so they are treated as
corroborating, not independent, and are not pooled. Retention definitions and
ascertainment differ across trials, and active follow-up in some DSD models could
inflate measured retention relative to passive standard-care follow-up. The absolute
NNT depends on the assumed baseline retention, which is stated explicitly and varied.
Patient-satisfaction and per-model effects claimed in v1 are not reported here
because no verifiable source underpins them.

## 6. Conclusion

Randomised evidence supports DSD scale-up for stable ART patients: viral suppression
is preserved (RR 1.01, 95% CI 1.00–1.02, I²=0%; concordant across two RCT-only MAs)
and retention improves (RR 1.09, 1.08–1.11; ~7 absolute points, NNT ≈14). The
benefit is real but model- and setting-dependent (single-model I² up to 90%), so
scale-up should be paired with local outcome monitoring rather than assumed uniform.

## 7. References (PMIDs verified against PubMed on 2026-07-09)

1. Bwire GM, Njiro BJ, Ndumwa HP, et al. Impact of differentiated service delivery models on retention in HIV care and viral suppression among people living with HIV in sub-Saharan Africa: a systematic review and meta-analysis of randomised controlled trials. *Rev Med Virol.* 2023;33(6):e2479. **PMID 37655428.**
2. Nega AD, Asemahagn MA, Getahun FA. Effectiveness of differentiated antiretroviral therapy delivery models for stable persons living with HIV in Africa: a systematic review and meta-analysis. *AIDS Res Ther.* 2026;23(1):21. **PMID 41582132.**
3. Grimsrud A, Bygrave H, Doherty M, et al. Reimagining HIV service delivery: the role of differentiated care from prevention to suppression. *J Int AIDS Soc.* 2016;19(1):21484. **PMID 27914186.**
4. Grimsrud A, Sharp J, Kalombo C, Bekker LG, Myer L. Implementation of community-based adherence clubs for stable antiretroviral therapy patients in Cape Town, South Africa. *J Int AIDS Soc.* 2015;18(1):19984. **PMID 26022654.**
5. Guyatt GH, Oxman AD, Schünemann HJ, Tugwell P, Knottnerus A. GRADE guidelines: a new series of articles in the Journal of Clinical Epidemiology. *J Clin Epidemiol.* 2011;64(4):380-382. **PMID 21185693.**
6. World Health Organization. *Consolidated Guidelines on HIV Prevention, Testing, Treatment, Service Delivery and Monitoring.* Geneva: WHO; 2021. (DSD service-delivery recommendations.)

**Removed from v1 (reproduce-or-remove):** the placeholder PRISMA counts and the
fabricated per-model subgroup table (no study data); the patient-satisfaction SMD
0.42 (no verifiable source); and citations whose stated coordinates point to
unrelated papers — v1 refs for Pasipamire (24:e25665 = a men's HIV-testing RCT),
Cassidy (23:e25474 = an adolescent viral-load cohort), Wilkinson (24:e25730 = a
drug-users policy essay), Decroo, Mukumbang, Geng, and Ehrenkranz — which could not
be reliably re-anchored and are dropped in favour of the verified MAs above.

---

*DRAFT for author review — not for live publication without sign-off. All numerals
regenerated by `98-dsd-art-verify.py`. According to PubMed metadata, every retained
PMID was verified by title/journal/pages match on 2026-07-09. Anchor estimates are
quoted verbatim from Bwire 2023 and Nega 2026; the two MAs are not pooled.*
