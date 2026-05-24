# Rewrite chunk 012 — entries 551-600

_Previous: rewrite-PHONE-011.md | Next: rewrite-PHONE-013.md | Index: rewrite-PHONE-INDEX.md_

Edit ONLY the `YOUR REWRITE` section under each entry. The `Original`
block is frozen — do not edit it. Save the file when done. On your
laptop run `python C:\E156\merge-rewrite.py` to assemble a new
workbook (`rewrite-workbook.NEW.txt`) with your edits applied.

---

## Entry 551 ([560/921]) — outcome-switching-ma-hf

<details><summary>Metadata</summary>

```
TITLE: Outcome-Switching in Heart-Failure Phase 3 Trials: CT.gov v2 API Misses 100% of Initial-vs-Current Primary-Outcome Drift
TYPE: methods  |  ESTIMAND: per-trial primary-outcome-drift rate between v1 and current registration
DATA: 22 pivotal post-2015 HF Phase 3 trials with results posted, n>=500 (FINEARTS-HF, DAPA-HF, EMPEROR-Reduced/Preserved, DELIVER, VICTORIA, VICTOR, GALACTIC-HF, SUMMIT, STEP-HFpEF, FINEARTS, PARADISE-MI, DAPA-MI, EMPACT-MI, EMPULSE, AFFIRM-AHF, HEART-FID, DIAMOND, TRANSFORM-HF, PARALLAX, PERSPECTIVE, OUTSTEP-HF, ENDEAVOR, DETERMINE-Preserved); CT.gov v2 API current view + Playwright Python scrape of ?tab=history&a=1
PATH: C:\Projects\Finrenone\outcome_switching
```

</details>

### Original (frozen — do not edit)

```
Does the CT.gov v2 API capture outcome-switching in pivotal heart-failure Phase 3 trials, or does scraping initial-registration history reveal more serious drift? We audited 22 pivotal post-2015 HF Phase 3 trials with results posted and n>=500, sourced from CT.gov on 2026-04-30. Two-comparator audit: v2 API current-vs-reported, and Playwright Python scrape of version 1 vs current registered for all 22. The v2 API alone detected 0/22 switching events; v1-vs-current detected 21/22 (95%) with drift, including 1/22 outcome-content change (DIAMOND, hard CV-event endpoint reframed as serum-potassium biomarker), 3/22 statistical-framework changes (PARADISE-MI, DAPA-HF, DELIVER, time-to-event reframed as cumulative-incidence), and 14/22 timeframe changes mixing 9 compressions and 5 extensions. The DIAMOND case study is the most serious drift: the primary outcome changed *what the trial measures*, invisible to the API. Small curated pivotal pool; published-manuscript pair deferred to v0.3.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 40947-41017 in rewrite-workbook.txt_

---

## Entry 552 ([561/921]) — ACORAMIDIS_ATTR_CM

<details><summary>Metadata</summary>

```
TITLE: Acoramidis — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Acoramidis trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41018-41084 in rewrite-workbook.txt_

---

## Entry 553 ([562/921]) — ACS_ANTIPLATELET_NMA

<details><summary>Metadata</summary>

```
TITLE: ACS Antiplatelet NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do ACS Antiplatelet NMA trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41085-41151 in rewrite-workbook.txt_

---

## Entry 554 ([563/921]) — ADC_HER2_ADJUVANT_NMA

<details><summary>Metadata</summary>

```
TITLE: ADC NMA in HER2+ Early Breast Cancer Adjuvant — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do ADC NMA in HER2+ Early Breast Cancer Adjuvant trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41152-41218 in rewrite-workbook.txt_

---

## Entry 555 ([564/921]) — ADC_HER2_LOW_NMA

<details><summary>Metadata</summary>

```
TITLE: ADC NMA in HER2-Low Metastatic Breast Cancer — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do ADC NMA in HER2-Low Metastatic Breast Cancer trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41219-41285 in rewrite-workbook.txt_

---

## Entry 556 ([565/921]) — ADC_HER2_NMA

<details><summary>Metadata</summary>

```
TITLE: ADC NMA in HER2+ MBC 2L+ PFS — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do ADC NMA in HER2+ MBC 2L+ PFS trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41286-41352 in rewrite-workbook.txt_

---

## Entry 557 ([566/921]) — AFICAMTEN_HCM

<details><summary>Metadata</summary>

```
TITLE: Aficamten — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: HR for stroke or systemic embolism
DATA: RapidMeta cardiology / electrophysiology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Aficamten trials support a clinically meaningful effect on the registered HR for stroke or systemic embolism? The RapidMeta cardiology / electrophysiology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41353-41419 in rewrite-workbook.txt_

---

## Entry 558 ([567/921]) — ALDO_SYNTHASE_NMA

<details><summary>Metadata</summary>

```
TITLE: Aldosterone Synthase Inhibitors in Resistant Hypertension NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Aldosterone Synthase Inhibitors in Resistant Hypertension NMA trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41420-41486 in rewrite-workbook.txt_

---

## Entry 559 ([568/921]) — ALOPECIA_JAKI_NMA

<details><summary>Metadata</summary>

```
TITLE: JAK Inhibitors in Severe Alopecia Areata — NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: HR for vertebral fracture
DATA: RapidMeta endocrinology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do JAK Inhibitors in Severe Alopecia Areata — NMA trials support a clinically meaningful effect on the registered HR for vertebral fracture? The RapidMeta endocrinology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41487-41553 in rewrite-workbook.txt_

---

## Entry 560 ([569/921]) — ANTIAMYLOID_AD_NMA

<details><summary>Metadata</summary>

```
TITLE: Anti-Amyloid mAbs NMA in Early Alzheimer Disease — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Anti-Amyloid mAbs NMA in Early Alzheimer Disease trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41554-41620 in rewrite-workbook.txt_

---

## Entry 561 ([570/921]) — ANTIPSYCHOTICS_SCHIZO_NMA

<details><summary>Metadata</summary>

```
TITLE: Antipsychotic Pivotal-Trial Summary NMA in Acute Schizophrenia — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Antipsychotic Pivotal-Trial Summary NMA in Acute Schizophrenia trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41621-41687 in rewrite-workbook.txt_

---

## Entry 562 ([571/921]) — ANTIVEGF_NAMD_NMA

<details><summary>Metadata</summary>

```
TITLE: Anti-VEGF Class NMA in Neovascular AMD — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: MD in ETDRS letters gained
DATA: RapidMeta ophthalmology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Anti-VEGF Class NMA in Neovascular AMD trials support a clinically meaningful effect on the registered MD in ETDRS letters gained? The RapidMeta ophthalmology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41688-41754 in rewrite-workbook.txt_

---

## Entry 563 ([572/921]) — ANTI_CD20_MS_NMA

<details><summary>Metadata</summary>

```
TITLE: Anti-CD20 Therapies in Relapsing MS — NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: HR for disability progression
DATA: RapidMeta neurology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Anti-CD20 Therapies in Relapsing MS — NMA trials support a clinically meaningful effect on the registered HR for disability progression? The RapidMeta neurology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41755-41821 in rewrite-workbook.txt_

---

## Entry 564 ([573/921]) — ATOPIC_DERM_NMA

<details><summary>Metadata</summary>

```
TITLE: Atopic Dermatitis Biologics + JAKi NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: HR for vertebral fracture
DATA: RapidMeta endocrinology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Atopic Dermatitis Biologics + JAKi NMA trials support a clinically meaningful effect on the registered HR for vertebral fracture? The RapidMeta endocrinology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41822-41888 in rewrite-workbook.txt_

---

## Entry 565 ([574/921]) — AVACINCAPTAD_GA

<details><summary>Metadata</summary>

```
TITLE: Avacincaptad Pegol — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Avacincaptad Pegol trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41889-41955 in rewrite-workbook.txt_

---

## Entry 566 ([575/921]) — AZITHROMYCIN_CHILD_MORTALITY

<details><summary>Metadata</summary>

```
TITLE: Mass Azithromycin for Under-5 Mortality in Sub-Saharan Africa — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Mass Azithromycin trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 41956-42022 in rewrite-workbook.txt_

---

## Entry 567 ([576/921]) — BIMEKIZUMAB_PSORIASIS

<details><summary>Metadata</summary>

```
TITLE: Bimekizumab — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for PASI-90 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Bimekizumab trials support a clinically meaningful effect on the registered OR for PASI-90 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42023-42089 in rewrite-workbook.txt_

---

## Entry 568 ([577/921]) — BPAL_MDRTB

<details><summary>Metadata</summary>

```
TITLE: BPaL / BPaLM Short Regimens for MDR / XDR Tuberculosis — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do BPaL / BPaLM Short Regimens trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42090-42156 in rewrite-workbook.txt_

---

## Entry 569 ([578/921]) — CAPIVASERTIB_BC

<details><summary>Metadata</summary>

```
TITLE: Capivasertib + Fulvestrant in HR+/HER2- Advanced Breast Cancer — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Capivasertib + Fulvestrant in HR+/HER2- Advanced Breast Cancer trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42157-42223 in rewrite-workbook.txt_

---

## Entry 570 ([579/921]) — CARDIORENAL_DKD_NMA

<details><summary>Metadata</summary>

```
TITLE: Modern Cardiorenal Therapies in CKD — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Modern Cardiorenal Therapies in CKD trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42224-42290 in rewrite-workbook.txt_

---

## Entry 571 ([580/921]) — CD_BIOLOGICS_NMA

<details><summary>Metadata</summary>

```
TITLE: Crohn's Disease Biologics Induction-Remission NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for clinical remission
DATA: RapidMeta gastroenterology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Crohn's Disease Biologics Induction-Remission NMA trials support a clinically meaningful effect on the registered OR for clinical remission? The RapidMeta gastroenterology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42291-42357 in rewrite-workbook.txt_

---

## Entry 572 ([581/921]) — CGRP_MIGRAINE_NMA

<details><summary>Metadata</summary>

```
TITLE: CGRP mAb Class NMA for Episodic Migraine Prevention — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: MD in monthly migraine days
DATA: RapidMeta neurology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do CGRP mAb Class NMA trials support a clinically meaningful effect on the registered MD in monthly migraine days? The RapidMeta neurology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42358-42424 in rewrite-workbook.txt_

---

## Entry 573 ([582/921]) — COVID_ANTIGEN_DTA

<details><summary>Metadata</summary>

```
TITLE: SARS-CoV-2 Rapid Antigen Tests for COVID-19 &mdash; DTA Living Review — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 0 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do SARS-CoV-2 Rapid Antigen Tests trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 0 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42425-42491 in rewrite-workbook.txt_

---

## Entry 574 ([583/921]) — DDIMER_PE_DTA

<details><summary>Metadata</summary>

```
TITLE: D-dimer for Pulmonary Embolism Rule-out &mdash; DTA Living Review — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 0 trials · 13000 participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do D-dimer trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 0 randomized trials with 13000 participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42492-42558 in rewrite-workbook.txt_

---

## Entry 575 ([584/921]) — DELANDISTROGENE_DMD

<details><summary>Metadata</summary>

```
TITLE: Delandistrogene Moxeparvovec Gene Therapy for Duchenne Muscular Dystrophy — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Delandistrogene Moxeparvovec Gene Therapy trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42559-42625 in rewrite-workbook.txt_

---

## Entry 576 ([585/921]) — DOAC_AF_NMA

<details><summary>Metadata</summary>

```
TITLE: DOAC Class NMA vs Warfarin for Stroke Prevention in AF — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: HR for stroke or systemic embolism
DATA: RapidMeta cardiology / electrophysiology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do DOAC Class NMA vs Warfarin trials support a clinically meaningful effect on the registered HR for stroke or systemic embolism? The RapidMeta cardiology / electrophysiology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42626-42692 in rewrite-workbook.txt_

---

## Entry 577 ([586/921]) — DOAC_VTE_NMA

<details><summary>Metadata</summary>

```
TITLE: DOAC Class NMA vs Warfarin for Acute VTE Treatment — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do DOAC Class NMA vs Warfarin trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42693-42759 in rewrite-workbook.txt_

---

## Entry 578 ([587/921]) — DOLUTEGRAVIR_ART_SSA

<details><summary>Metadata</summary>

```
TITLE: Dolutegravir First-Line ART in Sub-Saharan Africa — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Dolutegravir First-Line ART in Sub-Saharan Africa trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42760-42826 in rewrite-workbook.txt_

---

## Entry 579 ([588/921]) — DONANEMAB_AD_SOLO

<details><summary>Metadata</summary>

```
TITLE: Donanemab — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Donanemab trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42827-42893 in rewrite-workbook.txt_

---

## Entry 580 ([589/921]) — EFGARTIGIMOD_MG

<details><summary>Metadata</summary>

```
TITLE: Efgartigimod for Generalized Myasthenia Gravis — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Efgartigimod trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42894-42960 in rewrite-workbook.txt_

---

## Entry 581 ([590/921]) — ELACESTRANT_BC

<details><summary>Metadata</summary>

```
TITLE: Elacestrant in ESR1-Mutated HR+/HER2- Advanced Breast Cancer — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Elacestrant in ESR1-Mutated HR+/HER2- Advanced Breast Cancer trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 42961-43027 in rewrite-workbook.txt_

---

## Entry 582 ([591/921]) — ENSIFENTRINE_COPD

<details><summary>Metadata</summary>

```
TITLE: Ensifentrine for COPD — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: HR for moderate/severe exacerbations
DATA: RapidMeta respiratory medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Ensifentrine trials support a clinically meaningful effect on the registered HR for moderate/severe exacerbations? The RapidMeta respiratory medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43028-43094 in rewrite-workbook.txt_

---

## Entry 583 ([592/921]) — ETRASIMOD_UC

<details><summary>Metadata</summary>

```
TITLE: Etrasimod — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Etrasimod trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43095-43161 in rewrite-workbook.txt_

---

## Entry 584 ([593/921]) — FRAGILITY_FRACTURE_NMA

<details><summary>Metadata</summary>

```
TITLE: Fragility Fracture Pharmacotherapy NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Fragility Fracture Pharmacotherapy NMA trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43162-43228 in rewrite-workbook.txt_

---

## Entry 585 ([594/921]) — GENEXPERT_ULTRA_TB_DTA

<details><summary>Metadata</summary>

```
TITLE: GeneXpert MTB/RIF Ultra for Pulmonary TB &mdash; DTA Living Review — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · 5 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do GeneXpert MTB/RIF Ultra trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates 5 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43229-43295 in rewrite-workbook.txt_

---

## Entry 586 ([595/921]) — GLP1_CVOT_NMA

<details><summary>Metadata</summary>

```
TITLE: GLP-1 RA Class NMA for MACE in T2D CV-Outcomes — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do GLP-1 RA Class NMA trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43296-43362 in rewrite-workbook.txt_

---

## Entry 587 ([596/921]) — GLP1_MASH_NMA

<details><summary>Metadata</summary>

```
TITLE: Incretin Therapies in MASH/NASH — NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Incretin Therapies in MASH/NASH — NMA trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43363-43429 in rewrite-workbook.txt_

---

## Entry 588 ([597/921]) — HCC_1L_NMA

<details><summary>Metadata</summary>

```
TITLE: First-Line Hepatocellular Carcinoma — IO Combination NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do First-Line Hepatocellular Carcinoma — IO Combination NMA trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43430-43496 in rewrite-workbook.txt_

---

## Entry 589 ([598/921]) — HER2_LOW_ADC_NMA

<details><summary>Metadata</summary>

```
TITLE: HER2-Low Metastatic BC ADCs — NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do HER2-Low Metastatic BC ADCs — NMA trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43497-43563 in rewrite-workbook.txt_

---

## Entry 590 ([599/921]) — HF_QUADRUPLE_NMA

<details><summary>Metadata</summary>

```
TITLE: HF Quadruple Therapy NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do HF Quadruple Therapy NMA trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43564-43630 in rewrite-workbook.txt_

---

## Entry 591 ([600/921]) — HIV_LA_PREP_NMA

<details><summary>Metadata</summary>

```
TITLE: Long-Acting Injectable PrEP NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: IRR for HIV incidence
DATA: RapidMeta infectious disease review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Long-Acting Injectable PrEP NMA trials support a clinically meaningful effect on the registered IRR for HIV incidence? The RapidMeta infectious disease living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43631-43697 in rewrite-workbook.txt_

---

## Entry 592 ([601/921]) — HSCTN_NSTEMI_DTA

<details><summary>Metadata</summary>

```
TITLE: hs-cTn 0/1h for NSTEMI Rule-Out &mdash; DTA Living Review — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 5 trials · 6500 participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do hs-cTn 0/1h trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 5 randomized trials with 6500 participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43698-43764 in rewrite-workbook.txt_

---

## Entry 593 ([602/921]) — IL_PSORIASIS_NMA

<details><summary>Metadata</summary>

```
TITLE: IL-17 / IL-23 Biologics NMA in Plaque Psoriasis — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for PASI-90 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do IL-17 / IL-23 Biologics NMA in Plaque Psoriasis trials support a clinically meaningful effect on the registered OR for PASI-90 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43765-43831 in rewrite-workbook.txt_

---

## Entry 594 ([603/921]) — INAVOLISIB_BC

<details><summary>Metadata</summary>

```
TITLE: Inavolisib + Palbociclib + Fulvestrant in PIK3CA-Mutated HR+/HER2- Advanced BC — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · None trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Inavolisib + Palbociclib + Fulvestrant in PIK3CA-Mutated HR+/HER2- Advanced BC trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates all eligible phase 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43832-43898 in rewrite-workbook.txt_

---

## Entry 595 ([604/921]) — INCRETINS_T2D_NMA

<details><summary>Metadata</summary>

```
TITLE: Incretin Class NMA in Type 2 Diabetes — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: effect estimate with 95% CI
DATA: RapidMeta clinical medicine review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Incretin Class NMA in Type 2 Diabetes trials support a clinically meaningful effect on the registered effect estimate with 95% CI? The RapidMeta clinical medicine living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43899-43965 in rewrite-workbook.txt_

---

## Entry 596 ([605/921]) — IPTACOPAN_IGAN

<details><summary>Metadata</summary>

```
TITLE: Iptacopan — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: HR for vertebral fracture
DATA: RapidMeta endocrinology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Iptacopan trials support a clinically meaningful effect on the registered HR for vertebral fracture? The RapidMeta endocrinology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 43966-44032 in rewrite-workbook.txt_

---

## Entry 597 ([606/921]) — JAKI_AD_NMA

<details><summary>Metadata</summary>

```
TITLE: Oral JAK Inhibitors NMA in Moderate-Severe Atopic Dermatitis — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Oral JAK Inhibitors NMA in Moderate-Severe Atopic Dermatitis trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 44033-44099 in rewrite-workbook.txt_

---

## Entry 598 ([607/921]) — JAKI_RA_NMA

<details><summary>Metadata</summary>

```
TITLE: JAK Inhibitors NMA in MTX-IR RA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do JAK Inhibitors NMA in MTX-IR RA trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 44100-44166 in rewrite-workbook.txt_

---

## Entry 599 ([608/921]) — KRAS_G12C_NMA

<details><summary>Metadata</summary>

```
TITLE: KRAS G12C Inhibitors in Pretreated KRAS-G12C-Mutated Advanced NSCLC NMA — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for ACR20 response
DATA: RapidMeta rheumatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do KRAS G12C Inhibitors in Pretreated KRAS-G12C-Mutated Advanced NSCLC NMA trials support a clinically meaningful effect on the registered OR for ACR20 response? The RapidMeta rheumatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 44167-44233 in rewrite-workbook.txt_

---

## Entry 600 ([609/921]) — LEBRIKIZUMAB_AD

<details><summary>Metadata</summary>

```
TITLE: Lebrikizumab — Living Meta-Analysis (RapidMeta)
TYPE: living-ma  |  ESTIMAND: OR for EASI-75 response
DATA: RapidMeta dermatology review · 3 trials · None participants
PATH: (browser-native — see Code URL; no local path)
```

</details>

### Original (frozen — do not edit)

```
Do Lebrikizumab trials support a clinically meaningful effect on the registered OR for EASI-75 response? The RapidMeta dermatology living review aggregates 3 randomized trials with n participants in a browser-native, audit-trailed pipeline. Random-effects pooling on the log scale used the Hartung-Knapp-Sidik-Jonkman adjustment with back-transformation to the reported scale. The pooled estimate was the pooled estimate reported on the live dashboard, held in a continuously updated dashboard with prediction interval and sensitivity re-runs on demand. Between-study heterogeneity was quantified as I² with a prediction interval reported alongside the 95% CI. Results are written to a reproducibility capsule with a machine-readable config, an interactive reader, and a Vancouver reference pack so reviewers receive a self-contained submission. The dashboard does not establish individual-patient causality and cannot replace adjudicated trial-level review of risk of bias, outcome switching, or incomplete subgroup reporting.
```

### YOUR REWRITE

<!-- BEGIN-REWRITE -->
<!-- END-REWRITE -->

_Line range 44234-44300 in rewrite-workbook.txt_

---

