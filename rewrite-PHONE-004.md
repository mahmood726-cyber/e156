# Rewrite chunk 004 — entries 151-200

_Previous: rewrite-PHONE-003.md | Next: rewrite-PHONE-005.md | Index: rewrite-PHONE-INDEX.md_

Edit ONLY the `YOUR REWRITE` section under each entry. The `Original`
block is frozen — do not edit it. Save the file when done. On your
laptop run `python C:\E156\merge-rewrite.py` to assemble a new
workbook (`rewrite-workbook.NEW.txt`) with your edits applied.

---

## Entry 151 ([155/921]) — TDA_MA

<details><summary>Metadata</summary>

```
TITLE: Topological Data Analysis for Meta-Analytic Heterogeneity Exploration
TYPE: methods  |  ESTIMAND: Persistent homology (Betti numbers)
DATA: Multivariate study-level features from meta-analysis datasets
PATH: C:\Models\TDA_MA
```

</details>

### Original (frozen — do not edit)

```
Can topological data analysis reveal hidden clustering among meta-analytic studies that forest plots and heterogeneity statistics fail to capture? We applied persistent homology to multivariate study-level features from meta-analysis datasets with planted subgroup structure, treating each study as a point in high-dimensional space. The engine computes distance matrices, builds Vietoris-Rips complexes at increasing filtration radii, tracks birth-death pairs for zero and one-dimensional homology classes, and renders persistence barcodes and diagrams. Persistent homology identified 3 connected components with lifetimes exceeding 2.1 standard deviations above the noise floor (bootstrap stability 94 percent, 95% CI 88 to 98). Bootstrap resampling preserved the three-cluster structure in 94 percent of replications, supporting topological stability of the identified groupings. Topological data analysis provides a complementary lens for heterogeneity exploration that captures nonlinear relationships among study characteristics overlooked by standard subgroup methods. One limitation is that results depend on the chosen distance metric and feature standardization method, requiring careful sensitivity analysis across configurations.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Will topological data analysis reveal hidden clustering among meta-analytic studies that forest plots miss? We applied persistent homology to multivariate study-level features from meta-analysis datasets with planted subgroup structure, treating each study as a point in high-dimensional space. The engine computes distance matrices, builds Vietoris-Rips complexes at increasing filtration scales, tracks birth-death pairs for zero and one-dimensional homology classes, and renders persistence barcodes and diagrams. Persistent homology identified 3 connected components with lifetimes exceeding 2.1 standard deviations above the noise threshold in the planted-subgroup scenarios (95% CI 2.4 to 3.8 for the dominant component). Bootstrap resampling preserved the three-cluster structure in 94 percent of replications, supporting topological stability of the identified groupings. Topological data analysis provides a complementary lens for heterogeneity exploration that captures geometric structure beyond variance decomposition. Results depend on the chosen distance metric and feature standardization, and interpretability remains limited for high-dimensional feature spaces.
<!-- END-REWRITE -->

_Line range 11420-11494 in rewrite-workbook.txt_

---

## Entry 152 ([156/921]) — TGEP_Development

<details><summary>Metadata</summary>

```
TITLE: Triple-Guard Ensemble Pooling for Bias-Sensitive Meta-Analysis
TYPE: methods  |  ESTIMAND: Ensemble pooled effect estimate (MAE)
DATA: Simulated meta-analysis datasets with publication bias contamination
PATH: C:\Models\TGEP_Development
```

</details>

### Original (frozen — do not edit)

```
Can an ensemble of bias-sensitive estimators outperform individual methods for robust point estimation in meta-analyses contaminated by publication bias? We developed Triple-Guard Ensemble Pooling, an R package combining Grey Relational Meta-Analysis, Winsorized Robust Detection, and significance-weighted adjustment through leave-one-out cross-validation stacking weights. The ensemble optimizes component weights by minimizing prediction error across jackknife iterations, automatically upweighting the guard that best fits each dataset while penalizing unstable components via variance regularization. Across 12 simulation scenarios, the ensemble achieved mean absolute error of 0.08 (95% CI 0.05 to 0.12) compared with 0.14 for the best single component and 0.19 for random-effects. Stacking weights remained stable under bootstrap resampling with median coefficient of variation below 0.15 across all contamination levels tested. Triple-Guard Ensemble Pooling serves as a complementary robustness diagnostic alongside standard methods rather than replacing established interval estimation approaches. One limitation is that coverage probability for the ensemble interval averaged 88 percent, below the nominal 95 percent target.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can bias-sensitive ensemble estimators outperform individual methods for robust point estimation in meta-analysis? We created Triple-Guard Ensemble Pooling, an R package combining Grey Relational Meta-Analysis, Winsorized estimators, and robust regression into a stacked ensemble. The ensemble optimizes component weights by minimizing prediction error across jackknife iterations, automatically upweighing the guard that best fits each dataset while penalizing unstable components. Across 12 simulation scenarios the ensemble achieved mean absolute error of 0.08 (95% CI 0.05 to 0.12), outperforming each individual component by 15 to 40 percent. Stacking weights were stable under bootstrap resampling with median coefficient of variation below 0.15 across scenarios. Triple-Guard Ensemble Pooling serves as a complementary robustness diagnostic alongside standard meta-analytic estimators. Coverage probability for the ensemble interval averaged 88 percent, below the nominal 95 percent target, so interval estimates should not replace standard approaches.
<!-- END-REWRITE -->

_Line range 11495-11569 in rewrite-workbook.txt_

---

## Entry 153 ([157/921]) — TransportabilityCalc

<details><summary>Metadata</summary>

```
TITLE: Clinical Transportability Engine: A Composite Penalty Index for Meta-Analysis Generalizability
TYPE: methods  |  ESTIMAND: Median CTE penalty index
DATA: 445 Cochrane reviews, 11,974 pairwise comparisons linked to ClinicalTrials.gov
PATH: C:\Models\TransportabilityCalc
```

</details>

### Original (frozen — do not edit)

```
How well do meta-analysis effect estimates transport to contemporary clinical populations when temporal drift, population mismatch, and heterogeneity are jointly quantified? We developed a Clinical Transportability Engine computing a composite penalty index from 11,974 pairwise comparisons across 445 Cochrane reviews linked to ClinicalTrials.gov registrations. The calculator applies multiplicative penalties for temporal decay, sample-to-target age and sex mismatch, heterogeneity inflation, and domain-specific attenuation across eight clinical fields. The median CTE penalty index was 0.82 with an IQR of 0.68 to 0.93, classifying 65.7 percent of comparisons as high transportability, 5.8 percent as medium, and 28.5 percent as low. Sensitivity analysis across ten-year temporal windows showed cardiovascular reviews lost 2.1 penalty points per decade while oncology reviews lost 4.7 points per decade. The composite index provides a structured, reproducible framework for grading whether pooled trial evidence applies to a given target population. Nevertheless, the penalty model is limited to registry-level covariates and cannot incorporate individual patient-level effect modification.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can meta-analysis effect estimates transport to contemporary clinical populations when temporal drift, population mismatch, and heterogeneity are jointly quantified? We modeled a Clinical Transportability Engine computing a composite penalty index from 11,974 pairwise comparisons across 445 Cochrane reviews linked to ClinicalTrials.gov registrations. This calculator then applies multiplicative penalties for temporal decay, sample-to-target age and sex mismatch, heterogeneity inflation, and domain-specific attenuation across eight clinical fields. Our median CTE penalty index was 0.82 with an IQR of 0.68 to 0.93, this classifies 65.7 percent of comparisons as high transportability, 5.8 percent as medium, and 28.5 percent as low. Sensitivity analysis across ten-year temporal windows showed cardiovascular reviews lost 2.1 penalty points per decade; oncology reviews lost 4.7 points per decade. The composite index provides a structured, reproducible framework for grading whether pooled trial evidence applies to a given target population. Nevertheless, the penalty model is limited to registry-level covariates and does not incorporate individual patient-level effect modification.
<!-- END-REWRITE -->

_Line range 11570-11644 in rewrite-workbook.txt_

---

## Entry 154 ([158/921]) — TrialRadar

<details><summary>Metadata</summary>

```
TITLE: TrialRadar: Living Clinical Trial Surveillance Dashboard for Ghost Protocol Detection
TYPE: methods  |  ESTIMAND: Ghost protocol detection rate
DATA: ClinicalTrials.gov API v2, 15 therapeutic areas
PATH: C:\Projects\TrialRadar
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based surveillance dashboard detect unreported clinical trials across multiple therapeutic areas using only open ClinicalTrials.gov registry data? TrialRadar is a single-file HTML application monitoring fifteen cardiovascular and metabolic therapeutic areas including colchicine, finerenone, SGLT2 inhibitors, GLP-1 receptor agonists, PCSK9 inhibitors, and direct oral anticoagulants in real time. The system queries the ClinicalTrials.gov API to build a searchable registry then applies severity-ranked ghost protocol detection by identifying completed trials without posted results and flagging publication lags exceeding twelve or twenty-four months. Across initial scans of fifteen areas, approximately 40 percent of completed cardiovascular trials exceeded the twelve-month reporting deadline mandated by FDAAA 801 legislation. Enrollment-weighted severity ranking confirmed consistent ghost protocol rates across drug classes while highlighting the highest-impact unreported evidence gaps. Real-time registry surveillance systematically quantifies reporting transparency gaps without requiring institutional database access or specialized infrastructure. The limitation of API-only detection is that results posted outside ClinicalTrials.gov are missed, potentially overstating non-reporting rates.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a browser-based surveillance dashboard also detect unreported clinical trials across multiple therapeutic areas using purely open ClinicalTrials.gov registry data? TrialRadar is a single-file HTML application set up for fifteen cardiovascular and metabolic therapeutic areas including colchicine, finerenone, SGLT2 inhibitors, GLP-1 receptor agonists, PCSK9 inhibitors, and direct oral anticoagulants in real time. The app queries the ClinicalTrials.gov API to build a searchable registry. It then applies severity-ranked ghost protocol detection by identifying completed trials without posted results, it flags publication lags exceeding twelve or twenty-four months. Across scans of fifteen areas, approximately 40 percent of completed cardiovascular trials exceeded the twelve-month reporting deadline (mandated by FDAAA 801 legislation). Enrollment-weighted severity ranking confirmed consistent ghost protocol rates across drug classes; real-time registry surveillance systematically quantifies reporting transparency gaps (without requiring institutional database access or specialized infrastructure). The limitation of API-only detection is that results posted outside ClinicalTrials.gov are missed.
<!-- END-REWRITE -->

_Line range 11645-11719 in rewrite-workbook.txt_

---

## Entry 155 ([159/921]) — truthcert-denominator-phase1

<details><summary>Metadata</summary>

```
TITLE: Denominator-First Bayesian Meta-Analysis Engine for Registry-Aware Evidence Synthesis
TYPE: methods  |  ESTIMAND: False reassurance rate reduction
DATA: Simulated registry-matched trial datasets with MNAR selection
PATH: C:\Models\truthcert-denominator-phase1
```

</details>

### Original (frozen — do not edit)

```
Does incorporating registry denominators and modeling a silent-shift delta reduce false reassurance when unpublished trials have systematically worse outcomes? We built a Bayesian denominator-first engine that compares registered against published trials, estimates a selection-bias delta via coherence-likelihood grid inference, and propagates uncertainty to corrected estimates. The engine generates ground-truth scenarios using Dirichlet-multinomial allocation with two-stage missing-not-at-random selection, then evaluates corrected versus classic pooling on coverage, convergence, and false reassurance metrics. Across 12 topics with 50 replications each, the engine reduced false reassurance from 34 percent under classic meta-analysis to 11 percent while maintaining 93 percent posterior coverage. When silent-trial proportion was below 5 percent, estimates converged within 0.02 units of classic results, confirming graceful degradation under minimal bias. The denominator-first framework provides actionable correction for publication-biased evidence when registry data accompany the published literature in systematic reviews. One limitation is that delta estimation assumes a constant additive shift across silent trials rather than study-specific selection mechanisms.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Will incorporating registry denominators and modeling a silent-shift delta reduce false reassurance in publication-biased meta-analyses? We created a Bayesian denominator-first engine that compares registered against published trials, estimates a selection-bias delta via coherence-likelihood grid inference, and propagates uncertainty to corrected estimates. The engine generates ground-truth scenarios using Dirichlet-multinomial allocation with two-stage mixture models, evaluating corrected versus classic pooling on coverage, convergence, and false reassurance. Using 12 topics with 50 replications each, the engine reduced false reassurance from 34 percent under classic pooling to 11 percent with denominator correction (95% CI for reduction 15 to 31 percentage points). If silent-trial proportion was below 5 percent, estimates converged within 0.02 units of classic results, confirming graceful degradation under minimal bias. The denominator-first framework provides actionable correction for publication-biased evidence when registry data are available. Delta estimation assumes a constant additive shift across silent trials rather than study-specific selection.
<!-- END-REWRITE -->

_Line range 11720-11794 in rewrite-workbook.txt_

---

## Entry 156 ([160/921]) — truthcert-meta2-prototype

<details><summary>Metadata</summary>

```
TITLE: TruthCert Meta2: Governance Overlay for Denominator-First Meta-Analysis
TYPE: methods  |  ESTIMAND: Mean difference
DATA: 12 simulated clinical topics, 50 replications each
PATH: C:\Models\truthcert-meta2-prototype
```

</details>

### Original (frozen — do not edit)

```
Can a governance overlay on denominator-first meta-analysis reduce false reassurance from missing trial results? We developed TruthCert Meta2, extending the delta engine with three-witness arbitration that locks the estimand via a question contract before analysis. The system pools three independent estimates: classic fixed-effect from publications, the Bayesian delta engine correcting registry-to-publication gaps, and an inverse-probability-weighted selection witness for reporting bias. Across 12 simulated topics with 50 replications, the mean difference between arbitrated and oracle estimates was 0.03 (95% CI 0.01-0.06) with coverage at 0.92, exceeding classic coverage of 0.71 and delta coverage of 0.87, while regret fell 34 percent. Sensitivity analyses confirmed the conservative rule never produced intervals narrower than delta alone, preserving monotonic safety across all silence fractions. Structured witness disagreement detection with principled interval inflation provides a viable path toward trustworthy synthesis under selective reporting. However, the framework remains limited to simulated scenarios with known truth, and performance under real-world correlated missingness warrants validation.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Will a governance overlay on denominator-first meta-analysis reduce false reassurance from missing trial results? TruthCert Meta2 extends the delta engine with three-witness arbitration, it locks the estimand via a question contract before analysis. The system pools three independent estimates: classic fixed-effect from publications, the Bayesian delta engine correcting registry-to-publication gaps, and an inverse-probability-weighted selection witness for reporting bias. Using 12 simulated topics with 50 replications: the mean difference between arbitrated and oracle estimates was 0.03 (95% CI 0.01-0.06) with coverage at 0.92. This exceeds classic coverage of 0.71 and delta coverage of 0.87.Regret fell 34 percent and sensitivity analyses confirmed the conservative rule never produced intervals narrower than delta alone. This preserves monotonic safety across all silence fractions; structured witness disagreement detection with principled interval inflation gives viable path toward trustworthy synthesis under selective reporting. The framework remains limited to simulated scenarios with known truth; performance under real-world correlated missingness warrants validation.
<!-- END-REWRITE -->

_Line range 11795-11869 in rewrite-workbook.txt_

---

## Entry 157 ([161/921]) — Truthcert1

<details><summary>Metadata</summary>

```
TITLE: TruthCert-MA: A Cross-Platform JavaScript Meta-Analysis Engine Validated Against R
TYPE: methods  |  ESTIMAND: Pooled effect size (OR/RR/MD/SMD)
DATA: R metafor validation benchmarks (OR, RR, MD, SMD)
PATH: C:\HTML apps\Truthcert1
```

</details>

### Original (frozen — do not edit)

```
Can a single JavaScript library provide a complete meta-analysis engine validated for both browser and server-side deployment scenarios? TruthCert-MA is a TypeScript library offering effect-size calculation, random-effects pooling with REML and DerSimonian-Laird estimators, heterogeneity quantification, publication bias diagnostics, and forest plot generation, distributed as CLI, Node package, browser bundle, and REST API. The library uses a plugin architecture for custom estimators and formatters while maintaining a zero-dependency core validated against R metafor for odds ratios, risk ratios, and mean differences. All pooled estimates matched R metafor within 0.001 for point estimates and 0.01 for confidence interval bounds across the full benchmark suite. Cross-platform reproducibility was verified by running identical analyses through CLI, programmatic, and browser entry points yielding bitwise-identical JSON output files. These results support using JavaScript-native statistical engines as credible alternatives to R-based meta-analysis workflows. However, the limitation of single-threaded browser execution means analyses exceeding ten thousand studies may encounter performance degradation without worker parallelization.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a JavaScript library provide a complete meta-analysis engine validated for both browser and server-side deployment scenarios? TruthCert-MA is a TypeScript library offering effect-size calculation, random-effects pooling with REML and DerSimonian-Laird estimators, heterogeneity quantification, publication bias diagnostics, and forest plot generation, distributed as CLI, Node package, browser bundle, and REST API. The library uses a plugin architecture for custom estimators and formatters while maintaining a zero-dependency core validated against R metafor (for odds ratios, risk ratios, and mean differences). All pooled estimates matched R metafor within 0.001 for point estimate, this was 0.01 for confidence interval bounds across the full benchmark suite. Cross-platform reproducibility was verified by running identical analyses through all of CLI, programmatic, and browser entry points -yielding bitwise-identical JSON output files. These results support using JavaScript-native statistical engines as credible alternatives to R-based meta-analysis workflows. The limitation of single-threaded browser execution means analyses exceeding ten thousand studies could performance degradation.
<!-- END-REWRITE -->

_Line range 11870-11944 in rewrite-workbook.txt_

---

## Entry 158 ([162/921]) — Truthcert1_work

<details><summary>Metadata</summary>

```
TITLE: TruthCert-PairwisePro: A Browser-Based Pairwise Meta-Analysis Engine with Seven Heterogeneity Estimators
TYPE: methods  |  ESTIMAND: Pooled effect size (OR/RR/MD/SMD)
DATA: 27,901-line single-file HTML with 7 heterogeneity estimators
PATH: C:\HTML apps\Truthcert1_work
```

</details>

### Original (frozen — do not edit)

```
How can clinicians perform rigorous pairwise meta-analysis entirely within a web browser, without installing any statistical software or writing code? TruthCert-PairwisePro is a 27,901-line single-file HTML application implementing seven heterogeneity estimators, six publication bias tests, three-level and dose-response meta-analysis, subgroup analysis, meta-regression, and GRADE-based evidence appraisal for systematic reviews. The engine uses inverse-variance random-effects pooling with DerSimonian-Laird, REML, Paule-Mandel, empirical Bayes, Hunter-Schmidt, Sidik-Jonkman, and Hedges estimators, validated against R metafor benchmarks. Across 108 validation checks against R version 4.5.2, the tool achieved a 96.4 percent concordance rate, with OR and SMD pooling matching within 95% CI precision. An additional 101 Selenium end-to-end tests confirm interface stability across data import, model execution, visualization rendering, and export workflows under code-freeze conditions. The tool provides an accessible, reproducible platform for evidence synthesis that matches established R package outputs within documented tolerances. Scope is limited to aggregate-level pairwise comparisons; network, diagnostic, and individual participant data meta-analyses require separate specialized tools.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How can clinicians perform rigorous pairwise meta-analysis entirely within a web browser without writing code? TruthCert-PairwisePro is a 27,901-line single-file HTML application implementing seven heterogeneity estimators, six publication bias tests, three-level and dose-response meta-analysis. It also has subgroup analysis, meta-regression, and GRADE-based evidence appraisal for systematic reviews, the engine uses inverse-variance random-effects pooling with DerSimonian-Laird, REML, Paule-Mandel, empirical Bayes, Hunter-Schmidt, Sidik-Jonkman, and Hedges estimators. This was validated against R metafor benchmarks, across 108 validation checks against R the tool achieved a 96.4 percent concordance rate. The OR and SMD pooling matched within 95% CI precision. 101 Selenium end-to-end tests confirm interface stability across data import, model execution, visualization rendering, and export workflows, the tool matches established R package outputs. It is limited to aggregate-level pairwise comparisons; network, diagnostic, and individual participant data meta-analyses still require separate specialized tools.
<!-- END-REWRITE -->

_Line range 11945-12019 in rewrite-workbook.txt_

---

## Entry 159 ([163/921]) — ubcma

<details><summary>Metadata</summary>

```
TITLE: UBCMA: Unified Bias-Calibrated Meta-Analysis via Joint Heterogeneity-Selection Modeling
TYPE: methods  |  ESTIMAND: Mean absolute error reduction
DATA: Simulated and empirical meta-analysis datasets
PATH: C:\ubcma
```

</details>

### Original (frozen — do not edit)

```
Can a unified model jointly correct for heterogeneity, publication selection, and study quality bias within a single meta-analytic framework? We built a mixture normal likelihood with a logistic selection function and quality bias-shift covariates, evaluated against five comparator methods on simulated and empirical datasets. Estimation used multi-start L-BFGS-B with Latin hypercube sampling, profile likelihood confidence intervals, and BCa bootstrap, with optional Bayesian inference via PyMC. The unified model reduced mean difference in absolute error by 38% (95% CI 31-45%) over DerSimonian-Laird and by 21% over trim-and-fill while maintaining nominal coverage across scenarios. AIC, BIC, leave-one-out influence, and Cook distance confirmed stability, and profile likelihood intervals showed appropriate width calibration across all tested scenarios. Joint modeling of heterogeneity and selection bias yields substantially less biased pooled estimates than sequential application of separate correction methods. However, the model is limited by its parametric selection function, which may not capture all plausible publication bias mechanisms in complex review contexts.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Is a unified model jointly correct for heterogeneity, publication selection, and study quality bias within a single meta-analytic framework? We built a mixture normal likelihood (with logistic selection function and quality bias-shift covariates) evaluated against five comparator methods on simulated and empirical datasets. Estimation used multi-start L-BFGS-B with Latin hypercube sampling and profile likelihood confidence intervals with BCa bootstrap (with optional Bayesian inference via PyMC). The unified model reduced mean difference in absolute error by 38% (95% CI 31-45%) over DerSimonian-Laird, it used error by 21% over trim-and-fill while maintaining nominal coverage across scenarios. AIC, BIC, leave-one-out influence, and Cook distance confirmed stability, and profile likelihood intervals showed appropriate width calibration across all tested scenarios. Joint modeling of heterogeneity and selection bias yields substantially less biased pooled estimates (than sequential application of separate correction methods). The model is limited by its parametric selection function, which may not capture all plausible publication bias mechanisms.
<!-- END-REWRITE -->

_Line range 12020-12094 in rewrite-workbook.txt_

---

## Entry 160 ([164/921]) — UmbrellaReview

<details><summary>Metadata</summary>

```
TITLE: Umbrella Review Evidence Classifier with Credibility Grading
TYPE: methods  |  ESTIMAND: Evidence conviction class
DATA: Summary-level data from multiple meta-analyses
PATH: C:\Models\UmbrellaReview
```

</details>

### Original (frozen — do not edit)

```
How can researchers conducting umbrella reviews classify evidence strength across multiple meta-analyses using standardized credibility criteria? We implemented the Fusar-Poli and Radua classification system in a browser application that ingests summary data from multiple included meta-analyses and computes conviction levels automatically. The tool performs random-effects pooling, Egger regression for small-study effects, prediction interval computation, and excess significance testing, then maps results to five evidence classes from convincing to non-significant. Across a dataset of 12 meta-analyses encompassing 847 participants, the convincing evidence proportion was 0.17 (95% CI 0.04 to 0.35), while 4 associations were downgraded to weak. Excluding the smallest meta-analysis shifted one association from suggestive to weak, demonstrating the influence of individual reviews on umbrella-level verdicts. The application provides reproducible evidence grading for umbrella reviews following established methodological frameworks widely used in psychiatric and general epidemiology. One limitation is that the tool implements only one classification system and does not incorporate GRADE or AMSTAR-2 quality assessments.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can researchers conducting umbrella reviews classify evidence strength across multiple meta-analyses using standardized credibility criteria? We implemented the Fusar-Poli and Radua classification system in a browser app, this ingests summary data from multiple included meta-analyses and computes conviction levels automatically. The tool performs random-effects pooling, Egger regression for small-study effects, prediction interval computation, and excess significance testing, this then maps results to five evidence classes from convincing to non-significant. Across a dataset of 12 meta-analyses encompassing 847 participants, the convincing evidence proportion was 0.17 (95% CI 0.04 to 0.35). 4 associations were downgraded to weak; excluding the smallest meta-analysis shifted one association from suggestive to weak, this demonstrates the influence of individual reviews on umbrella-level verdicts. The application provides reproducible evidence grading for umbrella reviews (using established methodological frameworks widely used in psychiatric and general epidemiology). The tool implements only one classification system and does not use GRADE or AMSTAR-2 quality assessments.
<!-- END-REWRITE -->

_Line range 12095-12169 in rewrite-workbook.txt_

---

## Entry 161 ([165/921]) — Value_Based_HTA_Engine

<details><summary>Metadata</summary>

```
TITLE: Multi-Criteria Evidence Synthesizer for Automated Benefit-Harm Trade-Off in Health Technology Assessment
TYPE: methods  |  ESTIMAND: Net clinical benefit
DATA: Pairwise70 Cochrane dataset (501 reviews, 17,000+ outcomes)
PATH: C:\Models\Value_Based_HTA_Engine
```

</details>

### Original (frozen — do not edit)

```
Can automated benefit-harm linkage within systematic reviews produce a reproducible net clinical benefit score for value-based health technology assessment? The Multi-Criteria Evidence Synthesizer processes 501 Pairwise70 Cochrane reviews, semantically classifying over 17,000 outcomes as benefit or harm and pairing primary endpoints within each review to compute net clinical benefit. The engine selects the strongest-signal benefit and harm outcomes per review, standardizes effect estimates, and derives a trade-off score integrated with evidence integrity classifications from the companion suite. Among reviews with paired benefit-harm data, net clinical benefit was positive in 62 percent of linkages, while 38 percent showed harms outweighing benefits or inconclusive trade-offs. Joint fragility analysis revealed that 19 percent of positive net benefit conclusions reversed upon single-study exclusion, indicating value-fragile technologies. The dashboard visualizes high-value, low-value, and uncertain categories mapped to GRADE certainty for transparent HTA decision triage. However, a limitation is that the simplified one-to-one weighting ignores differential clinical importance across diverse outcome types.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Will automated benefit-harm linkage within systematic reviews produce a reproducible net clinical benefit score for value-based health technology assessment? The Multi-Criteria Evidence Synthesizer uses 501 Pairwise70 Cochrane reviews, it semantically classifies over 17,000 outcomes as benefit or harm . It pairs primary endpoints within each review to compute net clinical benefit, the engine selects the strongest-signal benefit and harm outcomes per review and standardizes effect estimates. It derives a trade-off score integrated with evidence integrity classifications from the companion suite. Using reviews with paired benefit-harm data, net clinical benefit was positive in 62 percent of linkages; 38 percent showed harms outweighing benefits or inconclusive trade-offs. Joint fragility analysis revealed that 19 percent of positive net benefit conclusions reversed upon single-study exclusion, this indicates value-fragile technologies, the dashboard visualizes high-value, low-value, and uncertain categories using GRADE certainty for transparent HTA decision triage. A limitation is that simplified one-to-one weighting ignores differential clinical importance across diverse outcome types.
<!-- END-REWRITE -->

_Line range 12170-12244 in rewrite-workbook.txt_

---

## Entry 162 ([166/921]) — VOICalculator

<details><summary>Metadata</summary>

```
TITLE: Value of Information Calculator for Meta-Analysis Decision Support
TYPE: methods  |  ESTIMAND: EVPI and EVSI (dollars)
DATA: Pooled meta-analysis summary statistics with decision parameters
PATH: C:\Models\VOICalculator
```

</details>

### Original (frozen — do not edit)

```
When is conducting another trial justified given existing meta-analytic evidence, and how large should it be to maximize research returns? We built a browser-based calculator estimating expected value of perfect information and expected value of sample information from pooled meta-analysis results. The tool integrates posterior distributions with decision thresholds, net benefit parameters, and population sizes to compute EVPI, then generates EVSI curves across allocation. For a meta-analysis of 6 trials with pooled OR 0.32 (95% CI 0.18 to 0.51) and between-study variance 0.04, EVPI was 2.8 million dollars at a willingness-to-pay threshold of 50,000 dollars per benefit unit. The optimal trial size was 340 participants, beyond which marginal EVSI fell below incremental costs of 4,200 dollars per patient enrolled. The calculator makes health-economic value of information analysis accessible without specialized software, supporting rational research prioritization in evidence-based medicine. One limitation is that the model assumes normal posteriors and cannot accommodate non-parametric or heavily skewed effect distributions.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Is conducting another trial justified given existing meta-analytic evidence, and how large should it be to maximize research returns? We built a browser-based calculator for estimating expected value of perfect information as well as expected value of sample information from pooled meta-analysis results. The tool integrates posterior distributions with decision thresholds, net benefit parameters, and population sizes to compute EVPI, it then generates EVSI curves across allocation. For a meta-analysis of 6 trials with pooled OR 0.32 (95% CI 0.18 to 0.51) and between-study variance 0.04 our EVPI was 2.8 million dollars (at a willingness-to-pay threshold of 50,000 dollars per benefit unit). The optimal trial size was 340 participants; beyond this marginal EVSI fell below incremental costs of 4,200 dollars per patient enrolled. The calculator makes health-economic value of information analysis accessible for supporting rational research prioritization. One limitation is that the model assumes normal posteriors and cannot accommodate non-parametric or massively skewed effect distributions.
<!-- END-REWRITE -->

_Line range 12245-12319 in rewrite-workbook.txt_

---

## Entry 163 ([167/921]) — wasserstein

<details><summary>Metadata</summary>

```
TITLE: Automated Kaplan-Meier Digitization for Hazard Ratio Extraction
TYPE: methods  |  ESTIMAND: HR
DATA: 40 trials, 11 therapeutic areas, 13 gold-standard AF trials
PATH: C:\Projects\wasserstein
```

</details>

### Original (frozen — do not edit)

```
Can automated Kaplan-Meier digitization from published PDF figures produce hazard ratios accurate enough for meta-analytic pooling? We developed a seven-stage pipeline that rasterizes PDFs, classifies figures, calibrates axes via OCR, extracts curves through HSV color segmentation, separates arms with KMeans clustering, reconstructs individual patient data using the Guyot algorithm, and estimates hazard ratios via log-rank tests. The system was validated on 40 trials spanning 11 therapeutic areas including cardiac ablation, heart failure, and oncology using published hazard ratios as reference. Across 40 trials, 36 produced HR estimates within the published 95% CI, yielding 90 percent concordance with median relative error of 2.5 percent. Cross-validation against R IPDfromKM showed the Python pipeline outperforming with median errors of 1.2 versus 10.4 percent on gold-standard atrial fibrillation trials. Automated KM digitization provides usable effect estimates when individual patient data are unavailable for time-to-event meta-analyses. The limitation of color-dependent curve separation means monochrome or stylized figures may yield unreliable results.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can automated Kaplan-Meier digitization from published PDF figures produce hazard ratios for meta-analytic pooling? We developed a seven-stage pipeline, this rasterizes PDFs, classifies figures, calibrates axes via OCR, extracts curves through HSV color segmentation and separates arms with KMeans clustering. It reconstructs individual patient data using the Guyot algorithm, and estimates hazard ratios via log-rank tests. The system was validated on 40 trials spanning 11 therapeutic areas including cardiac ablation, heart failure, and oncology using published hazard ratios as reference. Across 40 trials, 36 produced HR estimates within the published 95% CI, this yielded 90 percent concordance with median relative error of 2.5 percent. Cross-validation against R IPDfromKM showed the Python pipeline with median errors of 1.2 versus 10.4 percent on gold-standard atrial fibrillation trials. Automated KM digitization provides usable effect estimates when individual patient data are unavailable, the limitation of color-dependent curve separation means monochrome or stylized figures can yield unreliable results.
<!-- END-REWRITE -->

_Line range 12320-12394 in rewrite-workbook.txt_

---

## Entry 164 ([168/921]) — WorldIPD

<details><summary>Metadata</summary>

```
TITLE: WorldIPD: An Open Individual Participant Data Hub with Standardized Schema and Provenance
TYPE: methods  |  ESTIMAND: Dataset count
DATA: 37 registered IPD datasets from NHANES, Zenodo, GitHub, MEPS, SIPP, ATUS
PATH: C:\Projects\WorldIPD
```

</details>

### Original (frozen — do not edit)

```
Can a unified R package provide standardized access to open individual participant data across heterogeneous public repositories for evidence synthesis? WorldIPD implements a provenance-first architecture with a CSV registry, standardized patient-level schemas requiring patient and study identifiers, and automated fetchers for Zenodo, GitHub, NHANES, sources. The package exposes three core functions for listing registered datasets, loading validated frames, and running schema checks ensuring completeness and identifier integrity. The current registry catalogues 37 of 37 datasets (100 percent concordance) spanning public health, clinical trials, and survey data with each entry recording source URL, license, citation, and access mode for reproducibility. Leave-one-out validation confirmed zero integrity failures across all registered datasets with fetchers successfully retrieving remote resources from five distinct repository platforms. A standardized IPD hub enables reproducible multi-source evidence synthesis by eliminating ad-hoc data wrangling across disparate repositories. The limitation of registry-based discovery is that coverage depends on manual curation and datasets without permissive licenses remain excluded.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a R package provide standardized access to open individual participant data using heterogeneous public repositories for evidence synthesis? WorldIPD implements a provenance-first architecture with a CSV registry, it uses standardized patient-level schemas requiring patient and study identifiers, and automated fetchers for Zenodo, GitHub, NHANES, sources. The package has three core functions for listing registered datasets, loading validated frames, and running schema checks ensuring completeness and identifier integrity. The current registry catalogues 37 of 37 datasets (100 percent concordance) spanning public health, clinical trials, and survey data, each entry records source URL, license, citation, and access mode for reproducibility. Leave-one-out validation confirmed zero integrity failures across all registered datasets; fetchers successfully retrieved remote resources from five distinct repository platforms. A standardized IPD hub then enables reproducible multi-source evidence synthesis by eliminating ad-hoc data wrangling across disparate repositories. The limitation of registry-based discovery is that coverage depends on manual curation.
<!-- END-REWRITE -->

_Line range 12395-12469 in rewrite-workbook.txt_

---

## Entry 165 ([169/921]) — WorldIPD-private

<details><summary>Metadata</summary>

```
TITLE: WorldIPD-Private: Secure Scaffold for Non-Redistributable Individual Participant Data
TYPE: methods  |  ESTIMAND: Schema compliance rate
DATA: Non-redistributable IPD datasets (private access only)
PATH: C:\Projects\WorldIPD-private
```

</details>

### Original (frozen — do not edit)

```
Can a companion private repository extend an open IPD framework to handle non-redistributable datasets while preserving full schema compatibility? WorldIPD-private mirrors the WorldIPD architecture using identical CSV registry format, patient-level schema conventions, and validation functions but restricts all datasets to private access with no redistribution under license constraints. The scaffold stores datasets in a standard directory with registry entries tagged as private, enabling transparent resolution through an environment variable pointing to the local path. Schema compliance testing confirmed all private datasets pass the same validation rules applied to the open collection, achieving 100 percent structural concordance across repositories. Cross-loading experiments verified that analytic pipelines written against the WorldIPD API function identically when redirected to the private repository. A dual-repository architecture cleanly separates data governance from analytic code while maintaining full schema interoperability between open and restricted collections. The limitation of local-only storage is that collaborative access requires secure file sharing infrastructure not provided by the package.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Should a private repository extend an open IPD framework to handle non-redistributable datasets while preserving full schema compatibility? WorldIPD-private mirrors the WorldIPD architecture but uses identical CSV registry format, patient-level schema conventions, and validation functions. It restricts all datasets to private access with no redistribution under license constraints, the scaffold stores datasets in a standard directory with registry entries tagged as private. It enables transparent resolution through an environment variable pointing to the local path. Schema compliance testing confirmed all private datasets pass the same validation rules applied to the open collection, it achieved 100 percent structural concordance across repositories. Cross-loading experiments verified that analytic pipelines written against the WorldIPD API can function identically when redirected to the private repository. This dual-repository architecture cleanly separates data governance from analytic code The limitation of local-only storage is that collaborative access requires secure file sharing infrastructure.
<!-- END-REWRITE -->

_Line range 12470-12544 in rewrite-workbook.txt_

---

## Entry 166 ([170/921]) — 3dvitreous-grapher

<details><summary>Metadata</summary>

```
TITLE: 3D Vitreous Grapher: Interactive Three-Dimensional Visualization of Ophthalmic Surgical Anatomy
TYPE: methods  |  ESTIMAND: Rendering accuracy and anatomical fidelity
DATA: Ophthalmic anatomical models, vitreous chamber geometry parameters
PATH: C:\Projects\3dvitreous-grapher
```

</details>

### Original (frozen — do not edit)

```
Can interactive three-dimensional visualization of vitreous chamber anatomy improve spatial understanding for ophthalmic surgical planning and education? We developed a 3,474-line browser-based application rendering the vitreous chamber, retina, lens, and surrounding structures using WebGL-based three-dimensional graphics with real-time rotation, zoom, and cross-sectional viewing. The tool implements parametric anatomical models allowing users to adjust chamber dimensions, pathology overlays, and surgical instrument trajectories within the rendered scene. Rendered anatomical proportions matched published ophthalmic measurements within 2 percent across all standard vitreous dimensions including axial length, equatorial diameter, and retinal surface area. Interactive cross-sectional views enabled visualization of posterior vitreous detachment, macular hole geometry, and epiretinal membrane configuration from arbitrary viewing angles. Three-dimensional spatial understanding of vitreous anatomy could enhance surgical planning for vitreoretinal procedures where two-dimensional imaging provides incomplete spatial context. The tool uses simplified geometric models and does not incorporate patient-specific imaging data or intraoperative optical coherence tomography integration.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can interactive three-dimensional visualization of vitreous chamber anatomy improve spatial understanding for ophthalmic surgical planning? We developed a 3,474-line browser-based application rendering the vitreous chamber, retina, lens, and surrounding structures using WebGL three-dimensional graphics with real-time rotation and cross-sectional viewing. The tool implements parametric anatomical models allowing users to adjust chamber dimensions, pathology overlays, and surgical instrument trajectories within the rendered scene. Rendered anatomical proportions matched published ophthalmic measurements within 2 percent across all standard vitreous dimensions including axial length and equatorial diameter. Interactive cross-sectional views enabled visualization of posterior vitreous detachment, macular hole geometry, and epiretinal membrane configuration from arbitrary viewing angles. Three-dimensional spatial understanding of vitreous anatomy could enhance surgical planning for vitreoretinal procedures where two-dimensional imaging provides incomplete context. The tool uses simplified geometric models and does not incorporate patient-specific imaging data or intraoperative optical coherence tomography.
<!-- END-REWRITE -->

_Line range 12545-12620 in rewrite-workbook.txt_

---

## Entry 167 ([172/921]) — area1_small_sample_analysis

<details><summary>Metadata</summary>

```
TITLE: Small-Sample Meta-Analysis Methods: Characterization and Performance Under k < 100
TYPE: methods  |  ESTIMAND: Coverage probability and type I error rate
DATA: Simulation datasets with k = 2 to 100 studies; repo100 benchmark collection
PATH: C:\Projects\area1_small_sample_analysis
```

</details>

### Original (frozen — do not edit)

```
How do standard random-effects meta-analysis methods perform when the number of included studies is small, and which estimators maintain nominal coverage under sparse conditions? We characterized small-sample behaviour across DerSimonian-Laird, REML, Paule-Mandel, and Hartung-Knapp-Sidik-Jonkman methods using simulation experiments with k ranging from 2 to 100 studies drawn from the repo100 benchmark collection. The analysis computed coverage probability, type I error rate, mean squared error of the pooled estimate, and heterogeneity estimator bias across 10,000 replications per configuration. DerSimonian-Laird coverage dropped below 90 percent when k was below 10, while Hartung-Knapp maintained 94.2 percent coverage (95% CI 93.8 to 94.6) across all small-sample configurations. REML and Paule-Mandel showed intermediate performance with coverage recovering to nominal levels around k equals 15 for moderate heterogeneity scenarios. These results quantify the known small-sample penalty and support Hartung-Knapp as the default for meta-analyses with fewer than 15 studies. The analysis was limited to normal-normal models and did not assess binary outcome methods or exact small-sample approaches.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How do standard random-effects meta-analysis methods perform when the number of included studies is small? We characterized small-sample behaviour across DerSimonian-Laird, REML, Paule-Mandel, and Hartung-Knapp-Sidik-Jonkman methods using simulation experiments with k from 2 to 100 studies drawn from the repo100 benchmark collection. The analysis computed coverage probability, type I error rate, mean squared error, and heterogeneity estimator bias across 10,000 replications per configuration. DerSimonian-Laird coverage dropped below 90 percent when k was below 10, while Hartung-Knapp maintained 94.2 percent coverage (95% CI 93.8 to 94.6) across all small-sample configurations. REML and Paule-Mandel showed intermediate performance with coverage recovering to nominal levels around k equals 15 for moderate heterogeneity. These results quantify the known small-sample penalty and support Hartung-Knapp as the default for meta-analyses with fewer than 15 studies. The analysis was limited to normal-normal models and did not assess binary outcome methods.
<!-- END-REWRITE -->

_Line range 12621-12696 in rewrite-workbook.txt_

---

## Entry 168 ([173/921]) — asreview_5star

<details><summary>Metadata</summary>

```
TITLE: ASReview 5-Star: Enhanced Systematic Review Screening with Stopping Rules, IRR, and Meta-Analysis Integration
TYPE: methods  |  ESTIMAND: Screening recall and work saved over sampling
DATA: Systematic review reference datasets with relevance labels
PATH: C:\Projects\asreview_5star
```

</details>

### Original (frozen — do not edit)

```
Can machine-learning-assisted screening tools be extended with stopping rules, inter-rater reliability metrics, and integrated meta-analysis to create a complete systematic review workflow? We enhanced the ASReview active learning framework with five additional capabilities: evidence-based stopping rules, Cohen kappa inter-rater reliability calculation, PRISMA-compliant flow diagram generation, integrated random-effects meta-analysis, and structured data extraction templates. The enhanced platform applies active learning with support vector machine classifiers to prioritize likely relevant records while monitoring screening saturation through cumulative recall curves and stopping criteria. Across three benchmark datasets the system achieved 95 percent recall while screening only 23 percent of records (95% CI 19 to 27), with stopping rules correctly identifying the saturation point within 2 percentage points of complete recall. Inter-rater reliability monitoring flagged disagreement patterns before they could propagate into extraction inconsistencies. A unified screening-to-synthesis platform could reduce the technical overhead of switching between specialized tools at each review stage. The stopping rules assume stationary relevance distributions and may underperform when relevant records cluster late in the screening queue.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can machine-learning-assisted screening be extended with stopping rules, inter-rater reliability, and integrated meta-analysis for a complete systematic review workflow? We enhanced the ASReview active learning framework with five capabilities: evidence-based stopping rules, Cohen kappa inter-rater reliability, PRISMA flow diagram generation, integrated random-effects meta-analysis, and structured data extraction templates. The platform applies active learning with support vector machine classifiers to prioritize likely relevant records while monitoring screening saturation through cumulative recall curves. Across three benchmark datasets the system achieved 95 percent recall while screening only 23 percent of records (95% CI 19 to 27), with stopping rules correctly identifying the saturation point within 2 percentage points of complete recall. Inter-rater reliability monitoring flagged disagreement patterns before they could propagate into extraction inconsistencies. A unified screening-to-synthesis platform could reduce technical overhead of switching between specialized tools at each review stage. The stopping rules assume stationary relevance distributions and may underperform when relevant records cluster late in the screening queue.
<!-- END-REWRITE -->

_Line range 12697-12772 in rewrite-workbook.txt_

---

## Entry 169 ([174/921]) — AsSirat

<details><summary>Metadata</summary>

```
TITLE: As-Sirat: The Evidence Passport for Navigating Meta-Analytic Uncertainty
TYPE: methods  |  ESTIMAND: Evidence navigation score
DATA: Meta-analytic results with heterogeneity, bias, and certainty metrics
PATH: C:\Models\AsSirat
```

</details>

### Original (frozen — do not edit)

```
Can a structured evidence passport distil the complex landscape of meta-analytic uncertainty into an actionable navigation aid for clinical decision-makers? We developed As-Sirat as a 638-line browser application that assembles heterogeneity metrics, publication bias indicators, certainty of evidence ratings, and fragility indices into a unified evidence passport with traffic-light signalling. The tool ingests pooled estimates with confidence intervals, I-squared, tau-squared, Egger test results, GRADE ratings, and fragility index to generate a composite navigation profile across four uncertainty domains. Each domain receives a classification of green, amber, or red based on validated thresholds, with an overall evidence passport score computed as the weighted mean of domain ratings. Sensitivity analysis confirmed that domain classifications changed monotonically with input parameters and no paradoxical upgrades occurred across plausible ranges. Structured uncertainty navigation could help clinicians quickly assess whether a meta-analytic conclusion is robust enough to inform practice changes. The tool depends on pre-computed meta-analytic inputs and cannot perform primary pooling or assess study-level risk of bias.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a structured evidence passport distil meta-analytic uncertainty into an actionable navigation aid for clinical decision-makers? We developed As-Sirat as a 638-line browser application assembling heterogeneity metrics, publication bias indicators, certainty ratings, and fragility indices into a unified evidence passport with traffic-light signalling. The tool ingests pooled estimates with confidence intervals, I-squared, tau-squared, Egger test results, GRADE ratings, and fragility index to generate a composite navigation profile across four uncertainty domains. Each domain receives a classification of green, amber, or red based on validated thresholds; the overall evidence passport score is computed as the weighted mean of domain ratings. Sensitivity analysis confirmed that domain classifications changed monotonically with input parameters and no paradoxical upgrades occurred across plausible ranges. Structured uncertainty navigation could help clinicians quickly assess whether a meta-analytic conclusion supports practice changes. The tool depends on pre-computed meta-analytic inputs and cannot perform primary pooling or study-level risk of bias assessment.
<!-- END-REWRITE -->

_Line range 12773-12849 in rewrite-workbook.txt_

---

## Entry 170 ([175/921]) — cardio-ctgov-living-meta-portfolio

<details><summary>Metadata</summary>

```
TITLE: Cardio CT.gov Living Meta Portfolio: Automated Generation of 27 Topic-Specific Cardiovascular Evidence Reviews
TYPE: methods  |  ESTIMAND: documentation proportion
DATA: Repository inventory with 55 source files, 0 test files, 2 documents, and 55 assets.
PATH: C:\Projects\cardio-ctgov-living-meta-portfolio
```

</details>

### Original (frozen — do not edit)

```
Can a portfolio generator automatically produce validated topic-specific living meta-analysis applications for cardiovascular evidence from ClinicalTrials.gov registry data? We developed a pipeline that scans cardiovascular trial topics, generates individual review applications with PICO frameworks, and validates each against the shared ESC living meta-analysis engine. The generator emits project folders containing analysis configurations, reviewer panels with benchmark sections, topic-aware WebR validation links, and structured validation manifests for 27 cardiovascular topics. All 27 generated topic applications passed browser-level smoke validation with structural integrity checks confirming consistent metadata, analysis configuration, and reviewer panel completeness across the portfolio. Topic-aware validation ensures each generated application correctly inherits the shared synthesis engine including GRADE assessment with observed-denominator handling rather than placeholder sample sizes. Automated portfolio generation from registry data could accelerate the creation of living evidence surveillance systems across therapeutic areas. The pipeline depends on ClinicalTrials.gov metadata quality and cannot generate applications for topics lacking sufficient registered trial data.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a portfolio generator automatically produce validated topic-specific living meta-analysis applications for cardiovascular evidence from ClinicalTrials.gov? We developed a pipeline that scans cardiovascular trial topics and generates individual review applications with PICO frameworks, validating each against the shared ESC living meta-analysis engine. The generator emits project folders containing analysis configurations, reviewer panels with benchmark sections, and topic-aware WebR validation links for 27 cardiovascular topics. All 27 generated topic applications passed browser-level smoke validation with structural integrity checks confirming consistent metadata and analysis configuration across the portfolio. Topic-aware validation ensures each generated application correctly inherits the shared synthesis engine including GRADE assessment with observed-denominator handling. Automated portfolio generation from registry data could accelerate the creation of living evidence surveillance systems across therapeutic areas. The pipeline depends on ClinicalTrials.gov metadata quality and cannot generate applications for topics lacking sufficient registered trial data.
<!-- END-REWRITE -->

_Line range 12850-12924 in rewrite-workbook.txt_

---

## Entry 171 ([176/921]) — cbamm-project2

<details><summary>Metadata</summary>

```
TITLE: CBAMM Phase 2: Cochrane Bias-Adjusted Meta-Model Development
TYPE: methods  |  ESTIMAND: Bias-adjusted pooled effect estimate
DATA: Cochrane systematic review datasets with risk-of-bias assessments
PATH: C:\Projects\cbamm-project2
```

</details>

### Original (frozen — do not edit)

```
Can bias-adjusted meta-models correct pooled estimates when individual studies carry differential risk-of-bias ratings within Cochrane systematic reviews? We extended the CBAMM framework to incorporate study-level risk-of-bias weights derived from Cochrane domain assessments into random-effects pooling, implementing both multiplicative bias adjustment and selection model approaches. The phase two model applies domain-specific bias functions calibrated against empirical bias distributions from the BRANDO dataset to down-weight high-risk studies while preserving the contribution of low-risk evidence. Across validation scenarios the bias-adjusted pooled estimate shifted by a median of 0.08 standard deviations (95% CI 0.03 to 0.14) toward the null compared with unadjusted random-effects pooling. The direction of adjustment was consistent with known empirical bias patterns where inadequate allocation concealment and unblinded outcome assessment inflate treatment effects. Systematic bias adjustment within pooling could improve the accuracy of meta-analytic conclusions when included studies span heterogeneous risk-of-bias profiles. The approach requires reliable domain-level risk-of-bias assessments and the calibration dataset may not generalize across all clinical domains.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can bias-adjusted meta-models correct pooled estimates when individual studies carry differential risk-of-bias ratings within Cochrane reviews? We extended the CBAMM framework to incorporate study-level risk-of-bias weights from Cochrane domain assessments into random-effects pooling with multiplicative bias adjustment and selection model approaches. The model applies domain-specific bias functions calibrated against empirical distributions from the BRANDO dataset to down-weight high-risk studies while preserving low-risk evidence contribution. Across validation scenarios the bias-adjusted pooled estimate shifted by a median of 0.08 standard deviations (95% CI 0.03 to 0.14) toward the null compared with unadjusted random-effects pooling. The direction of adjustment was consistent with known empirical bias patterns where inadequate allocation concealment and unblinded assessment inflate treatment effects. Systematic bias adjustment within pooling could improve meta-analytic conclusions when included studies span heterogeneous risk-of-bias profiles. The approach requires reliable domain-level assessments and the calibration dataset may not generalize across all clinical domains.
<!-- END-REWRITE -->

_Line range 12925-13000 in rewrite-workbook.txt_

---

## Entry 172 ([177/921]) — childnajia

<details><summary>Metadata</summary>

```
TITLE: HIDAYAH: A Clinical Danger Detection Engine for Paediatric Emergency Triage
TYPE: clinical  |  ESTIMAND: Triage sensitivity and specificity
DATA: WHO IMCI danger signs, paediatric vital sign reference ranges by age group
PATH: C:\Projects\childnajia
```

</details>

### Original (frozen — do not edit)

```
Can an automated clinical danger detection engine provide reliable emergency triage for paediatric presentations in resource-limited settings using WHO Integrated Management of Childhood Illness criteria? We developed HIDAYAH as a 1,601-line browser application implementing age-stratified vital sign assessment, WHO danger sign detection, dehydration scoring, nutritional status classification, and composite severity grading for children from birth to fourteen years. The engine applies age-specific reference ranges for heart rate, respiratory rate, temperature, and oxygen saturation alongside clinical sign algorithms to generate real-time triage classifications of stable, caution, or danger. Using published WHO IMCI validation data the danger sign detection achieved sensitivity of 96 percent (95% CI 92 to 98) and specificity of 89 percent (95% CI 85 to 93) for identifying children requiring immediate medical intervention. All assessment algorithms were validated against WHO IMCI clinical guidelines with complete traceability from input parameters to triage classification. Automated paediatric triage could support frontline health workers in facilities where specialist paediatric assessment is unavailable. The tool cannot replace clinical examination and does not account for rare presentations outside standard WHO danger sign categories.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can an automated clinical danger detection engine provide reliable emergency triage for paediatric presentations using WHO IMCI criteria? We developed HIDAYAH as a 1,601-line browser application implementing age-stratified vital sign assessment, WHO danger sign detection, dehydration scoring, nutritional status classification, and composite severity grading for children from birth to fourteen years. The engine applies age-specific reference ranges for heart rate, respiratory rate, temperature, and oxygen saturation alongside clinical sign algorithms to generate real-time triage classifications. Using published WHO IMCI validation data the danger sign detection achieved sensitivity of 96 percent (95% CI 92 to 98) and specificity of 89 percent (95% CI 85 to 93) for identifying children requiring immediate intervention. All assessment algorithms were validated against WHO IMCI clinical guidelines with complete traceability from input parameters to triage classification. Automated paediatric triage could support frontline health workers in facilities where specialist assessment is unavailable. The tool cannot replace clinical examination and does not account for rare presentations outside standard danger sign categories.
<!-- END-REWRITE -->

_Line range 13001-13076 in rewrite-workbook.txt_

---

## Entry 173 ([178/921]) — CINeMA

<details><summary>Metadata</summary>

```
TITLE: CINeMA: Browser-Based Confidence in Network Meta-Analysis Across Six Domains
TYPE: methods  |  ESTIMAND: NMA confidence rating (Very Low to High)
DATA: Network meta-analysis contrast data with risk-of-bias and study-level metadata
PATH: C:\Models\CINeMA
```

</details>

### Original (frozen — do not edit)

```
Can the CINeMA framework for rating confidence in network meta-analysis results be implemented as a fully interactive browser tool without requiring R or Stata? We built a 1,670-line single-file application implementing all six CINeMA domains: within-study bias, reporting bias, indirectness, imprecision, heterogeneity, and incoherence, each generating domain-level judgments that combine into an overall confidence rating. The tool accepts contrast-level network data and computes contribution matrices, node-splitting incoherence tests, heterogeneity statistics, and optimal information size thresholds for each pairwise comparison. Domain judgments follow published CINeMA decision rules mapping quantitative metrics to no concern, some concern, or major concern classifications. Overall confidence ratings ranged from very low to high across test networks, with domain-level contributions traceable through interactive visualisation of the contribution matrix. Browser-based CINeMA assessment could lower the barrier to transparent confidence evaluation in network meta-analysis for review teams without statistical software expertise. The tool implements the published CINeMA algorithm and cannot accommodate unpublished extensions or custom domain weighting schemes.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can the CINeMA framework for rating confidence in network meta-analysis be implemented as a fully interactive browser tool without R or Stata? We built a 1,670-line application implementing all six CINeMA domains: within-study bias, reporting bias, indirectness, imprecision, heterogeneity, and incoherence, each generating domain-level judgments that combine into an overall confidence rating. The tool accepts contrast-level network data and computes contribution matrices, node-splitting incoherence tests, heterogeneity statistics, and optimal information size thresholds for each comparison. Domain judgments follow published CINeMA decision rules mapping quantitative metrics to no concern, some concern, or major concern classifications. Overall confidence ratings ranged from very low to high across test networks, with domain-level contributions traceable through interactive contribution matrix visualisation. Browser-based CINeMA assessment could lower the barrier to transparent confidence evaluation in network meta-analysis. The tool implements the published CINeMA algorithm and cannot accommodate unpublished extensions or custom domain weighting schemes.
<!-- END-REWRITE -->

_Line range 13077-13153 in rewrite-workbook.txt_

---

## Entry 174 ([179/921]) — claude-rct-work

<details><summary>Metadata</summary>

```
TITLE: Claude-RCT-Work: LLM-Assisted Randomised Controlled Trial Data Extraction Workflow
TYPE: methods  |  ESTIMAND: Extraction accuracy and concordance with manual extraction
DATA: Published RCT manuscripts for data extraction benchmarking
PATH: C:\Projects\claude-rct-work
```

</details>

### Original (frozen — do not edit)

```
Can large language model assisted workflows extract structured data from randomised controlled trial publications with accuracy comparable to manual human extraction? We developed a pipeline using Claude for extracting study characteristics, treatment arms, primary and secondary outcomes, hazard ratios, confidence intervals, and adverse event rates from published RCT manuscripts. The workflow applies structured prompting with field-level validation, cross-checking of extracted values against reported tables, and flagging of discrepancies between abstract and full-text reported results. Across a benchmark set of cardiovascular trial publications the automated pipeline achieved 94 percent field-level concordance (95% CI 91 to 96) with manual extraction by two independent reviewers. Discordance was concentrated in composite endpoint decomposition and subgroup analysis extraction where human reviewers also showed lower inter-rater agreement. LLM-assisted extraction could substantially reduce the time burden of systematic review data collection while maintaining accuracy at levels comparable to trained human reviewers. The pipeline requires final human verification and cannot reliably extract data from supplementary appendices or figures without optical character recognition integration.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can large language model workflows extract structured data from randomised controlled trial publications with accuracy comparable to manual extraction? We developed a pipeline using Claude for extracting study characteristics, treatment arms, outcomes, hazard ratios, confidence intervals, and adverse event rates from published RCT manuscripts. The workflow applies structured prompting with field-level validation, cross-checking against reported tables, and flagging of discrepancies between abstract and full-text results. Across cardiovascular trial publications the automated pipeline achieved 94 percent field-level concordance (95% CI 91 to 96) with manual extraction by two independent reviewers. Discordance was concentrated in composite endpoint decomposition and subgroup analysis extraction where human reviewers also showed lower inter-rater agreement. LLM-assisted extraction could reduce the time burden of systematic review data collection while maintaining accuracy comparable to trained reviewers. The pipeline requires final human verification and cannot reliably extract data from supplementary appendices or figures without OCR integration.
<!-- END-REWRITE -->

_Line range 13154-13229 in rewrite-workbook.txt_

---

## Entry 175 ([180/921]) — ctgov-actual-discipline-repeaters

<details><summary>Metadata</summary>

```
TITLE: CT.gov Actual-Discipline Repeaters
TYPE: methods  |  ESTIMAND: Any actual-field gap stock and rate among named lead sponsors with at least 100 older studies
DATA: 249,507 eligible older closed interventional studies with actual-field discipline fields derived from missing actual completion and actual enrollment markers
PATH: C:\Projects\ctgov-analyses/ctgov-actual-discipline-repeaters
```

</details>

### Original (frozen — do not edit)

```
Which named sponsors fail the CT.gov actual-field discipline test on missing actual completion and actual enrollment fields? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. We ranked named sponsors with at least 100 older studies by any actual-field gap, then compared rate outliers, sponsor-class rates, and counts across actual completion and actual enrollment fields. Boehringer Ingelheim carried the largest actual-discipline stock at 943 studies, followed by NCI at 615 and Novartis Pharmaceuticals at 292. Gynecologic Oncology Group had the sharpest large-sponsor actual-discipline rate at 83.8 percent, while NIH and NETWORK were highest among sponsor classes at 24.5 and 23.4 percent. The actual-field problem is not cosmetic because it obscures whether closed studies reported real completion timing and realized sample size with the discipline expected from mature trial records. These counts reflect missing registry fields among older closed studies and do not by themselves establish rule violations or intentional concealment.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which named sponsors fail the CT.gov actual-field discipline test on missing actual completion and actual enrollment fields? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. We ranked named sponsors with at least 100 older studies by any actual-field gap, then compared rate outliers, sponsor-class rates, and counts across actual completion and actual enrollment fields. Boehringer Ingelheim carried the largest actual-discipline stock at 943 studies, followed by NCI at 615 and Novartis Pharmaceuticals at 292. Gynecologic Oncology Group had the sharpest large-sponsor actual-discipline rate at 83.8 percent, while NIH and NETWORK were highest among sponsor classes at 24.5 and 23.4 percent. The actual-field problem is not cosmetic because it obscures whether closed studies reported real completion timing and realized sample size with the discipline expected from mature trial records. These counts reflect missing registry fields among older closed studies and do not by themselves establish rule violations or intentional concealment.
<!-- END-REWRITE -->

_Line range 13230-13304 in rewrite-workbook.txt_

---

## Entry 176 ([181/921]) — ctgov-actual-field-discipline

<details><summary>Metadata</summary>

```
TITLE: CT.gov Actual-Field Discipline
TYPE: methods  |  ESTIMAND: 2-year no-results rate across actual-field discipline groups among eligible older CT.gov studies
DATA: 249,507 eligible older closed interventional studies grouped by actual date/count discipline flags
PATH: C:\Projects\ctgov-analyses/ctgov-actual-field-discipline
```

</details>

### Original (frozen — do not edit)

```
How much hiddenness is concentrated in closed CT.gov studies that still fail to use actual completion or enrollment fields? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and tracked three closed-study actual-field indicators. The project compares two-year no-results rates, ghost-protocol rates, and status-specific missing-actual patterns across primary-completion, completion, and enrollment discipline. Missing actual enrollment corresponds to a 100.0 percent no-results rate and a 62.8 percent ghost-protocol rate. Missing actual primary completion reaches 100.0 percent no results, missing actual completion 95.3 percent, and suspended studies are worst on actual-field discipline. Closed-study actual-field discipline therefore functions as a direct structural warning sign for opacity rather than a minor metadata defect. The separation remains visible across all three fields and links directly to the stopped-study audit as well inside older registry cohorts. Actual-field flags come from registry status and date/count types, not from external audits of what sponsors truly knew or when.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How much hiddenness is concentrated in closed CT.gov studies that still fail to use actual completion or enrollment fields? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and tracked three closed-study actual-field indicators. The project compares two-year no-results rates, ghost-protocol rates, and status-specific missing-actual patterns across primary-completion, completion, and enrollment discipline; missing actual enrollment corresponds to a 100.0 percent no-results rate and a 62.8 percent ghost-protocol rate. Missing actual primary completion reaches 100.0 percent no results, missing actual completion 95.3 percent, and suspended studies are worst on actual-field discipline. Closed-study actual-field discipline therefore functions as a direct structural warning sign for opacity rather than a minor metadata defect. The separation remains visible across all three fields and links directly to the stopped-study audit as well inside older registry cohorts. Actual-field flags come from registry status and date/count types, not from external audits of what sponsors truly knew or when.
<!-- END-REWRITE -->

_Line range 13305-13379 in rewrite-workbook.txt_

---

## Entry 177 ([182/921]) — ctgov-black-box-sponsor-repeaters

<details><summary>Metadata</summary>

```
TITLE: CT.gov Black-Box Sponsor Repeaters
TYPE: methods  |  ESTIMAND: Black-box stock and rate among named lead sponsors in the older-study CT.gov universe
DATA: 249,507 eligible older closed interventional studies with named-sponsor black-box watchlists derived from the wave-nine sponsor table
PATH: C:\Projects\ctgov-analyses/ctgov-black-box-sponsor-repeaters
```

</details>

### Original (frozen — do not edit)

```
Which named sponsors dominate the CT.gov black-box subset where older studies have no results, no linked paper, and no detailed description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. Using the wave-nine sponsor watchlist, we ranked named sponsors by black-box stock and black-box rate, then compared that table with no-results and ghost counts. Boehringer Ingelheim carried the largest named black-box stock at 755 studies, followed by GlaxoSmithKline at 579 and Pfizer at 539. Bayer was the sharper large-sponsor outlier on rate at 48.1 percent, while several top black-box repeaters were industry portfolios with hundreds of missing-results studies. The named black-box table therefore makes the industry deep-silence problem much more visible than the broader sponsor stock tables do, especially across major drug-company portfolios overall. Black-box status is a registry-page visibility definition and should not be read as proof that a sponsor produced no documentation or dissemination outside linked CT.gov fields.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which named sponsors dominate the CT.gov black-box subset where older studies have no results, no linked paper, and no detailed description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. Using the wave-nine sponsor watchlist, we ranked named sponsors by black-box stock and black-box rate, then compared that table with no-results and ghost counts. Boehringer Ingelheim carried the largest named black-box stock at 755 studies, followed by GlaxoSmithKline at 579 and Pfizer at 539. Bayer was the sharper large-sponsor outlier on rate at 48.1 percent, while several top black-box repeaters were industry portfolios with hundreds of missing-results studies. The named black-box table therefore makes the industry deep-silence problem much more visible than the broader sponsor stock tables do, especially across major drug-company portfolios overall. Black-box status is a registry-page visibility definition and should not be read as proof that a sponsor produced no documentation or dissemination outside linked CT.gov fields.
<!-- END-REWRITE -->

_Line range 13380-13454 in rewrite-workbook.txt_

---

## Entry 178 ([183/921]) — ctgov-black-box-trials

<details><summary>Metadata</summary>

```
TITLE: CT.gov Black-Box Trials
TYPE: methods  |  ESTIMAND: Black-box trial stock and rate among eligible older CT.gov studies
DATA: 249,507 eligible older closed interventional studies with a black-box definition based on results, publication-link, and detailed-description silence
PATH: C:\Projects\ctgov-analyses/ctgov-black-box-trials
```

</details>

### Original (frozen — do not edit)

```
What appears when hiddenness is narrowed to black-box trials with no results, no linked publication, and no detailed description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. We defined a black-box trial as one with a two-year results gap, no linked publication reference, and no detailed description, then ranked sponsor classes, countries, and condition families. OTHER held the largest black-box stock at 21,375 studies, while INDUSTRY carried the highest large-class black-box rate at 23.4 percent. The United States still held 12,183 black-box studies on absolute stock, but healthy-volunteer portfolios were the sharpest condition-family extreme at 33.9 percent. The black-box view isolates a stricter silence state where industrial portfolios rate worse, while heterogeneous public and academic portfolios still dominate on count across the registry overall. Black-box status is a registry-visibility definition only and does not imply a study lacked internal documentation, external dissemination, or undiscovered reporting outside linked registry fields.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
What appears when hiddenness is narrowed to black-box trials with no results, no linked publication, and no detailed description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. We defined a black-box trial as one with a two-year results gap, no linked publication reference, and no detailed description, then ranked sponsor classes, countries, and condition families. OTHER held the largest black-box stock at 21,375 studies, while INDUSTRY carried the highest large-class black-box rate at 23.4 percent. The United States still held 12,183 black-box studies on absolute stock, but healthy-volunteer portfolios were the sharpest condition-family extreme at 33.9 percent. The black-box view isolates a stricter silence state where industrial portfolios rate worse, while heterogeneous public and academic portfolios still dominate on count across the registry overall. Black-box status is a registry-visibility definition only and does not imply a study lacked internal documentation, external dissemination, or undiscovered reporting outside linked registry fields.
<!-- END-REWRITE -->

_Line range 13455-13529 in rewrite-workbook.txt_

---

## Entry 179 ([184/921]) — ctgov-completion-delay-debt

<details><summary>Metadata</summary>

```
TITLE: CT.gov Completion-Delay Debt
TYPE: methods  |  ESTIMAND: 2-year no-results rate across registration-to-completion delay buckets among eligible older CT.gov studies
DATA: 249,507 eligible older closed interventional studies grouped by submission-to-completion delay
PATH: C:\Projects\ctgov-analyses/ctgov-completion-delay-debt
```

</details>

### Original (frozen — do not edit)

```
Does ClinicalTrials.gov hiddenness fall as trials take longer from first submission to completion, or do short-cycle studies report just as well? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and calculated submission-to-completion delay buckets. The project compares two-year no-results rates, ghost-protocol rates, full visibility, and purpose-specific contrasts across registration-to-completion intervals. Studies completed in the same calendar year they were first submitted showed an 85.7 percent no-results rate and a 54.1 percent ghost-protocol rate. Studies with a 6 to 10 year delay fell to 57.6 percent no results and 28.8 percent ghost protocols, with long-lag treatment studies also looking substantially cleaner. Fast-cycle studies therefore look most hidden, suggesting short operational timelines are not translating into faster public reporting. The contrast remains visible across treatment studies and other major purpose groups. Submission-to-completion lag is a registry proxy for operational duration and can reflect backfilled dates, protocol amendments, or changing trial mix.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Does ClinicalTrials.gov hiddenness fall as trials take longer from first submission to completion, or do short-cycle studies report just as well? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and calculated submission-to-completion delay buckets. The project compares two-year no-results rates, ghost-protocol rates, full visibility, and purpose-specific contrasts across registration-to-completion intervals. Studies completed in the same calendar year they were first submitted showed an 85.7 percent no-results rate and a 54.1 percent ghost-protocol rate. Studies with a 6 to 10 year delay fell to 57.6 percent no results and 28.8 percent ghost protocols, with long-lag treatment studies also looking substantially cleaner. Fast-cycle studies therefore look most hidden, suggesting short operational timelines are not translating into faster public reporting, the contrast remains visible across treatment studies and other major purpose groups. Submission-to-completion lag is a registry proxy for operational duration and can reflect backfilled dates, protocol amendments, or changing trial mix.
<!-- END-REWRITE -->

_Line range 13530-13604 in rewrite-workbook.txt_

---

## Entry 180 ([185/921]) — ctgov-completion-timing-repeaters

<details><summary>Metadata</summary>

```
TITLE: CT.gov Completion-Timing Repeaters
TYPE: methods  |  ESTIMAND: Completion-timing gap stock among older studies missing actual primary completion or actual completion fields
DATA: 249,507 eligible older closed interventional studies with completion-timing sponsor, component, and class summaries
PATH: C:\Projects\ctgov-analyses/ctgov-completion-timing-repeaters
```

</details>

### Original (frozen — do not edit)

```
Which named sponsors most often leave older CT.gov study pages without actual primary completion or actual completion timing fields? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. We defined a completion-timing gap as missing actual primary completion or missing actual completion among older closed studies, then ranked sponsors with at least 100 studies. Boehringer Ingelheim led the named-sponsor table at 930 studies, followed by National Cancer Institute at 601, Novartis Pharmaceuticals at 271, and EORTC at 166. Gynecologic Oncology Group had the highest large-sponsor completion-timing gap rate at 83.1 percent, while NETWORK reached 19.2 percent and NIH 17.2 percent as sponsor classes. Completion-timing gaps obscure when older studies truly finished, making the reporting window harder to read even before results, publications, or outcome text are evaluated. These counts reflect missing registry timing fields among older closed studies and do not by themselves establish concealment, intent, or legal breach alone.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which named sponsors most often leave older CT.gov study pages without actual primary completion or actual completion timing fields? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot. We defined a completion-timing gap as missing actual primary completion or missing actual completion among older closed studies, then ranked sponsors with at least 100 studies. Boehringer Ingelheim led the named-sponsor table at 930 studies, followed by National Cancer Institute at 601, Novartis Pharmaceuticals at 271, and EORTC at 166. Gynecologic Oncology Group had the highest large-sponsor completion-timing gap rate at 83.1 percent, while NETWORK reached 19.2 percent and NIH 17.2 percent as sponsor classes. Completion-timing gaps obscure when older studies truly finished, making the reporting window harder to read even before results, publications, or outcome text are evaluated. These counts reflect missing registry timing fields among older closed studies and do not by themselves establish concealment, intent, or legal breach alone.
<!-- END-REWRITE -->

_Line range 13605-13679 in rewrite-workbook.txt_

---

## Entry 181 ([186/921]) — ctgov-condition-ancient-backlog

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Ancient Backlog
TYPE: methods  |  ESTIMAND: Ancient-backlog stock among older closed interventional studies unresolved at least ten overdue years beyond the two-year mark
DATA: 249,507 eligible older closed interventional studies with ancient-backlog stock, rate, and overdue-years summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-ancient-backlog
```

</details>

### Original (frozen — do not edit)

```
Which condition families still hold the largest stock of CT.gov studies unresolved at least ten overdue years beyond the two-year reporting mark? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined ancient backlog as older studies with no posted results and at least ten overdue years beyond the two-year mark, then ranked large condition families. Oncology led the named-family table at 11,369 studies, while the broad OTHER bucket held 10,899 and cardiovascular followed at 6,545. Metabolic remained high on stock at 4,693, while healthy volunteers reached the highest large-family ancient-backlog rate at 31.5 percent. Ancient backlog separates diffuse registry stock from large disease portfolios and shows that very old silence remains prominent in major therapeutic areas. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than fixed clinical ontologies or mutually exclusive diagnoses within the registry as presented here.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families still hold the largest stock of CT.gov studies unresolved at least ten overdue years beyond the two-year reporting mark? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined ancient backlog as older studies with no posted results and at least ten overdue years beyond the two-year mark, then ranked large condition families. Oncology led the named-family table at 11,369 studies, while the broad OTHER bucket held 10,899 and cardiovascular followed at 6,545. Metabolic remained high on stock at 4,693, while healthy volunteers reached the highest large-family ancient-backlog rate at 31.5 percent. Ancient backlog separates diffuse registry stock from large disease portfolios and shows that very old silence remains prominent in major therapeutic areas. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than fixed clinical ontologies or mutually exclusive diagnoses within the registry as presented here.
<!-- END-REWRITE -->

_Line range 13680-13754 in rewrite-workbook.txt_

---

## Entry 182 ([187/921]) — ctgov-condition-description-black-box

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Description Black-Box
TYPE: methods  |  ESTIMAND: Description black-box stock among older studies with no results, no linked publication, no detailed description, and no primary outcome description
DATA: 249,507 eligible older closed interventional studies with description-black-box stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-description-black-box
```

</details>

### Original (frozen — do not edit)

```
Which condition families carry the most older CT.gov studies that are overdue, unlinked, and missing both detailed description and primary outcome description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a description black-box study as one with a two-year results gap, no linked publication, no detailed description, and no primary outcome description, then ranked large condition families. The broad OTHER bucket led the stock table at 3,366 studies, followed by Oncology at 2,619, Healthy volunteers at 2,516, and Cardiovascular at 1,798. Healthy volunteers had the highest large-family description-black-box rate at 17.8 percent, far above renal and urology at 8.5 percent and metabolic at 8.3 percent. The condition-family black-box view mixes diffuse registry stock with a very sharp healthy-volunteer blackout pattern that is more severe than ordinary no-results counts alone. Condition families are keyword-derived registry groupings, not formal disease ontologies or diagnoses.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families carry the most older CT.gov studies that are overdue, unlinked, and missing both detailed description and primary outcome description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a description black-box study as one with a two-year results gap, no linked publication, no detailed description, and no primary outcome description, then ranked large condition families. The broad OTHER bucket led the stock table at 3,366 studies, followed by Oncology at 2,619, Healthy volunteers at 2,516, and Cardiovascular at 1,798. Healthy volunteers had the highest large-family description-black-box rate at 17.8 percent, far above renal and urology at 8.5 percent and metabolic at 8.3 percent. The condition-family black-box view mixes diffuse registry stock with a very sharp healthy-volunteer blackout pattern that is more severe than ordinary no-results counts alone. Condition families are keyword-derived registry groupings, not formal disease ontologies or diagnoses.
<!-- END-REWRITE -->

_Line range 13755-13829 in rewrite-workbook.txt_

---

## Entry 183 ([188/921]) — ctgov-condition-detailed-description-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Detailed-Description Gap
TYPE: methods  |  ESTIMAND: Detailed-description-gap stock among older studies missing the detailed description field
DATA: 249,507 eligible older closed interventional studies with detailed-description-gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-detailed-description-gap
```

</details>

### Original (frozen — do not edit)

```
Which condition families most often leave older CT.gov study pages without detailed descriptions, removing the broad narrative paragraph for readers? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a detailed-description gap as a missing detailed description field, then ranked large condition families by stock and rate. The broad OTHER bucket led the condition-family detailed-description-gap stock table at 18,641 studies, followed by Oncology at 12,321, Cardiovascular at 8,808, and Healthy volunteers at 7,082. Healthy volunteers had the highest large-family detailed-description-gap rate at 50.2 percent, ahead of Immunology and dermatology at 41.7 percent and Renal and urology at 38.3 percent. Condition-family detailed-description gaps show where the broad study narrative disappears most often in major therapeutic areas, not only fringe portfolios. Condition families are keyword-derived registry groupings, not formal disease ontologies or mutually exclusive diagnoses across all studies. They simplify diagnoses into public buckets.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families most often leave older CT.gov study pages without detailed descriptions, removing the broad narrative paragraph for readers? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a detailed-description gap as a missing detailed description field, then ranked large condition families by stock and rate. The broad OTHER bucket led the condition-family detailed-description-gap stock table at 18,641 studies, followed by Oncology at 12,321, Cardiovascular at 8,808, and Healthy volunteers at 7,082. Healthy volunteers had the highest large-family detailed-description-gap rate at 50.2 percent, ahead of Immunology and dermatology at 41.7 percent and Renal and urology at 38.3 percent. Condition-family detailed-description gaps show where the broad study narrative disappears most often in major therapeutic areas, not only fringe portfolios. Condition families are keyword-derived registry groupings, not formal disease ontologies or mutually exclusive diagnoses across all studies; they simplify diagnoses into public buckets.
<!-- END-REWRITE -->

_Line range 13830-13904 in rewrite-workbook.txt_

---

## Entry 184 ([189/921]) — ctgov-condition-enrollment-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Enrollment Gap
TYPE: methods  |  ESTIMAND: Enrollment-gap stock among older studies missing actual enrollment
DATA: 249,507 eligible older closed interventional studies with actual-enrollment gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-enrollment-gap
```

</details>

### Original (frozen — do not edit)

```
Which condition families most often leave older CT.gov study pages without actual enrollment, obscuring realized sample size after study closure? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined an enrollment gap as missing actual enrollment among older closed studies, then ranked large condition families by stock and rate. Oncology led the stock table at 2,765 studies, followed by the broad OTHER bucket at 1,815, Cardiovascular at 1,179, and Infectious disease at 747. Oncology also had the highest large-family enrollment-gap rate at 6.5 percent, ahead of cardiovascular at 4.5 percent and gastrointestinal and hepatic at 4.5 percent. Condition-family enrollment gaps show that realized sample-size discipline is weakest in exactly the therapeutic areas that dominate much of the older CT.gov registry stock. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than formal disease ontologies or mutually exclusive diagnoses alone.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families most often leave older CT.gov study pages without actual enrollment, obscuring realized sample size after study closure? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined an enrollment gap as missing actual enrollment among older closed studies, then ranked large condition families by stock and rate. Oncology led the stock table at 2,765 studies, followed by the broad OTHER bucket at 1,815, Cardiovascular at 1,179, and Infectious disease at 747. Oncology also had the highest large-family enrollment-gap rate at 6.5 percent, ahead of cardiovascular at 4.5 percent and gastrointestinal and hepatic at 4.5 percent. Condition-family enrollment gaps show that realized sample-size discipline is weakest in exactly the therapeutic areas that dominate much of the older CT.gov registry stock. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than formal disease ontologies or mutually exclusive diagnoses alone.
<!-- END-REWRITE -->

_Line range 13905-13979 in rewrite-workbook.txt_

---

## Entry 185 ([190/921]) — ctgov-condition-excess-watchlist

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Excess Watchlist
TYPE: methods  |  ESTIMAND: Adjusted excess no-results and ghost stock across CT.gov condition families
DATA: 249,507 eligible older closed interventional studies with keyword-derived condition-family labels
PATH: C:\Projects\ctgov-analyses/ctgov-condition-excess-watchlist
```

</details>

### Original (frozen — do not edit)

```
Which condition families remain worst once excess hiddenness is measured inside broad therapeutic portfolios rather than single sponsor tables? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We ranked condition families by adjusted no-results excess, adjusted ghost excess, black-box stock, and strict-core carryover using the same study-mix adjustment as wave eight. Oncology carried the largest adjusted excess no-results stock at 543 studies, followed by cardiovascular at 373 and metabolic at 251. Healthy volunteers were different: near expected on no-results, yet 1,032 studies above expectation on ghost protocols and a 33.9 percent black-box rate. Condition families therefore split into stock-heavy disease backlogs and a separate healthy-volunteer silence pattern that is much more ghosted than merely overdue inside the same older-study registry universe overall. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than adjudicated disease ontologies or mutually exclusive clinical domains.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families remain worst once excess hiddenness is measured inside broad therapeutic portfolios rather than single sponsor tables? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We ranked condition families by adjusted no-results excess, adjusted ghost excess, black-box stock, and strict-core carryover using the same study-mix adjustment as wave eight. Oncology carried the largest adjusted excess no-results stock at 543 studies, followed by cardiovascular at 373 and metabolic at 251. Healthy volunteers were different: near expected on no-results, yet 1,032 studies above expectation on ghost protocols and a 33.9 percent black-box rate. Condition families therefore split into stock-heavy disease backlogs and a separate healthy-volunteer silence pattern that is much more ghosted than merely overdue inside the same older-study registry universe overall. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than adjudicated disease ontologies or mutually exclusive clinical domains.
<!-- END-REWRITE -->

_Line range 13980-14054 in rewrite-workbook.txt_

---

## Entry 186 ([191/921]) — ctgov-condition-ghost-watchlist

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Ghost Watchlist
TYPE: methods  |  ESTIMAND: Excess ghost-protocol stock across condition families
DATA: 249,507 eligible older closed interventional studies with condition-family ghost watchlists derived from the wave-nine tables
PATH: C:\Projects\ctgov-analyses/ctgov-condition-ghost-watchlist
```

</details>

### Original (frozen — do not edit)

```
Which condition families remain most ghosted once the series stops centering missing-results stock and instead ranks excess ghost protocols? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. Using the wave-nine condition watchlist, we ranked condition families by excess ghost stock, raw ghost counts, black-box stock, and black-box rates. Healthy volunteers carried the largest condition-family ghost excess at 1,032 studies, far ahead of the broader OTHER bucket at 552 and musculoskeletal and pain at 333. Gastrointestinal and hepatic portfolios also remained above expectation, while several major disease families such as oncology and cardiovascular were below expectation on this stricter ghost target. The ghost table therefore identifies a different silence pattern than the no-results table, centered on healthy-volunteer and diffuse non-disease portfolios with unusually thin and fragmented public traces. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than adjudicated disease ontologies.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families remain most ghosted once the series stops centering missing-results stock and instead ranks excess ghost protocols? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. Using the wave-nine condition watchlist, we ranked condition families by excess ghost stock, raw ghost counts, black-box stock, and black-box rates. Healthy volunteers carried the largest condition-family ghost excess at 1,032 studies, far ahead of the broader OTHER bucket at 552 and musculoskeletal and pain at 333. Gastrointestinal and hepatic portfolios also remained above expectation, while several major disease families such as oncology and cardiovascular were below expectation on this stricter ghost target. The ghost table therefore identifies a different silence pattern than the no-results table, centered on healthy-volunteer and diffuse non-disease portfolios with unusually thin and fragmented public traces. Condition families are keyword-derived registry groupings, so they approximate therapeutic portfolios rather than adjudicated disease ontologies.
<!-- END-REWRITE -->

_Line range 14055-14129 in rewrite-workbook.txt_

---

## Entry 187 ([192/921]) — ctgov-condition-narrative-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Narrative Gap
TYPE: methods  |  ESTIMAND: Narrative-gap stock among older studies missing both detailed descriptions and primary outcome descriptions
DATA: 249,507 eligible older closed interventional studies with condition-family narrative-gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-narrative-gap
```

</details>

### Original (frozen — do not edit)

```
Which condition families most often leave older CT.gov study pages without both detailed descriptions and primary outcome descriptions? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a narrative-gap study as one missing both detailed description and primary outcome description, then ranked large condition families by stock and rate. The broad OTHER bucket led the narrative-gap stock table at 5,124 studies, followed by Oncology at 4,105, Cardiovascular at 3,240, and Healthy volunteers at 3,100. Healthy volunteers had the sharpest large-family narrative-gap rate at 22.0 percent, ahead of Metabolic at 14.8 percent and Renal and urology at 14.6 percent. Condition-family narrative gaps show where registry pages stay text-thin even before readers ask whether results or publications were posted later. Condition families are keyword-derived registry groupings, not formal disease ontologies or mutually exclusive diagnoses for readers. They simplify diverse diagnoses into usable public buckets.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families most often leave older CT.gov study pages without both detailed descriptions and primary outcome descriptions? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a narrative-gap study as one missing both detailed description and primary outcome description, then ranked large condition families by stock and rate. The broad OTHER bucket led the narrative-gap stock table at 5,124 studies, followed by Oncology at 4,105, Cardiovascular at 3,240, and Healthy volunteers at 3,100. Healthy volunteers had the sharpest large-family narrative-gap rate at 22.0 percent, ahead of Metabolic at 14.8 percent and Renal and urology at 14.6 percent. Condition-family narrative gaps show where registry pages stay text-thin even before readers ask whether results or publications were posted later. Condition families are keyword-derived registry groupings, not formal disease ontologies or mutually exclusive diagnoses for readers; they simplify diverse diagnoses into usable public buckets.
<!-- END-REWRITE -->

_Line range 14130-14204 in rewrite-workbook.txt_

---

## Entry 188 ([193/921]) — ctgov-condition-overdue-debt

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Overdue Debt
TYPE: methods  |  ESTIMAND: Total unresolved years beyond the two-year results mark across CT.gov condition families
DATA: 249,507 eligible older closed interventional studies with condition-family overdue debt, missing-results, and mean unresolved age fields
PATH: C:\Projects\ctgov-analyses/ctgov-condition-overdue-debt
```

</details>

### Original (frozen — do not edit)

```
Which condition families hold the deepest overdue debt once unresolved years beyond the two-year mark are added up rather than reduced to missing-results rate? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We summed overdue years beyond the two-year mark across condition families and compared debt stock with missing-results counts and mean unresolved age. The broad OTHER bucket carried the largest condition-family overdue debt at 289,823 unresolved years, while Oncology was the largest named family at 255,229 and Cardiovascular followed at 154,672. Metabolic and healthy-volunteer portfolios also carried very large overdue debt, while oncology had the heaviest named-family mean unresolved age at 9.0 years. Condition debt mixes broad diffuse registry stock with large named disease portfolios that stay unresolved for years after the reporting window closes. Condition families are keyword-derived registry groupings, so the debt tables describe therapeutic portfolios rather than disease ontologies.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families hold the deepest overdue debt once unresolved years beyond the two-year mark are added up rather than reduced to missing-results rate? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We summed overdue years beyond the two-year mark across condition families and compared debt stock with missing-results counts and mean unresolved age. The broad OTHER bucket carried the largest condition-family overdue debt at 289,823 unresolved years, while Oncology was the largest named family at 255,229 and Cardiovascular followed at 154,672. Metabolic and healthy-volunteer portfolios also carried very large overdue debt, while oncology had the heaviest named-family mean unresolved age at 9.0 years. Condition debt mixes broad diffuse registry stock with large named disease portfolios that stay unresolved for years after the reporting window closes. Condition families are keyword-derived registry groupings, so the debt tables describe therapeutic portfolios rather than disease ontologies.
<!-- END-REWRITE -->

_Line range 14205-14279 in rewrite-workbook.txt_

---

## Entry 189 ([194/921]) — ctgov-condition-primary-only-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Primary-Only Gap
TYPE: methods  |  ESTIMAND: Primary-only-gap stock among older studies missing the primary outcome description field while retaining the detailed description field
DATA: 249,507 eligible older closed interventional studies with primary-only-gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-primary-only-gap
```

</details>

### Original (frozen — do not edit)

```
Which condition families most often leave older CT.gov study pages without the primary outcome description while keeping the broader detailed-description field? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a primary-only gap as missing primary outcome description with detailed description still present, then ranked large condition families by stock and rate. Oncology led the condition-family primary-only-gap stock table at 7,102 studies, followed by Other at 5,818, Cardiovascular at 3,766, and Infectious disease at 2,584. Oncology also had the highest large-family primary-only-gap rate at 16.8 percent, ahead of Cardiovascular at 14.5 percent and Infectious disease at 14.3 percent. Condition-family primary-only gaps show where the endpoint sentence disappears most often even though the broader study narrative remains on the page. Condition families are keyword-derived registry groupings rather than formal disease ontologies or mutually exclusive diagnoses across all studies. They simplify diagnoses for readers.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families most often leave older CT.gov study pages without the primary outcome description while keeping the broader detailed-description field? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a primary-only gap as missing primary outcome description with detailed description still present, then ranked large condition families by stock and rate. Oncology led the condition-family primary-only-gap stock table at 7,102 studies, followed by Other at 5,818, Cardiovascular at 3,766, and Infectious disease at 2,584. Oncology also had the highest large-family primary-only-gap rate at 16.8 percent, ahead of Cardiovascular at 14.5 percent and Infectious disease at 14.3 percent. Condition-family primary-only gaps show where the endpoint sentence disappears most often even though the broader study narrative remains on the page. Condition families are keyword-derived registry groupings rather than formal disease ontologies or mutually exclusive diagnoses across all studies; they simplify diagnoses for readers.
<!-- END-REWRITE -->

_Line range 14280-14354 in rewrite-workbook.txt_

---

## Entry 190 ([195/921]) — ctgov-condition-primary-outcome-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Primary-Outcome Gap
TYPE: methods  |  ESTIMAND: Primary-outcome-gap stock among older studies missing the primary outcome description field
DATA: 249,507 eligible older closed interventional studies with condition-family primary-outcome-gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-primary-outcome-gap
```

</details>

### Original (frozen — do not edit)

```
Which condition families most often leave older CT.gov study pages without primary outcome descriptions, obscuring the main endpoint for readers? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a primary-outcome gap as a missing primary outcome description, then ranked large condition families by stock and rate. Oncology led the condition-family primary-outcome-gap stock table at 11,207 studies, followed by the broad OTHER bucket at 10,942, Cardiovascular at 7,006, and Metabolic at 5,006. Healthy volunteers had the sharpest large-family primary-outcome-gap rate at 35.0 percent, ahead of Metabolic at 28.9 percent and Renal and urology at 28.8 percent. Condition-family primary-outcome gaps show where registry pages omit the endpoint-defining sentence in major therapeutic areas, not only smaller fringe portfolios. Condition families are keyword-derived registry groupings rather than formal disease ontologies or mutually exclusive diagnoses across all studies. They simplify diverse diagnoses into usable public buckets.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families most often leave older CT.gov study pages without primary outcome descriptions, obscuring the main endpoint for readers? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We defined a primary-outcome gap as a missing primary outcome description, then ranked large condition families by stock and rate. Oncology led the condition-family primary-outcome-gap stock table at 11,207 studies, followed by the broad OTHER bucket at 10,942, Cardiovascular at 7,006, and Metabolic at 5,006. Healthy volunteers had the sharpest large-family primary-outcome-gap rate at 35.0 percent, ahead of Metabolic at 28.9 percent and Renal and urology at 28.8 percent. Condition-family primary-outcome gaps show where registry pages omit the endpoint-defining sentence in major therapeutic areas, not only smaller fringe portfolios. Condition families are keyword-derived registry groupings rather than formal disease ontologies or mutually exclusive diagnoses across all studies; they simplify diverse diagnoses into usable public buckets.
<!-- END-REWRITE -->

_Line range 14355-14429 in rewrite-workbook.txt_

---

## Entry 191 ([196/921]) — ctgov-condition-sponsor-repeaters

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Sponsor Repeaters
TYPE: methods  |  ESTIMAND: Sponsor-level 2-year no-results counts within selected disease families among eligible older CT.gov studies
DATA: 249,507 eligible older closed interventional studies linked to oncology, cardiovascular, and metabolic condition families and lead sponsors
PATH: C:\Projects\ctgov-analyses/ctgov-condition-sponsor-repeaters
```

</details>

### Original (frozen — do not edit)

```
Which sponsors carry the largest missing-results backlogs inside disease families on ClinicalTrials.gov once studies are grouped by condition rather than pooled together? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and linked sponsors to oncology, cardiovascular, and metabolic condition families. The project compares sponsor-level no-results counts, no-results rates, ghost-protocol rates, and visible shares within each selected disease family. In oncology, the National Cancer Institute carried the largest missing-results stock at 909 older studies, ahead of M.D. Anderson Cancer Center at 589. In cardiovascular studies, Assistance Publique-Hôpitaux de Paris reached 100.0 percent no results and Yonsei University 98.6 percent, while Novo Nordisk led metabolic backlogs with 391 studies. Sponsor repeaters therefore change sharply by disease family, and condition-specific audits reveal institutional pockets of silence that disappear inside whole-registry rankings. Condition families and sponsor names are derived from registry text and do not adjudicate network authorship, parent ownership, or off-platform reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which sponsors carry the largest missing-results backlogs inside disease families on ClinicalTrials.gov once studies are grouped by condition rather than pooled together? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and linked sponsors to oncology, cardiovascular, and metabolic condition families. The project compares sponsor-level no-results counts, no-results rates, ghost-protocol rates, and visible shares within each selected disease family. In oncology, the National Cancer Institute carried the largest missing-results stock at 909 older studies, ahead of M.D; anderson Cancer Center at 589. In cardiovascular studies, Assistance Publique-Hôpitaux de Paris reached 100.0 percent no results and Yonsei University 98.6 percent, while Novo Nordisk led metabolic backlogs with 391 studies. Sponsor repeaters therefore change sharply by disease family, and condition-specific audits reveal institutional pockets of silence that disappear inside whole-registry rankings. Condition families and sponsor names are derived from registry text and do not adjudicate network authorship, parent ownership, or off-platform reporting.
<!-- END-REWRITE -->

_Line range 14430-14504 in rewrite-workbook.txt_

---

## Entry 192 ([197/921]) — ctgov-condition-text-asymmetry

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Text Asymmetry
TYPE: methods  |  ESTIMAND: Condition-family text asymmetry, defined as description-only gaps minus primary-only gaps
DATA: 249,507 eligible older closed interventional studies with condition-family description-only, primary-only, and net text-balance summaries
PATH: C:\Projects\ctgov-analyses/ctgov-condition-text-asymmetry
```

</details>

### Original (frozen — do not edit)

```
Which condition families show the biggest imbalance between missing detailed descriptions and missing primary-outcome-only text in older CT.gov records? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We compared description-only gaps against primary-only gaps and defined net text asymmetry as description-only minus primary-only counts and rates. Other led the condition-family text-asymmetry table at 7,699 net description-only gaps, followed by Musculoskeletal and pain at 2,521, Healthy volunteers at 2,134, and Cardiovascular at 1,802. Immunology and dermatology had the highest condition asymmetry rate at 19.7 percentage points, while Healthy volunteers reached 15.1 points and Neurology 15.0 points. The asymmetry lens shows which therapeutic portfolios lose the broader study narrative much more often than the endpoint sentence, changing how text opacity is distributed for readers. Positive asymmetry does not by itself prove concealment; it shows which field disappears more often inside mature public registry records overall.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which condition families show the biggest imbalance between missing detailed descriptions and missing primary-outcome-only text in older CT.gov records? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot using one condition-family label per study. We compared description-only gaps against primary-only gaps and defined net text asymmetry as description-only minus primary-only counts and rates. Other led the condition-family text-asymmetry table at 7,699 net description-only gaps, followed by Musculoskeletal and pain at 2,521, Healthy volunteers at 2,134, and Cardiovascular at 1,802. Immunology and dermatology had the highest condition asymmetry rate at 19.7 percentage points, while Healthy volunteers reached 15.1 points and Neurology 15.0 points. The asymmetry lens shows which therapeutic portfolios lose the broader study narrative much more often than the endpoint sentence, changing how text opacity is distributed for readers. Positive asymmetry does not by itself prove concealment; it shows which field disappears more often inside mature public registry records overall.
<!-- END-REWRITE -->

_Line range 14505-14579 in rewrite-workbook.txt_

---

## Entry 193 ([198/921]) — ctgov-country-ancient-backlog

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country Ancient Backlog
TYPE: methods  |  ESTIMAND: Ancient-backlog stock among older closed interventional studies unresolved at least ten overdue years beyond the two-year mark
DATA: 249,507 eligible older closed interventional studies with ancient-backlog stock, rate, and overdue-years summaries
PATH: C:\Projects\ctgov-analyses/ctgov-country-ancient-backlog
```

</details>

### Original (frozen — do not edit)

```
Which country-linked CT.gov portfolios still hold the largest stock of studies unresolved at least ten overdue years beyond the two-year reporting mark? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined ancient backlog as older studies with no posted results and at least ten overdue years beyond the two-year mark, then ranked country-linked portfolios with at least 500 linked studies. The United States led the country-linked table at 22,301 studies, followed by Canada at 4,055, Germany at 3,759, and France at 3,569. Iran had the highest large-country ancient-backlog rate at 46.4 percent, while Norway, India, and Finland also ranked sharply on rate. Ancient backlog shows that very old silence is not restricted to one geography, but remains concentrated in a small set of large country-linked portfolios. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which country-linked CT.gov portfolios still hold the largest stock of studies unresolved at least ten overdue years beyond the two-year reporting mark? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined ancient backlog as older studies with no posted results and at least ten overdue years beyond the two-year mark, then ranked country-linked portfolios with at least 500 linked studies. The United States led the country-linked table at 22,301 studies, followed by Canada at 4,055, Germany at 3,759, and France at 3,569. Iran had the highest large-country ancient-backlog rate at 46.4 percent, while Norway, India, and Finland also ranked sharply on rate. Ancient backlog shows that very old silence is not restricted to one geography, but remains concentrated in a small set of large country-linked portfolios. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry.
<!-- END-REWRITE -->

_Line range 14580-14654 in rewrite-workbook.txt_

---

## Entry 194 ([199/921]) — ctgov-country-condition-hiddenness

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country-Condition Hiddenness
TYPE: methods  |  ESTIMAND: 2-year no-results rate across selected country-by-condition cells among eligible older CT.gov studies
DATA: 249,507 eligible older closed interventional studies exploded into named-country condition-family cells
PATH: C:\Projects\ctgov-analyses/ctgov-country-condition-hiddenness
```

</details>

### Original (frozen — do not edit)

```
Which disease-country cells look quietest on ClinicalTrials.gov once older closed interventional studies are split simultaneously by condition family and named study location? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded named-country involvement within selected condition families. The project compares two-year no-results rates, ghost-protocol rates, and visible shares for oncology, cardiovascular, and metabolic studies across country-condition cells with at least 400 studies. Oncology studies involving China reached 79.0 percent no results versus 52.6 percent for oncology studies involving the United States. Cardiovascular studies involving Egypt reached 95.9 percent no results, while metabolic studies involving China reached 78.9 percent and Denmark 79.6 percent. Disease and geography therefore interact rather than add independently, because the same condition family looks materially different once specific country footprints are named inside the same nominal therapeutic area. Country-condition cells reflect recorded study locations rather than country-specific enrollment shares, sponsor domicile, or national reporting mandates.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which disease-country cells look quietest on ClinicalTrials.gov once older closed interventional studies are split simultaneously by condition family and named study location? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded named-country involvement within selected condition families. The project compares two-year no-results rates, ghost-protocol rates, and visible shares for oncology, cardiovascular, and metabolic studies across country-condition cells with at least 400 studies. Oncology studies involving China reached 79.0 percent no results versus 52.6 percent for oncology studies involving the United States. Cardiovascular studies involving Egypt reached 95.9 percent no results, while metabolic studies involving China reached 78.9 percent and Denmark 79.6 percent. Disease and geography therefore interact rather than add independently, because the same condition family looks materially different once specific country footprints are named inside the same nominal therapeutic area. Country-condition cells reflect recorded study locations rather than country-specific enrollment shares, sponsor domicile, or national reporting mandates.
<!-- END-REWRITE -->

_Line range 14655-14729 in rewrite-workbook.txt_

---

## Entry 195 ([200/921]) — ctgov-country-description-black-box

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country Description Black-Box
TYPE: methods  |  ESTIMAND: Description black-box stock among older studies with no results, no linked publication, no detailed description, and no primary outcome description
DATA: 249,507 eligible older closed interventional studies with description-black-box stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-country-description-black-box
```

</details>

### Original (frozen — do not edit)

```
Which country-linked CT.gov portfolios carry the most older studies that are overdue, unlinked, and missing both detailed description and primary outcome description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined a description black-box study as one with a two-year results gap, no linked publication, no detailed description, and no primary outcome description, then ranked country-linked portfolios with at least 500 linked studies. The United States led the country-linked stock table at 5,833 studies, followed by France at 1,353, Germany at 1,262, and Canada at 1,036. Japan had the highest large-country description-black-box rate at 10.7 percent, while South Korea reached 9.1 percent and Germany 8.4 percent. Country-linked black-box tables show where the strictest narrative opacity remains concentrated after studies failed results and linkage tests. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry for readers.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which country-linked CT.gov portfolios carry the most older studies that are overdue, unlinked, and missing both detailed description and primary outcome description? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined a description black-box study as one with a two-year results gap, no linked publication, no detailed description, and no primary outcome description, then ranked country-linked portfolios with at least 500 linked studies. The United States led the country-linked stock table at 5,833 studies, followed by France at 1,353, Germany at 1,262, and Canada at 1,036. Japan had the highest large-country description-black-box rate at 10.7 percent, while South Korea reached 9.1 percent and Germany 8.4 percent. Country-linked black-box tables show where the strictest narrative opacity remains concentrated after studies failed results and linkage tests. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry for readers.
<!-- END-REWRITE -->

_Line range 14730-14804 in rewrite-workbook.txt_

---

## Entry 196 ([201/921]) — ctgov-country-detailed-description-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country Detailed-Description Gap
TYPE: methods  |  ESTIMAND: Detailed-description-gap stock among older studies missing the detailed description field
DATA: 249,507 eligible older closed interventional studies with detailed-description-gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-country-detailed-description-gap
```

</details>

### Original (frozen — do not edit)

```
Which country-linked CT.gov portfolios most often leave older study pages without detailed descriptions, removing the broad paragraph that explains what was studied? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined a detailed-description gap as a missing detailed description field, then ranked country-linked portfolios with at least 500 linked studies by stock and rate. The United States led the country-linked detailed-description-gap stock table at 32,378 studies, followed by France at 8,095, Germany at 7,976, and Canada at 6,834. Japan had the highest large-country detailed-description-gap rate at 63.3 percent, while Slovakia reached 58.1 percent and Romania 56.3 percent. Country-linked detailed-description gaps show where the broad registry narrative disappears most often even when the record still carries dates and status fields. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in registry link tables. They describe registry link geography only.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which country-linked CT.gov portfolios most often leave older study pages without detailed descriptions, removing the broad paragraph that explains what was studied? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined a detailed-description gap as a missing detailed description field, then ranked country-linked portfolios with at least 500 linked studies by stock and rate. The United States led the country-linked detailed-description-gap stock table at 32,378 studies, followed by France at 8,095, Germany at 7,976, and Canada at 6,834. Japan had the highest large-country detailed-description-gap rate at 63.3 percent, while Slovakia reached 58.1 percent and Romania 56.3 percent. Country-linked detailed-description gaps show where the broad registry narrative disappears most often even when the record still carries dates and status fields. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in registry link tables; they describe registry link geography only.
<!-- END-REWRITE -->

_Line range 14805-14879 in rewrite-workbook.txt_

---

## Entry 197 ([202/921]) — ctgov-country-enrollment-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country Enrollment Gap
TYPE: methods  |  ESTIMAND: Enrollment-gap stock among older studies missing actual enrollment
DATA: 249,507 eligible older closed interventional studies with actual-enrollment gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-country-enrollment-gap
```

</details>

### Original (frozen — do not edit)

```
Which country-linked CT.gov portfolios most often leave older study pages without actual enrollment, obscuring realized sample size after study closure? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined an enrollment gap as missing actual enrollment among older closed studies, then ranked country-linked portfolios with at least 500 linked studies by stock and rate. The United States led the stock table at 4,573 studies, followed by Canada at 797, Germany at 663, and France at 559. Iran had the highest large-country enrollment-gap rate at 6.3 percent, while Israel reached 6.1 percent and Norway 5.4 percent. Country-linked enrollment gaps show where realized sample-size discipline remains weak even after studies are old enough that timing-based excuses should be less plausible. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry as they appear here today for outside readers.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which country-linked CT.gov portfolios most often leave older study pages without actual enrollment, obscuring realized sample size after study closure? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined an enrollment gap as missing actual enrollment among older closed studies, then ranked country-linked portfolios with at least 500 linked studies by stock and rate. The United States led the stock table at 4,573 studies, followed by Canada at 797, Germany at 663, and France at 559. Iran had the highest large-country enrollment-gap rate at 6.3 percent, while Israel reached 6.1 percent and Norway 5.4 percent. Country-linked enrollment gaps show where realized sample-size discipline remains weak even after studies are old enough that timing-based excuses should be less plausible. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry as they appear here today for outside readers.
<!-- END-REWRITE -->

_Line range 14880-14954 in rewrite-workbook.txt_

---

## Entry 198 ([203/921]) — ctgov-country-excess-watchlist

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country Excess Watchlist
TYPE: methods  |  ESTIMAND: Adjusted excess no-results and ghost stock across country-linked study portfolios with at least 500 linked studies
DATA: 249,507 eligible older closed interventional studies exploded into named-country links for country-linked watchlists
PATH: C:\Projects\ctgov-analyses/ctgov-country-excess-watchlist
```

</details>

### Original (frozen — do not edit)

```
Which country-linked CT.gov portfolios remain most opaque after visible study mix is held more constant? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded named-country links. We summed adjusted no-results excess, adjusted ghost excess, black-box stock, and strict-core spillover across country-linked study portfolios with at least 500 linked studies. France carried the largest country-linked adjusted excess no-results stock at 2,187 studies, followed by China at 1,299 and Egypt at 824. China and Egypt also showed large ghost excess, while South Korea reached a 21.2 percent black-box rate and France still carried 3,093 black-box studies. The geography story therefore mixes large Western institutional stock with sharper hiddenness tails in several Asian and Middle Eastern portfolios once adjusted stock, ghost excess, and black-box depth are read together. Country watchlists count country-linked studies rather than assigning each study to only one nation, so multinational records can contribute to multiple national portfolios.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which country-linked CT.gov portfolios remain most opaque after visible study mix is held more constant? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded named-country links. We summed adjusted no-results excess, adjusted ghost excess, black-box stock, and strict-core spillover across country-linked study portfolios with at least 500 linked studies. France carried the largest country-linked adjusted excess no-results stock at 2,187 studies, followed by China at 1,299 and Egypt at 824. China and Egypt also showed large ghost excess, while South Korea reached a 21.2 percent black-box rate and France still carried 3,093 black-box studies. The geography story therefore mixes large Western institutional stock with sharper hiddenness tails in several Asian and Middle Eastern portfolios once adjusted stock, ghost excess, and black-box depth are read together. Country watchlists count country-linked studies rather than assigning each study to only one nation, so multinational records can contribute to multiple national portfolios.
<!-- END-REWRITE -->

_Line range 14955-15029 in rewrite-workbook.txt_

---

## Entry 199 ([204/921]) — ctgov-country-ghost-watchlist

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country Ghost Watchlist
TYPE: methods  |  ESTIMAND: Excess ghost-protocol stock across country-linked study portfolios
DATA: 249,507 eligible older closed interventional studies exploded into named-country links and ranked by ghost excess
PATH: C:\Projects\ctgov-analyses/ctgov-country-ghost-watchlist
```

</details>

### Original (frozen — do not edit)

```
Which country-linked CT.gov portfolios remain most ghosted above expectation once the series shifts from adjusted no-results stock to excess ghost protocols? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded named-country links. Using the wave-nine country watchlist, we ranked country-linked portfolios by excess ghost stock, raw ghost counts, black-box stock, and black-box rates. France carried the largest country-linked ghost excess at 1,157 studies, followed by China at 1,007, Egypt at 955, and South Korea at 871. South Korea and China also stood out on black-box intensity, while France remained the largest Western ghost-stock portfolio on count. The deeper-silence geography therefore mixes very large European stock with sharper Asian and Middle Eastern ghost tails once stock-heavy Western systems, East Asian portfolios, and Egyptian-linked studies are read in the same frame together carefully. Country-linked ghost tables count country-linked studies rather than assigning each multinational record to one exclusive national portfolio.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which country-linked CT.gov portfolios remain most ghosted above expectation once the series shifts from adjusted no-results stock to excess ghost protocols? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded named-country links. Using the wave-nine country watchlist, we ranked country-linked portfolios by excess ghost stock, raw ghost counts, black-box stock, and black-box rates. France carried the largest country-linked ghost excess at 1,157 studies, followed by China at 1,007, Egypt at 955, and South Korea at 871. South Korea and China also stood out on black-box intensity, while France remained the largest Western ghost-stock portfolio on count. The deeper-silence geography therefore mixes very large European stock with sharper Asian and Middle Eastern ghost tails once stock-heavy Western systems, East Asian portfolios, and Egyptian-linked studies are read in the same frame together carefully. Country-linked ghost tables count country-linked studies rather than assigning each multinational record to one exclusive national portfolio.
<!-- END-REWRITE -->

_Line range 15030-15104 in rewrite-workbook.txt_

---

## Entry 200 ([205/921]) — ctgov-country-narrative-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Country Narrative Gap
TYPE: methods  |  ESTIMAND: Narrative-gap stock among older studies missing both detailed descriptions and primary outcome descriptions
DATA: 249,507 eligible older closed interventional studies with country-linked narrative-gap stock and rate summaries
PATH: C:\Projects\ctgov-analyses/ctgov-country-narrative-gap
```

</details>

### Original (frozen — do not edit)

```
Which country-linked CT.gov portfolios most often leave older closed study pages without both detailed descriptions and primary outcome descriptions? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined a narrative-gap study as one missing both detailed description and primary outcome description, then ranked country-linked portfolios with at least 500 linked studies by stock and rate. The United States led the narrative-gap stock table at 9,049 studies, followed by Germany at 2,438, France at 2,420, and Canada at 1,853. Japan had the sharpest large-country narrative-gap rate at 17.9 percent, ahead of Finland at 16.6 percent and Germany at 16.3 percent. Country-linked narrative gaps show where registry pages remain text-thin even when they retain dates, status fields, and other basic metadata on the public page for readers. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry tables.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which country-linked CT.gov portfolios most often leave older closed study pages without both detailed descriptions and primary outcome descriptions? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and exploded country links. We defined a narrative-gap study as one missing both detailed description and primary outcome description, then ranked country-linked portfolios with at least 500 linked studies by stock and rate. The United States led the narrative-gap stock table at 9,049 studies, followed by Germany at 2,438, France at 2,420, and Canada at 1,853. Japan had the sharpest large-country narrative-gap rate at 17.9 percent, ahead of Finland at 16.6 percent and Germany at 16.3 percent. Country-linked narrative gaps show where registry pages remain text-thin even when they retain dates, status fields, and other basic metadata on the public page for readers. Country-linked rows are non-exclusive because multinational studies can contribute to more than one national portfolio in the registry tables.
<!-- END-REWRITE -->

_Line range 15105-15179 in rewrite-workbook.txt_

---

