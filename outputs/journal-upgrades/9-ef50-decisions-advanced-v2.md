# The EF50 Decision Threshold: Measurement Uncertainty in HFmrEF — and Why It Matters Only at One Edge

**Published (base article):** Synthēsis · View/9
**Authors:** [Student first author]; Mahmood Ahmad (middle author).
**Version:** v2 — world-class upgrade (journal-upgrade program)
**Companion verification script:** `9-ef50-verify.py` (deterministic; scipy)
**Evidence tier:** HIGH for the measurement-uncertainty claim; the therapeutic framing rests on verified SGLT2i trials.
**Standard:** reproducible simulation · SEM/MDC · verified anchors · truth-first framing.

---

## Upgrade note (what changed from v1)

v1 presented a single-point misclassification simulation (true EF 45, SD 5 → 31.7%).
v2 (i) reproduces that result deterministically and **extends it to a full true-EF ×
measurement-SD grid**; (ii) adds an **SEM/MDC-versus-ICC** analysis showing the
minimal detectable change rivals the entire HFmrEF band; and (iii) adds the decisive
new element — a **therapeutic-consequence analysis** grounded in the *verified* SGLT2
inhibitor EF-spectrum trials, showing that EF misclassification is clinically
inconsequential across the HFmrEF↔HFpEF boundary (both benefit from SGLT2i) and matters
chiefly at the **HFrEF (≤40%) edge**, where GDMT Class-I status and device eligibility
turn. Three anchor PMIDs (Universal Definition, Thavendiranathan, ESC 2021) were
PubMed-verified; one unverifiable v1 claim ("60% remain HFmrEF at repeat echo") is
flagged, not asserted.

---

## Abstract

**Background.** Heart-failure classification hinges on left-ventricular ejection
fraction (LVEF): HFrEF ≤40%, HFmrEF 41–49%, HFpEF ≥50% (Universal Definition). The
HFmrEF band is 9 EF points wide, yet echocardiographic EF measurement carries temporal
variability that can exceed 10 EF points by 2D methods.

**Methods.** We modelled EF measurement as Gaussian around a patient's true EF and
computed the probability of cross-boundary misclassification across the HFmrEF band for
measurement SDs of 3, 5, and 8 EF units; derived SEM and minimal detectable change
(MDC) across intraclass-correlation (ICC) values; and mapped the *therapeutic*
consequence of misclassification onto verified guideline-directed-therapy and device
thresholds. Deterministic script; verified anchors.

**Results.** For a patient with true EF 45% and SD 5, total misclassification is
**31.7%** (15.9% to HFrEF, 15.9% to HFpEF). Across the band the total ranges 9.6–37.1%
(SD 3), 31.7–45.7% (SD 5), and 53.2–58.1% (SD 8). At ICC 0.90 the MDC is **8.8 EF
units** — essentially the whole HFmrEF band. Therapeutically, an HFmrEF↔HFpEF
misclassification does **not** change SGLT2-inhibitor eligibility (EMPEROR-Preserved HR
0.79, DELIVER HR 0.82; benefit continuous across EF, interaction NS), whereas an
HFmrEF↔HFrEF (≤40%) misclassification changes ARNI/MRA/β-blocker Class-I status and
ICD/CRT (≤35%) eligibility.

**Conclusion.** EF is a probabilistically imprecise measurement, and HFmrEF is a zone of
diagnostic indeterminacy whose width matches measurement noise. But the clinical stakes
are asymmetric: because SGLT2 inhibitors work across the EF spectrum, the consequential
boundary is the **lower** one (≤40%), where a threshold-sensitive decision should be
confirmed by a more reproducible modality (3D echo or cardiac MRI).

---

## 1. Introduction

Contemporary guidelines divide heart failure by a single number — LVEF — into HFrEF
(≤40%), HFmrEF (41–49%), and HFpEF (≥50%) (Universal Definition of Heart Failure,
Bozkurt 2021; 2021 ESC guideline). This taxonomy gates pharmacotherapy (Class-I
ARNI/ACEi, β-blocker, and MRA in HFrEF) and device therapy (ICD/CRT at EF ≤35%). The
architecture assumes EF can be measured precisely enough to justify hard categorical
cutpoints. That assumption is quantitatively fragile: the modified biplane Simpson's
method depends on image quality, observer skill, geometric assumptions, and temporal
sampling, and reproducibility studies report variability of 5–10 EF units. The HFmrEF
band is 9 units wide — narrower than the measurement noise that assigns patients to it.
This paper quantifies the resulting misclassification, then asks the question v1 did
not: *does it clinically matter, and where?*

## 2. Methods

We modelled a measured EF as N(true EF, SD²). For true EF ∈ {41,43,45,47,49} and SD ∈
{3,5,8} EF units, we computed P(measured ≤40 → misclassified HFrEF) = Φ((40−EF)/SD) and
P(measured ≥50 → misclassified HFpEF) = 1−Φ((50−EF)/SD). SEM = SD_between·√(1−ICC) and
MDC = 1.96·√2·SEM were computed across ICC ∈ {0.70,0.82,0.90,0.95} with a typical
between-patient SD of 10 EF units. Reproducibility anchors are from Thavendiranathan
2013 (JACC; 2D temporal EF variability >0.10, noncontrast 3D echo ~0.06). Therapeutic
consequences use the pre-specified EF thresholds of the 2021 ESC guideline and the
verified SGLT2-inhibitor EF-spectrum trials (EMPEROR-Preserved, DELIVER; see companion
SGLT2 verification `88-sglt2-hf-meta-verify.py` and paper 94). All values are emitted by
`9-ef50-verify.py`.

## 3. Results

### 3.1 Misclassification across the HFmrEF band

| True EF | SD 3 (HFrEF/HFpEF/total) | SD 5 | SD 8 |
|---|---|---|---|
| 41% | 36.9 / 0.1 / **37.1%** | 42.1 / 3.6 / **45.7%** | 45.0 / 13.0 / **58.1%** |
| 43% | 15.9 / 1.0 / **16.8%** | 27.4 / 8.1 / **35.5%** | 35.4 / 19.1 / **54.5%** |
| 45% | 4.8 / 4.8 / **9.6%** | 15.9 / 15.9 / **31.7%** | 26.6 / 26.6 / **53.2%** |
| 47% | 1.0 / 15.9 / **16.8%** | 8.1 / 27.4 / **35.5%** | 19.1 / 35.4 / **54.5%** |
| 49% | 0.1 / 36.9 / **37.1%** | 3.6 / 42.1 / **45.7%** | 13.0 / 45.0 / **58.1%** |

Even under the *conservative* SD of 5, roughly a third of patients whose true EF sits
mid-band (45%) will be measured outside HFmrEF; near the edges (41%, 49%) the rate rises
above 45%. At the realistic routine-2D SD of 8, more than half are misclassified
regardless of true EF. The two edges are asymmetric mirror images: a true EF of 41%
mostly leaks *downward* into HFrEF, a true EF of 49% *upward* into HFpEF.

### 3.2 The minimal detectable change rivals the band width

| ICC | SEM (EF units) | MDC (EF units) |
|---|---|---|
| 0.70 | 5.48 | 15.18 |
| 0.82 | 4.24 | 11.76 |
| 0.90 | 3.16 | **8.77** |
| 0.95 | 2.24 | 6.20 |

Even at an excellent ICC of 0.90, the MDC is **8.8 EF units** — essentially the entire
9-point HFmrEF band. A within-patient EF change smaller than the band width cannot be
statistically distinguished from measurement noise. Only 3D echo or cardiac MRI (ICC
approaching 0.95, MDC ~6) narrows this enough to make single-point band assignment
defensible.

### 3.3 The therapeutic asymmetry (new in v2)

The critical clinical insight is that the *two* HFmrEF boundaries do not carry equal
consequences.

- **Upper boundary (HFmrEF ↔ HFpEF, ~50%).** SGLT2 inhibitors reduce heart-failure
  events across the full EF spectrum: EMPEROR-Preserved HR **0.79 (0.69–0.90)**, DELIVER
  HR **0.82 (0.73–0.92)**, with benefit continuous across EF and **no significant
  EF-interaction** (paper 94, p=0.23). A patient shuffled between HFmrEF and HFpEF by
  measurement noise therefore receives the **same** Class-I/IIa SGLT2i recommendation
  either way. Misclassification here is largely inconsequential for the single therapy
  with proven benefit above EF 40%.
- **Lower boundary (HFmrEF ↔ HFrEF, ≤40%).** This is where misclassification bites. The
  strong Class-I HFrEF quartet (ARNI/ACEi, β-blocker, MRA — and the historical trial
  evidence base) and device eligibility (ICD/CRT at EF ≤35%) are gated at the ≤40% (and
  ≤35%) cutpoints. A true-EF-41% patient measured at 39% is reclassified into a
  category with markedly different Class-I obligations; a true-EF-45% patient measured at
  34% could be considered for an ICD they may not need.

The practical corollary: **threshold-sensitive decisions cluster at the lower edge**,
and it is there — not at the HFpEF boundary — that a confirmatory, more-reproducible
measurement (3D echo, contrast, or CMR) changes management.

### 3.4 GRADE

The measurement-imprecision evidence (reproducibility studies, deterministic
simulation) is **HIGH** certainty — it is arithmetic on established variance estimates.
The therapeutic-asymmetry claim rests on **HIGH**-certainty SGLT2i RCTs but on
guideline-threshold logic for the lower edge, so is best rated **MODERATE**.

## 4. Discussion

Two facts, once quantified, sit in tension. First, the HFmrEF band (9 EF units) is
narrower than the noise of the measurement that populates it: at a realistic 2D SD, a
third to a half of mid-band patients are misclassified, and the minimal detectable
change equals the band width even at excellent reproducibility. Second — and this is the
v2 contribution — the clinical cost of that misclassification is **not** uniform across
the band. Because SGLT2 inhibitors work across the entire EF spectrum, the HFmrEF↔HFpEF
ambiguity that dominates statistical discussions of "is this patient really mid-range?"
has little therapeutic consequence for the one drug class with proven benefit there.
The stakes concentrate at the lower boundary, where the historical HFrEF trial evidence,
the Class-I neurohormonal quartet, and device thresholds create a genuine fork.

This reframes the clinical recommendation. Blanket calls to "repeat all HFmrEF echoes"
misallocate effort. The high-yield action is targeted confirmation when a measured EF
sits near **40% (or 35%)** and a Class-I therapy or device decision hinges on which side
it falls — precisely the setting where the more reproducible modality (3D or CMR,
MDC ~6 vs ~9–12 for 2D) earns its cost. Near the 50% boundary, by contrast, the SGLT2i
recommendation is robust to the misclassification, and repeat imaging is lower-yield.

The measurement-science point stands on its own and is not controversial: EF is a
probabilistic estimate, HFmrEF is a zone of indeterminacy, and single-point categorical
assignment overstates precision. The advance here is to pair that with the therapeutic
map, so the uncertainty is acted upon where it matters and tolerated where it does not.

## 5. Limitations

The Gaussian measurement model is a simplification; real EF error may be skewed and
patient/image-quality dependent. The chosen SDs (3–8) and ICCs bracket the literature
but no single value is universal. The therapeutic-asymmetry argument uses guideline
thresholds and the SGLT2i EF-spectrum trials; other therapies (e.g., finerenone in
HFmrEF/HFpEF; emerging ARNI EF-subgroup data) may further flatten the upper boundary but
are not modelled here. The v1 claim that "only 60% of HFmrEF patients remain HFmrEF at
repeat echo" could not be verified to a primary source and is flagged, not asserted.

## 6. Conclusion

EF measurement noise (SD ~5–8 EF units; MDC ~9–12 for 2D) is comparable to or exceeds
the 9-point HFmrEF band, misclassifying roughly a third of mid-band patients and up to
half near the edges. But the consequences are asymmetric: SGLT2 inhibitors work across
the EF spectrum, so the HFmrEF↔HFpEF boundary is therapeutically forgiving, while the
HFmrEF↔HFrEF (≤40%) boundary gates Class-I GDMT and devices. Confirmatory,
high-reproducibility imaging should be targeted to the **lower** threshold, where
misclassification actually changes care.

---

## References

1. McDonagh TA, Metra M, Adamo M, et al. 2021 ESC Guidelines for the diagnosis and treatment of acute and chronic heart failure. *Eur Heart J.* 2021;42(36):3599–3726. PMID: 34447992. doi:10.1093/eurheartj/ehab368.
2. Bozkurt B, Coats AJS, Tsutsui H, et al. Universal definition and classification of heart failure. *Eur J Heart Fail.* 2021;23(3):352–380. PMID: 33605000. doi:10.1002/ejhf.2115.
3. Thavendiranathan P, Grant AD, Negishi T, et al. Reproducibility of echocardiographic techniques for sequential assessment of left ventricular ejection fraction and volumes. *J Am Coll Cardiol.* 2013;61(1):77–84. PMID: 23199515. doi:10.1016/j.jacc.2012.09.035.
4. Anker SD, Butler J, Filippatos G, et al. Empagliflozin in heart failure with a preserved ejection fraction (EMPEROR-Preserved). *N Engl J Med.* 2021;385(16):1451–1461. PMID: 34449189.
5. Solomon SD, McMurray JJV, Claggett B, et al. Dapagliflozin in heart failure with mildly reduced or preserved ejection fraction (DELIVER). *N Engl J Med.* 2022;387(12):1089–1098. PMID: 36027570.

---

*Data-integrity note.* PMIDs 34447992 (2021 ESC), 33605000 (Universal Definition), and
23199515 (Thavendiranathan) were verified by PubMed metadata match on 2026-07-04;
EMPEROR-Preserved (34449189) and DELIVER (36027570) are the same verified IDs used in the
Synthēsis SGLT2-HF v2 papers. The misclassification grid, SEM/MDC table, and the
therapeutic-consequence logic are emitted by `9-ef50-verify.py`. The v1 "60% remain
HFmrEF at repeat echo" claim (attributed to a source marked author-required in v1) was
**not** carried into v2 as a verified fact. **Build target:** `.docx` + figures via the
E156 host build (`outputs/journal-upgrades/build/9-ef50-v2/`); render the
misclassification heatmap (§3.1) and the therapeutic-asymmetry schematic (§3.3).
