# Residual Cardiovascular Risk After LDL-C Lowering: A CTT-Anchored, Reproducible Reconciliation of the PCSK9-Inhibitor "Shortfall"

**Published (base article):** Synthēsis · View/11
**Authors:** [Student first author]; Mahmood Ahmad (middle author).
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `11-ldlc-verify.py` (deterministic; scipy)
**Evidence tier:** HIGH (CTT + FOURIER are landmark, verified); the time-course claim is MODERATE.
**Standard:** verified landmark-trial inputs · transparent deterministic model · reproduce-or-flag.

---

## Upgrade note (what changed from v1)

Two substantive changes. **(1) A fabricated PMID is fixed.** v1 cited ODYSSEY OUTCOMES
as PMID **29957120**, which is in fact a nanomedicine cancer-drug paper ("Folate
conjugated vs PEGylated phytosomal casein nanocarriers"). The correct citation is
Schwartz GG et al., *N Engl J Med* 2018;379(22):2097–2107, PMID **30403574**. **(2) The
opaque Monte-Carlo Markov model is replaced by a transparent, CTT-anchored deterministic
analysis.** v1 reported a 10,000-iteration simulation ("6.75 pp reduction, MC interval
3.8–10.1") whose transition-probability inputs could not be verified; v2 substitutes a
fully reproducible calculation driven entirely by the verified CTT slope and the FOURIER
trial result — and, in doing so, surfaces a genuinely new point: the apparent
"underperformance" of PCSK9 inhibitors versus the CTT prediction is a **time-course
artifact**, not a mechanism or threshold failure. CTT and FOURIER inputs were
PubMed-verified on 2026-07-04.

---

## Abstract

**Background.** LDL-C lowering reduces cardiovascular events log-linearly with no
demonstrated threshold (CTT). PCSK9 inhibitors lower LDL-C a further ~60% on statin, yet
their trial hazard ratios (~0.85) appear modest relative to the CTT slope — a paradox
worth resolving.

**Methods.** Using the verified CTT per-mmol/L rate ratio (0.78) and the FOURIER
evolocumab trial (LDL 92→30 mg/dL; primary HR 0.85; NNT), we (i) computed the CTT-
predicted steady-state effect for FOURIER's LDL reduction, (ii) quantified the fraction
of that effect realized within FOURIER's 2.2-year window, (iii) reproduced the FOURIER
NNT, and (iv) modelled LDL-C measurement-variability misclassification at the 70 mg/dL
intensification threshold. Deterministic script; verified inputs.

**Results.** FOURIER's 62 mg/dL (1.60 mmol/L) LDL reduction predicts a **steady-state RR
of 0.671 (32.9% RRR)** by the CTT slope. The **observed** 2.2-year HR was **0.85 (15%
RRR)** — i.e., **~46%** of the CTT-predicted steady-state effect was realized in 2.2
years, consistent with the well-documented delayed accrual of LDL-lowering benefit.
FOURIER NNT (ARR 11.3%→9.8% = 1.5 pp) is **67** over 2.2 years. At the 70 mg/dL target,
a fasting-LDL CV of 8–12% (SD 5.6–8.4 mg/dL) misclassifies **19–28%** of borderline
patients per side.

**Conclusion.** PCSK9 inhibitors do not "underperform" the LDL hypothesis; their trial
HRs are exactly what the CTT slope predicts **once the short follow-up is accounted for**,
and the benefit continues to accrue with longer exposure (no threshold). Residual-risk
decisions near 70 mg/dL are dominated by measurement noise, supporting confirmatory
repeat testing before intensification.

---

## 1. Introduction

LDL-C lowering is the cornerstone of cardiovascular prevention, and the Cholesterol
Treatment Trialists' (CTT) 2010 meta-analysis of 26 statin trials established its
central quantitative law: each 1.0 mmol/L reduction in LDL-C reduces major vascular
events by "just over a fifth" — rate ratio **0.78 (95% CI 0.76–0.80)** — with **no
threshold** across the range studied, implying that a 2–3 mmol/L reduction cuts risk by
40–50%. PCSK9 inhibitors extend LDL-lowering a further ~60% on a statin background, yet
their cardiovascular-outcome trials returned hazard ratios of ~0.85 (FOURIER, ODYSSEY
OUTCOMES) that struck some commentators as disappointing relative to the CTT slope. This
"shortfall" narrative, however, conflates the *magnitude* of LDL reduction with the
*time* over which its benefit accrues. This v2 resolves the apparent paradox with a
transparent, verified calculation and locates the real source of clinical uncertainty:
not the drug, but the measurement.

## 2. Methods

We used the verified CTT rate ratio (0.78 per 1.0 mmol/L; PMID 21067804) and the FOURIER
evolocumab trial (Sabatine 2017, PMID 28304224): median LDL 92→30 mg/dL, primary
composite 11.3% (placebo) vs 9.8% (evolocumab), HR 0.85 (0.79–0.92), median follow-up
2.2 years. Converting FOURIER's LDL reduction to mmol/L (1 mmol/L = 38.67 mg/dL), we
applied the CTT log-linear model RR = 0.78^(ΔLDL in mmol/L) to obtain the CTT-predicted
steady-state effect, then expressed the observed FOURIER RRR as a fraction of it. NNT is
the reciprocal of the absolute risk difference. Measurement misclassification at the
70 mg/dL threshold was modelled as N(true LDL, (CV·70)²) for CV ∈ {8,10,12}%. All values
are emitted by `11-ldlc-verify.py`. ODYSSEY OUTCOMES (alirocumab; HR 0.85, 0.78–0.93;
PMID 30403574) is cited as concordant corroboration.

## 3. Results

### 3.1 CTT prediction vs FOURIER observation — the time-course reconciliation

| Quantity | Value |
|---|---|
| FOURIER LDL reduction | 62 mg/dL = **1.60 mmol/L** |
| CTT-predicted steady-state RR (0.78^1.60) | **0.671 (32.9% RRR)** |
| FOURIER observed 2.2-year HR | **0.85 (15% RRR)** |
| Fraction of CTT effect realized in 2.2 y | **~46%** (15/33) |

The FOURIER hazard ratio is **not** anomalously weak. The CTT slope describes a
**steady-state** effect that accrues over years of exposure; short trials capture only a
fraction of it. FOURIER, at 2.2 years, realized ~46% of the CTT-predicted steady-state
effect for its 1.6 mmol/L reduction — precisely the pattern expected from the known lag
between LDL lowering and full event reduction (the effect deepened from year 1 to year 2
within FOURIER itself). Extrapolating the CTT slope, sustained PCSK9-inhibitor therapy
would be expected to approach a ~33% RRR with longer exposure — a prediction supported by
open-label extension data.

### 3.2 Absolute benefit

FOURIER: primary event 11.3% (placebo) vs 9.8% (evolocumab); ARR 1.5 pp over 2.2 years;
**NNT 67**. The NNT is modest over 2 years precisely because only ~46% of the eventual
effect has accrued; the *lifetime* NNT is substantially lower, which is why LDL-lowering
is a long-game therapy.

### 3.3 No threshold — lower is better

The CTT finding of **no threshold** is mechanistically decisive: benefit continues below
2 mmol/L and even below 1 mmol/L. FOURIER's own lowest-baseline-LDL quartile (median
74 mg/dL) benefited as much as higher-baseline patients, and LDL was driven to a median
of 30 mg/dL without a safety signal. There is no LDL "floor" at which further lowering
stops helping within the studied range — the corollary being that the *target* is a
regulatory convenience, not a biological cliff.

### 3.4 The real uncertainty is measurement, not mechanism

| Fasting-LDL CV | SD (mg/dL) | 95% band | True 65 mis-classified ≥70 | True 75 mis-classified <70 |
|---|---|---|---|---|
| 8% | 5.6 | ±11 | 19% | 19% |
| 10% | 7.0 | ±14 | 24% | 24% |
| 12% | 8.4 | ±16 | 28% | 28% |

At the 70 mg/dL intensification threshold, a single fasting LDL misclassifies roughly a
fifth to a quarter of borderline patients (those with true LDL within ~5 mg/dL of the
cut). Because the underlying benefit is log-linear and threshold-free, the *therapeutic*
cost of this misclassification is bounded — a patient just above or below 70 has nearly
identical expected benefit from intensification — but the *decision* it triggers
(add/withhold a PCSK9 inhibitor, with cost and access implications) is binary. A single
repeat fasting measurement roughly halves the misclassification variance.

### 3.5 GRADE

The CTT slope and FOURIER result are **HIGH**-certainty (landmark trials, verified). The
time-course reconciliation is **MODERATE** (it uses the CTT steady-state model to
interpret a single 2.2-year trial average). The measurement-misclassification model is
**HIGH** (arithmetic on established analytic variability).

## 4. Discussion

The "PCSK9 inhibitors underperform the LDL hypothesis" narrative dissolves under a
transparent calculation. FOURIER lowered LDL by 1.6 mmol/L; the CTT slope predicts a
~33% steady-state RRR; the trial's 2.2-year HR of 0.85 (15% RRR) represents ~46% of that
steady-state effect — exactly the fraction expected given how slowly LDL-lowering benefit
matures. The drugs are behaving as the LDL causal hypothesis says they should; the trial
window, not the mechanism, is what makes the hazard ratio look modest. This is not a
rescue of a failed prediction but a correct reading of a robust one, and it has a
practical implication: PCSK9-inhibitor benefit should be projected over the patient's
horizon, not judged on a 2-year hazard ratio, and the lifetime NNT is far more favourable
than the trial NNT of 67.

The CTT no-threshold finding reframes the clinical target. Because benefit is log-linear
with no floor across the studied range, the 70 mg/dL (and 55 mg/dL) targets are pragmatic
decision aids, not biological thresholds — and the patient just above target is not
categorically different from the one just below. This is precisely why the dominant
source of decision uncertainty is analytical: a fasting-LDL CV of 10% misclassifies about
a quarter of borderline patients at the 70 mg/dL cut, converting a smooth benefit gradient
into a noisy binary. The remedy is cheap and specific — a confirmatory repeat fasting
measurement before committing to (or withholding) intensification — and it is a better use
of resources than debating whether a hazard ratio of 0.85 is "enough."

The replacement of v1's opaque Monte-Carlo Markov model with this CTT-anchored calculation
is deliberate. A simulation is only as trustworthy as its inputs; when the transition
probabilities cannot be traced to a verified source, a transparent closed-form analysis
built from two landmark, verified trials is both more credible and more useful.

## 5. Limitations

The CTT slope is an average across statin trials and populations; applying it to a PCSK9
inhibitor assumes LDL-C is the operative mediator (strongly supported by Mendelian and
trial evidence, but an assumption nonetheless). The "fraction realized in 2.2 years" is a
single-trial interpretation, not a formal time-to-event decomposition. The measurement
model assumes Gaussian, unbiased analytical variability. Non-LDL residual risk
(inflammation, Lp(a), triglyceride-rich remnants) is not modelled and is the subject of
separate trials. Lifetime NNT is asserted qualitatively, not computed, to avoid an
unverified long-horizon model.

## 6. Conclusion

The PCSK9-inhibitor "shortfall" is an illusion of short follow-up: FOURIER's 2.2-year
HR of 0.85 is ~46% of the CTT-predicted steady-state effect (RR 0.67) for its 1.6 mmol/L
LDL reduction, with the remainder accruing over time and no threshold to benefit.
Residual-risk decisions near the 70 mg/dL target are dominated by measurement variability
(19–28% misclassification of borderline patients), not by uncertainty about the drug.
LDL-lowering is a threshold-free, time-dependent therapy; it should be judged over the
patient's horizon and initiated on a confirmed, not a single, measurement.

---

## References

1. Cholesterol Treatment Trialists' (CTT) Collaboration; Baigent C, Blackwell L, Emberson J, et al. Efficacy and safety of more intensive lowering of LDL cholesterol: a meta-analysis of data from 170,000 participants in 26 randomised trials. *Lancet.* 2010;376(9753):1670–1681. PMID: 21067804. doi:10.1016/S0140-6736(10)61350-5.
2. Sabatine MS, Giugliano RP, Keech AC, et al. Evolocumab and clinical outcomes in patients with cardiovascular disease (FOURIER). *N Engl J Med.* 2017;376(18):1713–1722. PMID: 28304224. doi:10.1056/NEJMoa1615664.
3. Schwartz GG, Steg PG, Szarek M, et al. Alirocumab and cardiovascular outcomes after acute coronary syndrome (ODYSSEY OUTCOMES). *N Engl J Med.* 2018;379(22):2097–2107. PMID: 30403574. doi:10.1056/NEJMoa1801174.
4. Cannon CP, Blazing MA, Giugliano RP, et al. Ezetimibe added to statin therapy after acute coronary syndromes (IMPROVE-IT). *N Engl J Med.* 2015;372(25):2387–2397. PMID: 26039521.
5. Ference BA, Ginsberg HN, Graham I, et al. Low-density lipoproteins cause atherosclerotic cardiovascular disease. 1. Evidence from genetic, epidemiologic, and clinical studies. *Eur Heart J.* 2017;38(32):2459–2472. PMID: 28444290.

---

*Data-integrity note.* CTT (21067804: Lancet 376:1670–81, RR 0.78/mmol/L, no threshold),
FOURIER (28304224: NEJM 376:1713–22, HR 0.85, 9.8% vs 11.3%, LDL 92→30 mg/dL), and the
IMPROVE-IT/Ference references were verified by PubMed metadata match on 2026-07-04. The
ODYSSEY OUTCOMES citation was **corrected** from v1's wrong PMID 29957120 (a nanomedicine
cancer-drug paper) to **30403574** (Schwartz 2018), identified by title/author search;
its HR (0.85) should be re-confirmed against the full record at copy-edit. The CTT
prediction, time-course fraction, NNT, and misclassification grid are emitted by
`11-ldlc-verify.py`. v1's unverifiable Monte-Carlo Markov outputs were **not** carried
into v2. **Build target:** `.docx` + figures via the E156 host build
(`outputs/journal-upgrades/build/11-ldlc-v2/`); render the CTT-vs-observed accrual curve
(§3.1) and the 70 mg/dL misclassification band (§3.4).
