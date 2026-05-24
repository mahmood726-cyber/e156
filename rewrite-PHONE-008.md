# Rewrite chunk 008 — entries 351-400

_Previous: rewrite-PHONE-007.md | Next: rewrite-PHONE-009.md | Index: rewrite-PHONE-INDEX.md_

Edit ONLY the `YOUR REWRITE` section under each entry. The `Original`
block is frozen — do not edit it. Save the file when done. On your
laptop run `python C:\E156\merge-rewrite.py` to assemble a new
workbook (`rewrite-workbook.NEW.txt`) with your edits applied.

---

## Entry 351 ([355/921]) — SAARCe156Students

<details><summary>Metadata</summary>

```
TITLE: SAARC Clinical Trial Equity: 190 E156 Micro-Papers for Ziauddin Medical University
TYPE: methods  |  ESTIMAND: Gini coefficient of trial distribution
DATA: ClinicalTrials.gov API v2 (8 SAARC nations)
PATH: C:\saarc-e156-students
```

</details>

### Original (frozen — do not edit)

```
How equitably are clinical trials distributed across the eight SAARC nations, and what structural inequities shape South Asia's research landscape? This cross-sectional registry audit evaluated interventional trials across India, Pakistan, Bangladesh, Sri Lanka, Nepal, Afghanistan, Bhutan, and Maldives using ClinicalTrials.gov API v2 data. We computed Gini coefficients, Herfindahl-Hirschman indices, bootstrap confidence intervals, and 28 additional statistical methods across 190 structured analyses spanning geographic equity, disease burden concordance, governance sovereignty, methodological rigor, and a 50-paper Pakistan deep-dive. India accounts for over 80% of regional trial volume while Pakistan, Bangladesh, and smaller nations face severe per-capita research deficits with Gini exceeding 0.75. Sensitivity analyses using Theil decomposition, permutation tests, and Bayesian rate estimation confirmed inequality persistence across all analytical specifications. These findings reveal that SAARC clinical research capacity mirrors broader economic disparities rather than population health needs. Registry-only analysis cannot capture unregistered trials or assess within-country subnational variation beyond Pakistan's provincial breakdown.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26477-26550 in rewrite-workbook.txt_

---

## Entry 352 ([356/921]) — IHMEDataLakehouse

<details><summary>Metadata</summary>

```
TITLE: IHME Data Lakehouse: Registry-Driven GBD Pipeline for 6 Domains
TYPE: methods  |  ESTIMAND: Dataset coverage (N parquet datasets)
DATA: IHME GHDx bulk CSV exports (GBD 2021)
PATH: D:\Projects\ihme-data-lakehouse
```

</details>

### Original (frozen — do not edit)

```
What coverage does IHME's Global Burden of Disease data achieve when systematically catalogued through an automated lakehouse pipeline? We process six GBD data domains — cause-level results, risk factor attribution, covariates, population estimates, forecasts, and specialty datasets — spanning 369 diseases, 87 risk factors, and 204 countries from 1990 to 2021. A registry-driven Python pipeline fetches bulk CSV exports from known GHDx URLs, validates schemas, and promotes data through bronze and silver tiers preserving IHME's hierarchical coding. The lakehouse yields analysis-ready parquet datasets with dual schema: IHME-native for full fidelity and harmonized (iso3c/year/value) for cross-source joins. Checksums and manifests ensure provenance for files fetched via stable URLs. This infrastructure enables reproducible downstream analyses by eliminating ad-hoc data wrangling from IHME's bulk exports. Coverage gaps exist for datasets requiring authenticated GHDx access, which fall back to manual placement.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26551-26624 in rewrite-workbook.txt_

---

## Entry 353 ([357/921]) — CardioSynth

<details><summary>Metadata</summary>

```
TITLE: CardioSynth: Living Cardiology Evidence Synthesis Engine
TYPE: methods  |  ESTIMAND: Pooled risk ratio (MACE)
DATA: ClinicalTrials.gov API v2 structured results
PATH: C:\cardiosynth
```

</details>

### Original (frozen — do not edit)

```
Does colchicine reduce major adverse cardiovascular events after ST-elevation myocardial infarction? We synthesised randomised controlled trials from ClinicalTrials.gov structured results data, using dual-agent extraction with TruthCert validation across ten integrity checks. DerSimonian-Laird random-effects meta-analysis with Hartung-Knapp-Sidik-Jonkman correction pooled log risk ratios and back-transformed to the natural scale. The pooled risk ratio for MACE was extracted from all trials with posted results matching colchicine and myocardial infarction, with individual study estimates displayed in an inline SVG forest plot. Leave-one-out analysis confirmed robustness to exclusion of any single trial and the prediction interval quantified between-study heterogeneity beyond sampling error. Colchicine may reduce MACE after STEMI based on current evidence from ClinicalTrials.gov posted results, though the evidence base requires continuous monitoring as new trials complete. This living synthesis excludes grey literature, unpublished endpoints, and individual patient data beyond structured registry submissions.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26625-26698 in rewrite-workbook.txt_

---

## Entry 354 ([358/921]) — SuperTransportabilityMap

<details><summary>Metadata</summary>

```
TITLE: SuperTransportabilityMap: Global Generalization of ClinicalTrials.gov Evidence via Multi-Lake Demographic Calibration
TYPE: methods  |  ESTIMAND: Transportability Index (cross-regional generalization probability)
DATA: ClinicalTrials.gov (all data), IHME GBD, WHO GHO, World Bank WDI
PATH: C:\Projects\SuperTransportabilityMap
```

</details>

### Original (frozen — do not edit)

```
Can evidence from any published meta-analysis be automatically recalibrated for different global populations by projecting ClinicalTrials.gov cohorts onto demographic data lakes? We developed the SuperTransportabilityMap, an interactive dashboard linking all interventional trials in ClinicalTrials.gov to global demographic baselines from IHME, WHO, and the World Bank. The pipeline computes a Transportability Index, quantifying the distributional distance between trial-specific baseline characteristics and target population demographics across 195 countries. By applying inverse probability of participation weighting, the engine recalibrates any published meta-analytic treatment effect for specific national contexts. The web dashboard provides real-time choropleth visualizations, identifying regions where existing evidence is highly transportable versus domains requiring localized trials. Validation against multiregional mega-trials demonstrated a 34 percent reduction in out-of-sample prediction error for regional treatment effects compared to unadjusted pooling. The approach is limited by the frequent underreporting of granular demographic covariates in historical registry data.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26699-26773 in rewrite-workbook.txt_

---

## Entry 355 ([359/921]) — LivingMA-PFA-AF

<details><summary>Metadata</summary>

```
TITLE: PFA in AF: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\PFA_AF_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for pulsed-field ablation versus thermal ablation for atrial fibrillation? The v13 app ingested 3 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the ADVENT/CHAMPION/PULSED-AF pivotal cohort within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for pulsed-field ablation versus thermal ablation for atrial fibrillation without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26774-26847 in rewrite-workbook.txt_

---

## Entry 356 ([360/921]) — LivingMA-Watchman-Amulet

<details><summary>Metadata</summary>

```
TITLE: Watchman vs Amulet LAAO: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\LivingMeta_Watchman_Amulet
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for Amulet versus Watchman left atrial appendage occlusion? The v13 app ingested 2 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the AMULET IDE + SWISS-APERO pooled benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for Amulet versus Watchman left atrial appendage occlusion without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26848-26921 in rewrite-workbook.txt_

---

## Entry 357 ([361/921]) — LivingMA-Tricuspid-TEER

<details><summary>Metadata</summary>

```
TITLE: Tricuspid TEER: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\Tricuspid_TEER_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for transcatheter edge-to-edge repair for tricuspid regurgitation? The v13 app ingested 4 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the TRILUMINATE pivotal pooled benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for transcatheter edge-to-edge repair for tricuspid regurgitation without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26922-26995 in rewrite-workbook.txt_

---

## Entry 358 ([362/921]) — LivingMA-Inclisiran

<details><summary>Metadata</summary>

```
TITLE: Inclisiran siRNA PCSK9: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\Inclisiran_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for inclisiran siRNA PCSK9 therapy for LDL reduction? The v13 app ingested 4 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the Qiao 2026 ORION-pooled benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for inclisiran siRNA PCSK9 therapy for LDL reduction without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 26996-27069 in rewrite-workbook.txt_

---

## Entry 359 ([363/921]) — LivingMA-Tirzepatide

<details><summary>Metadata</summary>

```
TITLE: Tirzepatide CV/Obesity: A Transparent Living Meta-Analysis v13
TYPE: living-ma  |  ESTIMAND: RR
DATA: SURMOUNT-series RCTs deployed; ~3,148 patients across currently ingested trials
PATH: C:\Projects\Tirzepatide_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for tirzepatide in cardiometabolic disease? The v13 app ingested SURMOUNT-series RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex, with 3,148 patients across currently extracted trials. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the Lim 2026 SURMOUNT pooled benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for tirzepatide in cardiometabolic disease without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27070-27143 in rewrite-workbook.txt_

---

## Entry 360 ([364/921]) — LivingMA-Semaglutide-HFpEF

<details><summary>Metadata</summary>

```
TITLE: Semaglutide in HFpEF: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\Semaglutide_HFpEF_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for semaglutide in HFpEF with obesity? The v13 app ingested 3 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the Duhan 2025 STEP-HFpEF pooled benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for semaglutide in HFpEF with obesity without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27144-27217 in rewrite-workbook.txt_

---

## Entry 361 ([365/921]) — LivingMA-Leadless-Pacing

<details><summary>Metadata</summary>

```
TITLE: Leadless Cardiac Pacing: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: HR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\Leadless_Pacing_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for leadless pacing devices (Micra, Aveir)? The v13 app ingested 6 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged hazard ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled hazard ratio was concordant with the Ngo 2021 leadless-pacing pooled benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for leadless pacing devices (Micra, Aveir) without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27218-27291 in rewrite-workbook.txt_

---

## Entry 362 ([366/921]) — LivingMA-CSP

<details><summary>Metadata</summary>

```
TITLE: CSP vs BiV-CRT: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\CSP_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for conduction-system pacing (His-bundle, left-bundle-branch area)? The v13 app ingested 5 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the HOT-CRT and PhysioSync pooled benchmarks within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for conduction-system pacing (His-bundle, left-bundle-branch area) without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27292-27365 in rewrite-workbook.txt_

---

## Entry 363 ([367/921]) — LivingMA-Coronary-IVL

<details><summary>Metadata</summary>

```
TITLE: Coronary IVL: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\Coronary_IVL_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for coronary intravascular lithotripsy for calcified lesions? The v13 app ingested 6 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the Kereiakes 2021 DISRUPT series benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for coronary intravascular lithotripsy for calcified lesions without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27366-27439 in rewrite-workbook.txt_

---

## Entry 364 ([368/921]) — LivingMA-Omecamtiv

<details><summary>Metadata</summary>

```
TITLE: Omecamtiv Mecarbil HFrEF: A Transparent Living Meta-Analysis v13
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalisation
DATA: 1 RCT (GALACTIC-HF), 8,232 patients; single-trial state
PATH: C:\Projects\Omecamtiv_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does omecamtiv mecarbil, a cardiac myosin activator, reduce cardiovascular events in chronic heart failure with reduced ejection fraction? One randomized placebo-controlled trial is currently deployed in this living meta-analysis: GALACTIC-HF enrolled 8,232 patients with chronic HFrEF and elevated NT-proBNP and compared omecamtiv mecarbil against placebo. Single-trial inverse-variance estimate used the original publication's Cox model hazard ratio and confidence interval. GALACTIC-HF reported a hazard ratio of 0.92 (95% CI 0.86 to 0.99) for the primary composite of cardiovascular death or heart failure hospitalisation. The effect just crosses statistical significance, with an eight percent relative risk reduction that translates to modest absolute event reduction. Omecamtiv mecarbil reduces cardiovascular events by a small margin in chronic HFrEF, and clinical relevance remains debated. Single-trial evidence is the current state; regulatory approval was not granted, limiting real-world data accumulation and further meta-analytic pooling.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27440-27513 in rewrite-workbook.txt_

---

## Entry 365 ([369/921]) — LivingMA-CTFFR

<details><summary>Metadata</summary>

```
TITLE: CT-FFR Guided Revasc: A Transparent Living Meta-Analysis v13
TYPE: methods  |  ESTIMAND: RR
DATA: ClinicalTrials.gov, PubMed, OpenAlex
PATH: C:\Projects\CTFFR_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can a browser-based transparent living meta-analysis reproduce published pooled estimates for coronary CT angiography-derived fractional flow reserve? The v13 app ingested 4 RCTs from ClinicalTrials.gov cross-checked against PubMed and OpenAlex. DerSimonian-Laird random-effects pooling with HKSJ correction ran in-browser on the logged risk ratio, with cumulative, provenance, QA, and cross-validation engines logging every step. The pooled risk ratio was concordant with the Di Pietro 2025 PRECISE/FORECAST pooled benchmark within lockdown tolerance, and estimates update live as trials are ingested. Cross-validation against R metafor and Python scipy scripts reproduced the pooled point estimate, and leave-one-out plus REML-versus-HKSJ sensitivity preserved direction. A transparent browser-native pipeline matches benchmark pooled effects for coronary CT angiography-derived fractional flow reserve without server-side computation while surfacing every provenance decision. The app inherits CT.gov and PubMed coverage gaps, cannot synthesize unpublished data, and updates require manual re-ingestion.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27514-27587 in rewrite-workbook.txt_

---

## Entry 366 ([370/921]) — LivingMA-Vericiguat

<details><summary>Metadata</summary>

```
TITLE: Vericiguat in HF: A Transparent Living Meta-Analysis v13
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 3 RCTs (VICTORIA, VITALITY-HFpEF, SOCRATES-REDUCED), ~6,295 patients
PATH: C:\Projects\Vericiguat_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does vericiguat reduce cardiovascular death or heart failure hospitalization in symptomatic heart failure patients across ejection fraction strata? Three randomized placebo-controlled trials enrolling approximately 6,295 patients spanning worsening HFrEF (VICTORIA), HFpEF (VITALITY-HFpEF), and Phase 2 dose-ranging HFrEF (SOCRATES-REDUCED) were pooled. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction on trials reporting matched cardiovascular composite endpoints. The pooled estimate was driven by VICTORIA's hazard ratio of 0.90 (95% CI 0.82-0.98), with VITALITY-HFpEF finding no KCCQ improvement and SOCRATES-REDUCED contributing only dose-ranging Phase 2 signals on NT-proBNP. Leave-one-out sensitivity showed the overall direction depended on VICTORIA, with VITALITY-HFpEF and SOCRATES-REDUCED lacking power for hard cardiovascular endpoints. Vericiguat modestly reduces cardiovascular death or heart failure hospitalization in worsening HFrEF populations who can tolerate hypotension. The evidence base is dominated by a single positive trial, HFpEF benefit is unestablished, and symptomatic hypotension and syncope limit uptitration.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27588-27661 in rewrite-workbook.txt_

---

## Entry 367 ([371/921]) — LivingMA-Sotagliflozin

<details><summary>Metadata</summary>

```
TITLE: Sotagliflozin SGLT1/2i: A Transparent Living Meta-Analysis v13
TYPE: living-ma  |  ESTIMAND: HR for CV composite
DATA: 2 RCTs (SCORED, SOLOIST-WHF), 11,806 patients
PATH: C:\Projects\Sotagliflozin_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does sotagliflozin, a dual SGLT1 and SGLT2 inhibitor, reduce cardiovascular events in type 2 diabetes or acute heart failure? Two randomized placebo-controlled trials deployed in this living meta-analysis (SCORED, SOLOIST-WHF) enrolled 11,806 patients with type 2 diabetes or recent heart failure decompensation. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the two deployed trials. The pooled hazard ratio for the primary cardiovascular composite was 0.72 (95% CI 0.63 to 0.82), with no detectable heterogeneity (I-squared 0 percent). SCORED (HR 0.74) and SOLOIST-WHF (HR 0.67) both favour sotagliflozin, with consistent direction across chronic type 2 diabetes and acute heart failure populations. Sotagliflozin reduces cardiovascular events by approximately twenty-eight percent across chronic diabetes and acute heart failure settings. SOLOIST-WHF was terminated early, acute post-discharge windows may differ from chronic use, and ketoacidosis risk requires continued monitoring.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27662-27741 in rewrite-workbook.txt_

---

## Entry 368 ([373/921]) — modern-stats-global-health

<details><summary>Metadata</summary>

```
TITLE: Modern Non-Parametrics in Global Health: Integrating IHME, WHO, World Bank, and ClinicalTrials.gov Data
TYPE: methods  |  ESTIMAND: Non-parametric effect estimate (delta from linear baseline)
DATA: IHME GBD, World Bank WDI, WHO GHO, ClinicalTrials.gov API v2
PATH: C:\Users\user\modern-stats-global-health
```

</details>

### Original (frozen — do not edit)

```
Can modern non-parametric statistical methods improve the identification of global health trends across heterogeneous datasets? We harmonized open-access datasets from IHME, World Bank, WHO, and ClinicalTrials.gov covering global health indicators and interventional trial metadata. Modern non-parametric techniques, including generalized additive models and non-parametric causal inference, were applied to detect non-linear associations without parametric assumptions. The analysis revealed significant non-linear shifts in health outcomes, with non-parametric estimates diverging from linear baselines by 9 percent (95% CI 7 to 11) in high-volatility regions. Sensitivity analysis using fixed-seed bootstrap and TruthCert cryptographic hashing confirmed the stability and provenance of all derived estimates. These results suggest that non-parametric models capture critical epidemiological transitions that standard linear models systematically overlook. The study is limited to publicly available registry data and cannot account for country-specific reporting biases or unregistered trials.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27742-27815 in rewrite-workbook.txt_

---

## Entry 369 ([488/921]) — DCB_PAD_LivingMeta

<details><summary>Metadata</summary>

```
TITLE: Drug-Coated Balloons for Femoropopliteal PAD: A Living Systematic Review
TYPE: clinical  |  ESTIMAND: RR of primary patency at 12 months
DATA: ClinicalTrials.gov (IN.PACT SFA, ILLUMENATE, RANGER, PACCOCATH, LEVANT 2)
PATH: C:\Projects\DCB_PAD_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Do paclitaxel drug-coated balloons improve femoropopliteal patency versus plain balloon angioplasty in peripheral artery disease? We identified five randomized controlled trials from ClinicalTrials.gov comparing DCB to PTA in 1,299 patients with symptomatic femoropopliteal disease (IN.PACT SFA, ILLUMENATE Pivotal, RANGER SFA, PACCOCATH-FEM, LEVANT 2). Random-effects meta-analysis of binary patency outcomes was performed using the Mantel-Haenszel method with REML heterogeneity estimation. Pooled primary patency at 12 months favored DCB over PTA across all five trials, with clinically-driven target lesion revascularization rates consistently lower in DCB arms (range 2.4-15.6% vs 16.8-40.5%). Sensitivity analyses addressing the Katsanos 2018 late mortality signal found no significant excess mortality through 5 years in individual-patient-data meta-analysis (HR 1.08, 95% CI 0.72-1.61). These findings support DCB as superior to PTA for femoropopliteal patency, with the FDA advisory panel confirming favorable benefit-risk. The analysis is limited to paclitaxel-based DCBs and cannot address newer sirolimus-coated devices.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27816-27889 in rewrite-workbook.txt_

---

## Entry 370 ([489/921]) — Orforglipron_LivingMeta

<details><summary>Metadata</summary>

```
TITLE: Orforglipron for Cardiometabolic Disease: A Living Systematic Review
TYPE: clinical  |  ESTIMAND: HbA1c change and percent body weight change
DATA: ClinicalTrials.gov (Phase 2 T2DM, Phase 2 Obesity, ACHIEVE-1/3/4/5, ATTAIN-1/2)
PATH: C:\Projects\Orforglipron_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Can oral orforglipron, a non-peptide GLP-1 receptor agonist, achieve clinically meaningful glycemic and weight outcomes in type 2 diabetes and obesity? We identified eight interventional trials from ClinicalTrials.gov spanning Phase 2 dose-finding through Phase 3 pivotal programs (ACHIEVE and ATTAIN series), enrolling over 13,900 participants. Evidence mapping was performed for trials with published results, with meta-analytic pooling planned as Phase 3 data mature. In Phase 2, orforglipron 36-45mg reduced HbA1c by 1.50-1.67 percentage points versus placebo (P<0.001) and body weight by 9.4-14.7 percent versus 2.0 percent with placebo at 36 weeks. Dose-response analysis confirmed monotonic improvements across 12-45mg doses for both glycemic and weight endpoints. These Phase 2 results position orforglipron as the first oral non-peptide GLP-1 RA with efficacy comparable to injectable agents, pending Phase 3 confirmation. The analysis is limited to early-phase data, with six Phase 3 trials recently completed but not yet reporting results.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27890-27966 in rewrite-workbook.txt_

---

## Entry 371 ([374/921]) — MendelianMR

<details><summary>Metadata</summary>

```
TITLE: Browser-Based Mendelian Randomization with Five Estimators and Pleiotropy Diagnostics
TYPE: methodological  |  ESTIMAND: Causal OR via genetic instruments (IVW)
DATA: Published GWAS summary statistics (LDL-CHD, BMI-T2DM, SBP-Stroke, CRP-CHD)
PATH: C:\MendelianMR
```

</details>

### Original (frozen — do not edit)

```
Can browser-based Mendelian randomization replicate the causal inference pipeline traditionally requiring R or Stata packages? We implemented five MR methods -- inverse-variance weighted (fixed and random effects), MR-Egger regression, weighted median, simple median, and MR-PRESSO outlier detection -- as a single-file HTML application using JavaScript matrix algebra. Each method estimator was coded from first principles: IVW as weighted regression through the origin, MR-Egger as weighted regression with intercept (InSIDE assumption), and weighted median via sorted Wald ratios with bootstrap standard errors (1,000 replicates, seeded PRNG). Applied to 28 LDL-cholesterol SNPs and coronary heart disease, the tool produces IVW OR, Cochran Q heterogeneity, MR-Egger intercept test, F-statistics for instrument strength, and MR-PRESSO global and outlier tests with Bonferroni correction. Sensitivity analyses include leave-one-out IVW, scatter, forest, and funnel plots with method-specific regression lines. The tool fills a gap in browser-based causal inference, enabling MR analysis without software installation. This implementation is limited to two-sample summary-level MR and does not support multivariable MR or sample overlap corrections.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 27967-28041 in rewrite-workbook.txt_

---

## Entry 372 ([375/921]) — SafetyMA

<details><summary>Metadata</summary>

```
TITLE: Pharmacovigilance Meta-Analysis with Peto OR and Sequential Safety Monitoring
TYPE: methodological  |  ESTIMAND: Peto OR for rare adverse events
DATA: Rosiglitazone CV trials (Nissen 2007), SSRI suicidality, NSAID GI bleeding
PATH: C:\SafetyMA
```

</details>

### Original (frozen — do not edit)

```
Can a browser tool perform pharmacovigilance meta-analysis with the statistical rigor required for rare safety outcomes? We implemented three pooling methods -- Peto odds ratio (no continuity correction), Mantel-Haenszel with Robins-Breslow-Greenland variance, and DerSimonian-Laird random effects -- with explicit handling of zero-cell and double-zero studies. Zero-cell corrections include traditional (0.5), reciprocal of treatment-arm balance, and Sweeting empirical method; double-zero studies are excluded by default since they carry no information for the odds ratio. Applied to the Nissen 2007 rosiglitazone dataset (42 trials, 27 with zero events), Peto OR replicates the landmark finding of increased myocardial infarction risk. Sequential safety monitoring uses cumulative Peto OR with O'Brien-Fleming spending boundaries (z_alpha / sqrt(information fraction)) to detect emerging signals without inflating type I error. Visualizations include forest plots, L'Abbe risk plots, cumulative monitoring charts, and funnel plots. The tool does not support time-to-event safety outcomes or network pharmacovigilance across multiple drugs.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28042-28116 in rewrite-workbook.txt_

---

## Entry 373 ([376/921]) — PredModelMA

<details><summary>Metadata</summary>

```
TITLE: Prediction Model Validation Meta-Analysis with PROBAST Risk of Bias
TYPE: methodological  |  ESTIMAND: Pooled c-statistic (logit) and O:E ratio (log)
DATA: Framingham (10 validations), SCORE2 (7), QRISK3 (6)
PATH: C:\PredModelMA
```

</details>

### Original (frozen — do not edit)

```
Can prediction model validation studies be synthesized in a browser with the same statistical rigor as R packages like metamisc? We implemented c-statistic pooling via logit transformation (logit(c) = log(c/(1-c))) with delta-method standard errors (SE(logit) = SE(c)/(c(1-c))), and O:E ratio pooling on the natural log scale, both using REML or DerSimonian-Laird random effects. PROBAST risk-of-bias assessment covers four domains (Participants, Predictors, Outcome, Analysis) with traffic-light visualization and domain-level bar charts. Applied to 10 Framingham Risk Score external validations, the tool yields pooled c = 0.742 (95% CI 0.731-0.753) and pooled O:E = 1.09 (1.03-1.16), indicating moderate discrimination with slight underprediction -- consistent with published systematic reviews. Forest plots display study-level estimates with weight-proportional symbols and pooled diamonds for both discrimination and calibration. The tool enables rapid prediction model evidence synthesis without software installation or programming. This implementation does not support calibration-in-the-large meta-regression or net benefit decision curve pooling.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28117-28191 in rewrite-workbook.txt_

---

## Entry 374 ([377/921]) — RetractionImpact

<details><summary>Metadata</summary>

```
TITLE: Retraction Fragility Index -- Quantifying Meta-Analysis Robustness to Study Retractions
TYPE: meta-scientific  |  ESTIMAND: RFI (minimum retractions to reverse significance)
DATA: Statin mortality (11 trials), Ivermectin-COVID (7), Surgery vs Medical (7)
PATH: C:\RetractionImpact
```

</details>

### Original (frozen — do not edit)

```
How many study retractions would be needed to reverse the conclusion of a meta-analysis? We introduce the Retraction Fragility Index (RFI), the minimum number of studies whose removal changes a pooled result from significant to non-significant or vice versa. The pipeline quantifies leave-one-out influence, identifies the most influential study, and traces p-value decay as studies are removed in order of maximum impact. Applied to landmark statin mortality trials (11 studies, HR 0.87), the RFI exceeded the tested depth, indicating robust conclusions. A simulated ivermectin-COVID dataset (7 studies) yielded RFI = 1, so a single retraction reversed significance. Outputs include impact waterfall charts, fragility curves with an alpha 0.05 threshold, and leave-one-out forest plots with reversal flags. The method extends fragility analysis from within-study event changes to between-study retraction scenarios, but it does not model correlated retractions from the same research group or institution.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28192-28266 in rewrite-workbook.txt_

---

## Entry 375 ([378/921]) — LivingNMA

<details><summary>Metadata</summary>

```
TITLE: Browser-Based Living Network Meta-Analysis with Consistency Assessment and P-Scores
TYPE: methodological  |  ESTIMAND: Network treatment effects via graph-theoretic WLS
DATA: Anti-hypertensives (12 trials), Antidepressants (8), DOACs for AF (6)
PATH: C:\LivingNMA
```

</details>

### Original (frozen — do not edit)

```
Can frequentist network meta-analysis -- including consistency assessment and treatment ranking -- be performed entirely in a web browser? We implemented the graph-theoretic NMA framework (Ruecker 2012) using JavaScript matrix algebra: the design matrix X encodes treatment contrasts, weighted least squares yields beta = (X'WX)^(-1)X'WY, and the variance-covariance matrix provides all pairwise comparisons simultaneously. Consistency is assessed globally via the Q statistic decomposition (total Q minus within-design Q) and locally via node-splitting, which separates direct from indirect evidence for each comparison with direct data. Treatment rankings use P-scores -- the frequentist analogue of SUCRA -- computed as the mean probability of each treatment being superior across all pairwise comparisons. Applied to 12 anti-hypertensive trials across 6 treatments, the tool produces a network graph, league table, forest plots, and rankograms consistent with published NMA results. The living update feature enables sequential re-analysis as new trials emerge, tracking estimate evolution over time. This implementation assumes a common heterogeneity parameter across comparisons and does not handle multi-arm trial covariance adjustment.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28267-28340 in rewrite-workbook.txt_

---

## Entry 376 ([490/921]) — AuthorshipLedger

<details><summary>Metadata</summary>

```
TITLE: AuthorshipLedger: DOI Deposit and Contributor Resolution for the C Drive Portfolio
TYPE: methods  |  ESTIMAND: proportion of indexed projects reaching full DOI-registrable state
DATA: Governance and deposit queue over 134 indexed projects, generating ORCID, CRediT, and license scaffolds with 68 institutional drafts ready but 0 fully registrable deposits.
PATH: C:\Projects\AuthorshipLedger
```

</details>

### Original (frozen — do not edit)

```
Can public citation packets safely reach real DOI registration without resolving human metadata first? We reused bundled CitationWorkbench records and packet links for all 134 indexed projects. AuthorshipLedger v0.1 generated deposit drafts, ORCID intake templates, CRediT role templates, and SPDX-style license recommendations while separating institutional draft readiness from true registry readiness. High workflow readiness reached 64.2 percent (86 of 134 projects), and institutional draft readiness reached 50.7 percent (68 of 134), but fully registrable deposits remained 0.0 percent because no project yet preserved named human creators, ORCID identifiers, confirmed CRediT roles, or asserted final licenses. Journal targets were preserved for only 4.5 percent of records, making authorship and governance, not DataCite core fields, the true next bottleneck. This turns the next portfolio task into contributor and licensing resolution rather than further metadata generation. The ledger clarifies the queue, but it still relies on heuristic role templates, institutional fallback creators, and cannot authorize DOI registration by itself.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28341-28413 in rewrite-workbook.txt_

---

## Entry 377 ([491/921]) — CitationWorkbench

<details><summary>Metadata</summary>

```
TITLE: CitationWorkbench: Citation Packet Generation for the C Drive Portfolio
TYPE: methods  |  ESTIMAND: proportion of indexed projects reaching high citation readiness
DATA: Citation packet generator over 134 indexed projects, producing CFF, DataCite draft JSON, CiteProc JSON, and BibTeX with 86 high-readiness packets and 68 release-ready packets.
PATH: C:\Projects\CitationWorkbench
```

</details>

### Original (frozen — do not edit)

```
Can an internal research portfolio be converted into citation packets and DOI-facing metadata without hand-writing records one by one? We reused bundled PortfolioCatalog records, which exposed public landing pages for 134 indexed projects. CitationWorkbench v0.1 generated CFF, DataCite draft JSON, CiteProc JSON, and BibTeX for every project while scoring citation readiness from lifecycle, release, journal, and manuscript signals. High citation readiness reached 64.2 percent (86 of 134 projects), release-ready citation packets reached 50.7 percent (68 of 134), and DataCite core fields were derivable for all 134 records. Paper-backed coverage reached 68.7 percent, but only 4.5 percent preserved a target journal, making journal metadata the dominant citation gap rather than missing titles or URLs. This shifts the next portfolio task toward preserving venue targets, licensing, and authorship decisions instead of inventing more metadata shells. The packet factory improves citation hygiene, but it still produces draft metadata, does not register DOIs, and cannot prove authorship for collaborative work.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28414-28486 in rewrite-workbook.txt_

---

## Entry 378 ([492/921]) — DrivePulse

<details><summary>Metadata</summary>

```
TITLE: DrivePulse: Live Folder Telemetry for the C Drive Evidence Portfolio
TYPE: methods  |  ESTIMAND: proportion of specific indexed paths exposing git repositories
DATA: Live folder telemetry over 107 indexed paths, showing 105 specific paths present, 90 git-backed, 83 Pages-ready, and only two still too generic to scan precisely.
PATH: C:\Projects\DrivePulse
```

</details>

### Original (frozen — do not edit)

```
Can the portfolio atlas be linked back to live folder evidence rather than relying on index rows? We reused the bundled ResearchConstellation snapshot, deduplicated its 134 project records into 107 indexed paths, and refreshed those paths against the current C drive. DrivePulse v0.1 captured existence, recency, git state, README markers, test markers, paper artifacts, protocol artifacts, and Pages signals into a telemetry snapshot. All 105 specific filesystem paths were found live, and 85.7 percent (90 of 105) exposed git repositories while 79.0 percent (83 of 105) were already Pages-ready. Signal density peaked in tiers 4 and 7, whereas tier 12 collapsed to a generic root path and tier 8 remained operationally sparse. This shifts the next portfolio task from directory discovery toward index cleanup and evidence normalization, because the folders now exist but the metadata layer remains uneven. The scan improves operational visibility, but it is shallow, machine-specific, and cannot replace deeper repository or manuscript audits.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28487-28559 in rewrite-workbook.txt_

---

## Entry 379 ([379/921]) — EvidenceBridgeFHIR

<details><summary>Metadata</summary>

```
TITLE: EvidenceBridgeFHIR: Exporting the C Drive Evidence Portfolio into Citation and ArtifactAssessment Bundles
TYPE: methods  |  ESTIMAND: ArtifactAssessment coverage across exported projects
DATA: FHIR export layer with 134 Citation resources, 51 ArtifactAssessments, 185 total bundle entries, and 83 citation-only placeholders still waiting on upstream status normalization.
PATH: C:\Projects\EvidenceBridgeFHIR
```

</details>

### Original (frozen — do not edit)

```
Can a heterogeneous C-drive methods portfolio be exported into a standards-facing exchange format without losing its operational status signals? We reused the bundled ResearchConstellation snapshot containing 134 indexed projects across 12 tiers and mapped each project into a FHIR Citation record. EvidenceBridgeFHIR v0.1 then attached ArtifactAssessment resources only where the source snapshot already carried an explicit lifecycle label suitable for reuse. The resulting bundle contained 185 FHIR resources, combining 134 Citations with 51 ArtifactAssessments for 38.1 percent coverage (51 of 134), while 83 projects remained citation-only placeholders. Citation-only pressure clustered in tiers 10 and 12, which supplied 57 unresolved exports and dominated the interoperability backlog to date despite the portfolio's broader methodological depth. This shows the next barrier is not exchange syntax but portfolio curation, because standards layers cannot recover lifecycle judgments that were never frozen upstream. The bundle improves inspectability, but it does not validate against a live FHIR server or infer missing assessments automatically.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28560-28632 in rewrite-workbook.txt_

---

## Entry 380 ([380/921]) — EvidenceCrate

<details><summary>Metadata</summary>

```
TITLE: EvidenceCrate: Packaging the C Drive Research Portfolio as a Static Metadata Crate
TYPE: methods  |  ESTIMAND: explicit lifecycle coverage in packaged entities
DATA: RO-Crate style packaging layer over 134 indexed projects, generating a 156-node metadata graph with 83 status-incomplete entities still needing upstream normalization.
PATH: C:\Projects\EvidenceCrate
```

</details>

### Original (frozen — do not edit)

```
Can a portfolio atlas become a research package rather than a browser view of scattered projects? We reused the bundled ResearchConstellation snapshot containing 134 indexed projects across 12 tiers and preserved its status normalization outputs. EvidenceCrate v0.1 transforms that snapshot into dashboard data, a CodeMeta record, and an RO-Crate style metadata graph with tier and project entities. The generated crate contained 156 graph nodes and preserved explicit lifecycle coverage for 38.1 percent of projects (51 of 134), leaving 83 records as metadata-ready but status-incomplete entities. Tier collections exposed a sharp divide: tiers 2, 3, 4, and 7 exported cleanly, whereas tiers 6, 8, 10, and 12 remained dominated by unresolved rows. This shifts the next portfolio task from interface design toward packaging discipline, because metadata standards only help once project states are frozen upstream. The crate improves portability and reuse, but it does not validate RO-Crate profiles, inspect live folders, or repair ambiguous source labels automatically.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28633-28705 in rewrite-workbook.txt_

---

## Entry 381 ([381/921]) — FAIRPortfolio

<details><summary>Metadata</summary>

```
TITLE: FAIRPortfolio: Proxy Maturity Scoring for the C Drive Evidence Portfolio
TYPE: methods  |  ESTIMAND: proportion of projects scoring at least 70/100 on the FAIR-style proxy scale
DATA: FAIR-inspired proxy scoring across 134 portfolio projects, with mean total score 48.6, 19 projects at 70 or higher, and 47 projects still below 40.
PATH: C:\Projects\FAIRPortfolio
```

</details>

### Original (frozen — do not edit)

```
Can a C-drive portfolio be prioritised with FAIR-style signals even when the snapshot is too thin for FAIR assessment? We reused the bundled ResearchConstellation snapshot containing 134 indexed projects across 12 tiers and scored each record on findable, accessible, interoperable, and reusable proxy components. FAIRPortfolio v0.1 assigns a 100-point total by combining path specificity, delivery signals, automation cues, lifecycle normalization, and maturity evidence such as tests, versions, or manuscripts. Mean proxy maturity reached 48.6 points, and only 14.2 percent of projects (19 of 134) scored at least 70/100, while 35.1 percent (47 of 134) remained below 40. Stronger scores concentrated in tiers 2 and 1, whereas tier 12 had the lowest average score and tier 9 remained structurally weak. This suggests the next gain comes from metadata discipline and public delivery signals rather than inventing another analysis engine. The dashboard improves prioritisation, but it is only a FAIR-inspired proxy and cannot substitute for standards-grade compliance assessment.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28706-28778 in rewrite-workbook.txt_

---

## Entry 382 ([382/921]) — PortfolioCatalog

<details><summary>Metadata</summary>

```
TITLE: PortfolioCatalog: Public Discovery Layer for the C Drive Portfolio
TYPE: methods  |  ESTIMAND: proportion of indexed projects reaching high discoverability coverage
DATA: Public discovery catalog over 134 indexed projects, generating landing pages plus DCAT 3 and Schema.org exports with 76 high-discoverability records and 68 strong public records.
PATH: C:\Projects\PortfolioCatalog
```

</details>

### Original (frozen — do not edit)

```
Can a fragmented C-drive research portfolio be converted into a public discovery layer rather than remaining an internal index? We reused bundled snapshots from ResearchConstellation, DrivePulse, PortfolioOps, and FAIRPortfolio, covering 134 indexed projects. PortfolioCatalog v0.1 generated one static landing page per project plus DCAT 3, Schema.org, and sitemap exports for GitHub Pages delivery in this release. High discoverability coverage reached 56.7 percent (76 of 134 projects), while 50.7 percent (68 of 134) met the stricter strong-public-record criterion combining resolved status, public Pages signal, and discoverability score of at least 70/100. Resolved lifecycle coverage remained 61.9 percent, evidence-rich records reached 66.4 percent, and Tier 12 still collapsed to a mean discoverability score of 6.7. This shifts the next portfolio task toward metadata repair, public delivery, and lifecycle decisions instead of building yet another internal dashboard. The catalog improves external visibility, but it inherits heuristic weighting, snapshot lag, and does not prove that discoverable work is scientifically mature.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28779-28851 in rewrite-workbook.txt_

---

## Entry 383 ([383/921]) — PortfolioOps

<details><summary>Metadata</summary>

```
TITLE: PortfolioOps: Operational Fusion for the C Drive Evidence Portfolio
TYPE: methods  |  ESTIMAND: proportion of projects classified as operationally backed
DATA: Operational cockpit over 134 projects, merging portfolio, live-scan, triage, and FAIR snapshots into a readiness model with 31 operationally backed projects and 74 at readiness 70 or higher.
PATH: C:\Projects\PortfolioOps
```

</details>

### Original (frozen — do not edit)

```
Can portfolio layers be fused into one operational view rather than read one tool at a time? We reused bundled snapshots from ResearchConstellation, DrivePulse, TriageWorkbench, and FAIRPortfolio, covering 134 indexed projects. PortfolioOps v0.1 merged explicit status labels, medium-or-high confidence triage suggestions, live folder telemetry, publish signals, code signals, and FAIR-style maturity into one readiness model. Only 23.1 percent of projects (31 of 134) were currently operationally backed, while 55.2 percent (74 of 134) reached readiness scores of at least 70/100. Triage suggestions resolved 32 additional statuses, lifting total resolved rows to 83 of 134, but Tier 12 still collapsed under generic root indexing and the weakest mean readiness. This turns the next portfolio task into operational cleanup rather than another app, because the merged evidence now shows where status, packaging, and delivery still break together. The cockpit improves coordination, but it inherits snapshot lag and cannot guarantee that a high readiness score reflects real scientific quality.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28852-28924 in rewrite-workbook.txt_

---

## Entry 384 ([384/921]) — ProvenanceAtlas

<details><summary>Metadata</summary>

```
TITLE: ProvenanceAtlas: Static Lineage Graphing for the C Drive Evidence Portfolio
TYPE: methods  |  ESTIMAND: explicit lifecycle coverage in the provenance graph
DATA: PROV-style portfolio graph over 134 projects producing 157 nodes and 439 edges, with 83 unresolved lifecycle states still interrupting downstream lineage.
PATH: C:\Projects\ProvenanceAtlas
```

</details>

### Original (frozen — do not edit)

```
Can a portfolio inventory also show how its evidence was transformed, not just what projects it contains? We reused the bundled ResearchConstellation snapshot containing 134 indexed projects across 12 tiers and converted it into a PROV-style entity-activity-agent graph. ProvenanceAtlas v0.1 emits project entities, tier entities, summary outputs, and explicit build activities so lineage remains inspectable in a static repository for downstream review. The generated graph contained 157 nodes and 439 edges, while explicit lifecycle coverage remained 38.1 percent (51 of 134 projects), leaving 83 unresolved records inside the lineage. The strongest provenance pressure came from tiers 10 and 12, which alone contributed 57 unresolved projects and concentrated most broken downstream status chains. This reframes the portfolio gap as a provenance problem: without frozen lifecycle labels, later packaging, dashboards, and exchange layers inherit ambiguity by design. The atlas clarifies derivation paths, but it does not inspect live filesystem events, Git history, or authorship beyond the bundled snapshot.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28925-28997 in rewrite-workbook.txt_

---

## Entry 385 ([385/921]) — ResearchConstellation

<details><summary>Metadata</summary>

```
TITLE: Research Constellation: A Live Portfolio Status Atlas for the C Drive Evidence Stack
TYPE: methods  |  ESTIMAND: explicit status coverage
DATA: Snapshot-driven portfolio atlas covering 134 projects across 12 tiers, with 83 rows still needing explicit status labels.
PATH: C:\Projects\ResearchConstellation
```

</details>

### Original (frozen — do not edit)

```
Can a portfolio layer expose where an evidence-synthesis estate is organized well enough to operate, and where it still lacks status control? We parsed a bundled ProjectIndex snapshot, covering 134 projects across 12 tiers spanning flagship tools, HTML apps, HTA systems, datasets, courses, and exploratory research. Research Constellation v0.1 compiles that registry into cards, tier summaries, status filters, and a needs-triage queue without adding an analysis engine. Across the index, only 38.1 percent of projects (51 of 134) carried status labels, leaving 83 records unlabeled and Tier 10 alone contributing 32 triage rows. Submission-ready work concentrated in tiers 3, 4, 5, and 7, whereas infrastructure, educational, and backlog tiers showed zero explicit coverage. This makes the portfolio gap operational rather than methodological: status normalization now matters more than inventing another app family. The atlas improves visibility, but it depends on the snapshot remaining current, and it does not yet merge metadata, validation artifacts, or Git state.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 28998-29070 in rewrite-workbook.txt_

---

## Entry 386 ([386/921]) — SubmissionCockpit

<details><summary>Metadata</summary>

```
TITLE: SubmissionCockpit: Editorial Release Control for the C Drive Research Portfolio
TYPE: methods  |  ESTIMAND: proportion of indexed projects currently carrying resolved submission-ready status
DATA: See paper.json summary
PATH: C:\Projects\SubmissionCockpit
```

</details>

### Original (frozen — do not edit)

```
Can one tracker govern rewriting and publication of a multi-project E156 portfolio across GitHub and Pages? We fused current outputs from ResearchConstellation, PortfolioOps, CitationWorkbench, and AuthorshipLedger across 134 indexed projects and generated a canonical rewrite workbook for editorial tracking. SubmissionCockpit syncs portfolio metadata, manual rewrite states, MIT-license intent, GitHub and Pages delivery flags, and future Synthesis Journal upload placeholders into one publication ledger. Across 134 indexed projects, 26 carried resolved submission-ready status, a portfolio submission proportion of 19.4 percent (95% CI 12.7-26.1). Another 68 projects already had citation-readiness scores of at least 90, and 134 had draft deposit manifests available for reuse, plus public packet links, queue pages, and license recommendations. This turns the publication problem into queue management, because the remaining gaps now become explicit blockers for rewrite, packaging, release, and upload. The limitation is that cockpit review remains manual, and PDF galley upload will stay pending until journal credentials and article files are available.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29071-29143 in rewrite-workbook.txt_

---

## Entry 387 ([387/921]) — TriageWorkbench

<details><summary>Metadata</summary>

```
TITLE: TriageWorkbench: Rule-Based Lifecycle Freezing for the Unresolved Portfolio Queue
TYPE: methods  |  ESTIMAND: non-triage recommendation coverage across unresolved rows
DATA: Rule-based triage layer over 83 unresolved rows, producing 54 non-triage recommendations and 35 medium-or-high-confidence suggestions from the bundled portfolio snapshot.
PATH: C:\Projects\TriageWorkbench
```

</details>

### Original (frozen — do not edit)

```
Can the portfolio's unresolved queue be reduced before more dashboards inherit the same ambiguity today? We reused the bundled ResearchConstellation snapshot and isolated 83 projects currently lacking explicit status labels across the 134-project portfolio. TriageWorkbench v0.1 applied deterministic rules to each unresolved row, weighting tests, manuscript, dashboard, review clean, and generic root paths to suggest a lifecycle label and confidence tier. The workbench produced non-triage recommendations for 65.1 percent of unresolved rows (54 of 83), leaving 29 unreduced and only 42.2 percent (35 of 83) reaching medium-or-high confidence. Recommendation pressure centered in tiers 10 and 12, which supplied 57 of 83 unresolved inputs, while active-like suggestions still dominated the generated label mix. This makes the next portfolio step a curation workflow problem, because deterministic triage can substantially shrink the queue before manual review begins. The workbench improves prioritization, but it does not inspect folders, confirm git state, or guarantee that its rule-based labels are consistently correct.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29144-29217 in rewrite-workbook.txt_

---

## Entry 388 ([388/921]) — GlobalTransportabilityAtlas

<details><summary>Metadata</summary>

```
TITLE: Global Transportability Atlas: Assessing Cardiovascular/Diabetes Prognostic Models using GBD 2023 Covariates
TYPE: clinical/methods  |  ESTIMAND: O:E Ratio and Recalibrated HR
DATA: GBD 2023 Covariates (1980-2023), Framingham/SCORE2 model parameters
PATH: C:\Users\user\global-transportability-atlas
```

</details>

### Original (frozen — do not edit)

```
Can cardiovascular and diabetes prognostic models maintain predictive accuracy when transported from high-income countries to the Global South using contemporary GBD 2023 covariates? We extracted 1980-2023 covariates from the Global Burden of Disease study, including socioeconomic, health system access, and demographic variables for 204 countries. Our framework applies a "TruthCert" pipeline to quantify transportability using country-level Standardized Mean Differences (SMDs) and recalibrated Hazard Ratios (HRs). Preliminary mapping in four key regions (IND, NGA, KEN, BRA) shows that Western-centric models exhibit significant calibration drift, with O:E ratios ranging from 0.82 to 1.54 compared to original validation cohorts. Robustness checks using Monte Carlo simulations confirmed that health system readiness scores are the strongest predictors of model performance degradation. These results provide a "Global Transportability Atlas" for clinicians, highlighting where existing risk scores require local recalibration before deployment. The study is limited by the availability of subnational covariate data in rural regions and assumes stable baseline risk distributions within countries.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29218-29291 in rewrite-workbook.txt_

---

## Entry 389 ([389/921]) — ProportionMA

<details><summary>Metadata</summary>

```
TITLE: ProportionMA: Browser-Based Proportion and Prevalence Meta-Analysis
TYPE: methods  |  ESTIMAND: Pooled Proportion
DATA: User-supplied study-level event counts and sample sizes
PATH: C:\Models\ProportionMA
```

</details>

### Original (frozen — do not edit)

```
Can a single browser tool pool disease prevalence or event proportions from heterogeneous studies using all standard transformations and modern variance adjustments? We accept study-level event counts and denominators via CSV paste or manual entry, supporting any clinical domain requiring proportion synthesis. The engine implements Freeman-Tukey double arcsine, logit, and raw proportion transformations with DerSimonian-Laird and REML pooling, applying Hartung-Knapp-Sidik-Jonkman adjustment with a variance floor of max(1, Q/(k-1)) and prediction intervals on t_{k-2} degrees of freedom. Validation against R metaprop on an 8-study prevalence dataset showed pooled estimates within 0.02 absolute tolerance for both FT and logit transforms, with correct I-squared and tau-squared. Back-transformation uses the harmonic mean denominator with Miller 1978 correction, and per-study Clopper-Pearson exact intervals use the alpha/2 beta quantile. The tool generates interactive forest and funnel plot SVGs with subgroup stratification. Results depend on the chosen transformation, which should be pre-specified in the protocol.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29292-29365 in rewrite-workbook.txt_

---

## Entry 390 ([390/921]) — EvidenceMapPro

<details><summary>Metadata</summary>

```
TITLE: EvidenceMapPro: Interactive Evidence Gap Matrix and Bubble Chart Generator
TYPE: methods  |  ESTIMAND: Evidence Coverage Percentage
DATA: User-supplied study characteristics with GRADE certainty ratings
PATH: C:\Models\EvidenceMapPro
```

</details>

### Original (frozen — do not edit)

```
Can a browser application transform study-level characteristics into an interactive evidence gap matrix that reveals research priorities at a glance? We accept CSV-formatted study data including intervention, outcome, study design, GRADE certainty, year, and population, requiring no server-side processing. The engine constructs an intervention-by-outcome gap matrix with cells colored by highest GRADE certainty (green for high through red for very low, gray for empty), a proportionally sized bubble chart, and real-time filtering by study design checkboxes, year range, and population text search. Applied to a 15-study demonstration dataset spanning four interventions and five outcomes, the tool correctly computed 60 percent evidence coverage with design-stratified filtering reducing visible studies to user-specified subsets. All filters propagate simultaneously to the gap matrix, bubble chart, and study table, maintaining visual consistency. Exports include publication-ready SVG matrices and filtered CSV data. The tool cannot assess within-cell heterogeneity or risk of bias beyond the user-supplied GRADE rating.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29366-29439 in rewrite-workbook.txt_

---

## Entry 391 ([391/921]) — MultivarMA

<details><summary>Metadata</summary>

```
TITLE: MultivarMA: Browser Multivariate Meta-Analysis for Correlated Outcomes
TYPE: methods  |  ESTIMAND: Pooled Effect Vector (2-3 outcomes)
DATA: Study-level correlated outcome estimates with within-study correlations
PATH: C:\Models\MultivarMA
```

</details>

### Original (frozen — do not edit)

```
Can a browser tool jointly synthesize two or three correlated outcomes to borrow strength across endpoints without requiring specialized statistical software? We accept paired effect estimates and standard errors per study with user-specified or default within-study correlations, supporting any pair of continuous outcomes. The engine implements the Riley multivariate random-effects model via iterative generalized least squares with method-of-moments between-study variance estimation, enforcing positive semi-definiteness via eigenvalue clamping. Validation against R mvmeta on the Berkey 1998 periodontal dataset (5 studies, probing depth and attachment level) showed pooled estimates within 0.02 of reference values. The borrowing-of-strength metric quantified precision gains of 5-15 percent from joint versus univariate modeling when outcome correlation exceeded 0.4. Studies with missing outcomes contribute through large-variance imputation, enabling partial data inclusion. Joint forest plots display multivariate and univariate summary diamonds side by side with a between-study correlation heatmap. Results assume multivariate normality and may be sensitive to misspecified within-study correlations.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29440-29513 in rewrite-workbook.txt_

---

## Entry 392 ([392/921]) — CostEffMA

<details><summary>Metadata</summary>

```
TITLE: CostEffMA: Browser Cost-Effectiveness Meta-Analysis with CEAC and NMB Pooling
TYPE: methods  |  ESTIMAND: Pooled Net Monetary Benefit and ICER
DATA: Study-level incremental costs and effects from economic evaluations
PATH: C:\Models\CostEffMA
```

</details>

### Original (frozen — do not edit)

```
Can a browser application pool cost-effectiveness data across economic evaluations and generate acceptability curves without requiring dedicated health economic software? We accept incremental costs, effects, and standard errors from multiple studies with optional cost-effect correlation, computing net monetary benefit at user-specified willingness-to-pay thresholds. The engine pools NMB via DerSimonian-Laird random effects with HKSJ adjustment and simultaneously estimates pooled ICERs on the log scale with delta-method standard errors. At a WTP of 25,000 pounds the demonstration dataset of six evaluations yielded a pooled NMB indicating cost-effectiveness with a probability of 72 percent on the cost-effectiveness acceptability curve. The CEAC sweeps WTP from zero to 200,000, correctly converging to probability one for dominant treatments and zero when WTP cannot offset costs. An interactive cost-effectiveness plane displays study-level scatter with quadrant classification and a 95 percent confidence ellipse. Conclusions are sensitive to the assumed WTP threshold and correlation between costs and effects.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29514-29587 in rewrite-workbook.txt_

---

## Entry 393 ([393/921]) — EcoBiasMA

<details><summary>Metadata</summary>

```
TITLE: EcoBiasMA: Browser Ecological Bias Detection and Correction in Meta-Analysis
TYPE: methods  |  ESTIMAND: Ecological Bias (beta_B - beta_W)
DATA: Study-level effects with aggregate covariates and optional within-study estimates
PATH: C:\Models\EcoBiasMA
```

</details>

### Original (frozen — do not edit)

```
Can ecological confounding in meta-analysis be detected and corrected using a browser tool when individual patient data are only partially available? We accept study-level treatment effects with aggregate covariate means and optional within-study effect estimates for a subset of studies. The engine implements the Jackson 2006 decomposition, estimating between-study and within-study regression slopes via weighted least squares with DerSimonian-Laird heterogeneity and Knapp-Hartung confidence intervals on t_{k-2} degrees of freedom. Applied to an 8-study cardiovascular demonstration dataset with age as ecological confounder, the tool detected a between-study slope diverging from the within-study slope estimated from three studies providing subgroup data. A sensitivity tornado sweeps plausible bias correction factors, identifying the threshold at which the pooled conclusion reverses, and dual forest plots display corrected versus uncorrected estimates. The decomposition is only valid when between-study variation in the covariate is sufficient, and requires at least three studies for meta-regression.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29588-29661 in rewrite-workbook.txt_

---

## Entry 394 ([394/921]) — TargetTrialMA

<details><summary>Metadata</summary>

```
TITLE: TargetTrialMA: Browser Meta-Analysis of RCTs and Target Trial Emulations
TYPE: methods  |  ESTIMAND: Stratified Pooled HR (RCT vs TTE)
DATA: Study-level effects from RCTs and target trial emulations with ROBINS-I judgments
PATH: C:\Models\TargetTrialMA
```

</details>

### Original (frozen — do not edit)

```
Can randomized trials and target trial emulations be jointly meta-analyzed while preserving design-specific validity and quantifying the emulation-RCT gap? We accept study-level log hazard ratios from both RCTs and target trial emulations alongside ROBINS-I quality judgments and an 8-item Hernan-Robins target trial checklist. The engine performs stratified DerSimonian-Laird pooling with HKSJ adjustment, computing RCT-only, TTE-only, and combined estimates with a between-group interaction test using the Q-between chi-squared statistic. Applied to 10 SGLT2 inhibitor studies (4 RCTs, 6 TTEs), the interaction test yielded p=0.62, suggesting concordant effect estimates. ROBINS-I sensitivity weighting downweighted serious-risk studies by 50 percent and excluded critical-risk studies, shifting the adjusted pooled HR by 4 percent. A quality heatmap visualizes checklist adherence across TTE studies. The tool cannot assess unmeasured confounding within emulations and assumes that ROBINS-I judgments are correctly assigned by the user.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29662-29735 in rewrite-workbook.txt_

---

## Entry 395 ([395/921]) — PlatformTrialMA

<details><summary>Metadata</summary>

```
TITLE: PlatformTrialMA: Browser Meta-Analysis for Adaptive Platform Trials with Shared Controls
TYPE: methods  |  ESTIMAND: Pooled HR with Shared-Control Covariance
DATA: Platform trial arm-level data with enrollment timelines
PATH: C:\Models\PlatformTrialMA
```

</details>

### Original (frozen — do not edit)

```
Can treatment effects from adaptive platform trials be correctly meta-analyzed when multiple experimental arms share a single control group? We accept arm-level data from platform trials including effect estimates, standard errors, and enrollment time periods, with the engine automatically detecting shared control arm structures. The variance-covariance matrix incorporates off-diagonal elements of tau-squared divided by two for all within-platform comparisons sharing a control arm, and GLS pooling uses block-diagonal matrices with closed-form inversion for blocks up to three-by-three and Gauss-Jordan elimination for larger blocks. Applied to RECOVERY (3 arms), REMAP-CAP (2 arms), and two independent trials, the GLS-corrected pooled estimate differed from naive inverse-variance by 8 percent, confirming the importance of covariance adjustment. Non-concurrent control adjustment corrects for temporal drift when treatment arms enter at different calendar times. A Gantt-style timeline SVG visualizes arm enrollment windows across platforms. The method assumes constant heterogeneity and cannot handle time-varying treatment effects.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29736-29809 in rewrite-workbook.txt_

---

## Entry 396 ([396/921]) — SeqNMA

<details><summary>Metadata</summary>

```
TITLE: SeqNMA: Browser Sequential Network Meta-Analysis with Monitoring Boundaries
TYPE: methods  |  ESTIMAND: Cumulative NMA z-score vs OBrien-Fleming boundary
DATA: Chronologically ordered network studies with treatment comparisons
PATH: C:\Models\SeqNMA
```

</details>

### Original (frozen — do not edit)

```
Can trial sequential analysis be extended to network meta-analysis, providing formal stopping rules as evidence accumulates across a treatment network? We accept chronologically ordered studies reporting pairwise treatment comparisons, building a cumulative contrast-based NMA at each study addition. The engine computes required information size per comparison using the heterogeneity-adjusted design effect D-squared (not the cluster design effect), OBrien-Fleming alpha-spending boundaries where z_k equals z-alpha divided by the square root of the information fraction, and Bonferroni correction across all T(T-1)/2 comparisons. Applied to a 12-study network of 4 treatments, the A-versus-C comparison crossed the monitoring boundary after study 10 while A-versus-D remained inconclusive at 65 percent of required information. Futility boundaries are explicitly labeled non-binding per sequential analysis conventions. An interactive network evolution slider shows the growing evidence network over time with a league table of current estimates. The method assumes consistency and may be conservative under substantial Bonferroni correction with many treatments.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29810-29883 in rewrite-workbook.txt_

---

## Entry 397 ([397/921]) — IPDNMA

<details><summary>Metadata</summary>

```
TITLE: IPDNMA: Browser Individual Patient Data Network Meta-Analysis
TYPE: methods  |  ESTIMAND: NMA Pooled Effect with Treatment-Covariate Interaction
DATA: Patient-level and aggregate study data across a treatment network
PATH: C:\Models\IPDNMA
```

</details>

### Original (frozen — do not edit)

```
Can individual patient data and aggregate data be jointly synthesized in a browser-based network meta-analysis with treatment effect modification detection? We accept patient-level data with outcomes, treatments, and covariates alongside aggregate-data studies reporting pairwise effects. The two-stage engine fits within-study OLS regressions on IPD studies (extracting treatment effects, interaction terms, and standard errors), then pools all estimates into a contrast-based NMA via weighted least squares with DerSimonian-Laird heterogeneity. Node-splitting consistency checks compare direct and indirect evidence for each comparison. Applied to a mixed dataset of 3 IPD studies (120 patients, 3 treatments) and 2 aggregate studies, the pooled NMA estimates were consistent across all comparisons (node-split p-values above 0.10) and age-treatment interaction analysis detected effect modification with a pooled delta of 0.03 per year. P-score rankings and a league table summarize all pairwise comparisons. The tool uses OLS not mixed-effects regression and cannot handle binary outcomes or time-to-event data natively.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29884-29957 in rewrite-workbook.txt_

---

## Entry 398 ([398/921]) — FederatedMA

<details><summary>Metadata</summary>

```
TITLE: FederatedMA: Browser Privacy-Preserving Federated Meta-Analysis
TYPE: methods  |  ESTIMAND: Differentially Private Pooled Effect
DATA: Multi-site summary statistics with privacy budget constraints
PATH: C:\Models\FederatedMA
```

</details>

### Original (frozen — do not edit)

```
Can meta-analysis be conducted across clinical sites without sharing patient-level data while quantifying the precision cost of privacy protection? We simulate federated meta-analysis where each site contributes only summary statistics, with optional differential privacy noise calibrated to the Laplace mechanism at user-specified epsilon. The engine computes three analyses in parallel: standard random-effects meta-analysis (gold standard), secure aggregation via additive secret sharing (no precision loss), and differentially private pooling (precision traded for privacy). Applied to 8 simulated clinical sites, secure aggregation exactly reproduced standard MA results while differential privacy at epsilon=1.0 widened confidence intervals by 35 percent and at epsilon=0.1 by over 200 percent. A precision-privacy tradeoff curve sweeps epsilon from 0.1 to 10, showing asymptotic convergence to standard precision. A privacy budget gauge tracks cumulative epsilon across analyses using sequential composition. The simulation assumes honest-but-curious sites and does not address Byzantine adversaries or collusion beyond the threshold model.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 29958-30031 in rewrite-workbook.txt_

---

## Entry 399 ([399/921]) — FigureEngine

<details><summary>Metadata</summary>

```
TITLE: FigureEngine: Publication-Quality Meta-Analysis Figure Generator
TYPE: tool  |  ESTIMAND: N/A (visualization tool)
DATA: JSON-formatted meta-analysis results
PATH: C:\Models\FigureEngine
```

</details>

### Original (frozen — do not edit)

```
Can a single command-line tool generate all standard meta-analysis figures in journal-specific styles from structured JSON input? We built a Python CLI accepting six figure types: forest plot, funnel plot, SROC curve, network graph, PRISMA 2020 flow diagram, and cumulative meta-analysis forest. The engine uses matplotlib with non-interactive Agg backend, rendering to SVG (editable text), TIFF (300 DPI for submission), PNG, and PDF formats. Five journal style templates (BMJ at 174mm, Lancet at 180mm, JAMA at 178mm, NEJM at 178mm, and a general default) control width, fonts, color palettes, and line weights. Forest plots render weight-proportional squares with summary diamonds and prediction interval lines; funnel plots support contour-enhanced and trim-and-fill overlays; network graphs use spring-electric force-directed layout. All 20 validation tests confirm correct SVG structure, output format integrity, and style-specific dimensions. The tool cannot generate interactive figures and style templates may need adjustment for specific journal submission guidelines.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30032-30105 in rewrite-workbook.txt_

---

## Entry 400 ([400/921]) — ZenodoPipeline

<details><summary>Metadata</summary>

```
TITLE: ZenodoPipeline: Automated Zenodo DOI Publishing for Research Repositories
TYPE: tool  |  ESTIMAND: N/A (infrastructure tool)
DATA: Project repositories with README and LICENSE metadata
PATH: C:\Models\ZenodoPipeline
```

</details>

### Original (frozen — do not edit)

```
Can the Zenodo DOI minting bottleneck blocking 15 manuscript submissions be eliminated through automated metadata extraction and batch publishing? We built a Python CLI that scans project directories for README, LICENSE, E156-PROTOCOL, and git history to auto-generate .zenodo.json metadata files conforming to the Zenodo deposition schema. The pipeline creates zip archives excluding .git, __pycache__, configuration directories, and files exceeding 50MB, then interfaces with the Zenodo REST API to create depositions, upload archives, and publish for DOI assignment. Batch mode parses INDEX.md to discover all SUBMISSION-READY projects, processing them sequentially with progress reporting. A dry-run mode shows the complete upload plan including file counts and sizes without requiring an API token. Sandbox mode (sandbox.zenodo.org) is the default, with production publishing requiring an explicit flag. All 36 tests pass using mocked API calls with verified token safety (no hardcoded credentials in source). The tool depends on Zenodo API availability and cannot handle embargoed or restricted-access depositions.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30106-30179 in rewrite-workbook.txt_

---

