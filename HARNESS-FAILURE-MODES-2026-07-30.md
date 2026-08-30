# ORCHESTRATION-HARNESS FAILURE-MODE CATALOGUE — 2026-07-30

**Scope:** the machine that runs the lanes, not the evidence the lanes produce.
**Companion:** [`GOVERNING-RULES-ADDENDUM-2026-07-30.md`](GOVERNING-RULES-ADDENDUM-2026-07-30.md)
— the proposed §9–§17 that encode the defending rules. **Both STAGED, merged nowhere, not pushed.**
**`GOVERNING-RULES.md` is unmodified.**

**Sourcing discipline.** Every row is traced. `[REC]` = durable record (repo artifact, git object,
or orchestrator memory file), cited. `[ORCH]` = orchestrator-reported this session and recorded at
`active-sessions-index.md` §LANE OPS, but **not independently corroborated by an artifact** — kept
as `[ORCH]` rather than promoted, per §16. **Nothing here is invented; two items are corrections to
what the session believed** (F-07, F-03) and are flagged as such.

---

## 0. The one-line diagnosis

**§1–§8 govern the evidence. Nothing governed the machine.** Ten of the twelve failures below are
invisible to the existing rules not because the rules are wrong but because **they have no slot for
a spawn, a context budget, a model family, a transport, or a second writer.** The addendum is the
slot.

And the recurring shape underneath, in one sentence:
**an acknowledgement was mistaken for a state** — a spawn result for a lane, a lane title for a
model family, a `__verdict` for the verdict, a `[PASS]` print for a check, a push for a deploy, a
recollection for a measurement.

---

## 1. THE CATALOGUE

### F-01 · Spawn acknowledgement ≠ spawn state ("timeout-but-created") `[ORCH]`
**Instance.** `start_code_task` returned an over-token-limit/timeout result **and created the lane
anyway**. Re-firing on the failure-reading yields two lanes on one brief.
**Generalisation.** *Any* creating call whose result is truncated, timed out, or errored may still
have succeeded. The tool result is evidence about the **call**, never about the **world**.
**Same family in the record `[REC]`:** `start_code_task` → `session_stale_relogin`
(`dispatch-lane-reachability.md`); *"a clean `create_scheduled_task` result does not prove the task
will run"* (`rules/lessons.md`).
**DEFENDING RULE → §9.** Confirm by enumeration (`list_sessions`) after **every** spawn; ⛔ never
re-fire without it; recover `session_id` from the saved tool-result JSON; duplicate-check is part of
spawning, not of cleanup. Fails closed if enumeration is unavailable.

### F-02 · Context mass is a liveness risk, not just a cost `[ORCH]`
**Instance.** 200+-turn lanes were bounced by API 529s while **fresh small-context spawns went
through on the same brief at the same moment**. `active-sessions-index.md` already flags
`local_2f383c7e` as *"bloated 529-prone (avoid)"*.
**Generalisation.** The lane holding the most session knowledge is the least able to act on it.
Two corollaries: (a) hand off at a **clean commit**, so the successor inherits artifacts not turns;
(b) **a bounced bloated lane reports false vendor death** — the same shape as the recorded
*"liveness probe that queries the wrong model pool reports false death"* (`rules/lessons.md`).
**Tension resolved `[REC]`:** `orchestrator-is-the-folklore-vector.md` rule 4 says *don't interrupt
deep lanes* (best findings at turns 283/324/399). **Depth of reasoning is valuable; depth of
transcript is a liability.** Preserve the first by handing off artifacts.
**DEFENDING RULE → §10.** Fresh spawn per big step; hand off at a commit SHA; two 529 bounces = the
lane is DONE; per-lane liveness class in the index; never infer vendor outage without a fresh-lane
probe.

### F-03 · The orchestrator recalls where lanes fetch — folklore injection `[ORCH]`+`[REC]`
**Instance.** The orchestrator recalled **"44 contrasts"**. **Measured: 105.**
Verified this session against `outputs/hfref_league_export.json` (commit `53f83cc9e`):
`estimable_pairs: 105` · `contrasts_in_data: 30` · `nodes_in_network: 15` · `trials: 28` ·
engine `R 4.6.0 / netmeta 3.6.1`. A wrong EMPEROR-Reduced/HR premise entered a brief the same way.
**Generalisation `[REC]`.** Standing and measured: *"The lanes FETCH; I RECALL; I am UPSTREAM of all
of them"* — ~13 corrections in one session, **none self-caught**
(`orchestrator-is-the-folklore-vector.md`). Aspirational rules failed within the hour; the
mechanical tag-every-number rule caught two errors within hours.
**DEFENDING RULE → §16.** The POINTER RULE (no number in a brief without an artifact pointer);
`[MEASURED]`/`[INHERITED]`/`[RECOLLECTION-VERIFY]` tags; ⛔ never put a recalled specific into a
brief as fact; verify lane state before reporting it; report the orchestrator's own correction rate.

### F-04 · A lane's label is not its model family `[ORCH]`+`[REC]`
**Instance.** A gate lane **titled "Codex" was running Claude** — a §1 cross-family gate recorded as
satisfied while it was same-family.
**Generalisation.** Title, binary name, and seat name are labels. **Three prior instances of the
same error in the record `[REC]`:** *"routing a second CLI to Claude models collapses the panel to
one family — a failure mode that has already occurred"* (`IMPROVEMENT-HARNESS-2026-07-18.md` S12);
*"two Codex seats = more THROUGHPUT … NOT a second vendor family"*
(`rapidmeta-freeze-coordination.md`); agy declared dead by a probe against its persisted **Claude**
default while its Gemini pool was alive (`rules/lessons.md`).
**Precedent done right `[REC]`:** *"the probe was required to name its own family"*
(`AGY-FINAL-GATE-HFREF-2026-07-20.md`); *"Liveness proved by a real exec that named its own model
family"* (`ACS-ANTIPLATELET-NMA-2026-07-19.md`).
**DEFENDING RULE → §12.** ⛔ A gate lane must NAME ITS OWN FAMILY from a real exec before its
findings count; header records `vendor / model-id / family`; unverified cross-family pass is **VOID**;
family-neutral checks are honest but may never be reported as a cross-family pass.

### F-05 · One verdict surface is never all the verdict surfaces `[REC]`
**Instance.** HFrEF AUTO app live on `main` 2026-07-29: `window.__verdict` honest (`"UNCERTAIN"`,
28 trials, *"absence of findings … is absence of testing"*); a green badge at ~L1188 asserted
`INTERNAL CHECKS PASSED · Trials: 2 · Multi-source audit completed` — stale boilerplate, stale count,
self-contradictory within itself. **The gate read only `__verdict` and passed the app.** A genuine
cross-family (agy/Gemini) pass caught it; the gate and every same-family Claude review missed it.
(`rapidmeta-second-verdict-badge.md`; fixed at `b02990a02`, `9a2cdff58`.)
**Generalisation.** §7 at artifact level: **the machine-readable verdict and the human-visible
attestation are two surfaces; a gate that reads only the honest one certifies the dishonest one by
omission.** The reader sees the badge.
**DEFENDING RULE → §11.** Enumerate all verdict surfaces; grep **both** (`__verdict` **and**
`CHECKS PASSED / Trials: N`); disagreement = BLOCK; ⛔ no new surface without a same-commit gate
update; mutation test required; inherited boilerplate is UNEARNED by default.

### F-06 · A transport can silently truncate the payload `[REC]`
**Instance.** **PowerShell 5.1 silently truncates the agy prompt at the second embedded quote-pair**,
with `--add-dir` correct. The adversary answers a fragment; the fragment scores as a pass.
(`correcting-adversary-forgery-yields-finding.md`: *"invoke agy via BASH and prove the whole prompt
arrived with a marker test, or early passes are VOID."*)
**Generalisation.** A silent transport failure is **indistinguishable from a weak adversary** — and
weakness is exactly what §1 tells us to expect from a failed gate, so it hides in the one place we
are trained not to question. Related recorded traps: `agy --print` ignores `--model`; a heredoc
failure returns exit 2 / exit 0 zero-bytes and mimics a host defect — **read `cli.log`, never the
exit code**.
**DEFENDING RULE → §13.** ⛔ BASH only; **MARKER TEST** echoed in the adversary's first line or the
pass is VOID; blind-retrieval test for corpus claims; verbatim source quotes (never paraphrase);
four transport fields in every gate header.

### F-07 · In-repo self-checks attest to themselves `[REC]` — ⚠️ **with a correction**
**The standing principle, earned `[REC]`.** `IMPROVEMENT-HARNESS-2026-07-18.md` S8 —
*"The gate architecture is dominated by gates that can only pass"* — eight defects tabulated,
including `"Regression check PASS" at 0/1522 ok` (no `sys.exit(1)`) and `push ≠ deploy`.
⚠️ **CORRECTION.** The session note *"the repo pre-push git hook is THEATER (always PASS)"* `[ORCH]`
does not survive contact with the artifact. Checked 2026-07-30:
- `F:\rapidmeta-finerenone\.git\hooks\` has **no pre-push hook at all**; E156's is Sentinel's, which
  **does** fail closed (it even blocks a bypass log pointed at a discard target).
- `scripts/regression_check.py` **can fail today** — `return 1` on failing signals,
  `sys.exit(main())` — fixed at `552c1112d` (2026-07-18, *"make five gates able to fail"*).
- **What is still true:** `from playwright.sync_api import sync_playwright` (L181) is **unguarded**
  → `ImportError` mid-run; and the script has a **third exit code** (`return 2`, environment
  failure) that a caller testing `==0` / `!=1` reads as its opposite.
⇒ **Policy unchanged, instance re-scoped.** The theater case is historical; what is live is a
**trinary exit code and a crashable import**. Recording that precisely is F-03's rule applied to our
notes about ourselves.
**DEFENDING RULE → §14.** A self-check is evidence only with a **passing mutation test**; gates must
be binary at the boundary and any third state named in the caller and excluded from success; check
dependencies before claiming scope; `pipefail`; verify scope from what it globs; **push ≠ deploy**.

### F-08 · Concurrent writers on a shared file/ref `[REC]`
**Instance A — the collision.** Two lanes ran the **same gate-review brief, unannounced, twice**.
`CODEX-GATE-REVIEW-2026-07-23.md` watched `clone_contamination_gate.py` change under it mid-review
(27 441 B → 29 074 B, **crashing with `NameError: REGISTRY_LITERALS is not defined`** → 32 417 B) and
**stood down without writing**; `…-LANE-2.md` was the live editor and applied 14 fixes. Each lane
found a defect the other missed. *The split was lucky, not designed.*
**Instance B — the publish `[ORCH]`.** Concurrent lanes on the same branch produced an uncontrolled
publish: `398ae1047` (*"publish the HFrEF GDMT network NMA and link it from the landing page"*,
07-29 13:44) is an ancestor of `main`; `main == origin/main == b02990a02`.
**Instance C — the save `[ORCH]`.** The **fetch-guardrail** (*"confirm `origin/main == EXPECTED`
else STOP"*) **prevented a concurrent-lane double-push.** The only control in this catalogue with a
demonstrated save — which is why it is promoted from tactic to rule.
**DEFENDING RULE → §15.** Single writer per file **declared before the first write** in
`SHARED-LANE-NOTES.md`; detect collisions mechanically via `(size, mtime, md5)` re-check immediately
before writing, and pin findings to a snapshot hash; ⛔ **fetch-guardrail mandatory before any push**;
push stays Mahmood-only unless he authorises that specific push; **a landing-page link is a publish,
not a fix**, and needs the §1 gate plus an explicit go.

### F-09 · A cross-family gate that returns nothing has FAILED `[REC]`
**Standing (§1), reinforced this session.** The cross-family gate caught the false-green badge (F-05)
that the contamination gate and every same-family pass missed. And its weak-gate corollary fired
live: agy **tried to downgrade our over-claim finding after hearing our framing** — per the rule the
downgrade FAILED and the floor held (`rapidmeta-second-verdict-badge.md`).
**DEFENDING RULE.** §1 + §12 (family verified) + §13 (transport proven). **Expect the gate to move
you further from publishable; a pass that moves you toward it is a weak gate.**

### F-10 · The adversary forges in five classes — and correcting it is a GENERATOR `[REC]`
**Standing (§3a):** identifiers, quantities, quotations, attributions, **procedure-claims**. This
session added the payoff: **correcting the over-claim to source produced the finding neither side
had.** Gemini's false *"the retained unverified trials pull AWAY from the null"* (real: GALACTIC-HF
RR 0.998, Val-HeFT 1.018, Vizzardi 1.000) → correcting it exposed the symmetry violation in F-11.
Also recorded: agy passed blind retrieval 3/3 **while** fabricating its procedure —
**capability and honesty are separate axes.**
**DEFENDING RULE → §17.2.** Don't merely reject a forgery: **correct it to source and read what the
correction shows.**

### F-11 · An eviction rule applied to one row is not a rule `[REC]`
**Instance.** *"Unverified per-arm all-cause deaths + identical-counts ⇒ quarantine"* was met by
**three** trials — CARMEN (14/14/14, 572), GALACTIC-HF (1078/1078, 8232), Vizzardi (8/8, 130) — and
applied to **one**. Fixed at `402ec8811` (*"symmetric quarantine (3 trials) + CO-PRIMARY re-fit"*)
and `53f83cc9e`. The same fact cuts both ways and **both were reported**: it is the strongest
evidence of an inconsistent standard *and* the strongest refutation of a p-hacking charge
(~13,372 near-null unverified patients retained vs 572 removed).
**DEFENDING RULE → §17.1.** Run the eviction predicate across the **whole ledger**; assert
acted-on set == matched set, or name on the record why each unacted match falls short.

### F-12 · A deletion that moves results toward significance needs both fits, not a caveat `[REC]`
**Instance.** Quarantining CARMEN (RR≈1.00 on every edge) raised CI-excludes-1 **12→17** and pushed
two contrasts into nominal significance **on a provenance decision alone**. The app shipped only the
removed-fit ⇒ rated `DISCLOSED-BUT-INSUFFICIENT`. Related: `VERIFIED_FULL` was **overloaded** —
SPICE's `6/179, 3/91` were uniquely **back-inferred from rounded percentages**, not read verbatim
like CIBIS-II's *"156 vs 228"*.
**DEFENDING RULE → §17.3/§17.5.** Any inclusion decision that raises the count of significant
contrasts ⇒ **render both fits co-primary, side by side**; prose does not discharge it. And a
provenance tier that covers two different acts of knowing gets **split**, because it will be read as
the stronger one.

---

## 2. SUMMARY TABLE

| # | Failure mode (generalised) | Source | Defending rule | Can it fail? |
|---|---|---|---|---|
| F-01 | Spawn ack ≠ spawn state | `[ORCH]` | §9 confirm-by-enumeration | yes — no `list_sessions` ⇒ blocked |
| F-02 | Context mass = liveness risk | `[ORCH]` | §10 fresh spawn / hand off at commit | yes — 2 bounces ⇒ lane DONE |
| F-03 | Orchestrator recall enters briefs as fact | `[ORCH]`+`[REC]` | §16 pointer rule + tags | yes — untagged number ⇒ reject brief |
| F-04 | Lane label ≠ model family | `[ORCH]`+`[REC]` | §12 family named by real exec | yes — unnamed ⇒ pass VOID |
| F-05 | Second verdict surface unchecked | `[REC]` | §11 grep both, assert agreement | yes — disagreement ⇒ BLOCK |
| F-06 | Transport silently truncates prompt | `[REC]` | §13 bash + marker test | yes — no echo ⇒ pass VOID |
| F-07 | Self-check attests to itself | `[REC]` | §14 mutation test + binary boundary | yes — no mutation test ⇒ not reportable |
| F-08 | Concurrent writers / uncontrolled publish | `[REC]`+`[ORCH]` | §15 single writer + fetch-guardrail | yes — `origin/main` ≠ EXPECTED ⇒ STOP |
| F-09 | Weak/absent cross-family gate | `[REC]` | §1 + §12 + §13 | yes — empty return ⇒ FAILED pass |
| F-10 | Adversary forgery (5 classes) | `[REC]` | §3a + §17.2 correct-to-source | yes — unverified claim ⇒ rejected |
| F-11 | Asymmetric eviction | `[REC]` | §17.1 whole-ledger predicate | yes — set mismatch ⇒ FAIL |
| F-12 | Significance-increasing deletion shipped alone | `[REC]` | §17.3 co-primary render | yes — single fit ⇒ BLOCK |

---

## 3. DISPATCH PLAYBOOK — many parallel truth-gated threads without collisions

Written for the live configuration: **five parallel threads** (HFrEF NMA, Malaria NMA, Cardio
upgrade, Comm-disease/Africa upgrade, harness self-improvement), each ending in a cross-family gate
and Mahmood's go. Source: `active-sessions-index.md`; `cluster-harness-northstar.md`
(*"Dispatch is the single control plane… vendor lanes are stateless workers"*).

### 3.1 The five preconditions, before any thread is spawned
1. **Ownership map.** Each thread declares owned paths / repo / branch in `SHARED-LANE-NOTES.md`
   **before its first write**. Overlap is resolved *now*, not on collision.
2. **Reachability routing** (`dispatch-lane-reachability.md`): F:\E156-only Python/PubMed work →
   `start_task`; laptop-native, R/netmeta, SSH, agy → `start_code_task` on the right host, or Mahmood.
   **Routing a lane to a capability it cannot reach produces an honest-looking null.**
3. **Brief hygiene (§16).** Pointers, not values. Every number tagged. No recalled specifics.
4. **Expected refs.** Each thread's brief carries `EXPECTED = <origin/main SHA>` for its repo.
5. **Family plan.** Which family gates which thread — `anthropic` produces, `openai` (Codex)
   bug-hunts code, `google` (agy-Gemini) re-derives. Two Codex seats ≠ two families.

### 3.2 The loop, per thread
```
SPAWN      → list_sessions CONFIRM (§9); duplicate-check the brief
BRIEF      → pointers only; EXPECTED SHA; owned paths; declared family plan
WORK       → single writer; (size,mtime,md5) re-check before each write (§15)
COMMIT     → clean, atomic; artifacts written; this is the hand-off unit (§10)
GATE       → cross-family: family named by real exec (§12) + transport marker (§13)
             + BOTH verdict surfaces (§11) + mutation-tested gates only (§14)
VERIFY     → correct every adversary claim to source (§3a/§17.2); symmetry sweep (§17.1)
STAGE      → PROPOSED; nothing merged
GO         → Mahmood explicit; fetch-guardrail origin/main==EXPECTED else STOP (§15)
```

### 3.3 Collision avoidance — the four hard ones
- **One writer per file, ever.** Not "coordinate"; **one**. The 2026-07-28 review is the model: it
  saw the file moving, **stood down**, and staged its patch keyed to **function names** rather than
  line numbers *because the lines were moving*.
- **Branch per thread**, and `main` is written by exactly one lane at a time. A landing-page link is
  a publish (§15.5).
- **Fetch-guardrail is not optional** — it is the only control here with a demonstrated save.
- **Snapshot-pin every finding** (`md5`), so a report stays valid when the file moves under it.

### 3.4 Orchestrator turn discipline
- **Route instructions; don't narrate.** Elaborating messages to a deep lane are waste and can
  derail it (`orchestrator-is-the-folklore-vector.md` rule 4).
- **Prefer a fresh lane over a long one** for each big step (§10) — this is now also *how you avoid
  529s*, not only how you save context.
- **Verify lane state before reporting it** (§16.4). Lanes have been reported running while stopped.
- **Keep the session index current**: id, brief, branch, `EXPECTED`, liveness class
  (`LIVE`/`SUPERSEDED`/`BLOATED-AVOID`).
- **Report the orchestrator's own correction rate at session end** (§16.5).

### 3.5 What a thread must produce to be counted done
A commit SHA · both verdict surfaces agreeing · a gate report naming its adversary's **family**,
**transport**, and **marker/retrieval results** · a symmetry sweep on any eviction · co-primary fits
for any significance-increasing decision · everything **staged PROPOSED**, nothing merged, nothing
pushed without an explicit per-push go.

---

## 4. MEMORY-CONSOLIDATION SUGGESTIONS

Reviewed: the 64 files in the orchestrator memory dir + `MEMORY.md`. Five concrete items; **all are
proposals — no memory file was modified by this pass.**

### M-1 ⭐⭐ Promote LANE OPS out of `active-sessions-index.md` into its own durable memory
`active-sessions-index.md` is explicitly **point-in-time** (*"verify a lane is still live via
list_sessions before relying on it"*) and it is where the **durable** operational rules currently
live — the six-part LANE OPS block is the sole source for F-01, F-02, F-04, F-06(part), F-08. **A
volatile file is holding permanent knowledge**; the next session index rewrite deletes it.
→ **Create `lane-ops-protocol.md`** (type `feedback`) holding the spawn-confirm, context-budget,
family-verification, transport, and push-guardrail rules, linked as `[[lane-ops-protocol]]`. Leave
the *session ids* in the index, where they belong.

### M-2 ⚠️ Two stale headline states about vendor availability
- `codex-bug-finding.md` leads with 🔴 *"Codex is OUT UNTIL 25 JULY — credit-dead"*. **Codex ran live
  on 2026-07-28** as `gpt-5.5` on the gate review (`CODEX-GATE-REVIEW-2026-07-23.md` ×2, openai
  family). The red banner is now the most prominent false claim in that file.
- `agy-gemini-pool.md` leads with *"With Codex out till 25 July, agy-GEMINI is the SOLE cross-vendor
  decorrelation source"* — same stale premise; **three families are live**.
→ Rewrite both leads to the current state, and keep the *durable* content (two pools; route to
Gemini; probe the pool you intend to use; Codex is best at bug-finding; two Codex seats ≠ two
families).

### M-3 ⚠️ `MEMORY.md` index line contradicts `GOVERNING-RULES.md`
The index line for `structural-df-not-data` still reads *"Report information-gain (CIBIS-III 5.3×)"*.
**That bare ratio was WITHDRAWN** — `GOVERNING-RULES.md` §5 / `WITHDRAWALS-LEDGER.md` X-3: it is
×5.32 on the design-level estimate but ×3.37 against all direct ACEI-vs-BB evidence; *"state the base
or do not state the number."* An index line is exactly the surface a future lane will quote.
→ Amend to *"report information-gain **with its base** (bare ratios withdrawn, X-3)"*.

### M-4 `rapidmeta-freeze-coordination.md` is 80% expired lock text
The freeze lifted 2026-07-11; the file is still dominated by the historic lock. Its **durable**
content is three rules: (a) `git fetch` first, rebase onto Mahmood's pushes, never force over them;
(b) two Codex seats = throughput, not a second family; (c) single-writer discipline on rapidmeta.
→ Retitle around the durable rules (candidate: `repo-write-coordination.md`), demote the lock text to
a dated footnote, and link `[[lane-ops-protocol]]`.

### M-5 Overlapping adversary memories — keep both, but state the split in one line each
`adversary-forgery-five-classes.md` (the five classes) and
`correcting-adversary-forgery-yields-finding.md` (correct-to-source is a *generator*) genuinely say
different things, but their descriptions overlap enough that a recall pass may fetch only one.
→ One clarifying clause each: *"…what the adversary forges"* vs *"…what to DO with a forgery."*
Same treatment for `rapidmeta-second-verdict-badge.md`, whose lane-ops crumbs move to M-1.

**Also noted, not proposed as a change:** there are **two memory stores** in play — the orchestrator
store (`…/agent/memory/`, 64 files) and the project store
(`%USERPROFILE%\.claude\projects\F--E156\memory\`, e.g. `cross-regulator-divergence-footnote`,
`agy-native-corpus-reach-recipe`, `adversary-corpus-echo-failure`). They **overlap without
cross-linking** (agy invocation recipe exists in both; the corpus-echo lesson exists only in the
project store). Worth a deliberate decision on which store owns operational-harness knowledge — but
that is Mahmood's call, not a silent merge.

---

## 5. WHAT THIS PASS DID NOT DO

- **Did not modify `GOVERNING-RULES.md`.** The addendum is a separate file.
- **Did not modify any memory file.** §4 is proposals only.
- **Did not commit or push.** Both deliverables are `git add`-staged in `F:\E156` only.
- **Did not promote `[ORCH]` items to `[REC]`.** F-01, F-02, and instances B/C of F-08 rest on the
  orchestrator's own session note. Under §16 that is exactly the status they get. Corroborating them
  would need the dispatch transcripts, which were not read in this pass — **the honest residue.**
