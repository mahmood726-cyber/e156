# Fragility Synthesis: Independently Recomputed Fragility Indices Across Landmark Cardiovascular Trials

**Published (base article):** Synthēsis · View/13
**Authors:** [Student first author]; Mahmood Ahmad (middle author).
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `13-fragility-synth-verify.py` (deterministic; scipy)
**Evidence tier:** HIGH for the computed landmark FIs (verified 2×2 tables); corpus medians are cited context.
**Standard:** Walsh 2014 Fisher-exact FI · reproduce-from-source · internal-consistency validation.

---

## Upgrade note (what changed from v1)

v1 reported Fragility Index (FI) values for landmark trials but did not ship a
computation that a reader could run. v2 **independently recomputes every landmark FI
from the PubMed-verified 2×2 event tables** using an iterative two-sided Fisher-exact
procedure, and passes an internal-consistency check against two values this
journal-upgrade program computed independently elsewhere: **DAPA-HF FI = 62** (verified
in the SGLT2-HF fragility work) and **PLATO FI = 73** (verified in Synthēsis paper 27).
Both reproduce exactly, and v1's EMPEROR-Reduced (50) and PARADIGM-HF (118) values are
confirmed. The corpus-level medians remain cited from published analyses and are clearly
labelled as *not* recomputed here — the distinction between what this paper computes and
what it cites is now explicit.

---

## Abstract

**Background.** The Fragility Index (FI) — the minimum number of events that, added to the
fewer-event arm, would render a significant trial non-significant — measures how much a
result depends on a handful of events. The statistical fragility of the cardiovascular
guideline evidence base has not been characterised with fully reproducible computation.

**Methods.** We recomputed FI and the Fragility Quotient (FQ = FI/N) for four landmark
cardiovascular RCTs from their verified primary-endpoint 2×2 tables using iterative
two-sided Fisher-exact testing (Walsh 2014 definition), validated against two
independently-computed reference values, and juxtaposed the results with corpus-level
medians from published sub-domain analyses. Deterministic script.

**Results.** Landmark composite-endpoint FIs were **DAPA-HF 62**, **EMPEROR-Reduced 50**,
**PARADIGM-HF 118**, and **PLATO 73**, with FQ of **0.0039–0.0140**. The internal check
reproduced DAPA-HF (62) and PLATO (73) exactly. These robust FIs contrast sharply with
published corpus medians — revascularisation ~8, acute coronary syndrome ~12, general
cardiovascular ~13, antithrombotic ~24.5 — where a large minority of guideline-supporting
trials have FI < 10, often below the number of patients lost to follow-up.

**Conclusion.** Mega-trial composite endpoints are robust in absolute FI terms, but their
FQ is minuscule (0.4–1.4%): robustness is purchased with enormous sample size, not wide
margins. At the corpus level and for mortality-specific endpoints, cardiovascular evidence
is frequently fragile. An FI < 10 should trigger a GRADE imprecision flag for Class I
recommendations, and pre-specified FI targets belong in trial design.

---

## 1. Introduction

The p-value conflates effect size, precision, and sample size into a single number, and a
statistically significant result can still hinge on a few events. Walsh and colleagues
(2014) formalised this with the Fragility Index: the minimum number of patients in the
fewer-event arm whose outcome must flip from non-event to event to push a significant
two-sided Fisher-exact p-value above 0.05. The Fragility Quotient (FQ = FI/N) normalises
for trial size. Cardiovascular medicine is the ideal proving ground: its qualifying RCTs
are large and curated, its primary endpoints are hard binary outcomes, and its Class I
recommendations drive care for hundreds of millions. This paper's contribution is
methodological rigour — every landmark FI is recomputed from the source 2×2 table and
validated — paired with an honest juxtaposition against published corpus medians.

## 2. Methods

For each trial we extracted the primary-endpoint 2×2 table (events and N per arm) from the
PubMed-verified NEJM abstract. FI was computed by the Walsh 2014 procedure: identify the
fewer-event (typically treatment) arm; iteratively convert one non-event to an event in
that arm (holding N fixed), recomputing the two-sided Fisher-exact p at each step; FI is
the number of conversions at which p first exceeds 0.05. FQ = FI/N_total. The computation
(`13-fragility-synth-verify.py`) was validated against two reference FIs derived
independently elsewhere in this program (DAPA-HF, PLATO). Corpus-level medians are quoted
from published sub-domain analyses and are **not** recomputed.

## 3. Results

### 3.1 Recomputed landmark Fragility Indices (from verified 2×2 tables)

| Trial | PMID | Events treatment / N | Events control / N | Fisher p | **FI** | **FQ** |
|---|---|---|---|---|---|---|
| DAPA-HF | 31535829 | 386 / 2,373 | 502 / 2,371 | 1.6×10⁻⁵ | **62** | 0.0131 |
| EMPEROR-Reduced | 32865377 | 361 / 1,863 | 462 / 1,867 | 7.8×10⁻⁵ | **50** | 0.0134 |
| PARADIGM-HF | 25176015 | 914 / 4,187 | 1,117 / 4,212 | 5.8×10⁻⁷ | **118** | 0.0140 |
| PLATO | 19717846 | 864 / 9,333 | 1,014 / 9,291 | 1.8×10⁻⁴ | **73** | 0.0039 |

### 3.2 Internal-consistency validation

The computation reproduces two values derived independently earlier in this program:
**DAPA-HF FI = 62** (SGLT2-HF fragility work) and **PLATO FI = 73** (Synthēsis paper 27) —
both exact matches. This cross-check confirms the iterative Fisher-exact implementation is
correct and that the landmark FIs are reproducible from public data, not artefacts of a
particular software path.

### 3.3 The robustness–FQ paradox

All four composite-endpoint FIs are large in absolute terms (50–118), which reads as
"robust." But the FQ tells a subtler story: 0.0039–0.0140, i.e. flipping **0.4%–1.4%** of
randomised patients overturns the result. PLATO's FI of 73 looks impressive until one notes
it came from 18,624 patients (FQ 0.0039) — the robustness was bought with scale, not with a
wide safety margin per patient. This is the correct way to read mega-trial fragility: high
FI, tiny FQ.

### 3.4 Corpus medians — where fragility bites (cited, not recomputed)

| Domain | Median FI (published) |
|---|---|
| Myocardial revascularisation | ~8 |
| Acute coronary syndrome | ~12 |
| General cardiovascular | ~13 |
| ESC antithrombotic | ~24.5 |

At the corpus level the medians collapse toward single digits, and a large minority of
guideline-supporting trials have **FI < 10** — frequently **below the number of patients
lost to follow-up**, meaning the missing-data uncertainty alone could overturn the result.
Peripheral-arterial-disease trials are reported with median FI as low as ~2.5. Mortality-
specific endpoints (as opposed to composites) are systematically more fragile, because
deaths are rarer than the composite events that inflate mega-trial FIs.

### 3.5 GRADE mapping

| FI band | Interpretation | GRADE imprecision action |
|---|---|---|
| FI ≥ 20 | robust | no flag on FI grounds |
| 10 ≤ FI < 20 | moderate | consider flag if FI < LTFU |
| **FI < 10** | fragile | **imprecision flag for Class I claims** |
| FI < LTFU | missing data could overturn | downgrade |

## 4. Discussion

Recomputing the landmark fragility indices from source, rather than citing them, changes
the paper from an assertion into a demonstration — and the internal-consistency check
(DAPA-HF 62, PLATO 73 reproduced exactly) is the evidence that the computation is
trustworthy. The substantive finding is a two-tier evidence base. The mega-trials that
anchor modern cardiovascular guidelines (DAPA-HF, EMPEROR-Reduced, PARADIGM-HF, PLATO) are
robust in absolute FI (50–118); no plausible number of additional events overturns them.
But their FQ is minuscule (0.4–1.4%), a reminder that absolute FI scales with N and that
"robust" here means "large," not "wide-margin." Below this mega-trial stratum, the corpus
medians fall to single digits, a substantial fraction of guideline-supporting trials have
FI < 10, and the FI frequently falls below the number lost to follow-up — the point at
which missing data alone could reverse the conclusion.

The practical implications are concrete. First, GRADE imprecision assessment should
incorporate FI explicitly: an FI < 10 supporting a Class I recommendation is a red flag
that a p-value alone conceals, and an FI below the loss-to-follow-up count should trigger a
downgrade regardless of the p-value. Second, mortality endpoints deserve their own FI
reporting: a trial can have a robust composite FI and a fragile mortality FI, and conflating
them overstates the certainty of the survival claim — a distinction that matters most
precisely where it is most consequential. Third, trialists should pre-specify FI targets
alongside power calculations, so that a trial is designed to be robust, not merely
significant.

The honest scope of this paper is worth stating: what it *computes* are four landmark FIs,
verified and reproducible; what it *cites* are the corpus medians from published sub-domain
analyses. Keeping that boundary explicit is itself part of the fragility discipline — the
same discipline that asks how much a conclusion depends on a small number of events asks
also how much a review depends on numbers it did not itself verify.

## 5. Limitations

Four landmark trials are illustrative, not a systematic sample; the corpus medians are
quoted from published analyses whose specific source citations should be re-verified before
inclusion in a formal evidence table, and are not recomputed here. The FI is defined for
binary endpoints with two-sided Fisher-exact testing and does not directly apply to
time-to-event analyses (though the primary composites here are commonly reported as counts,
enabling the computation). Mortality-specific FIs were not recomputed for want of verified
CV-death 2×2 tables in the abstracts and are discussed qualitatively. The GRADE FI-band
mapping is a reasoned proposal, not a validated instrument.

## 6. Conclusion

Independently recomputed from verified 2×2 tables, the landmark cardiovascular composite
FIs are DAPA-HF 62, EMPEROR-Reduced 50, PARADIGM-HF 118, and PLATO 73 (FQ 0.004–0.014),
reproducing this program's prior DAPA-HF (62) and PLATO (73) values exactly. Mega-trial
composites are robust in absolute FI but tiny in FQ, while corpus medians (~8–24.5) and
mortality endpoints are frequently fragile. FI < 10 should flag GRADE imprecision for Class
I recommendations, and pre-specified FI targets should enter cardiovascular trial design.

---

## References

1. Walsh M, Srinathan SK, McAuley DF, et al. The statistical significance of randomized controlled trial results is frequently fragile: a case for a Fragility Index. *J Clin Epidemiol.* 2014;67(6):622–628. PMID: 24508144. [PMID to re-confirm at copy-edit]
2. McMurray JJV, Solomon SD, Inzucchi SE, et al. Dapagliflozin in patients with heart failure and reduced ejection fraction (DAPA-HF). *N Engl J Med.* 2019;381(21):1995–2008. PMID: 31535829. doi:10.1056/NEJMoa1911303.
3. Packer M, Anker SD, Butler J, et al. Cardiovascular and renal outcomes with empagliflozin in heart failure (EMPEROR-Reduced). *N Engl J Med.* 2020;383(15):1413–1424. PMID: 32865377. doi:10.1056/NEJMoa2022190.
4. McMurray JJV, Packer M, Desai AS, et al. Angiotensin–neprilysin inhibition versus enalapril in heart failure (PARADIGM-HF). *N Engl J Med.* 2014;371(11):993–1004. PMID: 25176015. doi:10.1056/NEJMoa1409077.
5. Wallentin L, Becker RC, Budaj A, et al. Ticagrelor versus clopidogrel in patients with acute coronary syndromes (PLATO). *N Engl J Med.* 2009;361(11):1045–1057. PMID: 19717846. doi:10.1056/NEJMoa0904327.

---

*Data-integrity note.* The four primary-endpoint 2×2 tables (PMIDs 31535829, 32865377,
25176015, 19717846) were verified by PubMed abstract match on 2026-07-04; PLATO's raw
counts were additionally verified in Synthēsis paper 27. FI/FQ are computed by
`13-fragility-synth-verify.py`, which reproduces DAPA-HF FI = 62 and PLATO FI = 73 exactly
as an internal-consistency check. Corpus-level medians (revascularisation ~8, ACS ~12,
general CV ~13, antithrombotic ~24.5, PAD ~2.5) are quoted from published sub-domain
analyses and are **not** recomputed; their specific source citations should be re-verified
before a formal table. The Walsh 2014 FI-definition PMID (24508144) is flagged for
copy-edit confirmation. **Build target:** `.docx` + figures via the E156 host build
(`outputs/journal-upgrades/build/13-fragility-synth-v2/`); render the FI-vs-FQ scatter
(§3.3) and the corpus-median bar chart (§3.4).
