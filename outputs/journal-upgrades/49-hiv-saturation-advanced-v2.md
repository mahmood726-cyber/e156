# The HIV Trial Saturation Index: HIV's Outsized Share of Africa's Clinical-Trial Portfolio
## World-Class Advanced Version (v2) — Draft for Author Dictation

**Published:** Synthēsis · View/49
**Authors:** [Student first author], Mahmood Ahmad (middle author; software / data curation / formal analysis), [Faculty senior author]
**This draft:** ~1,450 words · Category C→B advance (verified registry + literature)
**Provenance:** trial counts from `_africa_equity_verify.py` (AACT April-12-2026,
579,828 studies; 25,125 African-site = 4.33% baseline). Burden figures cited to
PubMed-verified sources.

> **v2 integrity note.** A PubMed audit found **all 11 of v1's PMIDs were wrong**
> (they pointed to a chitosan-chemistry paper, a gap-junction-protein paper, a
> grass-carp-steaming paper, a memory-reconsolidation paper, etc.), and 7 of the
> 11 cited references could not be located in PubMed at all — i.e. largely
> fabricated. v2 rebuilds the reference list from a small set of re-verified
> sources only. The quantitative core is the AACT-computed cross-disease African
> trial-share comparison.

---

## Abstract

**Background:** HIV/AIDS has been the dominant focus of clinical research in
sub-Saharan Africa (SSA) for two decades, driven by PEPFAR, the Global Fund, and
NIH investment. We quantified whether HIV is *over*-represented in Africa's
clinical-trial portfolio relative to other major diseases — a "saturation"
distinct from the neglect seen elsewhere.

**Methods:** AACT April-12-2026 full-registry analysis. For HIV and comparator
conditions we computed global trial count, African-site count (≥1 facility in the
54 AU states), and within-disease African share, benchmarked to the 4.33%
all-disease African-site baseline.

**Results:** 9,126 global HIV trials; **1,713 (18.77%) include an African site**
(7,404 interventional; 1,447 African = 19.54%) — **4.3× the 4.33% all-disease
baseline** and the highest African share of any disease examined. By contrast,
sickle cell disease (the most African monogenic disease) sits at 9.6%, cervical
cancer 5.2%, epilepsy 3.4%, and breast cancer 2.6%. HIV's African trial share is
2–7× that of these other high-burden conditions. HIV burden genuinely is
SSA-concentrated (the majority of people living with HIV are in SSA), and
landmark prevention evidence was generated there (HPTN 052 enrolled 54% of
subjects in Africa) [3].

**Conclusion:** HIV is not under-represented in African trials; it is by far the
most over-represented major disease, consistent with a research infrastructure
built around a single, well-funded epidemic. This "saturation" is a mirror image
of the neglect documented for sickle cell, cervical, breast, and epilepsy — and
raises the question of whether HIV-centric trial capacity can be leveraged for
other conditions.

---

## 1. Introduction

For two decades, the clinical-research infrastructure of sub-Saharan Africa has
been built substantially around HIV/AIDS, funded by PEPFAR, the Global Fund, and
NIH networks (HPTN, ACTG, IMPAACT). This concentration is defensible on burden
grounds — the majority of people living with HIV are in SSA — and it produced
landmark, practice-changing evidence generated on African soil, most notably HPTN
052, which established treatment-as-prevention and enrolled 54% of its subjects
in Africa [3]. But concentration has a corollary: if HIV commands a large share
of African trial capacity, other high-burden conditions may be relatively
crowded out. We quantify HIV's share of the African trial portfolio against a
full-registry baseline and against other diseases.

---

## 2. Methods

**Data.** AACT April-12-2026 flat-file snapshot; records reassembled by start
signature before field splitting.
**HIV trials.** `conditions.downcase_name` matching HIV / human immunodeficiency
virus / AIDS (distinct nct_ids; "hearing aids"/"band aids" excluded).
**African-site trial.** ≥1 `facilities.country` among the 54 AU states
(registry-wide 25,125 = 4.33%).
**Metric.** Within-disease African share vs the 4.33% baseline, compared across
diseases computed identically.

---

## 3. Results

### 3.1 HIV's African trial share vs the baseline and other diseases

| Condition | Global trials | African-site | African share |
|---|---|---|---|
| **HIV / AIDS** | 9,126 | 1,713 | **18.77%** |
| HIV / AIDS (interventional) | 7,404 | 1,447 | 19.54% |
| Sickle cell disease | 1,091 | 105 | 9.62% |
| Cervical cancer / HPV | 2,613 | 136 | 5.20% |
| Epilepsy | 2,103 | 72 | 3.42% |
| Breast cancer | 14,432 | 375 | 2.60% |
| **Registry baseline (all diseases)** | 579,828 | 25,125 | **4.33%** |

HIV's African trial share (18.77%) is **4.3× the all-disease baseline** and the
highest of any condition examined. It is roughly 2× the share for sickle cell
disease (itself the most African monogenic disorder), 3.6× cervical cancer, 5.5×
epilepsy, and 7.2× breast cancer. Nearly one in five HIV trials worldwide includes
an African site; for breast cancer it is one in 38.

### 3.2 Burden context (verified literature)

HIV burden is genuinely SSA-concentrated: the majority of people living with HIV
globally reside in sub-Saharan Africa [1,2 (UNAIDS)], and HIV remains a leading
cause of disease burden in the region [1]. The African centrality of HIV trials
is therefore burden-aligned in a way that distinguishes it from the neglect
seen for other conditions — HPTN 052, the trial that established
treatment-as-prevention, enrolled 54% of its subjects in Africa across nine
countries [3].

---

## 4. Discussion

The HIV portfolio is the clearest counter-example to the African-neglect
narrative: HIV is over-represented, not under-represented, in African trials.
This "saturation" reflects a genuine, burden-justified investment — but it also
frames the neglect of other diseases in sharper relief. The same continent that
hosts ~19% of the world's HIV trials hosts only 2.6% of breast-cancer trials and
3.4% of epilepsy trials, despite substantial and rising burdens of both. The
contrast is not an argument for less HIV research; it is an argument that the
trial *capacity* HIV funding built — investigator networks, GCP-compliant sites,
laboratory and data infrastructure, community engagement mechanisms — is a
transferable asset. Platform and basket approaches that add non-HIV arms to
established HIV trial sites, and deliberate capacity-sharing, could convert HIV
saturation into broader trial capability.

Two cautions apply. First, ≥1-African-site counting credits multinational trials
that may enrol relatively few African participants; the participant-weighted HIV
share, while still high, may be lower than 18.8%. Second, "saturation" is a
descriptive claim about trial siting, not a normative claim that HIV research
should shrink — the burden justification is real. The policy inference is about
*leveraging* HIV infrastructure for co-morbid and neglected conditions, not
redirecting it.

---

## 5. Limitations

Registry counts undercount trials registered only on non-ClinicalTrials.gov
registries (PACTR, etc.). Keyword matching for "HIV/AIDS" is broad and may include
trials where HIV is a co-condition; exclusions were applied for "hearing/band
aids". African-site counting credits any trial with ≥1 African facility.
Burden figures are cited from UNAIDS/GBD sources with their own uncertainty.
The cross-disease comparison uses identical methodology across conditions, so
relative shares are robust even where absolute counts are approximate.

---

## 6. Conclusion

Of 9,126 global HIV trials, 1,713 (18.77%) include an African site — 4.3× the
4.33% all-disease baseline and 2–7× the African share of sickle cell, cervical,
epilepsy, and breast-cancer trials. HIV is the most over-represented major disease
in Africa's trial portfolio, a burden-aligned "saturation" that stands in sharp
contrast to the neglect of other high-burden conditions. The transferable trial
capacity HIV funding created is the continent's largest under-used asset for
broadening African clinical research.

---

## References
*All PMIDs/DOIs verified against PubMed (title + journal + volume/pages match).
v1's 11 references were wrong or unlocatable and have been rebuilt.*

1. GBD 2019 Diseases and Injuries Collaborators. Global burden of 369 diseases and injuries in 204 countries and territories, 1990-2019. *Lancet.* 2020;396(10258):1204-1222. PMID: 33069326. DOI: 10.1016/S0140-6736(20)30925-9
2. UNAIDS. *Global HIV & AIDS statistics — Fact sheet.* Geneva: Joint United Nations Programme on HIV/AIDS. (report; not PubMed-indexed, no PMID)
3. Cohen MS, Chen YQ, McCauley M, et al. Prevention of HIV-1 infection with early antiretroviral therapy (HPTN 052). *N Engl J Med.* 2011;365(6):493-505. PMID: 21767103. DOI: 10.1056/NEJMoa1105243

*Source: metadata retrieved from PubMed. v1's citation list was largely fabricated
(7/11 references not locatable); v2 uses only verified sources plus the UNAIDS
fact sheet. The quantitative claims rest on the AACT computation, not on the
literature.*

---

*DRAFT for author dictation. Trial counts regenerated by `_africa_equity_verify.py`
against AACT 2026-04-12. Confidence: HIGH on registry counts (exact, identical
methodology across diseases); burden context cited from verified sources. Prior
reference list was fabricated and has been rebuilt.*
