# CARDIO-NMA SUITE — protocol vs non-protocol, done once and done right
**2026-07-17. Orchestrator. One PICO taken end-to-end, per Mahmood's "ONE NMA AT A TIME."**
Working dir + producing scripts: `C:\Projects\cardio-nma-suite-2026-07-17\`. Pre-registration frozen before any result: `PRESPEC.md` (2026-07-17 22:02:37 GMT).
Provenance tags per METHODS-CONTRACT §0d Rule 0: **[M]** = measured (producing script + frame named) · **[F]** = fetched citation · **[R]** = recollection, verify before use.

---

## TL;DR — the result is a new defect class, so we keep going one at a time
The naive protocol-vs-non-protocol proxy is **"does the trial have an NCT number."** On the canonical large statin CVD-outcome trial set, that proxy calls **10 of 20 trials "registered." The number that are *prospectively* registered — registered before the first patient was enrolled, which is the only kind of registration that constrains anything — is 0 of 20.** [M] Every registry record in the set was created **retrospectively**, a median of **79 months (6.6 years) after enrollment began** (range 24–112), with submission dates clustering in 2005–2006 — the ICMJE-mandate wave. Even JUPITER, the trial everyone calls "the modern registered statin trial," was submitted to ClinicalTrials.gov **32 months after its first patient**. [M]

⇒ **"Registered" as usually coded is not a protocol guarantee; it is a publication-era artefact.** Mahmood's clean within-era contrast (b) — *registered vs not, era held constant* — is **not merely under-powered in cardiology; it is unidentifiable in this trial universe, because the prospective-registration cell is empty (0/20)**, and that emptiness is now *measured*, not asserted. This is the new defect class this NMA produced ⇒ **it taught something, so the one-at-a-time cadence stays; do not batch yet.**

---

## 1. The reframe that had to happen first (why the corpus can't answer this internally)
| Fact | Value | Producing script | Frame |
|---|---|---|---|
| RapidMeta analyzable apps | 514 | `bias-shadow-2026-07-17/final_stats.py` | Served RapidMeta HTML corpus (1240 files; 726 stubs) |
| Trials that are NCT-tagged | 95.2% [M] | same | topics chosen so their RCTs are in CT.gov |
| Multi-treatment **network** objects in corpus | **0** [M] | same | every "NMA"-named app is pairwise-shaped (single pooled DL + 2-arm trials) |
| k (trials per app), median | 2 [M] | same | — |

The prior session concluded the corpus is *"protocol-mandatory by construction"* and therefore cannot contain a non-registered arm. **That conclusion is now itself downgraded:** it counted **NCT-presence**, and §3 below shows NCT-presence does not equal prospective registration. So even RapidMeta's "protocol arm" is of *unverified prospectivity*. The task genuinely requires leaving the corpus for the decades-spanning trials — exactly as Mahmood argued. His correction of my objection was right, and it was right for a deeper reason than either of us stated: the old trials aren't just *unregistered*, and the new ones aren't cleanly *registered* — **the registry's own timestamps split the field three ways, and nobody uses them.**

## 2. Deliverable #1 — the largest cardiology RCT syntheses (enumeration, provenance-tagged)
⚠️ Selection rule frozen in `PRESPEC.md` before looking: RCT-only (§0e); rank by k trials then n patients; single-class-vs-inert-comparator preferred for the deep dive so era is not *also* confounded with drug class. Multi-class HFrEF networks and DOAC-vs-warfarin AF networks were **pre-rejected as the deep PICO** (reasons in PRESPEC), kept only as enumeration rows.

| Synthesis (PICO) | k trials | n patients | Type | Tag |
|---|---|---|---|---|
| **Naci 2013** — statins, CV prevention, ACM + major coronary | **92** | **199,721** | Network MA | **[F]** PMID 23447425, DOI 10.1177/2047487313480435 |
| CTT 2010/2012 — statins per 1 mmol/L LDL, major vascular events | ~26–27 | ~170,000 | IPD pairwise | [R] verify k/n before quoting |
| BPLTTC — BP-lowering classes, CV events | ~50 | ~360,000 | IPD network/pairwise | [R] verify |
| Antithrombotic Trialists' — antiplatelet, vascular events | ~287 | ~200,000 | pairwise | [R] verify |
| HFrEF pharmacotherapy (e.g. Tromp 2022 Lancet) | ~70–75 | tens of thousands | Network MA | [R] verify |
| DOACs vs warfarin, AF, stroke/SE | ~4–10 | ~70,000 | pairwise/network | [R] — used below as the "new side is ~100% registered" case |

Only the Naci row is [M]/[F] this turn. The rest are **pointers to be fetched next**, not quoted as fact (§0d Rule 0). The IPD collaborations (CTT, BPLTTC, ATC) are the *largest by n* but are pairwise/subgroup, not multi-treatment networks — state which when citing.

## 3. Deliverable #2 — protocol vs non-protocol, SHOWN not filtered (the core result)
Producing script `reg_lag.py` → `reg_lag.json`. Frame: the 20 canonical large statin CVD-outcome RCTs commonly pooled by CTT/Naci; **NCT resolved from the registry (never recalled); startDate + studyFirstSubmitDate from the official ClinicalTrials.gov API v2** (`protocolSection.statusModule`). `lag = submit − start`. Classes: `unregistered` (no NCT; enrollment ended before CT.gov existed, 2000-02) · `retrospective` (submit after start, >3-mo grace) · `prospective` (submit ≤ start+3mo).

| Trial | Drug | Pub | NCT | Enroll start (reg) | First submitted | Lag (mo) | Class [M] |
|---|---|---|---|---|---|---|---|
| 4S | simvastatin | 1994 | — | — | — | — | unregistered |
| WOSCOPS | pravastatin | 1995 | — | — | — | — | unregistered |
| CARE | pravastatin | 1996 | — | — | — | — | unregistered |
| AFCAPS/TexCAPS | lovastatin | 1998 | — | — | — | — | unregistered |
| LIPID | pravastatin | 1998 | — | — | — | — | unregistered |
| HPS | simvastatin | 2002 | — | — | — | — | unregistered* |
| PROSPER | pravastatin | 2002 | — | — | — | — | unregistered |
| ASCOT-LLA | atorvastatin | 2003 | — | — | — | — | unregistered |
| MEGA | pravastatin | 2006 | — | — | — | — | no-NCT-found |
| 4D | atorvastatin | 2005 | — | — | — | — | no-NCT-found |
| ALLHAT-LLT | pravastatin | 2002 | NCT00000542 | 1993-08 | 1999-10-27 | 74 | retrospective |
| CARDS | atorvastatin | 2004 | NCT00327418 | 1997-01 | 2006-05-16 | 112 | retrospective |
| SPARCL | atorvastatin | 2006 | NCT00147602 | 1998-11 | 2005-09-06 | 82 | retrospective |
| TNT | atorvastatin | 2005 | NCT00327691 | 1998-04 | 2006-05-16 | 97 | retrospective |
| IDEAL | atorvastatin | 2005 | NCT00159835 | 1999-02 | 2005-09-08 | 79 | retrospective |
| SEARCH | simvastatin | 2010 | NCT00124072 | 1998-07 | 2005-07-22 | 84 | retrospective |
| CORONA | rosuvastatin | 2007 | NCT00206310 | 2003-09 | 2005-09-16 | 24 | retrospective |
| GISSI-HF | rosuvastatin | 2008 | NCT00336336 | 2002-08 | 2006-06-12 | 46 | retrospective |
| JUPITER | rosuvastatin | 2008 | NCT00239681 | 2003-02 | 2005-10-13 | 32 | retrospective |
| AURORA | rosuvastatin | 2009 | NCT00240331 | 2003-01 | 2005-10-16 | 33 | retrospective |

\*HPS is registered under ISRCTN (ISRCTN48489393), not CT.gov; its CT.gov record was not resolved — counted here as CT.gov-unregistered, ISRCTN status not date-checked. Flagged for the next pass.

**Summary [M]:** 20 trials · naive "has NCT" = **10** · **prospectively registered = 0** · retrospectively registered = 10 · unregistered/no-record = 10. Lag among the 10 with dates: min 24, **median 79**, max 112 months.

### The two contrasts, reported separately (never collapsed — Mahmood's instruction)
- **(a) OLD vs NEW = registration × era, honestly confounded.** This is estimable and is the practical clinician's question. The registration classification for it is done (table above). ⚠️ The *pooled effect* contrast (old ACM vs new ACM) requires per-trial all-cause-mortality extraction (deaths/N per arm) — **scoped as the next fetch, not fabricated here.** Anchor for it: Naci 2013 pooled ACM overall OR **0.87 [0.82, 0.92]**, primary-prevention **0.91 [0.83, 0.99]**, secondary **0.82 [0.75, 0.90]** [F] — computed with **registration timing ignored entirely**, which is precisely the gap.
- **(b) WITHIN-ERA registered vs not, era held constant — the clean estimate of what registration is worth.** **Result: unidentifiable in this trial universe.** [M] Not because k is small, but because the *prospective-registration cell is empty (0/20)*. You cannot estimate the value of prospective registration from a set in which no trial was prospectively registered. ⚠️ **Contrast (a) must never be quoted as (b).** The honest sentence: *"the naive protocol-vs-non-protocol gap in the statin literature is entirely registration × era; the era-free component is not merely small, it is unmeasurable here, and the reason is measured (0/20 prospective)."*

### What actually makes contrast (b) reachable (the refined design, for the next PICO)
Prospective registration only became possible/enforced after CT.gov (2000) + ICMJE (2005) + FDAAA (2007). So a *prospective* cell exists only for trials that **started ≥ ~2007** — the SGLT2i / ARNI / PCSK9 / DOAC era. Within that era, the clean 3-level ordinal the registry timestamps support is **prospective (started post-FDAAA, registered before enrollment) vs retrospective (started pre-2005, registered in the mandate wave) vs unregistered (completed pre-2000)**. That is the estimand nobody publishes, and it is measurable with `reg_lag.py` scaled to a modern-era PICO. ⚠️ Even there, expect the *unregistered-modern* cell to be near-empty (post-2007 major cardiology RCTs are ~universally registered) — so the modern clean contrast is **prospective vs retrospective**, not registered vs not.

## 4. Deliverable #3 — check against a published NMA on the same PICO
**Comparator: Naci et al. 2013, Eur J Prev Cardiol** [F] (PMID 23447425, [DOI](https://doi.org/10.1177/2047487313480435)) — a Bayesian NMA of 92 statin RCTs (199,721 patients), all-cause mortality OR 0.87 [0.82, 0.92].

**Decomposition of the difference between our frame and theirs (§7 four buckets, never collapsed):**
1. **Extraction error on shared trials (our bug):** none yet — we have not pooled effects, so no extraction dispute exists. Correct state to be in before claiming disagreement.
2. **Trial-set difference:** Naci pools 92 trials **treating registration timing as irrelevant** — all 92 enter the same network regardless of whether they were prospectively registered, retrospectively registered, or unregistered. **Our contribution is orthogonal to their estimate, not a disagreement with it:** we are not re-estimating the statin effect; we are measuring a trial-level covariate (registration prospectivity) that their synthesis, and every statin NMA, silently sets aside. Same PICO, different question — stated per §5 so neither launders the other.
3. **Analytic-choice difference:** Naci uses OR on a Bayesian network; the estimand-honest contrast for ACM across registration classes would use RR/HR with REML + HKSJ and a **null-crossing flag across FE/DL/PM/REML** (machinery already built & metafor-validated: `bias-shadow-2026-07-17/pool_estimators.py`). Recorded now so it is not an unstated choice later (the bedaquiline lesson).
4. **Bias-adjustment difference:** neither side applies one; stated so.

## 5. Non-negotiables from the brief — status
- **Record the estimator; flag null-crossing.** Machinery wired and validated (`pool_estimators.py`, FE/DL/PM/REML + z/HKSJ). On the *served RapidMeta corpus* the estimator-choice sign-flip rate is **2/469 (0.4%)** DL↔PM [M] (`final_stats.py`) — i.e. the bedaquiline-shaped defect is *rare* in the served corpus, but the flag now exists and fires. For the statin ACM pooling (pending per-trial fetch) the same flag will run.
- **"Unambiguous is not correct."** This deliverable is an *instance* of that rule paying off: every one of the 10 NCTs resolved to exactly one real, on-topic trial (the join was clean), and the naive reading — "10 registered" — was confidently, unanimously **wrong**. The registry timestamp is what caught it.
- **The registered-but-never-reported gap** ("the withdrawn confirmatory trial is exactly the gap"): not yet run for statins. Method for next pass: query CT.gov for phase-3/4 statin CVD-outcome trials with `overallStatus` in {TERMINATED, WITHDRAWN, UNKNOWN} and no results/publication link. Scoped, not claimed.
- **RCT-only (§0e):** entire frame is RCTs. ✓
- **`bias-adjusted-nma-adv` read-only:** untouched. Frozen TB holdout: untouched. ✓

## 6. The honest ledger — what is measured vs pending
**Measured this turn [M]:** the registration-lag table (0/20 prospective; 10 retrospective, median lag 79mo; 10 unregistered), JUPITER's 32-mo lag, the RapidMeta reframe numbers, the corpus estimator sign-flip rate. All reproduce from `reg_lag.py`, `final_stats.py`, and `provenance_ledger.json`.
**Fetched [F]:** Naci 2013 pooled ACM estimates and trial/patient counts.
**Pending (scoped, NOT fabricated):** per-trial all-cause-mortality events/N for the pooled effect contrast (a); scaling `reg_lag.py` across the RapidMeta corpus's NCTs to report its retrospective %; the registered-but-unreported statin trial search; HPS ISRCTN date-check.
**Not done and not claimed:** any pooled old-vs-new effect number; any within-era (b) effect number (unidentifiable — reported as such).

## 8. JOB 1 — THE CORPUS-WIDE LAG SCAN (added 2026-07-18) — **my statin finding does NOT generalise, and I lead with that**
Producing scripts: `corpus_reg_scan.py` → `corpus_reg_scan.json`, attacked by `reg_sensitivity.py` → `reg_sensitivity.json`. Cache `nct_reg_cache.json` shared via `C:\Projects\SHARED-LANE-NOTES.md`.
**Frame (§0b):** the SERVED local RapidMeta corpus (`corpus_records.jsonl`): 1,240 files → 726 stubs → **514 analyzable apps → 508 with ≥1 NCT → 1,075 unique NCTs** (1,376 refs). `how_drawn`: regex `^NCT\d{8}` over `trials[].id`, deduped. **Cannot contain:** live-only apps (local 1,240 ≠ live 1,448), non-CT.gov registries (ISRCTN/PACTR/EUCTR ≈ 4.8% "other"), the 726 stubs.

### ⚠️ THE HEADLINE IS UNFLATTERING TO MY OWN PRIOR RESULT — say it first (§17, §0)
**"RapidMeta is ~95% registered" was indeed the naive NCT-presence proxy. Re-pricing it does NOT collapse it — it corrects it modestly.** [M]

| Class (strict: submitted ≤ first-patient) | n / 1,075 | % [95% Wilson] |
|---|---|---|
| **PROSPECTIVE** | 825 | **76.7% [74.1, 79.2]** |
| RETROSPECTIVE | 249 | 23.2% [20.7, 25.8] |
| NONE (no usable record) | 1 | 0.1% [0.0, 0.5] |
| *prospective, 30-day grace* | *971* | *90.3% [88.4, 92.0]* |

**Adversarial bound on the month-precision parse** (329/1,074 startDates are month-only): strict **76.8% – 84.8%**; 30-day grace **90.4% – 93.2%**. ⚠️ **I got the direction of this caveat backwards on first pass and the sensitivity caught me:** `lag = submit − start`, so flooring a month-start to day 1 makes the lag *larger* and prospective *rarer* — the scan's choice was the **conservative** one, and its headline is a **lower** bound. Both scripts corrected on disk.

⇒ **The statin result (0/20 prospective) was TRUE but ERA-SPECIFIC, and must never be quoted as a general claim about the corpus.** The corpus is a *modern* corpus: **1,006/1,074 (93.7%) of its dated trials started ≥2007.** That single fact explains the whole difference — §0 in its own right (our ceiling ≠ the world's limit), caught this time before publication rather than after.

### Per-era — the confound, isolated
| First-patient era | n | prospective (strict) | prospective (30-day grace) |
|---|---|---|---|
| start < 2007 | 68 | **25.0% [16.2, 36.4]** | 44.1% [32.9, 55.9] |
| start ≥ 2007 (FDAAA) | 1,006 | **80.3% [77.7, 82.7]** | 93.5% [91.8, 94.9] |

The pre-2007 cell reproduces the statin finding's direction (25%, CI excludes 50%); the post-2007 cell inverts it. **Registration prospectivity is almost entirely an era variable.**

### ⭐ The timeline nobody has drawn — the year prospective became the norm
Prospective rate by first-patient year (n≥5): 2003 **0.0%** → 2004 15.4% → 2005 30.0% → 2006 45.5% → 2007 50.0% → **2008 60.0% ← first year >50%** → 2011 66.7% → 2014 76.7% → 2017 87.8% → **2018 93.5%** → **2021 96.0%**.
⇒ **Prospective registration becomes the norm in 2008 — one year after FDAAA (Sept 2007)** — and saturates >93% from 2018. [M]

### Lead time — how much warning the registry actually got (the weaker half of the good news)
| Lead | n / 1,074 | % [95%] |
|---|---|---|
| >180 d before start | 88 | 8.2% [6.7, 10.0] |
| 91–180 d | 160 | 14.9% [12.9, 17.2] |
| 31–90 d | 295 | 27.5% [24.9, 30.2] |
| 8–30 d | 206 | 19.2% [16.9, 21.6] |
| **0–7 d (just-in-time)** | 76 | **7.1% [5.7, 8.8]** |
| after start (retrospective) | 249 | 23.2% [20.8, 25.8] |

Median lag **−31 days**; p75 **−2 days**. Only **50.6%** got >30 days of lead. **A registration filed the week enrollment opens is a thinner guarantee than the binary "prospective" implies** — report the lead-time band, not just the flag. Worst retrospective lag: **4,998 days = 13.7 years**.

### ⭐⭐ The filter falls out — the sequence for "do all the cardio NMAs"
| App class (508 apps with ≥1 NCT) | n | % [95%] |
|---|---|---|
| **(b)-eligible — non-empty prospective cell** (Mahmood's literal definition) | 456 | **89.8% [86.8, 92.1]** |
| **…of which BOTH cells non-empty — a within-app (b) contrast is actually estimable** | **154** | **30.3% [26.5, 34.4]** |
| (a)-ONLY — no prospective trial at all | 52 | 10.2% [7.9, 13.2] |

⚠️ **Two numbers, and the difference matters.** By the literal definition **456 apps are (b)-eligible** — but 302 of those are **all-prospective**, so there is no non-prospective cell to contrast *against*: within them (b) is as unidentifiable as it was in the statins, for the mirror-image reason. **The count Mahmood needs tonight is 154** — the apps where both cells are non-empty and a within-app prospective-vs-not contrast can actually be run. That is not small; it is a working sequence.

## 9. JOB 2 — SGLT2i in heart failure, one PICO end-to-end (2026-07-18)
**App:** `SGLT2_HF_REVIEW.html` (identical trial set to `SGLT2I_HF_NMA_REVIEW.html`), k=5, measure=OR. Producing scripts `sglt2_hf_job2.py`, `soloist_probe.py`, `soloist_impact.py`, `sglt2_finish.py`. **Estimand note:** the registered protocol `F:\E156\protocols\sglt2-hf-protocol.md` covers the **full EF spectrum**, and this trial set does too (HFrEF + HFpEF) — so this is *SGLT2i-in-HF*, not HFrEF-only. Stated per §5; no amendment taken.

### Step 1 — reproduce as-published: **EXACT** [M]
My DL reproduces the baked `pooled_DL` at **Δ|logOR| = 0.000e+00**, Δτ² = 0.000e+00. The app's arithmetic is faithful.

### Step 2 — estimator panel + null-crossing: **a clean null (the no-harm stratum, §9)** [M]
| method | OR | z-CI | sig | τ² | I² |
|---|---|---|---|---|---|
| FE | 0.7349 | [0.687, 0.787] | ✓ | 0 | 0.0% |
| DL | 0.7116 | [0.623, 0.813] | ✓ | 0.0164 | 72.7% |
| PM | 0.7071 | [0.600, 0.833] | ✓ | 0.0284 | 82.2% |
| REML | 0.7086 | [0.609, 0.825] | ✓ | 0.0234 | 79.2% |

**No sign flip, no significance flip, no z→HKSJ downgrade.** The estimator choice does not move the conclusion here — reported as prominently as any win.
⚠️ **But the REML 95% prediction interval is [0.4403, 1.1404] — it CROSSES THE NULL.** The pooled CI is significant; the PI is not. The app displays neither the PI nor this fact.

### Step 3 — ⭐⭐ NEW DEFECT CLASS: **"right number, right endpoint, WRONG UNIT"**
**SOLOIST-WHF (NCT03521934) stores t 245/608, c 355/614. Those are not participants — they are the trial's RECURRENT-EVENT TOTALS.** [M]

CT.gov's own record says so verbatim: *"Combined endpoint of the **total number of occurrences (first and potentially subsequent)** of CV death, HHF, and urgent HF visits… calculated as the **total number of events per 100 person-years**"* — `paramType=NUMBER`, `unit='events per 100-person years'`, values **51** vs **76.3**, denominators 608/614 participants.

**Arithmetic confirmation** (`soloist_impact.py`): 245 ÷ 51 × 100 = **480.4 person-years** over 608 patients = **9.5 months** mean follow-up; placebo 355 ÷ 76.3 × 100 = 465.3 py over 614 = **9.1 months**. Both reconstruct SOLOIST's ~9-month median. 245/355 are the **rate numerators**.
⇒ The app forms `245/(608−245)` — but **608 − 245 = 363 is a count of nothing**: a participant may contribute more than one event. Implied **OR 0.4924** against the registry's own **rate ratio 0.6684** — the defect makes SOLOIST look **1.53× more protective** than its own registry entry.

**Why every existing gate misses it:** 245 < 608 so the arithmetic gate passes · right trial, right endpoint name, so the identity and comparison gates pass · the number is **real and is the trial's actual headline figure**, so no fabrication or wrong-row check fires. It is distinct from the xcheck lane's *"right number, wrong endpoint"* — here the endpoint is right too. **Only the `unit` field distinguishes them.**

**Impact — the heterogeneity is entirely manufactured** [M]:
| Pooling (REML) | ratio | 95% CI | τ² | I² | 95% PI |
|---|---|---|---|---|---|
| (i) as-published *(defect)* | 0.7086 | [0.609, 0.825] | 0.0234 | **79.2%** | [0.44, **1.14**] ← crosses null |
| (ii) SOLOIST excluded (k=4) | 0.7642 | [0.712, 0.821] | 0 | **0.0%** | [0.68, 0.86] |
| (iii) SOLOIST as rate ratio (k=5) | 0.7479 | [0.701, 0.798] | 0 | **0.0%** | [0.68, 0.82] |

**I² 79.2% → 0.0%. τ² 0.023 → 0. The prediction interval stops crossing the null.** The point estimate moves only +5.6% and **direction and significance never flip** — so a conclusion-level checker would call this meta fine. What the defect actually corrupts is the *heterogeneity*, and therefore anything downstream of it: the random-effects choice, τ²-based weighting, the PI, meta-regression, and a GRADE downgrade for inconsistency that the data do not support.

⭐ **The detector (implementable, and it reuses an instrument the xcheck lane already built).** That lane added `RATE_UNIT` exclusion to stop rates *falsely refuting* counts. The same signal, inverted, finds true defects: **if the registry's only version of the declared endpoint is a rate, and the app's stored numerator ≈ that rate's numerator (events ≈ rate/100 × plausible person-years), the cell is events-as-participants.** ⚠️ **The rate-only signal alone is NOT sufficient** — EMPEROR-Reduced and EMPEROR-Preserved also post rates only, yet their stored counts (361/1863, 415/2997) are the correct *published participant* counts. The discriminator is whether the stored numerator reconstructs the rate.

### Step 4 — the three counts, and the four buckets (§7) [M]
| | n |
|---|---|
| trials in the app's meta | 5 |
| present in CT.gov | 5 |
| with results posted | 5 |
| **posting a per-arm PARTICIPANT COUNT** | **2 / 5** |
| posting only rates for the primary | 3 / 5 |
| FDA applications with a review (this app) | **0** |

| Trial | Bucket |
|---|---|
| DAPA-HF | **1 AGREE** — all four cells reproduce in the registry |
| DELIVER | **1 AGREE** — all four cells reproduce |
| EMPEROR-Reduced | **4 UNRESOLVABLE** — registry posts rates only; count not refutable |
| EMPEROR-Preserved | **4 UNRESOLVABLE** — same |
| SOLOIST-WHF | **2 OUR BUG** — recurrent-event total as binomial count |

⚠️ **Only 2 of 5 trials in a flagship modern cardiology meta can be verified against the registry at all.** This is the ARISTOTLE finding reproduced on a cardiology PICO: *unconfirmable ≠ wrong.* And **the FDA referee is unavailable here — 0 applications with a review match this app**, so `FDA_REVIEWER_COMPUTED` could not be run. Coverage only; no reviewer comparison executed.

### Step 5 — both protocol arms: ⚠️ **(b) is NOT estimable here, and that is my selection error**
All five trials are **prospectively registered** (lags −13, −18, −14, −25, −46 days). [M] The non-prospective cell is **empty**, so the clean within-era contrast is unidentifiable — the mirror image of the statin failure.
**I chose this PICO by reasoning that the modern era is "where a prospective cell finally exists" — but the contrast needs BOTH cells, and my own JOB-1 scan had already produced the list of 154 apps that have both. I did not use my own filter.** That is the process defect of this run, and it is exactly the failure mode the filter was built to prevent.

### Step 6 — transparency payload ✅
`sglt2_transparency_ledger.jsonl` — 5 records in the `PROVENANCE-UX-2026-07-18` contract schema, six required fields populated, honouring all three render rules: `anchor_granularity=TAB_LEVEL` (CT.gov results is a JS SPA — no row anchors synthesised), `provenance_tag=REGISTRY_SPONSOR_REPORTED` (never bare "REGISTRY"), and `excerpt_verbatim` quoting the whole outcome row including arms not used.

### Step 7 — the next PICO, chosen by the filter this time
**16 cardio-named apps have BOTH cells non-empty** (contrast (b) genuinely estimable). Ranked:
`ALIROCUMAB_LIPID` k=6 (2 prospective / **4 non-prospective**) ← the only one with a substantial non-prospective cell · `HF_QUADRUPLE_NMA` k=6 (5/1) · `TNK_VS_TPA_STROKE` k=6 (5/1) · `ABLATION_AF` k=4 (3/1) · `FCM_HF` k=4 (2/2) · `DOAC_AF_NMA` k=3 (2/1) · `DABIGATRAN_VTE` k=3 (1/2) …
⇒ **`ALIROCUMAB_LIPID_AUTO_FULL_REVIEW.html` is the correct next PICO** — it is the only cardio app where the non-prospective cell is large enough for the contrast to carry any power.

## 10. THE BIAS-CODE STEP — SGLT2i-HF through `bias-adjusted-nma-adv` (2026-07-18)
**Engine:** read-only snapshot @ `7cf1663` (`bias-shadow-2026-07-17/engine_snapshot`). **Codex's laptop tree was never touched, and no SSH was needed** — the bias-shadow lane had already archived it for exactly this. Fed through the sanctioned `rapidmeta_adapter` schema. Producing script `run_engine_sglt2.py` → `engine_sglt2.json`.

### ⚠️ First: §4 says read the code before believing it — and **§4's own recorded finding is now OUT OF DATE**
The contract records *"no bias channel exists… `sponsor_bias.py` computes its adjustment after the fit, prints it, and never feeds back. Three dead layers."* **At `7cf1663` the channel is LIVE and I traced it end-to-end** [M]:
`model.py:627` calls `sponsor_auditor.adjust_doi_welton_quality()` **inside** the fit → `model.py:672` `variance = variance / rob_weight` → the adjustment reaches the estimate. It is gated by `apply_sponsor_bias`, which **fails closed** (`:622-626` raises unless real sponsor + attrition metadata are registered). `apply_indirectness`/`target_population` exist as a **separate** channel with the estimand named in code (`enriched_as_randomised` | `unselected_target`) — so run-in is *not* filed under `rob_weight`. **§4 should be amended: the layers are wired now.**

### The mechanism, and what it can arithmetically do
`adjust_doi_welton_quality`: industry sponsor → ×0.80; attrition LAR>0.05 → ×(1−min(0.30,(LAR−0.05)×2)); floor 0.1. **These are hand-set constants (§3 — not externally calibrated); treated as a sensitivity axis, not a truth.**

**Registry facts fetched for the gate** (real `Lost to Follow-up` dropWithdraw counts, **not** `started−completed`) [M]:
| Trial | Sponsor class | Randomised | **Real LTFU** | LAR |
|---|---|---|---|---|
| DAPA-HF | INDUSTRY | 4,744 | 2 | 0.00042 |
| EMPEROR-Reduced | INDUSTRY | 3,730 | 46 | 0.01233 |
| EMPEROR-Preserved | INDUSTRY | 5,988 | 22 | 0.00367 |
| DELIVER | INDUSTRY | 6,263 | 3 | 0.00048 |
| SOLOIST-WHF | INDUSTRY | 1,222 | 0 | 0.00000 |

⚠️ **I refused to derive LTFU from `started − completed`, and that refusal mattered.** Those imply LAR ≈ 0.28–0.32 for the EMPEROR pair (event-driven censoring, not attrition) and **1.00 for SOLOIST** (`completed=0` for both arms — terminated early on funding loss). Using them would have fired the attrition penalty on four of five trials from an artefact. The **real** LARs are 0.0004–0.0123 — **every one below the 0.05 threshold, so the attrition term never fires.**

⇒ **The adjustment collapses to a uniform ×0.80 on every study**, because *all five trials are industry-sponsored*.

### Raw vs bias-adjusted [M]
| Dataset | Arm | OR | 95% CI | se | τ (REML) | crosses null |
|---|---|---|---|---|---|---|
| k=5 as-published | RAW | 0.7086 | [0.580, 0.865] | 0.1019 | 0.15287 | no |
| k=5 as-published | **BIAS-ADJ** | **0.7123** | [0.586, 0.866] | 0.0995 | 0.138 | no |
| k=4 SOLOIST removed | RAW | 0.7642 | [0.697, 0.838] | 0.0472 | ~0 | no |
| k=4 SOLOIST removed | **BIAS-ADJ** | **0.7642** | [0.689, 0.847] | 0.0528 | ~0 | no |
| either | INDIRECT (both estimands) | identical to RAW | — | — | — | — |

**τ² cross-check (engine's own):** `METHODS_CROSSING_NULL = ()` — **no estimator crosses the null**, signs identical across FE/DL/PM/REML. Engine warns *"alternative τ² estimators produce different heterogeneity estimates"* at k=5 (τ² range 0–0.0284) and is silent at k=4. **The bedaquiline test is NEGATIVE for this PICO.**

⭐ **Independent-implementation cross-validation:** engine `taus={'rct': 0.15287}` is τ, so **τ² = 0.023369** — matching my independent pure-Python REML τ² of **0.023369** to 5 decimals. Two implementations, one number.

### ⭐⭐ THE STRUCTURAL FINDING — and it bounds the whole "use the NMA bias" programme for cardiology
**At k=4 the bias adjustment left the point estimate EXACTLY unchanged (0.7642 → 0.7642) and only widened the CI** (se 0.04721 → 0.05279, ratio **1.118 = 1/√0.8** — the predicted value). That is not a quirk of these data; it is a property of the mechanism:

> **A sponsor penalty applied uniformly to an all-industry evidence base is mathematically inert on the point estimate.** Inverse-variance weights are scale-invariant: dividing every variance by the same 0.80 leaves normalised weights identical, so only the pooled SE moves.

⚠️ **Essentially every major cardiology outcome trial is industry-sponsored.** So across this whole cardio programme the sponsor channel will widen CIs and never move point estimates. **The only channel that can move a cardiology estimate is attrition — and it requires LAR > 0.05, which these landmark trials miss by an order of magnitude.** The small k=5 shift (0.7086→0.7123, *away* from benefit) is not differential down-weighting; it is τ² re-estimation interacting with uniform inflation — and that heterogeneity is itself the SOLOIST artefact.

⚠️ **The indirectness channel returned numbers IDENTICAL to raw under BOTH estimands.** Reported as observed: on this dataset it is inert — either not wired for this data shape or requiring per-study covariates I did not supply. **Not** to be read as "indirectness makes no difference."

### ⭐⭐⭐ THE HEADLINE COMPARISON
| Source of movement | ΔOR |
|---|---|
| **Our own extraction defect** (SOLOIST events-as-participants) | 0.7086 → 0.7642 = **+7.8%** |
| The entire bias-adjustment engine | 0.7086 → 0.7123 = **+0.5%** |

**Our extraction defect moved the estimate ~8× more than the bias-adjustment engine did — and it fabricated the entire heterogeneity (I² 79%→0) on top.** For this PICO, data provenance dominates bias modelling by an order of magnitude. No direction change, no null crossing, no guideline reversal.

## 11. ⭐⭐⭐ CONTRAST (b) IS NOT ESTIMABLE IN CARDIOLOGY — the question closes, negative (2026-07-18)
Producing scripts `b_eligible_robustness.json`, `b_eligible_tiers.json` (from `corpus_reg_scan.json`, 1,075 NCTs / 508 apps). **This corrects a number I gave Mahmood.**

### The "154 estimable apps" was over-stated ~2.3×
I reported 154/508 apps with both registration cells non-empty as the working set for contrast (b). Re-tested against the date-precision convention [M]:
| Test | Result |
|---|---|
| strict both-cell apps (lag ≤ 0) | 154 |
| **robust** — both cells survive a 30-day grace | **68/154 = 44.2% [36.6, 52.0]** |
| **fragile** — contrast collapses under grace | **86/154 = 55.8% [48.0, 63.4]** |

**Cause [M]:** of 249 retrospective NCTs corpus-wide, **146 (58.6% [52.4, 64.6]) have lag ≤ 30 days**, and **86 of those (58.9%) carry month-precision start dates** ⇒ **34.5% [28.9, 40.6] of every "retrospective" call in the corpus is a near-zero-lag month-precision guess** that flooring `YYYY-MM` to day 1 manufactured.

### The filter that actually orders the list — and empties it
A contrast is only real if the non-prospective cell contains trials whose lag is **unambiguous** (>90 days — flooring cannot flip them):
| Tier | Definition | Count | Cardiology |
|---|---|---|---|
| **TIER-1** | ≥2 prospective AND ≥2 non-prospective with lag>90d | **2/154 = 1.3% [0.4, 4.6]** | **0** |
| TIER-2 | ≥1 and ≥1 hard | 29/154 = 18.8% [13.4, 25.7] | 5 |
| neither | contrast rests on ≤30d / ambiguous calls | **123/154 = 79.9% [72.8, 85.4]** | — |

**The only two TIER-1 apps are `MALARIA_ACT_REVIEW` (k=5, 2 vs 3 hard, max lag 946d) and `RELUGOLIX_FIBROIDS` (k=4, 2 vs 2, max lag 99d). Neither is cardiology.**
The five cardiology TIER-2 apps — FONDAPARINUX (×2), TNK_VS_TPA_STROKE, DABIGATRAN_VTE, FCM_HF — **every one has `hard = 1`**: a single unambiguously-retrospective trial. A 5-vs-1 or 3-vs-1 split is not an estimate of what registration is worth; with k=1 in a cell you cannot separate registration from that one trial's every other property. **It is a case study, not an estimate.**

### ⚠️ My own flip-flop, resolved
I first disqualified `ALIROCUMAB_LIPID` (lags +5/+7/+15 d on month precision), then retracted that because it survived the binary grace test. **The retraction was the error — my grace test was too weak.** Under the hard-cell filter ALIROCUMAB has **`hard = 0`, max lag 34 days**: its entire non-prospective cell is inside the date-precision noise. **The first call was right, for the right reason.** Recorded because §0d Rule 5 says the orchestrator's correction rate must be visible.

### ⭐⭐⭐ THE MECHANISM — the natural experiment closed itself
Contrast (b) is unidentifiable on **both** sides of the mandate, for **opposite** reasons:
- **Pre-2007:** registration varies in principle, but the *prospective* cell is ~empty (statins **0/20**; corpus pre-2007 cell 25.0% [16.2, 36.4] and thin — only 68/1,074 trials).
- **Post-2007** (93.7% of the corpus): the *prospective* cell is full (80.3% [77.7, 82.7]), but the *non-prospective* cell has collapsed — and what remains is late by **days, not years** (58.6% of retrospective calls ≤30d).

> **FDAAA did not merely make registration common; it made it near-simultaneous with enrollment. Universality and instantaneity arrived together, and together they destroyed the variation needed to price registration.** The window in which both cells are genuinely populated is vanishingly thin — **2 apps in 508, neither cardiological.**

⇒ **The clean estimate of what prospective registration is worth cannot be obtained from this corpus, in cardiology or near it.** Contrast **(a)** (old-vs-new, registration × era, confounded) remains the only reportable contrast, and it must never be quoted as (b). This is a **negative result that closes the question** rather than leaving it open — §17.

## 7. Decision (Mahmood's success criterion)
This NMA **produced a new defect class** — *NCT-presence ≠ prospective registration; the "registered arm" is contaminated with cosmetic mandate-wave registrations, and the registry timestamp measures it.* Per the brief ("Report ANY NEW DEFECT CLASS: that is the result… If one teaches nothing new, SAY SO — that is the signal to batch"), the signal is: **keep the one-at-a-time cadence.** The next PICO should be a **modern-era single-class network (SGLT2i in HFrEF, or DOACs in AF)** — chosen precisely because it is where a *prospective* registration cell finally exists, making Mahmood's clean contrast (b) estimable for the first time. The plan to turn the thousand into a sequence is: run `reg_lag.py` on each PICO's trial set first; the ones with a non-empty prospective cell are the ones where (b) can be reported; the rest get (a)-with-the-confound-named. That ordering is now a mechanical filter, not a judgement call.

---

## ⚠️ CORRECTION 2026-07-18 (REMEDIATION lane) — THE STATIN `0/20` IS **TAUTOLOGICAL**

Red-teamed in `ADVERSARIAL-REDTEAM-2026-07-18.md` §3: **WEAKENED — SEVERELY.** The *number*
is right and survived attack. Its **interpretation** in this document does not.

**The kill: the denominator is zero-capable.** Registry start dates, confirmed live against
the CT.gov v2 API:

| | count |
|---|---|
| started before ClinicalTrials.gov launched (2000-02) | **16 / 20** |
| started after CT.gov existed | 4 — GISSI-HF 2002-08, AURORA 2003-01, JUPITER 2003-02, CORONA 2003-09 |
| **started after the ICMJE mandate (2005-09-13)** | **0** |
| started after FDAAA (2007) | 0 |

The latest-starting trial began **2003-09, two years before the mandate**. 4S (1988), WOSCOPS
(1989), CARE (1989), AFCAPS (1990) and LIPID (1990) began **8–12 years before the registry
accepted its first record.** Prospective registration was **impossible** for 16 and
**unmandated** for the other 4.

⇒ `0/20` does **not** measure researcher behaviour. It measures **calendar**. The phrase
*"the prospective-registration cell is empty"* (lines 11, 71) is true but **cannot support**
the inference that registration practice is what emptied it.

**Honest cell: `0/4`** (registry-era starts), 95% Clopper–Pearson upper bound **60.2%** —
the data are compatible with a true prospective rate of nearly two-thirds.

**The 79-month lag (line 93) is a re-encoding of the start date, not a behavioural quantity.**
`studyFirstSubmitDate` timestamps **three administrative batch events**, not 11 decisions:
an ICMJE-deadline wave of 7 (incl. **MEGA 2005-09-13 — literally the deadline**), a Pfizer
same-day batch of 2 (CARDS and TNT both 2006-05-16, 9-year start gap), and one NHLBI legacy
seed (ALLHAT-LLT 1999-10-27, predating public launch). **Effective independent n ≈ 3, not 11.**
Regressing lag on `(ICMJE deadline − start date)` gives **R² = 0.9884**.

**Bonus defect — resolver false negative.** `reg_lag.py:63-74` requires an exact `acronym`
match, which CT.gov often leaves empty. **MEGA is registered: NCT00211705** (start 1994-02,
submit 2005-09-13, lag 139 months) but `reg_lag.json:143` records `"no-NCT-found"`.
Corrections: naive "has NCT" is **11/20, not 10/20**; unregistered is **9, not 10**; max lag
is **139, not 112**. Median stays 79 by coincidence of odd n.

### ⇒ Caveat that must travel with this number

> The statin 0/20 is **not** evidence that investigators declined to pre-register. Every
> trial in the frame began before the 2005 ICMJE mandate (latest start 2003-09) and 16/20
> began before ClinicalTrials.gov existed. The only interpretable cell is **0/4 prospective
> among trials that started after the registry opened**, 95% CI [0, 60%] — suggestive, not
> conclusive. The 79-month median lag is 98.8% determined by start date (R²=0.988).

**What survives intact:** the *unidentifiability* conclusion at line 71 stands, and is if
anything strengthened — contrast (b) is unidentifiable in this trial universe. The error is
only in *why*: the cell is empty because of **era**, not because of researcher choice. The
warning *"contrast (a) must never be quoted as (b)"* remains correct.

**One attack that FAILED, reported for symmetry:** the `lag <= 3` prospective cutline
(`reg_lag.py:118,123`) is fine — month-resolution, **more lenient than ICMJE**, and every lag
in the frame is ≥24 months, so no flooring error can flip any call. The cutline is biased
*toward* the null it failed to find.
