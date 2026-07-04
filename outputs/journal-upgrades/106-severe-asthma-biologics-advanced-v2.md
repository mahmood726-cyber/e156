# Severe Asthma Biologics: A Truth-First, Biomarker-Stratified Synthesis of Five Approved Agents (Reference-Corrected)

**Published (base article):** Synthēsis · View/106
**Authors:** Hamood Saeed (first/corresponding); Mahmood Ahmad (non-corresponding co-author, Tahir Heart Institute, Rabwah; ORCID 0000-0001-9107-3704).
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `106-asthma-biologics-verify.py` (deterministic)
**Evidence tier:** MODERATE–HIGH (pivotal placebo-controlled RCTs); indirect comparison caveats apply.
**Standard:** PRISMA 2020 · verified pairwise estimates · biomarker stratification · reproduce-or-flag.

---

## Upgrade note (what changed from v1, and why) — a reference-integrity repair

The v1 draft's reference list contained **fabricated PMIDs**. Verified against
PubMed on 2026-07-04, four of the pivotal-trial citations pointed to entirely
unrelated papers:

| v1 PMID | v1 claimed | What the PMID actually is |
|---|---|---|
| 34236781 | tezepelumab NAVIGATOR | a cardiac-surgery antioxidant-enzyme paper (*Braz J Cardiovasc Surg*) |
| 26302026 | mepolizumab RR 0.47 | a prediabetes-prevalence paper (*Metab Syndr Relat Disord*) |
| 28366640 | benralizumab | a voltammetric-sensor analytical-chemistry paper (*Anal Biochem*) |
| 28366441 | benralizumab | a gastric-endoscopy paper (*Gastrointest Endosc*) |

Only MENSA (25199059) and QUEST (29782217) were correct. v2 **rebuilds the pivotal
evidence base from verified primary reports**, replaces every RR with the figure read
from the correct trial abstract, adds a biomarker-stratified structure with the
low-eosinophil data that is the clinically decisive differentiator, and computes NNT
from published placebo rates. No de-novo network meta-analysis is fabricated: the full
arm-level network is not reproduced here, so formal SUCRA rankings are attributed to
published NMAs rather than recomputed. Every number below is emitted by the companion
script.

---

## Abstract

**Background.** Five biologics are approved for severe asthma — omalizumab (anti-IgE),
mepolizumab (anti-IL-5), benralizumab (anti-IL-5Rα), dupilumab (anti-IL-4Rα/IL-13),
and tezepelumab (anti-TSLP) — differing in mechanism and biomarker eligibility.

**Methods.** Verified synthesis of the pivotal placebo-controlled RCT for each agent,
with the annualized exacerbation rate ratio (RR) as the primary outcome, stratified by
blood-eosinophil phenotype. NNT computed from published placebo rates. All PMIDs and
RRs PubMed-verified.

**Results.** In eosinophil-enriched populations all agents markedly reduce
exacerbations: mepolizumab MENSA **0.47 (0.35–0.63)**; benralizumab SIROCCO Q8W
**0.49 (0.37–0.64)**, CALIMA Q8W 0.72 (0.54–0.95); dupilumab QUEST (eos ≥300)
**0.34 (0.24–0.48)**. In **unselected or low-eosinophil** asthma the picture diverges:
tezepelumab reduces exacerbations overall **0.44 (0.37–0.53)** and, critically,
**0.59 (0.46–0.75) in patients with eosinophils <300**; dupilumab retains benefit
(overall RR ≈0.53); omalizumab EXTRA reduces exacerbations 25% (**IRR 0.75, 0.61–0.92**)
in the allergic phenotype. NNT to prevent one exacerbation: tezepelumab ~0.85
patient-years, dupilumab ~2.4.

**Conclusion.** Biomarker profile, not a single composite rank, should govern biologic
selection. For blood eosinophils ≥300 cells/µL, anti-IL-5/IL-5Rα agents and dupilumab
provide similar large benefit. For **non-eosinophilic, low-eosinophil, or broadly
phenotyped** severe asthma, **tezepelumab** is the only agent with demonstrated
efficacy across the eosinophil spectrum.

---

## 1. Introduction

Severe asthma — uncontrolled despite high-dose inhaled corticosteroids plus a second
controller — affects 5–10% of people with asthma yet drives ~50% of asthma costs. Its
pathophysiology divides into T2-high (eosinophilic; IL-5–driven eosinophilia,
IL-4/IL-13–driven IgE and FeNO, upstream TSLP/alarmin signalling) and T2-low
(neutrophilic/paucigranulocytic). This division is the actionable axis for biologic
selection because each agent's eligibility and efficacy track a biomarker: omalizumab
requires allergic sensitisation and IgE range; mepolizumab and benralizumab require
blood eosinophils (≥150–300 cells/µL); dupilumab requires eosinophils ≥150 or FeNO ≥25
ppb; tezepelumab, acting upstream at TSLP, is **label-unrestricted by eosinophil count**.
Because head-to-head trials do not exist, indirect comparison is the appropriate frame —
but only if the underlying pairwise estimates are correct. v1's were not; v2 restores
them.

## 2. Methods

For each agent we used its pivotal, double-blind, placebo-controlled phase 3 trial (or,
for benralizumab, both replicate trials SIROCCO and CALIMA), and extracted the
annualized exacerbation RR versus placebo — overall and within the pre-specified
eosinophil strata reported by the trial. logRR and SE were derived from each published
RR and 95% CI (SE = (ln UL − ln LL)/(2×1.96)). A fixed-effect pooled estimate summarises
the T2-high class magnitude (not a ranking). NNT is the reciprocal of the annualized
rate difference (patient-years treated to prevent one exacerbation), computed from
published placebo and treatment rates. Formal comparative rankings (SUCRA) are cited from
published network meta-analyses; no de-novo NMA is computed here because the full
network and arm-level data are not reproduced. All PMIDs were verified by PubMed
metadata match on 2026-07-04.

## 3. Results

### 3.1 Verified pivotal-trial exacerbation reductions

| Agent | Trial (PMID) | Stratum | Exacerbation RR (95% CI) |
|---|---|---|---|
| Omalizumab (anti-IgE) | EXTRA, Hanania 2011 (21536936) | allergic, unselected eos | **0.75 (0.61–0.92)** |
| Mepolizumab (anti-IL-5) | MENSA, Ortega 2014 (25199059) | eosinophilic | **0.47 (0.35–0.63)** SC; 0.53 (0.39–0.71) IV |
| Benralizumab (anti-IL-5Rα) | SIROCCO, Bleecker 2016 (27609408) | eos ≥300 | **0.49 (0.37–0.64)** Q8W; 0.55 (0.42–0.71) Q4W |
| Benralizumab | CALIMA, FitzGerald 2016 (27609406) | eos ≥300 | 0.64 (0.49–0.85) Q4W; 0.72 (0.54–0.95) Q8W |
| Dupilumab (anti-IL-4Rα) | QUEST, Castro 2018 (29782217) | overall | ≈**0.53** (47.7% lower; rate 0.46 vs 0.87) |
| Dupilumab | QUEST | eos ≥300 | **0.34 (0.24–0.48)** (65.8% lower) |
| Tezepelumab (anti-TSLP) | NAVIGATOR, Menzies-Gow 2021 (33979488) | overall | **0.44 (0.37–0.53)** (rate 0.93 vs 2.10) |
| Tezepelumab | NAVIGATOR | **eos <300** | **0.59 (0.46–0.75)** (rate 1.02 vs 1.73) |

*Dupilumab overall RR is derived from the published 47.7% reduction and rate estimates;
its exact CI is approximate. All other RRs and CIs are read directly from the primary
abstracts.*

### 3.2 The T2-high class magnitude

Pooling the high-eosinophil-stratum estimates (mepolizumab SC, benralizumab SIROCCO-Q8W
and CALIMA-Q8W, dupilumab eos ≥300) gives a fixed-effect class RR of **0.50 (0.43–0.58)**
— roughly halving exacerbations. The pool is heterogeneous by design (benralizumab
CALIMA-Q8W 0.72 vs dupilumab 0.34) and is reported only to convey the T2-high class
magnitude, **not** to rank agents; ranking requires the full CrIs of a formal NMA.

### 3.3 The decisive low-eosinophil contrast

```
Exacerbation RR vs placebo, by eosinophil phenotype
   Favours biologic  <——|
HIGH eos (>=300):
  Dupilumab        ●            0.34
  Mepolizumab        ●          0.47
  Benralizumab(SIR)  ●          0.49
LOW / unselected:
  Tezepelumab (all)   ●         0.44
  Dupilumab (all)      ●        0.53
  Tezepelumab eos<300    ●      0.59
  Omalizumab (allergic)    ●    0.75
                 0.3  0.5  0.7  1.0
```

Anti-IL-5/IL-5Rα agents (mepolizumab, benralizumab) are **only** licensed and effective
in the eosinophil-high stratum. Tezepelumab is the sole agent with a **pre-specified,
statistically significant** exacerbation reduction in **eosinophil-low (<300)** patients
(RR 0.59, 0.46–0.75), consistent with its upstream TSLP mechanism acting proximal to the
eosinophilic cascade. Dupilumab retains overall benefit driven by FeNO/eosinophil-high
subgroups; omalizumab's benefit (IRR 0.75) is confined to the allergic phenotype.

### 3.4 Absolute benefit (NNT)

| Agent | Placebo rate (/pt-yr) | Treated rate | NNT (pt-yr / exacerbation prevented) |
|---|---|---|---|
| Tezepelumab (overall) | 2.10 | 0.93 | **0.85** |
| Dupilumab (overall) | 0.87 | 0.46 | 2.44 |
| Benralizumab CALIMA Q4W (eos ≥300) | 0.93 | 0.60 | 3.03 |

Tezepelumab's low NNT reflects its high-exacerbation NAVIGATOR population (placebo rate
2.10/pt-yr); NNTs are not directly comparable across trials with different baseline
event rates and are shown per-trial.

### 3.5 GRADE and comparative ranking

Per-agent-versus-placebo certainty is **MODERATE–HIGH** (large, replicated, low-bias
RCTs). Comparative (agent-versus-agent) certainty is **LOW–MODERATE**, resting on
indirect evidence with no head-to-head trials; published network meta-analyses should be
consulted for formal SUCRA rankings, always read alongside the pairwise credible
intervals rather than the rank alone.

## 4. Discussion

Once the fabricated citations are removed and the verified pivotal RRs restored, the
evidence resolves into a clean biomarker-stratified decision rule. In the
eosinophil-high stratum, four agents (mepolizumab, benralizumab, dupilumab, tezepelumab)
all approximately halve or better exacerbations, with dupilumab numerically strongest
(RR 0.34 at eos ≥300) — but the confidence intervals overlap substantially, and in the
absence of head-to-head trials no agent can be declared superior on exacerbation grounds
alone. Choice within this stratum should therefore be driven by comorbidities (dupilumab
for coexisting atopic dermatitis or chronic rhinosinusitis with nasal polyps),
oral-corticosteroid dependence, dosing convenience, and payer criteria.

The clinically decisive distinction lies **outside** the eosinophil-high stratum. Only
tezepelumab has a pre-specified, significant exacerbation reduction in patients with
blood eosinophils <300 (RR 0.59), and its overall effect (0.44) is the largest single
pairwise reduction in the set. This is mechanistically coherent: by blocking TSLP, an
epithelial alarmin upstream of the IL-5, IL-4/IL-13, and IgE pathways, tezepelumab is
not dependent on a downstream eosinophilic phenotype. For the substantial minority of
severe-asthma patients who are non-eosinophilic, low-eosinophil, or broadly/uncertainly
phenotyped, tezepelumab is the agent with randomised support; anti-IL-5/IL-5Rα agents
are simply not indicated. Dupilumab occupies an intermediate position, with efficacy
concentrated in FeNO-high or eosinophil-high subgroups.

The broader methodological lesson is about reference integrity. A comparative-efficacy
review whose pivotal citations are wrong is not merely imprecise — it is unusable,
because a reader cannot trace any number to its source. The v1→v2 repair here (four
fabricated PMIDs replaced with verified primary reports) is the precondition for any
downstream ranking to mean anything.

## 5. Limitations

Indirect comparison without head-to-head trials; the class pool is heterogeneous and is
descriptive only. Trials differ in eosinophil thresholds, baseline exacerbation rates,
dosing, and duration, so cross-trial RRs and NNTs are not strictly commensurable. The
dupilumab overall RR CI is derived from the published reduction rather than read
directly. Formal comparative rankings are deferred to published NMAs; this synthesis
verifies the pairwise inputs but does not recompute the network. OCS-sparing,
lung-function, and quality-of-life outcomes are not tabulated here.

## 6. Conclusion

With its reference base corrected, the severe-asthma-biologic evidence supports a
biomarker-first strategy. For blood eosinophils ≥300 cells/µL, mepolizumab,
benralizumab, dupilumab, and tezepelumab all substantially reduce exacerbations (class
RR ≈0.50; dupilumab strongest at 0.34), and selection is guided by comorbidity and
OCS-dependence rather than exacerbation efficacy alone. For non-eosinophilic,
low-eosinophil, or broadly phenotyped severe asthma, **tezepelumab** is the only agent
with demonstrated efficacy across the eosinophil spectrum (overall RR 0.44; eos<300 RR
0.59). Comparative ranking remains LOW–MODERATE certainty pending head-to-head trials.

---

## References

1. Hanania NA, Alpan O, Hamilos DL, et al. Omalizumab in severe allergic asthma inadequately controlled with standard therapy (EXTRA): a randomized trial. *Ann Intern Med.* 2011;154(9):573–582. PMID: 21536936. doi:10.7326/0003-4819-154-9-201105030-00002.
2. Ortega HG, Liu MC, Pavord ID, et al. Mepolizumab treatment in patients with severe eosinophilic asthma (MENSA). *N Engl J Med.* 2014;371(13):1198–1207. PMID: 25199059. doi:10.1056/NEJMoa1403290.
3. Bleecker ER, FitzGerald JM, Chanez P, et al. Efficacy and safety of benralizumab (SIROCCO): a randomised, phase 3 trial. *Lancet.* 2016;388(10056):2115–2127. PMID: 27609408. doi:10.1016/S0140-6736(16)31324-1.
4. FitzGerald JM, Bleecker ER, Nair P, et al. Benralizumab as add-on treatment for severe eosinophilic asthma (CALIMA): a randomised, phase 3 trial. *Lancet.* 2016;388(10056):2128–2141. PMID: 27609406. doi:10.1016/S0140-6736(16)31322-8.
5. Castro M, Corren J, Pavord ID, et al. Dupilumab efficacy and safety in moderate-to-severe uncontrolled asthma (QUEST). *N Engl J Med.* 2018;378(26):2486–2496. PMID: 29782217. doi:10.1056/NEJMoa1804092.
6. Menzies-Gow A, Corren J, Bourdin A, et al. Tezepelumab in adults and adolescents with severe, uncontrolled asthma (NAVIGATOR). *N Engl J Med.* 2021;384(19):1800–1809. PMID: 33979488. doi:10.1056/NEJMoa2034975.

---

*Data-integrity note.* All six reference PMIDs, journals, first authors, citations, and
the exacerbation RRs/rates were verified by PubMed metadata match on 2026-07-04; this
replaced four fabricated v1 PMIDs (34236781, 26302026, 28366640, 28366441). logRR/SE,
the class pool, and NNTs are computed by `106-asthma-biologics-verify.py`. The dupilumab
overall RR (≈0.53) and its CI are derived from the published 47.7% reduction; all other
values are read directly from the primary abstracts. v1's efficacy-NMA SUCRA figures and
`[author verify]`/`[author required]` placeholders were **not** carried into v2. **Build
target:** `.docx` + figures via the E156 host build
(`outputs/journal-upgrades/build/106-asthma-biologics-v2/`); render the biomarker-strata
forest plot (§3.3).
