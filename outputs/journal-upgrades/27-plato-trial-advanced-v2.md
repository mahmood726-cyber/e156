# The PLATO Trial — Was It Too Good to Be True? Exact Fragility and the Geographic Reversal
## World-Class Advanced Version (v2) — Draft for Author Dictation

**Published:** Synthēsis · View/27
**Authors:** [Student first author], Mahmood Ahmad (middle author; software / formal analysis), [Faculty senior author]
**Original body:** ~300 words / v1 advanced ~1,000 w
**This draft:** ~1,600 words · Category B advance
**Provenance:** the Fragility Index is computed exactly by the companion script
`27-plato-fragility-verify.py` (deterministic, two-sided Fisher exact, scipy).
Re-run to reproduce FI = 73.

> **v2 upgrade over v1.** v1 left the Fragility Index ("~70"), NNT, geographic
> p-interaction, and aspirin-dose figures as chi-square estimates or
> "[author required]" placeholders. v2 (a) computes the **exact** FI by two-sided
> Fisher exact test (FI = 73, FQ 0.39%), (b) replaces the guessed subgroup
> numbers with the **verified** figures from the Mahaffey 2011 geographic paper
> [3], and (c) corrects a factual error: the *region* interaction (p=0.045) was
> a **prespecified** subgroup analysis, not post-hoc — it was the *aspirin-dose*
> explanation that was explored post-hoc. All 9 references were PubMed-verified;
> 3 wrong v1 PMIDs (a cardiac-arrest paper, an Artemisia-allergy paper, and an
> organic-chemistry paper) were corrected or removed.

---

## Abstract

**Background:** PLATO (2009, n=18,624) found ticagrelor superior to clopidogrel
for the composite of cardiovascular death, myocardial infarction, or stroke in
acute coronary syndromes (HR 0.84, 95% CI 0.77–0.92, P<0.001) [2]. Two questions
recur: how statistically robust is the primary result, and how should the North
American subgroup reversal be interpreted?

**Methods:** We computed the exact Fragility Index (FI) of PLATO's primary
composite by two-sided Fisher exact test on the published crude event counts
(ticagrelor 864/9,333; clopidogrel 1,014/9,291), modifying a single arm (Walsh
method [4]). Geographic and aspirin-dose findings were taken from the verified
prespecified regional analysis [3].

**Results:** Baseline two-sided Fisher exact P = 1.8×10⁻⁴. **FI = 73** (adding 73
events to the ticagrelor arm raises P to 0.053); Fragility Quotient = 73/18,624 =
**0.39%**. A cross-check removing events from the clopidogrel arm gives FI = 75.
NNT (12-month crude event proportions) = 60. The prespecified region interaction
was P=0.045; the North American subgroup (~10% of patients) showed a directional
reversal (published HR 1.25). Mahaffey et al. [3] reported that a numerically
pro-clopidogrel result in ≥1 of 4 prespecified regions could arise by chance with
32% probability, and that of 37 factors examined only aspirin dose explained a
substantial fraction of the interaction: ≥300 mg/day maintenance aspirin was
taken by 53.6% of US vs 1.7% of rest-of-world patients, and in low-dose-aspirin
patients ticagrelor was superior.

**Conclusion:** PLATO's primary result is statistically robust (FI = 73 ≫ 10 —
well above the GRADE-imprecision and lost-to-follow-up thresholds). The North
American reversal is most parsimoniously explained by a combination of chance
(inevitable across four prespecified regions) and a genuine aspirin-dose
interaction, now encoded in the ticagrelor label's ≤100 mg/day aspirin
recommendation. "Too good to be true" is not supported for the global estimate.

---

## 1. Introduction

PLATO randomised 18,624 ACS patients to ticagrelor (180 mg load, 90 mg bid) or
clopidogrel (300–600 mg load, 75 mg daily) [2]. The 12-month primary composite
(CV death/MI/stroke) occurred in a Kaplan–Meier-estimated 9.8% vs 11.7% (HR 0.84,
P<0.001), a major advance over clopidogrel, the standard since CURE [1]. Two
durable concerns attach to the trial: the robustness of a result that reshaped
guidelines, and the North American subgroup, where the effect direction reversed.
The US FDA review flagged the geographic discrepancy and the possibility that
higher US aspirin maintenance doses blunted ticagrelor's benefit.

---

## 2. Methods

### 2.1 Fragility Index (exact)
The FI is the minimum number of patients in one arm whose status must change
(non-event→event) to render the 2×2 non-significant by a two-sided Fisher exact
test [4]. We used the published **crude** event counts — ticagrelor 864/9,333,
clopidogrel 1,014/9,291 — not the KM percentages (9.8%/11.7%), because the FI is
defined on the count table. Events were added to the ticagrelor arm (the arm with
fewer events, so adding events narrows the gap), holding its total fixed; only
one arm was modified. Fragility Quotient = FI ÷ total N. Computed in
`27-plato-fragility-verify.py` (scipy `fisher_exact`).

### 2.2 Geographic / aspirin figures
Taken from the prespecified regional analysis of Mahaffey et al., Circulation
2011 [3] (verified against source), not re-derived here (patient-level regional
data are not public).

---

## 3. Results

### 3.1 Fragility Index

| N | Ticagrelor events | Clopidogrel events | Fisher exact P | FI | FQ |
|---|---|---|---|---|---|
| 18,624 | 864 / 9,333 | 1,014 / 9,291 | 1.8×10⁻⁴ | **73** | **0.39%** |

Adding 73 events to the ticagrelor arm raises the two-sided Fisher P from
1.8×10⁻⁴ to 0.053 (first value ≥0.05). The reverse operation (removing events
from the clopidogrel arm) gives FI = 75 — consistent. The sample odds ratio
(0.833) matches the reported hazard ratio (0.84). By the Walsh benchmark (median
FI = 8 across high-impact RCTs [4]) and the Tignanelli observation that cardiac
and heart-failure RCTs are unusually robust [9], PLATO's FI of 73 places it among
the more robust large cardiovascular trials: it far exceeds the FI ≥ 10 informal
threshold below which GRADE imprecision or loss-to-follow-up could plausibly
overturn a result.

### 3.2 NNT
Using crude 12-month proportions (clopidogrel 10.91%, ticagrelor 9.26%): ARR =
1.66%, **NNT ≈ 60** to prevent one primary composite event over 12 months.

### 3.3 Geographic subgroup and aspirin dose (verified from [3])

The region-by-treatment interaction was **prespecified** and statistically
significant at P = 0.045, with a weaker ticagrelor effect in North America than
elsewhere; the North American subgroup HR was directionally reversed (published
HR ≈ 1.25). Mahaffey et al. [3] investigated this with two independent statistical
groups and reported:

- **Chance:** because a numerically pro-clopidogrel result in ≥1 of the 4
  prespecified regions could occur with **32% probability**, chance alone cannot
  be excluded.
- **Aspirin dose:** of 37 baseline/post-randomisation factors, **only aspirin
  maintenance dose** explained a substantial fraction of the interaction. A
  median maintenance aspirin dose **≥300 mg/day was taken by 53.6% of US patients
  vs 1.7% of rest-of-world patients.** In adjusted and landmark analyses, among
  low-dose-aspirin patients ticagrelor was superior (statistically so outside the
  US, similar within the US cohort).
- **Trial conduct:** systematic errors in trial conduct were ruled out.

*Correction to v1:* v1 described the geographic interaction as post-hoc. Per the
primary source it was a **prespecified** subgroup analysis; the aspirin-dose
*explanation* for it was the post-hoc exploration. This distinction matters for
how much weight the interaction carries.

---

## 4. Discussion

The two questions receive different answers. On **robustness**, PLATO's global
result is not fragile: FI = 73 means the significance survives any plausible
degree of outcome misclassification or differential loss to follow-up, and the
odds ratio reproduces the reported HR. The "too good to be true" framing is not
supported for the primary estimate; if anything, the result is unusually stable,
consistent with Tignanelli's observation that cardiovascular RCTs tend to be
robust [9].

On the **North American reversal**, the most defensible reading combines two
non-exclusive mechanisms. First, chance: across four prespecified regions, a
numerically adverse result in at least one is expected ~32% of the time even if
the true global effect holds — the multiplicity of subgroup contrasts inflates
the probability of an apparent reversal [10]. Second, a genuine, mechanistically
plausible aspirin-dose interaction: ticagrelor's adenosine-mediated and
COX-independent effects can be attenuated by high-dose aspirin, and the US–ROW
gap in ≥300 mg/day maintenance aspirin (53.6% vs 1.7%) is exactly the confounder
that would generate a regional signal. That aspirin dose alone, of 37 factors,
explained a substantial share of the interaction strengthens this reading.

The regulatory resolution encodes both caution and the mechanism: the ticagrelor
(Brilinta) label recommends maintenance aspirin ≤100 mg/day — a rare instance of
a subgroup-driven pharmacological hypothesis written into approved dosing. The
appropriate scientific posture is neither to dismiss the reversal nor to let it
overturn a robust global result, but to act on the tractable, plausible mechanism
(low-dose aspirin) it points to.

---

## 5. Limitations

The FI is computed on the crude primary-composite counts and does not incorporate
time-to-event/censoring structure (the trial's HR does); it is a robustness
descriptor, not a re-analysis of efficacy. Regional and aspirin-dose figures are
taken from the published prespecified analysis [3]; patient-level regional data
are not public, so those specific values are cited, not re-derived. Subgroup
interactions — even prespecified ones — have inflated type-I error and the
aspirin-dose explanation remains observational within the trial.

---

## 6. Conclusion

PLATO's primary result is statistically robust: exact Fragility Index = 73
(FQ 0.39%), far above thresholds at which imprecision or attrition could reverse
it, with NNT ≈ 60. The prespecified regional interaction (P=0.045) and the North
American directional reversal are most parsimoniously explained by chance across
four regions (≈32% probability of ≥1 adverse region) plus a plausible aspirin-dose
interaction (≥300 mg/day aspirin in 53.6% of US vs 1.7% of ROW patients), the
latter now reflected in the ≤100 mg/day aspirin label. The global conclusion
stands; the "too good to be true" concern is not supported.

---

## References
*All PMIDs/DOIs verified against PubMed (title + journal + volume/pages match).*

1. Yusuf S, Zhao F, Mehta SR, et al. Effects of clopidogrel in addition to aspirin in patients with acute coronary syndromes without ST-segment elevation (CURE). *N Engl J Med.* 2001;345(7):494-502. PMID: 11519503. DOI: 10.1056/NEJMoa010746
2. Wallentin L, Becker RC, Budaj A, et al. Ticagrelor versus clopidogrel in patients with acute coronary syndromes (PLATO). *N Engl J Med.* 2009;361(11):1045-1057. PMID: 19717846. DOI: 10.1056/NEJMoa0904327
3. Mahaffey KW, Wojdyla DM, Carroll K, et al. Ticagrelor compared with clopidogrel by geographic region in the Platelet Inhibition and Patient Outcomes (PLATO) trial. *Circulation.* 2011;124(5):544-554. PMID: 21709065. DOI: 10.1161/CIRCULATIONAHA.111.047498
4. Walsh M, Srinathan SK, McAuley DF, et al. The statistical significance of randomized controlled trial results is frequently fragile: a case for a Fragility Index. *J Clin Epidemiol.* 2014;67(6):622-628. PMID: 24508144. DOI: 10.1016/j.jclinepi.2013.10.019
5. Ibanez B, James S, Agewall S, et al. 2017 ESC Guidelines for the management of acute myocardial infarction in patients presenting with ST-segment elevation. *Eur Heart J.* 2018;39(2):119-177. PMID: 28886621. DOI: 10.1093/eurheartj/ehx393
6. Antman EM, Wiviott SD, Murphy SA, et al. Early and late benefits of prasugrel in patients with acute coronary syndromes undergoing PCI (TRITON-TIMI 38). *J Am Coll Cardiol.* 2008;51(21):2028-2033. PMID: 18498956. DOI: 10.1016/j.jacc.2008.04.002
7. Balshem H, Helfand M, Schünemann HJ, et al. GRADE guidelines: 3. Rating the quality of evidence. *J Clin Epidemiol.* 2011;64(4):401-406. PMID: 21208779. DOI: 10.1016/j.jclinepi.2010.07.015
8. Rothwell PM. Subgroup analysis in randomised controlled trials: importance, indications, and interpretation. *Lancet.* 2005;365(9454):176-186. PMID: 15639301. DOI: 10.1016/S0140-6736(05)17709-5
9. Tignanelli CJ, Napolitano LM. The Fragility Index in randomized clinical trials as a means of optimizing patient care. *JAMA Surg.* 2019;154(1):74-79. PMID: 30422256. DOI: 10.1001/jamasurg.2018.4318

*Source: metadata retrieved from PubMed. Removed/corrected from v1: Mahaffey PMID
(v1's 21747066 is a cardiac-arrest hypothermia paper → correct 21709065);
Montalescot "nonresponders" (v1's 16997791 is an Artemisia-allergy paper →
removed as tangential); Tignanelli PMID (v1's 30422145 is an organic-chemistry
paper → correct 30422256).*

---

*DRAFT for author dictation. FI regenerated by `27-plato-fragility-verify.py`
(FI=73, exact Fisher). Confidence: HIGH on FI/NNT (exact from published counts);
geographic/aspirin figures cited verbatim from the verified primary source [3].*
