# Cochrane in the Modern Random-Effects Era: Why DL Is Not Enough, and What Replaces It — A Worked Example

**Published (base article):** Synthēsis · View/cochrane-modern-re
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `cochrane-modern-re-verify.py` (deterministic; numpy+scipy)
**Evidence tier:** methodological demonstration on a verified clinical dataset.
**Standard:** REML/Paule–Mandel · HKSJ (t_{k−1}, q≥1 floor) · prediction interval · reproduce-or-flag.

---

## Upgrade note (what changed from v1)

v1 described the modern random-effects (RE) toolkit narratively. v2 **demonstrates it on a
verified clinical dataset** — the four pivotal SGLT2-inhibitor heart-failure trials (the
same PubMed-verified hazard ratios used across the Synthēsis SGLT2-HF papers) — with a
deterministic script that computes DerSimonian–Laird (DL), REML, and Paule–Mandel (PM)
τ²; the naive-z versus HKSJ intervals; and the prediction interval, side by side. Every
number is reproducible and matches the SGLT2-HF synthesis, so the methods lesson is
anchored to real, verified data rather than a toy example.

---

## Abstract

**Background.** For decades, Cochrane's default meta-analysis used the DerSimonian–Laird
(DL) random-effects estimator with a normal-approximation confidence interval (CI). At the
small trial counts (k) typical of clinical evidence, this default is now known to be
inadequate. We demonstrate the modern replacements on a verified dataset.

**Methods.** Using the four pivotal SGLT2-inhibitor heart-failure trials, we computed τ²
by DL, REML, and PM; the pooled hazard ratio with a normal-z CI versus the
Hartung–Knapp–Sidik–Jonkman (HKSJ) t_{k−1} CI (with the q≥1 floor); and the 95% prediction
interval. Deterministic script.

**Results.** Cochran Q=1.64 (df 3), I²=0%, and all three τ² estimators returned ~0 —
genuine homogeneity. The pooled HR was 0.778 in every model. But the interval changed
materially: the naive-z CI was **0.730–0.831** (width 0.101), while the modern **HKSJ
t_{k−1} CI was 0.701–0.865** (width **0.164**) — 62% wider, appropriately reflecting the
uncertainty of estimating between-trial variance from only four trials. The 95% prediction
interval (0.701–0.865) excluded unity.

**Conclusion.** DL with a z-interval understates uncertainty at small k even when
heterogeneity is genuinely zero, because it ignores the imprecision of τ̂². The modern
minimum — REML or PM for τ², HKSJ with t_{k−1} and the q≥1 floor for the CI, and a
prediction interval for forecasting — should be the default for clinical meta-analyses,
and this worked example shows exactly what each component does.

---

## 1. Introduction

Meta-analysis is only as trustworthy as its uncertainty quantification, and the field's
long-standing default — DerSimonian–Laird random effects with a normal-approximation
confidence interval — was designed for an era of larger k than most clinical questions
afford. Three specific problems bite at small k: DL's method-of-moments τ² estimator is
downward-biased; the normal-z interval ignores the extra uncertainty of having *estimated*
the between-study variance; and the CI answers the wrong question for a clinician, who
wants to know what the *next* trial will show (the prediction interval), not where the mean
effect lies. This paper demonstrates the modern replacements on verified data so that the
methods are concrete, not abstract.

## 2. Methods

We used the four pivotal SGLT2-inhibitor heart-failure trials — DAPA-HF 0.74 (0.65–0.85),
EMPEROR-Reduced 0.75 (0.65–0.86), EMPEROR-Preserved 0.79 (0.69–0.90), DELIVER 0.82
(0.73–0.92) — pooling on the log-hazard-ratio scale. We computed τ² by three estimators
(DL, REML, PM), the pooled HR with a normal-z CI and with the HKSJ correction using
t_{k−1} critical values and the q≥1 floor (so HKSJ can only widen, never narrow below the
DL interval), Cochran Q and I², and the 95% prediction interval PI = exp(μ ± t_{k−1}·√(τ²
+ SE²_pool)). All values are emitted by `cochrane-modern-re-verify.py`.

## 3. Results

### 3.1 Heterogeneity and τ² estimators

| Statistic | Value |
|---|---|
| Cochran Q (df 3) | 1.64 |
| I² | 0.0% |
| τ² — DerSimonian–Laird | 0.00000 |
| τ² — REML | 0.00000 |
| τ² — Paule–Mandel | 0.00000 |

Here the between-trial variance is genuinely ~0, so the estimators agree. This is the
important teaching case: **even when τ² is truly zero, the choice of interval still
matters**, because the interval must account for the fact that we *estimated* τ² and could
not have known in advance that it was zero.

### 3.2 The interval is where the modern methods differ

| Model | Pooled HR | 95% CI | Width |
|---|---|---|---|
| DL + normal-z (old Cochrane default) | 0.778 | 0.730–0.831 | 0.101 |
| REML + normal-z | 0.778 | 0.730–0.831 | 0.101 |
| **REML + HKSJ t_{k−1} (modern default)** | **0.778** | **0.701–0.865** | **0.164** |

```
Pooled SGLT2i HR — interval by method
 naive-z CI   [====]            0.730–0.831
 HKSJ t3 CI  [========]         0.701–0.865   (62% wider, honest at k=4)
            0.70   0.78   0.87
```

The point estimate is identical across methods (0.778), but the HKSJ interval is **62%
wider** than the naive-z interval. That extra width is not a defect — it is the honest
price of estimating a variance component from four trials. Reporting the narrow z-interval
would overstate precision, exactly the failure mode that has produced over-confident
small-k meta-analyses across the literature.

### 3.3 The prediction interval answers the clinician's question

The 95% prediction interval (REML, t_{k−1}) is **0.701–0.865** and **excludes unity** — a
future trial of the same design in a comparable population would be expected to show
benefit. This is the statistic that should accompany every clinical meta-analysis: the CI
describes the *mean* effect across trials; the PI describes the *range of true effects*,
which is what a clinician facing the next patient (or a guideline anticipating the next
trial) actually needs.

### 3.4 When it matters more than here

This dataset is the *easy* case (τ²=0), and even here the interval choice changes the width
by 62%. Under genuine heterogeneity at small k — the common situation — the gap is far
larger: DL under-estimates τ², the naive-z interval compounds the under-estimation, and the
pooled result can appear significant when a correct HKSJ interval and prediction interval
would span the null. The methods advocated here are therefore not a refinement for edge
cases; they are the default that prevents routine over-confidence.

## 4. Discussion

The modern random-effects toolkit rests on three replacements for the DL-plus-z default,
and this worked example isolates each. First, **REML or Paule–Mandel** should estimate τ²
instead of DL, because DL's method-of-moments estimator is downward-biased at small k;
here all three agree only because the truth is τ²=0, but that agreement cannot be assumed
in advance and does not hold under real heterogeneity. Second, the **HKSJ correction with
t_{k−1} and the q≥1 floor** should replace the normal-z interval, because it accounts for
the uncertainty of the estimated variance — and, as shown, it widens the interval by 62%
even in the zero-heterogeneity case, which is precisely when a naive analyst would wrongly
feel safest. The q≥1 floor is the essential guardrail: without it, HKSJ can pathologically
*narrow* the interval when Q < k−1, producing intervals more over-confident than the method
it replaces. Third, the **prediction interval** should be reported alongside the CI, because
it answers the forward-looking question the CI cannot.

None of this is controversial in the methods literature — it is the Cochrane Handbook's own
modern guidance — yet the DL-plus-z default persists in a large fraction of published
clinical meta-analyses, and with it a systematic overstatement of precision at exactly the
small k where clinical questions live. The value of a worked example on verified data is to
make the abstraction concrete: on four real, verified trials, switching from the old default
to the modern one leaves the point estimate untouched (0.778) and widens the interval by
62%, and adds a prediction interval that reframes the result from "the average trial showed
benefit" to "the next trial is expected to show benefit." Those are different claims, and
only the modern toolkit distinguishes them.

## 5. Limitations

The demonstration uses one dataset with τ²=0; the contrast under genuine heterogeneity is
described but not tabulated here (it would require a second worked example with a
heterogeneous corpus). HKSJ can itself be anticonservative in rare configurations, which is
why the q≥1 floor is mandatory. The prediction interval assumes normally-distributed
between-study effects, an assumption that is weak at very small k. These are refinements of,
not objections to, the recommended default.

## 6. Conclusion

On four verified SGLT2-inhibitor heart-failure trials, the pooled hazard ratio is 0.778
under every method, but the modern HKSJ t_{k−1} interval (0.701–0.865) is 62% wider than the
old DL-plus-z interval (0.730–0.831), and the prediction interval (0.701–0.865) excludes
unity. At the small k typical of clinical evidence, REML/PM for τ², HKSJ with the q≥1 floor
for the CI, and a prediction interval for forecasting are the minimum standard — DL with a
normal-z interval systematically overstates precision and should be retired as a default.

---

## References

1. Higgins JPT, Thomas J, Chandler J, et al. (eds). *Cochrane Handbook for Systematic Reviews of Interventions.* Version 6.5. Cochrane; 2024.
2. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247. PMID: 27406637. doi:10.1136/bmjopen-2015-010247.
3. Vaduganathan M, Docherty KF, Jhund PS, et al. SGLT-2 inhibitors in patients with heart failure: a comprehensive meta-analysis of five randomised controlled trials. *Lancet.* 2022;400(10354):757–767. PMID: 36115363. doi:10.1016/S0140-6736(22)01429-5.

---

*Data-integrity note.* The four SGLT2-inhibitor trial hazard ratios are the PubMed-verified
values used across the Synthēsis SGLT2-HF v2 papers (DAPA-HF 31535829, EMPEROR-Reduced
32865377, EMPEROR-Preserved 34449189, DELIVER 36027570); the pooled HR (0.778) matches the
Vaduganathan five-trial benchmark. All τ² estimators, the naive-z vs HKSJ intervals, and the
prediction interval are computed by `cochrane-modern-re-verify.py`. IntHout (27406637) was
verified earlier in this program. **Build target:** `.docx` + figures via the E156 host build
(`outputs/journal-upgrades/build/cochrane-modern-re-v2/`); render the interval-by-method panel
(§3.2).
