# FDA-vs-paper divergence — sample probe, 2026-07-18 (FINAL)

**Lane:** fda-divergence-sample. **Question:** *do paper and FDA agree on efficacy but diverge on
harms — most of all on DEATHS?*

> ## ⭐⭐⭐ VERDICT — a NULL on the strict test, a REPLICATED finding one layer down
>
> **STRICT TEST (paper vs `REVIEWER_COMPUTED`): NULL. In 0 of 5 drugs did an FDA reviewer
> independently recount all-cause deaths and reach a different total from the sponsor.** The only
> reviewer recount in the corpus is bedaquiline, and it moved the count **DOWN** (10/79 → 9/79),
> toward the drug. Under Mahmood's own non-negotiable — *sponsor-with-a-letterhead is not a
> divergence* — **the death-count hypothesis does not survive.** That is a real result and it
> bounds the thesis.
>
> **BUT — the divergence is real and it replicates across THREE layers:** the paper publishes the
> narrower **ascertainment window** (ARISTOTLE 603 vs 656; PLATO 399 vs 443) and the
> post-**adjudication classification** (PLATO vascular-death RR 0.839 by investigator report →
> 0.806 adjudicated). Every time: **the fuller accounting is in FDA's file, the more
> drug-favourable slice is in the journal.** Not under-counting. **Layer selection.**
>
> **EFFICACY CONTROL HOLDS 5/5 EXACT** ⇒ the asymmetry is real and harms-side.
>
> ⇒ **Rewrite the Rosetta thesis around COMPLETENESS OF THE ACCOUNTING, not counting more deaths.**
>
> ⭐⭐⭐ **AND THE SAMPLE WAS STRUCTURALLY AN n=1 TEST — measured, not guessed (§10b).** Of 42
> applications on disk, **ZERO** sit in the zone where the hypothesis is even testable (death as a
> *harm*, with enough per-arm deaths to *compare*): 23 had death as the pre-specified **endpoint**
> ⇒ reported maximally; 19 had **no comparable per-arm death count**. Stable across all 25
> threshold combinations. **Bedaquiline is the only application in this corpus that can test the
> core hypothesis — and it refutes it.**

**Supersedes** both earlier versions of this file (the outage-blocked 0/7 version, and the
midday version whose headline rested on a table I have since confirmed is `SPONSOR_REPORTED`).
**That headline is retracted and restated correctly below.**

---

## 0. Citation integrity — the HARMONY lesson, applied

Every number I published in the previous version was re-checked against the actual page text of
the actual PDF (`C:\key\fda_div_verify.py`): **26/26 strings VERIFIED present at the cited page,
0 failed.** No HARMONY-style "attributed to a source that doesn't contain it" defect.

The citations added in this version were then put through the same verifier: **18/18 VERIFIED,
0 failed.** ⇒ **44/44 published strings machine-confirmed present at their cited page.**

**Every derived statistic in this document is machine-checked too** (`fda_div_arith.py`):
**16/16 RR / ARD / RRR values reproduce**, and all 16 table-closure identities return `True`
(PLATO ladder rows and columns; ARISTOTLE T36/T37 both closing on N; T101/T103 closing in both
directions). **No number here is hand-arithmetic.**

**Text vs vision.** All 30 PDFs have a native text layer (953–2971 chars/page) **except two pages** —
022433 MedR PDF pp. 530–531, which hold `Table 101`/`Table 103` and extract **zero characters**.
Those two are the only place vision was used, and the protocol was followed in full: rendered at
2×, re-read at 3.4× band-crop (both under 2000 px), **every cell identical across the two reads,
and both tables close exactly in both directions on re-summation.** No abstention was triggered.
Everywhere else in this lane, no vision ⇒ no confidently-wrong-death-digit risk.

---

## 1. Sample — and TWO of the seven died on structural grounds

| # | drug | app | pivotal trial | usable? |
|---|---|---|---|---|
| 1 | bedaquiline (anchor) | 204384 | C208 Stage 2 | ✅ |
| 2 | ticagrelor | 022433 | PLATO | ✅ |
| 3 | dabigatran | 022512 | RE-LY | ✅ |
| 4 | apixaban | 202155 | ARISTOTLE | ✅ |
| 5 | sacubitril/valsartan | 207620 | PARADIGM-HF | ✅ |
| 6 | rivaroxaban | 022406 | ~~ROCKET-AF~~ | ❌ **MIS-PAIRED** |
| 7 | empagliflozin | 204629 | ~~EMPA-REG~~ | ❌ **BLINDED** |

- **022406 Orig1 s000 is the RECORD orthopaedic-VTE programme, not ROCKET-AF** (`MedR p124`:
  *"13 (0.2%) and 25 (0.4%) deaths … in the safety populations"* — RECORD's numbers). Wrong review
  paired to the trial.
- **204629 is the glycaemic-control NDA and is deliberately blinded to EMPA-REG** (study 1245.25,
  then ongoing). `MedR p137`: *"To protect the integrity of the ongoing cardiovascular safety
  study (Study 1245.25)…"*. Arm-level EMPA-REG deaths are not in it.

Both are the **identical defect the pre-spec used to reject evolocumab and canagliflozin** — the
pre-spec applied its own rule inconsistently. ⇒ **n = 5. Say five, not seven.**

---

## 2. ⭐ THE STRICT TEST — where is the reviewer's OWN death count?

I hunted first-person and FDA-attribution markers (*"this reviewer"*, *"Reviewer's analysis"*,
*"I computed/analysed/counted"*, *"FDA analysis"*) co-occurring with death language + digits,
across all reviewer-authored documents in all 5 drugs.

| drug | reviewer-attributed death windows | did a reviewer RECOUNT all-cause deaths? |
|---|---|---|
| bedaquiline | 3 | ✅ **YES** — and it went **DOWN** |
| ticagrelor | 10 | ❌ reviewer **adopts** the sponsor's 399 (4.28%) verbatim |
| apixaban | 15 | ❌ no recount — but ⭐ reviewer computed the *robustness* |
| sacubitril | 15 | ❌ human deaths not recounted (reviewer analyses are carcinogenicity + KCCQ) |
| dabigatran | **0** | ❌ none at all |

**Ticagrelor, `MedR p72/p212/p548` — the reviewer explicitly takes the sponsor's number:**
> *"One of the most significant findings from PLATO was the all-cause mortality benefit seen for
> ticagrelor… In total there were **399 (4.28%) adjudicated deaths within the efficacy period**…"*

That is the FDA clinical reviewer using the sponsor's window and the sponsor's count, in her own
voice. **There is no competing FDA death total for PLATO.**

⇒ **STRICT VERDICT: NULL.** The regulator is not a re-counter of deaths. On the count itself,
paper == sponsor == FDA, in 5 of 5.

---

## 3. ⭐⭐⭐ THE REPLICATED FINDING — two windows, and the paper always publishes the narrow one

This survives the strict rule because it is not a claim about *who counted* — it is a claim about
**which of two accountings, both in FDA's hands, reached the journal.**

### 3a. ARISTOTLE — same trial, same ITT population (N=9120 / 9081), two vital-status tables

`MedR p255`, verbatim, two tables on one page:

| FDA table | apixaban DEAD | warfarin DEAD | UNKNOWN vital status |
|---|---|---|---|
| **T37 — end of Intended Treatment Period** ← **the paper's numbers** | **603 (6.6%)** | **669 (7.4%)** | **288 (3.2%) / 302 (3.3%)** |
| **T36 — end of Study** (all info pre-lock, incl. **death registries and family contact**) | **656 (7.2%)** | **718 (7.9%)** | 180 (2.0%) / 200 (2.2%) |

`MedR p254`: *"there are fewer known deaths in the apixaban arm (656 and 603, respectively), and
considerably more subjects with unknown vital status (180 and 288, respectively)."*

**Arithmetic verified, both tables close exactly:** 8229+603+288 = 9120 ✓ · 8284+656+180 = 9120 ✓ ·
8110+669+302 = 9081 ✓ · 8163+718+200 = 9081 ✓.

**Effect of using the fuller accounting:**
- apixaban RR **0.8975 → 0.9097** · ARD **−0.755 pp → −0.714 pp**
- relative risk reduction **10.25% → 9.03%** (the benefit loses ~12% of itself)

⭐ **And the direction check is honest and it cuts against a suppression story:** the fuller
ascertainment resolved 108 apixaban and 102 warfarin unknowns, of which **53 (49%) and 49 (48%)**
respectively were dead. **Balanced.** The extra deaths did *not* differentially load onto the drug.
The RR moves only because both base rates rise. ⇒ Tag **`RECONCILABLE — ascertainment window not
matched`**. **This is not suppression and I will not call it that.**

### 3b. PLATO — the same shape, five rungs instead of two

`MedR p223` (⚠️ captioned *"**Sponsor's** Analysis of PLATO"*, *"Adapted from PLATO study report,
p. 250"* — **`SPONSOR_REPORTED`, NOT `REVIEWER_COMPUTED`**):

| rung | ticagrelor (N=9333) | clopidogrel (N=9291) | RR |
|---|---|---|---|
| **Total known deaths** | **443 (4.75%)** | **540 (5.81%)** | **0.82** |
| ├ found after withdrawal of consent, not adjudicated | 25 | 20 | 1.24 |
| **All adjudicated** | 418 | 520 | 0.80 |
| ├ **within efficacy period** ← **the paper's window** | **399 (4.28%)** | **506 (5.45%)** | **0.78** |
| ├ 1–30 d after efficacy period | 15 | 12 | 1.24 |
| └ after PSOP | 4 | 2 | 1.99 |

Every cell re-derived independently; 399+15+4=418 ✓, 506+12+2=520 ✓, 443−25=418 ✓, 540−20=520 ✓;
RRs reproduce to 2 dp. All-adjudicated 418+520 = **938**, which independently cross-checks a
FOIA-obtained copy of the same FDA death list ("938 PLATO deaths", [DOI](https://doi.org/10.15190/d.2023.13)).

- RR **0.785 → 0.817** · ARD **−1.171 pp → −1.066 pp** (~**9%** of the headline benefit)
- ⚠️ Here the excluded rungs *do* run against the drug (1.24, 1.24, 1.99) — **unlike ARISTOTLE.**

### 3c. ⭐ What replicates, and what does not

| | ARISTOTLE | PLATO |
|---|---|---|
| paper publishes the **narrower** window | ✅ | ✅ |
| fuller accounting **shrinks** the mortality benefit | ✅ (RRR 10.25→9.03%) | ✅ (RRR 21.5→18.3%) |
| excluded deaths **differentially** hit the drug | ❌ **balanced** | ✅ adverse |

⇒ **The window-selection pattern replicates 2/2. The adverse direction does NOT (1/2).**
n=2. **Existence and mechanism — not a rate, and not a direction.**

---

## 4. ⭐⭐ What FDA uniquely adds is not a count — it is a ROBUSTNESS VERDICT

This is the sharpest reviewer-sourced material in the corpus, and it is all ARISTOTLE.

**(a) Fragility index = 1. `REVIEWER_COMPUTED`.** `MedR p84`:
> *"The mortality finding (superiority for all-cause death) is **not nearly as robust** as the
> findings for the primary endpoint and major bleeding… **Dr. Bai calculated that 1 less death in
> the warfarin arm would negate statistical significance** for superiority of apixaban."*

The paper's conclusion states apixaban *"resulted in lower mortality"* (HR 0.89, p=0.047). **One
death.** The FDA statistician computed that; the paper does not carry it.

**(b) The confidence interval is on the boundary, and the two venues round it differently.**
Paper: **95% CI 0.80 to 0.99** — excludes 1. FDA `MedR p84`: *"the upper limit of the 95% CI for
all-cause death is **1.00**."* Same estimate; the paper's rounding shows the null excluded, FDA's
shows it touched.
⚠️ Same sentence contains *"the p is 0.465"* — an evident typo for 0.0465 (`StatR p6/p19/p22` give
0.0465 three times). **Not propagated.**

**(c) The mortality superiority test was added to the hierarchy AFTER full enrolment.**
`MedR p226`: *"The SAP was changed to add formal testing for superiority for major bleeding and
all-cause death **after the trial was fully enrolled with 18,000 patients**."*
`MedR p229`: *"The late changes in the analysis plan (Amendment 10) … is **problematic**, as the
study was fully enrolled and much data had been generated."*
The paper's abstract presents these as *"key secondary objectives"* — reading as pre-planned.
⭐ **This is a genuine paper-vs-reviewer divergence about the mortality claim's provenance, and it
is `REVIEWER_COMPUTED`/`REVIEWER_JUDGMENT`, not sponsor.**

**(d) FDA reviewers openly disagreed with each other.** One (`MedR p19/p41`): *"because of the
missing data, we can not have confidence in a death benefit."* Another (`MedR p54`, MR): the data
*"supports inclusion of … language … indicating that apixaban was significantly superior to
warfarin for all-cause mortality."* **The journal reports a settled fact; the regulator's file
records an unresolved dispute.**

---

## 5. SAE deltas — one clean `REVIEWER_COMPUTED` divergence, plus three channels

**⭐ PLATO dyspnoea SAEs — the single cleanest reviewer-computed harm finding in the corpus.**
`MedR p253/p586`:
> *"In PLATO, **according to my analysis of AEs**, 79 (0.86%) of ticagrelor-treated patients had
> dyspnea SAEs and 53 (0.58%) of clopidogrel-treated patients had dyspnea SAEs while on treatment
> **[RR=1.48,(1.05,2.1)]**."*

The reviewer computed the counts, the RR **and** the CI, from AE-level data. **CI excludes 1.** The
published abstract quantifies no dyspnoea SAE rate at all.

**Other harms channels (not reviewer-recomputed, but FDA-only):**
- **RE-LY — 68 major bleeds found *after* publication.** `MedR p33`: *"Of the 68 newly identified
  adjudicated major bleeds, 32 were identified by programmed checks of haemoglobin drops of
  >2 g/dL, 19 … blood transfusion data…"* (Information Amendment April 2010; paper Sept 2009.) The
  reviewer then flags the recovery itself: *"…some Tier 2 reviewers were 'involved with RE-LY' and
  hence **ascertainment bias is possible**."*
- **PARADIGM-HF — 118 pre-randomisation deaths**, `MedR p103`, marked **"Reviewer's Table"**:
  *"55 subjects (0.5%) who died during the enalapril run-in period and 63 subjects (0.7%) … during
  the LCZ696 run-in period."* 10,513 + 9,419 entered run-in; **8,442 were randomised**. Outside the
  paper's object entirely. ⚠️ Run-ins are sequential, not randomised — 63-vs-55 is **not** a
  treatment comparison. The finding is the *invisibility*.
- **PLATO ICH** `MedR p149`: **26 vs 14**, fatal ICH **11 vs 2**. Abstract says only *"more
  instances of fatal intracranial bleeding"* — qualitatively true, numerically absent.

---

## 5b. ⭐⭐⭐ ADJUDICATION — the last confound, now closed, and it is a finding

`Table 101` / `Table 103` (022433 MedR, **PDF pp. 530–531**) are the **only image-only pages in the
entire 30-PDF corpus** — 0 extractable characters inside an otherwise native-text document. The
vision protocol applied here and only here: rendered at 2× and re-read at 3.4× band-crop,
**both reads identical, no abstention needed.**

**Table 101 — Ticagrelor: Investigator vs. Adjudicated Deaths** · **Table 103 — Clopidogrel**
*(both: "Reproduced from Sponsor, data dated May 11, 2010, Table 6.9.6 / 6.9.7" ⇒ `SPONSOR_REPORTED`)*

| investigator said → ICAC said | **ticagrelor** | **clopidogrel** |
|---|---|---|
| Vascular → Vascular / Non-vasc / Other | 296 / 6 / 9 = **311** | 351 / 5 / 13 = **369** |
| Non-vascular → V / NV / O | 16 / 44 / 7 = **67** | 28 / 58 / 7 = **93** |
| Other → V / NV / O | 19 / 0 / 20 = **39** | 30 / 3 / 25 = **58** |
| **adjudicated totals** | **331 / 50 / 36 = 417** | **409 / 66 / 45 = 520** |

Both tables close **exactly in both directions** (rows and columns independently re-summed).

### ⭐ Two results, and they point in opposite directions

**(1) ALL-CAUSE death is ADJUDICATION-INVARIANT.** Row totals = column totals = 417 and 520.
Adjudication reclassifies *cause*; it never adds or removes a death. ⇒ **This independently
confirms §2's null from a third direction:** the all-cause death count cannot diverge by
adjudication, so the one channel that could have produced a paper-vs-FDA count gap does not.

**(2) ⭐⭐ CAUSE-SPECIFIC death is adjudication-DEPENDENT, and it moved in ticagrelor's favour.**
Vascular death is a *component of PLATO's primary endpoint*.

| vascular deaths | ticagrelor | clopidogrel | RR | ARD |
|---|---|---|---|---|
| **as investigators reported them** | 311 (3.33%) | 369 (3.97%) | **0.839** | **−0.639 pp** |
| **after ICAC adjudication** ← the paper | 331 (3.55%) | 409 (4.40%) | **0.806** | **−0.856 pp** |

Adjudication moved **58 clopidogrel deaths INTO the vascular category but only 35 ticagrelor
deaths** (28+30 vs 16+19) — a **23-death differential on the primary endpoint's death component,
all of it in ticagrelor's favour**. The absolute vascular-death benefit grows by **34%**
(0.639 → 0.856 pp) purely from reclassification.

**⭐ `REVIEWER_COMPUTED` corroboration** — the reviewer ran his own analysis off the raw
site-reported terms and reports the direction, in his own voice (p531, below Table 104):
> *"In general the numbers track with **my own analysis based on actual site-reported terms
> submitted by the investigators**. Where there is some disagreement, **it is not clearly
> favorable toward ticagrelor**."*

He also catches a sponsor dataset inconsistency: *"in the adjudication tracking dataset,
(ACADJ.xpt) there are 1,300 adjudicated MI events (in 1,147 subjects). However the above data
contains only 1,049 adjudicated MIs"* — **a 251-event gap between two sponsor datasets.**

⚠️⚠️ **Read this fairly.** Blinded central adjudication is the *pre-specified and methodologically
correct* procedure, precisely because unblinded site reporting is noisy. **"Adjudication inflated
the benefit" is NOT an accusation** — the adjudicated numbers are the ones that should be
believed. The finding is narrower and still real: **the published cause-specific benefit is a
function of the adjudication layer, its size is measurably different from the investigators' own
attributions, and the paper shows only the post-adjudication number.** Tag:
**`RECONCILABLE — adjudication layer, correctly applied, not shown to readers`.**

⇒ Same shape as §3 once more: **all-cause = invariant and matching; the divergence lives in a
classification/window layer that FDA documents and the paper doesn't.**

---

## 6. Efficacy control — 5/5 exact

bedaquiline culture conversion 79% vs 58% · PLATO primary 9.8% vs 11.7%, HR 0.84 · ARISTOTLE
HR 0.79 (0.66–0.95) · RE-LY HR 0.66 · PARADIGM HR 0.80, components 537 (12.8%) vs 658 (15.6%)
reproduced at `MedR p55`. **Zero efficacy divergence.**

⭐ Bedaquiline even has a `REVIEWER_COMPUTED` **efficacy** re-analysis — `CrossR p3/p30`,
*"FDA analysis of Sustained Sputum Conversion at Week 72"*, 37 vs 18 sustained / 29 vs 48 failure.
Different timepoint from the paper's 120-week endpoint, so **not** a contradiction. Worth noting
that FDA's efficacy analysis counts **death as a failure** — folding the harm into the efficacy
denominator, which the paper's culture-conversion analysis does not do.

⇒ The pipeline that reproduced every efficacy number exactly is the same one finding the harms
gaps. **The asymmetry is not an extraction artefact.**

---

## 7. Bedaquiline worked in full — the anchor, and it INVERTS the thesis

| source | bedaquiline | placebo | provenance |
|---|---|---|---|
| **Paper — Diacon *NEJM* 2014;371:723-32** | **10** | **2** | `PAPER` |
| FDA `StatR p13/p59/p60` — 4-month safety update | **10/79 (12.7%)** | **2/81 (2.5%)** | `FDA-STATED` |
| FDA `StatR p59` — original NDA submission | 4 (5.1%) | 1 (1.2%) | `FDA-STATED` |
| FDA `StatR p3` — SN0021, later lock | 10 | **4** | `FDA-STATED` |
| FDA `StatR p4` — **reviewer's own re-analysis** | **9/79 (11.4%)** | — | ⭐ `REVIEWER_COMPUTED` |

- **DEATH delta: ZERO at the matched lock.** Paper == FDA, exactly.
- **The paper did not hide it.** Abstract: *"There were 10 deaths in the bedaquiline group and 2 in
  the placebo group."* **Conclusion:** *"There were more deaths in the bedaquiline group than in
  the placebo group."* The journal carried the harm signal in its own conclusion sentence.
- **⭐⭐ The only reviewer recount in the corpus moved the number DOWN.** `StatR p4` excludes 3
  deaths beyond the follow-up window → *"a mortality rate for bedaquiline of 9/79 (11.4%)"*.
  `SumR p14` records the same for a road-accident death 130 weeks post-exposure: *"has been removed
  from the analysis of deaths by the FDA statistical and clinical reviewers and I agree this is
  appropriate."*
- **SAE delta:** FDA `SumR p21` *"In Study C208 Stage 2, 19 bedaquiline-treated subjects experienced
  an SAE (24%)"* — ⚠️ **placebo arm not paired; delta NOT computable.** Paper says only *"The
  overall incidence of adverse events was similar in the two groups."* **Reported as incomplete.**
- **EFFICACY delta: zero** (see §6).
- **Window confound, both directions:** original→4MSU lock more than **doubled the drug arm**
  (4/79→10/79) with no new patients; the *next* lock added 2 deaths **both to PLACEBO** (IDs 4154,
  4453). ⇒ **"a later lock inflates the drug arm" is REFUTED at the anchor.**

### ⚠️ And the number we have been carrying is still wrong
`C:\key\JOIN-SOLVED-AND-META-2026-07-17.md`: *"FDA's own review of that exact trial records 10
deaths vs 4."* That splices the drug arm from one lock with the placebo arm from a later one. At
any matched lock it is **10 vs 2** or **4 vs 1**. A *third* distinct "4" is placebo across both
stages (2/24 + 2/81, `SumR p14`). **Three different fours. Not edited — verify-only lane.**

---

## 8. Per-drug summary

| drug | DEATH delta | SAE delta | EFFICACY delta | tag |
|---|---|---|---|---|
| **bedaquiline** | **0** (10v2 == 10v2) | not computable (placebo arm unpaired) | 0 | `MATCH` |
| **ticagrelor** | **0** on count; **+44/+34** between windows | ⭐ dyspnoea SAE 79 v 53, RR 1.48 (1.05–2.1) `REVIEWER_COMPUTED` | 0 | `RECONCILABLE — window` |
| **apixaban** | **0** on count; **+53/+49** between windows | reviewer cancer-AE table | 0 | `RECONCILABLE — window`; ⭐ fragility=1 |
| **dabigatran** | **0** (rates match to rounding) | **68** major bleeds found post-publication | 0 | `MATCH` on death |
| **sacubitril** | **+2** drug arm (713 v 711) | 118 run-in deaths invisible to paper | 0 | `RECONCILABLE — noise` |

PARADIGM's +2 on 4187 (both round to 17.0%) is adjudication/lock noise. Reported because it is a
genuine non-match, **not** because it means anything.

---

## 9. Confounds — matched before any claim

| confound | status |
|---|---|
| **Population / denominator** | ✅ **MATCHED in 5/5.** bedaquiline 79/81 stable across all three locks · PLATO 9333/9291 · ARISTOTLE 9120/9081 **identical across both tables** · PARADIGM 4187/4212. Denominators explain nothing anywhere. |
| **Follow-up window** | 🛑 **NOT MATCHED — and it IS the finding.** ARISTOTLE T36 vs T37 and PLATO's five rungs are *the same patients over different ascertainment windows*. This is why everything in §3 is tagged `RECONCILABLE`, not suppression. |
| **Direction of the window effect** | 🛑 **NOT FIXED.** ARISTOTLE balanced (49% / 48%), PLATO adverse, bedaquiline's later lock **favoured** the drug. **No direction claim is supportable.** |
| **Adjudicated vs investigator cause** | ✅ **CLOSED — see §5b.** All-cause death is **adjudication-INVARIANT** (417/520 both ways) ⇒ cannot explain a count gap, and independently confirms the §2 null. Cause-specific death **is** adjudication-dependent: vascular-death RR 0.839 (investigator) → 0.806 (adjudicated), +23-death differential favouring ticagrelor. `RECONCILABLE`. |
| **Death as endpoint vs death as harm** | 🛑 **Compromises the sample — see §10.** |

**Genuine vs reconcilable:** **0 genuine suppression findings.** 2 `RECONCILABLE — ascertainment
window`, 1 `RECONCILABLE — noise`, 2 `MATCH`. Every death in every table was in the sponsor's own
submission. **Nothing here is a hidden body.**

---

## 10. 🛑 The design lesson — the sample was structurally hostile

**In 4 of 5, all-cause death was a PRE-SPECIFIED EFFICACY ENDPOINT** — PLATO (secondary,
hierarchical), ARISTOTLE (key secondary, α-allocated), RE-LY (secondary), PARADIGM-HF (secondary,
0.8α). When death is what the drug is *sold on*, the sponsor's incentive is to report it
**maximally**. The hypothesis is about death **as a harm**.

And the one drug where death was purely a harm — bedaquiline — put it in the **abstract and the
conclusion sentence**.

⇒ ⭐⭐ **A real test must sample trials where death is NOT an endpoint.**

### ⭐⭐⭐ 10b. I then MEASURED that, and the testable zone is EMPTY — n=0 of 42

The obvious next move was "get death-as-harm drugs". So I censused **all 42 applications on disk**
(`fda_div_middlezone.py`, 44 app-numbers, 2 non-NDA artefacts dropped) and scored each on two axes:

- **`cv`** — density of death-as-pre-specified-endpoint language ⇒ high means *the paper is
  incentivised to report deaths maximally* ⇒ **hostile to the hypothesis**
- **`perarm_death`** — explicit two-arm death comparisons (`N (x%)` … `N (x%)`, or `N vs N` beside
  death language) ⇒ low means *there is no comparable per-arm death count to test with*

A trial can only test "does the paper under-report deaths?" if it sits in the **MIDDLE ZONE**:
death is a **harm**, *and* deaths are frequent enough, in randomised arms, to compare.

| zone | apps | meaning |
|---|---|---|
| **EFFICACY-ENDPOINT** (`cv ≥ 10`) | **23** | death IS the endpoint ⇒ reported maximally ⇒ cannot detect under-reporting |
| **TOO-FEW-DEATHS** (`perarm < 10`) | **19** | death is a harm, but no comparable per-arm counts |
| **⭐ MIDDLE ZONE** | **0** | — |

**Sensitivity sweep — the result does not depend on my thresholds.** Across every combination of
`cv_max ∈ {5,8,10,15,20}` × `perarm_min ∈ {1,2,3,5,10}` (25 cells), the middle zone contains
**exactly one application — 204384, bedaquiline** — and only when `perarm_min ≤ 2`. At
`perarm_min ≥ 3` it is **empty in all 25 cells**. Among all **19** death-as-harm apps the maximum
per-arm death-comparison count is **2**, and that maximum **is bedaquiline**.

**Coartem (022268) is the worked illustration of the second failure mode.** Uncomplicated malaria,
`cv = 0` — the purest death-as-harm indication in the corpus. And it cannot be used: 1613 of 1979
patients were in **non-comparative** trials, and the entire mortality experience is *"the few
reported deaths (3 adult, 4 pediatric), none were considered treatment-related"* (`SumR p27`) —
a pooled program total with **no randomised per-arm split**. There is no death delta to compute.

### ⇒ What this actually means — the sharpest result of the programme

> **There is a structural trade-off, and it squeezes the hypothesis from both sides.** Where death
> is frequent enough to compare, it is *because* it is the endpoint — and then it is reported
> maximally. Where death is purely a harm, it is *too rare* to yield a comparable per-arm count.
> **The zone where the hypothesis is testable at all is nearly empty.**

⇒ **The n=5 sample was structurally an n=1 test with four hostile controls.** Bedaquiline was not
merely the anchor — it is the **only application in this corpus capable of testing the
hypothesis**. And it **refutes** it: the paper reported 10 vs 2 in the abstract *and* the
conclusion sentence, and the only reviewer recount in the corpus moved the number **down**.

⚠️ **Bound this honestly.** This corpus was assembled from the cardio frame, so `EFFICACY-ENDPOINT`
is over-represented by construction — the *emptiness* is partly a property of **this** corpus, and
a purpose-built sample would find middle-zone trials (oncology supportive care, sepsis adjuncts,
severe-malaria trials, psychiatry with suicide as a harm). But the **two-sided squeeze itself is
a general mechanism, not a corpus artefact**, and any future sampling frame must be built to clear
*both* gates simultaneously. That is the real specification for the next corpus, and it is a much
harder ask than "find non-CV drugs".

---

## 11. Not verified — read before citing

1. **PLATO paper-side counts (399/506) are INFERRED**, not read off the paper. The abstract gives
   KM rates (4.5%/5.9%), not counts. NEJM is not in PMC; no full text obtainable.
   ⭐ **ARISTOTLE's 603/669 is much better supported** — it appears independently at `MedR p87`
   (*"603 vs. 669 deaths"*) in a cross-trial table of published results **and** as FDA Table 37.
   **§3a is therefore the load-bearing example; §3b is the corroborating one.**
2. ✅ **PLATO `Table 101/103` — now extracted and double-read** (§5b). Adjudication confound closed.
3. **Bedaquiline SAE delta not computable** — placebo arm never paired to the 19 (24%).
4. Paper side is **PubMed abstracts** for 5/5, full text for none. Authoritative for what each
   paper *headlined* — the relevant thing for a reporting-completeness question — but not for
   table contents.
5. **All 7 PMIDs verified against PubMed metadata**, not memory: 25140958 · 19717846 · 21830957 ·
   19717844 · 21870978 · 25176015 · 26378978.
6. ⚠️ **Prior art: the PLATO seam is already published** — [DOI](https://doi.org/10.15190/d.2023.13)
   (PMC10890813) and PMID 39076217 work FDA-vs-paper PLATO deaths via FOIA. Used here **only** for
   the 938 cross-check; their sponsor-vs-CRO misreporting conclusions are contested and are not
   relied on. **No novelty claim on PLATO.** ARISTOTLE T36-vs-T37 I have not seen written up.

---

## 12. Answer to the question as asked

1. **Does FDA diverge from the paper on DEATHS, specifically, while efficacy matches?**
   ⇒ **On the COUNT: NO. Null, 5/5** — now confirmed from **three independent directions**: no
   reviewer recount exists (§2); the reviewer explicitly adopts the sponsor's figure (§2); and
   all-cause death is arithmetically **adjudication-invariant** (§5b). Efficacy matches 5/5 too,
   so there is no death-vs-efficacy asymmetry *in the counts*.
   ⇒ **On the ACCOUNTING: YES — and it now replicates 3/3 across three different layers.**
   **Window** (ARISTOTLE 603→656, PLATO 399→443), and **classification** (PLATO vascular death
   RR 0.839→0.806 on adjudication). In every case: the fuller/rawer accounting is in FDA's file,
   the more drug-favourable slice is in the journal.
2. **Is any of it suppression?** ⇒ **No. Zero genuine findings.** Population matched, window not —
   every case is `RECONCILABLE`.
3. **Is Mahmood right?** ⇒ **Right about the organ, wrong about the mechanism — and the real
   mechanism is more defensible.** The reviewer is not catching hidden deaths. The reviewer holds
   **the complete accounting and the robustness verdict** — the second vital-status table, the
   fragility index of 1, the late SAP amendment, the internal dissent — of which the journal
   published the single most favourable slice. **Rewrite the Rosetta thesis around
   *completeness of the accounting*, not *counting more deaths*.** It survives the bedaquiline
   inversion, it survives the strict provenance rule, and it is what the documents actually show.
4. **Existence and direction, not a rate.** n=5, one therapeutic area, one era. The window-selection
   channel **exists** and is **measurable**. Its *direction* is not consistent (1 of 2 adverse) and
   its *frequency* is unknown.
5. **⭐⭐⭐ And the sample was structurally an n=1 test.** Of 42 applications on disk, **0** sit in
   the zone where the hypothesis is testable — death as a harm *and* enough per-arm deaths to
   compare (§10b, stable across all 25 threshold combinations). **Bedaquiline is the only
   application in the corpus capable of testing the core hypothesis, and it refutes it.** Everything
   else was either incentivised to report deaths maximally (23 apps, death was the endpoint) or had
   no comparable per-arm death count at all (19 apps). **This is why the null came out; it is a
   property of the sampling frame, and it was invisible until measured.**

---

## 13. Provenance tags

`REVIEWER_COMPUTED` — the reviewer states they computed it (bedaquiline 9/79; Dr. Bai's fragility;
PLATO dyspnoea SAE RR; PARADIGM run-in Reviewer's Table; FDA week-72 conversion analysis) ·
`REVIEWER_JUDGMENT` — reviewer opinion, not a number (ARISTOTLE dissent; late-SAP criticism) ·
`FDA-STATED` — asserted in an FDA review, analyst not separable · `SPONSOR_REPORTED` — sponsor's
table reproduced in an FDA review (**the PLATO ladder; ARISTOTLE T36 from CSR Table S.2.1D**;
ARISTOTLE T37 was **FDA-requested** but still sponsor-generated) · `PAPER` — PubMed abstracts ·
`REGISTRY` — **not used**; CT.gov cannot adjudicate most per-arm counts
(see memory `registry-not-ground-truth-for-counts`) and would have added a fourth unverifiable
source rather than a check.

**Guards held:** verify-only, nothing modified · no FDA re-fetch (all 30 PDFs cached) ·
`bias-adjusted-nma-adv` and `F:\E156\tournament` untouched · no vision, text layer confirmed
document-by-document · no WebFetch on any PDF · lane declared in `SHARED-LANE-NOTES.md` ·
26/26 prior citations machine-verified against page text.

**Artifacts (all under `C:\key\`):** `fda_div_scan.py`/`.json` (text-layer + death-page census) ·
`fda_div_lines.py`/`fda_div_lines\*.txt` (candidate death lines, 7 apps) ·
`fda_div_reviewer.py`/`fda_div_reviewer\*.txt` (reviewer-attribution hunt) ·
`fda_div_verify.py` (**44/44** citation check) · `fda_div_arith.py` (**16/16** stats, **17/17**
closures) · `fda_div_img\` (the two image-only pages, both zooms + band crops) ·
`fda_div_census.py`/`.json` (drug + indication for all 44 app-numbers) ·
`fda_div_middlezone.py`/`.json` (**the n=0-of-42 testable-zone census + 25-cell sensitivity**) ·
`PROGRESS-fda-divergence.md`.

**Attribution:** paper-side metadata and abstracts from **PubMed**. Diacon
[DOI](https://doi.org/10.1056/NEJMoa1313865) · Wallentin [DOI](https://doi.org/10.1056/NEJMoa0904327) ·
Patel [DOI](https://doi.org/10.1056/NEJMoa1009638) · Connolly [DOI](https://doi.org/10.1056/NEJMoa0905561) ·
Granger [DOI](https://doi.org/10.1056/NEJMoa1107039) · McMurray [DOI](https://doi.org/10.1056/NEJMoa1409077) ·
Zinman [DOI](https://doi.org/10.1056/NEJMoa1504720) · Serebruany [DOI](https://doi.org/10.15190/d.2023.13).

---

## ⚠️ CORRECTION 2026-07-18 (REMEDIATION lane) — THE WINDOW CLAIM HAS AN UNADDRESSED CONFOUND

Red-teamed in `ADVERSARIAL-REDTEAM-2026-07-18.md` §4: **WEAKENED.** The headline was already
dead before the red team arrived — **this lane killed it itself**, and that self-refutation
is credited as the most honest artifact in the 2026-07-18 set. Nothing below reopens it.

**Confirmed and NOT weakened:** the strict test is a **NULL** — 0 of 5 drugs had an FDA
reviewer recount all-cause deaths to a different total. **"FDA counts more deaths than the
paper" is not supported and must not be quoted.** §10's own bound (*"structurally an n=1 test
with four hostile controls"*, empty middle zone 0 of 42) is correct and could not be weakened.

**The confound, on the one claim still standing.** The surviving claim is *"the paper always
publishes the narrower ascertainment window"* (replicates 2/2). `grep -n "pre-specif\|
prespecif\|protocol-defined\|primary analysis"` over this file returns hits only at `:27`,
`:287` and `:400` — **never attached to the window claim.**

But **both "narrow" windows _are_ the protocol-defined primary analysis periods**:
ARISTOTLE's *"intended treatment period"* and PLATO's *"efficacy period"* — this document's
own table at `:150` labels the PLATO rung *"within efficacy period ← the paper's window"*.
**A journal article reporting its pre-specified primary analysis window is doing what it is
required to do.** Framing that as *"window-selection"* or *"layer selection"* (`:19`) imputes
a choice where **protocol compliance is the null explanation**.

Additional weakening: **n=2**, both large antithrombotic CV outcome trials of the same era —
not two independent draws. And this lane itself records that **PLATO's FDA-vs-paper death
accounting is already published** (PMC10890813 / PMID 39076217), so one of the two
"replications" is a known case, not a discovery.

### ⇒ Caveat that must be attached

> The window finding is **not** evidence of selective reporting. In both cases the "narrow"
> window is the **protocol pre-specified primary analysis period**, which the paper is
> obliged to report; the finding is that the *fuller* accounting — which exists in FDA's
> hands and shrinks the benefit by ~9–12% of itself — does not appear **alongside** it.
> That is a claim about **absent secondary reporting**, not about choosing the narrow window.
> n=2, same drug class and era, and one of the two (PLATO) is already published.

**Related source-file correction, now applied:** `C:\key\JOIN-SOLVED-AND-META-2026-07-17.md`
carried *"FDA records 10 deaths vs 4"* for bedaquiline, splicing two data-locks. Flagged by
three lanes; **corrected 2026-07-18** by the remediation lane to record the matched pairs
(**10 vs 2** or **4 vs 1**) and the reviewer recount (**9/79 vs 2/81**, difference 8.9%,
exact 95% CI [1.1%, 18.2%]) — noting the recount moved the drug arm **down**, 10 → 9.
