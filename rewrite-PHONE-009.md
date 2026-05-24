# Rewrite chunk 009 — entries 401-450

_Previous: rewrite-PHONE-008.md | Next: rewrite-PHONE-010.md | Index: rewrite-PHONE-INDEX.md_

Edit ONLY the `YOUR REWRITE` section under each entry. The `Original`
block is frozen — do not edit it. Save the file when done. On your
laptop run `python C:\E156\merge-rewrite.py` to assemble a new
workbook (`rewrite-workbook.NEW.txt`) with your edits applied.

---

## Entry 401 ([401/921]) — WHODataLakehouse

<details><summary>Metadata</summary>

```
TITLE: WHO Data Lakehouse: Global Health Observatory and Expenditure Data Pipeline
TYPE: tool  |  ESTIMAND: N/A (data pipeline)
DATA: WHO GHO API (2000+ indicators) and GHED health expenditure data
PATH: D:\Projects\who-data-lakehouse
```

</details>

### Original (frozen — do not edit)

```
Can WHO Global Health Observatory data be systematically extracted, standardized, and cross-walked to IHME and World Bank datasets for integrated global health analysis? We built a Python pipeline with six domain-specific extractors covering mortality, morbidity, risk factors, health systems, expenditure, and immunization, pulling from the WHO GHO OData API with automatic pagination and 0.5-second rate limiting. A 66-country cross-walk maps WHO ISO3 codes to IHME location identifiers and World Bank country codes, enabling seamless joins across the three major global health data ecosystems. Quality checks compute completeness percentages, temporal coverage ranges, and flag outliers exceeding three standard deviations from country-specific trends. Applied to life expectancy and UHC service coverage indicators, the pipeline correctly extracted data for 194 WHO member states with completeness above 85 percent for post-2000 data. Parquet storage with incremental refresh minimizes redundant API calls across sessions. The pipeline is limited by WHO API rate limits and cannot access subnational or facility-level data not exposed through the GHO.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
Can WHO Global Health Observatory data be systematically extracted, standardized, and cross-walked for integrated global health analysis? We built a Python pipeline with six domain-specific extractors covering mortality, morbidity, risk factors, health systems, expenditure, and immunization across WHO public interfaces. A 66-country cross-walk links WHO ISO3 codes to IHME and World Bank identifiers for merged analyses. Applied to life expectancy and UHC service coverage, the pipeline extracted data for 194 WHO member states with completeness above 85 percent for post-2000 records. Parquet outputs and incremental refresh reduce redundant API calls, while quality checks flag outliers above three standard deviations from country-specific trends. This creates a reusable lakehouse for cross-system health analyses using WHO-first data. The pipeline remains constrained by WHO rate limits and lacks subnational or facility-level feeds absent from public APIs.
<!-- END-REWRITE -->

_Line range 30180-30253 in rewrite-workbook.txt_

---

## Entry 402 ([402/921]) — OmecamtivLivingMA

<details><summary>Metadata</summary>

```
TITLE: Omecamtiv Mecarbil in Heart Failure: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 1 RCT (GALACTIC-HF), 8,232 patients; single-trial state (COSMIC-HF and ATOMIC-AHF pending extraction)
PATH: C:\Projects\Omecamtiv_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does omecamtiv mecarbil, a selective cardiac myosin activator, reduce cardiovascular death or heart failure hospitalisation in patients with heart failure and reduced ejection fraction? One randomized placebo-controlled trial is currently deployed in this living meta-analysis: GALACTIC-HF enrolled 8,232 patients with chronic HFrEF and elevated NT-proBNP over a median follow-up of 21 months. Single-trial inverse-variance estimate used the original publication's Cox model hazard ratio and confidence interval. GALACTIC-HF reported a hazard ratio of 0.92 (95% CI 0.86 to 0.99) for the primary composite of cardiovascular death or heart failure hospitalisation, just crossing statistical significance. Subgroup and sensitivity analyses within the trial preserved the direction but the effect on all-cause mortality alone was not significant. Omecamtiv mecarbil provides a statistically modest reduction in the composite endpoint in HFrEF. Regulatory approval was not granted, and earlier phase trials such as COSMIC-HF and ATOMIC-AHF await data extraction into the living pool.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30254-30327 in rewrite-workbook.txt_

---

## Entry 403 ([403/921]) — SotagliflozinLivingMA

<details><summary>Metadata</summary>

```
TITLE: Sotagliflozin in Heart Failure and Diabetes: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 2 RCTs (SOLOIST-WHF, SCORED), 11,806 patients, CT.gov sourced
PATH: C:\Projects\Sotagliflozin_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does sotagliflozin, a dual SGLT1 and SGLT2 inhibitor, reduce cardiovascular events in patients with heart failure or type 2 diabetes and chronic kidney disease? Two randomized placebo-controlled trials deployed in this living meta-analysis (SOLOIST-WHF, SCORED) enrolled 11,806 patients and evaluated sotagliflozin 200 to 400 mg daily with median follow-up of nine to sixteen months. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the two deployed trials. The pooled hazard ratio for cardiovascular death or heart failure hospitalisation was 0.72 (95% CI 0.63 to 0.82), with no detectable heterogeneity (I-squared 0 percent). SCORED (HR 0.74) and SOLOIST-WHF (HR 0.67) both favoured sotagliflozin, confirming robustness across worsening heart failure and stable diabetic chronic kidney disease populations. Sotagliflozin demonstrates a clinically meaningful twenty-eight percent reduction in the composite cardiovascular endpoint. Both trials were terminated early due to funding loss, raising uncertainty about long-term efficacy and safety beyond sixteen months.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30328-30401 in rewrite-workbook.txt_

---

## Entry 404 ([404/921]) — TezepelumabLivingMA

<details><summary>Metadata</summary>

```
TITLE: Tezepelumab in Severe Asthma: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: RR for annualized asthma exacerbation rate
DATA: 3 RCTs (NAVIGATOR, PATHWAY, SOURCE), 1,395 patients, CT.gov sourced
PATH: C:\Projects\Tezepelumab_Asthma_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does tezepelumab, an anti-thymic stromal lymphopoietin monoclonal antibody, reduce exacerbation rates in adults with severe uncontrolled asthma irrespective of baseline eosinophil count? Three randomized placebo-controlled trials enrolling 1,395 patients with severe asthma evaluated subcutaneous tezepelumab 210 mg every four weeks over 28 to 52 weeks. DerSimonian-Laird random-effects meta-analysis pooled risk ratios on the log scale with HKSJ adjustment. The pooled risk ratio for annualized asthma exacerbations was 0.44 (95% CI 0.35-0.54), with negligible heterogeneity (I-squared 0%). Subgroup analyses by baseline blood eosinophil count showed consistent benefit across low, medium, and high eosinophil strata, distinguishing tezepelumab from eosinophil-selective biologics. Tezepelumab reduces severe asthma exacerbations by 56 percent regardless of inflammatory phenotype, supporting its role as a broad-acting upstream biologic. Follow-up is limited to one year, no head-to-head trials against existing biologics exist, and cost-effectiveness data outside the United States remain sparse.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30402-30475 in rewrite-workbook.txt_

---

## Entry 405 ([405/921]) — OsimertinibLivingMA

<details><summary>Metadata</summary>

```
TITLE: Osimertinib in EGFR-Mutant NSCLC: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for progression-free survival
DATA: 4 RCTs (FLAURA, FLAURA2, ADAURA, AURA3), 2,244 patients, CT.gov sourced
PATH: C:\Projects\Osimertinib_NSCLC_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does osimertinib, a third-generation EGFR tyrosine kinase inhibitor, improve progression-free survival across treatment settings in patients with EGFR-mutant non-small cell lung cancer? Four randomized controlled trials deployed in this living meta-analysis (FLAURA, FLAURA2, ADAURA, AURA3) enrolled 2,244 patients across first-line, combination, adjuvant, and second-line T790M-positive settings. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the four deployed trials. The pooled hazard ratio for progression-free survival was 0.40 (95% CI 0.35 to 0.45), with substantial heterogeneity (I-squared 92 percent) driven by differences in comparator arms and disease stage. The adjuvant ADAURA trial contributes the most extreme effect size (HR 0.20), while first-line FLAURA (HR 0.46) and combination FLAURA2 (HR 0.62) show attenuated but consistent benefit. Osimertinib demonstrates a consistent and large reduction in disease progression across EGFR-mutant NSCLC settings. High heterogeneity reflects genuine between-setting variation rather than inconsistency, and overall survival data remain immature for the newer trials.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30476-30549 in rewrite-workbook.txt_

---

## Entry 406 ([406/921]) — EnfortumabUCLivingMA

<details><summary>Metadata</summary>

```
TITLE: Enfortumab Vedotin in Urothelial Carcinoma: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for overall survival
DATA: 2 RCTs (EV-301, EV-302 KEYNOTE-A39), 1,494 patients, CT.gov sourced
PATH: C:\Projects\Enfortumab_UC_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does enfortumab vedotin, a Nectin-4-directed antibody-drug conjugate, improve overall survival in patients with locally advanced or metastatic urothelial carcinoma? Two randomized phase 3 trials deployed in this living meta-analysis (EV-301, EV-302 KEYNOTE-A39) enrolled 1,494 patients across platinum-pretreated and treatment-naive settings and compared enfortumab vedotin with or without pembrolizumab against standard chemotherapy. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the two deployed trials. The pooled hazard ratio for overall survival was 0.56 (95% CI 0.48 to 0.66), with substantial heterogeneity (Q 6.2 on one degree of freedom, I-squared 84 percent). EV-301 (HR 0.70) showed benefit against chemotherapy in platinum-pretreated disease, while EV-302 (HR 0.47) showed larger benefit in first-line disease with pembrolizumab combination. Enfortumab vedotin-based therapy reduces mortality in advanced urothelial carcinoma across both pretreated and first-line settings. Between-setting heterogeneity reflects the additive effect of pembrolizumab in first-line use rather than inconsistency in the single-agent effect.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30550-30623 in rewrite-workbook.txt_

---

## Entry 407 ([407/921]) — KRASG12CLivingMA

<details><summary>Metadata</summary>

```
TITLE: KRAS G12C Inhibitors in NSCLC: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for progression-free survival
DATA: 2 RCTs (CodeBreaK 200, KRYSTAL-12), 798 patients, CT.gov sourced
PATH: C:\Projects\KRAS_G12C_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Do KRAS G12C inhibitors, sotorasib and adagrasib, improve progression-free survival compared with docetaxel in pretreated patients with KRAS G12C-mutant non-small cell lung cancer? Two randomized phase 3 trials enrolling 798 patients with KRAS G12C-positive advanced NSCLC compared targeted KRAS G12C inhibition against intravenous docetaxel after platinum chemotherapy failure. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for progression-free survival was 0.62 (95% CI 0.51-0.74), with no detectable heterogeneity (I-squared 0%). Both trials independently demonstrated objective response rates exceeding 30 percent compared with under 15 percent for docetaxel, validating the targeted approach. KRAS G12C inhibitors reduce disease progression by 38 percent and offer a substantially less toxic alternative to taxane chemotherapy. Overall survival benefit is modest, central nervous system activity is limited, and resistance mechanisms remain incompletely characterized.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30624-30697 in rewrite-workbook.txt_

---

## Entry 408 ([408/921]) — PembrolizumabAdjuvantMelanomaLivingMA

<details><summary>Metadata</summary>

```
TITLE: Adjuvant Pembrolizumab in Resected Melanoma: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for recurrence-free survival
DATA: 2 RCTs (KEYNOTE-716, KEYNOTE-942 INTerCEPT), 1,240 patients, CT.gov sourced
PATH: C:\Projects\Pembro_Adj_Mel_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does adjuvant pembrolizumab improve recurrence-free survival in patients with resected high-risk stage II or III melanoma? Two randomized phase 3 trials deployed in this living meta-analysis (KEYNOTE-716, KEYNOTE-942 INTerCEPT) enrolled 1,240 patients with completely resected high-risk cutaneous melanoma and compared pembrolizumab-based therapy against placebo or observation. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the two deployed trials. The pooled hazard ratio for recurrence-free survival was 0.63 (95% CI 0.46 to 0.85), with no detectable heterogeneity (I-squared 0 percent). KEYNOTE-716 evaluated standard adjuvant pembrolizumab in stage IIB-IIC disease (HR 0.65), while KEYNOTE-942 INTerCEPT tested individualised neoantigen mRNA-1345 combined with pembrolizumab (HR 0.56). Adjuvant pembrolizumab-based therapy reduces recurrence risk by approximately 37 percent in resected high-risk melanoma. Overall survival data remain immature, immune-related adverse events affect roughly 20 percent of patients, and the neoantigen-combination strategy awaits phase 3 confirmation.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30698-30771 in rewrite-workbook.txt_

---

## Entry 409 ([409/921]) — InclisiranLivingMA

<details><summary>Metadata</summary>

```
TITLE: Inclisiran for LDL Cholesterol Lowering: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for major adverse cardiovascular events
DATA: 3 RCTs (ORION-9, ORION-10, ORION-11), 3,660 patients, CT.gov sourced
PATH: C:\Projects\Inclisiran_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does inclisiran, a small interfering RNA targeting hepatic PCSK9 messenger RNA, reduce major adverse cardiovascular events in patients with established atherosclerotic disease or familial hypercholesterolemia? Three randomized phase 3 trials enrolling 3,660 patients with elevated LDL cholesterol despite maximum tolerated statin therapy compared subcutaneous inclisiran twice yearly against placebo. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for cardiovascular events was 0.77 (95% CI 0.56-1.07), with no detectable heterogeneity (I-squared 0%) across heterozygous familial hypercholesterolemia and ASCVD populations. Pooled LDL cholesterol reduction was approximately 50 percent versus placebo, consistent across all three trials. Inclisiran reliably lowers LDL cholesterol with semi-annual dosing, but the cardiovascular outcome estimate remains imprecise pending the larger ORION-4 trial. Long-term cardiovascular benefit is unproven, cost-effectiveness is contested, and twice-yearly injection logistics may not suit all health systems.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30772-30845 in rewrite-workbook.txt_

---

## Entry 410 ([410/921]) — AntiplatelietNMALivingMA

<details><summary>Metadata</summary>

```
TITLE: P2Y12 Monotherapy after PCI: Living Network Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for net clinical benefit composite
DATA: 4 RCTs (TWILIGHT, TICO, HOST-EXAM, GLOBAL LEADERS), 31,604 patients, CT.gov sourced
PATH: C:\Projects\Antiplatelet_NMA_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does P2Y12 inhibitor monotherapy after short dual antiplatelet therapy reduce net adverse clinical events compared with prolonged DAPT after percutaneous coronary intervention? Four randomized trials deployed in this living meta-analysis (TWILIGHT, TICO, HOST-EXAM, GLOBAL LEADERS) enrolled 31,604 patients with acute or chronic coronary syndromes and compared early aspirin discontinuation against continued DAPT. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the four deployed trials. The pooled hazard ratio for net adverse clinical events was 0.74 (95% CI 0.67 to 0.81), with substantial heterogeneity (Q 12.0 on three degrees of freedom, I-squared 75 percent). TWILIGHT (HR 0.56) and TICO (HR 0.66) show stronger benefit than HOST-EXAM (HR 0.73) and GLOBAL LEADERS (HR 0.87), reflecting different DAPT durations and risk populations. P2Y12 monotherapy after one to three months of DAPT reduces bleeding without a clear ischemic penalty. Effect magnitude depends on DAPT timing, population risk, and whether the composite emphasises bleeding or ischemia.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30846-30919 in rewrite-workbook.txt_

---

## Entry 411 ([411/921]) — DupilumabCOPDLivingMA

<details><summary>Metadata</summary>

```
TITLE: Dupilumab in Type 2 Inflammation COPD: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: RR for annualized COPD exacerbation rate
DATA: 2 RCTs (BOREAS, NOTUS), 1,874 patients, CT.gov sourced
PATH: C:\Projects\Dupilumab_COPD_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does dupilumab, an IL-4 receptor alpha antagonist, reduce moderate or severe exacerbations in patients with chronic obstructive pulmonary disease and elevated blood eosinophils? Two randomized phase 3 trials enrolling 1,874 patients with COPD, blood eosinophils above 300 cells per microliter, and at least one prior exacerbation despite triple inhaler therapy compared dupilumab 300 mg subcutaneously every two weeks against placebo over 52 weeks. DerSimonian-Laird random-effects meta-analysis pooled risk ratios on the log scale with HKSJ correction. The pooled risk ratio for annualized moderate or severe exacerbations was 0.77 (95% CI 0.64-0.93), with no detectable heterogeneity (I-squared 0%). Both trials demonstrated parallel improvements in lung function and quality of life. Dupilumab reduces COPD exacerbations by 23 percent in the type 2 inflammation phenotype defined by elevated eosinophils. Effect outside this phenotype is unproven, long-term safety beyond one year is unknown, and biomarker thresholds for treatment selection remain unsettled.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30920-30993 in rewrite-workbook.txt_

---

## Entry 412 ([412/921]) — SemaglutideCKDLivingMA

<details><summary>Metadata</summary>

```
TITLE: Semaglutide in Diabetic Kidney Disease: Living Meta-Analysis (FLOW Trial)
TYPE: living-ma  |  ESTIMAND: HR for kidney composite outcome
DATA: 1 RCT (FLOW), 3,533 patients, CT.gov sourced
PATH: C:\Projects\Semaglutide_CKD_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does semaglutide reduce kidney disease progression and cardiovascular death in patients with type 2 diabetes and chronic kidney disease? The FLOW randomized controlled trial enrolled 3,533 patients with type 2 diabetes and chronic kidney disease (eGFR 25 to 75 mL/min/1.73m2 with elevated albuminuria) and compared subcutaneous semaglutide 1 mg weekly against placebo on top of standard renin-angiotensin system blockade. The trial reported the composite kidney outcome as a single hazard ratio with no meta-analytic pooling possible from one trial. The hazard ratio for the primary kidney composite (50 percent eGFR decline, ESKD, kidney death, or cardiovascular death) was 0.76 (95% CI 0.66-0.88, P less than 0.001). Subgroup benefit was consistent across age, sex, baseline eGFR, and albuminuria categories. Semaglutide reduces kidney and cardiovascular events by 24 percent in diabetic chronic kidney disease. Generalizability to non-diabetic CKD is unknown, and the trial was stopped early for efficacy.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 30994-31067 in rewrite-workbook.txt_

---

## Entry 413 ([413/921]) — ARNIHFLivingMA

<details><summary>Metadata</summary>

```
TITLE: Sacubitril/Valsartan Across Heart Failure Spectrum: Living Meta-Analysis of Randomized Trials
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 3 RCTs (PARADIGM-HF, PARAGON-HF, PARADISE-MI), 19,519 patients, CT.gov sourced
PATH: C:\Projects\Finrenone\ARNI_HF_REVIEW.html
```

</details>

### Original (frozen — do not edit)

```
Does sacubitril-valsartan reduce cardiovascular death or heart failure hospitalization across the heart failure ejection fraction spectrum compared with renin-angiotensin system blockade alone? Three randomized controlled trials enrolling 19,519 patients with HFrEF, HFpEF, or post-myocardial infarction left ventricular dysfunction compared sacubitril-valsartan against enalapril or valsartan. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for cardiovascular death or heart failure hospitalization was 0.84 (95% CI 0.78-0.90), with low heterogeneity (I-squared 11%). Effect was strongest in HFrEF (PARADIGM-HF) and attenuated in HFpEF and post-MI populations, suggesting ejection fraction modifies treatment effect. Sacubitril-valsartan reduces composite heart failure events by 16 percent across the EF spectrum, with the largest absolute benefit in reduced ejection fraction. Hypotension and angioedema are notable adverse effects, transition from ACE inhibitors requires a 36-hour washout, and HFpEF benefit is borderline and population-dependent.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31068-31141 in rewrite-workbook.txt_

---

## Entry 414 ([414/921]) — LivingMAPortfolio

<details><summary>Metadata</summary>

```
TITLE: Living Evidence Portfolio: 57 Reproducible Single-File Meta-Analyses Across 12 Specialties
TYPE: tool  |  ESTIMAND: N/A (portfolio benchmark validation)
DATA: 57 living MA apps across 12 specialties, 766 trials, 23 published benchmarks
PATH: C:\Projects\LivingMA_Portfolio
```

</details>

### Original (frozen — do not edit)

```
Can a transparent portfolio of living systematic reviews maintain methodological fidelity at scale across multiple medical specialties using a single-file HTML architecture? We built and validated 57 living meta-analysis applications across 12 specialties (cardiology, oncology, nephrology, pulmonology, neurology, hepatology, dermatology, peripheral vascular, pulmonary vascular, cardiometabolic, interventional, network meta-analysis), each comprising approximately 14,000 lines of self-contained HTML, JavaScript, and inlined CSS. Every app embeds 31 analytic engines including DerSimonian-Laird pooling, Hartung-Knapp adjustment, GRADE assessment, cross-validation, provenance hashing, and 18 automated quality checks. Each pooled estimate was independently parsed and compared against published meta-analytic benchmarks for 23 of the 57 topics where direct comparators existed. All 23 benchmarked apps reproduced their published pooled estimates within 10 percent of the reference, demonstrating computational fidelity at portfolio scale. The portfolio is constrained by reliance on aggregate trial data and cannot replicate analyses requiring individual participant data.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31142-31217 in rewrite-workbook.txt_

---

## Entry 415 ([493/921]) — EvidenceCollapsar

<details><summary>Metadata</summary>

```
TITLE: The Evidence Collapsar: A Quantum Meta-Analysis Engine
TYPE: methods  |  ESTIMAND: Quantum-Collapsed Hazard Ratio and Von Neumann Entropy
DATA: Simulated 501 MLM Systematic Reviews
PATH: C:\Users\user\evidence-collapsar
```

</details>

### Original (frozen — do not edit)

```
Do classical inverse-variance meta-analyses overstate clinical certainty by ignoring the unmeasured bias inherent in observational and poorly-controlled trials? We re-evaluated 5 simulated systematic reviews using a novel Quantum Probability framework, representing each trial as a two-level state vector (qubit) where amplitudes correspond to 'Valid' and 'Biased' probabilities. Our "Evidence Collapsar" pipeline calculates the mixed density matrix across trials to compute a final observer-dependent Hazard Ratio and the system's Von Neumann Entropy. In domains with high bias probability, such as early COVID-19 ivermectin trials, the quantum-collapsed HR shifts significantly toward the null (1.0), whereas robust reviews maintain their effect sizes with low quantum entropy. This method provides a mathematically rigorous penalization for structural ambiguity, moving beyond deterministic pooling. The approach is limited by the requirement for accurate prior estimation of the bias probabilities for individual trials, which remains a subjective input.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31218-31293 in rewrite-workbook.txt_

---

## Entry 416 ([494/921]) — TDA-Meta

<details><summary>Metadata</summary>

```
TITLE: Topological Evidence Gaps: Identifying Structural Voids in Global Medical Research
TYPE: methods  |  ESTIMAND: Topological Isolation Score (0-100) via Persistent Homology
DATA: Simulated 3D Clinical Domains (Socioeconomic, Prevalence, Infrastructure)
PATH: C:\Users\user\tda-meta
```

</details>

### Original (frozen — do not edit)

```
Does the current corpus of clinical trials adequately cover the global health landscape, or are there structural voids where evidence cannot be safely transported? We mapped simulated global health domains into a 3D clinical space (Socioeconomic Index, Disease Prevalence, Healthcare Access) and applied 0-D Persistent Homology (Topological Data Analysis) to identify structural connectivity. The algorithm computes the birth and death of connected components, isolating "evidence gaps" based on their topological persistence. Regions such as 'Somalia Neglected Tropical Diseases' emerged as extreme topological voids with isolation scores exceeding 70%, indicating a complete lack of proximal evidence for transportability. This TDA approach moves beyond standard demographic summaries, proving mathematically that no existing Western-centric trial data can be safely transported to these isolated domains without catastrophic calibration failure. The analysis is limited by the heuristic dimensionality reduction of the clinical space, requiring higher-fidelity IHME covariates for fully rigorous topological mapping.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31294-31369 in rewrite-workbook.txt_

---

## Entry 417 ([495/921]) — RetractionGravity

<details><summary>Metadata</summary>

```
TITLE: Retraction Gravity: Portfolio Impact Mapping of Clinical Evidence Failures
TYPE: methods  |  ESTIMAND: Attenuated Reliability Score via DAG Propagation
DATA: Simulated Clinical Research Dependency Graph (Nodes/Edges)
PATH: C:\Users\user\retraction-gravity
```

</details>

### Original (frozen — do not edit)

```
How does the retraction of a foundational clinical trial or the falsification of a core statistical method impact a cascading portfolio of dependent medical research? We mapped a simulated medical evidence portfolio as a Directed Acyclic Graph (DAG) consisting of datasets, methods, and clinical projects. We applied a "Retraction Gravity" algorithm, modeled as a Bayesian belief shock, to propagate reliability failures from root nodes through all dependent child nodes. In scenarios where a core dataset is retracted due to fraud, the model demonstrates that immediate downstream projects drop to near-zero reliability, while collateral projects suffer attenuated but significant "TruthCert" degradation (e.g., portfolio health dropping from 100% to 68%). This framework replaces static evidence grading with a dynamic, living portfolio health score. The model is limited by the assumption of uniform gravity attenuation and requires precise mapping of all code and data dependencies to accurately quantify systemic clinical risk.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31370-31443 in rewrite-workbook.txt_

---

## Entry 418 ([415/921]) — FinerenoneLivingMA

<details><summary>Metadata</summary>

```
TITLE: Finerenone in Cardiorenal Disease: Living Meta-Analysis of Phase 3 Trials
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 4 RCTs (FIDELIO-DKD, FIGARO-DKD, FINEARTS-HF, ARTS-HF), 19,022 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does finerenone, a non-steroidal mineralocorticoid receptor antagonist, reduce major adverse cardiovascular events in adults with chronic kidney disease, type 2 diabetes, or heart failure with preserved ejection fraction? Four randomized placebo-controlled phase 3 trials enrolling 19,022 patients across diabetic kidney disease and HFpEF populations compared finerenone against placebo on top of guideline-directed therapy. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ adjustment. The pooled hazard ratio for the cardiovascular composite was 0.86 (95% CI 0.79-0.92), with no detectable heterogeneity (I-squared 0%). Effect was consistent across CKD severity strata, baseline albuminuria, and ejection fraction subgroups. Finerenone reduces cardiovascular events by 14 percent across cardiorenal-metabolic populations and is the first MRA validated for HFpEF. Hyperkalemia is more common with finerenone than placebo, monitoring requirements increase pharmacy burden, and absolute risk reduction is modest in lower-risk subgroups.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31444-31517 in rewrite-workbook.txt_

---

## Entry 419 ([416/921]) — GLP1CVOTLivingMA

<details><summary>Metadata</summary>

```
TITLE: GLP-1 Receptor Agonists in Cardiovascular Outcome Trials: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 10 RCTs (LEADER, SUSTAIN-6, SELECT, REWIND, PIONEER-6, HARMONY, EXSCEL, ELIXA, AMPLITUDE-O, FREEDOM-CVO), 79,816 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Do GLP-1 receptor agonists reduce major adverse cardiovascular events in adults with type 2 diabetes or established cardiovascular disease across the full spectrum of approved agents? Ten randomized placebo-controlled cardiovascular outcome trials enrolling 79,816 patients compared GLP-1 receptor agonists against placebo over median follow-up of 1.6 to 5.4 years. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the three-component MACE composite was 0.86 (95% CI 0.81-0.90), with moderate heterogeneity (I-squared 39%) reflecting differences between exenatide, lixisenatide, and the more potent agents semaglutide, liraglutide, and dulaglutide. The mortality reduction was driven primarily by semaglutide and liraglutide. GLP-1 receptor agonists reduce cardiovascular events by 14 percent across the diabetes and obesity spectrum. Effect heterogeneity by molecule is clinically relevant, gastrointestinal tolerability limits real-world persistence, and oral semaglutide trial data are still maturing.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31518-31591 in rewrite-workbook.txt_

---

## Entry 420 ([417/921]) — SGLT2HFLivingMA

<details><summary>Metadata</summary>

```
TITLE: SGLT2 Inhibitors in Heart Failure: Living Meta-Analysis Across the EF Spectrum
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 5 RCTs (DAPA-HF, EMPEROR-Reduced, EMPEROR-Preserved, DELIVER, SOLOIST-WHF), 21,947 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Do SGLT2 inhibitors reduce cardiovascular death or heart failure hospitalization in patients with heart failure across the full ejection fraction spectrum? Five randomized placebo-controlled trials enrolling 21,947 patients with HFrEF, HFmrEF, or HFpEF compared dapagliflozin or empagliflozin against placebo over median follow-up of 16 to 27 months. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio was 0.77 (95% CI 0.72-0.82), with no detectable heterogeneity (I-squared 0%) across EF strata. Subgroup analysis showed consistent benefit irrespective of diabetes status, baseline diuretic use, and natriuretic peptide levels. SGLT2 inhibitors reduce cardiovascular events by 23 percent across the heart failure spectrum, establishing them as foundational therapy in all four pillars of HF guideline-directed treatment. Genitourinary infections are more common, mycotic infections require monitoring, and class-effect generalisability to canagliflozin remains less robustly demonstrated in HF.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31592-31665 in rewrite-workbook.txt_

---

## Entry 421 ([418/921]) — SGLT2CKDLivingMA

<details><summary>Metadata</summary>

```
TITLE: SGLT2 Inhibitors in Chronic Kidney Disease: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for kidney composite outcome
DATA: 3 RCTs (CREDENCE, DAPA-CKD, EMPA-KIDNEY), 19,609 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Do SGLT2 inhibitors reduce kidney disease progression and renal death in adults with chronic kidney disease, with or without diabetes? Three randomized placebo-controlled trials enrolling 19,609 patients with CKD stages 2-4 and varying degrees of albuminuria compared canagliflozin, dapagliflozin, or empagliflozin against placebo on top of renin-angiotensin system blockade. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the kidney composite (sustained eGFR decline, ESKD, or renal death) was 0.68 (95% CI 0.62-0.75), with low heterogeneity (I-squared 18%). Benefit was consistent across diabetes status, baseline eGFR, and albuminuria categories. SGLT2 inhibitors reduce kidney disease progression by 32 percent across diabetic and non-diabetic CKD. Effect attenuates at very low eGFR, low-albuminuria subgroups derive smaller benefit, and acute eGFR drops at initiation can cause unnecessary discontinuation.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31666-31739 in rewrite-workbook.txt_

---

## Entry 422 ([419/921]) — BempedoicAcidLivingMA

<details><summary>Metadata</summary>

```
TITLE: Bempedoic Acid for Cardiovascular Prevention: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 4 RCTs (CLEAR Outcomes, CLEAR Harmony, CLEAR Wisdom, CLEAR Tranquility), 17,891 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does bempedoic acid, an ATP-citrate lyase inhibitor, reduce major adverse cardiovascular events in statin-intolerant patients or as add-on therapy to maximally tolerated statins? Four randomized placebo-controlled trials enrolling 17,891 patients with established or high-risk atherosclerotic cardiovascular disease compared bempedoic acid against placebo. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the four-component MACE composite was 0.90 (95% CI 0.72-1.12), with moderate heterogeneity (I-squared 42%) driven by the larger CLEAR Outcomes trial. CLEAR Outcomes alone showed HR 0.87 (0.79-0.96) for the primary endpoint. Bempedoic acid offers a non-statin option for LDL cholesterol lowering with measurable but modest cardiovascular benefit. Long-term cardiovascular benefit beyond CLEAR Outcomes follow-up is unproven, gout flare risk requires monitoring, and the effect is smaller than statin trials of comparable LDL reduction.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31740-31813 in rewrite-workbook.txt_

---

## Entry 423 ([420/921]) — PCSK9LivingMA

<details><summary>Metadata</summary>

```
TITLE: PCSK9 Monoclonal Antibodies for Cardiovascular Prevention: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 2 RCTs (FOURIER, ODYSSEY OUTCOMES), 46,488 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Do PCSK9 monoclonal antibodies reduce major adverse cardiovascular events in patients with established atherosclerotic cardiovascular disease on maximally tolerated statin therapy? Two randomized placebo-controlled trials enrolling 46,488 patients with stable ASCVD or recent acute coronary syndrome compared evolocumab or alirocumab against placebo over median follow-up of 22 to 33 months. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the cardiovascular composite was 0.85 (95% CI 0.80-0.90), with no detectable heterogeneity (I-squared 0%). LDL cholesterol reductions averaged 60 percent in both trials, and absolute benefit was greatest in patients with the highest baseline cholesterol or recurrent events. PCSK9 inhibitors reduce cardiovascular events by 15 percent and offer the largest LDL reduction available outside lipoprotein apheresis. High cost limits widespread access, injection site reactions affect a minority, and absolute event reduction in stable disease is modest at 1 to 2 percent.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31814-31887 in rewrite-workbook.txt_

---

## Entry 424 ([421/921]) — IVIronHFLivingMA

<details><summary>Metadata</summary>

```
TITLE: Intravenous Iron in Heart Failure with Iron Deficiency: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 4 RCTs (CONFIRM-HF, AFFIRM-AHF, IRONMAN, HEART-FID), 6,404 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does intravenous ferric carboxymaltose or ferric derisomaltose reduce cardiovascular events in patients with heart failure and iron deficiency? Four randomized placebo-controlled trials enrolling 6,404 patients with HFrEF or HFmrEF and concomitant iron deficiency compared intravenous iron against placebo over median follow-up of 12 to 21 months. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the composite of cardiovascular death or first heart failure hospitalization was 0.87 (95% CI 0.79-0.96), with no detectable heterogeneity (I-squared 0%). Total heart failure hospitalisation reduction was the dominant component of benefit, while cardiovascular mortality showed no signal. Intravenous iron reduces heart failure hospitalisations by 13 percent in iron-deficient HFrEF without altering mortality. Hypophosphataemia is a class concern with ferric carboxymaltose, the optimal iron deficiency definition (ferritin or transferrin saturation cutoff) is contested, and oral iron has not shown comparable benefit.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31888-31961 in rewrite-workbook.txt_

---

## Entry 425 ([422/921]) — AblationAFLivingMA

<details><summary>Metadata</summary>

```
TITLE: Catheter Ablation for Atrial Fibrillation: Living Meta-Analysis of Hard Endpoints
TYPE: living-ma  |  ESTIMAND: HR for all-cause mortality or composite events
DATA: 4 RCTs (CASTLE-AF, CABANA, EAST-AFNET 4, RAFT-AF), 7,211 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does catheter ablation for atrial fibrillation reduce mortality or cardiovascular events compared with medical rhythm or rate control across heart failure and unselected atrial fibrillation populations? Four randomized controlled trials enrolling 7,211 patients with paroxysmal or persistent atrial fibrillation compared ablation-based rhythm control against medical therapy. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the trial-specific composite primary endpoint was 0.77 (95% CI 0.68-0.87), with no detectable heterogeneity. Effect was largest in CASTLE-AF (HFrEF subgroup, HR 0.62) and EAST-AFNET 4 (early-stage AF, HR 0.79), and attenuated in CABANA which enrolled an unselected population. Catheter ablation reduces hard cardiovascular outcomes by 23 percent across selected atrial fibrillation populations. Procedural complications are non-trivial, operator volume strongly modifies outcomes, and benefit in unselected lower-risk AF populations remains uncertain.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 31962-32035 in rewrite-workbook.txt_

---

## Entry 426 ([423/921]) — RivaroxabanVascLivingMA

<details><summary>Metadata</summary>

```
TITLE: Low-Dose Rivaroxaban for Vascular Protection: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 4 RCTs (COMPASS, VOYAGER-PAD, ATLAS ACS 2, COMMANDER HF), 45,242 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does low-dose rivaroxaban added to antiplatelet therapy reduce major adverse cardiovascular events in vascular disease populations including stable CAD, PAD, post-ACS, and heart failure? Four randomized placebo-controlled trials enrolling 45,242 patients compared rivaroxaban 2.5 mg twice daily plus aspirin against aspirin or placebo over 21 to 28 months. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the cardiovascular composite was 0.85 (95% CI 0.78-0.93), with moderate heterogeneity (I-squared 49%) reflecting different patient populations. Effect was consistent in stable atherosclerotic disease and post-revascularization PAD but absent in heart failure (COMMANDER HF was null). Low-dose rivaroxaban plus aspirin reduces cardiovascular events by 15 percent in vascular disease but offers no benefit in heart failure. Major bleeding risk is increased, the dual-pathway strategy is reserved for patients without high bleeding risk, and its role versus DAPT in post-MI patients remains nuanced.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32036-32109 in rewrite-workbook.txt_

---

## Entry 427 ([424/921]) — ColchicineCVDLivingMA

<details><summary>Metadata</summary>

```
TITLE: Colchicine for Cardiovascular Disease: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 5 RCTs (COLCOT, LoDoCo2, COPS, CLEAR-SYNERGY, CONVINCE), 22,205 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does low-dose colchicine reduce major adverse cardiovascular events in patients with chronic coronary disease, recent myocardial infarction, or recent ischemic stroke? Five randomized controlled trials enrolling 22,205 patients across post-MI, stable CAD, post-PCI, and post-stroke populations compared colchicine 0.5 mg daily against placebo or usual care over median follow-up of 6 to 36 months. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the cardiovascular composite was 0.88 (95% CI 0.75-1.02), with moderate heterogeneity (I-squared 45%) driven by divergent CLEAR-SYNERGY (HR 0.99) and LoDoCo2 (HR 0.69) results. The COLCOT and LoDoCo2 trials supported the original benefit signal while CLEAR-SYNERGY in post-MI showed no effect. Colchicine offers a modest and population-dependent reduction in cardiovascular events. The CLEAR-SYNERGY null result challenges the broader anti-inflammatory CV hypothesis, gastrointestinal intolerance affects 5 to 10 percent of patients, and optimal patient selection is unresolved.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32110-32183 in rewrite-workbook.txt_

---

## Entry 428 ([425/921]) — SotaterceptPAHLivingMA

<details><summary>Metadata</summary>

```
TITLE: Sotatercept in Pulmonary Arterial Hypertension: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for time to clinical worsening
DATA: 3 RCTs (STELLAR, HYPERION, ZENITH), 818 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does sotatercept, an activin signaling inhibitor, reduce clinical worsening events in patients with pulmonary arterial hypertension across treatment-naive, established, and high-risk populations? Three randomized placebo-controlled phase 3 trials enrolling 818 patients with WHO Group 1 PAH compared sotatercept against placebo on top of stable background PAH therapy. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for time to clinical worsening was 0.22 (95% CI 0.15-0.31), with no detectable heterogeneity (I-squared 0%) across newly diagnosed, established, and high-risk PAH cohorts. Effect magnitude was consistent across STELLAR, HYPERION, and ZENITH despite differences in baseline risk and background therapy. Sotatercept reduces clinical worsening events by 78 percent and represents a new mechanistic class for PAH targeting bone morphogenetic protein signaling. Long-term safety data beyond two years are immature, anaemia and telangiectasias are common, and access in low- and middle-income countries is constrained by injection cost.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32184-32257 in rewrite-workbook.txt_

---

## Entry 429 ([426/921]) — TDXdBreastLivingMA

<details><summary>Metadata</summary>

```
TITLE: Trastuzumab Deruxtecan in HER2-Positive Breast Cancer: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for progression-free survival
DATA: 4 RCTs (DESTINY-Breast02/03/04/06), 2,555 patients
PATH: C:\Projects\TDXd_Breast_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does trastuzumab deruxtecan, an anti-HER2 antibody-drug conjugate, improve progression-free survival across HER2-positive and HER2-low metastatic breast cancer settings? Four randomized phase 3 trials deployed in this living meta-analysis (DESTINY-Breast03, DESTINY-Breast04, DESTINY-Breast02, DESTINY-Breast06) enrolled 2,555 patients across pretreated HER2-positive, pretreated HER2-low, and first-line HER2-low settings. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the four deployed trials. The pooled hazard ratio for progression-free survival was 0.46 (95% CI 0.41 to 0.52), with substantial heterogeneity (I-squared 90 percent) reflecting different control arms and HER2 expression strata. Benefit was largest against ado-trastuzumab emtansine in DESTINY-Breast03 (HR 0.28) and smaller against physician-choice chemotherapy in DESTINY-Breast06 (HR 0.63). Trastuzumab deruxtecan reduces disease progression by approximately 54 percent and has redefined treatment across HER2-expressing breast cancer subtypes. Interstitial lung disease is a class effect requiring vigilance, optimal HER2-low cutoff is being refined, and cost limits global access.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32258-32331 in rewrite-workbook.txt_

---

## Entry 430 ([427/921]) — ObesityNMALivingMA

<details><summary>Metadata</summary>

```
TITLE: GLP-1 and Incretin Therapies for Obesity: Living Network Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for at least 5 percent body weight loss
DATA: 5 RCTs (STEP-1, SURMOUNT-1/-2, Wharton orforglipron, semaglutide oral), patients across 5 trials
PATH: C:\Projects\Obesity_NMA_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Which incretin-based pharmacotherapy produces the largest weight reduction in adults with obesity or overweight with comorbidities? Five randomized placebo-controlled trials evaluating semaglutide 2.4 mg, tirzepatide 5/10/15 mg, and orforglipron 36 mg were combined in a network meta-analysis using a common placebo arm. DerSimonian-Laird random-effects pooling on the log odds ratio scale with HKSJ correction synthesised the proportion achieving at least 5 percent body weight loss. The pooled odds ratio against placebo was 13.64 (95% CI 7.97-23.34), with substantial heterogeneity (I-squared 91%) reflecting dose-dependent effects from 5 mg tirzepatide to 15 mg tirzepatide. Tirzepatide 15 mg ranked first for weight loss probability, followed by semaglutide 2.4 mg and orforglipron 36 mg. Incretin-based pharmacotherapy is reshaping obesity care with progressively larger effects from earlier to newer agents. Trial follow-up is mostly under two years, weight regain on discontinuation is substantial, and head-to-head comparisons against bariatric surgery remain limited.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32332-32405 in rewrite-workbook.txt_

---

## Entry 431 ([428/921]) — AntiAmyloidADLivingMA

<details><summary>Metadata</summary>

```
TITLE: Anti-Amyloid Antibodies in Early Alzheimers Disease: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for cognitive decline reduction
DATA: 4 RCTs (Clarity AD, TRAILBLAZER-ALZ 2, Study 201, ABBY/BLAZE), patients across trials
PATH: C:\Projects\AntiAmyloid_AD_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Do anti-amyloid monoclonal antibodies (lecanemab, donanemab, aducanumab) slow cognitive decline in patients with early symptomatic Alzheimers disease and confirmed amyloid pathology? Four randomized placebo-controlled trials enrolling patients with early Alzheimers disease compared anti-amyloid antibodies against placebo over 18 to 24 months. DerSimonian-Laird random-effects meta-analysis pooled CDR-SB change ratios with HKSJ correction. The pooled odds ratio for cognitive decline reduction favoured anti-amyloid therapy, with substantial heterogeneity (I-squared 74%) reflecting differences between agents and patient selection. Lecanemab and donanemab phase 3 trials demonstrated 27 to 35 percent slowing of CDR-SB decline, while aducanumab data were inconsistent across trials. Anti-amyloid antibodies modestly slow Alzheimers disease progression at the population level. Amyloid-related imaging abnormalities (ARIA) affect 10 to 30 percent of treated patients including symptomatic cases, infusion logistics are complex, and clinically meaningful benefit at the individual patient level remains contested.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32406-32479 in rewrite-workbook.txt_

---

## Entry 432 ([429/921]) — BimekizumabPsoriasisLivingMA

<details><summary>Metadata</summary>

```
TITLE: Bimekizumab for Plaque Psoriasis: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for PASI 90 response at week 16
DATA: 4 RCTs (BE VIVID, BE READY, BE SURE, BE RADIANT), patients across trials
PATH: C:\Projects\Bimekizumab_Pso_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does bimekizumab, an IL-17A and IL-17F dual inhibitor, achieve superior skin clearance compared with placebo or other biologics in adults with moderate to severe plaque psoriasis? Four randomized phase 3 trials enrolling patients with moderate to severe plaque psoriasis compared bimekizumab against placebo, ustekinumab, adalimumab, or secukinumab. DerSimonian-Laird random-effects meta-analysis pooled odds ratios for PASI 90 response on the log scale with HKSJ correction. The pooled odds ratio for PASI 90 versus placebo was 25.69 (95% CI 4.29-153.92), with extreme heterogeneity (I-squared 97%) reflecting head-to-head versus placebo control comparators. Bimekizumab consistently outperformed comparators including ustekinumab and secukinumab in head-to-head trials, with PASI 100 rates exceeding 60 percent. Bimekizumab achieves the highest documented skin clearance rates among approved psoriasis biologics. Oral candidiasis incidence is markedly elevated due to IL-17F blockade, long-term durability beyond two years is being characterized, and direct comparisons against guselkumab and risankizumab in head-to-head trials are limited.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32480-32553 in rewrite-workbook.txt_

---

## Entry 433 ([430/921]) — LipidHubLivingMA

<details><summary>Metadata</summary>

```
TITLE: Combined Lipid-Lowering Strategies: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 5 RCTs (REDUCE-IT, RESPECT-EPA, STRENGTH, IMPROVE-IT, FOURIER), 64,454 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Do combined lipid-lowering strategies beyond statin monotherapy reduce major adverse cardiovascular events across heterogeneous trial designs and add-on agents? Five randomized placebo-controlled trials enrolling 64,454 patients with established or high-risk atherosclerotic disease compared icosapent ethyl, ethyl-EPA, ezetimibe, or PCSK9 inhibitors against placebo on top of statin therapy. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the cardiovascular composite was 0.89 (95% CI 0.76-1.04), with substantial heterogeneity (I-squared 79%) reflecting widely divergent agents and trial designs. Effect was largest in REDUCE-IT (HR 0.75, icosapent ethyl) and FOURIER (HR 0.85, evolocumab), but null in STRENGTH (omega-3 carboxylic acids). Combined lipid-lowering offers heterogeneous benefit dependent on specific agent and patient population. Mineral oil control in REDUCE-IT remains controversial, omega-3 ester formulation may modify effect, and cost effectiveness varies markedly across the agents.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32554-32627 in rewrite-workbook.txt_

---

## Entry 434 ([431/921]) — DCBPADLivingMA

<details><summary>Metadata</summary>

```
TITLE: Drug-Coated Balloons in Peripheral Artery Disease: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for target lesion revascularization
DATA: 5 RCTs (IN.PACT SFA, LEVANT 2, ILLUMENATE, RANGER II SFA, BIOLUX P-III), patients across trials
PATH: C:\Projects\DCB_PAD_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Do drug-coated balloons reduce target lesion revascularization compared with plain balloon angioplasty in patients with femoropopliteal peripheral artery disease? Five randomized controlled trials enrolling patients with symptomatic femoropopliteal disease compared paclitaxel-coated balloons against uncoated balloons over 12-month primary follow-up. DerSimonian-Laird random-effects meta-analysis pooled odds ratios on the log scale with HKSJ correction. The pooled odds ratio for target lesion revascularization was 2.07 (95% CI 1.01-4.25) in favour of drug-coated balloons, with substantial heterogeneity (I-squared 85%) reflecting differences in lesion length, vessel diameter, and operator technique. Patency advantages over uncoated balloons were consistent across trials but late mortality concerns from a 2018 meta-analysis prompted FDA review. Drug-coated balloons reduce repeat revascularization in femoropopliteal PAD with maintained primary patency. The 2018-era mortality signal was not confirmed in subsequent analyses, optimal paclitaxel dose-density remains debated, and long-term limb salvage benefit is uncertain.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32628-32701 in rewrite-workbook.txt_

---

## Entry 435 ([432/921]) — PAHNMALivingMA

<details><summary>Metadata</summary>

```
TITLE: PAH Combination Therapy: Living Network Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for clinical worsening
DATA: 4 RCTs (STELLAR, GRIPHON, SERAPHIN, PATENT-1), 2,352 patients
PATH: C:\Projects\PAH_NMA_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Which combination therapy strategy minimises clinical worsening in pulmonary arterial hypertension? Four randomized placebo-controlled trials deployed in this living meta-analysis (STELLAR, GRIPHON, SERAPHIN, PATENT-1) enrolled 2,352 patients with WHO Group 1 PAH and compared sotatercept, selexipag, macitentan, or riociguat against placebo. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the four deployed trials. The pooled hazard ratio for clinical worsening was 0.52 (95% CI 0.43 to 0.63), with substantial heterogeneity (Q 11.2 on three degrees of freedom, I-squared 73 percent). STELLAR (HR 0.16) with activin-receptor sotatercept shows the largest effect; SERAPHIN (HR 0.55), GRIPHON (HR 0.60), and PATENT-1 (HR 0.46) give consistent endothelin and cGMP-pathway benefit. Combination and targeted PAH therapies reduce clinical worsening by approximately forty-eight percent across pulmonary vasodilator mechanisms. Heterogeneity reflects mechanism differences across drug classes rather than trial quality, and head-to-head comparisons remain limited.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32702-32775 in rewrite-workbook.txt_

---

## Entry 436 ([433/921]) — ResmetiromMASHLivingMA

<details><summary>Metadata</summary>

```
TITLE: Resmetirom for Metabolic Dysfunction-Associated Steatohepatitis: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for NASH resolution at week 52
DATA: 3 RCTs (MAESTRO-NASH, MAESTRO-NAFLD-1, Phase 2 MGL-3196), 1,411 patients
PATH: C:\Projects\Resmetirom_MASH_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does resmetirom, a thyroid hormone receptor beta agonist, achieve NASH resolution and fibrosis improvement in patients with metabolic dysfunction-associated steatohepatitis? Three randomized placebo-controlled trials enrolling 1,411 patients with biopsy-proven NASH compared resmetirom 80 mg or 100 mg against placebo over 52 weeks. DerSimonian-Laird random-effects meta-analysis pooled odds ratios for NASH resolution on the log scale with HKSJ correction. The pooled odds ratio was 5.76 (95% CI 3.30-10.08), with moderate heterogeneity (I-squared 67%) reflecting dose-response between 80 mg and 100 mg arms and between phase 2 and phase 3 designs. NASH resolution rates were 26 percent (80 mg) and 30 percent (100 mg) versus 10 percent placebo in the pivotal MAESTRO-NASH trial. Resmetirom achieves the first FDA-approved pharmacotherapy for NASH with measurable histologic and biochemical improvement. Effect on hard liver outcomes (decompensation, transplant, mortality) is unproven, biopsy-based eligibility is invasive and limits real-world uptake, and long-term durability beyond one year is unknown.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32776-32849 in rewrite-workbook.txt_

---

## Entry 437 ([434/921]) — KBindersLivingMA

<details><summary>Metadata</summary>

```
TITLE: Potassium Binders for RAASi Enablement: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for normokalemia maintenance
DATA: 3 RCTs with analysis data (OPAL-HK, HARMONIZE, DIAMOND), 1,227 patients; AMETHYST-DN pending extraction
PATH: C:\Projects\K_Binders_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Do oral potassium binders (patiromer, sodium zirconium cyclosilicate) maintain normokalemia and enable continuation of renin-angiotensin-aldosterone system inhibitors in patients with chronic hyperkalemia? Three randomized placebo-controlled trials with complete analysis data deployed in this living meta-analysis (OPAL-HK, HARMONIZE, DIAMOND) enrolled 1,227 patients with elevated baseline potassium on RAASi therapy and compared potassium binders against placebo. DerSimonian-Laird random-effects meta-analysis pooled odds ratios on the log scale for maintaining normokalemia. The pooled odds ratio was 4.40 (95% CI 1.90 to 10.21), with substantial heterogeneity (I-squared 85 percent) reflecting different binder agents, doses, and patient populations. OPAL-HK (OR 8.60), HARMONIZE (OR 4.60), and DIAMOND (OR 2.42) all favour binders with decreasing effect size as trials moved to less selected populations. Potassium binders effectively maintain normokalemia in patients with hyperkalemia constraining RAASi optimization. Hard cardiovascular outcome data are absent, hypomagnesaemia is a concern with patiromer, and the absolute magnitude of long-term RAASi continuation benefit remains undemonstrated.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32850-32923 in rewrite-workbook.txt_

---

## Entry 438 ([435/921]) — TirzepatideCVLivingMA

<details><summary>Metadata</summary>

```
TITLE: Tirzepatide in Cardiometabolic Disease: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for at least 5 percent body weight loss
DATA: 4 RCTs (SURMOUNT-1/-2/-3/-4), 3,148 patients (pooled-arms subset)
PATH: C:\Projects\Tirzepatide_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does tirzepatide, a dual GIP and GLP-1 receptor agonist, achieve clinically meaningful weight reduction across obesity, type 2 diabetes, and weight maintenance settings? Four randomized placebo-controlled phase 3 trials with a pooled-arms subset of 3,148 patients with obesity, with or without diabetes, compared tirzepatide 5/10/15 mg weekly against placebo over 36 to 88 weeks. DerSimonian-Laird random-effects meta-analysis pooled odds ratios for at least 5 percent weight loss with HKSJ correction. The pooled odds ratio was 22.94 (95% CI 12.46-42.23), with substantial heterogeneity (I-squared 89%) reflecting dose-dependent effects across the 5 to 15 mg dose range. Mean weight reductions ranged from 15 to 21 percent across the highest dose arms. Tirzepatide produces the largest documented pharmacologic weight reduction approaching the lower end of bariatric surgery outcomes. Cardiovascular outcome trials remain pending, gastrointestinal tolerability and dose escalation logistics affect persistence, and weight regain following discontinuation is substantial.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32924-32997 in rewrite-workbook.txt_

---

## Entry 439 ([436/921]) — SemaglutideHFpEFLivingMA

<details><summary>Metadata</summary>

```
TITLE: Semaglutide in HFpEF with Obesity: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for KCCQ improvement
DATA: 2 RCTs (STEP-HFpEF, STEP-HFpEF DM), 1,145 patients
PATH: C:\Projects\Semaglutide_HFpEF_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does semaglutide improve heart failure symptoms and exercise capacity in patients with obesity and heart failure with preserved ejection fraction, with and without type 2 diabetes? Two randomized placebo-controlled trials enrolling 1,145 patients with HFpEF, obesity (BMI greater than 30), and KCCQ-CSS less than 90 compared semaglutide 2.4 mg weekly against placebo over 52 weeks. DerSimonian-Laird random-effects meta-analysis pooled odds ratios on the log scale with HKSJ correction. The pooled odds ratio for KCCQ improvement above the responder threshold was 1.98 (95% CI 1.33-2.94), with moderate heterogeneity (I-squared 62%) reflecting differences between non-diabetic and diabetic populations. Six-minute walk distance improvements were larger in the non-diabetic STEP-HFpEF cohort. Semaglutide produces meaningful symptomatic and functional improvements in obesity-related HFpEF. Hard cardiovascular outcomes are not the primary endpoint, generalizability beyond high-BMI HFpEF is limited, and the mechanism of benefit (weight loss versus direct cardiac effect) is debated.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 32998-33071 in rewrite-workbook.txt_

---

## Entry 440 ([437/921]) — TicagrelorMonoLivingMA

<details><summary>Metadata</summary>

```
TITLE: Ticagrelor Monotherapy after Short DAPT: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for net clinical benefit
DATA: 3 RCTs (TWILIGHT, TICO, GLOBAL LEADERS), 28,241 patients
PATH: C:\Projects\Ticagrelor_Mono_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does ticagrelor monotherapy after short-duration dual antiplatelet therapy reduce net adverse clinical events compared with continued DAPT in patients undergoing percutaneous coronary intervention? Three randomized controlled trials deployed in this living meta-analysis (TWILIGHT, TICO, GLOBAL LEADERS) enrolled 28,241 patients with acute or chronic coronary syndromes compared against continued DAPT for 12 months. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the three deployed trials. The pooled hazard ratio for the net clinical benefit composite was 0.81 (95% CI 0.73 to 0.89), with substantial heterogeneity (Q 19.1 on two degrees of freedom, I-squared 90 percent). TWILIGHT (HR 0.56) and TICO (HR 0.66) show stronger benefit than GLOBAL LEADERS (HR 0.93), reflecting differences in risk population and DAPT transition timing. Ticagrelor monotherapy after short DAPT reduces net adverse events but effect size is highly trial-dependent. Generalisability to complex PCI is uncertain, optimal DAPT duration before transition is contested, and aspirin-free strategies require careful patient selection.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33072-33145 in rewrite-workbook.txt_

---

## Entry 441 ([438/921]) — IcosapentEthylLivingMA

<details><summary>Metadata</summary>

```
TITLE: Icosapent Ethyl for Cardiovascular Prevention: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 3 RCTs (REDUCE-IT, STRENGTH, JELIS), 39,902 patients
PATH: C:\Projects\Icosapent_Ethyl_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does icosapent ethyl or pure EPA supplementation reduce major adverse cardiovascular events in patients with elevated triglycerides on statin therapy? Three randomized placebo-controlled trials deployed in this living meta-analysis (REDUCE-IT, STRENGTH, JELIS) enrolled 39,902 patients with elevated triglycerides and established or high-risk cardiovascular disease. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the three deployed trials. The pooled hazard ratio was 0.86 (95% CI 0.81 to 0.91), with substantial heterogeneity (I-squared 88 percent) reflecting divergent results across REDUCE-IT (HR 0.75), STRENGTH (HR 0.99), and JELIS (HR 0.81). The mineral oil placebo controversy in REDUCE-IT remains unresolved and likely contributes to the contrast with the null STRENGTH trial. Pure EPA formulations show cardiovascular benefit but the omega-3 carboxylic acid mixture in STRENGTH does not. Mineral oil placebo effects on inflammation and lipids confound REDUCE-IT interpretation, atrial fibrillation risk is increased with high-dose omega-3, and effect of generic fish oil is unproven.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33146-33219 in rewrite-workbook.txt_

---

## Entry 442 ([439/921]) — MavacamtenHCMLivingMA

<details><summary>Metadata</summary>

```
TITLE: Mavacamten in Hypertrophic Cardiomyopathy: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for symptomatic improvement
DATA: 3 RCTs (EXPLORER-HCM, VALOR-HCM, Phase 3 China), 444 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does mavacamten, a cardiac myosin inhibitor, improve symptoms and left ventricular outflow tract obstruction in patients with obstructive hypertrophic cardiomyopathy? Three randomized placebo-controlled trials enrolling 444 patients with symptomatic obstructive HCM compared mavacamten against placebo over 16 to 30 weeks. DerSimonian-Laird random-effects meta-analysis pooled odds ratios for the primary symptomatic composite with HKSJ correction. The pooled odds ratio was 6.67 (95% CI 2.09-21.30), with substantial heterogeneity (I-squared 79%) reflecting differences in baseline severity and outcome definition. EXPLORER-HCM in chronic obstructive HCM and VALOR-HCM in patients eligible for septal reduction therapy both showed substantial symptomatic improvement and LVOT gradient reduction. Mavacamten provides the first targeted pharmacotherapy for obstructive HCM with effect sizes comparable to invasive septal reduction. Reversible LVEF reduction requires monitoring, drug-drug interactions with CYP2C19 and CYP3A4 inhibitors are clinically relevant, and long-term outcome data on hard endpoints remain immature.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33220-33293 in rewrite-workbook.txt_

---

## Entry 443 ([440/921]) — ATTRCMLivingMA

<details><summary>Metadata</summary>

```
TITLE: Tafamidis and Vutrisiran in ATTR Cardiomyopathy: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for all-cause mortality
DATA: 4 RCTs (ATTR-ACT, ATTRibute-CM, HELIOS-B, APOLLO-B); APOLLO-B HR Peto-derived from event counts
PATH: C:\Projects\AttrCM_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Do TTR stabilizers (tafamidis, acoramidis) and TTR silencers (vutrisiran, patisiran) reduce all-cause mortality in transthyretin amyloid cardiomyopathy? Four placebo-controlled randomized trials (ATTR-ACT, ATTRibute-CM, HELIOS-B, APOLLO-B) enrolling patients with wild-type or hereditary disease were pooled, with APOLLO-B's hazard ratio imputed via Peto one-step log-rank from event counts. DerSimonian-Laird random-effects meta-analysis was applied on the log hazard ratio scale, with heterogeneity quantified by Cochran Q and I-squared. The pooled hazard ratio for all-cause mortality was 0.71 (95% CI 0.59 to 0.86), with no detectable heterogeneity and I-squared 0 percent across four trials. ATTR-ACT, ATTRibute-CM, and HELIOS-B contributed the dominant inverse-variance weight; APOLLO-B contributed low weight because its primary endpoint was six-minute walk distance with short mortality follow-up. TTR-targeted therapy reduces mortality by approximately 29 percent in ATTR cardiomyopathy across stabilizer and silencer mechanisms. Cost remains a major access barrier, and APOLLO-B's imputed hazard ratio should be replaced when longer follow-up yields a published estimate.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33294-33367 in rewrite-workbook.txt_

---

## Entry 444 ([441/921]) — IntensiveBPLivingMA

<details><summary>Metadata</summary>

```
TITLE: Intensive Blood Pressure Lowering: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for MACE composite
DATA: 3 RCTs (SPRINT, STEP, ESPRIT), 22,712 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Does intensive systolic blood pressure lowering to below 120 mmHg reduce major adverse cardiovascular events compared with standard blood pressure targets in adults at elevated cardiovascular risk? Three randomized controlled trials enrolling 22,712 patients with elevated cardiovascular risk compared intensive blood pressure targets against standard targets over median follow-up of 2 to 5 years. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the cardiovascular composite was 0.81 (95% CI 0.72-0.92), with no detectable heterogeneity (I-squared 0%). Mortality reduction was concordant in SPRINT and ESPRIT but not in STEP, while heart failure hospitalisation reduction was robust across trials. Intensive blood pressure lowering reduces cardiovascular events by 19 percent across diverse high-risk populations. Acute kidney injury, syncope, and electrolyte disturbances are more common with intensive targets, automated office BP measurement is essential to replicate trial conditions, and absolute benefit in low-risk patients is small.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33368-33441 in rewrite-workbook.txt_

---

## Entry 445 ([442/921]) — IncretinHFpEFLivingMA

<details><summary>Metadata</summary>

```
TITLE: Incretin Therapies in HFpEF: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 3 RCTs (STEP-HFpEF, STEP-HFpEF DM, SUMMIT), 1,648 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Do incretin-based therapies (semaglutide, tirzepatide) reduce cardiovascular events in patients with heart failure with preserved ejection fraction and obesity, with or without diabetes? Three randomized placebo-controlled trials enrolling 1,648 patients with HFpEF and obesity compared semaglutide 2.4 mg or tirzepatide 15 mg weekly against placebo over 52 weeks. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for the cardiovascular composite was 0.41 (95% CI 0.19-0.89), with moderate heterogeneity (I-squared 55%) reflecting different agents and event accrual. Symptomatic and functional improvements were robust across trials, while hard cardiovascular event reduction was driven by SUMMIT in tirzepatide-treated patients. Incretin therapies reduce cardiovascular events in obesity-related HFpEF, expanding pharmacologic options beyond SGLT2 inhibitors. Weight loss versus direct cardiac mechanism remains debated, generalizability to non-obese HFpEF is limited, and long-term safety beyond one year requires monitoring.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33442-33515 in rewrite-workbook.txt_

---

## Entry 446 ([443/921]) — DOACCancerVTELivingMA

<details><summary>Metadata</summary>

```
TITLE: DOACs vs LMWH for Cancer-Associated VTE: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for VTE recurrence
DATA: 4 RCTs (HOKUSAI VTE-Cancer, SELECT-D, ADAM VTE, CARAVAGGIO), 2,894 patients
PATH: C:\Projects\Finrenone
```

</details>

### Original (frozen — do not edit)

```
Do direct oral anticoagulants (edoxaban, rivaroxaban, apixaban) provide non-inferior efficacy compared with low-molecular-weight heparin for treatment of cancer-associated venous thromboembolism? Four randomized controlled trials enrolling 2,894 patients with active cancer and acute VTE compared DOACs against dalteparin over 3 to 12 months. DerSimonian-Laird random-effects meta-analysis pooled hazard ratios on the log scale with HKSJ correction. The pooled hazard ratio for VTE recurrence was 0.60 (95% CI 0.36-1.00), with moderate heterogeneity (I-squared 63%) reflecting different cancer subtypes and DOAC agents. Apixaban (CARAVAGGIO) and rivaroxaban (SELECT-D) showed the most favourable efficacy-to-bleeding ratios, while edoxaban and gastrointestinal cancers required individualized risk assessment. DOACs are now first-line for most cancer-associated VTE except in luminal gastrointestinal malignancy. Bleeding risk in upper GI cancer remains higher with DOACs than LMWH, drug-drug interactions with anticancer therapies require monitoring, and apixaban has emerged as the preferred agent in many guidelines.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33516-33589 in rewrite-workbook.txt_

---

## Entry 447 ([444/921]) — HFrEFNMALivingMA

<details><summary>Metadata</summary>

```
TITLE: Foundational HFrEF Therapies: Living Network Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for CV death or HF hospitalization
DATA: 3 RCTs (DAPA-HF, EMPEROR-Reduced, PARADIGM-HF), 16,873 patients
PATH: C:\Projects\HFrEF_NMA_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Which foundational HFrEF therapy reduces cardiovascular events most when added to guideline-directed medical therapy? Three randomized placebo-controlled trials deployed in this living meta-analysis (DAPA-HF, EMPEROR-Reduced, PARADIGM-HF) enrolled 16,873 patients with heart failure and reduced ejection fraction and compared dapagliflozin, empagliflozin, or sacubitril-valsartan against standard therapy. Inverse-variance fixed-effect meta-analysis pooled hazard ratios on the log scale across the three deployed trials. The pooled hazard ratio for the primary cardiovascular composite was 0.78 (95% CI 0.73 to 0.83), with no detectable heterogeneity (Q 1.2 on two degrees of freedom, I-squared 0 percent). DAPA-HF (HR 0.74), EMPEROR-Reduced (HR 0.75), and PARADIGM-HF (HR 0.80) give consistent twenty to twenty-five percent relative risk reductions. Foundational HFrEF therapies reduce cardiovascular events by approximately twenty-two percent on top of background medical therapy. Network consistency between SGLT2 inhibitors and ARNIs is within sampling error; head-to-head trials would refine drug sequencing.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33590-33663 in rewrite-workbook.txt_

---

## Entry 448 ([445/921]) — EmpaMILivingMA

<details><summary>Metadata</summary>

```
TITLE: Empagliflozin Post-Myocardial Infarction: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: HR for HF hospitalization or death
DATA: 1 RCT (EMPACT-MI), 6,522 patients; single-trial state (EMMY pending extraction)
PATH: C:\Projects\Empa_MI_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does empagliflozin started early after acute myocardial infarction reduce heart failure hospitalisation or death in patients with preserved or reduced ejection fraction? One randomized placebo-controlled trial is currently deployed in this living meta-analysis: EMPACT-MI enrolled 6,522 patients with recent myocardial infarction within 14 days and compared empagliflozin 10 mg daily against placebo. Single-trial inverse-variance estimate used the original publication's Cox model hazard ratio and confidence interval. EMPACT-MI reported a hazard ratio of 0.90 (95% CI 0.76 to 1.06) for the primary composite of heart failure hospitalisation or death. The effect does not reach statistical significance and shows a smaller point estimate than that observed in chronic heart failure SGLT2 trials. Empagliflozin started post-myocardial infarction shows a directional but non-significant benefit in this single trial; the post-MI population differs from chronic HFrEF populations. EMMY and similar post-MI trials would update the pool; single-trial evidence remains preliminary.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33664-33737 in rewrite-workbook.txt_

---

## Entry 449 ([446/921]) — PFAAFLivingMA

<details><summary>Metadata</summary>

```
TITLE: Pulsed Field Ablation for Atrial Fibrillation: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for AF recurrence
DATA: 3 RCTs (ADVENT, CHAMPION, PULSED AF), 1,117 patients (analysis subset)
PATH: C:\Projects\PFA_AF_LivingMeta
```

</details>

### Original (frozen — do not edit)

```
Does pulsed field ablation provide non-inferior efficacy and superior safety compared with thermal ablation (radiofrequency or cryoballoon) for paroxysmal or persistent atrial fibrillation? Three randomized or single-arm pivotal trials deployed in this living meta-analysis (ADVENT, CHAMPION, PULSED AF) enrolled 1,117 patients in the analysis subset comparing pulsed field ablation against thermal ablation. DerSimonian-Laird random-effects meta-analysis pooled odds ratios on the log scale for atrial arrhythmia freedom. The pooled odds ratio at 12 months was 1.16 (95% CI 0.78 to 1.72), with moderate heterogeneity (I-squared 47 percent) reflecting different patient populations and ablation systems. Non-inferiority for efficacy was achieved across all trials with markedly reduced phrenic nerve palsy and esophageal lesion rates compared with thermal ablation. Pulsed field ablation matches thermal ablation efficacy with superior tissue specificity and safety profile. Long-term durability beyond 12 months is being characterized, persistent AF data are limited, and operator learning curve effects on outcomes require ongoing monitoring.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33738-33811 in rewrite-workbook.txt_

---

## Entry 450 ([447/921]) — WatchmanAmuletLivingMA

<details><summary>Metadata</summary>

```
TITLE: Watchman vs Amulet LAAO Devices: Living Meta-Analysis
TYPE: living-ma  |  ESTIMAND: OR for stroke or systemic embolism
DATA: 2 RCTs (AMULET IDE, SWISS-APERO 3yr), 2,099 patients
PATH: C:\Projects\LivingMeta_Watchman_Amulet
```

</details>

### Original (frozen — do not edit)

```
Does the Amplatzer Amulet provide superior or non-inferior efficacy and safety compared with the Watchman device for left atrial appendage occlusion in patients with non-valvular atrial fibrillation and contraindication to oral anticoagulation? Two randomized controlled trials enrolling 2,099 patients with non-valvular AF and OAC contraindication compared Amulet against Watchman 2.5 or Watchman FLX. DerSimonian-Laird random-effects meta-analysis pooled odds ratios on the log scale with HKSJ correction. The pooled odds ratio for ischemic stroke or systemic embolism was 0.72 (95% CI 0.35-1.45), with moderate heterogeneity (I-squared 65%) reflecting different comparator generations (W2.5 vs FLX). Both trials demonstrated non-inferior efficacy with Amulet showing advantages in peridevice leak rates and device-related thrombus. Amulet matches Watchman efficacy with potential advantages in seal completeness. Comparison against the newer Watchman FLX is incomplete, long-term durability beyond 5 years is being characterized, and procedural complications vary substantially with operator experience.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 33812-33885 in rewrite-workbook.txt_

---

