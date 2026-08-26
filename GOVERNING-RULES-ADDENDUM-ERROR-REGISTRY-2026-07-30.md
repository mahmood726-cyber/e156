# GOVERNING RULES — ADDENDUM §18: THE ARTIFACT ERROR REGISTRY

**Status:** PROPOSED · STAGED · **`GOVERNING-RULES.md` is unmodified** · nothing merged, nothing pushed.
**Date:** 2026-07-30

**Companions.**
- [`GOVERNING-RULES-ADDENDUM-2026-07-30.md`](GOVERNING-RULES-ADDENDUM-2026-07-30.md) — §9–§17, the
  **orchestration harness** (spawns, context budget, model family, transport, second writers).
- [`HARNESS-FAILURE-MODES-2026-07-30.md`](HARNESS-FAILURE-MODES-2026-07-30.md) — F-01…F-12, the
  failures those rules defend against.
- **`F:\rapidmeta-finerenone\RAPIDMETA_ERROR_REGISTRY.md`** — the registry this section makes
  mandatory. **67** error types, each with a detector that can fail.
- **`F:\rapidmeta-finerenone\RAPIDMETA_ERROR_SWEEP.{md,json}`** — the corpus-wide prevalence matrix.
- **`F:\rapidmeta-finerenone\assets\js\rapidmeta-guards.js`** — the **20** fail-closed engine guards.
- **`F:\rapidmeta-finerenone\RAPIDMETA_BATCH_PLAN.md`** — the Phase-1 engine patch (909 root apps) and the 24 gated Phase-2 data batches.
- **`F:\rapidmeta-finerenone\tests\fixtures\rapidmeta_error_fixtures.json`** — 3 source-verified worked examples.

---

## The one-line diagnosis

**§1–§8 govern the evidence. §9–§17 govern the machine that produces it. Nothing governed the
ARTIFACT.** Every rule above operates on a claim, a lane or a gate; none of them has a slot for a
*rendered app* — a badge, an outcome selector, a RoB sanitiser, a panel that should not have drawn.
The registry is that slot.

And the recurring shape underneath, in one sentence — the artifact-level twin of §9–§17's
*"an acknowledgement was mistaken for a state"*:

> **an internally plausible number was mistaken for a sourced one.**

Every one of the 67 types errs toward looking clean or looking deep. The arithmetic layer is
*perfectly* clean in the worst cases: RIFAPENTINE_TB recomputed its log-odds-ratio from a fabricated
2×2 to **Δ = 0.00e+00**, exactly, and its badge said checks passed. The pipeline is faithful; its
input is not.

---

## §18.1 · The registry is the checklist. Every app, every batch. ⭐⭐⭐

**RULE.** No app may be reported as upgraded, corrected, verified or release-ready until every
**STATIC** detector in `RAPIDMETA_ERROR_REGISTRY.md` has been run against its final file and every
firing has been dispositioned by id.

```
python scripts/rapidmeta_error_sweep.py --only RM-XXX      # per detector
python scripts/rapidmeta_error_sweep.py                    # corpus matrix
```

⛔ **A per-app report that names no registry ids has not run the checklist.** "Looks clean" is not a
disposition; `RM-F01: no finding` is.

**Fails closed:** if the sweep cannot parse an app's `realData`, that is a **finding about the app**
(recorded in the JSON `errors` block), not a clean result.

---

## §18.2 · A detector firing is a HYPOTHESIS, not a defect ⚠️⚠️

**RULE.** Every firing gets one of the five dispositions from the cardio recipe — *citation
corrected · claim withdrawn · re-sourced · quarantined · counts corrected* — each with its evidence.
**"Claim withdrawn" applies to your own audit's findings too, and must be recorded.**

The HFrEF pass withdrew **three of its five** findings on verification. SPICE "has no primary source"
was an artefact of searching on an acronym that never appears in the PubMed record; had it been
quarantined as the first audit proposed, the network would have lost its only between-trial loop.
The APIXABAN round-1 fix shipped **two manufactured explanations** of correctly-identified
manufactured numbers, and both were caught by the cross-family gate.

⛔ Never delete a row to resolve a firing. **Quarantine, never silent deletion** — retain it flagged,
with a stated reinstatement condition, and make the verifier **block if it is deleted rather than
flagged**.

---

## §18.3 · The engine guards are the fix; a per-app patch is not ⭐⭐⭐

**RULE.** Where the registry marks a type **base-engine-shared**, a per-app fix is a **workaround**
and must be labelled one. The fix is the guard in `assets/js/rapidmeta-guards.js`, and it must ship
with the seed that proves it can fail.

**35 of the 67 types are base-engine-shared, and 24 of them are fixed by one engine patch — see `RAPIDMETA_BATCH_PLAN.md` Phase 1.** `safeRob` alone silently downgraded **every**
Some-Concerns rating in **every** app that carries the sanitiser.

⛔ A guard without a passing entry in `tests/mutate_guards_selftest.py` is not evidence. Current
state: **119/119 unit tests pass; 14/14 re-seeded shipped defects are caught; the file restores
green.** This is §14 (mutation test) applied to the engine.

---

## §18.4 · N/A is not a pass, and a tested zero is not an untested one ⭐⭐

**RULE.** Every gate reports **PASS**, **FAIL** or **N/A with its reason**. A counter of `0` for a
gate that does not apply is a **BLOCK**, not a pass.

- GRIM on binary per-arm counts → **N/A** (no mean of a bounded integer scale to reconstruct).
  `P0_grim: 0` reads as a pass and must not ship.
- Benford below 30 digits → **UNDERPOWERED**. "Cannot test", not "no signal".
- Registry concordance on unregistered trials → **N/A**, with the covered fraction stated
  ("covers 9 of 27").
- Fragility index on an indirect contrast → **UNDEFINED**. State it is *unmeasurable*, not favourable.

**Running the gates does not earn a PASS.** It converts "untested" into "tested, with N findings".
Say which.

---

## §18.5 · Grep BOTH verdict surfaces — this is §11 at artifact level ⭐⭐⭐

**RULE.** Enumerate every verdict surface before reading one. Minimum three:
`window.__verdict` · the visible `#rapidmeta-integrity-badge` · the `realData` ledger's own trial
count. **Disagreement is a BLOCK.**

- Read the badge by a **balanced-`<div>` walk**, never a regex — a regex matches a prefix and
  silently leaves the rest.
- Replace a badge **wholesale**, never by patch-and-append. That is exactly how "Trials: 28" survived
  beside "27 trials", and how the 10-vs-14 internal-consistency-rounds pair shipped in **both**
  sentences of the same badge.
- **Read `reasons[]` first.** It often already names the bug: APIXABAN_ACS's own verdict object
  carried *"2 AACT outcome-direction divergence(s)"* while its badge rendered green over it.
  **The corpus's own audit output is more honest than its badges.**
- ⛔ No new verdict surface without a same-commit gate update.

---

## §18.6 · Estimand before arithmetic ⭐⭐⭐

**RULE.** No estimate enters a model without an explicit estimand tag, and the poolability test is an
**ALLOWLIST**. `"RR" !== String(d?.estimandType ?? "HR")` is a **denylist**, and a denylist is what
let a recurrent-event rate ratio into a hazard-ratio model and produced a spurious pooled 0.84.

- **≥2 SAME-estimand estimates or no pool.** Name the held-out trials **with their estimand** — not
  "no published HR", which is false when the trial has a published effect that simply is not a
  hazard ratio.
- A recurrent-event total is **not** a patient count. Render "N vs M total events" plus the published
  per-100-patient-year rates; a percentage of the randomised n is not a risk.
- **Peto output is an OR.** "Peto HR" is a contradiction.
- **Read `unitOfMeasure` before using any posted registry value.** `"percentage of participants"` is
  a proportion; `"percentage of participants/100-pt years"` is an incidence rate, and multiplying it
  by a denominator fabricates a count that exists in no document.
- **Bind arms by group TITLE, never by index.** ClinicalTrials.gov lists placebo first.

---

## §18.7 · Direction is derived, never asserted ⭐⭐⭐

**RULE.** Every outcome row carries an explicit **polarity** (`benefit` / `harm` / `neutral`), and
every direction word, NNT and NNH is computed from `polarity × effect`.

An OR < 1 on a **good** outcome (culture conversion, treatment completion) means the intervention is
**worse**. Pooling a good outcome and a bad outcome on one scale with no sign reconciliation is a
**P0** — and it happened, at RIFAPENTINE_TB, where the app computed correctly what it should not have
been computing at all.

**And the framing is part of the rule.** Any correction that moves a headline must say, in these
words: *"this is a provenance correction, not a result that got better or worse. The evidence did not
change. The app was wrong."* APIXABAN_ACS moved from a nominally significant **benefit** (OR 0.850)
to a nominally significant **harm** (OR 1.975) on a provenance decision alone.

---

## §18.8 · Machinery is gated on k and on estimand, and suppression is visible ⭐⭐

**RULE.** Every panel declares its threshold and prints an **on-panel reason** when suppressed.
Keep the forest plot and the pooled estimate; suppress the depth theatre.

Funnel/Egger/trim-fill **k ≥ 10** · Copas **k ≥ 15** · meta-regression **k ≥ 10** · subgroup
interaction **≥ 2 per subgroup** · TSA/RIS **k ≥ 5** · NMA surfaces **network required**, node-split
**closed loop required** · L'Abbé **binary only** · NNT **observed baseline risk required** ·
DerSimonian-Laird **inadmissible below k = 10** · τ²/I² **not interpretable below k = 3**.

**Suppression extends to every derivative of an invalid pool** — leave-one-out, Baujat, influence,
sensitivity, cumulative MA, conditional power, RoB-ME. *A leave-one-out of an invalid pool is exactly
as misleading as the pool.*

Where a panel is **not applicable** rather than under-powered, **remove it with a note that explains
the absence**, not a blank space.

---

## §18.9 · Protocol provenance: keep the mechanism, drop the attribution ⭐⭐⭐

**MAHMOOD'S RULING, and it cuts both ways.**

**KEEP.** A publicly-pushed, version-controlled protocol commit **is** a legitimate tamper-evident
protocol-provenance record, and on three axes it is **stronger** than a registry entry:
tamper-evident rather than only curated (git history is a Merkle chain — altering an earlier commit
changes every later hash, and once public, third parties hold the originals); the whole protocol
diffable line by line across its history rather than summarised as field-level revision notes; and
ungated — no third party decides whether or how quickly a protocol may be recorded.

**DROP, both of them.**
1. The **ICMJE attribution**. ICMJE has **no** systematic-review registration requirement at all —
   its 2005 mandate covers clinical trials. There is no such statement to cite.
2. The **literal PROSPERO-equivalence label**. It is a different mechanism with different properties,
   and the page must say what a registry has that git does not: custody by an independent
   institution, and the settled expectation of journals and reviewers in this field.

**STATE the caveat.** A commit's date field is author-settable, so **a commit date on its own proves
nothing**. The evidence is the **PUBLIC PUSH**. Two strengtheners, not to be conflated: an external
time anchor (RFC 3161 / OpenTimestamps) proves content existed by a given time independently of the
repo owner — worth adding, because GitHub's public events feed is not retained indefinitely; a
GPG/SSH-signed tag proves authorship and tree integrity, but the time inside a signature is
**self-asserted**. *Signing proves who and what; anchoring proves when.*

⛔ **DO NOT OVER-CORRECT.** The first ARNI fix deleted the mechanism outright and replaced it with a
flat "NOT prospectively registered" — throwing away a legitimate mechanism along with the false
claims attached to it. Guard **G11** now blocks the deletion as well as the attribution.

**And keep them separate.** For a review whose protocol was written alongside the analysis, the review
is **not** prospectively registered by any mechanism, git included. Reframing the mechanism must not
smuggle a prospective claim into a retrospective review.

---

## §18.10 · Corpus scope: never fix one app when the defect is corpus-wide ⭐⭐

**RULE.** Before fixing a defect in one app, run its detector across the corpus and **state the
denominator in the commit message**. A per-app fix to a corpus-wide defect leaves the corpus wrong
and the record misleading.

Measured scopes on record: `safeRob` — every app carrying the sanitiser · the sacubitril/valsartan
alias table — **526 apps**, 56 of them global-health · the `pooling-repair` scope-lock bypass —
corpus-wide · `paper-studio.js` `ensureAnalysisReady` — every app · SGLT2i contamination — 148 + 7 +
154 clones across three commits.

**And check the diff shape.** After any app edit, `git diff --numstat` must show a line count
proportional to the **edit**, not to the **file**. A CRLF/LF read-write mismatch turned a 2-line badge
edit into a **6341-line whole-file rewrite**, which would have made the 526-app remediation
unreviewable.

---

## §18.11 · Every batch ends where §1 and §9–§17 say it does

A registry pass is **not** a release. It ends exactly as §3.5 of the dispatch playbook requires:

> A commit SHA · both verdict surfaces agreeing · a gate report naming its adversary's **family**,
> **transport**, and **marker/retrieval results** · a symmetry sweep on any eviction · co-primary
> fits for any significance-increasing decision · everything **staged PROPOSED**, nothing merged,
> nothing pushed without an explicit per-push go.

Plus, from §18: **every registry id dispositioned**, **every N/A printed with its reason**, and the
**"still not done"** list written.

**Push ≠ deploy.** `main` is the deploy ref. Say "on GitHub, NOT live" whenever the pushed ref ≠ the
deploy ref.

---

## §18.12 · What §18 deliberately does NOT claim

- **The sweep is STATIC only.** Eleven registry types are SOURCE-class (they need a registry/PubMed
  lookup per trial) and two are RENDER-class (they need a browser). **A zero in the sweep is not a
  clean result for those types**, and any report that treats it as one is making the §18.4 error one
  level up.
- **Per-app source verification is not automatable.** Measured: `95 min + 20·k + 5·findings`,
  ~3–4 h/app at the corpus mean k = 3.6.
- **Nothing in the registry rests on a branch name.** An earlier draft recorded two entries as
  "branch reserved, no commits landed" (`fix/attr-cm-helios-nct`,
  `fix/incretin-hfpef-kccq-scope-lock`). Both branches had in fact advanced between the branch
  listing and the write-up, and the entries now cite the landed commits (`9e658033f`, `788156034`).
  **This is §16 firing on this very document**: a recalled branch state entered a draft as fact and
  was caught by re-reading the artifact. Recording it rather than silently correcting it is the rule.
