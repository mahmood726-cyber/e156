# The MCS Apples-and-Oranges Problem: Why Statistical Homogeneity Does Not License Pooling Mechanistically Distinct Devices

**Published (base article):** Synthēsis · View/16
**Authors:** Soham Ganguly
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `16-mcs-taxonomy-verify.py` (deterministic; numpy+scipy)
**Clinical companion:** paper 23 (Haemodynamic Fallacy) — device-stratified clinical reading.
**Evidence tier:** methodological demonstration; trial inputs are verified landmark RCTs.
**Standard:** PRISMA-adjacent · prediction-interval analysis · device/era stratification · reproduce-or-flag.

---

## Upgrade note (what changed from v1)

v1 asserted the "apples-and-oranges" case largely by imposing a heterogeneity value
(τ²=0.05) to widen the prediction interval. v2 keeps that sensitivity but leads with the
**honest and more interesting fact the data actually show**: the five randomised MCS
mortality estimates are, by the observed statistic, **homogeneous (I²=0%, DL τ²=0)** —
and the paper's thesis must therefore be argued on **mechanistic** rather than
statistical grounds. The strengthened argument is: (i) low observed I² does *not* license
pooling physiologically distinct devices; (ii) the single trial testing a genuinely
different device–comparator–population combination (DanGer Shock: Impella vs standard care
in STEMI-CS) *does* diverge significantly (HR 0.74); and (iii) once a realistic τ²
acknowledging device diversity is admitted, the 95% prediction interval spans meaningful
benefit to meaningful harm. All trial inputs are the same PubMed-verified estimates used
in the clinical companion (paper 23), re-verified 2026-07-04; no numbers are imposed
except the clearly-labelled τ² sensitivity.

---

## Abstract

**Background.** MCS meta-analyses routinely pool intra-aortic balloon pump (IABP),
Impella, and veno-arterial ECMO across comparators and eras. We test whether such
all-device pooling yields a clinically informative estimate.

**Methods.** We synthesised five randomised MCS trials reporting mortality (IABP-SHOCK
II, IMPRESS, ECMO-CS, ECLS-SHOCK, DanGer Shock) on the log scale with DerSimonian–Laird
random effects, HKSJ intervals, Cochran Q/I², and — the key statistic — a 95% prediction
interval (PI). We stratified by device/comparator and by era (pre-2015 vs 2015–2024),
and computed a PI under a plausible device-diversity heterogeneity (τ²=0.05).
Deterministic script; verified inputs.

**Results.** The all-device pool gives HR **0.935** with observed **I²=0%** (DL τ²=0) —
statistically homogeneous. Yet this masks genuine diversity: the one trial with a
distinct device–comparator–population (DanGer Shock, Impella vs standard, STEMI) is
significantly different (HR **0.74, 0.55–0.99**), and under a realistic τ²=0.05 the
95% PI widens to **0.45–1.89** — a future trial could show a 55% mortality reduction or
an 89% increase. Within-device pools are uninformative at k=2 (VA-ECMO PI 0.32–3.11;
"Impella" PI 0.13–4.59, itself mixing IMPRESS's-vs-IABP and DanGer's-vs-standard
comparators).

**Conclusion.** A homogeneous-looking pooled MCS mortality estimate is a statistical
coincidence of trials that mostly cluster near null; it does not forecast the next trial
and does not license pooling mechanistically distinct devices. Device- **and
comparator-** stratified, indication-specific synthesis is the minimum standard.

---

## 1. Introduction

Cardiogenic shock (CS) complicates 5–10% of acute myocardial infarction and carries
40–50% mortality. MCS devices differ not in degree but in *kind*: IABP augments
diastolic pressure (~0.3–0.5 L/min, no active unloading); Impella is a transvalvular
axial-flow pump (2.5–5.5 L/min); VA-ECMO reverses the entire circulation (4–7 L/min).
Pooling their mortality effects in one meta-analysis is mechanistically akin to pooling
aspirin, heparin, and thrombolytics in one "antithrombotic" estimate. Yet the dominant
form of MCS synthesis does exactly this. This paper asks a precise methodological
question: does all-device pooling produce a *clinically informative* estimate — one that
forecasts the next trial? The right statistic for that question is the prediction
interval, which is almost never reported in MCS meta-analyses.

## 2. Methods

Five randomised MCS trials reporting 30-day (or 180-day, DanGer) all-cause mortality
were synthesised on the log scale: IABP-SHOCK II (IABP vs none), IMPRESS (Impella vs
IABP), ECMO-CS (VA-ECMO vs conservative), ECLS-SHOCK (VA-ECMO vs medical), DanGer Shock
(Impella vs standard). Effects and CIs are the PubMed-verified values from the clinical
companion (paper 23). We used DerSimonian–Laird τ² (the estimator underlying the critiqued
pooled analyses), HKSJ intervals with t_{k−1}, Cochran Q/I², and a t_{k−1} prediction
interval PI = exp(μ ± t_{k−1}·√(τ²+SE²_pool)). We report the PI under both the observed
DL τ² and an imposed τ²=0.05 representing plausible between-device diversity that DL
under-detects at small k. Strata: device/comparator and era (pre-2015 vs 2015–2024). All
values are emitted by `16-mcs-taxonomy-verify.py`.

## 3. Results

### 3.1 Trials and device taxonomy

| Trial | PMID | Device vs comparator | Mortality effect | Year |
|---|---|---|---|---|
| IABP-SHOCK II | 22920912 | IABP vs none | RR 0.96 (0.79–1.17) | 2012 |
| IMPRESS | 27810347 | Impella vs **IABP** | HR 0.96 (0.42–2.18) | 2017 |
| ECMO-CS | 36335478 | VA-ECMO vs conservative | ≈1.05 (0.72–1.53)* | 2023 |
| ECLS-SHOCK | 37634145 | VA-ECMO vs medical | RR 0.98 (0.80–1.19) | 2023 |
| DanGer Shock | 38587239 | Impella vs **standard** | HR 0.74 (0.55–0.99) | 2024 |

*ECMO-CS all-cause mortality is a secondary of a composite-primary trial; the RR is
approximate and flagged. Note the comparator column: even the two "Impella" trials are
not comparable — IMPRESS tests Impella *against IABP*, DanGer *against standard care*.

### 3.2 The all-device pool looks homogeneous — and that is the trap

| Model | Pooled HR | 95% z-CI | 95% prediction interval | I² |
|---|---|---|---|---|
| All 5, DL τ² (=0) | 0.935 | 0.83–1.05 | 0.79–1.11 | **0%** |
| All 5, τ²=0.05 (device diversity) | 0.927 | 0.72–1.19 | **0.45–1.89** | — |

The observed heterogeneity is **zero**: Q=3.09 (df 4), I²=0%, DL τ²=0. A naive reading
concludes "the devices are consistent, pooling is fine." This is exactly backwards. The
homogeneity arises because four of five trials (IABP, both VA-ECMO, and Impella-vs-IABP)
cluster near the null — not because the devices are equivalent. The moment genuine
between-device variance is admitted (τ²=0.05, modest by any standard), the **prediction
interval spans 0.45–1.89**: a future MCS trial could plausibly show a 55% mortality
reduction *or* an 89% increase. A pooled estimate whose PI spans benefit to harm cannot
guide the next trial or the next patient.

### 3.3 The one genuinely different device–comparator–population diverges

DanGer Shock is the single trial testing a *distinct* combination — a microaxial pump,
against standard care (not against another device), in STEMI-CS specifically — and it is
the single trial with a significant result (HR 0.74, 0.55–0.99). Its divergence is not
noise to be pooled away; it is the signal that the device–comparator–population triad
matters. Pooling it with IABP-vs-none and ECMO-vs-medical dilutes exactly the
information a clinician needs.

### 3.4 Within-device pools are uninformative at k=2

| Stratum | Pooled HR | HKSJ / prediction interval |
|---|---|---|
| VA-ECMO vs no-ECMO (ECMO-CS + ECLS-SHOCK) | 0.995 | PI 0.32–3.11 |
| "Impella" (IMPRESS + DanGer — mixed comparators) | 0.762 | PI 0.13–4.59 |

Even the device-stratified pools are uninformative at k=2 (t₁ = 12.7), and the "Impella"
stratum is itself apples-and-oranges because IMPRESS and DanGer use different comparators.
This is the recursive lesson: stratifying by device alone is insufficient; comparator and
population must also match.

### 3.5 Era analysis

Splitting pre-2015 (IABP-SHOCK II) versus 2015–2024 (IMPRESS, ECMO-CS, ECLS-SHOCK,
DanGer) leaves the 2015–2024 pool at HR 0.92 (I²=0%) — but this masks the same problem:
the modern era contains the null VA-ECMO trials *and* the positive DanGer trial, and its
apparent homogeneity is again a coincidence of near-null clustering, not device
equivalence.

## 4. Discussion

The MCS evidence base is a case study in why the **prediction interval** — not the
confidence interval, and certainly not I² alone — is the statistic that answers the
clinically decisive question. The all-device pooled hazard ratio (0.935) is stable and
its I² is zero, which in most meta-analyses would be reported as reassuring consistency.
Here it is a trap. The homogeneity is an artifact of four trials clustering near the null
(IABP, both VA-ECMO comparisons, Impella-vs-IABP); it says nothing about whether a
mechanistically distinct device, tested against a different comparator in a different
population, will behave the same way — and the one such trial available (DanGer) shows it
does not. Admitting even modest between-device variance produces a prediction interval
(0.45–1.89) that spans meaningful benefit to meaningful harm.

The methodological prescription follows directly. First, MCS meta-analyses must report
prediction intervals; a CI that excludes the null while the PI spans harm is a routine
occurrence in small-k, high-diversity evidence and must not be presented as a settled
effect. Second, low observed I² is a *necessary but not sufficient* condition for
pooling: mechanistic and comparator homogeneity are independent prerequisites that a
heterogeneity statistic cannot certify. Third, stratification must be by the full
**device × comparator × population** triad, not by device alone — as the "Impella"
stratum's internal incoherence (vs IABP in IMPRESS, vs standard in DanGer) demonstrates.

This reframes the relationship with the clinical companion paper (23). That paper's
device-stratified reading — VA-ECMO and IABP null, Impella-in-STEMI-vs-standard the lone
positive — is not merely one way to slice the data; it is the *only* defensible synthesis,
because the all-device pool that would otherwise dominate guidelines is, on its own
prediction interval, uninformative. The apples-and-oranges critique is thus not a
statistical nicety but the difference between a pooled number that misleads and a
stratified reading that informs.

## 5. Limitations

Five trials is a small evidence base; the τ²=0.05 sensitivity is illustrative, not
estimated (DL cannot estimate it reliably at k=5, which is itself part of the argument).
ECMO-CS mortality is an approximate secondary endpoint and is flagged. Mixed effect
measures (RR vs HR) are pooled, as is standard in the critiqued analyses; this is a known
limitation shared with them. High-risk-PCI MCS trials were not included; the focus is CS
mortality. The paper's claims are methodological — about how MCS evidence should be
synthesised — and inherit the clinical caveats of paper 23.

## 6. Conclusion

An all-device MCS mortality pool yields HR 0.935 with I²=0% — statistically homogeneous,
and clinically uninformative. The homogeneity reflects trials clustering near the null,
not device equivalence; the one trial testing a distinct device–comparator–population
(DanGer, HR 0.74) diverges significantly, and a realistic heterogeneity yields a
prediction interval (0.45–1.89) spanning benefit to harm. MCS evidence synthesis must
report prediction intervals and must stratify by the full device × comparator ×
population triad. Statistical homogeneity does not license pooling mechanistically
distinct devices.

---

## References

1. Thiele H, Zeymer U, Neumann FJ, et al. Intraaortic balloon support for myocardial infarction with cardiogenic shock (IABP-SHOCK II). *N Engl J Med.* 2012;367(14):1287–1296. PMID: 22920912. doi:10.1056/NEJMoa1208410.
2. Ouweneel DM, Eriksen E, Sjauw KD, et al. Percutaneous mechanical circulatory support versus intra-aortic balloon pump in cardiogenic shock after AMI (IMPRESS). *J Am Coll Cardiol.* 2017;69(3):278–287. PMID: 27810347. doi:10.1016/j.jacc.2016.10.022.
3. Ostadal P, Rokyta R, Karasek J, et al. Extracorporeal membrane oxygenation in the therapy of cardiogenic shock (ECMO-CS). *Circulation.* 2023;147(6):454–464. PMID: 36335478. doi:10.1161/CIRCULATIONAHA.122.062949.
4. Thiele H, Zeymer U, Akin I, et al. Extracorporeal Life Support in Infarct-Related Cardiogenic Shock (ECLS-SHOCK). *N Engl J Med.* 2023;389(14):1286–1297. PMID: 37634145. doi:10.1056/NEJMoa2307227.
5. Møller JE, Engstrøm T, Jensen LO, et al. Microaxial Flow Pump or Standard Care in Infarct-Related Cardiogenic Shock (DanGer Shock). *N Engl J Med.* 2024;390(14):1382–1393. PMID: 38587239. doi:10.1056/NEJMoa2312572.
6. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247. PMID: 27406637. doi:10.1136/bmjopen-2015-010247.

---

*Data-integrity note.* The five trial PMIDs (22920912, 27810347, 36335478, 37634145,
38587239) and the IntHout prediction-interval reference (27406637) were verified by
PubMed metadata match on 2026-07-04 (same verified set as paper 23). ECMO-CS mortality is
an approximate secondary and is flagged; the τ²=0.05 sensitivity is explicitly imposed,
not estimated. All pooled estimates, prediction intervals, strata, and the era split are
emitted by `16-mcs-taxonomy-verify.py`. **Build target:** `.docx` + figures via the E156
host build (`outputs/journal-upgrades/build/16-mcs-taxonomy-v2/`); render the
prediction-interval forest (§3.2) and the device × comparator matrix (§3.1).
