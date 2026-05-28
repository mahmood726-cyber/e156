# E156-PROTOCOL — e156 living evidence capsules (flagship suite)

- **Project:** e156 living evidence capsules — flagship suite (12 meta-analysis designs)
- **Created:** 2026-05-28
- **Dashboard:** https://mahmood726-cyber.github.io/e156/flagship/
- **Repository path:** `e156/flagship/`
- **Status:** built and engine-verified (Node); deployed to GitHub Pages. Demo data is illustrative.

## Description (E156 form)

This suite asks whether a single self-contained HTML file can carry a complete, trustworthy
evidence-synthesis analysis for each major meta-analytic design. Each capsule embeds editable
demonstration data and recomputes its estimates live in the browser with no server or
dependencies. The methods span pairwise, network, diagnostic, prevalence, dose-response,
survival/RMST, Bayesian, and meta-regression analyses, plus RoB2, PRISMA 2020, trial sequential
analysis, and GRADE. Each capsule reports its primary estimand with an interval and a
heterogeneity summary, and exposes the exact engine code for inspection. Robustness rests on a
self-auditing assurance ribbon that only clears when the internal arithmetic reconciles, and on
a copy-paste R script that reproduces the estimate in the field-standard package. The intended
use is teaching, prototyping, and transparent reporting — not a replacement for a protocolised
systematic review. Boundaries: the data shipped is illustrative, browser rendering was not
exhaustively verified across engines, and Gold-tier assurance requires independent reproduction.

## Contributors

Authored as tooling/methodology/software. Per the e156 authorship rule, on any derived
manuscript MA serves as a middle author (software / methodology), never first or senior author.

## Verification

- Engines validated in Node against hand or independent recomputation (estimates + edge cases).
- Structural checks: balanced tags, no literal `</script>` in template literals, no hardcoded local paths.
- Offline: no external CDNs or network calls.
