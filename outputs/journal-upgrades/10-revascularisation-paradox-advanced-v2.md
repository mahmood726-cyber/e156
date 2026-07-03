# The Revascularisation Paradox: Statistical Fragility of the CABG-vs-PCI Evidence Base
## World-Class Advanced Version (v2) — Draft for Author Dictation

**Published:** Synthēsis · View/10
**Authors:** [Student first author], Mahmood Ahmad (middle author; software / formal analysis), [Faculty senior author]
**This draft:** ~1,400 words · Category B advance
**Provenance:** the FAME-3 Fragility Index is computed exactly by
`fragility_multi_verify.py` (deterministic, two-sided Fisher exact, scipy).
Re-run to reproduce FI = 6.

> **v2 upgrade over v1.** v1 computed the Fragility Index for FAME-3 via a
> chi-square approximation (FI ≈ 6). v2 computes the **exact** two-sided Fisher
> FI (FI = 6, FQ 0.40%, baseline p = 0.0133) and states explicitly which trials
> admit an exact binary FI (FAME-3) versus which require individual-patient data
> for an exact log-rank FI (the time-to-event trials). All reference PMIDs were
> re-verified against PubMed.

---

## Abstract

**Background:** Landmark trials comparing coronary-artery bypass grafting (CABG)
with percutaneous coronary intervention (PCI) have shaped revascularisation
guidelines, but the statistical robustness of their headline results is
under-examined. We quantified fragility for the FAME-3 primary composite and
place the wider CABG-vs-PCI evidence base in a fragility frame.

**Methods:** Exact Fragility Index (FI) by two-sided Fisher exact test on
published crude event counts, modifying one arm (Walsh method [1]); Fragility
Quotient FQ = FI/N [2]. For the FAME-3 1-year primary composite the counts
(FFR-PCI 80/757; CABG 51/743) were verified against the primary publication.
Time-to-event trials (SYNTAX, FREEDOM, EXCEL, ISCHEMIA) are discussed with the
explicit caveat that a binary FI is a lower bound on the true log-rank FI.

**Results:** FAME-3: baseline two-sided Fisher P = 0.0133; **FI = 6** (adding 6
events to the CABG arm raises P to 0.060), **FQ = 0.40%**. The significant
1-year superiority of CABG over FFR-guided PCI in three-vessel disease therefore
hinges on 6 events out of 1,500 patients — below the median FI (≈8) of RCTs in
high-impact journals and well under the 1% Fragility-Quotient threshold.

**Conclusion:** At least one pivotal contemporary revascularisation trial rests
on a strikingly fragile primary result. Fragility indices should accompany
CABG-vs-PCI trial reporting so that guideline recommendations reflect not only
statistical significance but its robustness.

---

## 1. Introduction

The choice between CABG and PCI in multivessel and left-main coronary disease is
governed by a small number of pivotal RCTs — SYNTAX, FREEDOM, EXCEL, NOBLE,
ISCHEMIA, and FAME-3 — whose results have at times conflicted and provoked public
controversy (notably the EXCEL mortality debate). Statistical significance (or
its absence) has driven guideline class-of-recommendation changes. Yet a P value
below 0.05 says nothing about how *many events* separate a "significant" from a
"non-significant" result. The Fragility Index (FI) — the number of
event/non-event reclassifications needed to cross P = 0.05 — makes that
robustness explicit [1]. We apply it to the FAME-3 primary composite (an
exact binary computation) and frame the broader evidence base.

---

## 2. Methods

**Fragility Index (exact).** For a significant 2×2 result, the minimum number of
patients in one arm whose status changes from non-event to event to raise the
two-sided Fisher exact P to ≥0.05 [1]. Events are added to the arm with fewer
events (narrowing the difference); only one arm is modified. FQ = FI ÷ total N,
the fragility relative to trial size [2]. Computed in `fragility_multi_verify.py`
(scipy `fisher_exact`).

**FAME-3 counts (verified).** Fearon et al.: FFR-guided PCI vs CABG in
three-vessel disease; 1-year primary composite (death, MI, stroke, or repeat
revascularisation) in 80/757 (10.6%) PCI vs 51/743 (6.9%) CABG.

**Time-to-event trials.** SYNTAX, FREEDOM, EXCEL, ISCHEMIA report time-to-event
outcomes; a binary FI treats end-of-follow-up cumulative counts as a 2×2 table,
ignoring censoring, and is a **lower bound** on the true log-rank FI, which needs
individual-patient data. We therefore do not assert exact binary FIs for these
trials from summary statistics.

---

## 3. Results

### 3.1 FAME-3 — exact Fragility Index

| Outcome | PCI | CABG | Fisher P | FI | FQ |
|---|---|---|---|---|---|
| 1-yr primary composite | 80/757 | 51/743 | 0.0133 | **6** | **0.40%** |

Adding 6 events to the CABG arm (51 → 57) raises the two-sided Fisher exact P from
0.0133 to 0.060 — non-significant. The significant 1-year superiority of CABG over
FFR-guided PCI in three-vessel disease thus depends on 6 events among 1,500
randomised patients. By the Walsh benchmark (median FI ≈ 8 across high-impact
RCTs [1]) and a Fragility-Quotient threshold of <1% (fragility relative to trial
size [2]), FAME-3's primary result is fragile: FI = 6 < 8 and FQ = 0.40% < 1%.

### 3.2 The wider evidence base (framing, not exact FI)

The revascularisation trials span the significance spectrum: FAME-3 (significant,
fragile as shown), ISCHEMIA (primary composite non-significant — an invasive
strategy did not reduce CV death/MI versus conservative care), and EXCEL (a
non-inferiority design whose *secondary* longer-term mortality signal fuelled
controversy). A single fragile primary result (FAME-3) sitting alongside a null
mega-trial (ISCHEMIA) and a disputed non-inferiority trial (EXCEL) is precisely
the configuration in which fragility reporting matters most: small shifts in a
handful of events could reconcile — or further divide — trials that currently
appear to conflict.

---

## 4. Discussion

The FAME-3 result illustrates the revascularisation paradox: a guideline-relevant
comparison decided by a margin of six events. This is not a criticism of FAME-3's
conduct — it is a well-run trial — but of interpreting P < 0.05 as if all
significant results were equally secure. An FI of 6 means that plausible
differences in event adjudication, a handful of additional CABG events, or modest
loss to follow-up could have rendered the primary comparison non-significant.

Two implications follow. First, **reporting**: FI and FQ should accompany the
primary result of every pivotal revascularisation RCT, as several editorial
groups now encourage, so that guideline committees weigh robustness alongside
significance. Second, **synthesis**: when trials appear to conflict (FAME-3
favouring CABG, ISCHEMIA null, EXCEL disputed), fragility analysis clarifies how
much of the apparent disagreement is driven by a few events versus a genuine
difference in effect — a question a bare P value cannot answer.

The time-to-event caveat is important and honest: for SYNTAX, FREEDOM, EXCEL, and
ISCHEMIA the binary FI understates the true log-rank FI, so we decline to assert
exact fragility for them without IPD. This restraint is itself the point — precise
fragility claims require the right method and verified counts, not a plausible
approximation dressed as exact.

---

## 5. Limitations

Only FAME-3's primary composite is computed exactly, because it is reported as a
binary count and the counts were verified against the primary publication. The
binary FI ignores time-to-event structure and is a lower bound for the other
trials; exact log-rank FIs require IPD not available here. FI/FQ describe
statistical robustness, not clinical importance, effect size, or external
validity, and a fragile result is not a wrong result.

---

## 6. Conclusion

FAME-3's significant 1-year superiority of CABG over FFR-guided PCI in
three-vessel disease rests on an exact Fragility Index of 6 (FQ 0.40%) — below
the median FI of high-impact RCTs and under the 1% fragility threshold. In an
evidence base that already contains a null mega-trial (ISCHEMIA) and a disputed
non-inferiority trial (EXCEL), routine reporting of the Fragility Index would let
guideline committees weigh not just whether a revascularisation result is
significant, but how securely.

---

## References
*All PMIDs/DOIs verified against PubMed (title + journal + volume/pages match).
v1 had 6/12 wrong PMIDs (incl. a subungual-melanoma paper for FAME-3 and a
fabricated "Bakal 2015" citation); rebuilt below.*

1. Walsh M, Srinathan SK, McAuley DF, et al. The statistical significance of randomized controlled trial results is frequently fragile: a case for a Fragility Index. *J Clin Epidemiol.* 2014;67(6):622-628. PMID: 24508144. DOI: 10.1016/j.jclinepi.2013.10.019
2. Tignanelli CJ, Napolitano LM. The Fragility Index in randomized clinical trials as a means of optimizing patient care (defines the Fragility Quotient, FI/N). *JAMA Surg.* 2019;154(1):74-79. PMID: 30422256. DOI: 10.1001/jamasurg.2018.4318
3. Fearon WF, Zimmermann FM, De Bruyne B, et al. Fractional flow reserve-guided PCI as compared with coronary bypass surgery (FAME 3). *N Engl J Med.* 2022;386(2):128-137. PMID: 34735046. DOI: 10.1056/NEJMoa2112299
4. Serruys PW, Morice MC, Kappetein AP, et al. Percutaneous coronary intervention versus coronary-artery bypass grafting for severe coronary artery disease (SYNTAX). *N Engl J Med.* 2009;360(10):961-972. PMID: 19228612. DOI: 10.1056/NEJMoa0804626
5. Farkouh ME, Domanski M, Sleeper LA, et al. Strategies for multivessel revascularization in patients with diabetes (FREEDOM). *N Engl J Med.* 2012;367(25):2375-2384. PMID: 23121323. DOI: 10.1056/NEJMoa1211585
6. Stone GW, Sabik JF, Serruys PW, et al. Everolimus-eluting stents or bypass surgery for left main coronary artery disease (EXCEL, 3-year). *N Engl J Med.* 2016;375(23):2223-2235. PMID: 27797291. DOI: 10.1056/NEJMoa1610227
7. Stone GW, Kappetein AP, Sabik JF, et al. Five-year outcomes after PCI or CABG for left main coronary disease (EXCEL). *N Engl J Med.* 2019;381(19):1820-1830. PMID: 31562798. DOI: 10.1056/NEJMoa1909406
8. Maron DJ, Hochman JS, Reynolds HR, et al. Initial invasive or conservative strategy for stable coronary disease (ISCHEMIA). *N Engl J Med.* 2020;382(15):1395-1407. PMID: 32227755. DOI: 10.1056/NEJMoa1915922
9. Mäkikallio T, Holm NR, Lindsay M, et al. Percutaneous coronary angioplasty versus coronary artery bypass grafting in treatment of unprotected left main stenosis (NOBLE). *Lancet.* 2016;388(10061):2743-2752. PMID: 27810312. DOI: 10.1016/S0140-6736(16)32052-9
10. Carter RE, McKie PM, Storlie CB. The Fragility Index: a P-value in sheep's clothing? *Eur Heart J.* 2017;38(5):346-348. PMID: 28417139. DOI: 10.1093/eurheartj/ehw495

*Source: metadata retrieved from PubMed. Every PMID independently re-verified
(not taken from the audit unchecked). FAME-3 event counts (80/757; 51/743) are
consistent with the published 10.6%/6.9% primary-composite rates.*

---

*DRAFT for author dictation. FAME-3 FI regenerated by `fragility_multi_verify.py`
(FI=6, exact Fisher). Confidence: HIGH for FAME-3 (exact, verified counts);
other trials framed qualitatively with the log-rank caveat.*
