# Intravenous Calcium for Calcium-Channel-Blocker Toxicity: A Reproducible Evidence Map of an RCT-Free Intervention
## World-Class Advanced Version (v2) — Draft for Author Review

**Published:** Synthēsis · View/30
**Authors:** Niraj S Kumar et al. · Mahmood Ahmad (middle author; verification / software / data curation)
**Original body:** ~1,350 words · **This draft:** ~2,000 words
**Companion verification script:** `30-iv-calcium-ccb-verify.py` (deterministic; stdlib + scipy)
**Evidence base:** case reports, case series, 2 observational cohorts — **no RCTs**
**GRADE:** VERY LOW (all outcomes)

> **Reproduce-or-remove upgrade note (what changed from v1).** This paper's core
> conclusions are unchanged and correct: there are no RCTs, pooling is not
> appropriate, and GRADE is VERY LOW. Verification changed the *evidence
> plumbing*, not the message:
> **(1) Reference integrity.** Of 13 checkable PMIDs, four were wrong. Two are
> corrected (Shepherd 15827071→**15811898**; Cole 29472096→**29452919**), one is
> corrected with fixed pages (Isbister → **39305202**, 91(3):740-747, *not*
> 91(1):98-107), and **two cited papers cannot be located in PubMed at all**
> (Wax/Donovan 2001 and Markovchick 1988) and are **removed** rather than
> fabricated — their claims are re-anchored on verified sources and on the
> stoichiometry below. **(2)** v1 stated "41 of 66 CCB patients had cardiac
> arrests" — the 41 arrests (and 31 deaths) are **cohort-wide across all 199**
> Cole-2018 patients, not the 66 CCB subset; corrected. **(3)** v1's Nakamura
> case said "no additional therapy" — the source reports the patient was
> **refractory to calcium gluconate, glucagon and catecholamines first**, then
> responded to CaCl₂; corrected. **(4)** The elemental-calcium figures are now
> **derived from molecular weights** in the companion script (272.6 and 89.4 mg;
> ratio 3.05:1). **(5)** The 2020 AAPCC figure is flagged AS-CITED (not
> verifiable here); a verifiable 2003 poison-centre denominator is added.

---

## Abstract

**Background.** Calcium-channel-blocker (CCB) poisoning is among the most lethal
cardiovascular drug overdoses. Intravenous calcium is recommended first-line, yet
no randomised trial has ever tested it. We build a reproducible evidence map that
separates what is *calculable* (dosing stoichiometry, cohort descriptors) from
what is *inferable* (efficacy), and refuses to manufacture the latter.

**Methods.** Structured synthesis of human evidence (case reports, case series,
two observational cohorts). No pooling: clinical heterogeneity and near-universal
publication bias make a pooled "response rate" uninterpretable, so none is
computed. A companion script derives elemental-calcium content from molecular
weights and reports descriptive cohort proportions with Wilson intervals,
explicitly labelled as cohort descriptors — not treatment effects. Every PMID was
re-verified against PubMed metadata. GRADE was applied for non-RCT evidence.

**Results.** 10% CaCl₂ delivers **272.6 mg** elemental Ca²⁺ per 10 mL vs **89.4 mg**
for 10% calcium gluconate — a **3.05:1** ratio, so 1 g CaCl₂ ≈ 3 g gluconate at
equal elemental dose (all derived from MW, not asserted). Non-dihydropyridine
(verapamil, diltiazem) toxicity responds more consistently to calcium than
dihydropyridine (amlodipine) toxicity, a pattern consistent with L-type-channel
pharmacology and with Isbister 2024 (236 overdoses: amlodipine commonest at
62.3%; 18.6% received calcium; 3.0% died). Isolated calcium efficacy cannot be
estimated: in every cohort calcium was one of several concurrent therapies.

**Conclusion.** IV calcium is a pharmacologically justified, case-series-supported
first-line *temporising* measure — most reliably for non-dihydropyridine CCBs —
delivered while high-dose insulin euglycaemic therapy (HIET) takes effect. GRADE
VERY LOW; this reflects the irreducibly observational nature of toxicology
evidence, not a remediable gap.

---

## 1. Introduction

CCB poisoning is a leading cause of pharmaceutical cardiovascular death. Verifiable
poison-centre data show the scale: in 2003, US poison centres logged **9,650 CCB
ingestions with 57 deaths** (case fatality 0.59%, 95% CI 0.46–0.76%; Olson 2005),
representing over a third of cardiovascular-drug poison-centre deaths. (A commonly
cited 2020 AAPCC figure — 6,132 exposures, 45 deaths — could not be verified
against the NPDS annual report here and is flagged AS-CITED.) Long-acting
formulations are disproportionately lethal because peak toxicity may be delayed
12–18 hours.

IV calcium is recommended first-line on pharmacological grounds: raising
extracellular ionised calcium competitively shifts CCB–channel binding, increasing
the fraction of L-type channels available for activation — membrane stabilisation
by electrochemical gradient, not chemical neutralisation. The model predicts a
larger effect for high-myocardial-affinity non-dihydropyridines (verapamil >
diltiazem > dihydropyridines), a transient effect, and limited efficacy as
monotherapy. This paper tests how much of that can actually be *shown* from
human data — and is candid about how little can.

## 2. Methods

**Design.** Structured evidence map of human data: any report of IV calcium (any
salt/dose) for CCB overdose with ≥1 haemodynamic or survival outcome. Sources:
PubMed/EMBASE to June 2026, plus the Baid 2023 systematic review (PMID 37664357)
as a case-identification source.

**Why no pooling.** CCB type, dose, co-ingestants, concurrent therapies, and
outcome definitions differ across every report, and positive case reports are
preferentially published. A pooled "haemodynamic response rate" would therefore
estimate the *publication process*, not the *drug*. Per the al-Nafīs discipline of
not overclaiming, no pooled efficacy estimate is computed. Descriptive proportions
from the two structured cohorts are reported with Wilson 95% CIs and explicitly
framed as cohort descriptors.

**Verification.** Elemental calcium is derived from molecular weights in the
companion script. Every PMID was matched to PubMed metadata (title, journal,
pages); wrong PMIDs were corrected and unlocatable references removed. GRADE for
observational evidence (start VERY LOW; upgrade only on large effect + dose-response
+ plausible confounding direction).

## 3. Results

### 3.1 The dosing question is fully calculable (NEW: derived, not asserted)

The single quantitative fact clinicians most need — how much elemental calcium a
given ampoule delivers — needs no trial. From molecular weights (companion script):

| Preparation | MW (g/mol) | Elemental Ca²⁺ per 10 mL of 10% | mEq |
|-------------|-----------|-------------------------------|-----|
| CaCl₂·2H₂O | 147.01 | **272.6 mg** | 13.6 |
| Ca gluconate·H₂O | 448.39 | **89.4 mg** | 4.5 |

The ratio is **3.05:1**, so the bedside rule "**1 g CaCl₂ ≈ 3 g calcium gluconate**"
(≈270 mg elemental Ca²⁺ either way) is exactly correct. CaCl₂ is preferred via
central access for speed of ionised-calcium rise; peripheral extravasation risks
tissue necrosis, so calcium gluconate is the safe peripheral alternative at triple
the volume. This reproduces v1's 272/90 mg figures and supersedes the removed
Markovchick citation, which is unlocatable in PubMed.

### 3.2 Mechanistic subgroup: non-DHP responds; DHP often does not

The pharmacology predicts, and the case literature supports, a class gradient:

| CCB class | Agents | Calcium haemodynamic response | Evidence |
|-----------|--------|-------------------------------|----------|
| Phenylalkylamine | Verapamil | More consistent (BP + rhythm) | Moderate case-series congruence |
| Benzothiazepine | Diltiazem | More consistent than DHP | Limited but congruent |
| Dihydropyridine | Amlodipine, nifedipine | Inconsistent; vasopressors usually required | Inconsistent |

The landmark proof-of-concept is Woie & Storstein 1981 (PMID 7274286): refractory
verapamil poisoning (BP 83/63, HR 42, unresponsive to epinephrine and pacing)
reversed to MAP ~80 and sinus rhythm after 20 mL of 10% calcium gluconate.
Dihydropyridine toxicity, dominated by peripheral vasodilation and (for amlodipine)
a 30–50 h half-life, is mechanistically less amenable to competitive reversal — and
the corrected Nakamura 2025 case (PMID 40206927) illustrates the nuance: an
amlodipine-overdose patient in shock **refractory to calcium gluconate, glucagon
and catecholamines** nonetheless responded to **calcium chloride**, suggesting the
higher-elemental-content salt can matter when gluconate has failed. (v1 wrongly
described this case as CaCl₂ "with no additional therapy.")

### 3.3 Cohort descriptors (explicitly NOT calcium efficacy)

Two structured cohorts anchor the quantitative picture; both confound calcium with
multimodal care, so these are descriptors, not effects (Wilson 95% CIs; script):

**Cole 2018** (PMID 29452919) — 199 patients given high-dose insulin for BB/CCB
poisoning (66 CCB-only, 88 BB-only, 45 both): cohort-wide cardiac arrest **20.6%**
(41/199, 15.6–26.8), in-hospital death **15.6%** (31/199, 11.2–21.3), hypoglycaemia
**31%**. *These are whole-cohort figures*; v1's "41 of 66 CCB patients arrested" was
an error — the arrests are not isolable to the CCB subset, still less to calcium.

**Isbister 2024** (PMID 39305202) — 236 CCB overdoses, 2014–2023: amlodipine the
commonest agent **62.3%** (147/236), any IV calcium **18.6%** (44/236), high-dose
insulin **8.9%** (21/236), hypotension **38.6%** (91/236), death **3.0%** (7/236).
Dihydropyridine overdoses rose to a median 9/year (from 3/year the prior decade,
p<0.001), and diltiazem/verapamil drove the ICU and dysrhythmia burden — precisely
the agents where calcium is expected to help most.

### 3.4 Calcium versus HIET: complementary, not competing

| | IV calcium | HIET |
|---|-----------|------|
| Mechanism | Competitive L-type antagonism (↑ extracellular Ca²⁺) | Inotropy via restored myocardial glucose metabolism |
| Onset | 5–10 min | 30–45 min |
| Role | Immediate temporising bridge | Definitive metabolic support |
| Evidence | Case reports/series | Case series + observational cohorts |
| GRADE | VERY LOW | VERY LOW |

Expert consensus (St-Onge 2017, PMID 27749343; St-Onge systematic review 2014, PMID
25283255) positions calcium and HIET as complementary first-line agents. Shepherd &
Klein-Schwartz (PMID 15811898) found high-dose insulin outperformed calcium,
glucagon and catecholamines in animal models with 12/13 survival in early human
case experience; Krenz & Kaakeh (PMID 30141827) report 80–100% HIET success across
case series — figures that, like the calcium data, reflect multimodal management.

### 3.5 GRADE

| Domain | Assessment |
|--------|-----------|
| Design | Case reports/series + 2 observational cohorts → start VERY LOW |
| Risk of bias | High (publication + selection bias) — at floor |
| Large effect | Woie 1981 complete reversal → possible upgrade trigger |
| Dose-response | Pharmacologically plausible; not quantified → no upgrade |
| Confounding direction | Concurrent therapies → cannot isolate calcium → no upgrade |
| **Final** | **VERY LOW** |

The defensible evidence statement: *"We have very low confidence that IV calcium
improves survival in CCB toxicity; practice is supported by pharmacological
rationale and consistent, though confounded, haemodynamic case observations —
most reliably for non-dihydropyridine agents."*

## 4. Discussion

IV calcium sits in the same evidentiary position as most acute-toxicology
antidotes: universally recommended, never randomised. The correct framing is not
"unproven, therefore withhold," but "pharmacological reasoning plus consistent (if
confounded) case observations support use of a low-risk, rapidly-available agent in
a life-threatening condition where higher-quality evidence is neither available nor
ethically obtainable." A placebo-controlled RCT withholding an active agent from a
patient in cardiogenic shock would not pass review. The realistic evidence frontier
is not a trial but a **propensity-matched poison-centre registry analysis** — the
Cole and Isbister databases show such data exist and are underexploited.

Two practice points survive verification cleanly. First, the salt choice is a solved
arithmetic problem: CaCl₂ delivers 3× the elemental calcium of equal-volume
gluconate, central access permitting. Second, the class gradient is real and
actionable — verapamil/diltiazem toxicity is where calcium is most likely to buy
time, while amlodipine toxicity almost always needs HIET, vasopressors, and
sometimes extracorporeal support regardless of calcium.

## 5. Limitations

Publication bias is structural: successful case reports are preferentially
published, so the population response rate to calcium is unknowable from the
literature — which is exactly why no pooled rate is reported here. In every cohort
calcium was co-administered with vasopressors, HIET, or atropine, so its isolated
contribution cannot be determined. Outcome definitions are non-standardised. The
2020 AAPCC exposure/fatality figure could not be independently verified and is
flagged AS-CITED. The descriptive proportions in §3.3 are cohort statistics, not
efficacy estimates, and must not be read as such.

## 6. Conclusion

No RCTs exist for IV calcium in CCB toxicity, and none are ethically forthcoming.
Case-series evidence since 1981 consistently supports haemodynamic benefit, most
reliably for verapamil and diltiazem, where competitive L-type antagonism is
directly engaged. CaCl₂ 10% delivers 272.6 mg elemental Ca²⁺ per 10 mL — 3.05× the
content of equal-volume calcium gluconate (89.4 mg) — a difference that is
calculable, not conjectural, and that favours central CaCl₂ for speed while
peripheral gluconate is the safe alternative. GRADE VERY LOW for all outcomes;
calcium should be given promptly as a temporising bridge while HIET and other
definitive therapies are mobilised.

## 7. References (PMIDs re-verified against PubMed; corrections flagged)

1. Alshaya OA, et al. Calcium channel blocker toxicity: a practical approach. *J Multidiscip Healthc.* 2022;15:1851-1862. **PMID 36065348.**
2. Baid H, et al. Treatment modalities in calcium channel blocker overdose: a systematic review. *Cureus.* 2023;15(8):e42854. **PMID 37664357.** *(consolidates v1's duplicate self-reference ref 6)*
3. DeWitt CR, Waksman JC. Pharmacology, pathophysiology and management of calcium channel blocker and beta-blocker toxicity. *Toxicol Rev.* 2004;23(4):223-238. **PMID 15898828.**
4. Shepherd G, Klein-Schwartz W. High-dose insulin therapy for calcium-channel blocker overdose. *Ann Pharmacother.* 2005;39(5):923-930. **PMID 15811898.** **[corrected — v1's 15827071 = a linezolid serotonin-toxicity paper]**
5. Cole JB, Arens AM, Laes JR, et al. High dose insulin for beta-blocker and calcium channel-blocker poisoning. *Am J Emerg Med.* 2018;36(10):1817-1824. **PMID 29452919.** **[corrected — v1's 29472096 = a radiotherapy dosimetry paper]**
6. Nakamura S, Shinohara N. Successful use of calcium chloride in acute calcium channel blocker overdose with shock. *Cureus.* 2025;17(3):e80320. **PMID 40206927.**
7. Woie L, Storstein L. Successful treatment of suicidal verapamil poisoning with calcium gluconate. *Eur Heart J.* 1981;2(3):239-242. **PMID 7274286.**
8. St-Onge M, et al. Treatment for calcium channel blocker poisoning: a systematic review. *Clin Toxicol.* 2014;52(9):926-944. **PMID 25283255.**
9. St-Onge M, et al. Experts consensus recommendations for the management of calcium channel blocker poisoning in adults. *Crit Care Med.* 2017;45(3):e306-e315. **PMID 27749343.**
10. Krenz JR, Kaakeh Y. An overview of hyperinsulinemic-euglycemic therapy in calcium channel blocker and β-blocker overdose. *Pharmacotherapy.* 2018;38(11):1130-1142. **PMID 30141827.**
11. Woodward C, Pourmand A, Mazer-Amirshahi M. High dose insulin therapy for beta blocker/calcium channel blocker toxicity. *Daru.* 2014;22(1):36. **PMID 24713415.**
12. Isbister GK, Jenkins S, Harris K, Downes MA, Isoardi KZ. Calcium channel blocker overdose: not all the same toxicity. *Br J Clin Pharmacol.* 2025;91(3):740-747. **PMID 39305202.** **[corrected — v1 had no PMID and wrong pages 91(1):98-107]**
13. Olson KR, et al. Calcium channel blocker ingestion: an evidence-based consensus guideline for out-of-hospital management. *Clin Toxicol.* 2005;43(7):797-822. **PMID 16440509.** *(added — verifiable 2003 poison-centre denominator)*

**Removed as unlocatable in PubMed (reproduce-or-remove):** v1 ref 4 "Wax PM,
Donovan JW. A clinical review of the management of calcium channel blocker
toxicity. *J Toxicol Clin Toxicol.* 2001;39(4):305-314" (v1 PMID 11480460 = a
paediatric-burns fluid-resuscitation paper; no such Wax/Donovan article is
retrievable). v1 ref 10 "Markovchick V. Calcium gluconate for calcium channel
blocker toxicity. *Ann Emerg Med.* 1988;17(7):664-666" (v1 PMID 3132982 = a
dicarboxylic-acid biochemistry paper; 3377302 at that page is an ED-design letter;
no Markovchick calcium article is retrievable). Both claims are re-anchored on the
derived stoichiometry (§3.1) and the verified reviews above.

---

*DRAFT for author review — not for live publication without sign-off. All numerals
regenerated by `30-iv-calcium-ccb-verify.py`. According to PubMed metadata, every
retained PMID was verified by title/journal/pages match on 2026-07-09. No RCT
exists; nothing here is a pooled treatment effect.*
