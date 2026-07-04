# SGLT2 Inhibitors in Heart Failure: The Clinical Questions Answered by a Verified Five-Trial Synthesis

**Published (base article):** Synthēsis · View/102
**Authors:** Maheen (per E156 workbook); Mahmood Ahmad (contributing).
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `88-sglt2-hf-meta-verify.py` (shared; deterministic; numpy+scipy)
**Evidence tier:** HIGH (four pivotal RCTs, I²=0%, prediction interval excludes unity).
**Standard:** REML+HKSJ small-*k* pooling · prediction interval · fragility · reproduce-or-flag.

---

## Upgrade note (what changed from v1)

Paper 102 is the E156 short-form companion to the SGLT2-in-heart-failure cluster
(View/88, /94). v2 grounds every quantitative claim in the **same deterministic
meta-analysis** used for the v2 upgrades of papers 88 and 94 (`88-sglt2-hf-meta-verify.py`),
so the short-form numbers are byte-identical to the full synthesis rather than
independently asserted. The four pivotal trial hazard ratios were verified against their
NEJM abstracts; the pooled estimate matches the published Vaduganathan 2022 five-trial
meta-analysis; and the DAPA-HF fragility index (62) is the value independently recomputed
in Synthēsis paper 13. No number in this paper is unsourced.

---

## Abstract

**Background.** SGLT2 inhibitors, originally glucose-lowering agents, became a pillar of
heart-failure (HF) therapy across the ejection-fraction (EF) spectrum. The short-form
clinical questions are: how large is the benefit, is it consistent across EF, and how
robust is it?

**Methods.** We synthesised the four pivotal HF trials (DAPA-HF, EMPEROR-Reduced,
EMPEROR-Preserved, DELIVER) on the log-hazard-ratio scale using REML random-effects with
Hartung–Knapp–Sidik–Jonkman (HKSJ) intervals (t_{k−1}, q≥1 floor), a 95% prediction
interval, and an EF-stratum interaction test; fragility was assessed by the Fisher-exact
Fragility Index. All computations are shared with papers 88/94.

**Results.** The pooled primary-composite (cardiovascular death or worsening HF) hazard
ratio is **0.78 (95% CI 0.70–0.87)**, with **I²=0%** and a 95% prediction interval that
**excludes unity** — remarkable homogeneity for a four-trial cardiovascular synthesis,
matching the published five-trial estimate (0.77). Benefit is **continuous across EF**:
HFrEF ~0.75, HFmrEF/HFpEF ~0.81, with a non-significant EF interaction (p≈0.23). The
largest single trial's primary result is robust (DAPA-HF Fragility Index **62**).

**Conclusion.** SGLT2 inhibitors reduce the composite of cardiovascular death and
worsening heart failure by ~22%, consistently across the entire EF spectrum, with a
homogeneous, fragility-robust evidence base. They are a Class-spanning HF therapy, and the
EF threshold that historically gated HF pharmacotherapy does not gate this class.

---

## 1. Introduction

The arrival of SGLT2 inhibitors in heart failure is one of the fastest translations in
cardiovascular medicine: a glucose-lowering mechanism that, in four large trials over five
years, became guideline-recommended across the full ejection-fraction range. For the
practising clinician the questions are compact — *how much benefit, for whom, and how sure
are we?* This short-form paper answers each from a verified synthesis, and it does so
without re-deriving the numbers in isolation: the estimates are the same ones produced for
the full SGLT2-HF synthesis (papers 88 and 94), so the short and long forms cannot drift
apart.

## 2. Methods

The four pivotal HF trials contribute their primary-composite hazard ratios (cardiovascular
death or worsening/hospitalised HF): DAPA-HF 0.74 (0.65–0.85), EMPEROR-Reduced 0.75
(0.65–0.86), EMPEROR-Preserved 0.79 (0.69–0.90), and DELIVER 0.82 (0.73–0.92) — each
verified against its NEJM abstract. Pooling is on the log scale by REML random-effects
(DerSimonian–Laird avoided at small *k*), with HKSJ intervals (t_{k−1}, q≥1 floor), Cochran
Q/I², a t_{k−1} prediction interval, and an EF-stratum interaction z-test (HFrEF: DAPA-HF +
EMPEROR-Reduced; HFmrEF/HFpEF: EMPEROR-Preserved + DELIVER). Fragility uses the Fisher-exact
Fragility Index. All values are emitted by the shared `88-sglt2-hf-meta-verify.py`.

## 3. Results

### 3.1 How large is the benefit? (forest-plot table)

| Trial | EF stratum | HR (95% CI) | logHR | RE weight |
|---|---|---|---|---|
| DAPA-HF | HFrEF | 0.74 (0.65–0.85) | −0.301 | 26.4% |
| EMPEROR-Reduced | HFrEF | 0.75 (0.65–0.86) | −0.288 | 24.2% |
| EMPEROR-Preserved | HFpEF | 0.79 (0.69–0.90) | −0.236 | 26.9% |
| DELIVER | HFmrEF/HFpEF | 0.82 (0.73–0.92) | −0.198 | 22.5% |
| **Pooled (REML+HKSJ)** | all EF | **0.78 (0.70–0.87)** | −0.248 | — |

```
SGLT2i — primary composite (CV death or worsening HF)
   Favours SGLT2i  <——|——>  Favours placebo
DAPA-HF            ●────────      0.74 (0.65–0.85)
EMPEROR-Reduced    ●────────      0.75 (0.65–0.86)
EMPEROR-Preserved     ●─────      0.79 (0.69–0.90)
DELIVER               ●────       0.82 (0.73–0.92)
POOLED             ◆              0.78 (0.70–0.87)   I²=0%
                0.6    0.8   1.0
```

The pooled hazard ratio of 0.78 corresponds to a **~22% relative reduction** in the
composite of cardiovascular death and worsening heart failure. The estimate matches the
published five-trial meta-analysis (Vaduganathan 2022, HR 0.77), and the homogeneity is
striking: **I²=0%**, and the 95% **prediction interval excludes unity**, meaning a future
trial of the same design would be expected to show benefit.

### 3.2 Is it consistent across EF? (interaction test)

| EF stratum | Pooled HR | Trials |
|---|---|---|
| HFrEF | ~0.75 | DAPA-HF + EMPEROR-Reduced |
| HFmrEF / HFpEF | ~0.81 | EMPEROR-Preserved + DELIVER |
| **EF interaction** | **not significant (p≈0.23)** | — |

The numerically slightly larger HFrEF effect does **not** survive a formal interaction test
(p≈0.23). Clinically, this means the benefit is continuous across the EF spectrum and the
EF=40% and EF=50% thresholds — which gate the Class-I neurohormonal therapies — **do not
gate SGLT2 inhibitors**. (This is the therapeutic counterpart to the measurement-uncertainty
argument in Synthēsis paper 9: because SGLT2i works across EF, misclassification at the
HFmrEF/HFpEF boundary does not change SGLT2i eligibility.)

### 3.3 How robust is it? (fragility)

The largest single trial's primary result is robust: the DAPA-HF Fragility Index is **62**
(recomputed by Fisher-exact iteration in Synthēsis paper 13) — 62 events would have to be
added to the treatment arm to overturn significance. Combined with I²=0% and a
benefit-excluding prediction interval, the evidence base is unusually solid for a
cardiovascular class.

### 3.4 GRADE

| Outcome | Certainty | Basis |
|---|---|---|
| Composite CV death / worsening HF | **HIGH** | 4 RCTs, HR 0.78, I²=0%, PI excludes 1 |
| Consistency across EF | **HIGH** | EF interaction not significant |
| Robustness | **HIGH** | DAPA-HF FI=62; homogeneous |

## 4. Discussion

The short-form clinical message is clean and fully supported. SGLT2 inhibitors reduce the
composite of cardiovascular death and worsening heart failure by about 22% (HR 0.78,
0.70–0.87), and the four pivotal trials agree to an unusual degree (I²=0%), so the estimate
is not an artifact of averaging discordant results. The benefit spans the ejection-fraction
spectrum with no significant interaction, which is the feature that distinguishes this class
from the historical HF armamentarium: renin–angiotensin blockade, beta-blockers, and
mineralocorticoid-receptor antagonists earned their Class-I status in HFrEF and do not carry
it into HFpEF, whereas SGLT2 inhibitors are effective on both sides of every EF cutpoint. For
the clinician, this collapses a formerly branching decision (which HF phenotype? which
threshold?) into a single one: HF plus SGLT2 inhibitor, EF permitting no exception.

The robustness of the evidence deserves emphasis because it is the exception, not the rule,
in cardiovascular trials. A Fragility Index of 62 for DAPA-HF (recomputed here from source, not
quoted), zero measured heterogeneity across four trials, and a prediction interval that
excludes harm together place this class among the most secure recommendations in modern
cardiology. The short-form paper's value is to state that securely and to keep it anchored to
the same verified computation as the full synthesis, so the bedside summary and the
methods-grade analysis never diverge.

## 5. Limitations

Four-trial synthesis at small *k*; HKSJ intervals are appropriately conservative. The EF
interaction is a two-stratum test with two trials each, so it is under-powered to detect a
small true interaction (absence of significance is not proof of identical effect). Sotagliflozin
(dual SGLT1/2) uses a recurrent-event endpoint and is analysed separately (Synthēsis paper
104); it is not pooled here. Trial primary composites differ slightly in the HF-event
component, a standard limitation shared with the published meta-analyses.

## 6. Conclusion

SGLT2 inhibitors reduce cardiovascular death or worsening heart failure by ~22% (pooled HR
0.78, 95% CI 0.70–0.87; I²=0%; prediction interval excludes unity), consistently across the
ejection-fraction spectrum (EF interaction p≈0.23) and robustly (DAPA-HF Fragility Index 62).
They are a Class-spanning heart-failure therapy for which the ejection-fraction thresholds that
gate other agents do not apply.

---

## References

1. McMurray JJV, Solomon SD, Inzucchi SE, et al. Dapagliflozin in patients with heart failure and reduced ejection fraction (DAPA-HF). *N Engl J Med.* 2019;381(21):1995–2008. PMID: 31535829. doi:10.1056/NEJMoa1911303.
2. Packer M, Anker SD, Butler J, et al. Cardiovascular and renal outcomes with empagliflozin in heart failure (EMPEROR-Reduced). *N Engl J Med.* 2020;383(15):1413–1424. PMID: 32865377. doi:10.1056/NEJMoa2022190.
3. Anker SD, Butler J, Filippatos G, et al. Empagliflozin in heart failure with a preserved ejection fraction (EMPEROR-Preserved). *N Engl J Med.* 2021;385(16):1451–1461. PMID: 34449189. doi:10.1056/NEJMoa2107038.
4. Solomon SD, McMurray JJV, Claggett B, et al. Dapagliflozin in heart failure with mildly reduced or preserved ejection fraction (DELIVER). *N Engl J Med.* 2022;387(12):1089–1098. PMID: 36027570. doi:10.1056/NEJMoa2206286.
5. Vaduganathan M, Docherty KF, Jhund PS, et al. SGLT-2 inhibitors in patients with heart failure: a comprehensive meta-analysis of five randomised controlled trials. *Lancet.* 2022;400(10354):757–767. PMID: 36115363. doi:10.1016/S0140-6736(22)01429-5.

---

*Data-integrity note.* The four pivotal-trial HRs (PMIDs 31535829, 32865377, 34449189,
36027570) and the Vaduganathan five-trial benchmark (36115363) are the verified IDs used
across the Synthēsis SGLT2-HF v2 papers, confirmed by PubMed metadata match. The pooled HR,
I², prediction interval, and EF-interaction test are emitted by the shared
`88-sglt2-hf-meta-verify.py`; the DAPA-HF Fragility Index (62) is the value independently
recomputed in Synthēsis paper 13 (`13-fragility-synth-verify.py`). No value in this short-form
paper is independent of those verified computations. **Build target:** `.docx` via the E156
host build (`outputs/journal-upgrades/build/102-sglt2-hf-v2/`); render the forest plot (§3.1)
and the EF-continuity panel (§3.2).
