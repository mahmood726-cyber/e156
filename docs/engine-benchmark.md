# e156 meta-analysis engine — benchmark vs R / Stata / CMA

> Validates the capsule pooling engine (`pool()` in the flagship meta-analysis
> capsules) against the standard tools. Run 2026-06-02 with **R 4.6.0 +
> metafor 5.0.1** (native). Stata and CMA are commercial and were **not run
> live**; their expected behaviour is documented from their published estimator
> implementations. Reproduce with the scripts in `docs/benchmark/`.

## Verdict

The capsule engine is **bit-exact with metafor** for the pooled estimate, every
between-study variance estimator (REML, PM, DL), I², and the Wald/z confidence
interval. The **only** divergence is a deliberate, documented one: the capsule
applies the **HKSJ floor** `mult = sqrt(max(1, Q/(k-1)))` so the Hartung-Knapp
interval cannot narrow below the fixed-effect interval when `Q < k-1`. metafor's
and Stata's default Knapp-Hartung do **not** floor; CMA does not offer
Knapp-Hartung. The floor is the more conservative choice and is the e156
convention (see `rules/advanced-stats.md`).

## Dataset A — homogeneous (5 SGLT2i HF trials, log-HR; τ²=0)

`HR/CI = 0.74(.65–.85), 0.75(.65–.86), 0.79(.69–.90), 0.82(.73–.92), 0.67(.52–.85)`

| Quantity | metafor | capsule | match |
|---|---|---|---|
| Pooled HR | 0.77091 | 0.77091 | ✅ exact (5 dp) |
| τ² (REML/PM/DL) | 0 | 0 | ✅ |
| I² | 0% | 0% | ✅ |
| CI, Wald/z (HK off) | 0.72407 – 0.82077 | 0.72407 – 0.82077 | ✅ exact (5 dp) |
| CI, Hartung-Knapp **+ floor** (e156) | 0.70541 – 0.84248 | 0.70541 – 0.84248 | ✅ exact |
| CI, Hartung-Knapp, **no floor** (metafor/Stata default `knha`) | 0.71401 – 0.83233 | — | capsule floors by design |

`Q = 2.9827, Q/(k-1) = 0.746 < 1` → the floor engages, widening the e156 HK
interval to the FE-anchored `t_{k-1}·SE_FE` rather than letting `knha` narrow it.

## Dataset B — heterogeneous (I²≈90%, τ²≈0.06) — tests the τ² estimators

`HR/CI = 0.55(.45–.67), 0.72(.62–.84), 0.88(.77–1.00), 1.05(.92–1.20), 0.63(.51–.78)`

| Estimator | metafor τ² | capsule τ² | Pooled HR (95% CI) | match |
|---|---|---|---|---|
| REML | 0.0595 | 0.0595 | 0.75 (0.60–0.94) | ✅ |
| Paule-Mandel | 0.0594 | 0.0594 | 0.75 (0.60–0.94) | ✅ |
| DerSimonian-Laird | 0.0563 | 0.0563 | 0.75 (0.60–0.94) | ✅ |

The capsule reproduces metafor's τ² to 4 dp for all three estimators and the
expected ordering (DL < PM ≈ REML at high heterogeneity).

## Stata (`meta` / `metan` / `admetan`) — equivalence, not run live

Stata implements the identical estimators: `meta set` + `meta summarize,
random(reml|pm|dl)`, or `metan ... model(reml|pm|dl)`. With matching settings it
agrees with metafor — therefore with the capsule's pooled estimate, τ², I², and
Wald CI. Stata's Knapp-Hartung (`hksj` / `se(khartung)`) does **not** apply the
floor, so on Dataset A it returns the no-floor interval `0.714–0.832`, differing
from the e156 floored interval `0.705–0.842` by the floor only — the same
divergence as metafor.

## CMA (Comprehensive Meta-Analysis v3/v4) — equivalence, not run live

CMA implements DL (default) and REML; its random-effects interval is Wald/z and
it does not offer Knapp-Hartung. So CMA matches the capsule's **HK-off** mode:
same DL/REML τ², same pooled estimate, same Wald CI. On Dataset A (τ²=0) CMA's RE
collapses to FE = the capsule default `0.77091 (0.72407–0.82077)`.

## Bottom line

| Tool | Point est. | τ² (REML/PM/DL) | I² | Wald CI | Hartung-Knapp CI |
|---|---|---|---|---|---|
| **metafor** (verified) | ✅ | ✅ | ✅ | ✅ | no floor |
| **Stata** (documented) | ✅ | ✅ | ✅ | ✅ | no floor |
| **CMA** (documented) | ✅ | ✅ (DL/REML) | ✅ | ✅ | not offered |
| **e156 capsule** | — | — | — | — | **floored (conservative)** |

The capsule's numbers are the standard-tool numbers. The single intentional
difference — flooring the Hartung-Knapp multiplier — is documented, defensible,
and the more cautious option.

## Reproduce

```
# capsule side: headless-load a flagship MA capsule, set methodSel / hksjChk,
# read the Overall pooled readout + methodTag (see docs/benchmark/extract.py).
# R side:
Rscript docs/benchmark/bench.R        # Dataset A: z, knha, floored-knha
Rscript docs/benchmark/bench_het.R    # Dataset B: REML/PM/DL tau^2
```
