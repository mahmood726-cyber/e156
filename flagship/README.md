# e156 living evidence capsules — flagship suite

Twelve self-contained HTML files, one per evidence-synthesis design. Every estimate is
computed live in the browser, the data is editable, the engine is reader-inspectable, and
each result ships with a copy-paste R script that reproduces it in the standard package.
No server, no build step, no external dependencies — open any file and it runs offline.

**Live:** https://mahmood726-cyber.github.io/e156/flagship/

> The capsule must agree with itself before asking the world to agree with it.

## The 12 capsules

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

`index.html` is the landing page linking all twelve.

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
