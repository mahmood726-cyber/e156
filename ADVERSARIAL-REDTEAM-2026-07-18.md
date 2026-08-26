# ADVERSARIAL RED TEAM — 2026-07-18

**Lane:** adversarial-redteam. **Mandate:** break today's headline findings before any of them is
quoted or shipped. **Mode:** VERIFY-ONLY — no app, no code, no repo modified. Read-only on
`bias-adjusted-nma-adv`, `tournament`, all RapidMeta repos.

**Vendors used.** Claude (this lane, code + corpus arithmetic) · **Codex `gpt-5.5`** (openai family;
liveness proved by real exec returning `OK Codex, GPT-5 family`, not a status page) · **agy
`Gemini 3.1 Pro (High)`** (google family). Three families. ⚠️ `gpt-5.6` is **not available on this
ChatGPT seat** (`400 invalid_request_error`) — the codex-model-comparison verdict cannot be
exercised here; `gpt-5.5` was used instead.

**Seed-check.** 6 findings attacked → **2 REFUTED, 4 WEAKENED, 0 clean survivals.** The attack was
not too soft. It also was not uniformly hostile: §3 attack-4 and §5 attack-1 **failed**, and one
sub-attack in §3 (the label gate) **failed and is reported as failing**.

**⚠️ The panel disagreed once, and I did not paper over it.** On whether k=2 makes null-crossing
*mathematically certain*, Gemini said yes, **Codex said no — data-dependent**. Codex is right in
principle and I have adopted its correction (§1.3). The 100% figure is an empirical property of
*this* corpus, not a theorem.

---

## RANKING — (prominence) × (severity of flaw)

| # | Finding | Verdict | Inflation |
|---|---|---|---|
| **1** | Null-crossing rate (bias engine) | 🔴 **REFUTED** | 17.4% → **2.2%** (8×), **shipped live to users** |
| **2** | Cross-check reproduction 65.3% | 🔴 **REFUTED as stated** | 65.3% → **42.5%** |
| **3** | Statin 0/20 prospective | 🟠 **WEAKENED — severely** | number correct, interpretation is a tautology |
| **4** | FDA death divergence | 🟠 **WEAKENED** | headline already self-refuted; window claim has an unaddressed confound |
| **5** | HARMONY fix (`8b2eaeac0`) | 🟠 **numbers SURVIVE / validation WEAKENED** | plus a live revert landmine |
| **6** | "Reconstructable by construction" | 🟠 **WEAKENED** | demonstrated on **12 cells**, 0 failures ever recorded |

---

## 1. 🔴 REFUTED — THE NULL-CROSSING FINDING

> **Do not quote a null-crossing rate of 17.4%. The honest number is 2.2%, and it is not a finding.**

This is the most dangerous item in today's set: it is the ⭐⭐⭐ headline, it is **already rendered to
users** as a warning banner in 62 apps, and it is wrong by a factor of eight.

### 1.1 The kill — FE is not a heterogeneity estimator

`build_transparency_ledger.py:111`:

```python
for m in ('FE', 'DL', 'PM', 'REML'):
```

and the shipped user-facing string (`build_transparency_ledger.py:117-134`):

> `FLAGGED - the four conventions DISAGREE on whether the effect crosses the null … Read this
> pooled result as estimator-sensitive.`
> `Cross-checked against three other heterogeneity conventions: …`

**FE is not a heterogeneity convention.** FE sets τ² ≡ 0 *by assumption* and targets a common-effect
estimand; DL/PM/REML are competing **estimators of τ²** inside one random-effects estimand. An
FE-vs-RE difference is a **change of estimand**, not an estimator swap. Confirmed independently in
`pool_estimators.py:158-164`, where `all_estimators()` builds `FE` by passing a hard-coded `0.0`
alongside three genuine τ² estimators.

**Both decorrelated vendors agree, unprompted:**
- **Codex (openai):** *"Yes… FE fixes `tau2=0` and targets a common-effect estimand. Calling all
  four 'heterogeneity estimators' is sloppy."*
- **Gemini (google):** *"Absolutely not… statistically illiterate… conflates model selection with
  estimator variance."* Verdict returned: **REFUTED.**

### 1.2 The measurement — 87.1% of the banners are false

Recomputed from `engine_shadow_final.jsonl` (n=373; 357 with evaluable diagnostics):

| quantity | value |
|---|---|
| apps that would show the **FLAGGED** banner | **62 / 357 = 17.4%** |
| genuine RE-only disagreement (drop FE, keep DL/PM/REML) | **8 / 357 = 2.2%** |
| ⇒ **false-flag rate among shipped banners** | **87.1%** (54 of 62) |

The 8 survivors have k ∈ {3,3,3,4,4,5,5,6}. **None has k ≥ 10.** Per the house rule *"never use DL
for k<10"*, every surviving case sits in the region where τ² is barely estimable — so even the 2.2%
is not evidence of estimator fragility, it is evidence of small-k noise.

### 1.3 The corpus cannot support the metric at all

| k | apps | share |
|---|---|---|
| **2** | **226** | **60.6%** |
| 3 | 94 | 25.2% |
| 4 | 32 | 8.6% |
| ≥5 | 21 | 5.6% |

`model.py:453` → `df = n_studies - n_params`; `model.py:69` → `scipy.stats.t.ppf(0.975, df)`.
At k=2, **df=1, t=12.706 vs z=1.960 — a 6.5× CI inflation.**

Verified numerically, exact reproduction of a shipped interval (`ABATACEPT_PSA`):

```
est=0.60306  se=1.08877
df=1 → CI [-13.231, 14.437]   ← EXACTLY the shipped bias_adjusted CI
df=2 → CI [ -4.082,  5.288]
z    → CI [ -1.531,  2.737]
```

- **226/226 (100%)** of k=2 apps cross the null under the shipped interval.
- **204/373 (54.7%)** of all shipped CIs have log-width > 10 — a ratio range wider than
  **22,000-fold**. `ALEMTUZUMAB_TX`: **[-45.53, 45.77]**. These intervals are vacuous.

⚠️ **Codex's correction, adopted:** this is *not* a mathematical guarantee. Crossing is avoided iff
`|effect|/SE > 12.706`, which is data-dependent. **100% is what this corpus did, not what algebra
forces.** State it that way.

### 1.4 One attack that FAILED — report it

I expected a missing HKSJ `max(1, Q/(k-1))` floor. **The floor is present in both live paths** —
`pairwise.py:270-272` (`q_factor = max(1.0, raw_factor) if hksj_floor else raw_factor`) and
`model.py:465` (`q_factor = max(1.0, q_stat / df)`). **This attack fails; the floor is correctly
implemented.** No credit claimed.

⚠️ **One refinement, found by Codex after I had written this off — and it is a partial reversal of
my own "attack failed".** There is a **third** branch: `model.py:374`, the `exact_binomial_no_tau`
path, hard-sets `q_factor = 1.0`, bypassing the floor entirely. So "the floor is present in both
paths" was imprecise — it is present in the two paths I checked, and absent in a third I had not
found. **Materiality: nil for today's numbers** — `tau_method` is `REML` for **373/373** corpus
records, so the exact-binomial branch never executed. The floor claim stands *for this corpus* but
should not be stated as a blanket property of the engine.

Codex also notes there is **no finite-CI or `se > 0` guard at the counting site** (`pairwise.py:518`);
inputs are validated upstream at `pairwise.py:819`, so `se=0` is not expected in normal fits, but the
counting logic itself is permissive. Boundary `tau2=0` fits are marked `status="passed"`
(`pairwise.py:487`) and **do** count toward crossing — which is the same defect as §1.1 seen from the
counting side.

### ⇒ Caveat that must be attached (verbatim)

> The null-crossing flag compares FE against DL/PM/REML. FE is a different **estimand**, not a
> different τ² estimator, so 87.1% of flagged apps are flagged for a model change rather than
> estimator sensitivity. Restricted to genuine τ² estimators the rate is **2.2% (8/357)**, all at
> k ≤ 6, none at k ≥ 10. Separately, 60.6% of the corpus has k=2, where the HKSJ t-interval uses
> df=1 (t=12.71, 6.5× wider than z) and **all 226 k=2 apps cross the null**; for those apps
> "crosses the null" carries essentially no information about the data.

**Action (not taken — verify-only lane):** the shipped banner text is user-facing and currently
misinforms in 54 of 62 apps. Either drop FE from the comparison set or relabel it explicitly as
`FE-vs-RE (model change)` separate from `DL/PM/REML (estimator check)`.

---

## 2. 🔴 REFUTED AS STATED — CROSS-CHECK REPRODUCTION 65.3%

> **The denominator is selected on the outcome, and the word "exactly" is false.**

The plumbing is honest — an independent re-implementation reproduced **494/494** matches. The
defects are in the **definitions**.

### 2.1 Selection on the outcome (the structural kill)

`xcheck2.py:168-175` — a pair enters the "checkable" denominator **only if** the app's stored
`(tN, cN)` already equal two CT.gov denominators:

```python
gt = [g for g, v in D.items() if eqi(v, tN)]
gc = [g for g, v in D.items() if eqi(v, cN)]
```

No anchor → `CANNOT_CHECK / no_arm_anchor_denominators_absent` (`xcheck2.py:223-224`) — **191 pairs
excluded, all on trials that do post results.** So 65.3% answers *"given the app already agrees with
the registry on both denominators, how often does it also agree on the numerators?"* Conditioning
checkability on prior agreement with the measured quantity is textbook selection on the outcome.

### 2.2 The tolerance admits off-by-one as "exact"

`xcheck2.py:92-94`:

```python
# tolerance: reported to ~1dp, so up to 0.05% of N, plus rounding slack
return v / 100.0 * N, max(1.0, N * 0.0006 + 0.5)
```

The comment justifies `N*0.0005`; the code ships a slope 20% steeper **and a hard floor of one whole
participant**. At N=9,000 the tolerance is **±5.9 participants**. **65 of 494 (13.2%) pass only on
this slack; 17 are off by ≥1 whole participant** (e.g. `AVATROMBOPAG_*`/NCT02227693 stores 8/11
where the registry implies 9; `CEFTAZIDIME_AVIBACTAM`/NCT02475733 stores 21/22 where the registry
implies 22). The report's phrase *"recomputed **exactly**"* is false for at least 17 pairs.

**Compounding bug found in the same path:** `tier_of` (`xcheck2.py:71`) treats `'proportion' in unit`
as a percentage and `implied()` divides by 100 unconditionally. `LESINURAD_GOUT`/NCT01493531 posts
`unit='Proportion of Subjects'` on a **0–1 scale** (0.554/0.665) → computed as `0.554/100×204 = 1.13`,
which the ≥1.0 tolerance floor then "matches" to a stored 1. True counts: **113/204 and 133/200.**
Two bugs producing one fake `APP_CORRECT`.

### 2.3 The 70 wrong-endpoint pairs are scored APP_CORRECT

They are flagged in the report but **retained in the 494**. Four checked by hand against raw payloads:

| App | NCT | Declared endpoint | What the matched row actually is |
|---|---|---|---|
| `APIXABAN_AF` | NCT02942407 | ISTH major bleeding | `"Participants Experiencing Mortality"` = 21, 13 **exact** |
| `CRIZOTINIB_ALK` | NCT02838420 | PFS (RECIST) | `"Serious Adverse Events"` 15.2%×125=**19.0**, 25.8%×62=**16.0** |
| `DASABUVIR_HEPATITIS_C` | NCT02487199 | SVR12 | `"Any TESAE"` = 3, 1 (SVR12 is ~97%; 3/13=23% is impossible) |
| `BIMEKIZUMAB_AXIAL` | NCT02963506 | ASAS40 | serious-AE row (ASAS40 ~45–50%, not 3%) |

This is the **`right-number-wrong-endpoint`** class living *inside the numerator of the reproduction
rate*. Mechanism: `xcheck2.py:158-205` scans every outcome × row × category for any numeric match
and takes `if exact: break` — the **first** hit, not the best. **100 APP_CORRECT pairs came from
trials offering >50 candidate rows; 29 from trials offering >200 (max 2,889).** Unadjusted
multiple-comparison surface.

### 2.4 Attacks that FAILED — report them

- **Percentage-vs-integer over-correction: DOES NOT OCCUR.** `tier_of` orders `is_pct` before
  `paramType == COUNT_OF_PARTICIPANTS`, which *could* misfire, but **0 of 494 APP_CORRECT matches**
  hit that path. The fix did not over-correct. **Attack fails.**
- **Label gate: SURVIVES.** I expected the 2-non-stopword-token gate (`xcheck2.py:107-115`) to be
  worthless. Only **10 of 418** "consistent" matches rest on generic boilerplate. The 70 is a fair
  count, not a gross undercount. **Attack fails.**

### 2.5 Corrected rates

| Framing | Rate |
|---|---|
| Report headline | 494/756 = **65.3%** [61.9, 68.7] |
| − 17 demonstrable off-by-one false positives | 477/756 = 63.1% |
| − 69 precision-aware failures | 425/756 = 56.2% |
| Endpoint-validated numerator | 408/756 = 54.0% |
| Report numerator, **unconditioned** denominator | 494/959 = 51.5% |
| **Endpoint-validated + unconditioned** | **408/959 = 42.5% [39.5, 45.7]** |

### ⇒ Defensible statement (use this instead)

> Among 959 (app, trial) pairs where the trial posted results and the app stored per-arm counts,
> **42.5% [39.5, 45.7]** reproduced from CT.gov at both a matching denominator **and** a matching
> endpoint.

**Withdraw two things as written:** the word *"exactly"*, and the framing of 65.3% as *"the number
worth having"*. 65.3% must never appear without the sentence *"checkable is defined as the app's
denominators already matching the registry's."*

---

## 3. 🟠 WEAKENED — SEVERELY — STATIN 0/20 PROSPECTIVE

> **The number is right and I could not break it. As a claim about researcher behaviour it is a
> tautology.**

### 3.1 The kill — the denominator is zero-capable

Registry start dates, confirmed live against the CT.gov v2 API today:

| | count |
|---|---|
| started before CT.gov launched (2000-02) | **16 / 20** |
| started after CT.gov existed | 4 — GISSI-HF 2002-08, AURORA 2003-01, JUPITER 2003-02, CORONA 2003-09 |
| **started after the ICMJE mandate (2005-09-13)** | **0** |
| started after FDAAA (2007) | 0 |

The latest-starting trial began **2003-09, two years before the mandate**. 4S (1988), WOSCOPS (1989),
CARE (1989), AFCAPS (1990), LIPID (1990) began **8–12 years before ClinicalTrials.gov accepted its
first record**. Prospective registration was **impossible** for 16 and unmandated for the other 4.

**Honest denominator: 0/4** (registry-era starts), 95% Clopper-Pearson upper bound **60.2%** — the
data are compatible with a true prospective rate of nearly two-thirds.

### 3.2 The 79-month lag is a re-encoding of the start date

`studyFirstSubmitDate` timestamps **three administrative batch events**, not 11 decisions:
- **ICMJE-deadline wave (7):** SEARCH 2005-07-22, SPARCL 2005-09-06, IDEAL 2005-09-08,
  **MEGA 2005-09-13 — literally the ICMJE deadline**, CORONA 2005-09-16, JUPITER 2005-10-13,
  AURORA 2005-10-16
- **Pfizer same-day batch (2):** CARDS and TNT both **2006-05-16** — identical submit date, 9-year
  start gap
- **NHLBI legacy seed (1):** ALLHAT-LLT **1999-10-27 — predates the registry's public launch**

**Effective independent n ≈ 3, not 11.** Regressing lag on `(ICMJE deadline − start date)` gives
**R² = 0.9884**. The median 79-month lag is 98.8% determined by start date alone and carries
essentially no behavioural information.

### 3.3 One attack that FAILED — the cutline is fine

`reg_lag.py:118` computes `lag = ym(submit) - ym(start)` at month resolution, classified prospective
at `lag <= 3` (`:123`). That grace is **more lenient than ICMJE**, and every lag in the frame is
≥24 months, so no flooring error can flip any call. Under strict ICMJE the answer is still 0/20.
**The cutline is biased toward the null it failed to find. Attack fails.**

### 3.4 Bonus defect — resolver false negative

`resolve()` (`reg_lag.py:63-74`) requires an exact `acronym` match, which CT.gov often leaves empty.
**MEGA is registered: NCT00211705, start 1994-02, submit 2005-09-13, lag 139 months** — but
`reg_lag.json:143` records `"no-NCT-found"`. Corrections: naive "has NCT" is **11/20, not 10/20**;
unregistered is **9, not 10**; max lag is **139, not 112**. Median stays 79 by coincidence of odd n.

### ⇒ Caveat that must be attached (verbatim)

> The statin 0/20 is **not** evidence that investigators declined to pre-register. Every trial in the
> frame began before the 2005 ICMJE mandate (latest start 2003-09) and 16/20 began before
> ClinicalTrials.gov existed. The only interpretable cell is **0/4 prospective among trials that
> started after the registry opened**, 95% CI [0, 60%] — suggestive, not conclusive. The 79-month
> median lag is 98.8% determined by start date (R²=0.988) and is not a behavioural quantity.

The memory note already declares the result era-specific and forbids corpus-wide quoting — that
defence holds. What is missing: the denominator is **zero-capable**, MEGA is a resolver miss, and
the lag is mechanically derived. The bare sentence *"prospectively registered = 0/20"* remains
quotable out of context and should not be.

---

## 4. 🟠 WEAKENED — FDA DEATH DIVERGENCE

**The headline was already dead before I arrived, and the owning lane killed it itself.**
`FDA-DIVERGENCE-SAMPLE-2026-07-18.md:8` reports the strict test as a **NULL** — 0 of 5 drugs had an
FDA reviewer recount deaths to a different total. I confirm that and add nothing: **"FDA counts more
deaths than the paper" is not supported and must not be quoted.** The one reviewer recount in the
corpus (bedaquiline) moved the number **down**, 10/79 → 9/79. That lane's self-refutation is the
most honest artifact in today's set.

Two of Mahmood's specified attacks were **already run and closed by that lane**, and I verify the
closure:
- **Population/denominator:** matched 5/5 (`:371`) — bedaquiline 79/81 stable across all three
  locks; ARISTOTLE 9120/9081 identical across both tables. Explains nothing.
- **Adjudicated-vs-investigator:** all-cause death is **adjudication-invariant** (417/520 both ways,
  `:374`). Cannot explain a count gap.
- **"Is the FDA number really REVIEWER_COMPUTED or a sponsor table with a letterhead?"** — the lane
  flags this itself: PLATO's five-rung table is captioned *"**Sponsor's** Analysis"* and is tagged
  `SPONSOR_REPORTED, NOT REVIEWER_COMPUTED` (`:144`, `:246`).
- **Bedaquiline 10-vs-4:** the lane already establishes these are **two different data-locks**
  (`:341`) and that any matched pair is **10 vs 2** or **4 vs 1**. ⚠️ `C:\key\JOIN-SOLVED-AND-META-2026-07-17.md`
  still carries *"FDA records 10 deaths vs 4"*, splicing two locks. Not edited by me (verify-only);
  the owner should fix it.

### 4.1 My attack on the SURVIVING claim — and it lands

The claim still standing is *"the paper always publishes the narrower ascertainment window"*
(replicates 2/2, `:170`). **The confound the document never addresses is pre-specification.**

`grep -n "pre-specif\|prespecif\|protocol-defined\|primary analysis"` over the whole file returns
hits only at `:27` (endpoint-density scoring), `:287` (adjudication) and `:400` (scoring axis) —
**never attached to the window claim.**

But both "narrow" windows *are the protocol-defined primary analysis periods*: ARISTOTLE's
**"intended treatment period"** and PLATO's **"efficacy period"** — the document's own table
(`:150`) labels the PLATO rung *"within efficacy period ← the paper's window"*. A journal article
reporting its **pre-specified primary analysis window** is doing what it is required to do. Framing
that as *"window-selection"* or *"layer selection"* (`:19`) imputes a choice where protocol
compliance is the null explanation.

Additional weakening: **n=2**, both large antithrombotic CV outcome trials of the same era — not two
independent draws from a general phenomenon. And the lane itself records that **PLATO's FDA-vs-paper
death accounting is already published** (PMC10890813 / PMID 39076217), so one of the two
"replications" is a known case, not a discovery.

### ⇒ Caveat that must be attached (verbatim)

> The window finding is **not** evidence of selective reporting. In both cases the "narrow" window
> is the **protocol pre-specified primary analysis period**, which the paper is obliged to report;
> the finding is that the *fuller* accounting — which exists in FDA's hands and shrinks the benefit
> by ~9–12% of itself — does not appear **alongside** it. That is a claim about absent secondary
> reporting, not about choosing the narrow window. n=2, same drug class and era, and one of the two
> (PLATO) is already published.

**Credit where due:** the lane's §10 already concedes the sample was *"structurally an n=1 test with
four hostile controls"* and that the middle zone is empty (0 of 42 apps). That bound is correct and
I could not weaken it further.

---

## 5. 🟠 NUMBERS SURVIVE / VALIDATION WEAKENED — THE HARMONY FIX (`8b2eaeac0`)

Commit `8b2eaeac0` lives in `F:\rapidmeta-finerenone`, touches one file (`GLP1_CVOT_REVIEW.html:4230`),
and **is an ancestor of `origin/main`** — i.e. genuinely deployed, not a repeat of the
push≠deploy failure.

### 5.1 The circularity attack — structurally valid, empirically defeated

The checksum compares, inside a *single* `outcomes:[...]` literal at `GLP1_CVOT_REVIEW.html:4230`:

```
LHS  CVD(102) + MI(160) + Stroke(76)                        = 338
RHS  row "3-pt MACE (CV Death, Nonfatal MI, Nonfatal Stroke)" = 338
```

Both operands are stored app claims in the same object — **internal consistency, exactly as
suspected**, and the commit message concedes it ("validated by the internal composite checksum").

**But the RHS has an external anchor the commit never claimed.** Europe PMC's record for
PMID 30291013 carries the paper's own abstract verbatim: *"The primary composite outcome occurred in
338 (7%) of 4731 patients … and in 428 (9%) of 4732 patients … (hazard ratio 0·78, 95% CI
0·68–0·90)"*. So 338/428 **is** confirmed from the publication. The check is not circular in the way
alleged — **but it is anchored by luck, not by design.**

### 5.2 The uniform-shift attack — valid in principle, fails empirically

Three components, one equation, per arm ⇒ **two degrees of freedom unconstrained**. Any uniform
shift passes. The checksum cannot detect it. **The attack is sound.**

It fails on an external test the commit never ran — inverting CT.gov's `Events per 100 person-years`
into implied person-years (arms are 1:1 with identical follow-up, so arm PY must match):

| Outcome | implied PY albi | implied PY placebo | ratio |
|---|---:|---:|---:|
| MACE 338/428 | 7396 | 7291 | 1.014 |
| CV death 102/109 | 6335 | 6337 | **1.000** |
| All-cause 196/205 | 8033 | 8008 | **1.003** |

Pre-fix values scored **0.929** and **0.943** — materially worse. The new values are more consistent
with registry rates. (Necessary, not sufficient — the test is invariant to uniform scaling.)

### 5.3 What remains genuinely unverified

- **The four component counts were NOT verified against Hernandez 2018 Table 2.** Europe PMC reports
  `isOpenAccess: N`, no PMCID; Unpaywall reports `oa_status: bronze`; the publisher PDF 302'd to a
  bot-check and the green copy 403'd. **Neither was bypassed.** Only the composite they sum to was
  externally confirmed. **Table 2 remains unread — I am not papering over that.**
- **Unreconciled residual:** CV death implies 6,335 PY but all-cause death implies 8,033 PY — a
  **27% gap** between two time-to-death outcomes that should share follow-up. Nothing in the commit
  explains it.

### 5.4 ⚠️ Live landmine — a silent revert is one merge away

- **The checksum is a one-off, not a gate.** Zero computational checksums in the shipped HTML (the
  only `CHECKSUM` hit is prose inside the evidence blob); no committed `.py` asserts it; the patch
  script was never committed. Nothing prevents regression.
- **The old values are alive in the repo.** Branch `fix/count-provenance-2026-07-12` still carries
  **`113/130` and `196/218`**. Merging it silently reverts the fix — **and nothing would catch it.**

### ⇒ Caveat that must be attached (verbatim)

> The HARMONY composite 338/428 is externally confirmed from the Hernandez 2018 abstract via
> Europe PMC — but **not by the checksum**, which is a 2-DOF-underdetermined internal identity with
> no persistence and no regression guard. The four component counts remain **UNVERIFIED against
> Hernandez 2018 Table 2** (paper not open-access; not bypassed). A 27% person-year discrepancy
> between CV-death and all-cause-death remains unexplained, and branch
> `fix/count-provenance-2026-07-12` still carries the pre-fix values.

---

## 6. 🟠 WEAKENED — "RECONSTRUCTABLE BY CONSTRUCTION" / THE TRANSPARENCY THESIS

> **The provenance schema is excellent and it has never once been tested against a cell that could
> fail.**

Measured directly from the lane's own outputs:

| artifact | count |
|---|---|
| `excerpt_verification.json` — data points with a verified verbatim excerpt | **12** |
| distinct apps covered | **3** |
| of those 12, `ok: true` | **12 (100%)** |
| `transparency_ledger_final.jsonl` — apps | 62 |
| `transparency_ledger_final.jsonl` — **total `data_points`** | **12** |
| corpus in the shadow run | 373 |
| live app corpus | ~1,448 |

All 14 provenance fields (`url_deep`, `excerpt_verbatim`, `anchor_granularity`, `verification`,
`copyright_note`, …) are populated **12/12**. But the ledger covers 62 apps and carries **12 data
points total** — the deep-link-plus-excerpt layer exists for roughly **0.8% of the shadow corpus and
~0.2% of the live corpus**, with a **100% success rate and zero recorded failures**.

**This is the house's own "a gate must be able to fail" lesson.** A verifier that has never returned
a failure has not been shown to discriminate. And the failure mode is already known from two
independent lanes today:
- **HARMONY** (§5): the MACE counts **do not exist in CT.gov at all** — the registry posts only
  rates. A deep-link to the registry cannot source that cell.
- **Bedaquiline C208:** CT.gov's structured death field is **`null` for all four arms**, and none of
  the 25 serious-event terms is a death term. Any pipeline trusting
  `adverseEventsModule.deathsNumAffected` reads that trial as **0 deaths** against a true 10/79 vs 2/81.

⇒ The two cells anyone would most want to cite are **exactly the two that cannot carry a registry
deep-link.** The 12 verified cells are not a random sample of the corpus; they are cells that
happened to be verifiable.

### ⇒ Caveat that must be attached (verbatim)

> "Reconstructable by construction" is demonstrated on **12 data points across 3 apps** — ~0.8% of
> the shadow corpus, ~0.2% of the live corpus — with **no failure cases recorded**. The base rate at
> which an arbitrary stored cell can carry a true deep-link **plus** a verbatim excerpt is
> **unmeasured**. Two known counterexamples (HARMONY's MACE counts, absent from CT.gov; bedaquiline's
> null death field) show the failure mode is real and lands on high-value cells. Until a sample
> including *failures* is drawn, quote the schema as a **design**, not as a measured capability.

**The narrative that does survive:** "memory, not capability" is corroborated by the orphan
enumeration in `HARNESS-AND-INVENTORY-2026-07-17.md:105-140` — and note that lane **refuted all
three of its own named orphan claims** (`refmatch.py` has 2 non-test importers at `refjoin.py:72`
and `forestgold.py:51`; `channel.py` has 5; `tau2_cross_check_report` was **not found on disk at
all** and is tagged INHERITED/unverifiable). The corrected structural finding — *one internally
vascularised organ needing one anastomosis*, not 31 dead modules — is the version to quote.

---

## APPENDIX — what I could NOT break

Reported so the report is not a list of only-successes:
1. **The HKSJ `max(1, ·)` floor** is correctly implemented in the two live code paths
   (`pairwise.py:270-272`, `model.py:465`). Expected defect absent. ⚠️ **Partially reversed** — Codex
   found a third branch, `model.py:374` (`exact_binomial_no_tau`), that hard-sets `q_factor = 1.0`
   and bypasses the floor. Immaterial today (`tau_method` is REML for **373/373** records, so it
   never executed) but the floor is **not** a blanket property of the engine.
2. **The percentage-vs-integer fix did not over-correct** — 0 of 494 APP_CORRECT matches take the
   dangerous ordering path in `tier_of` (`xcheck2.py:70-74`).
3. **The cross-check label gate holds** — only 10 of 418 "consistent" matches rest on generic
   boilerplate. The 70 wrong-endpoint count is fair, not a gross undercount.
4. **The statin lag cutline is fine** — and is *more lenient* than ICMJE, biased toward the null it
   failed to find.
5. **The cross-check ledger arithmetic is honest** — an independent re-implementation reproduced
   **494/494**. Every defect found is definitional, not fabricated.
6. **The FDA lane's own bounds** (§10: empty middle zone, 0/42; sample structurally n=1) could not be
   weakened further. It bounded itself correctly before I got there.
7. **HARMONY's numbers are right**, and `8b2eaeac0` really is on the deployed ref.

---

## CLOSING — the refutation that stuck

Not a green count. The single most consequential thing in this document:

> **62 live apps currently render a banner telling readers their pooled result is
> "estimator-sensitive". In 54 of them (87.1%) that banner is firing on a fixed-effect-vs-random-effects
> model change, not on estimator sensitivity. The honest rate is 2.2%, and 60.6% of the corpus has
> k=2, where the interval used cannot discriminate anyway.**

Two decorrelated vendors reached that independently — and one of them (Codex) also corrected *me*,
which is the reason to keep running them.

---

## ⚠️ CORRECTION 2026-07-18 (REMEDIATION lane) — THE BANNER IS **NOT LIVE**

This document's §1 and its CLOSING paragraph state that the null-crossing banner is
**"already rendered to users"**, **"shipped live to users"**, and that
**"62 live apps currently render a banner"**. **That is not true, and it is this report's
single most-quotable sentence.**

**Measured, whole corpus:** `0` of **1,658** `*REVIEW*.html` files in
`F:\rapidmeta-finerenone` contain the string `conventions DISAGREE` or `estimator-sensitive`.
The banner text exists in exactly four places, none of them an app:

```
C:\Projects\bias-shadow-2026-07-17\build_transparency_ledger.py     (the generator)
C:\Projects\bias-shadow-2026-07-17\transparency_ledger.jsonl        (shadow output)
C:\Projects\bias-shadow-2026-07-17\transparency_ledger_final.jsonl  (shadow output)
F:\E156\ADVERSARIAL-REDTEAM-2026-07-18.md                           (this report)
```

⇒ The banner is **SHADOW-ONLY**. **No user has ever seen a false banner.** Nothing needed
removing from live apps, and **"87.1% of shipped banners are false" must not be quoted as a
live-harm claim** — the correct framing is *"87.1% of the banners this generator WOULD ship
are false, caught before deployment."*

**The statistical finding itself is CONFIRMED, independently recomputed** by the remediation
lane from `engine_shadow_final.jsonl` (n=373; 357 with ≥2 passing estimators):

| quantity | redteam | remediation lane | agree |
|---|---|---|---|
| flagged with FE in the set | 62/357 = 17.4% | **62/357 = 17.4%** | ✓ |
| flagged, DL/PM/REML only | 8/357 = 2.2% | **8/357 = 2.2%** | ✓ |
| false-flag rate | 87.1% (54/62) | **87.1% (54/62)** | ✓ |
| survivor k values | all ≤6, none ≥10 | **[3,3,3,4,4,5,5,6]** | ✓ |

The 8 survivors match `null_crossing_corrected.json` app-for-app. **One narrowing:** the
k=2 share is **61.1% (218/357)** over the *evaluable* set, not 60.6% (226/373) over all
records — both are right on their own denominator; state which one you mean.

**Status of the underlying fix:** `build_transparency_ledger.py:111` still reads
`for m in ('FE', 'DL', 'PM', 'REML')` (mtime 10:43, unchanged). **The generator defect is
NOT yet fixed** — it is owned by the integration lane (`local_f660330f`), which has computed
the corrected 8-app list but has not yet amended the generator. Verified, not fixed, by the
remediation lane per the single-writer guard.

⭐ **The general lesson, which is the same one this report is about:** a verify-only lane
inferred deployment from the presence of a generator and a populated output file. Reading
the artefact is not the same as reading the *deployed* artefact — the same
`push ≠ deploy` family as `rapidmeta-fabricated-nct-sweep`. **Grep the live corpus before
writing "shipped".**

---
---

# FINAL PASS — 2026-07-18, pre-reset. Three live findings, kill-or-survive.

**Nothing below goes ESC-ready or public without surviving this section.**
**Result: 2 KILL · 2 SURVIVE · 2 WEAKENED · 1 allegation REFUTED (ours).**

---

## 7. 🔴 KILL — `HF_QUADRUPLE_NMA_REVIEW` POOLS AN ACTIVE-COMPARATOR TRIAL INTO A PLACEBO NODE

**Verdict: DEFECT CONFIRMED bit-for-bit. Do not ship this app or quote its OR.**
Present in **all three copies**: `F:\rapidmeta-finerenone`, `F:\rmf-deploy`, `C:\Projects\_rmf-live-fix`.

App's own embedded payload:

```json
"measure": "OR",
"pooled_DL": {"I2": 0.0, "Q": 3.0969884542610955, "k": 6,
              "logEffect": -0.24970183806283014, "se": 0.0267202981113297, "tau2": 0.0}
```

### 7.1 The six trials — decoded from the app, NCTs resolved

| NCT | Trial | Population (stored `group`) | Comparator | Class | OR |
|---|---|---|---|---|---|
| NCT03036124 | DAPA-HF | HFrEF (LVEF≤40%) | placebo | SGLT2i | 0.723 |
| NCT03057977 | EMPEROR-Reduced | HFrEF (LVEF≤40%) | placebo | SGLT2i | 0.731 |
| NCT03619213 | DELIVER | **HFmrEF/HFpEF (LVEF>40%)** | placebo | SGLT2i | 0.808 |
| NCT03057951 | EMPEROR-Preserved | **HFpEF (LVEF>40%)** | placebo | SGLT2i | 0.780 |
| **NCT01035255** | **PARADIGM-HF** | HFrEF | 🛑 **ENALAPRIL (ACTIVE)** | **ARNI** | 0.774 |
| NCT04435626 | FINEARTS-HF | **HFmrEF/HFpEF (LVEF≥40%)** | placebo | nonsteroidal MRA | 0.832 |

**Confirmed defects:** ① 3 HFrEF pooled with 3 HFpEF/HFmrEF; ② five placebo-controlled pooled with
**one active-controlled**; ③ **four drug classes** pooled into a single OR as one intervention.
Despite "NMA" in the filename this is **not a network meta-analysis** — it is one pairwise pool of
"some drug vs whatever its own control happened to be."

⚠️ **Part of the original allegation was wrong and is corrected here: TOPCAT and PARAGON-HF are NOT
in this file.** The HFpEF mixing is real, but via DELIVER / EMPEROR-Preserved / FINEARTS-HF.

### 7.2 PARADIGM-HF is in the pool — proven by exact reproduction

Independent recomputation of inverse-variance DL from the app's own six `(y, v)` pairs:

```
ALL 6       : logOR = -0.2497018381   se = 0.0267202981   Q = 3.0970
SHIPPED     : logOR = -0.24970183806  se = 0.0267202981   Q = 3.0969884543
MATCH (1e-9): True
```

The shipped estimate reproduces **only** with NCT01035255 included. Confirmed independently against
CT.gov v2 `armGroups`:

```json
{"label":"LCZ696","type":"EXPERIMENTAL"},
{"label":"Enalapril","type":"ACTIVE_COMPARATOR","interventionNames":["Drug: Enalapril 10 mg BID"]}
```

**No placebo arm.** Enalapril is an efficacious ACE inhibitor, so PARADIGM's contribution is biased
**toward the null** relative to a placebo contrast.

### 7.3 ⭐⭐⭐ THE APP VIOLATES ITS OWN DISPLAYED EXCLUSION CRITERION

This is the sharpest item in the final pass. The app's own rendered exclusion table reads, verbatim:

> **Comparator** — *Include:* "Placebo, sham, or standard of care" · *Exclude:* **"Active comparator
> without placebo arm"**

**PARADIGM-HF meets that stated exclusion criterion and is bootstrapped as `status:"include"` anyway.**
The app even *knows* the comparator — its stored `group` string says *"…200 mg BID vs enalapril 10 mg
BID"* — while app state declares `comp:"Placebo (common network comparator)"`. The seeding function
filters on **phase only**:

```js
getCanonicalBootstrapIds(){return Object.entries(this.realData??{})
  .filter(([,data])=>!isPhaseTwoLike(data?.phase??"")).map(([id])=>id)}
```

All six are `phase:"III"` ⇒ all six pooled. **There is no comparator or population filter anywhere in
the seeding path.** The eligibility criteria are *rendered to the reader* but never *enforced in code*.

### 7.4 🟢 SURVIVE — the I²=0 allegation is REFUTED (our own allegation, killed)

I² is **computed live in JS, not hardcoded**:

```js
const Q=Math.max(0,sW_y2-sWY*sWY/sW), df=data.length-1,
      tau2 = df>0 && Q>df ? (Q-df)/(sW-sW2/sW) : 0;
```

`Q = 3.097` on `df = 5`. Q < df ⇒ I² = 0 is **arithmetically correct, not degenerate and not
fabricated**. The six ORs genuinely are tight (0.723–0.832). The app even self-flags
`"I² unreliable with only k=" + k + " studies"`. **The inference "I²=0 across mixed populations must
mean the statistic is broken" is wrong, and I am recording it as a refuted allegation of our own.**

⭐ **But this is the real lesson, and it is worse than the original allegation.** Statistical
homogeneity does not imply clinical homogeneity. I² measures dispersion of effect sizes and is
**structurally blind to estimand incoherence** — so it returns its maximally reassuring value,
*"no heterogeneity, pool with confidence"*, on a pool whose members share no estimand.
**This defect survives every heterogeneity gate in the app because I² is the wrong instrument to
detect it.** The house rule *"I²=0 ≠ homogeneity"* firing in a shipped app.

### 7.5 ⚠️ The honest limit — do NOT over-claim numerical impact

| set | k | pooled OR | 95% CI | Q | I² |
|---|---|---|---|---|---|
| all 6 (with PARADIGM) | 6 | **0.7790** | 0.7393–0.8209 | 3.097 | 0% |
| without PARADIGM | 5 | 0.7810 | 0.7345–0.8305 | 3.073 | 0% |

**Δ OR = 0.002. No conclusion flips.** Nobody may say "the active-comparator trial distorts the
estimate" — it barely does. The correct statement is that the estimate **has no interpretation**,
not that it has the wrong value.

### ⇒ Caveat / action

> `HF_QUADRUPLE_NMA_REVIEW` pools six trials spanning HFrEF and HFpEF/HFmrEF, four drug classes, and
> five placebo-controlled plus **one active-comparator** trial (PARADIGM-HF vs enalapril,
> NCT01035255) into a single OR of 0.779 — **in violation of the app's own displayed exclusion
> criterion**, because eligibility is rendered to the reader but filtered in code on **phase only**.
> Inclusion confirmed by exact reproduction of the shipped estimate. The reported **I²=0 is
> arithmetically correct (Q=3.10 < df=5) and clinically meaningless.** Removing PARADIGM-HF changes
> the pool by 0.002: **the defect is validity, not magnitude.**

⭐ **Generalisable, and it is the highest-value item here:** *criteria that are displayed but not
enforced.* Any app rendering an eligibility table should be checked for whether the seeding path
actually filters on it. Here it filters on phase alone. **This is a corpus-wide grep, not a one-app fix.**

---

## 8. 🟠 WEAKENED — ESC "~2% OF CONCLUSIONS FLIP" IS AMBIGUOUS

`ESC-EXHIBIT-VERDICT-2026-07-18.md` §4 carries *"Estimator alone, corpus-wide **~2% of conclusions
flip** [R — bias lane calibration, verify before quoting]"* — correctly tagged `[R]` with an explicit
instruction to verify. **Verified [M]**, and it resolves two ways:

| definition of "flip" | measured |
|---|---|
| **significance status** changes across DL/PM/REML | **8/357 = 2.24%** |
| **direction (sign)** changes across DL/PM/REML | **2/357 = 0.56%** |

⇒ **Upgrade `[R]` → `[M]` as 2.24%, and say "significance status", not "conclusions".** A reader
hearing "conclusions flip" pictures a direction reversal, which happens **4× less often**.

⚠️ **It must also carry §1's caveat:** 2.24% is the **FE-excluded** figure. Computed the way the
shipped transparency ledger does it — with FE in the set — the same quantity reads **17.4%**. If the
ESC number and the app banner appear in one document they contradict each other by **8×**.

---

## 9. FDA-CONTRADICTS-PUBLISHED CANDIDATES — paper side checked FIRST

### 9.1 ✅ SURVIVES — the already-published trap was self-caught by both lanes

- `FDA-DEEP-DIVE-2026-07-18.md:11` — *"the single most quotable item — the medication-error scandal
  — is **already published**, and I nearly shipped it as new."* Scoring rows 13/14 mark medication
  errors (**Alexander 2013**) and China falsified data (**JAMA Intern Med 2019**) ⛔ **PUBLISHED**.
- `ESC-EXHIBIT-VERDICT-2026-07-18.md:2` — *"We have **NOT** found a cardiology NMA whose conclusion
  *we* change… the conclusion-change is the field's **OWN** published analysis, not ours."* The
  ticagrelor/PLATO reversal is disqualified because with-vs-without-PLATO is the 2025 JAHA paper's
  own central published design (12 mentions of "without PLATO").

**I could not find a third instance of the trap. The discipline is working.**

### 9.2 ✅ SURVIVES — the Marciniak caveat is attached, and **I was wrong about what was missing**

Present in **four** places, not three:
- `:44-45` lists **both** Ref ID **3232518** (Marciniak, *Dissent: completeness of follow-up*) **and**
  Ref ID **3236037** (Beasley & Rose, ***Rebuttal to Marciniak***).
- Scoring row 7: *"⭐ **contested** — Rebutted internally; use only with §5b."*
- `:366` — *"It does **not** require Marciniak. The contradiction stands on Tables 68/69 alone, which
  are mainstream-review, not dissent."*
- ⭐ **And the disposition I claimed was missing is already there, verbatim:**
  > *"⇒ **Apixaban was approved. Marciniak's recommendations were not adopted.** Any use of §3e/§3f
  > must say: *this is one FDA reviewer's signed dissent, rebutted internally and not the agency's
  > position.* Presenting Marciniak as 'the FDA found' would be exactly the overreach that got the
  > ticagrelor reversal framing disqualified."*

🔴 **Correction against myself:** I drafted a "required addition — state that apixaban was approved."
**That requirement was already met and my demand was wrong.** Recorded rather than quietly deleted,
because a red team that invents missing caveats is failing the same way as one that misses real ones.

### 9.3 ✅ SURVIVES — extraction verified 4/4 against the source PDF; **one required edit**

**Both checks I expected to leave unresolved returned before reset. §3b is cleared, with one wound.**

**(a) Extraction is CLEAN — the "our own error" attack is KILLED.** Re-extracted from
`C:\key\fda_target_pdf\202155Orig1s000MedR.pdf`, **PDF p.292 = internal p.165, footer
`Reference ID: 3134464`** — the doc's citation is exact. Raw text of Table 69:

```
Table 69 ARISTOTLE – FDA's Analysis of All-cause Death by Site TTR / ITT Population, during ITP
             156 / 2210  3.87   193 / 2189  4.91   0.79 (0.64, 0.97)
>55.3 – 64.6 215 / 2829  4.09   235 / 2854  4.41   0.93 (0.77, 1.11)
>64.6 – 72.7 142 / 2398  3.06   155 / 2423  3.32   0.92 (0.73, 1.16)
> 72.7        88 / 1633  2.83    86 / 1608  2.81   1.00 (0.74, 1.34)
```

| check | result |
|---|---|
| HRs 0.79 (0.64–0.97) / 1.00 (0.74–1.34) | ✅ verbatim |
| Table 69 = *"FDA's Analysis"*, Table 68 = *"Applicant's Analysis"* | ✅ verbatim labels |
| 55.3 / 72.7 are genuine **Q1/Q3 site-TTR cutpoints** | ✅ explicit at p.288 (*"equal numbers of sites in each quartile"*) |
| Warfarin quartile deaths sum to **669**; apixaban **601** (vs 603); denominators 9070/9074 | ✅ exact |
| Applicant top-quartile HR **1.23 (0.84, 1.78)** | ✅ exact (3.07/2.54 = 1.21) |
| Wallentin 0.91 (0.74–1.13) / 0.91 (0.71–1.16), P-int 0.34 | ✅ Europe PMC verbatim, **PMID 23640971** |

**(b) Prior art: NONE — novelty holds.** Five Europe PMC sweeps: `"ARISTOTLE" AND "site TTR"` → **0
hits**; `"apixaban" AND "center TTR"` → 9, none regulatory; `AUTH:"Marciniak TA"` → 51 papers, **all
on PLATO/ticagrelor/clopidogrel/ivabradine, none on apixaban or ARISTOTLE**. No published comparison
of the FDA TTR table to Wallentin. **No HARMONY/Alexander-2013 trap here.**

### 🟠 The one wound — "sufficient explanation" is OVERSTATED and must be edited

The 10-vs-17 comparison **is** apples-to-apples (Wallentin's *"interquartile limits 61% and 71%"* and
FDA's 55.3/72.7 are both 25th/75th percentiles; medians agree at 66 vs 64.6). But the shrinkage
mechanism **does not fit the pattern**:

- Compression is **asymmetric**: Q1 moves 55.3 → 61 (**+5.7 points**); Q3 moves 72.7 → 71 (**−1.7**).
- Range-compression predicts the largest divergence where compression is largest — the **bottom**.
- Observed: bottom 0.79 vs 0.91 (Δ0.12); **top 1.00 vs 0.91 (Δ0.09) — where the cutpoints nearly
  coincide (72.7 vs 71).** The top-quartile divergence is **essentially unexplained** by compression.
- Second unmodelled difference: FDA weights **equal sites per quartile**; Wallentin's weighting of
  centre-average TTR is **unstated** (likely patient-weighted).

⇒ **REQUIRED EDIT to `FDA-DEEP-DIVE-2026-07-18.md:185`:** downgrade *"That is a **sufficient**
explanation for the divergence"* → *"a **partial** explanation; the weighting scheme (equal-sites vs
unstated) differs too, and compression does not account for the top-quartile divergence."* As
written, the doc **over-explains its own finding** — which is the rarer failure, but it would collapse
under a reviewer who checks the cutpoints.

⇒ Defensible claim, narrow, and now fully sourced: *a published "no interaction" result is
method-dependent and was never reported as such* — with **the sponsor's own NDA analysis (Table 68,
HR 1.23) agreeing with FDA, not the paper.** Two of three analyses in the regulatory file show
attenuation; only the published one does not. **Never characterise this as the paper being wrong.**

---

## FINAL-PASS SUMMARY

| # | Item | Verdict |
|---|---|---|
| **7.1–7.3** | `HF_QUADRUPLE_NMA_REVIEW` — active comparator + population + class mixing, **against the app's own displayed exclusion criterion** | 🔴 **KILL** (confirmed bit-for-bit) |
| **7.4** | "I²=0 proves the statistic is broken" — **our own allegation** | 🟢 **REFUTED** — I² is computed and correct; it is simply blind to the defect |
| **7.5** | "the active-comparator trial distorts the estimate" | 🔴 **KILL the magnitude framing** — Δ OR = 0.002 |
| **8** | ESC "~2% of conclusions flip" | 🟠 **2.24%** (significance) / **0.56%** (direction); must be FE-excluded |
| **9.1** | Already-published trap | ✅ **self-caught by both lanes**; no third instance |
| **9.2** | Marciniak dissent caveat | ✅ **attached in 4 places** — my "missing caveat" demand was **wrong**, recorded |
| **9.3** | FDA TTR extraction (Tables 68/69) | ✅ **SURVIVES** — verified 4/4 verbatim against the source PDF |
| **9.3** | FDA TTR novelty | ✅ **SURVIVES** — 0 prior art across 5 Europe PMC sweeps |
| **9.3** | *"shrinkage is a **sufficient** explanation"* | 🟠 **WOUNDED — required edit.** Compression is asymmetric; top-quartile divergence occurs where cutpoints agree |

**Closing, and it is not a green count.** Two shipped artifacts today were *arithmetically correct and
false as claims*: the null-crossing banner (§1, FE is not a τ² estimator) and this app's I²=0 badge
(§7.4, Q<df on a pool with no shared estimand). In both cases **every internal check passed** — the
arithmetic was right, the gate was live, the statistic was computed honestly. **The defect class to
hunt next is not miscomputation; it is a correct number answering a question nobody asked.** And the
mechanism that let it ship is now named: **eligibility criteria displayed to the reader but never
enforced in the seeding code.** That is a grep, and it should be run corpus-wide before anything else.

---
---

# HFrEF RECOVERY — ADVERSARY PASS (`HFREF-OURS-VS-PUBLISHED-2026-07-18.md`, Parts IV–VII)

**Mandate:** break the HFrEF recovery result before it goes ESC-ready. **Mode:** VERIFY-ONLY.

---

## 10. 🔴 KILL THE FRAMING — "THE OFFSET VANISHED" IS NOT MEASURABLE AT PART VI's PRECISION

> **This kill is independent of the circularity question and lands on its own. Even if every T5
> number is pristine, the headline as written must not go to ESC.**

Part VI headlines: *"the disagreement with Tang has collapsed to zero… Four of six nodes now
reproduce Tang to within 1%."*

### 10.1 Tang was ALREADY inside our confidence interval on 6 of 6 nodes — in Part V

| node | Part V (the "offset" state) | Tang | ratio | **Tang inside Part V CI?** |
|---|---|---|---|---|
| ACEI | 0.886 (0.801–0.979) | 0.83 | 1.067 | ✅ **YES** |
| ACEI+MRA | 0.667 (0.570–0.779) | 0.62 | 1.076 | ✅ **YES** |
| ACEI+BB | 0.640 (0.526–0.778) | 0.59 | 1.085 | ✅ **YES** |
| ARNI+BB | 0.548 (0.442–0.680) | 0.51 | 1.075 | ✅ **YES** |
| ACEI+BB+MRA | 0.639 (0.392–1.042) | 0.52 | 1.229 | ✅ **YES** |
| ACEI+BB+MRA+SGLT2i | 0.556 (0.337–0.920) | 0.46 | 1.209 | ✅ **YES** |

**6 of 6.** The "systematic ~7–8% offset across four independent chains" that Parts I–V treated as a
standing disagreement **was never a statistically detectable disagreement at all.** It was a
point-estimate difference well inside our own uncertainty. Eliminating it is therefore not the
resolution of a discrepancy — it is movement within noise.

### 10.2 ⭐⭐⭐ Part VI cannot measure the thing it claims to have fixed

Minimum offset vs Tang that would fall **outside Part VI's own 95% CI** — i.e. the smallest
disagreement Part VI is capable of detecting:

| node | Part VI CI | **min detectable offset** |
|---|---|---|
| ACEI | 0.534–1.300 | **+56%** |
| ACEI+MRA | 0.396–0.994 | **+58%** |
| ACEI+BB | 0.368–0.945 | **+60%** |
| ARNI+BB | 0.312–0.816 | **+62%** |
| ACEI+BB+MRA | 0.307–1.128 | **+92%** |
| ACEI+BB+MRA+SGLT2i | 0.265–0.992 | **+93%** |

**The offset Part VI claims to have eliminated is 7–8%. Part VI's best node cannot resolve an offset
below 56%.** Agreeing "to within 1%" at a resolution of ±56% is not evidence of agreement; it is a
coincidence of point estimates inside an interval that spans a factor of 2.4.

And the direction of travel is the wrong way round: **Part V was the more discriminating network.**
Its minimum detectable offsets were ACEI **±11%**, ACEI+MRA ±17%, ACEI+BB ±22%, ARNI+BB ±24% — i.e.
Part V could *almost* have detected a 7–8% offset (ACEI, 7% vs an 11% threshold); Part VI cannot come
within a factor of seven of it. **Recovery bought accuracy at the cost of the precision required to
verify the accuracy.**

### 10.3 What is genuinely true, and what must be struck

✅ **Genuinely true and worth keeping:** the k=1 → k=5 diagnosis is real and important. The Placebo→ACEI
edge carried **I²=32.5%** heterogeneity that was *structurally invisible at k=1*, and the earlier
tight intervals were **false precision**. The doc says this itself — *"Part VI is simultaneously our
most accurate and our least precise estimate — and both movements are corrections"* — and that
sentence is the honest one.

✅ **Also true and generalisable:** *"materiality must be judged per-edge, not per-trial."* Four
trials with ~38 deaths between them, each triaged LOW-WEIGHT, were collectively decisive because they
all landed on one thin edge. That is a real methodological lesson and survives intact.

🛑 **Must be struck:** *"the disagreement with Tang has collapsed to zero"* and *"four of six nodes
now reproduce Tang to within 1%"* as evidence of validation. The 1% agreement is **not a measurement**
— it is a point estimate inside an interval too wide to test it.

### ⇒ Caveat that must be attached (verbatim)

> Tang's estimate lay inside our 95% CI on **6 of 6 nodes in Part V**, before any of the four
> backbone trials were recovered — so the "7–8% systematic offset" was never a statistically
> detectable disagreement. Part VI's intervals widened 1.3×–4.4× on the log scale; its minimum
> detectable offset is **+56% to +93%**, against a claimed 7–8% offset. **The convergence in point
> estimates cannot be verified at the precision the network now has.** What Part VI establishes is
> that a k=1 edge produced false precision and hid I²=32.5% — a real and important correction — not
> that our network reproduces Tang.

---

## 11. 🟢 SURVIVES — MAHMOOD'S PREDICTION DEFLATION IS CORRECT (I tried to break the deflation)

Mahmood asked me to sanity-check whether the lane's own deflation to p≈0.57 was right — i.e. whether
it **under**-sold a prediction that was actually informative. **The deflation is correct, and if
anything it is generous.** Both checks reproduced independently:

```
C(37,2) / C(49,2)                          = 0.5663265306
Fisher exact, one-sided (less)             p = 0.5663
Fisher exact, two-sided                    p = 1.0000
hypergeom P(0 failures among 12 registered) = 0.5663265306
```

- **The arithmetic is exactly right.** Strata (12 registered / 37 unregistered, 2 failures) are
  correctly assigned and the one-sided hypergeometric is the right test for "did both failures land
  in the unregistered stratum by chance."
- ⚠️ **It is weaker than the doc states.** The doc reports one-sided p ≈ 0.57; the **two-sided
  Fisher p is 1.0000** — the observed table is the single most likely outcome under independence.
  Worth stating, because it makes the non-informativeness sharper, not softer.
- **The tautology argument is sound.** *"For any pre-2000 trial the protocol arm is true by
  construction"* is correct: CT.gov opened 2000-02, UMIN-CTR 2005-06; Hy-C (1992) and MUCHA (2004)
  predate their respective registries. ⭐ **This is structurally the same defect as §3 of this report
  (the statin 0/20 tautology) — a zero-capable stratum.** Two independent lanes reached the same
  form of error-check on the same day; that consistency is itself evidence the check is real.
- **The lane's own carve-out is fair:** the *materiality* arm was frozen at 20:20:50 from n and edge
  position, before failures were known, so both failures landing immaterial was not guaranteed. That
  is genuine, modest content and the doc claims no more than that.

⇒ **SURVIVES. No correction needed.** The lane deflated its principal's prediction correctly rather
than banking it — the harder and rarer direction of error. This is the one item in today's set I
attacked and found nothing to take away.

---

## 12. 🟢 SURVIVES — THE T5 CIRCULARITY ATTACK FAILS. This was the load-bearing risk and it holds.

> **"We now agree with Tang" is NOT "we copied Tang's inputs."** Tang and our T5 route are two
> independent extractions of the same primary trials. Convergence is genuine.

### 12.1 Neither donor is a Tang data source

Tang's full text fetched via Europe PMC (`PMC11585106/fullTextXML`, 146,853 bytes, 72 references):

- **Burnett 2017 (PMC5265698): ZERO occurrences.** Absent from the reference list under every form
  tried (`Thirty Years`, `Cope S`, `Earley`, `Senni`, `28087688` → all 0). **Tang has never seen it.**
- **PMC9546056: Tang DOES cite it — as reference [70] — but only in Discussion.** All six body
  citations sit at byte offsets 67737–71260, five inside `<title>Comparisons with similar
  studies</title>` and one inside `<title>Strengths and limitations</title>`. Methods begins at
  offset 6032. **Ref [70] never appears in Methods, search strategy, or data extraction.** The citing
  sentences are related-work framing — *"Our findings align with previous meta-analyses [69, 70]"* —
  comparing **conclusions**, not sourcing data.

### 12.2 Tang cites the ORIGINAL primary for all four backbone trials

| trial | Tang's Table 1 ref | resolves to |
|---|---|---|
| FEST | [39] | Erhardt L, MacLean A, Ilgenfritz J, et al. *Eur Heart J* 1995;16(12):1892–9 |
| CASSIS | [66] | Widimsky J, Kremer HJ, Jerie P, Uhlir O. *Eur J Clin Pharmacol* 1995;49(1–2):95–102 |
| Brown 1995 | [33] | Brown EJ Jr, Chew PH, MacLean A, et al. *Am J Cardiol* 1995;75(8):596–600 |
| Captopril-Digoxin | [23] | Captopril-Digoxin Multicenter Research Group. *JAMA* 1988;259(4):539–44 |

**Not one is attributed to a review.**

### 12.3 ⭐ The distinction that decides it — and the affirmative evidence

Two independent extractions of the **same primary trial** is **not** circularity — it is two routes
to one ground truth, and agreement is meaningful. Circularity requires Tang to have copied a donor's
extraction, or both to have copied a common third. **Neither holds.**

⭐ **Affirmative evidence Tang read the primaries rather than harvesting counts:** Tang reports
**Captopril-Digoxin N=300** — the full three-arm enrollment from the JAMA primary. Our T5 route gives
the two-arm subset **204** (104+100). *A count-harvest from the donor would have inherited 204.*
Tang's denominator is the primary's. Denominators otherwise match exactly (FEST 308/308, CASSIS
248/248, Brown 241/241) — neutral, since published totals appear identically everywhere; the
**divergent** cell is the informative one, and it points to independence.

### 12.4 An attack that could not be run, stated as a limit

**Tang publishes no arm-level counts anywhere** — verified in both layers. Main Table 1 has columns
Study | Trial name | Population | No | Age | Male % | Background | Treatment | Control | follow-up —
**no event column**. The supplement (`12872_2024_4339_MOESM1_ESM.docx`, 25,753 chars) holds Table S1
(RoB), S2–S4 (league tables), S5 (SUCRA); `Event` → 0, `Death` → 0, `n/N` → 0. **No extraction table.**

⇒ A count-for-count comparison against Tang **is impossible**, so the strongest form of the
circularity test cannot be run in either direction. **Residual risk, stated honestly: Tang's authors
demonstrably read PMC9546056 (they cite it), and silent uncited count-harvesting is unfalsifiable
from the published record.** It is unevidenced, and the Captopril-Digoxin denominator argues against
it — but it cannot be excluded.

### ⇒ Verdict

**SURVIVES.** The Part VI convergence is not manufactured by shared inputs. ⚠️ It is still subject to
**§10** — the convergence is real in provenance but unverifiable at Part VI's precision. Those are
two different attacks and only one of them failed.

---

## 13. 🔴 WRONG-IDENTIFIER DEFECT IN THE LOAD-BEARING FILE — must be fixed before ESC

`HFREF-OURS-VS-PUBLISHED-2026-07-18.md` misattributes its **dominant data donor** — the source of
47% of all recoveries — in six places (lines 677, 678, 749, 908, 1130, and §VI-1).

**The file says:** *"Aimo 2022, J Intern Med"*, linking `europepmc.org/article/MED/`**`35389544`**.

**Verified independently via Europe PMC REST:**

| identifier | what it actually is |
|---|---|
| **PMC9546056** | **De Marzo V, Savarese G, Tricarico L, Hassan S, Iacoviello M, Porto I, Ameri P.** "Network meta-analysis of medical therapy efficacy in more than 90,000 patients with heart failure and reduced ejection fraction." *J Intern Med* 2022;292(2):333–49. **PMID 35332595** |
| **PMID 35389544** | 🛑 **Zhang et al., "In Operando Identification of In Situ Formed Metalloid Zinc^δ+ Active Sites for Highly Efficient Electrocatalyzed Carbon Dioxide Reduction," *Angewandte Chemie Int Ed*.** No PMCID. **A chemistry paper.** |

The PMCID and supplement filename are correct (`JOIM-292-333-s001.docx` matches *J Intern Med*
292:333) — **only the author name and PMID are wrong**. This does not touch the convergence verdict,
but a submission-facing artifact currently cites an **electrocatalysis paper** as the PMID of the
source behind nearly half its data.

⇒ **Required fixes before ESC:**
1. **Rename Aimo → De Marzo** and **PMID 35389544 → 35332595** in all six places, including
   line 749 (*"PMC9546056 (Aimo 2022)"*) and line 1130 (*"Aimo's own exclusion note"*).
2. ⭐ **Disclose that Tang cites the donor as ref [70]**, and that the citation is **Discussion-only,
   not Methods.** This fact is currently absent from the file. **Disclosed and characterised, it is a
   strength — it shows we checked. Undisclosed and found by an ESC reviewer, it looks like
   concealment.**

⭐ This is the house identifier rule firing exactly as written: *"treat trial IDs, NCT IDs, PMIDs,
DOIs as typed fields, not approximate text."* The PMCID was right, the supplement filename was right,
the data was right — and the PMID still pointed at another field's literature.

---

## 14. 🟢 SURVIVES (with a fragility) — NO EVIDENCE THE RECOVERED COUNTS WERE CHOSEN TO CLOSE THE GAP

The tuning hypothesis: recovered counts were selected, consciously or not, in the direction that
closes the Tang gap (0.886 → 0.833, i.e. favouring ACEI). **Tested directly on the four backbone
trials, and it fails.**

| trial | counts (ACEI vs placebo) | RR | direction | IV weight |
|---|---|---|---|---|
| FEST | 5/155 vs 3/153 | **1.645** | 🔴 **AGAINST ACEI** | 17.7% |
| CASSIS | 7/200 vs 6/48 | **0.280** | favours ACEI | 32.4% |
| Brown 1995 | 3/116 vs 4/125 | 0.808 | favours ACEI | 16.2% |
| Captopril-Digoxin | 8/104 vs 6/100 | **1.282** | 🔴 **AGAINST ACEI** | 33.8% |

**Two of four point against ACEI, and they carry 51.5% of the inverse-variance weight.** A tuned set
would not look like this. **The recovered counts are not cherry-picked.**

Corroborating anti-tuning evidence in the doc, which I checked rather than accepted:
- Part III's rule set **overturned 8 of 14** of the lane's own prior ad-hoc exclusions — toward
  **more** inclusion (BORDERLINE/BELONGS) — and the trials were **still excluded** on the frozen
  design detectors. A rule set that merely re-derived prior intuition would be worthless; this one
  contradicted its author.
- It includes an explicit retraction: Hy-C's *"non-randomised-era design"* claim **retracted as
  never verified**.
- SOLVD-prevent (n=4,228), CAPRICORN (1,959), SHIFT (6,558), VICTORIA (5,050) were **fully recovered
  and still excluded** — large, available, and out, because the frozen verdict said so.

### ⚠️ THE FRAGILITY — the convergence rests on one small unbalanced trial

**CASSIS carries 32.4% of the backbone weight on an RR of 0.280 — the most extreme value in the set —
from a highly unbalanced design (ACEI 200 vs placebo 48, roughly 4:1).** It is the single trial
pulling the ACEI node down toward Tang's 0.83.

⇒ **A leave-one-out on CASSIS must be run and reported before ESC.** If removing CASSIS restores an
offset, then "the offset vanished" is really "one small unbalanced trial with 6 placebo deaths moved
the point estimate," which is a materially weaker claim than the one Part VI makes. *In CASSIS's
favour:* it is the **best-sourced** of the four — T4 (kup.at, an independent non-review source) **plus**
T5 ×2 — so this is a **leverage** concern, not a provenance concern.

### ⚠️ NOT VERIFIED BEFORE DELIVERY — state it rather than imply it

**I could not independently confirm the 20:20:50 freeze artifact.** `grep -rl "20:20:50"` over
`F:\E156` returns only three files that *reference* the timestamp
(`HFREF-OURS-VS-PUBLISHED`, `PREDICTION-MAHMOOD`, `SHARED-LANE-NOTES`) — **no frozen list, JSON, or
script bearing that mtime**, and a `find -newermt` sweep of `F:\E156` and `C:\key` for the 20:15–20:25
window returned nothing. `PREDICTION-MAHMOOD-2026-07-18.md` **does** check out (mtime 20:41 vs a
claimed 20:40:53 recording), so *that* pre-registration is real.

⇒ **The freeze is currently self-attested, not independently verifiable.** The behavioural evidence
above (8 overturned calls, 4 large trials recovered-then-excluded, 2 of 4 counts against ACEI) is
**consistent** with a genuine freeze and is what I would actually rely on — but the artifact itself
should be produced, or the claim softened from *"frozen at 20:20:50"* to *"recorded in the Part-VI
narrative."* **Do not cite a timestamp that has no artifact behind it.**

---

## HFrEF PASS — SUMMARY

| # | Claim | Verdict |
|---|---|---|
| **10** | *"The 7–8% offset vanished; 4/6 nodes reproduce Tang to 1%"* | 🔴 **KILL THE FRAMING** — Tang was already inside our CI on **6/6** nodes in Part V; Part VI's min detectable offset is **+56–93%** vs a 7–8% claim |
| **12** | T5 circularity — *"we copied Tang's inputs"* | 🟢 **SURVIVES** — Burnett uncited by Tang; De Marzo cited **Discussion-only**; Tang cites all four primaries; Captopril-Digoxin N=300 vs our 204 proves independent extraction |
| **13** | Donor identifier | 🔴 **DEFECT** — *"Aimo 2022 / PMID 35389544"* is **De Marzo 2022 / PMID 35332595**; 35389544 is an **electrocatalysis paper**. Six places. Fix before ESC |
| **14** | Counts tuned to close the gap | 🟢 **SURVIVES** — 2 of 4 backbone trials point **against** ACEI, carrying 51.5% of weight |
| **14b** | The 20:20:50 freeze artifact | ⚠️ **UNVERIFIED** — no artifact found; behaviourally consistent, but soften the claim or produce the file |
| **14c** | CASSIS leverage | 🟠 **run leave-one-out before ESC** — 32.4% weight, RR 0.280, 200 vs 48 design |
| **11** | Mahmood's prediction deflated to p≈0.57 | 🟢 **SURVIVES** — arithmetic exact; two-sided p is **1.0000**, i.e. even less informative than stated; tautology argument sound |
| — | k≥2 edges are genuine independent trials, not companion papers | ⚠️ **NOT COMPLETED** — see below |

⚠️ **One requested attack did not finish: the k≥2 / near-duplicate check** (are FEST, CASSIS, Brown,
Captopril-Digoxin genuinely separate trials rather than companion papers or shared-program protocols,
the US-Carvedilol D3 risk in reverse). Partial reassurance only: the four are from four different
sponsors, journals and years (Eur Heart J 1995 · Eur J Clin Pharmacol 1995 · Am J Cardiol 1995 ·
JAMA 1988) with distinct drugs (fosinopril · cilazapril · fosinopril · captopril), and the doc's D3
detector demonstrably caught the real instance (MOCHA/PRECISE/Colucci/Cohn). **But FEST and Brown 1995
are both fosinopril trials published in 1995 and share an author (MacLean A) — that pair specifically
must be checked for patient overlap before ESC.** I am flagging it rather than clearing it.

**Closing.** The load-bearing risk Mahmood named — circularity via T5 — **does not hold**, and the
recovery work is sound. What does not survive is the **framing**: a network whose intervals span a
factor of 2.4 cannot certify agreement to 1%. The strongest true statement available is the one the
lane already wrote and then over-claimed past — *a k=1 edge produced false precision and concealed
I²=32.5%.* That is a real finding about our own method. **"We reproduce Tang" is not.**

---

## 15. 🔴🔴🔴 AMENDMENT — THE CONVERGENCE IS ONE TRIAL, AND THAT TRIAL'S COUNTS DO NOT EXIST

> **This section supersedes the "fragility" caveat in §14 and hardens §10 from "unverifiable" to
> "refuted." The leave-one-out I recommended has now been run. It is decisive.**
> **`HFREF-OURS-VS-PUBLISHED` Part VI must NOT go to ESC in its current form.**

### 15.1 CASSIS's arm counts match no arm of the published trial

Verified independently via Europe PMC, **PMID 7614505** (Cardiology 1995;86 Suppl 1:34–40),
abstract verbatim:

> *"443 patients with chronic heart failure … cilazapril (CLZ) 2.5 mg once daily (**n = 221**),
> captopril (CPT) 25–50 mg three times daily (**n = 108**), or **placebo (PLA) for 12 weeks followed
> by CLZ 2.5**…"*

**Real arms: cilazapril 221 · captopril 108 · placebo 114 (443 − 221 − 108).**
**The doc records `ACEI 7/200 vs placebo 6/48`** (line 1096).

| doc value | any real arm? |
|---|---|
| ACEI **200** | ❌ not 221, not 108, not 329 (combined ACEI) |
| placebo **48** | ❌ **42% of the real placebo arm (114)** |

Neither denominator exists in the trial. And the design forecloses the contrast the doc is drawing:
**the placebo arm received placebo for only 12 weeks, then crossed to cilazapril.** There is no clean
placebo comparison to extract at all.

### 15.2 ⭐⭐⭐ Leave-one-out: CASSIS *is* the convergence, the heterogeneity, and the widening

Reproduced the shipped Part VI figure exactly, then removed CASSIS:

| set | RR (95% CI) | k | τ² | I² |
|---|---|---|---|---|
| **All 5 — reproduces shipped Part VI** | **0.833 (0.534–1.300)** | 5 | **0.0898** | **32.5%** |
| **WITHOUT CASSIS** | **0.891 (0.807–0.984)** | 4 | **0.0000** | **0.0%** |
| *(Part V, k=1)* | *0.886 (0.801–0.979)* | 1 | — | — |
| *Tang* | *0.83* | | | |

*(The all-5 row matches the doc's `0.833 (0.534–1.300), τ²=0.0898, I²=32.5%` to three decimals,
confirming the pooling model is correctly specified.)*

**Three separate Part VI headline claims collapse to this one trial:**

1. **The convergence.** Without CASSIS the estimate is **0.891** — back to essentially the Part V
   value of 0.886. The ratio to Tang returns to **1.073**, i.e. **the "7–8% systematic offset"
   reappears exactly.** ⇒ *"The disagreement with Tang has collapsed to zero"* is, precisely,
   **"one trial with non-existent denominators moved the point estimate."**
2. **The heterogeneity lesson.** *"The Placebo→ACEI edge carries real heterogeneity (I²=32.5%) that
   was structurally invisible at k=1"* — **without CASSIS, τ²=0.0000 and I²=0.0%.** The entire
   heterogeneity finding is CASSIS. The other four trials are perfectly homogeneous.
3. **The false-precision correction.** The CI widening (0.807–0.984 → 0.534–1.300) that §10 identified
   as destroying the network's discriminating power is **also entirely CASSIS.**

⇒ **The single most-quoted sentence of Part VI, the methodological lesson drawn from it, and the
precision loss that made the lesson unverifiable are all one 1995 supplement-sourced trial whose
denominators cannot be found in its own publication.**

### 15.3 🔴 CORRECTION AGAINST MYSELF

In §14 I graded the CASSIS issue **"SURVIVES (with a fragility)"** and merely *recommended* a
leave-one-out before ESC. **That was too soft, and my stated reason was wrong.** I wrote that CASSIS
was *"best-sourced of the four — T4 (kup.at) plus T5 ×2 — so this is a leverage concern, not a
provenance concern."* **Both halves were wrong:** it is a leverage concern **and** a provenance
concern, and the multiplicity of sources (three) did not protect it — three sources agreeing on a
denominator that does not appear in the trial is **three copies of one error**, which is exactly the
failure mode §12's circularity attack was designed to find and did not, because I tested the *donor's*
independence rather than the *number's* correctness against the primary.

⭐ **The generalisable lesson, and it is the sharpest one in this report:** *multiple-sourcing
establishes that a number was copied consistently — not that it is right.* Provenance depth and
provenance **correctness** are different tests. Every T5-derived count in this network needs the
second test, not just the first.

### 15.4 ⚠️ One rule WAS applied in the gap-closing direction — detector D6

PIONEER-HF was excluded (line 1108) as **`D6 — 2-month follow-up, below the mortality floor.`** But
**FEST is a 12-week trial** and **CASSIS's placebo period is 12 weeks** — barely above that floor,
with mortality as an incidental safety count rather than an endpoint. Both were **included**, and
both sit on the one edge (`Placebo→ACEI`, k=1→k=5) whose thickening produced the headline.

**A short trial on an already-thick edge was excluded; short trials on the thin decisive edge were
included.** I found **no evidence this was deliberate** — but it is the one place in Parts IV–VII
where a rule was applied asymmetrically in the direction that closes the Tang gap. **D6 needs a
stated numeric threshold and a symmetric re-run.**

### 15.5 ✅ What still stands — the anti-tuning verdict SURVIVES, and strongly

The defects above are **errors, not tuning**, and the evidence for that is strong enough to state
plainly:

- **EPHESUS is the decisive test and it exonerates the lane.** V-4 line 960 shows that including
  EPHESUS moves the two worst ratios **1.228/1.210 → 1.062/1.046** — it would have closed the two
  remaining gaps — and it was **kept out of the primary anyway**. *You cannot tune toward a target
  while discarding the single lever that most closes it.*
- **SOLVD-prevent (4,228), CAPRICORN (1,959), SHIFT (6,558), VICTORIA (5,050)** were all fully
  recovered — counts on file — and **still excluded**, every one **away** from Tang's inclusion set.
- **Part III's 8-of-14 overturns are genuine**, 7 of 8 moving toward Tang's set (making the lane's
  own prior look worse), and one is an explicit **self-retraction of an unsourced claim**.
- **2 of 4 backbone trials point against ACEI** (§14), carrying 51.5% of the weight.

⇒ **This is a competent lane that made a data error on one trial, not a lane that steered.** The
distinction matters for how the finding is repaired: **re-source CASSIS, don't re-audit the process.**

### 15.6 The freeze artifact — KILLED, independently confirmed

`grep -rln "20:20:50"` over `F:\E156`, `C:\key`, `C:\Projects` returns **exactly three files, all
retrospective narrative prose**; `git log --since="2026-07-18 17:00"` is **empty**; the earliest
on-disk trace is `SHARED-LANE-NOTES.md` at **20:39:54 — 19 minutes AFTER the claimed freeze and after
the Part-VI recovery calls had run.** No JSON, no list, no script.

⚠️ **Distinguish two freezes, because one is real:** `NMA-INCLUSION-AUDIT-CRITERIA.md` has mtime
**19:50:15** and genuinely predates Parts V/VI/VII. **The D1–D7 criteria freeze survives. The
verdict freeze does not.** Stop citing 20:20:50 as a provenance guarantee; cite the criteria file,
which exists.

### 15.7 Prediction deflation — two corrections, both against the lane

§11's SURVIVE verdict holds and is reinforced: **0.566 is the *minimum attainable* p-value for this
design** — the test could not have produced a significant result under *any* outcome. Two errors,
neither changing the verdict:

1. **Line 1275 conflates p with power:** *"a test with p ≈ 0.57 power to detect a violation."* A
   p-value is not power. Correct: *"a test whose minimum attainable p-value is 0.57, hence zero power
   at any conventional α."*
2. **The Fisher test covers only the tautological arm** (reachability × registration). The
   *materiality* arm — the substantive half, which the lane itself identifies as the real content —
   gives `C(26,2)/C(49,2) = 0.276`, **~2× more informative than the arm actually reported.** The lane
   **under-credited its own principal's prediction.**

---

## ⇒ REVISED HFrEF VERDICT

| # | Claim | Verdict |
|---|---|---|
| **15.1–15.2** | *"The 7–8% offset vanished; 4/6 nodes reproduce Tang to 1%"* | 🔴🔴 **REFUTED.** Remove CASSIS — whose denominators (200, 48) match no arm of PMID 7614505 (221/108/114) — and the estimate returns to **0.891**, ratio **1.073**: the offset comes back exactly |
| **15.2** | *"The edge carries real heterogeneity (I²=32.5%) invisible at k=1"* | 🔴 **REFUTED** — without CASSIS **τ²=0.0000, I²=0.0%** |
| **15.3** | My own §14 "fragility, not provenance" grading | 🔴 **WRONG — corrected here** |
| **15.4** | Detector D6 symmetry | 🟠 **asymmetric in the gap-closing direction** — needs a numeric threshold + re-run |
| **15.5** | Tuning / steering | 🟢 **SURVIVES** — EPHESUS kept out though it would have closed the gap; 4 large trials recovered-then-excluded; 8 self-overturns |
| **15.6** | 20:20:50 verdict freeze | 🔴 **KILLED** — no artifact, no commit; earliest trace 19 min later. *Criteria* freeze (19:50:15) is real |
| **15.7** | p≈0.57 deflation | 🟢 **SURVIVES** — but "p as power" is an error, and the materiality arm (0.276) was under-credited |

**Required before any ESC use:** ① re-source or pull CASSIS and re-run the backbone; ② fix
De Marzo/PMID 35332595 (§13); ③ disclose Tang's ref [70]; ④ give D6 a numeric threshold and re-run
symmetrically; ⑤ stop citing 20:20:50; ⑥ check FEST/Brown for patient overlap (both fosinopril, 1995,
shared author MacLean A).

**Closing.** I came into this pass hunting circularity, and circularity is not what was wrong — §12
cleared it on real evidence. The defect was one layer lower and I nearly walked past it: **I verified
that our sources were independent of Tang, and did not verify that our numbers were right.** Three
independent donors carried the same wrong denominator, and multiplicity read as confirmation. The
convergence that looked too good was too good — but the tell was never in the agreement. It was in a
placebo arm of 48 that no one had checked against a trial of 114.
