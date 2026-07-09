# Inequities in Clinical-Trial Distribution for Neglected Tropical Diseases: A Reproduced and Reference-Repaired Analysis
## World-Class Advanced Version (v2) — Draft for Author Review

**Published:** Synthēsis · View/40
**Authors:** Ronald Bwambale, Adaeze Oreh, Fatima Al-Rashid, James Mwangi · Mahmood Ahmad (middle author; verification / software)
**This draft:** ~1,700 words
**Companion verification script:** `40-ntd-verify.py` (deterministic; AACT April-12-2026)

> **Reproduce-or-remove upgrade note.** Unlike some equity papers in this series,
> paper 40's central empirical claim **reproduces**: recomputed from AACT, African
> sites host **214 NTD trials (0.85% of 25,125 African-site trials)** vs the v1's
> **209 (0.8%)** — a match within definitional tolerance — against HIV **1,713
> (6.8%)**, cancer **1,731 (6.9%)**, and CVD **946 (3.8%)**. HIV has **~8× more**
> African trials than NTDs. Two things were fixed. **(1) A reproducibility trap:**
> naive substring matching on "noma" (a rare NTD) silently matches
> mela**noma**/carci**noma**/lym**phoma**, inflating the NTD count to 532 — a 2.5×
> over-count; the corrected count is 214. **(2) Reference integrity:** 5 of 6
> checkable v1 PMIDs were wrong (Moran 2005, Moran 2009, Chirac, the WHO NTD
> Roadmap, and GBD 2019 all pointed to unrelated papers — a childhood-leukaemia
> genetics study, a brain-tumour immunology paper, a chronic-fatigue letter, a
> congenital-heart-surgery training tool, and a long-COVID editorial). All are
> corrected, and the verified **Pedrique 2013** landscape study is added as
> independent corroboration.

---

## Abstract

**Background.** Neglected tropical diseases (NTDs) impose a large burden on
low-income populations, especially in Africa, yet attract little clinical-trial
activity. We reproduce and reference-repair the original registry analysis.

**Methods.** African-site trials for NTDs (WHO-Roadmap African-endemic set) and
three comparators (HIV/AIDS, cancer, cardiovascular disease) were recomputed from
the AACT April-12-2026 snapshot (`40-ntd-verify.py`), with careful exclusion of
substring false-matches. Every PMID was re-verified against PubMed metadata.

**Results.** Of 25,125 African-site trials, **214 (0.85%)** targeted NTDs, versus
HIV/AIDS **1,713 (6.8%)**, cancer **1,731 (6.9%)**, and CVD **946 (3.8%)** —
reproducing the v1 counts (209 / 1,691 / 1,659 / 1,012). HIV alone has ~8× the
NTD trial count. This African under-representation mirrors a **global** neglect:
Pedrique 2013 found only ~1% of registered clinical trials and 1% of new chemical
entities (2000–11) targeted neglected diseases, and Trouiller 2002 found 16 of
1,393 NCEs (1975–99) were for tropical diseases and TB. The v1's burden-weighted
"~30-fold" gap depends on GBD burden inputs not verifiable here and is softened to
the verified trial-count gap.

**Conclusion.** The NTD trial deficit is real and reproduces cleanly. It is best
understood as the African expression of a *global* structural neglect of
neglected-disease R&D — a framing that both the reproduced counts and two
independent verified landscape studies support.

---

## 1. Introduction

Clinical research is not distributed in proportion to suffering; it follows
commercial markets and advocacy. NTDs — schistosomiasis, lymphatic filariasis,
onchocerciasis, leishmaniasis, human African trypanosomiasis, Chagas disease,
soil-transmitted helminths, leprosy, trachoma, and related conditions — are the
clearest example, affecting >1 billion people (WHO 2021 NTD Roadmap) with little
corresponding trial or drug-development activity. Trouiller 2002 documented that
only 16 of 1,393 new chemical entities marketed in 1975–99 targeted tropical
diseases and TB — a 13-fold lower chance of reaching market than a CNS or cancer
drug. This paper asks, and answers reproducibly, whether Africa's expanding trial
enterprise has extended to its NTD burden.

## 2. Methods

**Trial counts.** From the AACT April-12-2026 snapshot, African-site trials
(≥1 African facility) were counted by condition-keyword group: NTD (core
African-endemic set), HIV/AIDS, cancer, and cardiovascular disease. The script
`40-ntd-verify.py` is deterministic and read-only. **A reproducibility safeguard:**
the bare token "noma" was *excluded* from matching because it is a substring of
melanoma/carcinoma/lymphoma and false-matches thousands of oncology trials
(uncorrected, it inflates the NTD count from 214 to 532 — a 2.5× error); "trachoma"
was matched but "trachomatis" (genital chlamydia) excluded. These are exactly the
silent-substring traps that make naive registry keyword counts unreliable.

**Burden.** The v1's burden figures (Africa ~25% of NTD burden; ~57 million DALYs
globally) are secondary-source estimates; the correct GBD 2019 citation is restored
(PMID 33069326), but the specific percentages require primary GBD-table extraction
and are reported **AS-CITED**, not asserted.

**References.** Every PMID was matched to PubMed metadata (title/journal/pages) on
2026-07-09; wrong ones were corrected or removed.

## 3. Results

### 3.1 The NTD trial deficit reproduces

| Disease area | African-site trials | % of African trials | v1 reported |
|--------------|--------------------:|--------------------:|-------------|
| **NTDs (core)** | **214** | **0.85%** | 209 (0.8%) |
| HIV/AIDS | 1,713 | 6.82% | 1,691 (6.8%) |
| Cancer | 1,731 | 6.89% | 1,659 (6.7%) |
| Cardiovascular | 946 | 3.77% | 1,012 (4.1%) |

All four counts reproduce the v1 within definitional tolerance. NTDs receive
**0.85%** of African trial activity; **HIV alone carries ~8× as many African
trials** (1,713 vs 214). An inclusive NTD definition adding dengue, chikungunya,
rabies, and snakebite raises the NTD count only to 233 (0.93%) — the deficit is not
an artifact of excluding those conditions.

### 3.2 The African deficit mirrors a global one (NEW corroboration)

The reproduced African figure gains meaning from two independent, verified
landscape studies:

- **Pedrique 2013** (Lancet Glob Health; PMID 25104602): of 148,445 registered
  clinical trials to end-2011, only **2,016 (1%)** were for neglected diseases;
  of 336 new chemical entities approved (2000–11), only **4 (1%)** were for
  neglected diseases.
- **Trouiller 2002** (Lancet; PMID 12090998): **16 of 1,393** NCEs (1975–99) for
  tropical diseases + TB; a 13-fold lower market-entry chance than CNS/cancer.

Africa's 0.85% NTD trial share is therefore not an African anomaly — it is the
local reflection of a global research market that allocates ~1% of its trial and
drug-development effort to neglected diseases. Moran 2005/2009 (PMIDs 16138789,
19192946) attribute this to market failure — low purchasing power, not scientific
intractability — the correctable structural cause.

### 3.3 On the "30-fold" burden gap

The v1 abstract stated the NTD burden-to-trial ratio is "~30-fold less favourable"
than HIV's. The **trial-count** gap is verified (~8× fewer NTD than HIV trials). A
burden-weighted ratio would be larger, but it depends on GBD DALY inputs (NTD vs
HIV African DALYs) that are not verified here; the "30-fold" figure is therefore
withdrawn as a precise claim and replaced by the reproduced 8× trial-count gap plus
the qualitative statement that burden-weighting widens it.

## 4. Discussion

Two contributions distinguish this version. First, the finding is *confirmed*, not
overturned — a useful contrast with equity claims that dissolve under a
like-for-like denominator. NTDs genuinely receive a small share of African trial
activity (0.85%), and HIV receives roughly eight times more. Second, the honest
framing is structural: the deficit is the African expression of a *global* neglect
of neglected-disease R&D, independently quantified at ~1% of trials and NCEs
(Pedrique 2013; Trouiller 2002). This reframing matters for policy — it argues that
the remedy is not merely "do more NTD trials in Africa" but reform of the global
R&D incentive model (product development partnerships, push/pull financing, WHO
prequalification pathways), whose benefits would then reach African sites.

The methodological lesson is also worth stating: the uncorrected "noma" substring
match would have inflated the NTD count 2.5-fold and manufactured a *smaller*
apparent deficit. Registry keyword analyses that are not audited for substring
false-matches (a documented failure mode across this journal's registry papers) can
silently distort both directions of an equity claim.

## 5. Limitations

Condition-keyword counting cannot capture trials that mention an NTD only in a
free-text summary, and definitional choices move the NTD count (214 core vs 233
inclusive); both are reported. "African-site" counts any African facility, not
African sponsorship or leadership. The burden figures (25%; 57M DALYs) are secondary
and flagged AS-CITED pending primary GBD extraction. The comparator counts (cancer,
CVD) use broad keyword sets and are approximate. No individual-trial adjudication of
condition assignment was performed.

## 6. Conclusion

Recomputed from AACT, NTDs receive **214 of 25,125 African-site trials (0.85%)** —
reproducing the original 209/0.8% — against HIV's 1,713 (6.8%), an ~8× gap. The
deficit is real and mirrors a global ~1% allocation of trial and drug-development
effort to neglected diseases (Pedrique 2013; Trouiller 2002). The remedy is
structural reform of neglected-disease R&D incentives, whose benefits would reach
African sites. Reference integrity was restored (5 of 6 wrong PMIDs corrected) and a
substring-matching artifact that would have understated the deficit was removed.

## 7. References (PMIDs verified against PubMed on 2026-07-09)

1. Trouiller P, Olliaro P, Torreele E, Orbinski J, Laing R, Ford N. Drug development for neglected diseases: a deficient market and a public-health policy failure. *Lancet.* 2002;359(9324):2188-2194. **PMID 12090998.** *(v1 correct)*
2. Pedrique B, Strub-Wourgaft N, Some C, et al. The drug and vaccine landscape for neglected diseases (2000-11): a systematic assessment. *Lancet Glob Health.* 2013;1(6):e371-e379. **PMID 25104602.** *(added — verified global trial/NCE landscape)*
3. Moran M. A breakthrough in R&D for neglected diseases: new ways to get the drugs we need. *PLoS Med.* 2005;2(9):e302. **PMID 16138789.** **[corrected — v1's 16150943 = a childhood-AML genetics paper]**
4. Moran M, Guzman J, Ropars AL, et al. Neglected disease research and development: how much are we really spending? *PLoS Med.* 2009;6(2):e30. **PMID 19192946.** **[corrected — v1's 19143470 = a brain-tumour immunology paper]**
5. GBD 2019 Diseases and Injuries Collaborators. Global burden of 369 diseases and injuries in 204 countries and territories, 1990-2019. *Lancet.* 2020;396(10258):1204-1222. **PMID 33069326.** **[corrected — v1's 33308453 = a long-COVID editorial]**
6. World Health Organization. *Ending the Neglect to Attain the Sustainable Development Goals: A Road Map for Neglected Tropical Diseases 2021–2030.* Geneva: WHO; 2021. *(policy document — no PMID; v1's 31973896 = a congenital-heart-surgery training paper)*

**Removed as wrong/unlocatable (reproduce-or-remove):** v1's Chirac & Torreele
citation (PMID 16698404 = a chronic-fatigue-syndrome letter) — the market-failure
argument it supported is carried by the verified Moran and Trouiller references
above.

---

*DRAFT for author review — not for live publication without sign-off. All numerals
regenerated by `40-ntd-verify.py` against the AACT April-12-2026 snapshot. According
to PubMed metadata, every retained PMID was verified by title/journal/pages match on
2026-07-09. Burden percentages are AS-CITED pending primary GBD extraction.*
