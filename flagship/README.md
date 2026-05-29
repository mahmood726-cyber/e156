# e156 living evidence capsules — flagship suite

Forty self-contained HTML files spanning five method families — meta-analysis,
meta-research, causal inference, primary study designs, and health economics. Every
estimate is computed live in the browser, the data is editable, the engine is
reader-inspectable, and each result ships with a copy-paste R script that reproduces it in
the standard package. No server, no build step, no external dependencies — open any file
and it runs offline. `index.html` links all 40.

**Live:** https://mahmood726-cyber.github.io/e156/flagship/

> The capsule must agree with itself before asking the world to agree with it.

## Meta-analysis designs (15)

| # | Type | File | What it does |
|---|------|------|--------------|
| 1 | Pairwise | `sglt2-hf-capsule.html` | Random-effects pooling + estimator suite, GOSH, selection models, influence, in-browser R |
| 2 | Network | `nma-capsule.html` | Network meta-analysis with consistency checks, league table, SUCRA |
| 3 | Diagnostic | `dta-capsule.html` | Summary ROC, pooled sensitivity/specificity, threshold-effect check |
| 4 | Prevalence | `prevalence-capsule.html` | Logit random-effects single-proportion pooling with prediction interval |
| 5 | Dose-response | `doseresponse-capsule.html` | Two-stage random-effects trend with an uncertainty band |
| 6 | Survival / RMST | `survival-capsule.html` | Pooled restricted mean survival time + non-proportional-hazards check |
| 7 | Bayesian | `bayesian-capsule.html` | Full posterior, credible intervals, P(benefit), shrinkage forest — exact grid over (μ, τ) |
| 8 | Meta-regression | `metaregression-capsule.html` | Random-effects regression on a moderator, bubble plot, R² |
| 9 | Risk of bias (RoB2) | `rob2-capsule.html` | Cochrane RoB2 with algorithmically derived overall, traffic-light matrix |
| 10 | PRISMA 2020 | `prisma-capsule.html` | Flow diagram that reconciles — every box derived, negatives flagged |
| 11 | Trial sequential analysis | `tsa-capsule.html` | Cumulative Z vs O'Brien–Fleming boundary, heterogeneity-adjusted RIS |
| 12 | GRADE SoF | `grade-capsule.html` | Certainty derived from eight domains, absolute effects per 1000 |
| 13 | IPD | `ipd-capsule.html` | Within-trial vs across-trial effect modification; the ecological/aggregation bias only patient-level data resolves |
| 14 | Three-level | `threelevel-capsule.html` | REML variance decomposition for nested effect sizes; within- vs between-cluster (I²₂/I²₃) split |
| 15 | Correlation | `correlation-capsule.html` | Fisher z pooling with exact 1/(n−3) variance, back-transformed to r with a prediction interval |

## Meta-research & evidence integrity (7)

| Type | File | What it does |
|------|------|--------------|
| p-curve | `pcurve-capsule.html` | Right-skew (evidential value) test, 33%-power flatness test, estimated power |
| Fragility index | `fragility-capsule.html` | Single-patient flips to undo significance (Fisher's exact), vs lost-to-follow-up |
| Excess significance | `excess-significance-capsule.html` | Observed vs expected significant studies (Ioannidis–Trikalinos) |
| Prediction-interval gap | `prediction-gap-capsule.html` | CI excludes null but 95% prediction interval does not |
| Benford screening | `benford-capsule.html` | First-digit distribution vs Benford's law (χ² + Nigrini MAD) |
| Study overlap (CCA) | `overlap-cca-capsule.html` | Corrected covered area for overlapping reviews |
| Publication bias | `pubbias-capsule.html` | Funnel asymmetry, Egger's test, Duval–Tweedie trim-and-fill, conditional PET-PEESE |

## Causal & quasi-experimental (5)

| Type | File | What it does |
|------|------|--------------|
| Mendelian randomization | `mr-capsule.html` | IVW, MR-Egger (+ pleiotropy intercept), weighted median |
| Difference-in-differences | `did-capsule.html` | 2×2 group×period effect with the parallel-trends counterfactual |
| Regression discontinuity | `rdd-capsule.html` | Local linear jump at a cutoff, adjustable bandwidth |
| Interrupted time series | `its-capsule.html` | Segmented regression: level change + slope change |
| Propensity-score balance | `psbalance-capsule.html` | Love plot of SMDs before vs after adjustment |

## Primary study designs (8)

| Type | File | What it does |
|------|------|--------------|
| RCT / CONSORT | `rct-capsule.html` | Flow reconciliation, RR/OR/ARR/NNT, sample-size adequacy |
| Prediction model (TRIPOD) | `prediction-capsule.html` | ROC/AUC + Brier + calibration plot/slope |
| Observational (STROBE) | `strobe-capsule.html` | Crude vs adjusted, DAG, E-value |
| Diagnostic (STARD) | `stard-capsule.html` | Se/Sp/PPV/NPV/LRs (Wilson CIs) + prevalence dependence |
| Survival (KM/Cox) | `survival-primary-capsule.html` | Kaplan–Meier, log-rank, Cox HR, Schoenfeld PH check |
| Cluster RCT | `cluster-capsule.html` | ICC, design effect, effective N, naive-vs-cluster-adjusted CI (df = clusters − 2) |
| Non-inferiority | `noninferiority-capsule.html` | Risk difference vs a pre-specified margin, the five interpretation zones, one-sided NI test |
| Decision curve | `dca-capsule.html` | Net benefit vs threshold probability; model against treat-all and treat-none |

## Health economics & HTA (5)

| Type | File | What it does |
|------|------|--------------|
| Cost-effectiveness | `ce-plane-capsule.html` | ICER, CE plane + WTP threshold, INMB, dominance |
| Acceptability curve | `ceac-capsule.html` | Seeded PSA, scatter, probability cost-effective vs WTP |
| Markov model | `markov-capsule.html` | Transition matrix, cohort trace, discounted cost/QALYs |
| Transportability | `transportability-capsule.html` | Effect-modifier SMDs + effect re-standardised to target |
| Value of information | `voi-capsule.html` | EVPI from a seeded PSA: per-person + population EVPI across willingness-to-pay |

`index.html` is the landing page linking all 40.

## What every capsule shares

- **Self-auditing assurance ribbon** (Bronze / Silver / Gold) that turns green only when the numbers reconcile; Gold is reserved for independent reproduction.
- **Editable data** that re-runs the analysis on every keystroke and persists in `localStorage`.
- **Reader-inspectable engine** — an "inspect the computation" panel prints the exact JavaScript via `Function.toString()`.
- **R cross-validation** — a copy-paste script for `metafor`, `meta`, `bayesmeta`, `mada`, `robvis`, `RTSA`, or GRADEpro.
- **Seeded accent** — each capsule's colour is hashed from its slug, so the suite is visually distinct but coherent.

## Status & honesty

- The statistical engines are **verified in Node** (estimates, edge cases, and structural integrity); each was checked against hand or independent recomputation.
- All capsules carry **illustrative demo data** — edit any table to load your own.
- Pooling is on the log scale and back-transformed; continuity corrections apply only to zero cells; heterogeneity is reported as τ² alongside I².
- These are analytical demonstrators, not a substitute for a full protocolised review.
