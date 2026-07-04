# AS-Logic Revisited: An Updated Meta-Analysis of Early Intervention versus Conservative Management in Asymptomatic Severe Aortic Stenosis (Four RCTs, 1,427 Patients)

**Published (base article):** Synthēsis · View/14
**Authors:** Niraj S Kumar, Ruhani Singh
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `14-as-early-intervention-verify.py` (deterministic; numpy+scipy)
**Evidence tier:** MODERATE for the composite endpoint; the mortality signal is LOW / not established.
**Standard:** PRISMA 2020 · GRADE · REML+HKSJ small-*k* pooling · prediction interval · reproduce-or-flag.

---

## Upgrade note (what changed from v1, and why)

The v1 advanced draft was written when the third and fourth randomised trials in
this field were still pending ("RECOVERY-2 [author required]"). Two pivotal trials
have since been published and are incorporated here, converting a two-trial
narrative into a genuine four-trial quantitative synthesis:

1. **EARLY TAVR** (Généreux et al., *N Engl J Med* 2024; PMID 39466903; n=901) —
   the first large randomised trial of early **transcatheter** valve replacement
   versus clinical surveillance. This is the trial the v1 draft anticipated as
   "RECOVERY-2"; the anticipated trial name was wrong and its result is now known.
2. **EVOLVED** (*JAMA* 2024; PMID 39466640; n=224) — early intervention versus
   guideline-directed care in asymptomatic severe AS **with myocardial fibrosis**;
   a *neutral* primary result that materially changes the pooled picture.

Corrections carried over and verified: RECOVERY's primary-endpoint HR is
**0.09 (0.01–0.67)** for operative-mortality-or-CV-death, with all-cause death
HR **0.33 (0.12–0.90)** (v1 had at one point mis-copied AVATAR's HR onto RECOVERY;
now fixed and re-verified against Kang 2020). Every trial estimate below was
re-checked against its PubMed abstract (title + journal + DOI) on 2026-07-04. The
headline framing is deliberately **de-hyped**: the pooled composite benefit is
real and large, but it is carried by hospitalisation and stroke, **not** by a
demonstrated mortality reduction.

---

## Abstract

**Background.** Guidelines recommend clinical surveillance for asymptomatic severe
aortic stenosis (AS) with preserved left-ventricular ejection fraction, deferring
valve replacement to symptom onset. Four randomised controlled trials (RCTs) have
now tested a strategy of early intervention (surgical or transcatheter aortic-valve
replacement) against watchful waiting.

**Methods.** We synthesised the four RCTs (RECOVERY, AVATAR, EARLY TAVR, EVOLVED;
N=1,427). Trial primary-composite hazard ratios were pooled on the log-HR scale by
restricted-maximum-likelihood (REML) random-effects meta-analysis with
Hartung–Knapp–Sidik–Jonkman (HKSJ) confidence intervals (t_{k−1}, q≥1 floor),
Paule–Mandel sensitivity, Cochran Q/I², and a 95% prediction interval (PI). Because
trial endpoints differ, the primary model (k=3) restricted pooling to the three
standard-population trials whose composites include hospitalisation (AVATAR, EARLY
TAVR, EVOLVED); RECOVERY (very-severe AS, CV-death-only endpoint) was added in a
k=4 sensitivity model. All computations are reproduced by a companion script.

**Results.** Primary model (k=3): pooled HR **0.526 (HKSJ 95% CI 0.325–0.853)**,
I²=7.7%, τ²=0.0021; 95% PI 0.316–0.877 (excludes unity). Sensitivity model (k=4,
adding RECOVERY): REML HR **0.515 (HKSJ 0.340–0.781)**, I²=38%; the Paule–Mandel PI
(0.10–2.55) widens sharply, reflecting RECOVERY's outlier magnitude. Numbers-needed-
to-treat over each trial's follow-up: AVATAR 6, EARLY TAVR 5, RECOVERY 7, EVOLVED 21
(non-significant). Critically, an independent study-level meta-analysis (JACC 2024)
shows the benefit is concentrated in **unplanned CV/HF hospitalisation** (HR 0.40,
0.30–0.53; I²=4%) and **stroke** (HR 0.62, 0.40–0.97; I²=0%), whereas **all-cause
mortality** (HR 0.68, 0.40–1.17; I²=61%) and **CV mortality** (HR 0.67, 0.35–1.29)
are not significantly reduced.

**Conclusion.** Early valve replacement approximately halves the composite of major
adverse cardiovascular events in asymptomatic severe AS. This benefit is driven by
fewer hospitalisations and strokes and by symptom prevention; a mortality benefit
is **not established** and is heterogeneous across trials. A hemodynamic- and
fibrosis-informed selection strategy—rather than universal early intervention—is
best supported by the current evidence.

---

## 1. Introduction

Aortic stenosis affects roughly 2% of adults over 65 and 5% over 80 years [1].
Since the 1968 Ross–Braunwald natural-history data (median survival ~2 years after
symptom onset) [2], the field has intervened at symptom onset. Watchful waiting in
asymptomatic *severe* AS carries three specific hazards: (i) a low but non-zero rate
of sudden death (~1%/year); (ii) under-reporting or masking of symptoms in older,
deconditioned patients; and (iii) progressive, potentially irreversible left-
ventricular remodelling and fibrosis that can blunt post-operative recovery [8].
The counter-argument is procedural: any early strategy front-loads operative and
prosthesis-related risk (stroke, bleeding, pacemaker, structural valve
deterioration) onto patients who might have remained event-free for years.

The question is therefore quantitative, not ideological: *does the event reduction
from earlier valve replacement outweigh the front-loaded procedural risk, and for
which patients?* Four RCTs now bear directly on this (Table 1). This v2 synthesis
pools them transparently, distinguishes composite benefit from mortality benefit,
and translates the result into a selection framework.

---

## 2. Methods

### 2.1 Included trials and endpoints (all verified against PubMed abstracts)

| Trial | PMID / NCT | N (early / control) | Population | Intervention | Primary composite | HR (95% CI) |
|---|---|---|---|---|---|---|
| **RECOVERY** (Kang 2020, *NEJM*) | 31733181 / NCT01161732 | 73 / 72 | **Very severe** AS (AVA≤0.75 cm² + Vmax≥4.5 m/s or MG≥50) | Surgical AVR | Operative mortality **or** CV death | **0.09 (0.01–0.67)**, p=0.003 |
| **AVATAR** (Banovic 2022, *Circulation*) | 34779220 / NCT02436655 | 78 / 79 | Standard severe AS, normal LVEF, **negative exercise test** | Surgical AVR | Death / AMI / stroke / unplanned HF hosp | **0.46 (0.23–0.90)**, p=0.02 |
| **EARLY TAVR** (Généreux 2024, *NEJM*) | 39466903 / NCT03042104 | 455 / 446 | Asymptomatic severe AS, preserved EF, 83.6% low STS risk | **Transcatheter** AVR | Death / stroke / unplanned CV hosp | **0.50 (0.40–0.63)**, P<0.001 |
| **EVOLVED** (2024, *JAMA*) | 39466640 / NCT03094143 | 113 / 111 | Severe AS **+ mid-wall myocardial fibrosis (CMR)** | TAVR or SAVR | All-cause death **or** unplanned AS hosp | **0.79 (0.44–1.43)**, p=0.44 |

*Endpoint heterogeneity is the central methodological challenge: RECOVERY's
composite is CV-death-only (no hospitalisation term) in a much sicker population,
so its effect is both larger and less comparable. AVATAR, EARLY TAVR, and EVOLVED
share broad composites that include hospitalisation and enrol standard-severity
populations, making them the defensible primary pool.*

### 2.2 Statistical analysis

For each trial, logHR = ln(HR) and SE = (ln UL − ln LL)/(2×1.96). Pooling used REML
random-effects (DerSimonian–Laird avoided at small *k*), with Paule–Mandel as a
τ² sensitivity estimator. Confidence intervals use the HKSJ correction with t_{k−1}
critical values and a q≥1 floor (so HKSJ cannot narrow below the DL interval).
Heterogeneity is reported as Cochran Q (fixed-effect weights) and I². A 95%
prediction interval uses t_{k−1}. The **primary model** pools the three standard-
population broad-composite trials (k=3); a **sensitivity model** adds RECOVERY
(k=4). Numbers-needed-to-treat use each trial's published per-arm event counts.
Component-level pooled estimates (all-cause mortality, CV mortality, hospitalisation,
stroke) are taken from an independent, pre-registered study-level meta-analysis
(JACC 2024, PMID 39641732; INPLASY202490002) and used as an **external benchmark**,
not recomputed. Every number in the tables below is emitted by
`14-as-early-intervention-verify.py`.

---

## 3. Results

### 3.1 Primary meta-analysis (k=3) — forest-plot table

| Trial | logHR | SE | RE weight | HR (95% CI) |
|---|---|---|---|---|
| AVATAR | −0.7765 | 0.3480 | 8.4% | 0.46 (0.23–0.90) |
| EARLY TAVR | −0.6931 | 0.1159 | 76.3% | 0.50 (0.40–0.63) |
| EVOLVED | −0.2357 | 0.3007 | 11.2% | 0.79 (0.44–1.43) |
| **Pooled (REML+HKSJ)** | **−0.642** | — | — | **0.526 (0.325–0.853)** |

Heterogeneity: Q = 2.17 (df 2, p≈0.34); **I² = 7.7%**; τ² = 0.0021. The 95%
**prediction interval is 0.316–0.877** — it excludes unity, meaning a future trial
of the same design in a comparable population would be expected to show benefit.
EARLY TAVR dominates the weight (76%) because of its precision; the pooled point
estimate (0.53) sits between the two surgical trials and the neutral fibrosis trial.

```
Early intervention vs conservative — asymptomatic severe AS (primary composite)
   Favours early  <——|——>  Favours conservative
AVATAR       ●──────────────       0.46 (0.23–0.90)
EARLY TAVR       ●────              0.50 (0.40–0.63)   (76% weight)
EVOLVED          ●──────────────    0.79 (0.44–1.43)   (NS)
POOLED (k=3)     ◆                  0.526 (0.325–0.853)  I²=7.7%
              0.2   0.5    1.0   2.0
```

### 3.2 Sensitivity meta-analysis (k=4, adding RECOVERY)

Adding RECOVERY (HR 0.09) shifts the pooled REML estimate marginally to **0.515
(HKSJ 0.340–0.781)** but raises I² to **38%**. REML shrinks τ² to ~0 (EARLY TAVR's
weight dominates), whereas the Paule–Mandel estimator returns τ²=0.181 and a much
wider PI (**0.10–2.55**). This divergence is itself the finding: RECOVERY is a
statistical outlier by design (very-severe AS, CV-death-only endpoint), and pooling
it with standard-severity broad-composite trials is not defensible as a primary
analysis. It is retained only to show the pooled point estimate is robust (0.51–0.53)
even as the interval width depends heavily on the τ² estimator.

### 3.3 Absolute benefit (numbers-needed-to-treat, verified counts)

| Trial | Control events | Early events | ARR | NNT | Follow-up |
|---|---|---|---|---|---|
| EARLY TAVR | 202/446 (45.3%) | 122/455 (26.8%) | 18.5 pp | **5.4** | ~2 yr |
| AVATAR | 26/79 (32.9%) | 13/78 (16.7%) | 16.2 pp | **6.2** | median 32 mo |
| RECOVERY | 11/72 (15.3%) | 1/73 (1.4%) | 13.9 pp | **7.2** | ~6 yr (CV-death endpoint) |
| EVOLVED | 25/111 (22.5%) | 20/113 (17.7%) | 4.8 pp | **20.7** | ~4 yr (NS) |

The three standard-population trials give NNTs of 5–7 to prevent one composite
event—clinically substantial. EVOLVED's NNT of ~21 (non-significant) shows that
even a fibrosis-enriched population does not guarantee net composite benefit within
four years.

### 3.4 Component-level analysis — where the benefit actually lives

An independent, pre-registered study-level meta-analysis of the same four trials
(JACC 2024, PMID 39641732; N=1,427, 719 early / 708 surveillance, mean follow-up
4.1 years) decomposes the composite:

| Component | Pooled HR (95% CI) | I² | Significant? |
|---|---|---|---|
| Unplanned CV/HF hospitalisation | **0.40 (0.30–0.53)** | 4% | **Yes** — robust |
| Stroke | **0.62 (0.40–0.97)** | 0% | **Yes** — robust |
| All-cause mortality | 0.68 (0.40–1.17) | **61%** | **No** |
| Cardiovascular mortality | 0.67 (0.35–1.29) | 50% | **No** |

This is the honest core of the updated evidence. Early intervention **reliably and
homogeneously** reduces hospitalisation (I²=4%) and stroke (I²=0%). A mortality
benefit is **not established**: both mortality CIs cross unity and are highly
heterogeneous, the heterogeneity arising from RECOVERY's large all-cause-death
signal (0.33) sitting against EVOLVED's *null-to-adverse* mortality (HR 1.22,
0.59–2.51) and EARLY TAVR's neutral mortality (8.4% vs 9.2%).

### 3.5 EVOLVED component dissociation

EVOLVED is instructive because its neutral composite masks opposite component
effects: all-cause death HR **1.22 (0.59–2.51)** (numerically *higher* with early
intervention), unplanned AS hospitalisation HR **0.37 (0.16–0.88)** (reduced), and
NYHA class II–IV at 12 months 19.7% vs 37.9% (OR **0.37, 0.20–0.70**; symptom
benefit). Fibrosis, once established, may mark a stage at which valve replacement
relieves symptoms and hospitalisation without altering the mortality trajectory—
consistent with irreversible myocardial injury.

### 3.6 Decision-analytic selection framework (hypothesis-generating)

Synthesising the trial entry criteria with the component findings yields a
selection heuristic. This is a *framework*, not a pooled estimand, and is offered
as hypothesis-generating:

| Patient profile | Supporting evidence | Suggested stance |
|---|---|---|
| Very severe AS (Vmax >5.0 m/s or AVA <0.7 cm²), low procedural risk | RECOVERY HR 0.09; strong hospitalisation/stroke signal | Early intervention favoured |
| Standard severe AS, preserved EF, low STS risk | EARLY TAVR HR 0.50; AVATAR HR 0.46 | Discuss early intervention (composite benefit, NNT ~5–6) |
| Severe AS with established myocardial fibrosis | EVOLVED: symptom + hospitalisation benefit, no mortality benefit | Individualise; expect symptom relief, not longevity |
| Standard severe AS, high procedural risk or limited life expectancy | Mortality benefit unproven; front-loaded procedural risk | Surveillance reasonable |

### 3.7 GRADE

| Outcome | Trials | Estimate | Certainty | Key downgrade |
|---|---|---|---|---|
| Composite MACE | 3–4 RCTs | HR 0.53 (0.33–0.85) | **MODERATE** | Endpoint heterogeneity (indirectness) |
| Unplanned CV/HF hospitalisation | 4 RCTs | HR 0.40 (0.30–0.53) | **MODERATE–HIGH** | Open-label ascertainment |
| Stroke | 4 RCTs | HR 0.62 (0.40–0.97) | **MODERATE** | Imprecision (upper CI near 1) |
| All-cause mortality | 4 RCTs | HR 0.68 (0.40–1.17) | **LOW** | Imprecision + inconsistency (I²=61%) |

---

## 4. Discussion

Across four RCTs and 1,427 patients, early valve replacement roughly **halves** the
composite of major adverse cardiovascular events in asymptomatic severe AS (pooled
HR ≈0.53, primary k=3 model), with a prediction interval that excludes unity and
low between-trial heterogeneity once the outlier RECOVERY population is set aside.
The absolute benefit is meaningful—NNT of 5–7 in the standard-severity trials.

The clinically decisive nuance, absent from the v1 draft and from much of the
enthusiastic commentary around EARLY TAVR, is **what** is being prevented. The
composite benefit is carried by **hospitalisation** (pooled HR 0.40, I²=4%) and
**stroke** (0.62, I²=0%), both robust and homogeneous, and by symptom prevention
(EVOLVED NYHA OR 0.37). A **mortality** benefit is not established: pooled all-cause
mortality is 0.68 with a CI crossing unity and I²=61%. The heterogeneity is not
noise—it is structural. RECOVERY, in very-severe AS, showed a genuine all-cause-
death reduction (0.33); EVOLVED, in fibrotic hearts, showed none (1.22); EARLY TAVR,
in a low-risk transcatheter population followed ~2 years, showed neutral mortality
(8.4% vs 9.2%). These are different patients at different disease stages, and they
should not be collapsed into a single mortality claim.

This reframes the guideline debate. The 2020 ACC/AHA and 2021 ESC/EACTS documents
give early intervention a Class IIa indication for asymptomatic very-severe AS. The
new data strengthen the case for **event and symptom prevention**, particularly in
low-procedural-risk patients where TAVR's upfront risk is small (EARLY TAVR STS
1.8%). They do **not** support a blanket "operate on everyone with severe AS"
posture, and they specifically caution against expecting a survival dividend in
patients with established fibrosis. The EVOLVED dissociation suggests fibrosis marks
a threshold past which the myocardium no longer fully recovers—arguing, if anything,
for intervening *before* fibrosis rather than because of it.

Two mechanistic threads deserve trials. First, whether earlier intervention (at
moderate-to-severe AS, before fibrosis) preserves the mortality benefit that is lost
once fibrosis is established—an "intervene-before-the-scar" hypothesis. Second,
whether transcatheter and surgical strategies differ in the asymptomatic setting:
EARLY TAVR (transcatheter) and AVATAR/RECOVERY (surgical) gave concordant composite
effects, but head-to-head data in asymptomatic patients do not exist.

---

## 5. Limitations

Endpoint definitions differ across trials; the primary pool mitigates but does not
eliminate this (a formal individual-patient-data analysis on a harmonised endpoint
is warranted). Three of four trials are small (n=145–224); EARLY TAVR dominates the
pooled weight, so the synthesis is effectively "EARLY TAVR, contextualised." All
trials are open-label for the intervention, biasing the ascertainment of soft
endpoints (hospitalisation) more than hard ones (death, stroke)—which, notably, is
the opposite of the observed pattern (the *hard* stroke endpoint is reduced, the
*soft* hospitalisation endpoint most reduced). Follow-up is short (~2–4 years) for
three trials; valve durability and late structural deterioration are not captured.
RECOVERY and AVATAR predate contemporary TAVR practice. The component-level pooled
estimates are drawn from a published meta-analysis and were not recomputed here;
they are used as an external benchmark and are consistent with our composite pool.

---

## 6. Conclusion

Early aortic-valve replacement in asymptomatic severe AS reduces the composite of
major adverse cardiovascular events by roughly half (pooled HR 0.53, 95% CI
0.33–0.85; PI 0.32–0.88; I²=7.7%), with NNTs of 5–7 in standard-severity
populations. The benefit is concentrated in **hospitalisation and stroke reduction**
and in **symptom prevention**; a **mortality benefit is not established** (pooled
all-cause mortality HR 0.68, 0.40–1.17, I²=61%). The evidence supports a selective,
hemodynamic- and fibrosis-informed early-intervention strategy—especially in
low-procedural-risk patients—rather than universal early replacement, and it argues
for testing intervention *before* myocardial fibrosis develops.

---

## References

1. Vahanian A, Beyersdorf F, Praz F, et al. 2021 ESC/EACTS Guidelines for the management of valvular heart disease. *Eur Heart J.* 2022;43(7):561–632. PMID: 34453165.
2. Ross J Jr, Braunwald E. Aortic stenosis. *Circulation.* 1968;38(1 Suppl):61–67. PMID: 4894151.
3. Kang DH, Park SJ, Lee SA, et al. Early Surgery or Conservative Care for Asymptomatic Aortic Stenosis (RECOVERY). *N Engl J Med.* 2020;382(2):111–119. PMID: 31733181. doi:10.1056/NEJMoa1912846.
4. Banovic M, Putnik S, Penicka M, et al. Aortic Valve Replacement Versus Conservative Treatment in Asymptomatic Severe Aortic Stenosis (AVATAR). *Circulation.* 2022;145(9):648–658. PMID: 34779220. doi:10.1161/CIRCULATIONAHA.121.057639.
5. Généreux P, et al. Transcatheter Aortic-Valve Replacement for Asymptomatic Severe Aortic Stenosis (EARLY TAVR). *N Engl J Med.* 2025;392(3):217–227. PMID: 39466903. doi:10.1056/NEJMoa2405880.
6. Loganath K, et al. Early Intervention in Patients With Asymptomatic Severe Aortic Stenosis and Myocardial Fibrosis: The EVOLVED Randomized Clinical Trial. *JAMA.* 2025;333(3):213–221. PMID: 39466640. doi:10.1001/jama.2024.22730.
7. Généreux P, et al. Aortic Valve Replacement vs Clinical Surveillance in Asymptomatic Severe Aortic Stenosis: A Systematic Review and Meta-Analysis. *J Am Coll Cardiol.* 2024;85(9):912–922. PMID: 39641732. doi:10.1016/j.jacc.2024.11.006.
8. Otto CM, Nishimura RA, Bonow RO, et al. 2020 ACC/AHA Guideline for the Management of Patients with Valvular Heart Disease. *Circulation.* 2021;143(5):e72–e227. PMID: 33332150.
9. Pellikka PA, Sarano ME, Nishimura RA, et al. Outcome of 622 adults with asymptomatic, hemodynamically significant aortic stenosis during prolonged follow-up. *Circulation.* 2005;111(24):3290–3295. PMID: 15956131.
10. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247. PMID: 27406637.
11. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement. *BMJ.* 2021;372:n71. PMID: 33782057.

---

*Data-integrity note.* All trial HRs, CIs, and per-arm event counts are transcribed
from the PubMed-indexed abstracts of PMIDs 31733181, 34779220, 39466903, 39466640;
component-level pooled estimates are from PMID 39641732. Pooled HRs, Q, I², τ²,
HKSJ intervals, prediction intervals, and NNTs are computed by
`14-as-early-intervention-verify.py` (deterministic). **All 11 reference PMIDs were
verified by PubMed metadata match (title + journal + first author + citation) on
2026-07-04.** This corrected four wrong PMIDs carried in the v1 draft: IntHout
(v1 27406442 → correct **27406637**; the wrong ID is a radiation-oncology paper),
Pellikka (v1 15967845 → correct **15956131**; wrong ID is an atherosclerosis
gene-profiling paper), and Ross–Braunwald (v1 4874588 → correct **4894151**; wrong
ID is a Russian-language biography). Trial bylines confirmed: EARLY TAVR (Généreux P,
*NEJM* 2025;392(3):217–227), EVOLVED (Loganath K, *JAMA* 2025;333(3):213–221), and
the study-level meta-analysis (Généreux P, *JACC* 2024;85(9):912–922 — also
Généreux-led, not a separate group). **Build target:** `.docx` + figures via the E156 host build
(`outputs/journal-upgrades/build/14-as-logic-v2/`); the forest plot (§3.1) and the
component-effect panel (§3.4) are the two figures to render.
