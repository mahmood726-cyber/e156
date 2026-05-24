# Rewrite chunk 001 — entries 1-50

_Previous: rewrite-PHONE-000-HEADER.md | Next: rewrite-PHONE-002.md | Index: rewrite-PHONE-INDEX.md_

Edit ONLY the `YOUR REWRITE` section under each entry. The `Original`
block is frozen — do not edit it. Save the file when done. On your
laptop run `python C:\E156\merge-rewrite.py` to assemble a new
workbook (`rewrite-workbook.NEW.txt`) with your edits applied.

---

## Entry 1 ([1/921]) — 501MLM

<details><summary>Metadata</summary>

```
TITLE: MLM501: Cochrane Multilevel Meta-Analysis Effects Table from 501 Reviews
TYPE: methods  |  ESTIMAND: SMD
DATA: 501 Cochrane systematic reviews
PATH: C:\Projects\501MLM
```

</details>

### Original (frozen — do not edit)

```
Could a single R package unify effect-size data from hundreds of Cochrane reviews into a coherent multilevel meta-analysis effects table? We gathered  501 Cochrane systematic reviews covering dichotomous and continuous outcomes using python code. We preserved study-level moderators, DOI provenance, and original data URLs. MLM501 deprives standardized treatment effects and standard errors It  fits three-level random-effects models via metafor, and computes fragility indices using the MAFI algorithm for robustness. In the 501-review corpus the pooled SMD was 0.24 (95% CI 0.18-0.31). There was substantial review-level heterogeneity, and the median fragility index was 3.. This indicates most pooled conclusions depend on very few event reassignments. Our Leave-one-review-out analyses and robust variance estimation confirmed the  stability of the overall effect direction (for both log-odds-ratio and standardized-mean-difference cohorts). A single importable table with full provenance enables rapid cross-review methods research (without repeated manual extraction from the Cochrane archive). The package doesn't address outcome definition heterogeneity across reviews. Users should exercise caution when pooling across clinically dissimilar interventions.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a R package unify effect-size data from Cochrane reviews from 2023 onwards into a coherent multilevel meta-analysis effects table? We downloaded 501 Cochrane systematic reviews covering dichotomous and continuous outcomes while preserving study-level moderators. MLM501 derives standardized treatment effects and standard errors, fits three-level random-effects models via metafor, it computes fragility indices using the MAFI algorithm for robustness. Across corpus the pooled SMD was 0.24 (95% CI 0.18-0.31) (with substantial review-level heterogeneity). The median fragility index was 3, indicating most pooled conclusions depend on very few event reassignments. The Leave-one-review-out analyses and robust variance estimation confirmed stability of the overall effect direction for both log-odds-ratio and standardized-mean-difference cohorts. A single importable table with full provenance enables rapid cross-review methods research, the package cannot however address outcome definition heterogeneity across reviews.
<!-- END-REWRITE -->

_Line range 94-168 in rewrite-workbook.txt_

---

## Entry 2 ([2/921]) — 501MLM_Submission

<details><summary>Metadata</summary>

```
TITLE: MLM501 Software Article: Building Large-Scale Meta-Analytic Datasets from Cochrane Reviews
TYPE: methods  |  ESTIMAND: OR
DATA: 501 Cochrane reviews, 12,847 study records
PATH: C:\Projects\501MLM_Submission
```

</details>

### Original (frozen — do not edit)

```
How can researchers efficiently construct large-scale multilevel meta-analysis datasets from Cochrane systematic reviews while preserving full data provenance? We developed MLM501 as an R package and applied it to 501 Cochrane reviews, extracting study-level effect sizes, moderators, and DOI-linked provenance metadata. The package automates effect-size derivation for dichotomous and continuous endpoints, fits three-level hierarchical models, computes fragility indices, and exports structured tables with audit trails. From 501 reviews the package assembled 12,847 study-level records with a pooled OR of 0.78 (95% CI 0.72-0.85) for the dichotomous cohort, confirming feasibility of automated large-scale construction. Cross-validation against manually extracted values from five benchmark reviews showed perfect concordance, and all unit tests passed across R versions 4.1 through 4.5. This tool reduces weeks of manual extraction to minutes, enabling methodological researchers to study cross-review heterogeneity patterns at scale. The current scope is limited to Cochrane reviews with downloadable data, and the importer cannot handle proprietary or non-standard review formats.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can we efficiently construct large-scale multilevel meta-analysis datasets from Cochrane systematic reviews with full data provenance? We have created MLM501 as an R package and applied it to 501 Cochrane reviews. We extracted study-level effect sizes, moderators, and DOI-linked provenance metadata using python code.The package automates effect-size derivation for dichotomous and continuous endpoints It fits three-level hierarchical models and computes fragility indices. From 501 reviews the package assembled 12,847 study-level records. The pooled OR was 0.78 (95% CI 0.72-0.85) for the dichotomous cohort, this confirms feasibility of automated large-scale construction. This tool can reduce  manual extraction enabling methodological researchers to study cross-review heterogeneity patterns . However, current scope is Cochrane reviews with downloadable data.
<!-- END-REWRITE -->

_Line range 169-243 in rewrite-workbook.txt_

---

## Entry 3 ([3/921]) — AdaptSim

<details><summary>Metadata</summary>

```
TITLE: AdaptSim: A Browser-Based Simulator for Adaptive Group-Sequential Trial Design Matching rpact to Four Decimal Places
TYPE: methods  |  ESTIMAND: Boundary computation accuracy vs rpact (decimal places of agreement)
DATA: Validated against rpact R package; 3 pre-loaded CV trial examples
PATH: C:\AdaptSim
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based tool reproduce adaptive group-sequential trial designs with the accuracy of established software while remaining usable at the point of care? We implemented the Armitage-McPherson-Rowe recursive integration algorithm with 32-point Gauss-Legendre quadrature in a single-file browser application supporting four alpha-spending functions and both binding and non-binding futility rules. AdaptSim calculates monitoring boundaries, simulates operating characteristics with up to 100,000 Monte Carlo trials, and exports protocol-ready outputs. Boundary calculations matched rpact to four decimal places, with mean sensitivity to true effect of 0.98 (95% CI 0.96 to 0.99) and Monte Carlo type I error within 0.002 of nominal alpha. Three worked examples based on DAPA-HF, EMPEROR-Reduced, and SPRINT showed that the interface supports realistic cardiovascular trial scenarios without local installation. A free browser implementation could widen access to adaptive design methods that otherwise depend on specialist software. The current version is limited to group-sequential designs and does not yet support adaptive enrichment or platform trials.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Is it possible to create a browser-based tool for reproducing adaptive group-sequential trial designs with the accuracy of established software? We have  implemented the Armitage-McPherson-Rowe recursive integration algorithm with 32-point Gauss-Legendre quadrature in a browser application. This supports four alpha-spending functions. It also supports both binding and non-binding futility rules. This calculates monitoring boundaries and simulates operating characteristics. This uses up to 100,000 Monte Carlo trials, and exports protocol-ready outputs. Our Boundary calculations matched rpact to four decimal places. The mean sensitivity to true effect was 0.98 (95% CI 0.96 to 0.99) (and Monte Carlo type I error within 0.002 of nominal alpha). Three examples using DAPA-HF, EMPEROR-Reduced, and SPRINT were used which showed that the interface can support realistic cardiovascular trial scenarios. A public  browser implementation could widen access to adaptive design methods The current version is still  limited to group-sequential designs at this time.
<!-- END-REWRITE -->

_Line range 244-318 in rewrite-workbook.txt_

---

## Entry 4 ([4/921]) — advanced-nma-pooling

<details><summary>Metadata</summary>

```
TITLE: Advanced NMA Pooling Toolkit with Bias Adjustment and Survival Extensions
TYPE: methods  |  ESTIMAND: Bias-adjusted treatment effect (log-odds)
DATA: Contrast-level NMA data with aggregate and individual patient data
PATH: C:\Models\advanced-nma-pooling
```

</details>

### Original (frozen — do not edit)

```
How can network meta-analysis accommodate individual patient data alongside aggregate data while adjusting for design-related biases across heterogeneous evidence sources? We developed a Python toolkit implementing multilevel network meta-regression, bias-adjusted models, and survival extensions for advanced evidence synthesis across different data types. The package provides frequentist and Bayesian backends with Stan integration, strict schema validation, config-driven pipelines, and validation against R netmeta and multinma benchmarks. In 18 network comparisons, the bias-adjusted model achieved mean absolute error of 0.003 log-odds units (95% CI 0.001 to 0.008) versus 0.021 for unadjusted pooling against R references. Design-stratified adjustment shifted the ranking probability for the top treatment by 11 percentage points relative to naive pooling, demonstrating clinically relevant sensitivity to design confounding. The toolkit enables reproducible advanced NMA workflows through command-line pipelines with model-card JSON outputs for transparent reporting and audit. One limitation is that Bayesian backends require Stan compilation, creating installation dependencies that may restrict accessibility for non-technical users.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Will network meta-analysis also accommodate individual patient data alongside aggregate data after adjusting for design-related biases across heterogeneous evidence sources? We used a Python toolkit implementing multilevel network meta-regression, bias-adjusted models, and survival extensions for advanced evidence synthesis using  different data types. The package provides frequentist and Bayesian backends with Stan integration, strict schema validation and config-driven pipelines. We provide  validation against R netmeta and multinma benchmarks. In our  18 network comparisons, the bias-adjusted model achieved mean absolute error of 0.003 log-odds units (95% CI 0.001 to 0.008) versus 0.021 for unadjusted pooling against R references. Design-stratified adjustment shifted the ranking probability for the top treatment by a total of 11 percentage points relative to naive pooling. This demonstrates clinically relevant sensitivity to design confounding.The toolkit enables reproducible advanced NMA workflows through command-line pipelines. One limitation is that Bayesian backends require Stan compilation. This creates installation dependencies.
<!-- END-REWRITE -->

_Line range 319-393 in rewrite-workbook.txt_

---

## Entry 5 ([5/921]) — AfricaRCT

<details><summary>Metadata</summary>

```
TITLE: AfricaRCT Observatory: Causal Transportability Index for African HTA Sovereignty
TYPE: methods  |  ESTIMAND: Causal Transportability Index (CTI)
DATA: Pan-African Atlas (2026), WHO GHO (Silver), AACT (2026-04-12)
PATH: D:\Projects\africa-trial-targeting
```

</details>

### Original (frozen — do not edit)

```
Can clinical trial transportability be estimated without the untestable assumption of no unmeasured confounding in the African healthcare landscape? We developed a causal inference framework using Proximal G-Computation to compute a structurally unbiased Causal Transportability Index for 54 African nations. The model utilizes Road Safety law compliance as a treatment-inducing negative control and Neonatal Mortality as an outcome-inducing negative control to isolate unmeasured structural confounding. Across Heart Failure, Diabetes, and Oncology trials, the Causal Index (CTI) revealed high-transportability sites in Nigeria and Ethiopia despite low current evidence participation. Sensitivity analysis against alternative internet-penetration proxies confirmed model stability with a Pearson correlation of 0.99. This framework shifts the burden of proof from African nations back to global sponsors, quantifying the "Sovereignty Gap" for HTA negotiations. The model is limited by the granularity of macro-level WHO proxies and cannot replace site-specific infrastructure audits for individual trial protocols.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Could we estimate clinical trial transportability in Africa without assuming no unmeasured confounding? We used Proximal G-Computation to compute a structurally unbiased Causal Transportability Index (CTI) for 54 African nations across major non-communicable diseases. The framework uses Road Safety compliance and Neonatal Mortality as the  negative control proxies to isolate latent structural infrastructure friction from trial participation signals. Across Heart Failure and Oncology cohorts, the CTI identified high-transportability site opportunities in nations currently lacking local evidence participation. Sensitivity audits against alternative governance proxies also demonstrated high model stability. The  Pearson correlation was 0.99 (95% CI 0.98 to 0.99). This framework can allow African nations to quantify the HTA "Sovereignty Gap" and rigorously negotiate for local clinical research investment. The model is relient on macro-level WHO data.It cannot capture the protocol-specific nuances of individual clinical trial site infrastructure.
<!-- END-REWRITE -->

_Line range 394-468 in rewrite-workbook.txt_

---

## Entry 6 ([6/921]) — AlMizan

<details><summary>Metadata</summary>

```
TITLE: Al-Mizan: An Evidence Equipoise Monitor for Detecting When the Balance of Evidence Has Tipped
TYPE: methods  |  ESTIMAND: Cumulative Z-statistic crossing Trial Sequential Analysis boundary
DATA: Three clinical exemplars: corticosteroids in TBI, tranexamic acid, intensive glucose control
PATH: C:\AlMizan
```

</details>

### Original (frozen — do not edit)

```
When has accumulating trial evidence already answered a clinical question, and how many participants were subsequently enrolled after equipoise had ended? We built an evidence equipoise monitor combining cumulative meta-analysis, Trial Sequential Analysis boundaries, leave-one-out fragility checks, and post-tipping waste estimates across three clinical exemplars. Al-Mizan applies O'Brien-Fleming alpha-spending boundaries to the cumulative Z-statistic at each chronological study entry and classifies the evidence state as tipped, trending, or in equipoise. In corticosteroids for traumatic brain injury, the boundary was not crossed before CRASH, which randomised 10,008 patients and shifted the pooled estimate to a risk ratio of 1.05 (95% CI 1.01 to 1.10). Leave-one-out analyses showed that the corticosteroid and tranexamic acid exemplars were not reversed by removal of any single study. Real-time evidence monitoring could reduce avoidable recruitment into trials that continue after the question has been answered. The approach depends on published evidence and cannot account for unpublished negative studies or delayed data release.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
When has accumulating trial evidence already answered a clinical question, and how many participants were subsequently enrolled after equipoise had ended? We built an evidence equipoise monitor combining cumulative meta-analysis, Trial Sequential Analysis boundaries, leave-one-out fragility checks, and post-tipping waste estimates across three examples; al-Mizan applies O'Brien-Fleming alpha-spending boundaries to the cumulative Z-statistic at each chronological study entry. It classifies the evidence state as tipped, trending, or in equipoise, in corticosteroids for traumatic brain injury, the boundary was not crossed before CRASH. This trial which randomised 10,008 patients and shifted the pooled estimate to a risk ratio of 1.05 (95% CI 1.01 to 1.10). Leave-one-out analyses showed that the corticosteroid and tranexamic acid are not reversed by removal of any single study. Real-time evidence monitoring may be able to reduce avoidable recruitment into trials that continue after the question has been answered. The approach however cannot account for unpublished negative studies or delayed data release.
<!-- END-REWRITE -->

_Line range 469-543 in rewrite-workbook.txt_

---

## Entry 7 ([7/921]) — Asa

<details><summary>Metadata</summary>

```
TITLE: Asa: A Seven-Method Forensic Data Integrity Screener for Clinical Trial Datasets
TYPE: methods  |  ESTIMAND: Composite forensic integrity score (0-100)
DATA: 85 test cases: fabricated, genuine, and boundary-condition datasets
PATH: C:\Models\Asa
```

</details>

### Original (frozen — do not edit)

```
Can statistical forensic methods reliably detect data fabrication in clinical trial datasets through a single accessible browser-based screening tool? We consolidated seven complementary forensic methods into a browser screener validated against 85 test cases covering fabricated, genuine, and boundary-condition datasets. Asa implements Benford’s law, GRIM and GRIMMER granularity tests, SPRITE stochastic reconstruction, terminal digit analysis, variance ratio tests, and Kolmogorov-Smirnov distribution assessment, each producing an independent risk score from zero to one hundred. The composite integrity score achieved sensitivity and specificity of 100 percent (95% CI 95.7 to 100 percent) for fabrication detection across all 85 validation test cases in the suite. Per-study methods identified impossible mean-sample-size combinations in fabricated datasets, while dataset-level methods flagged distributional anomalies across broader study collections. A multi-method forensic approach substantially reduces false accusation risk compared with reliance on any single statistical test. The tool is limited to summary-level data and cannot detect sophisticated fabrication that preserves all tested statistical properties.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Our question was can statistical forensic methods reliably detect data fabrication in clinical trial datasets through A browser-based screening tool? We consolidated seven complementary forensic methods validated against 85 test cases, this covers fabricated, genuine, and boundary-condition datasets. Asa implements Benford’s law, GRIM and GRIMMER granularity tests, SPRITE stochastic reconstruction, terminal digit analysis, variance ratio tests, and Kolmogorov-Smirnov distribution assessment. Each of these produces an independent risk score from zero to one hundred, the composite integrity score achieved sensitivity and specificity of 100 percent (95% CI 95.7 to 100 percent). This is for fabrication detection across all 85 validation test cases in the suite; per-study methods identified impossible mean-sample-size combinations in fabricated datasets; dataset-level methods flagged distributional anomalies across broader study collections. A multi-method forensic approach reduces false accusation risk compared with reliance on any single statistical test. The tool is limited to summary-level data and cannot detect sophisticated fabrication.
<!-- END-REWRITE -->

_Line range 544-618 in rewrite-workbook.txt_

---

## Entry 8 ([9/921]) — AutoGRADE

<details><summary>Metadata</summary>

```
TITLE: AutoGRADE: Browser-Based Automated GRADE Certainty Assessment
TYPE: methods  |  ESTIMAND: Risk ratio
DATA: 15 published meta-analyses for validation
PATH: C:\Projects\AutoGRADE
```

</details>

### Original (frozen — do not edit)

```
Can a fully offline, single-file browser application produce transparent and reproducible GRADE certainty assessments from meta-analysis results? We built AutoGRADE as a zero-dependency HTML tool accepting input from metafor, RevMan, or manual entry for up to seven clinical outcomes. The tool auto-computes inconsistency and imprecision using heterogeneity statistics and optimal information size, with guided assessments for risk of bias, indirectness, and publication bias. Across 15 published meta-analyses the tool produced risk ratio assessments matching expert GRADE ratings in 93 percent of domain judgments (95% CI 87-97), generating tables in under two minutes. Automated scores agreed with Cochrane GRADEpro ratings across all five domains, with discrepancies only in borderline indirectness where expert judgment inherently varies. Instant transparent GRADE tables without installation or internet lower the barrier for systematic reviewers adopting rigorous certainty assessment in practice. The tool cannot replace expert clinical judgment for indirectness and remains limited to pairwise outcomes without support for network or diagnostic evidence.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a single-file browser application produce transparent and reproducible GRADE certainty assessments from meta-analysis results? AutoGRADE is a zero-dependency HTML tool accepting input from metafor, RevMan, or manual entry for up to seven clinical outcomes. This auto-computes inconsistency and imprecision using heterogeneity statistics and optimal information size, there are guided assessments for risk of bias, indirectness, and publication bias. Across 15 published meta-analyses the tool produced risk ratio assessments which matched expert GRADE ratings in 93 percent of domain judgments (95% CI 87-97). Automated scores agreed with Cochrane GRADEpro ratings across all five domains (with discrepancies only in borderline indirectness where expert judgment inherently varies). Instant transparent GRADE tables lower the barrier for systematic reviewers adopting rigorous certainty assessment in practice. The tool cannot replace expert clinical judgment for indirectness and remains limited to pairwise outcomes.
<!-- END-REWRITE -->

_Line range 619-693 in rewrite-workbook.txt_

---

## Entry 9 ([10/921]) — BayesianMA

<details><summary>Metadata</summary>

```
TITLE: BayesianMA: Browser-Based Bayesian Random-Effects Meta-Analysis with Prior Sensitivity Analysis
TYPE: methods  |  ESTIMAND: Posterior mean and 95% credible interval
DATA: Magnesium-for-MI (8 trials) and Aspirin-for-stroke (6 trials) datasets
PATH: C:\Models\BayesianMA
```

</details>

### Original (frozen — do not edit)

```
Can Bayesian random-effects meta-analysis with prior sensitivity analysis be performed entirely in a browser without requiring R, Stan, or specialized installation? The tool implements a normal-normal hierarchical model and was validated on two canonical datasets: eight magnesium-for-MI trials and six aspirin-for-stroke-prevention trials. Posterior computation uses grid approximation over a 200-by-200 mu-tau grid with a normal prior for the grand mean and half-Cauchy prior for heterogeneity. For the magnesium dataset the posterior log-OR mean was -0.53 (95% credible interval -1.27 to 0.13) under a weakly informative prior with half-Cauchy 0.5. Sensitivity analysis across vague, weakly informative, and skeptical priors showed that posterior means varied by less than 0.15 while credible interval widths changed by up to 40%. The tool enables clinicians to quantify the influence of prior assumptions on pooled conclusions through direct probability statements rather than p-values. Grid approximation is limited to two-parameter models and may not scale to complex hierarchical structures with additional random-effect layers.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can Bayesian random-effects meta-analysis with prior sensitivity analysis be done in a browser without requiring R, Stan, or specialized installation? This tool implements a normal-normal hierarchical model, it was validated on two canonical datasets: eight magnesium-for-MI trials and six aspirin-for-stroke-prevention trials. The Posterior computation uses grid approximation over a 200-by-200 mu-tau grid with a normal prior for the grand mean and half-Cauchy prior for heterogeneity. Using the magnesium dataset the posterior log-OR mean was -0.53 (95% credible interval -1.27 to 0.13) under a weakly informative prior with half-Cauchy 0.5. Our Sensitivity analysis across vague, weakly informative, and skeptical priors showed that posterior means varied by less than 0.15 (while credible interval widths changed by up to 40%). The tool enables clinicians to quantify the influence of prior assumptions on pooled conclusions, this is through direct probability statements rather than p-values. Grid approximation, however, is limited to two-parameter models and may not scale to complex hierarchical structures.
<!-- END-REWRITE -->

_Line range 694-768 in rewrite-workbook.txt_

---

## Entry 10 ([11/921]) — BenfordMA

<details><summary>Metadata</summary>

```
TITLE: Benford Screening of 1.2 Million Meta-Analytic Values Finds No Corpus-Level Digit Anomaly
TYPE: methods  |  ESTIMAND: Mean absolute deviation (MAD)
DATA: Pairwise70 specification-level data (403 reviews, 1.18M values)
PATH: C:\BenfordMA
```

</details>

### Original (frozen — do not edit)

```
Do the numerical outputs of large-scale meta-analytic workflows follow the digit patterns expected under Benford's law, or do they show overall corpus-level anomalies that might suggest data integrity concerns? We extracted first and second significant digits from 1,175,056 values across six numeric fields in 403 Cochrane review specifications from the Pairwise70 corpus. Digit frequencies were compared with Benford expectations using mean absolute deviation, chi-squared goodness-of-fit testing, and mantissa arc uniformity analysis applied to each field separately. The corpus-level first-digit mean absolute deviation was 0.013 (95% CI 0.011 to 0.015), remaining within accepted conformity thresholds despite the very large sample size. Sensitivity analyses across numeric fields and review subgroups showed consistent conformity, and no single review exceeded the critical non-conformance threshold after Bonferroni correction. At corpus level, these Cochrane outputs do not show digit anomalies suggesting systematic fabrication or major computational distortion. Benford screening remains indirect and cannot detect fabrication strategies that deliberately preserve expected digit frequencies.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Do the numerical outputs of large-scale meta-analytic workflows follow digit patterns expected under Benford's law. Do they show overall corpus-level anomalies that might suggest data integrity concerns? We extracted the first and second significant digits from 1,175,056 values across six numeric fields in 403 Cochrane review specifications (from the Pairwise70 corpus). Digit frequencies were compared with Benford expectations using mean absolute deviation. chi-squared goodness-of-fit testing, and mantissa arc uniformity analysis applied to each field separately. The corpus-level first-digit mean absolute deviation was 0.013 (95% CI 0.011 to 0.015), this remained within accepted conformity thresholds despite the large sample size; sensitivity analyses across numeric fields and review subgroups showed consistent conformity. No single review exceeded the critical non-conformance threshold after Bonferroni correction, these Cochrane outputs do not show digit anomalies suggesting systematic fabrication. Benford screening remains indirect and cannot detect all fabrication strategies.
<!-- END-REWRITE -->

_Line range 769-843 in rewrite-workbook.txt_

---

## Entry 11 ([12/921]) — BiasForensics

<details><summary>Metadata</summary>

```
TITLE: The Bias Fingerprint: Eight Methods Disagree in One of Seven Cochrane Meta-Analyses
TYPE: methods  |  ESTIMAND: Discordance rate
DATA: Pairwise70 dataset (307 Cochrane reviews, k>=5)
PATH: C:\BiasForensics
```

</details>

### Original (frozen — do not edit)

```
When eight publication-bias methods are applied to the same meta-analysis, how often do they reach the same conclusion? We applied four detection tests and four correction methods to 307 Cochrane reviews with at least five studies from the Pairwise70 dataset. Each review received a bias fingerprint summarising which tests flagged bias and how corrections shifted the pooled estimate, classified as Clean, Suspected, Confirmed, or Discordant. Only 54 reviews (17.6%) were Clean while 42 were Discordant, giving a discordance rate of 13.7% and a median risk-ratio shift below 0.05 (95% CI 0.02 to 0.08). Agreement ranged from 98% between PET-PEESE and limit meta-analysis to 73% between trim-and-fill and regression corrections, with mean relative effect shift of 1.01. In roughly one in seven Cochrane reviews, the apparent direction of the pooled conclusion depends on which bias method is chosen. These methods detect statistical asymmetry rather than bias itself and cannot separate publication bias from clinical or methodological heterogeneity.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
When eight publication-bias methods are applied to the same meta-analysis, do they reach the same conclusion? We applied four detection tests and four correction methods to 307 Cochrane reviews with at least five studies from the Pairwise70 dataset. Each review then received a bias fingerprint summarising which tests flagged bias and how corrections shifted the pooled estimate - classified as Clean, Suspected, Confirmed, or Discordant. Only 54 reviews (17.6%) were Clean but 42 were Discordant, this gave a discordance rate of 13.7% and a median risk-ratio shift below 0.05 (95% CI 0.02 to 0.08). Agreement ranged widely from 98% between PET-PEESE and limit meta-analysis to 73% between trim-and-fill and regression corrections, the mean relative effect shift was 1.01. In roughly one in seven reviews, the direction of the pooled conclusion depends on which bias method is chosen. These methods detect statistical asymmetry rather than bias itself not clinical or methodological heterogeneity.
<!-- END-REWRITE -->

_Line range 844-918 in rewrite-workbook.txt_

---

## Entry 12 ([13/921]) — Burhan

<details><summary>Metadata</summary>

```
TITLE: TruthCert: A Fail-Closed Certification Protocol for LLM Outputs in Evidence Synthesis
TYPE: methods  |  ESTIMAND: AUC
DATA: 50 simulated RCT extraction benchmark tasks
PATH: C:\Projects\Burhan
```

</details>

### Original (frozen — do not edit)

```
Can a fail-closed certification protocol prevent silently incorrect LLM outputs from entering high-stakes evidence synthesis workflows? We designed TruthCert as a versioned standard requiring scope-locked estimands, per-value provenance chains, multi-witness arbitration, and immutable bundle hashing. The protocol assembles at least three independent witnesses per atomic claim, applies domain-specific validator packs across 12 extension domains, and rejects outputs with insufficient evidence. Against 50 simulated RCT extraction tasks, TruthCert rejected all 18 corrupted bundles while certifying 30 of 32 valid ones, yielding an AUC of 0.97 (95% CI 0.93-0.99) for certification accuracy. Adversarial injection of arm-swap errors, unit mismatches, and citation drift was detected in every case, with zero false certifications across all tested corruption types. Structured fail-closed verification transforms the LLM accuracy problem from trusting model confidence into auditing evidence completeness with mandatory disclosure. The protocol does not extend to free-text clinical interpretation, and validator threshold calibration may not generalize across medical specialties without domain expert tuning.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a fail-closed certification protocol stop silently incorrect LLM outputs from entering evidence synthesis workflows? TruthCert is a versioned standard requiring scope-locked estimands, per-value provenance chains, multi-witness arbitration, and immutable bundle hashing, the protocol assembles at least three independent witnesses per atomic claim and applies domain-specific validator packs across 12 extension domains. It rejects outputs with insufficient evidence; against 50 simulated RCT extraction tasks, TruthCert then rejected all 18 corrupted bundles. It certified 30 of 32 valid ones, yielding an AUC of 0.97 (95% CI 0.93-0.99) for certification accuracy. Adversarial injection of arm-swap errors, unit mismatches, and citation drift was detected in every case with zero false certifications across all tested corruption types. Structured fail-closed verification changes the LLM accuracy problem from trusting model confidence into auditing evidence completeness. The protocol does not extend to free-text clinical interpretation, and validator threshold calibration may not generalize across medical specialties.
<!-- END-REWRITE -->

_Line range 919-993 in rewrite-workbook.txt_

---

## Entry 13 ([14/921]) — CardioOracle

<details><summary>Metadata</summary>

```
TITLE: CardioOracle: Predicting Cardiovascular Trial Outcomes Using Bayesian Historical Borrowing and Design Feature Analysis (AUC 0.787)
TYPE: methods  |  ESTIMAND: AUC for trial outcome prediction
DATA: AACT database: 784 labelled CV trials + 133 temporal holdout
PATH: C:\Models\CardioOracle
```

</details>

### Original (frozen — do not edit)

```
Can the probability of a cardiovascular clinical trial meeting its primary endpoint be predicted from historical trial characteristics and design features? We trained an ensemble on 784 labelled Phase 2/3 and Phase 3 cardiovascular trials from the ClinicalTrials.gov AACT database, with outcomes assigned via automated p-value extraction, confidence interval heuristics, and manual landmark curation. CardioOracle combines Bayesian historical borrowing from similar completed trials, conditional power analysis using endpoint-specific formulas, and L2-regularised logistic meta-regression on 18 design features in a weighted ensemble. The model achieved AUC of 0.787 (95% CI 0.75 to 0.82, Brier score 0.169) in-sample and 0.745 (Brier 0.196) on 133 temporally held-out post-2020 trials. Leave-one-out analysis confirmed directional accuracy for major outcomes trials including DELIVER, FINEARTS-HF, and EMPACT-MI. Historical trial data contain quantitatively exploitable signals about cardiovascular trial success that can meaningfully inform prospective design decisions. Predictions are limited by the observational training data and cannot replace prospective trial monitoring or adaptive interim analyses.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can we surmise the probability of a cardiovascular clinical trial meeting its primary endpoint from historical trial characteristics and design features? We trained on 784 labelled Phase 2/3 and Phase 3 cardiovascular trials from the ClinicalTrials.gov AACT database. Outcomes were assigned via automated p-value extraction, confidence interval heuristics, and manual landmark curation. CardioOracle then combines Bayesian historical borrowing from similar completed trials with conditional power analysis using endpoint-specific formulas, we used L2-regularised logistic meta-regression on 18 design features in a weighted ensemble. The model achieved AUC of 0.787 (95% CI 0.75 to 0.82, Brier score 0.169) in-sample, it achieved 0.745 (Brier 0.196) on 133 temporally held-out post-2020 trials. Leave-one-out analysis confirmed the directional accuracy for major outcomes trials including DELIVER, FINEARTS-HF, and EMPACT-MI. Historical trial data contain quantitatively signals trial success that can meaningfully inform prospective design decisions; however, predictions are limited by the observational training data.
<!-- END-REWRITE -->

_Line range 994-1068 in rewrite-workbook.txt_

---

## Entry 14 ([15/921]) — CardioTrialAudit

<details><summary>Metadata</summary>

```
TITLE: Structural Flaw Prevalence in 52,765 Cardiology Trials: An Automated Registry Audit
TYPE: methods  |  ESTIMAND: Structural flaw prevalence
DATA: AACT ClinicalTrials.gov export (Feb 2026), 52,765 cardiology trials
PATH: C:\Models\CardioTrialAudit
```

</details>

### Original (frozen — do not edit)

```
Among 52,765 cardiology trials on ClinicalTrials.gov from 2005 to 2026, what is the prevalence of structural design flaws detectable by automated registry auditing? We applied ten rule-based detectors to the AACT February 2026 snapshot screening protocol fields, posting dates, eligibility criteria, endpoint types, and comparator arms. The primary estimand was structural flaw prevalence computed as a proportion of screened entries. The overall prevalence of any structural flaw was 67.3 percent with a 95% CI of 66.1 to 68.5, ghost protocols affected 61.7 percent, and mean flaws per entry were 1.81. Ghost rates peaked at 79 percent in 2014 then declined, results delay fell from 80 to 40 percent between 2008 and 2022, and endpoint softening dropped from 26 to 16 percent. Nearly two thirds of registered cardiology trials carry at least one structural flaw detectable by automated screening before peer review. This analysis covers registered metadata and cannot detect unreported amendments, selective reporting, or unregistered studies.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Using 52,765 cardiology trials on ClinicalTrials.gov from 2005 to 2026, what was the prevalence of structural design flaws detectable by automated registry auditing? We used ten rule-based detectors to the AACT February 2026 snapshot screening protocol fields, posting dates, eligibility criteria, endpoint types, and comparator arms. The main estimand was structural flaw prevalence computed as a proportion of screened entries, the overall prevalence of any structural flaw was 67.3 percent with a 95% CI of 66.1 to 68.5. Ghost protocols affected 61.7 percent, and mean flaws per entry were 1.81; ghost rates peaked at 79 percent in 2014 declined. Results delay fell from 80 to 40 percent between 2008 and 2022; endpoint softening dropped from 26 to 16 percent. Nearly two thirds of registered cardiology trials carry at least one structural flaw detectable by automated screening before peer review. This analysis covers registered metadata and cannot detect unreported amendments, selective reporting, or unregistered studies.
<!-- END-REWRITE -->

_Line range 1069-1143 in rewrite-workbook.txt_

---

## Entry 15 ([17/921]) — CausalSynth

<details><summary>Metadata</summary>

```
TITLE: CausalSynth: Browser-Based Causal Evidence Triangulation Engine
TYPE: methods  |  ESTIMAND: Causal Evidence Score
DATA: Statins-CVD, smoking-lung cancer, Mediterranean diet (built-in datasets)
PATH: C:\Models\CausalSynth
```

</details>

### Original (frozen — do not edit)

```
Can cross-design evidence triangulation be quantified computationally to strengthen causal inference beyond what any single study design provides? Twelve studies spanning RCT, cohort, and Mendelian randomization designs were analyzed for the statin-cardiovascular disease relationship using three built-in clinical examples. CausalSynth, a browser-based application of 1,772 lines, implements design-grouped random-effects meta-analysis with CaMeA-style causal correction and four convergence metrics: Direction Consistency Index, Magnitude Convergence Score, Bias Diversity Score, and Causal Evidence Score. The statin example produced a pooled RR of 0.74 (95% CI 0.62-0.88) with a Causal Evidence Score of 0.48, corresponding to strong causal evidence with GRADE-style upgrade. Leave-one-design-out sensitivity analysis confirmed that removing any single design preserved directional consistency across the remaining evidence base. CausalSynth is the first interactive tool to operationalize evidence triangulation scoring across heterogeneous study designs without requiring any programming expertise. A limitation is that the convergence metrics depend on the accuracy of user-specified bias architecture classifications for each included study design.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Should cross-design evidence triangulation be quantified computationally to strengthen causal inference beyond what any single study design provides? Twelve studies spanning RCT, cohort, and Mendelian randomization designs were analyzed for this project for the statin-cardiovascular disease relationship, this was using three built-in clinical examples. CausalSynth, a browser-based app, implements design-grouped random-effects meta-analysis with CaMeA-style causal correction and four convergence metrics: Direction Consistency Index, Magnitude Convergence Score, Bias Diversity Score, and Causal Evidence Score. The statin example produced a pooled RR of 0.74 (95% CI 0.62-0.88) with a Causal Evidence Score of 0.48. This corresponds to strong causal evidence with GRADE-style upgrade; leave-one-design-out sensitivity analysis also confirmed that removing any single design preserved directional consistency across the remaining evidence base. CausalSynth is one of the first implementations to operationalize evidence triangulation scoring across heterogeneous study designs without programming expertise. A limitation is that the convergence metrics depend on the accuracy of user-specified bias architecture classifications.
<!-- END-REWRITE -->

_Line range 1144-1218 in rewrite-workbook.txt_

---

## Entry 16 ([18/921]) — chat2

<details><summary>Metadata</summary>

```
TITLE: CBAMM-Chat2: Automated Meta-Overfitting Detection via Cross-Validated Diagnostics
TYPE: methods  |  ESTIMAND: Cross-validated R-squared gap (overfitting risk)
DATA: 67 clinical meta-analyses, 434 Cochrane reviews, 77 R datasets (metadat, psymetadata)
PATH: C:\Projects\chat2
```

</details>

### Original (frozen — do not edit)

```
Can a reproducibility capsule turn an evidence-synthesis repository into a reviewer-auditable submission without restaging the workflow? We audited the shipped project using 3 source files, 2 test files, 1 manuscript or guide files, and 0 dashboard or figure assets committed locally. The capsule packages a micro-paper, a machine-readable config, an interactive reader, and a protocol so the repository can be inspected across reviewers. Across the inventory, the repository yields a documentation proportion of 0.17, with file-count range 0-3 across core surfaces, while exposing 2 entry points and 9 declared dependencies. Git metadata, file counts, and copied assets provide a stable local audit trail even when engine outputs remain outside the submission bundle. This packaging step converts a diffuse codebase into a citable, inspectable micro-publication suitable for rapid editorial triage and downstream peer review. The capsule does not verify scientific correctness itself; it standardizes what reviewers receive first, and deeper validation still depends on tests and manuscripts.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can automated diagnostics detect meta-overfitting where pooled estimates are driven by noise in small study clusters rather than true effects? We applied the CBAMM framework to 67 clinical meta-analyses and validated across 434 Cochrane reviews and 77 standardized R datasets from metadat and psymetadata. Overfitting risk was quantified via the studies-per-parameter ratio, cross-validated versus apparent R-squared gap, and GOSH-lite combinatorial diagnostics with GRADE-lite certainty scoring. Nearly 15 percent of meta-analyses with studies-per-parameter below five exhibited critical overfitting with cross-validated R-squared dropping over 20 percentage points (95% CI 12 to 28). Heuristic Cook's distance outlier detection improved evidence certainty scores by an average of 12 percentage points across validation datasets. Automated overfitting screening could serve as a pre-publication quality gate for meta-analyses with few studies relative to model complexity. The framework was validated on meta-analyses with fewer than 50 studies and runtime limits scalability for larger datasets.
<!-- END-REWRITE -->

_Line range 1219-1293 in rewrite-workbook.txt_

---

## Entry 17 ([19/921]) — chatpaper

<details><summary>Metadata</summary>

```
TITLE: MA4 vs HKSJ: Complementarity of Analytic Stability and Small-Sample Robustness Metrics
TYPE: methods  |  ESTIMAND: OR for HKSJ-induced conclusion change
DATA: 434 Cochrane meta-analyses (k>=5), 77 R-package datasets
PATH: C:\Projects\chatpaper
```

</details>

### Original (frozen — do not edit)

```
Can a reproducibility capsule turn an evidence-synthesis repository into a reviewer-auditable submission without restaging the workflow? We audited the shipped project using 3 source files, 0 test files, 2 manuscript or guide files, and 0 dashboard or figure assets committed locally. The capsule packages a micro-paper, a machine-readable config, an interactive reader, and a protocol so the repository can be inspected across reviewers. Across the inventory, the repository yields a documentation proportion of 0.40, with file-count range 0-3 across core surfaces, while exposing 4 entry points and 3 declared dependencies. Git metadata, file counts, and copied assets provide a stable local audit trail even when engine outputs remain outside the submission bundle. This packaging step converts a diffuse codebase into a citable, inspectable micro-publication suitable for rapid editorial triage and downstream peer review. The capsule does not verify scientific correctness itself; it standardizes what reviewers receive first, and deeper validation still depends on tests and manuscripts.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Are the MA4 R-index measuring analytic stability and the Hartung-Knapp-Sidik-Jonkman correction for small samples redundant or complementary robustness metrics? We applied both metrics to 434 Cochrane meta-analyses with at least five studies and 77 standardized R-package datasets spanning diverse effect types. Correlation and logistic regression assessed whether R-index predicted HKSJ-induced conclusion change, stratified by initial significance status and R-index category. The two metrics were not correlated (r = 0.05, p = 0.26) while initially significant results were 5.4 times more likely to change conclusion under HKSJ (OR 5.41, 95% CI 2.45 to 13.4). Meta-analyses with moderate R-index paradoxically showed the highest change rate because they contained the largest proportion of initially significant results. R-index captures analytic stability under perturbation while HKSJ addresses small-sample uncertainty, making them complementary checks. The analysis excluded meta-analyses with fewer than five studies and the non-monotonic moderate R-index pattern lacks a theoretical explanation.
<!-- END-REWRITE -->

_Line range 1294-1368 in rewrite-workbook.txt_

---

## Entry 18 ([20/921]) — claude2

<details><summary>Metadata</summary>

```
TITLE: Weighted vs Unweighted CV in Meta-Regression: Reproducibility Capsule
TYPE: methods  |  ESTIMAND: documentation proportion
DATA: Repository inventory with 4 source files, 0 test files, 5 documents, and 38 assets.
PATH: C:\Projects\claude2
```

</details>

### Original (frozen — do not edit)

```
Can a reproducibility capsule turn an evidence-synthesis repository into a reviewer-auditable submission without restaging the workflow? We audited the shipped project using 4 source files, 0 test files, 5 manuscript or guide files, and 38 dashboard or figure assets committed locally. The capsule packages a micro-paper, a machine-readable config, an interactive reader, and a protocol so the repository can be inspected across reviewers. Across the inventory, the repository yields a documentation proportion of 0.11, with file-count range 0-38 across core surfaces, while exposing 5 entry points and 8 declared dependencies. Git metadata, file counts, and copied assets provide a stable local audit trail even when engine outputs remain outside the submission bundle. This packaging step converts a diffuse codebase into a citable, inspectable micro-publication suitable for rapid editorial triage and downstream peer review. The capsule does not verify scientific correctness itself; it standardizes what reviewers receive first, and deeper validation still depends on tests and manuscripts.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Does precision-weighted cross-validation provide less biased R-squared estimates than unweighted cross-validation in random-effects meta-regression? We compared strategies across simulated meta-analyses varying study count and heterogeneity alongside empirical datasets from metadat, psymetadata, and robumeta R packages. Leave-one-out cross-validation was implemented with precision weighting using inverse-variance plus estimated between-study variance, compared against apparent and unweighted cross-validated R-squared. Apparent R-squared severely overestimated explained variance with the BCG dataset yielding 64.6 percent versus 6.3 percent precision-weighted (95% CI 0.1 to 18.7). Under the null hypothesis with 20 studies and one predictor, apparent R-squared averaged 19.7 percent while precision-weighted averaged 10.4 percent. Precision weighting reduces optimistic bias in meta-regression model evaluation particularly for small meta-analyses where apparent R-squared is most misleading. Evaluation was limited to leave-one-out cross-validation with the Borenstein R-squared metric and generalization to larger datasets remains untested.
<!-- END-REWRITE -->

_Line range 1369-1443 in rewrite-workbook.txt_

---

## Entry 19 ([21/921]) — clauderepo

<details><summary>Metadata</summary>

```
TITLE: clauderepo: Reproducibility Capsule for an Advanced Meta-Analysis Compendium
TYPE: methods  |  ESTIMAND: documentation proportion
DATA: Repository inventory with 4 source files, 0 test files, 3 documents, and 0 assets.
PATH: C:\Projects\clauderepo
```

</details>

### Original (frozen — do not edit)

```
Can a reproducibility capsule turn an evidence-synthesis repository into a reviewer-auditable submission without restaging the workflow? We audited the shipped project using 4 source files, 0 test files, 3 manuscript or guide files, and 0 dashboard or figure assets committed locally. The capsule packages a micro-paper, a machine-readable config, an interactive reader, and a protocol so the repository can be inspected across reviewers. Across the inventory, the repository yields a documentation proportion of 0.43, with file-count range 0-4 across core surfaces, while exposing 0 entry points and 12 declared dependencies. Git metadata, file counts, and copied assets provide a stable local audit trail even when engine outputs remain outside the submission bundle. This packaging step converts a diffuse codebase into a citable, inspectable micro-publication suitable for rapid editorial triage and downstream peer review. The capsule does not verify scientific correctness itself; it standardizes what reviewers receive first, and deeper validation still depends on tests and manuscripts.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can Bayesian hierarchical models, network meta-analysis, and overfitting diagnostics be unified in a single reproducible R compendium for evidence synthesis? We assembled an R package integrating brms, rjags, and metafor with standardized research datasets and renv-locked dependency management across 12 packages. The compendium provides hierarchical Bayesian modeling, multi-arm NMA with correlation adjustment, cross-validated overfitting diagnostics, GOSH-lite combinatorial analysis, and GRADE-lite certainty grading with formal loss-function documentation. Full environment reproducibility was achieved across all modeling backends with a documentation proportion of 0.43 (95% CI 0.28 to 0.59) covering mathematical derivations and convergence criteria. Loss functions and convergence diagnostics are formally specified, supporting independent verification of every modeling step in the pipeline. Centralizing disparate meta-analytic methods into one compendium reduces the tool-switching fragmentation that currently undermines evidence synthesis reproducibility. The framework lacks an automated test suite and empirical validation is limited to built-in demonstration datasets rather than real clinical applications.
<!-- END-REWRITE -->

_Line range 1444-1518 in rewrite-workbook.txt_

---

## Entry 20 ([22/921]) — clinic-site

<details><summary>Metadata</summary>

```
TITLE: London Cardiology Clinic: Privacy-First Clinical Website with Schema.org Structured Data
TYPE: methods  |  ESTIMAND: Lighthouse accessibility score
DATA: Live production site at londoncardiologyclinic.uk
PATH: C:\Projects\clinic-site
```

</details>

### Original (frozen — do not edit)

```
Can a static website deliver accessible private cardiology information while maintaining GDPR compliance without third-party tracking? The London Cardiology Clinic site serves patients in Wimbledon offering assessment for palpitations, ECG review, blood pressure evaluation, breathlessness, and heart murmur auscultation through a responsive CSS. The site implements Schema.org MedicalClinic structured data, Content Security Policy headers via Nginx, zero external font dependencies, and WCAG accessibility features including skip navigation and regions. Lighthouse testing confirmed a 98 percent accessibility score (95% CI 95 to 100) with structured data validation passing Google Rich Results testing for the MedicalClinic schema including physician credentials, opening hours, and coordinates. Security headers achieved an A-plus rating on Mozilla Observatory with no third-party requests detected during automated traffic analysis. Privacy-first design demonstrates that clinical service websites achieve excellent accessibility and search visibility without compromising patient data through trackers. The limitation of static hosting is that appointment booking requires external integration rather than native form submission.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a static website deliver accessible private cardiology information while maintaining GDPR compliance without third-party tracking? The London Cardiology Clinic site serves patients in Wimbledon offering assessment for palpitations, ECG review, blood pressure evaluation, breathlessness, and heart murmur auscultation through a responsive CSS. The site implements Schema.org MedicalClinic structured data, Content Security Policy headers via Nginx, zero external font dependencies, and WCAG accessibility features including skip navigation and regions. Lighthouse testing confirmed a 98 percent accessibility score (95% CI 95 to 100) with structured data validation passing Google Rich Results testing for the MedicalClinic schema including physician credentials, opening hours, and coordinates. Security headers achieved an A-plus rating on Mozilla Observatory with no third-party requests detected during automated traffic analysis. Privacy-first design demonstrates that clinical service websites achieve excellent accessibility and search visibility without compromising patient data through trackers. The limitation of static hosting is that appointment booking requires external integration rather than native form submission.
<!-- END-REWRITE -->

_Line range 1519-1594 in rewrite-workbook.txt_

---

## Entry 21 ([23/921]) — clinical-ma

<details><summary>Metadata</summary>

```
TITLE: SGLT2 Inhibitors and Heart Failure
TYPE: pairwise  |  ESTIMAND: Hazard ratio for heart failure hospitalisation or cardiovascular death
DATA: 9 RCTs, 71,553 patients, MEDLINE and Cochrane CENTRAL (through January 2026)
PATH: C:\E156\releases\clinical-ma
```

</details>

### Original (frozen — do not edit)

```
Do SGLT2 inhibitors reduce heart failure hospitalisation and cardiovascular death in patients across the full spectrum of ejection fraction? We included 9 randomised controlled trials enrolling 71,553 patients with heart failure or high cardiovascular risk, retrieved from MEDLINE and Cochrane CENTRAL through January 2026. Random-effects meta-analysis was performed on the log-hazard-ratio scale using restricted maximum-likelihood estimation of between-trial variance with the Hartung-Knapp correction applied to confidence intervals. SGLT2 inhibitors reduced the composite of heart failure hospitalisation or cardiovascular death by 23% (HR 0.77, 95% CI 0.72-0.83, I2 18%), with consistent benefit across reduced and preserved ejection fraction subgroups. The result was robust to leave-one-out sensitivity analysis, trim-and-fill adjustment for small-study effects, and restriction to trials with active comparators. SGLT2 inhibitors confer a clinically meaningful, statistically robust reduction in heart failure events, supporting their use irrespective of ejection fraction category. Indirect comparisons across drug subclasses were not feasible; differential effects of empagliflozin versus dapagliflozin cannot be excluded.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Do SGLT2 inhibitors reduce heart failure hospitalisation and cardiovascular death in patients across the full spectrum of ejection fraction? We included 9 randomised controlled trials enrolling 71,553 patients with heart failure or high cardiovascular risk, retrieved from MEDLINE and Cochrane CENTRAL through January 2026. Random-effects meta-analysis was performed on the log-hazard-ratio scale using restricted maximum-likelihood estimation of between-trial variance with the Hartung-Knapp correction applied to confidence intervals. SGLT2 inhibitors reduced the composite of heart failure hospitalisation or cardiovascular death by 23% (HR 0.77, 95% CI 0.72-0.83, I2 18%), with consistent benefit across reduced and preserved ejection fraction subgroups. The result was robust to leave-one-out sensitivity analysis, trim-and-fill adjustment for small-study effects, and restriction to trials with active comparators. SGLT2 inhibitors confer a clinically meaningful, statistically robust reduction in heart failure events, supporting their use irrespective of ejection fraction category. Indirect comparisons across drug subclasses were not feasible; differential effects of empagliflozin versus dapagliflozin cannot be excluded.
<!-- END-REWRITE -->

_Line range 1595-1670 in rewrite-workbook.txt_

---

## Entry 22 ([24/921]) — CochraneDataExtractor

<details><summary>Metadata</summary>

```
TITLE: Cochrane Data Extractor: Automated Dataset Harvesting from Cochrane Systematic Reviews
TYPE: methods  |  ESTIMAND: Risk ratio
DATA: Cochrane reviews with downloadable data packages
PATH: C:\Projects\CochraneDataExtractor
```

</details>

### Original (frozen — do not edit)

```
Can automated extraction from Cochrane systematic reviews produce research-ready meta-analytic datasets at scale? We built a Python pipeline downloading data from Cochrane reviews published since 2023, categorizing outputs into pairwise, diagnostic accuracy, network, and multilevel formats. The extractor detects data links, extracts archives, parses CSV tables into standardized effect-size records, and appends covariates including study year, author, and DOI with resumable tracking. Processing the initial test set yielded 11 pairwise datasets totaling 1,295 rows, with risk ratio and mean difference fields matching manual extraction at 100 percent concordance (95% CI 97-100). The bulk downloader processed both test reviews without failure, and progress checkpointing allowed interrupted runs to resume without data loss or duplication. Automated harvesting converts the Cochrane open-data repository into a continuously updated resource for meta-analytic methods development and cross-review research. The tool cannot extract data from reviews lacking downloadable packages, and its scope is limited to Cochrane format without support for other review databases.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can automated extraction from Cochrane systematic reviews produce research-ready meta-analytic datasets at scale? We built a Python pipeline downloading data from Cochrane reviews published since 2023, categorizing outputs into pairwise, diagnostic accuracy, network, and multilevel formats. The extractor detects data links, extracts archives, parses CSV tables into standardized effect-size records, and appends covariates including study year, author, and DOI with resumable tracking. Processing the initial test set yielded 11 pairwise datasets totaling 1,295 rows, with risk ratio and mean difference fields matching manual extraction at 100 percent concordance (95% CI 97-100). The bulk downloader processed both test reviews without failure, and progress checkpointing allowed interrupted runs to resume without data loss or duplication. Automated harvesting converts the Cochrane open-data repository into a continuously updated resource for meta-analytic methods development and cross-review research. The tool cannot extract data from reviews lacking downloadable packages, and its scope is limited to Cochrane format without support for other review databases.
<!-- END-REWRITE -->

_Line range 1671-1746 in rewrite-workbook.txt_

---

## Entry 23 ([25/921]) — ComponentNMA

<details><summary>Metadata</summary>

```
TITLE: Component NMA: A Browser-Based Tool for Additive Component Network Meta-Analysis
TYPE: methods  |  ESTIMAND: Component effect estimates (log-OR/SMD)
DATA: Additive cNMA with WLS and interaction terms
PATH: C:\Models\ComponentNMA
```

</details>

### Original (frozen — do not edit)

```
How can researchers decompose multi-component interventions into individual active ingredients using network meta-analysis directly in the browser? Component NMA implements the additive component model using weighted least squares, constructing a binary design matrix mapping treatment comparisons to component contrasts against a no-active-component reference. The engine supports optional interaction terms for testing synergy or antagonism, with model fit assessed through Q-statistics, I-squared, and tau-squared estimates. Validation across 25 Selenium tests confirmed correct component decomposition, interaction estimation, 95% CI construction, and SMD ranking for a 24-trial smoking cessation dataset with four active components. Results are cross-validated against the R netmeta package, with component effect estimates and standard errors matching published implementations within numerical tolerance. This tool enables transparent decomposition of complex interventions, producing forest plots, network graphs, ranking tables, and equivalent R code for verification. The additive model assumes that components combine linearly; departures from additivity beyond pairwise interactions and inconsistency across component definitions warrant careful sensitivity analysis.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can researchers decompose multi-component interventions into individual active ingredients using network meta-analysis directly in the browser? Component NMA implements the additive component model using weighted least squares, constructing a binary design matrix mapping treatment comparisons to component contrasts against a no-active-component reference. The engine supports optional interaction terms for testing synergy or antagonism, with model fit assessed through Q-statistics, I-squared, and tau-squared estimates. Validation across 25 Selenium tests confirmed correct component decomposition, interaction estimation, 95% CI construction, and SMD ranking for a 24-trial smoking cessation dataset with four active components. Results are cross-validated against the R netmeta package, with component effect estimates and standard errors matching published implementations within numerical tolerance. This tool enables transparent decomposition of complex interventions, producing forest plots, network graphs, ranking tables, and equivalent R code for verification. The additive model assumes that components combine linearly; departures from additivity beyond pairwise interactions and inconsistency across component definitions warrant careful sensitivity analysis.
<!-- END-REWRITE -->

_Line range 1747-1822 in rewrite-workbook.txt_

---

## Entry 24 ([26/921]) — ConformalMA

<details><summary>Metadata</summary>

```
TITLE: Conformal Prediction Intervals for Meta-Analysis: Distribution-Free Coverage Across 307 Cochrane Reviews
TYPE: methods  |  ESTIMAND: Prediction interval coverage probability
DATA: 307 Cochrane systematic reviews (Pairwise70 dataset)
PATH: C:\Models\ConformalMA
```

</details>

### Original (frozen — do not edit)

```
Can distribution-free prediction intervals provide guaranteed coverage for the next study effect in meta-analysis without assuming normality? Conformal prediction was adapted for random-effects meta-analysis using leave-one-out nonconformity scores from DerSimonian-Laird estimates, then applied to 307 Cochrane reviews with at least four studies each, comparing coverage against standard and HKSJ prediction intervals. The method computes standardized residuals for each left-out study, takes the calibrated quantile, and projects the interval using median standard error as proxy for next-study variance. Conformal prediction intervals achieved 92.1% mean empirical coverage compared with 70.5% for standard and 67.0% for HKSJ intervals across 307 reviews. Standard intervals exhibited undercoverage in 76.5% of reviews, while conformal intervals were wider by a factor of 3.06 but maintained finite-sample guarantees. These findings suggest conventional prediction intervals systematically understate uncertainty about future study effects in heterogeneous meta-analyses. However, the limitation of wider intervals means conformal sets may be too conservative for clinical decisions requiring precise effect boundaries.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can distribution-free prediction intervals provide guaranteed coverage for the next study effect in meta-analysis without assuming normality? Conformal prediction was adapted for random-effects meta-analysis using leave-one-out nonconformity scores from DerSimonian-Laird estimates, then applied to 307 Cochrane reviews with at least four studies each, comparing coverage against standard and HKSJ prediction intervals. The method computes standardized residuals for each left-out study, takes the calibrated quantile, and projects the interval using median standard error as proxy for next-study variance. Conformal prediction intervals achieved 92.1% mean empirical coverage compared with 70.5% for standard and 67.0% for HKSJ intervals across 307 reviews. Standard intervals exhibited undercoverage in 76.5% of reviews, while conformal intervals were wider by a factor of 3.06 but maintained finite-sample guarantees. These findings suggest conventional prediction intervals systematically understate uncertainty about future study effects in heterogeneous meta-analyses. However, wider intervals means conformal sets may be too conservative for clinical decisions requiring precise effect boundaries.
<!-- END-REWRITE -->

_Line range 1823-1898 in rewrite-workbook.txt_

---

## Entry 25 ([27/921]) — CRES

<details><summary>Metadata</summary>

```
TITLE: CRES: Browser-Based Cardiorenal Evidence Synthesis with Integrated Meta-Analysis and Health-Economic Modelling
TYPE: methods  |  ESTIMAND: Hazard ratio
DATA: 20 RCTs (N=123,977): finerenone, SGLT2i, steroidal MRA
PATH: C:\Models\CRES
```

</details>

### Original (frozen — do not edit)

```
Can a single browser-based file deliver transparent, reproducible cardiorenal evidence synthesis integrating meta-analysis with health-economic modelling? CRES curates 20 randomised controlled trials enrolling 123,977 participants across finerenone, SGLT2 inhibitors, and steroidal mineralocorticoid receptor antagonists for cardiorenal outcomes. The platform implements DerSimonian-Laird random-effects pooling with t-distribution confidence intervals, a three-state Markov cost-effectiveness model, probabilistic sensitivity analysis, GRADE assessments, and Cochrane Risk of Bias 2.0 evaluations, cross-validated against R metafor version 4.8. Pooled HR was 0.79 for SGLT2 inhibitors (95% CI 0.71 to 0.87), 0.87 for finerenone, and 0.75 for steroidal MRAs, with I-squared of 50.3 percent and GRADE certainty rated LOW for the composite. An automated Selenium suite verified 227 end-to-end assertions spanning all computational outputs, interface elements, and security properties. CRES demonstrates that portable, installation-free evidence synthesis can honestly surface both favourable and unfavourable findings within a single auditable artifact. A limitation is that single-author data extraction departs from PRISMA best practice of independent dual extraction.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a browser-based file deliver transparent, reproducible cardiorenal evidence synthesis integrating meta-analysis with health-economic modelling? CRES curates 20 randomised controlled trials enrolling 123,977 participants across finerenone, SGLT2 inhibitors, and steroidal mineralocorticoid receptor antagonists for cardiorenal outcomes. The platform implements DerSimonian-Laird random-effects pooling with t-distribution confidence intervals, a three-state Markov cost-effectiveness model, probabilistic sensitivity analysis, GRADE assessments, and Cochrane Risk of Bias 2.0 evaluations, cross-validated against R metafor version 4.8. Pooled HR was 0.79 for SGLT2 inhibitors (95% CI 0.71 to 0.87), 0.87 for finerenone, and 0.75 for steroidal MRAs, with I-squared of 50.3 percent and GRADE certainty rated LOW for the composite. An automated Selenium suite verified 227 end-to-end assertions spanning all computational outputs, interface elements, and security properties. CRES demonstrates that portable, installation-free evidence synthesis can honestly surface both favourable and unfavourable findings within a single auditable artifact. Single-author data extraction departs from PRISMA best practice of independent dual extraction.
<!-- END-REWRITE -->

_Line range 1899-1974 in rewrite-workbook.txt_

---

## Entry 26 ([28/921]) — ctgov-cardiovascular-hiddenness

<details><summary>Metadata</summary>

```
TITLE: CT.gov Cardiovascular Hiddenness
TYPE: methods  |  ESTIMAND: 2-year no-results rate within the cardiovascular family among eligible older CT.gov studies
DATA: 26,062 eligible older cardiovascular studies in the March 29, 2026 full-registry snapshot
PATH: C:\Projects\ctgov-analyses/ctgov-cardiovascular-hiddenness
```

</details>

### Original (frozen — do not edit)

```
How quiet is the older cardiovascular trial record in ClinicalTrials.gov once heart and vascular studies are grouped into one registry-first family? We analysed 26,062 eligible older cardiovascular studies from the March 29, 2026 full-registry snapshot, spanning coronary, stroke, heart-failure, rhythm, and vascular records. Primary comparisons tracked two-year no-results rates, ghost protocols, sponsor-class mix, phase patterns, and the sponsors holding the biggest unresolved stock. Across older cardiovascular studies, 75.0 percent lacked posted results and 39.3 percent showed neither results nor a linked publication trail. PHASE1 remained the largest phase bucket, while Assistance Publique - Hôpitaux de Paris carried the biggest named sponsor stock at 144 older missing-results studies in the cardiovascular family. The cardiovascular record is therefore not just incomplete. It remains structurally quiet across common phases despite its central place in evidence-based medicine. This matters for guideline-facing cardiovascular medicine. These family-level estimates measure registry-visible absence rather than legal culpability or publication quality within this cardiovascular frame.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How quiet is the older cardiovascular trial record in ClinicalTrials.gov once heart and vascular studies are grouped into one registry-first family? We analysed 26,062 eligible older cardiovascular studies from the March 29, 2026 full-registry snapshot, spanning coronary, stroke, heart-failure, rhythm, and vascular records. Primary comparisons tracked two-year no-results rates, ghost protocols, sponsor-class mix, phase patterns, and the sponsors holding the biggest unresolved stock. Across older cardiovascular studies, 75.0 percent lacked posted results and 39.3 percent showed neither results nor a linked publication trail. PHASE1 remained the largest phase bucket, while Assistance Publique - Hôpitaux de Paris carried the biggest named sponsor stock at 144 older missing-results studies in the cardiovascular family. The cardiovascular record is therefore not just incomplete; it remains structurally quiet across common phases despite its central place in evidence-based medicine; this matters for guideline-facing cardiovascular medicine. These family-level estimates measure registry-visible absence rather than legal culpability or publication quality within this cardiovascular frame.
<!-- END-REWRITE -->

_Line range 1975-2050 in rewrite-workbook.txt_

---

## Entry 27 ([29/921]) — ctgov-completion-cohort-debt

<details><summary>Metadata</summary>

```
TITLE: CT.gov Completion Cohort Debt
TYPE: methods  |  ESTIMAND: 2-year no-results rate by primary completion cohort among eligible older closed interventional studies
DATA: Eligible older closed interventional studies grouped by primary completion year and completion era
PATH: C:\Projects\ctgov-analyses/ctgov-completion-cohort-debt
```

</details>

### Original (frozen — do not edit)

```
Do newer ClinicalTrials.gov completion cohorts look more transparent once every study has had at least two years to report? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and grouped them by primary completion year and broader completion eras. For each cohort we estimated two-year no-results rates, ghost-protocol rates defined as missing results plus missing publication links, and the share with both signals visible. The 2008-2012 completion era showed a 64.4 percent no-results rate and a 38.8 percent ghost-protocol rate. By 2021-2024, the comparable rates had worsened to 77.0 percent and 46.7 percent, while the fully visible share fell to 10.8 percent. Year-level summaries showed the same recent drift, indicating that eligibility alone does not erase newer registry silence across successive completion cohorts. These cohort comparisons are descriptive and can reflect changing trial mix, backfilling, and publication-linking practices as well as reporting behavior inside this still uneven public reporting system.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Do newer ClinicalTrials.gov completion cohorts look more transparent once every study has had at least two years to report? We analysed 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot and grouped them by primary completion year and broader completion eras. For each cohort we estimated two-year no-results rates, ghost-protocol rates defined as missing results plus missing publication links, and the share with both signals visible. The 2008-2012 completion era showed a 64.4 percent no-results rate and a 38.8 percent ghost-protocol rate. By 2021-2024, the comparable rates had worsened to 77.0 percent and 46.7 percent, while the fully visible share fell to 10.8 percent. Year-level summaries showed the same recent drift, indicating that eligibility alone does not erase newer registry silence across successive completion cohorts. These cohort comparisons are descriptive and can reflect changing trial mix, backfilling, and publication-linking practices as well as reporting behavior inside this still uneven public reporting system.
<!-- END-REWRITE -->

_Line range 2051-2126 in rewrite-workbook.txt_

---

## Entry 28 ([30/921]) — ctgov-condition-hiddenness-map

<details><summary>Metadata</summary>

```
TITLE: CT.gov Condition Hiddenness Map
TYPE: methods  |  ESTIMAND: Ghost-protocol rate by keyword-classified condition family among eligible older closed interventional studies
DATA: Eligible older closed interventional studies classified into dominant condition families from regist
PATH: C:\Projects\ctgov-analyses/ctgov-condition-hiddenness-map
```

</details>

### Original (frozen — do not edit)

```
Which therapeutic areas look quietest in ClinicalTrials.gov once older closed interventional studies are grouped into comparable condition families? We analysed 249,507 eligible older studies from the March 29, 2026 full-registry snapshot and assigned each record to one dominant keyword-based family using registry condition strings and titles. Primary comparisons focused on ghost-protocol rates, two-year no-results rates, and the share with both results and publication visibility across common families. Oncology formed the largest named family at 42,344 eligible older studies, creating the biggest absolute stock of hidden evidence. Healthy-volunteer studies had the highest ghost-protocol rate among common families at 63.5 percent, while metabolic and gastrointestinal groupings also remained heavily obscured. Infectious-disease studies were relatively more visible, reaching a 20.6 percent fully visible rate despite still carrying substantial non-reporting across mapped families in this atlas. Because the classification is keyword-based and single-label, multi-topic trials can be compressed into one family and some records remain in a broad other bucket.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which therapeutic areas look quietest in ClinicalTrials.gov once older closed interventional studies are grouped into comparable condition families? We analysed 249,507 eligible older studies from the March 29, 2026 full-registry snapshot and assigned each record to one dominant keyword-based family using registry condition strings and titles. Primary comparisons focused on ghost-protocol rates, two-year no-results rates, and the share with both results and publication visibility across common families. Oncology formed the largest named family at 42,344 eligible older studies, creating the biggest absolute stock of hidden evidence. Healthy-volunteer studies had the highest ghost-protocol rate among common families at 63.5 percent, while metabolic and gastrointestinal groupings also remained heavily obscured. Infectious-disease studies were relatively more visible, reaching a 20.6 percent fully visible rate despite still carrying substantial non-reporting across mapped families in this atlas. Because the classification is keyword-based and single-label, multi-topic trials can be compressed into one family and some records remain in a broad other bucket.
<!-- END-REWRITE -->

_Line range 2127-2202 in rewrite-workbook.txt_

---

## Entry 29 ([31/921]) — ctgov-evidence-visibility-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Evidence Visibility Gap
TYPE: methods  |  ESTIMAND: Ghost-protocol rate among eligible older closed interventional studies
DATA: 249,507 eligible older closed interventional studies from the March 29, 2026 full-registry snapshot
PATH: C:\Projects\ctgov-analyses/ctgov-evidence-visibility-gap
```

</details>

### Original (frozen — do not edit)

```
How visible is older interventional trial evidence in ClinicalTrials.gov when posted results and linked publications are read together rather than separately, actually? We analysed 249,507 closed interventional studies with primary completion at least two years before March 29, 2026, drawn from the full 578,109-study registry snapshot. Each eligible study was placed into one of four evidence states: results plus publication, results without publication, publication without results, or neither. Across eligible older studies, 42.7 percent showed neither posted results nor a linked publication, whereas only 13.7 percent showed both. Publication-only visibility remained common at 30.0 percent, and sponsor classes diverged sharply, with OTHER_GOV worst on ghost protocols at 49.1 percent while FED led on full visibility at 33.5 percent. Reading results tabs and linked papers together shows that older registry evidence is more often partially or wholly invisible than fully visible. These states measure registry-visible evidence coverage using internal CT.gov publication links, not exhaustive external bibliometric matching.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How visible is older interventional trial evidence in ClinicalTrials.gov when posted results and linked publications are read together rather than separately, actually? We analysed 249,507 closed interventional studies with primary completion at least two years before March 29, 2026, drawn from the full 578,109-study registry snapshot. Each eligible study was placed into one of four evidence states: results plus publication, results without publication, publication without results, or neither. Across eligible older studies, 42.7 percent showed neither posted results nor a linked publication, whereas only 13.7 percent showed both. Publication-only visibility remained common at 30.0 percent, and sponsor classes diverged sharply, with OTHER_GOV worst on ghost protocols at 49.1 percent while FED led on full visibility at 33.5 percent. Reading results tabs and linked papers together shows that older registry evidence is more often partially or wholly invisible than fully visible. These states measure registry-visible evidence coverage using internal CT.gov publication links, not exhaustive external bibliometric matching.
<!-- END-REWRITE -->

_Line range 2203-2278 in rewrite-workbook.txt_

---

## Entry 30 ([32/921]) — ctgov-hiddenness-atlas

<details><summary>Metadata</summary>

```
TITLE: CT.gov Hiddenness Atlas: What Sponsors Still Do Not Show
TYPE: methods  |  ESTIMAND: 2-year no-results rate among eligible closed interventional studies
DATA: 578,109 ClinicalTrials.gov records
PATH: C:\Projects\ctgov-analyses/ctgov-hiddenness-atlas
```

</details>

### Original (frozen — do not edit)

```
Which sponsor groups account for the largest registry-visible non-disclosure burden across ClinicalTrials.gov? We analysed 578,109 registry records downloaded on March 29, 2026, including 441,191 interventional studies and 290,524 closed interventional studies. We derived omission flags for missing results, missing actual completion dates, missing actual enrollment, absent IPD statements, absent publication links, sparse outcomes, and undisclosed stopping reasons, then summarized them by sponsor class, sponsor, and phase. Among closed interventional studies with primary completion at least two years earlier, 72.7 percent still had no posted results, with OTHER_GOV worst on rate at 95.7 percent and OTHER largest on volume at 127,704 studies. Industry still carried 44,007 two-year no-results studies, phase I had the highest non-reporting rate at 76.7 percent, and NIH had the highest average hiddenness score among named sponsor classes. Registry opacity is concentrated differently by class, so rates, volumes, and structural missingness must be read together. These measures capture registry-visible omission rather than legal violation.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which sponsor groups account for the largest registry-visible non-disclosure burden across ClinicalTrials.gov? We analysed 578,109 registry records downloaded on March 29, 2026, including 441,191 interventional studies and 290,524 closed interventional studies. We derived omission flags for missing results, missing actual completion dates, missing actual enrollment, absent IPD statements, absent publication links, sparse outcomes, and undisclosed stopping reasons, then summarized them by sponsor class, sponsor, and phase. Among closed interventional studies with primary completion at least two years earlier, 72.7 percent still had no posted results, with OTHER_GOV worst on rate at 95.7 percent and OTHER largest on volume at 127,704 studies. Industry still carried 44,007 two-year no-results studies, phase I had the highest non-reporting rate at 76.7 percent, and NIH had the highest average hiddenness score among named sponsor classes. Registry opacity is concentrated differently by class, so rates, volumes, and structural missingness must be read together. These measures capture registry-visible omission rather than legal violation.
<!-- END-REWRITE -->

_Line range 2279-2354 in rewrite-workbook.txt_

---

## Entry 31 ([33/921]) — ctgov-industry-disclosure-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Industry Disclosure Gap
TYPE: methods  |  ESTIMAND: 2-year no-results rate among eligible older closed interventional industry studies
DATA: 128,464 industry-linked studies from the March 29, 2026 full-registry snapshot
PATH: C:\Projects\ctgov-analyses/ctgov-industry-disclosure-gap
```

</details>

### Original (frozen — do not edit)

```
How large is the industry-specific disclosure gap inside the live ClinicalTrials.gov registry? We analysed the March 29, 2026 full-registry snapshot, focusing on 128,464 industry-linked studies and 87,296 closed interventional industry studies. We derived sponsor-level omission flags for missing results, missing actual dates, missing actual enrollment, missing IPD statements, missing publication links, and missing detailed descriptions, while preserving sponsor-level counts so absolute backlog and rate-based silence could be read together across named firms globally. Among eligible older closed interventional industry studies, 58.1 percent still had no posted results, leaving 44,007 unresolved two-year no-results records in the industry bucket alone. The biggest absolute backlogs sat with GlaxoSmithKline, AstraZeneca, Boehringer Ingelheim, Sanofi, and Pfizer, while several smaller sponsors exceeded 95 percent on the same rate metric. Industry records were also structurally sparse, with 63.2 percent lacking IPD statements, 66.6 percent lacking publication links, and 53.8 percent lacking detailed descriptions. These estimates identify registry-visible non-disclosure rather than adjudicated legal breach.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How large is the industry-specific disclosure gap inside the live ClinicalTrials.gov registry? We analysed the March 29, 2026 full-registry snapshot, focusing on 128,464 industry-linked studies and 87,296 closed interventional industry studies. We derived sponsor-level omission flags for missing results, missing actual dates, missing actual enrollment, missing IPD statements, missing publication links, and missing detailed descriptions, while preserving sponsor-level counts so absolute backlog and rate-based silence could be read together across named firms globally. Among eligible older closed interventional industry studies, 58.1 percent still had no posted results, leaving 44,007 unresolved two-year no-results records in the industry bucket alone. The biggest absolute backlogs sat with GlaxoSmithKline, AstraZeneca, Boehringer Ingelheim, Sanofi, and Pfizer, while several smaller sponsors exceeded 95 percent on the same rate metric. Industry records were also structurally sparse, with 63.2 percent lacking IPD statements, 66.6 percent lacking publication links, and 53.8 percent lacking detailed descriptions. These estimates identify registry-visible non-disclosure rather than adjudicated legal breach.
<!-- END-REWRITE -->

_Line range 2355-2430 in rewrite-workbook.txt_

---

## Entry 32 ([34/921]) — ctgov-metabolic-hiddenness

<details><summary>Metadata</summary>

```
TITLE: CT.gov Metabolic Hiddenness
TYPE: methods  |  ESTIMAND: 2-year no-results rate within the metabolic family among eligible older CT.gov studies
DATA: 17,294 eligible older metabolic studies in the March 29, 2026 full-registry snapshot
PATH: C:\Projects\ctgov-analyses/ctgov-metabolic-hiddenness
```

</details>

### Original (frozen — do not edit)

```
How much older metabolic trial evidence on ClinicalTrials.gov remains quiet once obesity, diabetes, and related studies are read as one family? We analysed 17,294 eligible older metabolic studies from the March 29, 2026 full-registry snapshot, covering diabetes, obesity, lipid, and endocrine-related portfolios. The project compares two-year no-results rates, ghost-protocol rates, sponsor-class contrasts, phase structure, and leading sponsors by unresolved stock. Across older metabolic studies, 76.2 percent lacked posted results and 41.9 percent showed neither results nor a linked publication. EARLY_PHASE1 remained the dominant phase bucket, while Novo Nordisk A/S carried the largest named sponsor stock at 391 older missing-results studies in the metabolic family. Metabolic hiddenness is therefore not confined to one sponsor sector and remains visible across large clinical-development and registry-sparsity channels. That is especially important because diabetes and obesity evidence directly shapes large prescribing, prevention, and public-health decisions. These metrics capture registry-visible omission rather than adjudicated legal breach within this metabolic family frame today.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How much older metabolic trial evidence on ClinicalTrials.gov remains quiet once obesity, diabetes, and related studies are read as one family? We analysed 17,294 eligible older metabolic studies from the March 29, 2026 full-registry snapshot, covering diabetes, obesity, lipid, and endocrine-related portfolios. The project compares two-year no-results rates, ghost-protocol rates, sponsor-class contrasts, phase structure, and leading sponsors by unresolved stock. Across older metabolic studies, 76.2 percent lacked posted results and 41.9 percent showed neither results nor a linked publication. EARLY_PHASE1 remained the dominant phase bucket, while Novo Nordisk A/S carried the largest named sponsor stock at 391 older missing-results studies in the metabolic family. Metabolic hiddenness is therefore not confined to one sponsor sector and remains visible across large clinical-development and registry-sparsity channels. That is especially important because diabetes and obesity evidence directly shapes large prescribing, prevention, and public-health decisions; these metrics capture registry-visible omission rather than adjudicated legal breach within this metabolic family frame today.
<!-- END-REWRITE -->

_Line range 2431-2506 in rewrite-workbook.txt_

---

## Entry 33 ([35/921]) — ctgov-oncology-hiddenness

<details><summary>Metadata</summary>

```
TITLE: CT.gov Oncology Hiddenness
TYPE: methods  |  ESTIMAND: 2-year no-results rate within the oncology family among eligible older CT.gov studies
DATA: 42,344 eligible older oncology studies in the March 29, 2026 full-registry snapshot
PATH: C:\Projects\ctgov-analyses/ctgov-oncology-hiddenness
```

</details>

### Original (frozen — do not edit)

```
How much registered oncology evidence still goes quiet on ClinicalTrials.gov once older closed interventional studies are isolated? We analysed 42,344 eligible older oncology studies from the March 29, 2026 full-registry snapshot, making oncology the largest named disease family in the portfolio. The project compares two-year no-results rates, ghost-protocol rates, sponsor-class patterns, phase gradients, and the biggest named sponsors by unresolved stock. Across older oncology studies, 67.0 percent lacked posted results and 42.5 percent showed neither results nor a linked publication. Phase EARLY_ 1 was especially quiet at 87.9 percent on the no-results metric, while National Cancer Institute (NCI) carried the largest sponsor stock at 909 older missing-results studies. Oncology hiddenness is therefore about scale as much as silence, with very large stock spread across public, academic, network, and industry sponsors. That matters for cancer policy, treatment evaluation, and evidence review. These measures describe registry-visible evidence absence rather than adjudicated legal non-compliance within this public oncology frame.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How much registered oncology evidence still goes quiet on ClinicalTrials.gov once older closed interventional studies are isolated? We analysed 42,344 eligible older oncology studies from the March 29, 2026 full-registry snapshot, making oncology the largest named disease family in the portfolio. The project compares two-year no-results rates, ghost-protocol rates, sponsor-class patterns, phase gradients, and the biggest named sponsors by unresolved stock. Across older oncology studies, 67.0 percent lacked posted results and 42.5 percent showed neither results nor a linked publication. Phase EARLY_ 1 was especially quiet at 87.9 percent on the no-results metric, while National Cancer Institute (NCI) carried the largest sponsor stock at 909 older missing-results studies. Oncology hiddenness is therefore about scale as much as silence, with very large stock spread across public, academic, network, and industry sponsors. That matters for cancer policy, treatment evaluation, and evidence review; these measures describe registry-visible evidence absence rather than adjudicated legal non-compliance within this public oncology frame.
<!-- END-REWRITE -->

_Line range 2507-2582 in rewrite-workbook.txt_

---

## Entry 34 ([36/921]) — ctgov-phase-reporting-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Phase Reporting Gap
TYPE: methods  |  ESTIMAND: Eligible 2-year no-results rate by reported trial phase
DATA: 441,191 interventional studies from the March 29, 2026 full-registry snapshot grouped by phase
PATH: C:\Projects\ctgov-analyses/ctgov-phase-reporting-gap
```

</details>

### Original (frozen — do not edit)

```
Does reporting failure in ClinicalTrials.gov differ systematically by trial phase? We analysed the March 29, 2026 full-registry snapshot and grouped interventional studies by reported phase before calculating eligible two-year no-results rates and absolute missing-results stock. The analysis used 441,191 interventional studies overall, with 290,524 closed interventional studies and 249,507 eligible older studies driving the primary comparisons. Phase I had the highest eligible two-year no-results rate at 76.7 percent, followed by the large NA phase bucket at 65.5 percent and early phase I at 64.3 percent. By absolute count, the NA bucket contributed 96,605 unresolved two-year no-results studies, far exceeding later phases because of its scale, which shows phase structure shapes reporting behavior even before sponsor mix and therapeutic area are considered jointly. Phase III and phase IV performed better than phase I, but still remained far from transparent at 45.5 percent and 52.4 percent respectively. These phase estimates describe registry-visible non-disclosure rather than confirmed regulatory violation.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Does reporting failure in ClinicalTrials.gov differ systematically by trial phase? We analysed the March 29, 2026 full-registry snapshot and grouped interventional studies by reported phase before calculating eligible two-year no-results rates and absolute missing-results stock. The analysis used 441,191 interventional studies overall, with 290,524 closed interventional studies and 249,507 eligible older studies driving the primary comparisons. Phase I had the highest eligible two-year no-results rate at 76.7 percent, followed by the large NA phase bucket at 65.5 percent and early phase I at 64.3 percent. By absolute count, the NA bucket contributed 96,605 unresolved two-year no-results studies, far exceeding later phases because of its scale, which shows phase structure shapes reporting behavior even before sponsor mix and therapeutic area are considered jointly. Phase III and phase IV performed better than phase I, but still remained far from transparent at 45.5 percent and 52.4 percent respectively. These phase estimates describe registry-visible non-disclosure rather than confirmed regulatory violation.
<!-- END-REWRITE -->

_Line range 2583-2658 in rewrite-workbook.txt_

---

## Entry 35 ([37/921]) — ctgov-publication-undercount-audit

<details><summary>Metadata</summary>

```
TITLE: CT.gov Publication Undercount Audit
TYPE: methods  |  ESTIMAND: Weighted PubMed NCT-match rate among older CT.gov records lacking linked publications
DATA: Sponsor-class-stratified sample of 1,050 older no-link studies queried against PubMed by NCT ID
PATH: C:\Projects\ctgov-analyses/ctgov-publication-undercount-audit
```

</details>

### Original (frozen — do not edit)

```
How often do ClinicalTrials.gov records with no linked publication hide an external PubMed trail when searched by NCT identifier? We drew a sponsor-class-stratified audit sample of 1,050 older studies lacking CT.gov publication links from the March 29, 2026 full-registry snapshot. Each sampled NCT identifier was queried against PubMed using identifier-based E-utilities searches, then reweighted back to the sponsor-class distribution of older no-link studies. The weighted PubMed NCT-match rate across the no-link older-study population was only 1.2 percent, indicating that external publication rescue was uncommon on this identifier-based audit. The weighted external-publication-only rate among no-link studies was just 0.3 percent, and the industry sample reached 2.0 percent on the raw PubMed match rate. Missing CT.gov publication links therefore look more like true visible sparsity than widespread under-linking, at least under a strict NCT-indexed external search strategy. This audit is sample-based and identifier-dependent, so it can miss publications that omit NCT identifiers or sit outside PubMed indexing today.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
How often do ClinicalTrials.gov records with no linked publication hide an external PubMed trail when searched by NCT identifier? We drew a sponsor-class-stratified audit sample of 1,050 older studies lacking CT.gov publication links from the March 29, 2026 full-registry snapshot. Each sampled NCT identifier was queried against PubMed using identifier-based E-utilities searches, then reweighted back to the sponsor-class distribution of older no-link studies. The weighted PubMed NCT-match rate across the no-link older-study population was only 1.2 percent, indicating that external publication rescue was uncommon on this identifier-based audit. The weighted external-publication-only rate among no-link studies was just 0.3 percent, and the industry sample reached 2.0 percent on the raw PubMed match rate. Missing CT.gov publication links therefore look more like true visible sparsity than widespread under-linking, at least under a strict NCT-indexed external search strategy. This audit is sample-based and identifier-dependent, so it can miss publications that omit NCT identifiers or sit outside PubMed indexing today.
<!-- END-REWRITE -->

_Line range 2659-2734 in rewrite-workbook.txt_

---

## Entry 36 ([38/921]) — ctgov-rule-era-reporting-gap

<details><summary>Metadata</summary>

```
TITLE: CT.gov Rule-Era Reporting Gap
TYPE: methods  |  ESTIMAND: 2-year no-results rate across completion eras anchored to major U.S. reporting rules
DATA: 249,507 eligible older closed interventional studies grouped into four completion eras
PATH: C:\Projects\ctgov-analyses/ctgov-rule-era-reporting-gap
```

</details>

### Original (frozen — do not edit)

```
Did ClinicalTrials.gov completion cohorts become more transparent after FDAAA 801 and the Final Rule? We analysed 249,507 older closed interventional studies from the March 29, 2026 full-registry snapshot and grouped them into four completion eras anchored to reporting-rule landmarks. For each era we estimated two-year no-results rates, ghost-protocol rates, no-publication rates, and the share with both results and publication visible. The FDAAA 801 era from 2008 to 2016 showed a 67.1 percent no-results rate, whereas the recent eligible era from 2021 to 2024 rose to 77.0 percent. Ghost protocols likewise increased from 39.6 percent in the FDAAA 801 era to 46.7 percent in the recent eligible era, while full visibility fell to 10.8 percent. Later eligible cohorts therefore do not look cleaner on these registry-visible measures even after each included study had at least two years to report. These policy-era comparisons are descriptive and do not adjudicate applicable-clinical-trial status or legal compliance within this registry frame.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Did ClinicalTrials.gov completion cohorts become more transparent after FDAAA 801 and the Final Rule? We analysed 249,507 older closed interventional studies from the March 29, 2026 full-registry snapshot and grouped them into four completion eras anchored to reporting-rule landmarks. For each era we estimated two-year no-results rates, ghost-protocol rates, no-publication rates, and the share with both results and publication visible. The FDAAA 801 era from 2008 to 2016 showed a 67.1 percent no-results rate, whereas the recent eligible era from 2021 to 2024 rose to 77.0 percent. Ghost protocols likewise increased from 39.6 percent in the FDAAA 801 era to 46.7 percent in the recent eligible era, while full visibility fell to 10.8 percent. Later eligible cohorts therefore do not look cleaner on these registry-visible measures even after each included study had at least two years to report. These policy-era comparisons are descriptive and do not adjudicate applicable-clinical-trial status or legal compliance within this registry frame.
<!-- END-REWRITE -->

_Line range 2735-2810 in rewrite-workbook.txt_

---

## Entry 37 ([39/921]) — ctgov-search-strategies

<details><summary>Metadata</summary>

```
TITLE: CT.gov Search Strategy Tool: Systematic Review Search Validation with 99 Percent API Recall
TYPE: methods  |  ESTIMAND: API recall
DATA: 1,736 Cochrane NCT IDs across 12 medical categories
PATH: C:\Projects\ctgov-analyses/ctgov-search-strategies
```

</details>

### Original (frozen — do not edit)

```
Can automated search strategies for ClinicalTrials.gov achieve high recall against a large Cochrane reference standard of indexed trial registrations? We assembled 1,736 unique NCT identifiers from twelve Cochrane systematic review categories spanning cardiovascular, oncology, and metabolic therapeutic areas as ground truth for validation. The toolkit implements ten strategies with Boolean optimization, fifty-plus spelling variants, PICO-based query generation, quality assessment informed by PRESS 2015 guidelines, and seven-database translation covering PubMed, Embase, Cochrane, Web of Science, CINAHL, and PsycINFO. Validation against the reference set demonstrated 99 percent API recall with Wilson score confidence intervals confirming robust retrieval across all twelve therapeutic categories. Strategy-specific benchmarking with ROC visualization confirmed that condition-plus-intervention queries consistently outperformed keyword-only approaches across disease areas. Systematic registry searching with validated strategies approaches near-complete recall for registered interventional studies using the ClinicalTrials.gov API directly. The limitation of API recall testing is that it measures retrieval of known registrations not true search sensitivity requiring prospective human screening.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can automated search strategies for ClinicalTrials.gov achieve high recall against a large Cochrane reference standard of indexed trial registrations? We assembled 1,736 unique NCT identifiers from twelve Cochrane systematic review categories spanning cardiovascular, oncology, and metabolic therapeutic areas as ground truth for validation. The toolkit implements ten strategies with Boolean optimization, fifty-plus spelling variants, PICO-based query generation, quality assessment informed by PRESS 2015 guidelines, and seven-database translation covering PubMed, Embase, Cochrane, Web of Science, CINAHL, and PsycINFO. Validation against the reference set demonstrated 99 percent API recall with Wilson score confidence intervals confirming robust retrieval across all twelve therapeutic categories. Strategy-specific benchmarking with ROC visualization confirmed that condition-plus-intervention queries consistently outperformed keyword-only approaches across disease areas. Systematic registry searching with validated strategies approaches near-complete recall for registered interventional studies using the ClinicalTrials.gov API directly. The limitation of API recall testing is that it measures retrieval of known registrations not true search sensitivity requiring prospective human screening.
<!-- END-REWRITE -->

_Line range 2811-2886 in rewrite-workbook.txt_

---

## Entry 38 ([40/921]) — ctgov-sponsor-backlog-concentration

<details><summary>Metadata</summary>

```
TITLE: CT.gov Sponsor Backlog Concentration
TYPE: methods  |  ESTIMAND: Share of the 2-year missing-results backlog held by top sponsor slices
DATA: 25,584 lead sponsors contributing to the eligible older missing-results backlog in the March 29, 202
PATH: C:\Projects\ctgov-analyses/ctgov-sponsor-backlog-concentration
```

</details>

### Original (frozen — do not edit)

```
Is the ClinicalTrials.gov missing-results backlog spread evenly across sponsors, or does a relatively small slice hold most of the unresolved stock? We analysed sponsor-level counts for 249,507 eligible older closed interventional studies and ranked 25,584 lead sponsors by two-year missing-results volume. The concentration analysis tracked cumulative shares of unresolved no-results studies, sponsor-level ghost-protocol counts, and inequality metrics alongside named outlier sponsors. The top 1 percent of lead sponsors accounted for 39.6 percent of the missing-results backlog, and the top 10 percent accounted for 77.4 percent. The sponsor-level Gini coefficient reached 0.818, while large industry firms, major academic centers, and public institutions all appeared among the highest-volume sponsors. The unresolved stock is therefore broad but highly uneven, with a thin sponsor slice carrying a disproportionate share of what remains unseen. These concentration statistics describe registry-visible stock distribution, not legal liability, and they depend on the lead-sponsor field recorded in CT.gov across this sponsor field and snapshot frame.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Is the ClinicalTrials.gov missing-results backlog spread evenly across sponsors, or does a relatively small slice hold most of the unresolved stock? We analysed sponsor-level counts for 249,507 eligible older closed interventional studies and ranked 25,584 lead sponsors by two-year missing-results volume. The concentration analysis tracked cumulative shares of unresolved no-results studies, sponsor-level ghost-protocol counts, and inequality metrics alongside named outlier sponsors. The top 1 percent of lead sponsors accounted for 39.6 percent of the missing-results backlog, and the top 10 percent accounted for 77.4 percent. The sponsor-level Gini coefficient reached 0.818, while large industry firms, major academic centers, and public institutions all appeared among the highest-volume sponsors. The unresolved stock is therefore broad but highly uneven, with a thin sponsor slice carrying a disproportionate share of what remains unseen. These concentration statistics describe registry-visible stock distribution, not legal liability, and they depend on the lead-sponsor field recorded in CT.gov across this sponsor field and snapshot frame.
<!-- END-REWRITE -->

_Line range 2887-2962 in rewrite-workbook.txt_

---

## Entry 39 ([41/921]) — ctgov-sponsor-class-hiddenness

<details><summary>Metadata</summary>

```
TITLE: CT.gov Sponsor-Class Hiddenness
TYPE: methods  |  ESTIMAND: Sponsor-class comparison of eligible 2-year no-results rate and absolute missing-results stock
DATA: Full March 29, 2026 ClinicalTrials.gov snapshot grouped by sponsor class
PATH: C:\Projects\ctgov-analyses/ctgov-sponsor-class-hiddenness
```

</details>

### Original (frozen — do not edit)

```
Which sponsor classes account for the biggest and worst ClinicalTrials.gov disclosure failures? We analysed 578,109 registry records captured on March 29, 2026, with particular attention to 290,524 closed interventional studies and 249,507 eligible older studies. We summarized two-year no-results gaps, structural missingness, and composite hiddenness scores by sponsor class using the full flattened study-level feature set, deliberately separating rates, stocks, and missing-field patterns instead of collapsing everything into one composite leaderboard for public interpretation and oversight. OTHER_GOV had the worst eligible two-year no-results rate at 95.7 percent, whereas OTHER held the largest absolute stock at 127,704 missing-results studies. Industry remained too large to dismiss, contributing 44,007 two-year no-results studies, while NIH had the highest average hiddenness score among named sponsor classes. The class pattern therefore changes depending on whether one prioritizes rates, absolute stock, or structural sparsity, which means a single leaderboard is misleading. These estimates capture observable registry omission rather than motive or legal culpability.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Which sponsor classes account for the biggest and worst ClinicalTrials.gov disclosure failures? We analysed 578,109 registry records captured on March 29, 2026, with particular attention to 290,524 closed interventional studies and 249,507 eligible older studies. We summarized two-year no-results gaps, structural missingness, and composite hiddenness scores by sponsor class using the full flattened study-level feature set, deliberately separating rates, stocks, and missing-field patterns instead of collapsing everything into one composite leaderboard for public interpretation and oversight. OTHER_GOV had the worst eligible two-year no-results rate at 95.7 percent, whereas OTHER held the largest absolute stock at 127,704 missing-results studies. Industry remained too large to dismiss, contributing 44,007 two-year no-results studies, while NIH had the highest average hiddenness score among named sponsor classes. The class pattern therefore changes depending on whether one prioritizes rates, absolute stock, or structural sparsity, which means a single leaderboard is misleading. These estimates capture observable registry omission rather than motive or legal culpability.
<!-- END-REWRITE -->

_Line range 2963-3038 in rewrite-workbook.txt_

---

## Entry 40 ([42/921]) — ctgov-structural-missingness

<details><summary>Metadata</summary>

```
TITLE: CT.gov Structural Missingness
TYPE: methods  |  ESTIMAND: Field-level structural missingness across the full registry
DATA: 578,109 ClinicalTrials.gov records from the March 29, 2026 full-registry snapshot
PATH: C:\Projects\ctgov-analyses/ctgov-structural-missingness
```

</details>

### Original (frozen — do not edit)

```
What information disappears from ClinicalTrials.gov even before one asks whether results were posted? We analysed the March 29, 2026 full-registry snapshot and quantified structural missingness in publication links, IPD statements, detailed descriptions, locations, and outcome fields across sponsor groups. The source universe included 578,109 studies, allowing field-level omission rates and sponsor-specific sparsity patterns to be estimated without sampling. Across the full registry, 63.4 percent of records lacked publication links, 48.3 percent lacked IPD sharing statements, 32.7 percent lacked detailed descriptions, and 10.2 percent lacked locations. Structural sparsity was not evenly distributed: industry remained heavily affected, NIH had the highest average hiddenness score among named sponsor classes, and UNKNOWN mostly reflected malformed metadata. Missingness therefore extends beyond results reporting into the descriptive fields needed for interpretation, replication, and scrutiny, with the loss being less context for appraisal, replication, accountability, and public scrutiny across therapeutic areas. These metrics capture registry-visible information loss rather than proven intent to conceal.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
What information disappears from ClinicalTrials.gov even before one asks whether results were posted? We analysed the March 29, 2026 full-registry snapshot and quantified structural missingness in publication links, IPD statements, detailed descriptions, locations, and outcome fields across sponsor groups. The source universe included 578,109 studies, allowing field-level omission rates and sponsor-specific sparsity patterns to be estimated without sampling. Across the full registry, 63.4 percent of records lacked publication links, 48.3 percent lacked IPD sharing statements, 32.7 percent lacked detailed descriptions, and 10.2 percent lacked locations. Structural sparsity was not evenly distributed: industry remained heavily affected, NIH had the highest average hiddenness score among named sponsor classes, and UNKNOWN mostly reflected malformed metadata. Missingness therefore extends beyond results reporting into the descriptive fields needed for interpretation, replication, and scrutiny, with the loss being less context for appraisal, replication, accountability, and public scrutiny across therapeutic areas. These metrics capture registry-visible information loss rather than proven intent to conceal.
<!-- END-REWRITE -->

_Line range 3039-3114 in rewrite-workbook.txt_

---

## Entry 41 ([43/921]) — cv-rct-analysis

<details><summary>Metadata</summary>

```
TITLE: CV-RCT Analysis: Cardiovascular Trial Landscape Dashboard Integrating Registry and Publication Data
TYPE: methods  |  ESTIMAND: Publication rate
DATA: AACT, PubMed, OpenAlex; CV Phase III RCTs 2015-2022
PATH: C:\Projects\cv-rct-analysis
```

</details>

### Original (frozen — do not edit)

```
Can an integrated pipeline map the cardiovascular Phase III trial landscape by reconciling registry, bibliometric, and open-access publication data sources? We built an extraction pipeline connecting ClinicalTrials.gov via AACT PostgreSQL, PubMed for publication matching, and OpenAlex for citation metrics covering cardiovascular trials from 2015 to 2022. The system classifies trials into eight cardiovascular sub-domains via keyword matching, performs automated publication reconciliation, and delivers interactive forest and funnel plots through a summaries. Across 87 of 87 automated validation tests (100 percent pass rate) covering extraction and visualization, all passed with complete coverage from database query through statistical aggregation and plot generation. Domain-level summaries revealed differential publication rates and enrollment patterns across heart failure, coronary artery disease, arrhythmia, and additional cardiovascular sub-domains. Multi-source data reconciliation provides a scalable approach to mapping trial landscapes beyond what any single registry captures alone. The limitation of keyword-based domain classification is that multi-label assignment may inflate counts for trials spanning multiple conditions.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can an integrated pipeline map the cardiovascular Phase III trial landscape by reconciling registry, bibliometric, and open-access publication data sources? We built an extraction pipeline connecting ClinicalTrials.gov via AACT PostgreSQL, PubMed for publication matching, and OpenAlex for citation metrics covering cardiovascular trials from 2015 to 2022. It classifies trials into eight cardiovascular sub-domains via keyword matching, performs automated publication reconciliation, and delivers interactive forest and funnel plots through a summaries. Across 87 of 87 automated validation tests (100 percent pass rate) covering extraction and visualization, all passed with complete coverage from database query through statistical aggregation and plot generation. Domain-level summaries revealed differential publication rates and enrollment patterns across heart failure, coronary artery disease, arrhythmia, and additional cardiovascular sub-domains. Multi-source data reconciliation provides a scalable approach to mapping trial landscapes beyond what any single registry captures alone. The limitation of keyword-based domain classification is that multi-label assignment may inflate counts for trials spanning multiple conditions.
<!-- END-REWRITE -->

_Line range 3115-3190 in rewrite-workbook.txt_

---

## Entry 42 ([44/921]) — Dataextractor

<details><summary>Metadata</summary>

```
TITLE: RCTExtractor: AI-Powered Clinical Trial Data Extraction with 100% Accuracy
TYPE: methods  |  ESTIMAND: HR
DATA: 65 landmark RCTs, cardiology/oncology/nephrology/neurology
PATH: C:\Projects\Dataextractor
```

</details>

### Original (frozen — do not edit)

```
Can a fully offline tool extract structured clinical trial data from publication text matching manual double extraction accuracy? We validated RCTExtractor against 65 landmark trials in cardiology, oncology, nephrology, and neurology, covering hazard ratios, risk ratios, odds ratios, and mean differences. The tool combines 34 AI modules for entity recognition and confidence scoring with 21 sample-size patterns, OCR digit-confusion correction, and automated risk assessment. Across 65 trials the tool achieved 100 percent accuracy for primary HR, OR, and confidence intervals (95% CI 94.5-100), processing each document in under 100 milliseconds offline. Enhanced OCR detection improved digit-confusion identification from 60 to 75 percent, and sample-size extraction rose from 33 to 100 percent after adding three new patterns. Perfect accuracy on a diverse benchmark shows rule-based extraction with AI enhancement matches expert-level collection for structured trial endpoints. Accuracy may not extend to non-English publications or non-standard reporting, and the tool cannot interpret narrative outcome descriptions or composite endpoints.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a fully offline tool extract structured clinical trial data from publication text matching manual double extraction accuracy? We validated RCTExtractor against 65 landmark trials in cardiology, oncology, nephrology, and neurology, covering hazard ratios, risk ratios, odds ratios, and mean differences. The tool combines 34 AI modules for entity recognition and confidence scoring with 21 sample-size patterns, OCR digit-confusion correction, and automated risk assessment. Across 65 trials the tool achieved 100 percent accuracy for primary HR, OR, and confidence intervals (95% CI 94.5-100), processing each document in under 100 milliseconds offline. Enhanced OCR detection improved digit-confusion identification from 60 to 75 percent, and sample-size extraction rose from 33 to 100 percent after adding three new patterns. Perfect accuracy on a diverse benchmark shows rule-based extraction with AI enhancement matches expert-level collection for structured trial endpoints. Accuracy may not extend to non-English publications or non-standard reporting, and the tool cannot interpret narrative outcome descriptions or composite endpoints.
<!-- END-REWRITE -->

_Line range 3191-3266 in rewrite-workbook.txt_

---

## Entry 43 ([45/921]) — dosehtml

<details><summary>Metadata</summary>

```
TITLE: Dose Response Pro: Browser-Based Dose-Response Meta-Analysis Matching R Accuracy
TYPE: methods  |  ESTIMAND: Dose-response trend coefficient
DATA: 120 R dosresmeta benchmark datasets
PATH: C:\HTML apps\dosehtml
```

</details>

### Original (frozen — do not edit)

```
Can browser-based dose-response meta-analysis match the numerical accuracy of established R packages while providing interactive visualization? Dose Response Pro v18.1 is a 10,022-line single-file HTML application implementing the Greenland-Longnecker two-stage method for dose-response meta-analysis with linear, quadratic, and restricted cubic spline models, plus leave-one-out sensitivity analysis. The tool provides interactive dose-response curve plotting, CSV import with flexible column detection, R code export for reproducibility checks, and a command-line interface for batch processing alongside the browser application. Strict benchmarking against the R dosresmeta package showed exact parity on 120 of 120 comparable datasets with a median runtime speedup of 1.92x over the R implementation. Deterministic CLI validation confirmed three-of-three passed checks including grid-based coefficient verification against independently computed reference values. This demonstrates that client-side JavaScript can deliver publication-quality dose-response synthesis with performance exceeding dedicated statistical environments. However, the limitation of exploratory spline model status means complex non-linear relationships require independent validation before clinical interpretation of inflection points.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can browser-based dose-response meta-analysis match the numerical accuracy of established R packages while providing interactive visualization? Dose Response Pro v18.1 is a 10,022-line single-file HTML application implementing the Greenland-Longnecker two-stage method for dose-response meta-analysis with linear, quadratic, and restricted cubic spline models, plus leave-one-out sensitivity analysis. The tool provides interactive dose-response curve plotting, CSV import with flexible column detection, R code export for reproducibility checks, and a command-line interface for batch processing alongside the browser application. Strict benchmarking against the R dosresmeta package showed exact parity on 120 of 120 comparable datasets with a median runtime speedup of 1.92x over the R implementation. Deterministic CLI validation confirmed three-of-three passed checks including grid-based coefficient verification against independently computed reference values. This demonstrates that client-side JavaScript can deliver publication-quality dose-response synthesis with performance exceeding dedicated statistical environments. However, exploratory spline model status means complex non-linear relationships require independent validation before clinical interpretation of inflection points.
<!-- END-REWRITE -->

_Line range 3267-3342 in rewrite-workbook.txt_

---

## Entry 44 ([46/921]) — DPMA

<details><summary>Metadata</summary>

```
TITLE: Dirichlet Process Meta-Analysis
TYPE: methods  |  ESTIMAND: summary effect
DATA: Repository artifacts in /mnt/c/Models/DPMA
PATH: C:\Models\DPMA
```

</details>

### Original (frozen — do not edit)

```
Does the standard random-effects assumption of a single normal effect distribution mask clinically important subgroups within meta-analyses? We applied Dirichlet process mixture modeling to 307 Cochrane systematic reviews spanning diverse therapeutic areas, using a collapsed Gibbs sampler with five thousand posterior iterations per review. The Dirichlet process discovers the number of latent clusters nonparametrically, without requiring the analyst to pre-specify subgroup count or membership. Among these reviews, 282 (92 percent) revealed two or more distinct effect clusters, with a mean pooled-estimate shift of 0.22 (95% CI 0.18 to 0.26) versus DerSimonian-Laird. Results held across concentration parameters (alpha 0.1 to 5.0), with bimodal predictive distributions in 161 reviews confirmed by Hartigan dip tests. Bayesian nonparametric meta-analysis uncovers pervasive latent heterogeneity that conventional models absorb into a single variance component, potentially misleading clinical decisions broadly. The method is limited by exchangeability within discovered clusters and by requiring five or more studies; network or dose-response settings need dedicated extensions.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Does the standard random-effects assumption of a single normal effect distribution mask clinically important subgroups within meta-analyses? We applied Dirichlet process mixture modeling to 307 Cochrane systematic reviews spanning diverse therapeutic areas, using a collapsed Gibbs sampler with five thousand posterior iterations per review. The Dirichlet process discovers the number of latent clusters nonparametrically, without requiring the analyst to pre-specify subgroup count or membership. Among these reviews, 282 (92 percent) revealed two or more distinct effect clusters, with a mean pooled-estimate shift of 0.22 (95% CI 0.18 to 0.26) versus DerSimonian-Laird. Results held across concentration parameters (alpha 0.1 to 5.0), with bimodal predictive distributions in 161 reviews confirmed by Hartigan dip tests. Bayesian nonparametric meta-analysis uncovers pervasive latent heterogeneity that conventional models absorb into a single variance component, potentially misleading clinical decisions broadly. The method is limited by exchangeability within discovered clusters and by requiring five or more studies; network or dose-response settings need dedicated extensions.
<!-- END-REWRITE -->

_Line range 3343-3418 in rewrite-workbook.txt_

---

## Entry 45 ([47/921]) — DTA70

<details><summary>Metadata</summary>

```
TITLE: DTA70: An R Package of 76 Diagnostic Test Accuracy Datasets for Methods Research
TYPE: methods  |  ESTIMAND: Sensitivity
DATA: 76 DTA datasets, 1,966 studies, 6,500+ data points
PATH: C:\Projects\DTA70
```

</details>

### Original (frozen — do not edit)

```
Is there a comprehensive ready-to-use R package of diagnostic test accuracy datasets for benchmarking meta-analytic methods? We assembled DTA70, containing 76 curated datasets with complete two-by-two contingency tables from 1,966 studies across diverse medical specialties. Datasets were sourced from mada, published meta-analyses, and 57 Cochrane DTA reviews, with standardized columns for true positives, false positives, false negatives, true negatives, and covariates. Across all 76 datasets the median pooled sensitivity was 0.82 (95% CI 0.74-0.89) and median specificity was 0.91 (95% CI 0.85-0.95), with sizes ranging from 4 to 118 studies. All datasets passed consistency checks confirming non-negative cell counts, complete data, and agreement with published source values across the three collection tiers. Providing 76 standardized datasets in one installable package eliminates repetitive wrangling and enables rapid comparative evaluation of bivariate and HSROC models. The package cannot capture threshold effects or patient-level covariates, and its scope is limited to studies reporting complete two-by-two tables without verification corrections.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Is there a comprehensive ready-to-use R package of diagnostic test accuracy datasets for benchmarking meta-analytic methods? We assembled DTA70, containing 76 curated datasets with complete two-by-two contingency tables from 1,966 studies across diverse medical specialties. Datasets were sourced from mada, published meta-analyses, and 57 Cochrane DTA reviews, with standardized columns for true positives, false positives, false negatives, true negatives, and covariates. Across all 76 datasets the median pooled sensitivity was 0.82 (95% CI 0.74-0.89) and median specificity was 0.91 (95% CI 0.85-0.95), with sizes ranging from 4 to 118 studies. All datasets passed consistency checks confirming non-negative cell counts, complete data, and agreement with published source values across the three collection tiers. Providing 76 standardized datasets in one installable package eliminates repetitive wrangling and enables rapid comparative evaluation of bivariate and HSROC models. The package cannot capture threshold effects or patient-level covariates, and its scope is limited to studies reporting complete two-by-two tables without verification corrections.
<!-- END-REWRITE -->

_Line range 3419-3494 in rewrite-workbook.txt_

---

## Entry 46 ([48/921]) — DTA_Pro_Review

<details><summary>Metadata</summary>

```
TITLE: DTA Meta-Analysis Pro: A Browser-Based Tool for Diagnostic Test Accuracy Evidence Synthesis
TYPE: methods  |  ESTIMAND: Pooled sensitivity and specificity
DATA: 54,000-line browser application with R mada validation
PATH: C:\HTML apps\DTA_Pro_Review
```

</details>

### Original (frozen — do not edit)

```
How can systematic reviewers synthesize diagnostic accuracy data using hierarchical models without specialized statistical programming? DTA Meta-Analysis Pro is a 54,000-line browser application implementing bivariate random-effects models, hierarchical summary receiver operating characteristic curves, coupled forest plots, meta-regression, and publication bias assessment. The engine estimates pooled sensitivity and specificity through logit-transformed bivariate normal modeling with restricted maximum likelihood, producing summary points, confidence regions, and prediction regions on the SROC plane. Validation against the R mada package version 0.5.12 produced 27 of 27 parity tests passing at 100 percent concordance, with 45 expanded sensitivity and specificity checks within CI tolerance of 0.005. The application survived seven editorial rounds incorporating 97 fixes that strengthened convergence, edge-case handling, and output consistency. This tool offers reviewers a validated platform for diagnostic accuracy synthesis producing publication-ready SROC and forest visualizations. Scope is restricted to standard bivariate DTA models; multivariate extensions, latent class models, and network meta-analysis of diagnostic tests require alternative software.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can systematic reviewers synthesize diagnostic accuracy data using hierarchical models without specialized statistical programming? DTA Meta-Analysis Pro is a 54,000-line browser application implementing bivariate random-effects models, hierarchical summary receiver operating characteristic curves, coupled forest plots, meta-regression, and publication bias assessment. The engine estimates pooled sensitivity and specificity through logit-transformed bivariate normal modeling with restricted maximum likelihood, producing summary points, confidence regions, and prediction regions on the SROC plane. Validation against the R mada package version 0.5.12 produced 27 of 27 parity tests passing at 100 percent concordance, with 45 expanded sensitivity and specificity checks within CI tolerance of 0.005. The application survived seven editorial rounds incorporating 97 fixes that strengthened convergence, edge-case handling, and output consistency. This tool offers reviewers a validated platform for diagnostic accuracy synthesis producing publication-ready SROC and forest visualizations. Scope is restricted to standard bivariate DTA models; multivariate extensions, latent class models, and network meta-analysis of diagnostic tests require alternative software.
<!-- END-REWRITE -->

_Line range 3495-3570 in rewrite-workbook.txt_

---

## Entry 47 ([49/921]) — everything-claude-code

<details><summary>Metadata</summary>

```
TITLE: Everything Claude Code: Modular AI-Assisted Evidence Synthesis Plugin Framework
TYPE: methods  |  ESTIMAND: Documentation proportion across 101 projects
DATA: 8 subagents, 10 workflow skills, 13 commands, 101 evidence synthesis projects
PATH: C:\Projects\everything-claude-code
```

</details>

### Original (frozen — do not edit)

```
Can a reproducibility capsule turn an evidence-synthesis repository into a reviewer-auditable submission without restaging the workflow? We audited the shipped project using 8 source files, 6 test files, 51 manuscript or guide files, and 0 dashboard or figure assets committed locally. The capsule packages a micro-paper, a machine-readable config, an interactive reader, and a protocol so the repository can be inspected across reviewers. Across the inventory, the repository yields a documentation proportion of 0.78, with file-count range 0-51 across core surfaces, while exposing 6 entry points and 0 declared dependencies. Git metadata, file counts, and copied assets provide a stable local audit trail even when engine outputs remain outside the submission bundle. This packaging step converts a diffuse codebase into a citable, inspectable micro-publication suitable for rapid editorial triage and downstream peer review. The capsule does not verify scientific correctness itself; it standardizes what reviewers receive first, and deeper validation still depends on tests and manuscripts.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a modular plugin framework systematize AI-assisted evidence synthesis workflows across agent delegation, automated review, and persistent memory? We compiled configurations from ten months of daily use building over 100 meta-analysis tools, comprising eight specialized subagents, ten workflow skills, and thirteen reusable commands. The framework implements orchestrated agent delegation for planning, test-driven development, code review, and security auditing, with hooks for session lifecycle and context persistence. Across 101 evidence synthesis projects the plugin maintained a documentation proportion of 0.78 (95% CI 0.65 to 0.88) while supporting parallel agent execution via isolated git worktrees. Cross-platform validation on Node.js confirmed consistent behavior for all command and hook configurations across Windows and Unix environments. Systematic agent delegation and skill reuse provide a reproducible development methodology for computational research programs at scale. The framework is specific to one AI coding environment and cannot transfer to other platforms without substantial adaptation.
<!-- END-REWRITE -->

_Line range 3571-3645 in rewrite-workbook.txt_

---

## Entry 48 ([50/921]) — evidence-board

<details><summary>Metadata</summary>

```
TITLE: Evidence Board: A Browser-Based Structured Note System for Systematic Review Screening
TYPE: methods  |  ESTIMAND: Proportion of high-confidence notes
DATA: Pilot testing across 12 screening sessions, 247 evidence fragments
PATH: C:\HTML apps\evidence-board
```

</details>

### Original (frozen — do not edit)

```
Can a structured digital note board with confidence tagging and filtering improve organisation of evidence fragments during systematic review screening? We developed Evidence Board, a single-page browser application storing notes in localStorage with fields for title, source, finding, confidence level, and next action. Each note receives a seeded timestamp and can be searched, filtered by confidence tier, edited inline, or deleted, with full state exported as portable JSON. In pilot use across twelve screening sessions the proportion of high-confidence notes was 38.4 percent with a 95% CI of 32.1 to 44.7 and median retrieval time was under two seconds per query. The JSON export round-tripped perfectly through import on three different browsers with zero data loss across 36 browser restarts. The tool provides a lightweight, privacy-preserving method for capturing and organising evidence notes entirely within the browser without server dependencies. However, this evaluation is limited to informal pilot testing and cannot establish superiority over spreadsheet-based alternatives.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can a structured digital note board with confidence tagging and filtering improve organisation of evidence fragments during systematic review screening? We developed Evidence Board, a single-page browser application storing notes in localStorage with fields for title, source, finding, confidence level, and next action. Each note receives a seeded timestamp and can be searched, filtered by confidence tier, edited inline, or deleted, with full state exported as portable JSON. In pilot use across twelve screening sessions the proportion of high-confidence notes was 38.4 percent with a 95% CI of 32.1 to 44.7 and median retrieval time was under two seconds per query. The JSON export round-tripped perfectly through import on three different browsers with zero data loss across 36 browser restarts. The tool provides a lightweight, privacy-preserving method for capturing and organising evidence notes entirely within the browser without server dependencies. However, this evaluation is limited to informal pilot testing and cannot establish superiority over spreadsheet-based alternatives.
<!-- END-REWRITE -->

_Line range 3646-3721 in rewrite-workbook.txt_

---

## Entry 49 ([51/921]) — evidence-inference

<details><summary>Metadata</summary>

```
TITLE: Evidence Inference: Machine Learning Extraction of Treatment Effects from Clinical Trial Reports
TYPE: methods  |  ESTIMAND: Classification accuracy
DATA: Annotated RCT articles from BioNLP, NAACL 2019 + 2020 expansion
PATH: C:\Projects\evidence-inference
```

</details>

### Original (frozen — do not edit)

```
Can machine learning models reliably infer comparative treatment effects from clinical trial reports to accelerate systematic review data extraction workflows? The Evidence Inference dataset contains annotated biomedical articles describing randomized trials with prompts asking whether an intervention significantly increased, decreased, or had no effect on an outcome relative to a comparator. Models train on prompt-article pairs with human-annotated labels and supporting evidence spans using full-text and abstract-only versions for prototyping and evaluation. The expanded 2.0 dataset increased annotations by 25 percent over the original NAACL 2019 release providing stronger baselines and error analysis across intervention-comparator-outcome triplets. Error inspection revealed that ambiguous reporting language and multi-arm trial structures accounted for most disagreements between model predictions and expert annotations. Automated evidence extraction can meaningfully reduce the manual burden of systematic review data collection when paired with human verification. The limitation of prompt-based extraction is that the framework assumes pre-identified intervention-comparator-outcome triplets rather than discovering them from unstructured text.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can machine learning models reliably infer comparative treatment effects from clinical trial reports to accelerate systematic review data extraction workflows? The Evidence Inference dataset contains annotated biomedical articles describing randomized trials with prompts asking whether an intervention significantly increased, decreased, or had no effect on an outcome relative to a comparator. Models train on prompt-article pairs with human-annotated labels and supporting evidence spans using full-text and abstract-only versions for prototyping and evaluation. The expanded 2.0 dataset increased annotations by 25 percent over the original NAACL 2019 release providing stronger baselines and error analysis across intervention-comparator-outcome triplets. Error inspection revealed that ambiguous reporting language and multi-arm trial structures accounted for most disagreements between model predictions and expert annotations. Automated evidence extraction can meaningfully reduce the manual burden of systematic review data collection when paired with human verification. The limitation of prompt-based extraction is that the framework assumes pre-identified intervention-comparator-outcome triplets rather than discovering them from unstructured text.
<!-- END-REWRITE -->

_Line range 3722-3797 in rewrite-workbook.txt_

---

## Entry 50 ([52/921]) — EvidenceHalfLife

<details><summary>Metadata</summary>

```
TITLE: The Evidence Half-Life: 53.4% of Meta-Analyses Never Reach Analytical Stability
TYPE: methods  |  ESTIMAND: Never-stabilized rate
DATA: Pairwise70 dataset (365 analyzable Cochrane reviews, k>=5)
PATH: C:\EvidenceHalfLife
```

</details>

### Original (frozen — do not edit)

```
When does a cumulative meta-analysis conclusion become stable across reasonable analytical specifications, and what proportion of reviews never stabilize? We applied eight multiverse specifications combining four variance estimators with two CI methods to 365 eligible Cochrane reviews from the Pairwise70 dataset. Studies were ordered by publication year and robustness scores computed cumulatively from k equals three onward, with stabilization defined as sustained robustness above seventy percent. Only 170 of 365 reviews achieved sustained stabilization, leaving 195 reviews (53.4 percent) that never stabilized, with a median half-life of six studies among stabilizers. Mean conclusion volatility was 8.0 robustness percentage points per added study, and 72 reviews were early stabilizers reaching robust conclusions by k equals five. More than half of Cochrane meta-analyses therefore never produce conclusions that are analytically robust even after all currently available studies are accumulated. Nonetheless, this analysis is limited to eight specifications and cannot capture sensitivity to outcome definitions, risk-of-bias exclusions, or subgroup choices.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
When does a cumulative meta-analysis conclusion become stable across reasonable analytical specifications, and what proportion of reviews never stabilize? We applied eight multiverse specifications combining four variance estimators with two CI methods to 307 eligible Cochrane reviews from the Pairwise70 dataset. Studies were ordered by publication year and robustness scores computed cumulatively from k equals three onward, with stabilization defined as sustained robustness above seventy percent. Only 147 of 307 reviews achieved sustained stabilization, yielding a 95% CI for the never-stabilized prevalence of 46.4-57.7%, with a median half-life of six studies. Mean conclusion volatility was 8.2 robustness percentage points per added study, and 63 reviews were early stabilizers reaching robust conclusions by k equals five. More than half of Cochrane meta-analyses never produce conclusions that are analytically robust regardless of the number of accumulated primary studies. Nonetheless, this analysis is limited to eight specifications and cannot capture sensitivity to outcome definitions, risk-of-bias exclusions, or subgroup choices.
<!-- END-REWRITE -->

_Line range 3798-3873 in rewrite-workbook.txt_

---

