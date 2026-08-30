# Workbook provenance record — entry `AfricaRCT`

**Written 2026-08-30 by an automated audit of `rewrite-workbook.txt`. Read-only finding.
Nothing was restored, reverted or chosen. Both versions are reproduced verbatim
from the git blobs so the author can decide from the text rather than from a
summary.**

---

## What happened

Commit `b94f34dbdd7d` (2026-05-06 12:46:12 +0100, mahmood789) replaced the `YOUR REWRITE` body of entry
`AfricaRCT` with prose on a different subject. Its message says:

> workbook: normalize all entry denominators to current total (678)

and its body describes a mechanical sweep normalising `[N/<various>]` headers to
`[N/678]` across 669 entries. **A denominator sweep has no reason to touch a
body.** The commit changed one file with 762 insertions and 675 deletions, which
is the shape in which a single substantive edit is invisible.

The substitution **stands at HEAD today** — the current text is the replacement,
not the original.

## Why it was not caught

`P0-workbook-rewrite-touched`, the gate that exists to block exactly this,
matched the literal `"YOUR REWRITE:"` while this workbook writes
`"YOUR REWRITE (at most 156 words, 7 sentences):"` 1,864 times. It therefore
computed protected ranges for **11 of 1,875 blocks (0.6%)** — 65 of 122,369
lines — and reported green over that sliver. The gate and the substitution are
one finding: *the protection was never watching the thing it named.* Fixed
2026-08-30; it now covers 1,875 of 1,875.

## Audit of the whole file, for context

47 protected-region events across 7 of the 73 commits that touch the workbook:

| n | state |
|---|---|
| 38 | the author's text is still present in a `YOUR REWRITE` block at HEAD — bookkeeping churn from renumbering sweeps, nothing lost |
| 7 | entries removed by `4595d7a8`, whose message names every removal (2 private + 5 published-to-journal) |
| 1 | `CochraneDataExtractor` — removed in that same commit, but its text survives at HEAD only inside a `CURRENT BODY`, not a `YOUR REWRITE` |
| **1** | **this one — the only substitution** |

**6 of the 7 commits changed protected text under a message describing
something else.** On the stricter reading — the message must name the protected
field — it is 7 of 7.

---

## VERSION A — before `b94f34dbdd7d` (146 words)

Present in the repository at commit `633b92067e59`.

```
How inequitably are clinical trials distributed across Africa relative to its disease burden and population share? We queried the ClinicalTrials.gov API v2 for all registered interventional RCTs from 2000 to 2026 covering Africa, Europe, China, India, and South America. A 57-dimension audit applied economic indices including Gini and Herfindahl, network entropy, Benford digit screening, and methodological rigor lenses to trial metadata across therapeutic areas. The Clinical Coverage Index for mental health was 15.0 (95% CI 12.1 to 18.3) and secondary care delivery reached 48.6, indicating Africa hosts a fraction of the trials its burden warrants. Per-country aggregation revealed that continent-level API queries undercount African trials by approximately twofold compared with summing individual nation results. Multi-dimensional inequity auditing exposes structural gaps in trial distribution invisible to simple count comparisons. The analysis relies on ClinicalTrials.gov metadata only and cannot capture trials registered solely in WHO ICTRP partner registries.
```

## VERSION B — after `b94f34dbdd7d`, and the text at HEAD today (135 words)

```
Can we estimate clinical trial transportability in Africa without assuming no unmeasured confounding? We used Proximal G-Computation to compute a structurally unbiased Causal Transportability Index (CTI) for 54 African nations across major non-communicable diseases. The framework uses Road Safety compliance and Neonatal Mortality as negative control proxies to isolate latent structural infrastructure friction from trial participation signals. Across Heart Failure and Oncology cohorts, the CTI identified high-transportability site opportunities in nations currently lacking local evidence participation. Sensitivity audits against alternative governance proxies demonstrated high model stability with a Pearson correlation of 0.99 (95% CI 0.98 to 0.99). This framework allows African nations to quantify the HTA "Sovereignty Gap" and rigorously negotiate for local clinical research investment. The model relies on macro-level WHO data and cannot capture the protocol-specific nuances of individual clinical trial site infrastructure.
```

---

## Status

**Undecided, deliberately.** Which of these is the author's intended entry for
`AfricaRCT` is a question about his writing, and it is his to answer. This file
exists so that answering it does not require a git archaeologist.

Nothing here modifies `rewrite-workbook.txt`.
