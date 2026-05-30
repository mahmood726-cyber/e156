# Protocol — SGLT2 inhibitors and the risk of cardiovascular death or worsening heart failure

**Type:** Living systematic review and trial-level random-effects meta-analysis
**Version:** 1.0
**Drafted:** 2026-05-30
**Registration:** This protocol is pre-registered by committing it to public version control. The Git commit that first introduces this file — its SHA and the commit timestamp recorded by GitHub — is the authoritative, tamper-evident registration record (an open, code-native alternative to PROSPERO for a living, reproducible review). Subsequent substantive changes are tracked as dated amendments (below) and as further commits.

> The plan below is fixed **before** data extraction. The companion capsule
> (`flagship/sglt2-hf-capsule.html`) executes exactly this plan and re-runs it live;
> it links back to the registered commit of this protocol.

---

## 1. Review question

In adults with heart failure, do SGLT2 inhibitors added to guideline-directed therapy, compared with placebo, reduce the risk of the composite of cardiovascular death or worsening heart failure?

## 2. PICO

- **Population** — Adults with heart failure across the full ejection-fraction spectrum (HFrEF, HFmrEF, HFpEF).
- **Intervention** — An SGLT2 inhibitor added to background guideline-directed therapy.
- **Comparator** — Placebo.
- **Outcome (primary)** — Composite of cardiovascular death or a worsening-heart-failure event (hospitalisation for heart failure or an urgent HF visit), as adjudicated in each trial.
- **Estimand** — The pooled hazard ratio for the primary composite, intention-to-treat.

## 3. Eligibility criteria

**Include** if all of:
1. Randomised, placebo-controlled design.
2. Population is heart failure (the index condition), any ejection fraction.
3. Intervention is an SGLT2 inhibitor vs placebo.
4. Reports a hazard ratio (with a 95% confidence interval) for the primary composite, or sufficient data to derive one.

**Exclude** if any of:
- Population is type 2 diabetes or chronic kidney disease **without** heart failure as the index condition (HF only a secondary/exploratory outcome).
- Non-randomised design (observational, registry cohort, single-arm).
- Secondary or subgroup publication of an already-included trial (to avoid double-counting); such reports are retained only as companion references to the index trial.
- No primary HF composite hazard ratio reported or derivable.

## 4. Information sources and search strategy

- **Sources** — ClinicalTrials.gov (registry) and PubMed/MEDLINE. Reference lists of included trials and relevant reviews are hand-searched.
- **Planned search concepts** — (`SGLT2 inhibitor` OR `dapagliflozin` OR `empagliflozin` OR `sotagliflozin` OR `canagliflozin` OR `ertugliflozin`) AND (`heart failure`) AND (`randomized` OR `randomised` OR `placebo`).
- **Limits** — Human; randomised controlled trials; English-language reports of the primary results.
- **Dates** — From database inception to the search date recorded at each living-review update.
- **Deduplication** — By NCT identifier, then by normalised title.
- **Search yields** — The exact counts at each stage (records identified, after de-duplication, screened, full-text assessed, included) are recorded in the capsule's PRISMA flow at each update and are not pre-specifiable.

## 5. Study selection

- Two reviewers screen titles/abstracts independently against the eligibility criteria, then full texts of records passing the first stage.
- Disagreements are resolved by discussion or a third reviewer.
- Inter-reviewer agreement is reported as Cohen's κ at the title/abstract stage.
- Every excluded full-text record is listed with its specific exclusion reason; every screened record (included and excluded) is shown with a link to its registry entry and publication.

## 6. Data extraction

- Two reviewers extract independently into a structured form; discrepancies reconciled against the source.
- **Items** — trial name, registry ID (NCT), agent, publication year and source, 2×2 event counts (events and totals per arm), the reported hazard ratio and 95% confidence interval, and RoB 2 domain judgements.
- Each extracted value is traceable to the trial's registry record and primary publication (row-level provenance).
- A live denominator check confirms events never exceed the arm total.

## 7. Risk of bias

- Each trial is appraised independently by two reviewers using the Cochrane RoB 2 tool across its five domains, with an algorithmically-derived overall judgement.
- Disagreements reconciled by discussion or a third reviewer.

## 8. Effect measures and synthesis

- Hazard ratios are pooled on the natural-log scale by inverse-variance random-effects meta-analysis.
- Each trial's log-HR standard error is recovered from its confidence interval as (ln UCL − ln LCL) / (2 × 1.96).
- Between-study variance τ² is estimated by **Paule–Mandel** (primary; DerSimonian–Laird is biased for k < 10). REML and DL are reported as sensitivity analyses.
- A 95% **prediction interval** is computed on t₍k−1₎ degrees of freedom (Cochrane Handbook v6.5).
- A Hartung–Knapp–Sidik–Jonkman confidence interval is reported as a sensitivity analysis (with the q/df variance floor).
- **Heterogeneity** — I² and τ², with Cochran's Q.

## 9. Robustness, subgroups, and reporting bias

- **Influence** — leave-one-out, and a GOSH plot of every subset meta-analysis.
- **Cumulative** — meta-analysis by year of publication.
- **Subgroups** — by SGLT2-inhibitor agent (pre-specified).
- **Meta-regression** — on year of publication.
- **Reporting/publication bias** — contour-style funnel plot with Egger's radial regression test (acknowledged low power at k < 10), a Vevea–Hedges selection model, and a robust Bayesian model-averaging (RoBMA) sensitivity analysis where feasible.

## 10. Certainty of evidence

- Certainty in the pooled estimate is rated with **GRADE** across its domains. Inconsistency and imprecision are derived live from the analysis; risk of bias, indirectness, publication bias and the overall rating are reviewer judgements recorded explicitly.

## 11. Software and reproducibility

- The analysis is executed in the browser by the companion capsule (offline, single file), with the engine reader-inspectable.
- Every estimate is independently reproducible against R's `metafor` (a copy-paste script and an in-browser WebR run are provided).
- **Gold** assurance is reserved for an independent reviewer who re-runs the analysis and signs a certificate; the authors cannot grant it.

## 12. Authorship and competing interests

- Where a co-author serves on the editorial board of the target journal (`Synthēsis`), that author is restricted to a middle-author position, takes no role in editorial decisions on this manuscript, and handling is by an independent editor — disclosed in the submission.

## 13. Amendments log

| Date | Version | Change |
|------|---------|--------|
| 2026-05-30 | 1.0 | Initial registered protocol. |
