# Breast Cancer Trial Disparities in Africa: Rising Burden, Falling-Behind Trial Share
## World-Class Advanced Version (v2) — Draft for Author Dictation

**Published:** Synthēsis · View/61
**Authors:** [Student first author], Mahmood Ahmad (middle author; software / data curation / formal analysis), [Faculty senior author]
**This draft:** ~1,500 words · Category C→B advance (verified registry + literature)
**Provenance:** trial counts from `_africa_equity_verify.py` (AACT April-12-2026,
579,828 studies; 25,125 African-site = 4.33% baseline). Burden/biology figures
cited to PubMed-verified sources.

> **v2 integrity note.** A PubMed audit found **all 11 of v1's PMIDs were wrong**
> (pointing to an immune-system paper, a hydrogel-micropatterning paper, an
> Alzheimer's-mouse exercise paper, a fluid-dynamics paper, etc.), with several
> citations unlocatable/fabricated and one PMID reused within the paper for two
> different claims. v2 rebuilds the reference list from re-verified sources only.

---

## Abstract

**Background:** Breast cancer is now the most commonly diagnosed cancer in women
worldwide, with rising incidence and disproportionately poor survival in
sub-Saharan Africa (SSA). We quantified Africa's share of breast-cancer trial
activity against a full-registry baseline.

**Methods:** AACT April-12-2026 full-registry analysis. Breast-cancer trials were
counted globally and by African site (≥1 facility in the 54 AU states); the
within-disease African share was benchmarked to the 4.33% all-disease African-site
rate. Burden/biology figures were taken from PubMed-verified sources.

**Results:** 14,432 global breast-cancer trials; **375 (2.60%) include an African
site** (11,256 interventional; 297 African = 2.64%) — *below* the 4.33% all-disease
baseline. This under-representation coincides with a large and growing SSA burden
(breast cancer is a leading female cancer globally [1,2]), later-stage
presentation in SSA cohorts [3], a higher proportion of aggressive
triple-negative/basal biology in women of African ancestry [4,7], and limited
management infrastructure [6].

**Conclusion:** Breast cancer's African trial share (2.6%) is below the low
all-disease baseline, even as incidence rises and SSA outcomes lag. The evidence
guiding breast-cancer care is generated overwhelmingly outside the region where
survival is worst and biology may differ.

---

## 1. Introduction

Breast cancer is the most frequently diagnosed cancer in women globally and among
the leading causes of female cancer death [1,2]. In sub-Saharan Africa the burden
is rising, presentation is frequently at later stage [3], and survival is
substantially worse than in high-income settings [6]. There is also a biological
dimension: women of African ancestry have a higher proportion of aggressive
triple-negative/basal-like tumours [4,7], which respond differently to therapy
and for which trial evidence in African populations is limited. We ask whether
African breast-cancer trial activity matches the African burden, using a
full-registry denominator.

---

## 2. Methods

**Data.** AACT April-12-2026 flat-file snapshot; records reassembled by start
signature before field splitting.
**Trials.** `conditions.downcase_name` matching breast cancer / breast carcinoma /
breast neoplasm / breast tumour (distinct nct_ids; "male breast" excluded).
**African-site trial.** ≥1 `facilities.country` among the 54 AU states
(registry-wide 25,125 = 4.33%).
**Metric.** Within-disease African share vs the 4.33% baseline.
**Burden/biology figures.** From verified sources [1–7]; not re-derived.

---

## 3. Results

### 3.1 African share of breast-cancer trials (AACT 2026-04-12)

| Metric | Global | African-site | African share |
|---|---|---|---|
| All breast-cancer trials | 14,432 | 375 | **2.60%** |
| Interventional only | 11,256 | 297 | 2.64% |
| Registry baseline (all diseases) | 579,828 | 25,125 | 4.33% |

Breast cancer has one of the largest disease-specific trial enterprises in the
registry (14,432 trials) — yet its African trial share (2.60%) is **below** the
4.33% all-disease baseline. Africa is under-represented in breast-cancer trials
even relative to its already-low overall trial participation.

### 3.2 Burden and biology context (verified literature)

| Quantity | Value / statement | Source |
|---|---|---|
| Global rank of breast cancer among female cancers | leading diagnosed female cancer | Sung 2021 [1]; Ferlay 2021 [2] |
| Stage at diagnosis in SSA | later-stage than HIC (documented across SSA) | Jedy-Agba 2016 [3] |
| Tumour biology, African ancestry | higher triple-negative/basal proportion | Adisa 2012 [4]; O'Brien 2010 [7] |
| Management capacity in Africa | limited; treatment-access gaps | Pace 2016 [5]; Vanderpuye 2017 [6] |

The convergence — rising incidence, later-stage presentation, more aggressive
biology, limited treatment capacity, and *below-baseline* trial siting — defines
a compounding disadvantage: the population with the worst breast-cancer outcomes
is the least studied.

---

## 4. Discussion

Breast cancer is the mirror image of the "no trials at all" neglect story: the
global enterprise is enormous (14,432 trials), so the African deficit is purely
distributional and, unlike cervical cancer, falls *below* the all-disease
baseline. Three features make this especially consequential. First, **biology**:
the higher prevalence of triple-negative disease in women of African ancestry
[4,7] means efficacy and toxicity findings from predominantly non-African,
hormone-receptor-positive-enriched trial populations may not transfer. Second,
**stage and access**: later-stage presentation [3] and constrained treatment
capacity [5,6] change which interventions are even relevant — early-detection
strategies, stage-appropriate protocols, and affordable regimens need African
evidence. Third, **scale of the missed opportunity**: with 14,432 trials
worldwide, raising the African share merely to the 4.33% baseline would roughly
double African breast-cancer trial participation.

The actionable agenda mirrors other African-oncology priorities: African-sited
trials of early detection and downstaging, treatment protocols validated in
triple-negative-enriched African populations, and pragmatic studies of
affordable, deliverable regimens within existing capacity [5,6]. The registry
signal — 2.6% African siting for a disease of rising African burden — is a clear
call for that investment.

---

## 5. Limitations

Registry counts undercount trials registered only on non-ClinicalTrials.gov
registries. Keyword matching may miss trials coding breast cancer as a secondary
condition. African-site counting credits any trial with ≥1 African facility,
over-crediting large multinational trials that enrol few African participants; the
participant-weighted African share is likely lower still. Biology and burden
statements are supported by the cited literature but the trial-share analysis
itself does not measure participant ancestry or stage.

---

## 6. Conclusion

Of 14,432 global breast-cancer trials, only 375 (2.60%) include an African site —
below the 4.33% all-disease baseline — even as breast-cancer incidence rises in
sub-Saharan Africa, presentation is later-stage, tumour biology is more often
aggressive in women of African ancestry, and treatment capacity is limited. The
population with the worst outcomes is the least studied. Merely reaching the
baseline African share would roughly double African breast-cancer trial
participation; genuine equity requires African-sited trials matched to African
biology, stage, and capacity.

---

## References
*All PMIDs/DOIs re-verified against PubMed (title + journal + volume/pages match).
v1's 11 wrong PMIDs replaced; unlocatable citations dropped.*

1. Sung H, Ferlay J, Siegel RL, et al. Global cancer statistics 2020: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries. *CA Cancer J Clin.* 2021;71(3):209-249. PMID: 33538338. DOI: 10.3322/caac.21660
2. Ferlay J, Colombet M, Soerjomataram I, et al. Cancer statistics for the year 2020: an overview. *Int J Cancer.* 2021;149(4):778-789. PMID: 33818764. DOI: 10.1002/ijc.33588
3. Jedy-Agba E, McCormack V, Adebamowo C, dos-Santos-Silva I. Stage at diagnosis of breast cancer in sub-Saharan Africa: a systematic review and meta-analysis. *Lancet Glob Health.* 2016;4(12):e923-e935. PMID: 27855871. DOI: 10.1016/S2214-109X(16)30259-5
4. Adisa CA, Eleweke N, Alfred AAA, et al. Biology of breast cancer in Nigerian women: a pilot study. *Ann Afr Med.* 2012;11(3):169-175. PMID: 22684136. DOI: 10.4103/1596-3519.96880
5. Pace LE, Shulman LN. Breast cancer in sub-Saharan Africa: challenges and opportunities to reduce mortality. *Oncologist.* 2016;21(6):739-744. PMID: 27091419. DOI: 10.1634/theoncologist.2015-0429
6. Vanderpuye V, Grover S, Hammad N, et al. An update on the management of breast cancer in Africa. *Infect Agent Cancer.* 2017;12:13. PMID: 28228841. DOI: 10.1186/s13027-017-0124-y
7. O'Brien KM, Cole SR, Tse CK, et al. Intrinsic breast tumor subtypes, race, and long-term survival in the Carolina Breast Cancer Study. *Clin Cancer Res.* 2010;16(24):6100-6110. PMID: 21169259. DOI: 10.1158/1078-0432.CCR-10-1533
8. Bray F, Ferlay J, Soerjomataram I, et al. Global cancer statistics 2018: GLOBOCAN estimates. *CA Cancer J Clin.* 2018;68(6):394-424. PMID: 30207593. DOI: 10.3322/caac.21492

*Source: metadata retrieved from PubMed. All prior references were wrong/fabricated
and have been rebuilt from verified sources.*
