# GOVERNING RULES — PROPOSED ADDENDUM §9–§17 (ORCHESTRATION HARNESS)

> **STATUS: PROPOSED. STAGED, NOT MERGED, NOT PUSHED.**
> `GOVERNING-RULES.md` is **not modified by this file.** If Mahmood accepts, these sections
> append after §8 and before *Hard constraints*. Until then, §1–§8 are the only governing rules.
>
> **Why this file exists.** §1–§8 govern the *evidence*: what a trial is, what a df means, what an
> adversary may be trusted for. Nothing in them governs the *machine that runs the lanes* — how a
> lane is spawned, how big it may get, how it proves its own identity, how two of them avoid
> writing to the same ref. Every failure in `HARNESS-FAILURE-MODES-2026-07-30.md` is of that second
> kind, and each one was invisible to §1–§8 **because §1–§8 do not have a slot for it.**
>
> **Design constraint, taken from the record.** The orchestrator memory records the measured result
> that decides the form of every rule below:
> *"§0d is mechanical ('tag every number') → it CAUGHT TWO of my errors within hours. §0 is prose
> ('don't report our ceiling as the world's limit') → I violated it within an HOUR of writing it.
> ⇒ Every rule that asks me to be more careful is theatre. Only rules that force a LANE to check do
> anything."* (`orchestrator-is-the-folklore-vector.md`)
> **Therefore every rule below names a command, a grep, or a comparison that a lane executes and
> that can return FAIL. No rule below asks anyone to be more careful.**

**Source key.** `[REC]` = in the durable record (repo artifact, git object, or orchestrator memory
file), cited inline. `[ORCH]` = orchestrator-reported this session, recorded in
`active-sessions-index.md` §LANE OPS but not independently corroborated by an artifact — per §16
these are tagged, not laundered into fact.

---

## §9. SPAWN-CONFIRM PROTOCOL ⚠️⚠️
*(the "timeout-but-created" trap)*

**The failure.** `start_code_task` returned an over-token-limit / timeout result **and the lane was
created anyway.** The tool result reads as failure; the world contains a live lane. Re-firing on
that reading creates a **second lane on the same brief** — which is how the two-lane collisions in
§15 begin. `[ORCH]` — recorded at `active-sessions-index.md` §LANE OPS (b).

**Corroborating class in the record `[REC]`:** the spawn path is already known to fail in ways whose
error text does not describe the state — `start_code_task` returning `session_stale_relogin`
(`dispatch-lane-reachability.md`), and the standing lesson that *"a clean `create_scheduled_task`
result does not prove the task will run"* (`rules/lessons.md`, Ops/Deploy). Same family: **the
acknowledgement is not the state.**

**THE RULE — mechanical:**

1. **A spawn is not complete until it is CONFIRMED by enumeration.** After every spawn call —
   success, timeout, or error — the next action is `list_sessions`. The lane exists iff it appears
   there. **The spawn tool's return value is evidence about the CALL, never about the LANE.**
2. ⛔ **NEVER re-fire a timed-out or errored spawn without a `list_sessions` confirm first.**
   This is the single mechanical rule; everything else in §9 is recovery.
3. **Recovery of a lost `session_id`.** A timed-out spawn still writes its tool-result JSON. Recover
   from disk rather than re-firing:
   `find /sessions -name '<result-file>' | xargs python3 -c '...json.load...'` → read `session_id`.
   `[ORCH]`
4. **Confirm-before-brief.** No brief is sent to a lane whose `session_id` came from a failed call
   until that id has been matched against `list_sessions` output. A brief sent to a
   guessed/reconstructed id is a brief sent nowhere, and its absence is silent.
5. **Duplicate check is part of spawn, not of cleanup.** Before spawning onto any brief, grep the
   session list for a lane already on that brief. Two lanes on one brief must be a *decision*, never
   a *discovery* — the 2026-07-28 gate review discovered it twice
   (`CODEX-GATE-REVIEW-2026-07-23-LANE-2.md`: *"this is the second unannounced two-lane collision on
   this brief"*). `[REC]`

**How this rule can fail (it must be able to):** if `list_sessions` is itself unreachable, the
protocol FAILS CLOSED — do not spawn, do not re-fire, report the blocker. An unconfirmable spawn is
a blocked spawn, not an assumed one.

---

## §10. LANE CONTEXT BUDGET ⚠️⚠️
*(bloated lanes are bounced; fresh lanes get through)*

**The failure.** Large lanes (200+ turns) were repeatedly bounced by API 529s while **fresh
small-context spawns slipped through on the same brief at the same moment.** Context mass is
therefore not merely a cost — it is a **liveness risk**, and the lane holding the most session
knowledge is the one most likely to be unable to act on it. `[ORCH]` —
`active-sessions-index.md` §LANE OPS (a); the same index names lane `local_2f383c7e` as
*"bloated 529-prone (avoid)"*, i.e. the policy was already being applied ad hoc.

**Tension with the record, stated honestly `[REC]`:** `orchestrator-is-the-folklore-vector.md` rule 4
says *"Don't interrupt deep lanes. The session's best findings came at turns 283, 324, 399."*
**Both are true and they are not in conflict** once the distinction is drawn:
**depth of REASONING is valuable; depth of TRANSCRIPT is a liability.** The resolution is to preserve
the former across a fresh lane by handing off *artifacts*, not *turns*.

**THE RULE — mechanical:**

1. **Prefer a FRESH spawn for any big step.** A "big step" = a new sub-brief, a re-fit, a gate, a
   publish. Do not append it to a lane that has already done a big step.
2. **HAND OFF AT A CLEAN COMMIT.** A lane hands off only when its work is committed (or written to a
   named artifact) and the successor's brief cites **the commit SHA / file path**, never a summary of
   the predecessor's reasoning. This is the §16 pointer rule applied to lane succession: *an error
   cannot propagate through a value I never sent.*
3. **A lane that has been 529-bounced twice is DONE.** Do not retry it a third time. Commit or
   write out whatever is complete, spawn fresh from the artifact, and mark the old lane superseded
   in the session index. (Consistent with `rules/debugging.md` "stop at 3": the third attempt is an
   architecture signal, not a hypothesis.)
4. **The session index carries a per-lane liveness class**: `LIVE` / `SUPERSEDED` / `BLOATED-AVOID`.
   A lane is not re-briefed without reading that class first.
5. ⚠️ **Do not read a 529 as a vendor outage.** A fresh lane succeeding at the same moment refutes
   the outage reading. This is the same shape as the `lessons.md` liveness rule —
   *"a liveness probe that queries the wrong model pool reports false death"* — one level up: **a
   bounced bloated lane reports false vendor death.** Probe with a fresh small lane before declaring
   a vendor down. `[REC]`

---

## §11. BOTH-VERDICT-SURFACES GATE ⚠️⚠️
*(the gate checked the honest surface and missed the reassuring one)*

**The failure `[REC]`.** On the HFrEF AUTO app live on `main` 2026-07-29, `window.__verdict` (~L1123)
was honest — `"UNCERTAIN"`, `n_trials_seen: 28`, *"Absence of findings here is absence of testing,
not a clean bill."* — while a **green human-visible badge (~L1188)** asserted
`INTERNAL CHECKS PASSED · Fabrication-risk 0.275 · Trials: 2 · Multi-source audit completed`:
stale app-shell boilerplate, a stale trial count (2, not 28), and a self-contradiction inside itself
(`10` vs `14` rounds). **The contamination gate inspected only `__verdict` and passed the app.**
A genuine cross-family (agy/Gemini) pass caught it; the gate and every same-family Claude review
missed it. Source: `rapidmeta-second-verdict-badge.md`; remediated at commits `b02990a02`
(*"kill the false green integrity badge"*) and `9a2cdff58` (*"rewrite the badge wholesale; add
self-contradiction gate"*).

**THE GENERALISATION.** This is the §7 reporting-layer rule at the level of the artifact:
**a machine-readable verdict and a human-visible attestation are two surfaces, and the gate that
reads only the honest one certifies the dishonest one by omission.** The reader sees the badge.

**THE RULE — mechanical:**

1. **Enumerate the verdict surfaces of an artifact before gating it.** For a RapidMeta app that is
   at minimum: (a) the `window.__verdict` JSON, (b) the visible
   `CHECKS PASSED / Trials: N / audit completed` badge, (c) any headline/league-table caption
   carrying a count or a pass-word.
2. **The gate greps ALL of them and asserts AGREEMENT** on: pass/uncertain state, trial count `N`,
   rounds count, and risk figure. **Disagreement = BLOCK**, not warn.
3. ⛔ **No new surface may be added to a template without being added to the gate in the same
   commit.** A surface the gate cannot see is a surface that can go falsely green.
4. **Mutation test required.** Seed an app whose badge says `PASSED` while `__verdict` says
   `UNCERTAIN`, and assert the gate BLOCKS. Per §14 a gate without a passing mutation test is
   presumed non-functional.
5. **Boilerplate is guilty until re-derived.** Any attestation string inherited from a template
   clone is `UNEARNED` unless this artifact's own run produced it. Default state of an inherited
   badge is BLOCK.

---

## §12. MODEL-FAMILY VERIFICATION ⚠️⚠️⚠️
*(a lane titled "Codex" was running Claude)*

**The failure.** A gate lane **titled "Codex" was actually running Claude** — i.e. a pass recorded as
cross-family was same-family, and the mandatory §1 gate was **not satisfied while appearing to be.**
`[ORCH]` — `active-sessions-index.md` §LANE OPS (d).

**The record already contains this failure mode as a KNOWN one `[REC]`:**
`IMPROVEMENT-HARNESS-2026-07-18.md` S12: *"routing a second CLI to Claude models collapses the panel
to one family — **a failure mode that has already occurred**."* And
`rapidmeta-freeze-coordination.md`: *"two Codex seats = more THROUGHPUT … NOT a second vendor family.
Do NOT present a Codex×2 panel as heterogeneous consensus."* And `rules/lessons.md`: agy was declared
quota-dead by a probe that queried its **persisted default model** (a Claude pool) while its Gemini
pool was fully alive. **Three independent instances of one error: the label is not the family.**

**THE RULE — mechanical:**

1. ⛔ **A gate lane MUST NAME ITS OWN MODEL FAMILY in its output, produced by a real exec, before
   any of its findings are counted.** The lane title, the CLI binary name, and the seat name are all
   **labels** and none is evidence.
2. **The probe must be a real completion that echoes model + family**, not a status page, not
   `login status`, not a quota meter. Precedent already executed correctly:
   `AGY-FINAL-GATE-HFREF-2026-07-20.md` — *"a check that can only report 'alive' is not a check. So
   the probe was required to name its own family"*; `ACS-ANTIPLATELET-NMA-2026-07-19.md` —
   *"Liveness proved by a real exec that named its own model family."* `[REC]`
3. **The verdict header records the family triple**: `vendor / model-id / family`
   (`anthropic` · `openai` · `google`), and the **family must differ from the produced-work lane's
   family** or the pass is recorded as `SECOND-FAMILY-WITNESS: UNAVAILABLE` — a status the record
   already uses correctly (`LANE-STATE-BOARD.md`, `AGY-GEMINI-REDERIVE-3LANES-2026-07-19.md`).
4. ⛔ **A cross-family pass whose family was not verified at run time is VOID and must be re-run.**
   It may not be retro-labelled from the lane title.
5. **Family-neutral work is honest and must be labelled as such.** Deterministic arithmetic
   re-derivation and PubMed identifier lookup catch real error classes and require no second family
   — but they **do not decorrelate methodological judgement** and may never be reported as a
   cross-family pass (`AGY-GEMINI-REDERIVE-3LANES-2026-07-19.md`). `[REC]`

---

## §13. ADVERSARY TRANSPORT — agy VIA BASH, AND PROVE THE PROMPT ARRIVED ⚙️
*(a silently truncated prompt makes the gate a fiction)*

**The failure `[REC]`.** **PowerShell 5.1 silently truncates the agy prompt at the second embedded
quote-pair**, even with correct `--add-dir` ordering. The adversary then answers a *fragment* of the
brief, and the answer is scored as a pass. Recorded in
`correcting-adversary-forgery-yields-finding.md`: *"invoke agy via BASH and prove the whole prompt
arrived with a marker test, or early passes are VOID."*

**THE RULE — mechanical:**

1. ⛔ **Invoke agy from BASH, never from PowerShell.** (House rule already:
   `rules/lessons.md` — long prompts truncate; pass the prompt as an **argument**, not stdin;
   `--add-dir` at the **exact** directory; **never write "shell"/"grep"/"search"** in the prompt,
   even to forbid them, because that triggers the `command`-permission denial that mimics a host
   defect.)
2. **MARKER TEST — every pass, no exceptions.** Embed a unique marker near the **end** of the prompt
   (e.g. `TRANSPORT-MARK: <8-hex>`) and **require the adversary to echo it in its first line.**
   No echo ⇒ the prompt was truncated ⇒ **the pass is VOID**, re-run. This makes a transport failure
   *loud*, which is the entire point: it currently fails *silently*, and a silent transport failure
   is indistinguishable from a weak adversary.
3. **BLIND RETRIEVAL TEST — every corpus-level claim.** Ask for a specific string/value that is
   present in the corpus and **absent from the prompt**. Failure ⇒ its "I searched everything" is a
   procedure-claim forgery (§3a, fifth forgeable class). Note the recorded asymmetry: agy has passed
   retrieval 2/2 and 3/3 while *simultaneously* fabricating its procedure —
   **capability and honesty are separate axes.** `[REC]`
4. **Read `cli.log`, never the exit code.** A shell/heredoc failure returns exit 2 / exit 0
   zero-bytes and is indistinguishable from a host defect (§1). `[REC]`
5. **Quote source text VERBATIM into an adversary prompt.** A paraphrase is laundered back as
   apparent evidence (§3a: *"not enough evidence"* → *"insufficient evidence"*). `[REC]`
6. **Record the transport in the verdict header**: shell used, marker echoed Y/N, retrieval test
   n/n, `--add-dir` path. A gate report without these four fields is not a gate report.

---

## §14. INDEPENDENT VERIFICATION OVER SELF-CHECKS ⚠️⚠️
*(a repo's own gate is a claim, not a check)*

**The standing principle, already earned `[REC]`.** `IMPROVEMENT-HARNESS-2026-07-18.md` S8 —
*"The gate architecture is dominated by gates that can only pass"* — with a table of eight defects
that shipped past their own gate, including `"Regression check PASS" at 0/1522 ok | pre-push hook |
no sys.exit(1) — gate could not fail` and `push ≠ deploy | push success | pushed ref ≠ tracked ref`.
`rules/lessons.md`: *"A gate with no `sys.exit(1)` is verification theater — it can only delay, never
block."*

⚠️ **CORRECTION TO THE SESSION'S OWN NOTE — the artifact was checked and the claim needs re-scoping.**
`active-sessions-index.md` §LANE OPS (f) states *"The repo pre-push git hook is THEATER (always
PASS)."* Verified on disk 2026-07-30:
- `F:\rapidmeta-finerenone\.git\hooks\` contains **no pre-push hook at all** (E156 has one — Sentinel's,
  which does fail closed, including on a discard-target bypass log).
- `scripts/regression_check.py` **can fail today**: `return 1` on any failing signal, `sys.exit(main())`
  — fixed at commit `552c1112d` (2026-07-18, *"fix(gates): make five gates able to fail"*).
- **What is still true of that script:** (i) `from playwright.sync_api import sync_playwright` at
  L181 is **unguarded** — a missing Playwright raises `ImportError` mid-run; (ii) it has a **third
  exit code** — `return 2` for "environment failure, NOT reporting app results" — and any caller
  testing `== 0` or `!= 1` reads that third state as its opposite.
⇒ **The policy stands and the instance is corrected.** The theater instance is historical (2026-07-05,
0/1522); what is live is a **trinary exit code and a crashable import**. Recording it precisely is the
point — §16 applies to the orchestrator's notes about the harness exactly as it applies to its notes
about trials.

**THE RULE — mechanical:**

1. ⛔ **An in-repo self-check is EVIDENCE ONLY IF a mutation test shows it BLOCKING a known-bad
   input.** No passing mutation test ⇒ the gate is presumed non-functional and its PASS is not
   reportable. (Precedent done right: the 2026-07-28 gate review seeded a contaminated fixture —
   *"BLOCKED, both variants; clean control PASSES"*.) `[REC]`
2. **A gate must be BINARY at its boundary.** Any third state (`environment failure`, `skipped`,
   `unverified`) must be **named in the caller** and must **never** be counted in the success set.
   This is the `SKIP-as-pass` verdict lesson (`rules/lessons.md`): *a missing baseline is not a pass;
   encode that distinction in the verdict, not in a comment.*
3. **Every dependency a gate needs is checked BEFORE the gate claims scope.** An unguarded import in
   a gate is a gate that can die without a verdict. Import-check first, report `BLOCKED — dependency
   missing`, exit non-zero.
4. **`$?` through a pipe is a lie** — `set -o pipefail` / `${PIPESTATUS[0]}`; never wrap a gate you
   need to watch in `| tail`. `[REC]`
5. **Verify the gate's real SCOPE from what it globs and executes, not from its docstring**
   ("53 apps" was 1522). `[REC]`
6. **PUSH ≠ DEPLOY.** Before claiming anything is live, confirm (a) which ref the deploy pipeline
   tracks and (b) that the pushed ref IS that ref. Say *"on GitHub, NOT live"* whenever they differ.
   `[REC]`

---

## §15. CONCURRENT-LANE COORDINATION AND THE FETCH GUARDRAIL ⚠️⚠️
*(additionally proposed — the failure that nearly published twice)*

**The failures `[REC]`.**
- **Two lanes ran the same gate-review brief unannounced**, twice.
  `CODEX-GATE-REVIEW-2026-07-23.md` observed `clone_contamination_gate.py` changing under it mid-review
  (27 441 B → 29 074 B **crashing with `NameError: REGISTRY_LITERALS is not defined`** → 32 417 B) and
  **correctly stood down without writing**; `…-LANE-2.md` was the live editor and applied 14 fixes.
  The split was *lucky*, not designed: each lane found a defect the other missed (F5; the `realData`
  laundering vector).
- **Concurrent lanes on the same branch produced an uncontrolled publish.** `[ORCH]` The publish
  commit `398ae1047` (*"publish the HFrEF GDMT network NMA and link it from the landing page"*,
  2026-07-29 13:44) is an ancestor of `main`, and `main == origin/main == b02990a02`.
- **The fetch-guardrail prevented the double-push** — *"confirm `origin/main == EXPECTED` else
  STOP"*. `[ORCH]` It is the one control in this list that has a **demonstrated save**, which is why
  it is promoted from tactic to rule.

**THE RULE — mechanical:**

1. **SINGLE WRITER PER FILE, DECLARED BEFORE THE FIRST WRITE.** Every lane appends its owned paths to
   `SHARED-LANE-NOTES.md` (append-only; each lane owns its own section) **before** touching them, and
   is READ-ONLY everywhere else. The file already exists and already carries this contract —
   the failure was lanes not being *required* to read it.
2. **DETECT THE COLLISION MECHANICALLY, DON'T HOPE TO NOTICE IT.** Before writing a file, record
   `(size, mtime, md5)`; re-check immediately before the write. **Changed ⇒ STOP and report**, do not
   merge, do not clobber. Pin all findings to a snapshot hash, never to the live file — the 2026-07-28
   lane did exactly this (`pinB md5 59a28d5d…`) and it is what made its report usable.
3. ⛔ **FETCH-GUARDRAIL BEFORE ANY PUSH — MANDATORY.**
   `git fetch && [ "$(git rev-parse origin/main)" = "$EXPECTED" ] || STOP`.
   `EXPECTED` is the SHA the lane was briefed with. Mismatch = another writer landed = **STOP and
   report**, never rebase-and-push in the same breath.
4. **Push authority.** Push remains **Mahmood-only** unless he explicitly authorises *that specific
   push* (hard constraint, unchanged). Where authorised: configured git auth,
   `GIT_TERMINAL_PROMPT=0`, **STOP on any credential prompt**, **never force**, never `--no-verify`.
   `[ORCH]`
5. **Publishing is an outward-facing act and needs its own confirm.** A commit that adds a link from
   the landing page is a **publish**, not a fix, regardless of its commit-type prefix. It requires
   the §1 cross-family gate to have cleared *and* an explicit go — the same bar as any merge.
6. **On resume, `git fetch` FIRST**, read exactly what landed, rebase onto it, build on it, never
   force over it (`rapidmeta-freeze-coordination.md`). `[REC]`

---

## §16. THE BRIEFER IS BOUND TOO — PROVENANCE TAGS AND THE POINTER RULE ⚠️⚠️
*(additionally proposed — the orchestrator is the folklore vector)*

**The failure this session `[REC]`.** The orchestrator **recalled "44 contrasts"; the measured value
is 105.** Verified against the artifact:
`outputs/hfref_league_export.json` (commit `53f83cc9e`) — `estimable_pairs: 105`,
`contrasts_in_data: 30`, `nodes_in_network: 15`, `trials: 28`, engine `R 4.6.0 / netmeta 3.6.1`.
A wrong EMPEROR-Reduced/HR premise entered a brief the same way. `[ORCH]`
This is the documented standing pattern: *"The lanes FETCH; I RECALL; I am UPSTREAM of all of
them"* — ~13 corrections in one session, **none caught by the orchestrator itself**
(`orchestrator-is-the-folklore-vector.md`).

**THE RULE — mechanical (this is §0d of `METHODS-CONTRACT.md`, promoted here because lanes read
this file):**

1. ⭐⭐ **THE POINTER RULE. No number enters a brief unless it is in `INDEX.md` / a named artifact
   with a producing script. Otherwise write the POINTER and let the lane fetch it.**
   *An error cannot propagate through a value I never sent.*
2. **PROVENANCE-TAG EVERY NUMBER THAT DOES ENTER:**
   `[MEASURED — <pointer>]` · `[INHERITED — unverified]` · `[MY RECOLLECTION — VERIFY BEFORE USE]`
   (default: wrong). **Untagged = an assertion the lane inherits as fact.** Proven: caught two
   orchestrator errors within hours on 2026-07-16.
3. ⛔ **NEVER put a recalled specific — a count, a trial name, an HR, a premise about what a trial
   showed — into a lane brief as fact.** State it as a question the lane must resolve, or omit it.
4. **Verify lane state before reporting it** — lanes have been reported running when they had
   silently stopped. §9's `list_sessions` confirm is the mechanical form of this.
5. **Report the orchestrator's own correction rate per session, unprompted.**
   *"A rate I don't measure cannot decline."*
6. ⚠️ **THE TELL: when a brief feels AUTHORITATIVE, that is the feeling of RECALLING rather than
   FETCHING.** Coherence is what a false model feels like from the inside.

---

## §17. SYMMETRY, CO-PRIMARY, AND TIER OVERLOADING ⚠️⚠️
*(additionally proposed — the evidence-layer lessons of 2026-07-30, stated as gates)*

**The failures `[REC]`** (`correcting-adversary-forgery-yields-finding.md`, commits `402ec8811`,
`53f83cc9e`, `outputs/HFREF_FINDINGS_RESOLVED_2026-07-30.md`):

1. ⭐⭐ **AN EVICTION/QUARANTINE RULE MUST BE APPLIED SYMMETRICALLY OR IT IS A DOUBLE STANDARD.**
   The rule *"unverified per-arm all-cause deaths + identical-counts pattern ⇒ quarantine"* was met by
   **three** trials (CARMEN 572, GALACTIC-HF 8232, Vizzardi 130) and applied to **one**.
   **THE GATE:** before any eviction lands, run the eviction predicate across the **whole ledger** and
   assert the acted-on set equals the matched set — **or name, on the record, why each unacted match
   does not reach the bar.** A rule applied to one row is not a rule.
2. ⭐⭐⭐ **CORRECT THE ADVERSARY'S OVER-CLAIM TO SOURCE; DON'T MERELY REJECT IT — THE CORRECTION IS
   OFTEN THE FINDING.** Gemini's false *"the retained unverified trials pull AWAY from the null"*
   (real: GALACTIC-HF RR 0.998, Val-HeFT 1.018, Vizzardi 1.000) surfaced, on correction, the
   symmetry violation **neither the same-family resolution nor Gemini had stated.** Extends §3a:
   verifying to source is not only a defence, it is a **generator**.
3. ⚠️ **A DELETION THAT MOVES RESULTS TOWARD SIGNIFICANCE NEEDS BOTH FITS SHOWN CO-PRIMARY, NOT A
   CAVEAT.** Quarantining CARMEN raised CI-excludes-1 **12→17** and pushed two contrasts into nominal
   significance **on a provenance decision alone**. Shipping only the removed-fit was rated
   `DISCLOSED-BUT-INSUFFICIENT`. **THE GATE:** any inclusion decision that increases the count of
   significant contrasts ⇒ the artifact must render **both fits side by side**; prose disclosure does
   not discharge it. (This is §8, self-serving-direction, made renderable.)
4. **REPORT A FINDING THAT CUTS BOTH WAYS IN BOTH DIRECTIONS.** GALACTIC-HF retained is
   simultaneously the strongest evidence of an inconsistent standard **and** the strongest refutation
   of a p-hacking charge (~13,372 near-null unverified patients retained vs 572 removed). *A finding
   that only cut against us would itself be suspect.*
5. **DO NOT OVERLOAD A PROVENANCE TIER.** `VERIFIED_FULL` covered both CIBIS-II's verbatim
   *"156 vs 228"* and SPICE's `6/179, 3/91` **uniquely back-inferred from rounded percentages** —
   real, but not the same evidentiary act. **Recovered-from-percentages gets its own tier.**
   Generalisation: when one tier label covers two different *acts of knowing*, it will be read as the
   stronger one.

---

### Adoption note

Nothing above is merged. If accepted, §9–§17 append to `GOVERNING-RULES.md` after §8; the *Hard
constraints* block stays last and unchanged. Two items in §14 and §16 are **corrections to
session-generated notes** (`LANE OPS (f)`; "44 contrasts") and should be applied to
`active-sessions-index.md` whether or not the addendum is adopted.
