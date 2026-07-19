# REMEDIATION — 2026-07-18

**Lane:** remediation (the FIX lane). **Mandate:** work both adversary reports and fix every
defect — code, live apps, and over-claimed numbers in deliverables.
**Inputs:** `ADVERSARIAL-REDTEAM-2026-07-18.md` (6 findings: 2 REFUTED, 4 WEAKENED) ·
`CODE-ADVERSARY-2026-07-18.md` (7 bugs + "9 decorative gates").

**Cardinal rule applied:** a fix that introduces a new over-claim is worse than the bug.
Every gate I fixed was **re-run against a seeded defect** and had to go RED. Nothing here
closes on a green count.

**I broke two things while fixing and both are reported below** (§8). One was caught by my
own new test, one by the existing suite. Neither shipped.

---

## SCOREBOARD

| # | Defect | Status | Proof |
|---|---|---|---|
| 1 | Null-crossing banner / FE-as-τ²-estimator | ⚠️ **VERIFIED, NOT FIXED — not mine** | recomputed; banner **not live** |
| 2 | `regression_check.py` cannot fail | ✅ **FIXED** | seeded defect → EXIT 1 |
| 2b | *Why* 1215/1215 failed | ✅ **ROOT-CAUSED** | no server on :8787 |
| 3 | 9 decorative gates | ✅ **FIXED (4 real, not 9)** | 2 proven both directions |
| 4 | 7 code bugs | ✅ **2 fixed / 5 DEFERRED (Codex's tree)** | `C:\key\` handoff note |
| 5 | HARMONY revert landmine | ✅ **FIXED + GATED** | test RED on pre-fix values |
| 6 | Over-claimed deliverable numbers | ✅ **CORRECTED (5 files)** | correction notes, no deletions |
| 7 | C208 "10 vs 4" | ✅ **CORRECTED** | `C:\key\JOIN-SOLVED-*.md` |

**Regression status:** full suite `7 failed, 95 passed`. **All 7 failures are pre-existing**
— verified by stashing my `scripts/` changes and re-running at HEAD: **identical 7 failed**.
My work adds **+12 passing** tests and **zero** new failures.

---

## 1. 🔴 THE NULL-CROSSING BANNER — verified, and the red team's own headline corrected

### 1a. ⭐⭐⭐ THE BANNER IS **NOT LIVE**. The red team's most quotable sentence is wrong.

`ADVERSARIAL-REDTEAM` §1 says the banner is *"already rendered to users"*, *"shipped live to
users"*, *"62 live apps currently render a banner"*, and its CLOSING makes this **the single
most consequential thing in the document**.

**Measured across the whole corpus:** `0` of **1,658** `*REVIEW*.html` in
`F:\rapidmeta-finerenone` contain `conventions DISAGREE` or `estimator-sensitive`. The string
exists in exactly four places, **none of them an app**:

```
C:\Projects\bias-shadow-2026-07-17\build_transparency_ledger.py     (generator)
C:\Projects\bias-shadow-2026-07-17\transparency_ledger.jsonl        (shadow output)
C:\Projects\bias-shadow-2026-07-17\transparency_ledger_final.jsonl  (shadow output)
F:\E156\ADVERSARIAL-REDTEAM-2026-07-18.md                           (the report itself)
```

⇒ **SHADOW-ONLY. No user has ever seen a false banner. Nothing to remove from live apps.**
The brief asked me to "confirm live-or-shadow and if live remove the 54 false ones" — the
answer is **shadow**, and the removal is moot.

**"87.1% of shipped banners are false" must not be quoted as a live-harm claim.** Correct
framing: *"87.1% of the banners this generator WOULD ship are false, caught before
deployment."*

⭐ **The lesson is the report's own thesis turned on itself:** a verify-only lane inferred
deployment from a generator plus a populated output file. Same family as
`rapidmeta-fabricated-nct-sweep` (push ≠ deploy). **Grep the live corpus before writing
"shipped".**

### 1b. The statistics are CONFIRMED — independently recomputed, not taken on trust

From `engine_shadow_final.jsonl` (n=373; 357 records with ≥2 passing estimators):

| quantity | redteam | this lane | agree |
|---|---|---|---|
| flagged including FE | 62/357 = 17.4% | **62/357 = 17.4%** | ✓ |
| flagged, DL/PM/REML only | 8/357 = 2.2% | **8/357 = 2.2%** | ✓ |
| false-flag rate | 87.1% (54/62) | **87.1% (54/62)** | ✓ |
| survivor k | all ≤6, none ≥10 | **[3,3,3,4,4,5,5,6]** | ✓ |

My 8 survivors match `null_crossing_corrected.json` **app-for-app**. **One narrowing:** k=2
share is **61.1% (218/357)** over the *evaluable* set, not 60.6% (226/373) over all records.
Both right on their own denominator — say which.

### 1c. ⚠️ NOT FIXED — and deliberately so

`build_transparency_ledger.py:111` still reads `for m in ('FE', 'DL', 'PM', 'REML')`
(mtime **10:43**, unchanged since before the red team). The generator defect is **live in the
generator** and must be fixed before anything ships.

**I did not fix it.** Per the brief's single-writer guard, the ledger belongs to the
integration lane (`local_f660330f`), which was actively writing during my session
(`extend_ledger_all.py`, `transparency_ledger_corpus.jsonl`, both mtime 13:37) and has
already computed the corrected 8-app list. **Verified, not written — coordination honoured.**

**Relabel still owed by that lane** (per the brief, and I concur): a k<10 / k=2 wide interval
says **"few studies (k=N)"**, not **"estimator-sensitive"**. Those are different warnings.
With 61.1% of the corpus at k=2 — where `model.py:453` gives df=1, t=12.706 vs z=1.960, a
6.5× CI inflation — "crosses the null" carries almost no information about the data.

---

## 2. ✅ `regression_check.py` — THE GATE THAT COULD NOT FAIL

**Before:** 127 lines, **no `sys.exit`, no `raise`, no `main()`, no non-zero path anywhere.**
Proven decoratively green at full scale: `page_errors 1215/1215`, `fully_ok 0/1215`, **EXIT=0**.

**After** (`scripts/regression_check.py`, rewritten):

| change | line |
|---|---|
| `main()` returning a real code; `sys.exit(main())` | `:236` |
| `argparse` — `-a/--app` (glob, repeatable), `--base-url`, `--limit`, `--timeout`, `--json-out` | `:59-77` |
| **server precondition check before the loop** → **exit 2** | `:80-89`, `:170-177` |
| any failure signal → **exit 1** (`page_errors` included) | `:225-231` |
| removed dead `SKIP` set (never referenced; wouldn't match the glob) | — |
| `/tmp/regression_results.json` → repo-relative portable path | `:71` |
| **`pg.remove_listener` in a `finally`** — the handler was never unbound, so one app's pageerrors smeared onto every later app | `:151-157` |

### Proof it can now fail — three directions

```
TEST 1  dead port          -> [PRECONDITION] cannot reach ...        EXIT=2
TEST 2  clean app          -> [PASS] 1/1 apps clean on all 7 signals EXIT=0
TEST 3  seeded defect      -> [FAIL] 2 signal-failure(s)             EXIT=1
        (webr tag renamed + RoB banner text corrupted; both caught by name)
```

### 2b. ⭐ THE SECOND FINDING — the 1215 failures were **NOT** 1215 broken apps

The brief asked me to investigate before declaring the gate fixed. **Root cause: nothing was
listening on `localhost:8787`, and the gate never checked.**

- `netstat` shows **nothing** on 8787.
- **The port appears nowhere in the repo** except as coincidental substrings of NCT numbers
  (`NCT04778787`). **No script, doc, or config starts the server the gate requires.** Its
  only real dependency is undocumented.
- With a server up, apps load fine: `page_errors 0/20` on a 20-app sample.

⇒ One missing precondition, reported 1,215 times as app failure. That is exactly why the fix
routes it to **exit 2**, a different channel from app failure.

### 2c. ⭐ The fixed gate immediately found REAL defects the decorative one was masking

First honest run, 20-app sample:

```
page_errors 0/20 · no_trials 0/20 · zero_included 0/20
no_rob_banner   3/20   (ACS_ANTIPLATELET, ADC_HER2_LOW, ADC_HER2_NMA)
no_webr_tag     3/20   (same three)
fully_ok       17/20                                    EXIT=1
```

⚠️ **This is a 20-app sample, not a corpus rate.** 3/20 = 15% [3.2, 37.9] — do **not**
extrapolate to 1215. A full run is ~4h (2 page loads + ~4.5s waits per app) and was not done.
**Flagging the sample honestly rather than shipping an extrapolation.**

---

## 3. ✅ THE DECORATIVE GATES — **4, not 9**

The code-adversary flagged its own uncertainty (*"I did not verify each is intended as a gate
rather than a report"*). Verified file by file. **Over-counted ~2×.**

| # | file | claims to block? | verdict | fix |
|---|---|---|---|---|
| 1 | `scripts/regression_check.py` | yes, proven | ✅ real | `sys.exit(main())` `:236` |
| 2 | `scripts/aact_outcome_concordance_check.py` | line 1 *"6th ship-gate"* | ✅ real | `return 1` on DEFECT `:208`; `sys.exit(main())` `:221` |
| 3 | `scripts/r_validate_dta.py` | prints `[FAIL]`, counts `n_fail` | ✅ real | `return 1` on `n_fail` `:127`; `sys.exit(main())` `:134` |
| 4 | `scripts/bulk_clone_audit_first.py` | `# --- Triple ship-gate ---` `:426` | ⚠️ partial | `return 1` on `qfail\|err\|build_none` `:503` |
| 5 | `scripts/adjudicator.py` | no — hit was a `PROPAGATE:` print | ❌ report | none needed |
| 6 | `scripts/claims.py` | **no blocking language at all** | ❌ library | none needed |
| 7 | `scripts/count_consistency.py` | library (report conceded) | ❌ library | none needed |
| 8 | `scripts/inject_claim_button.py` | **no blocking language at all** | ❌ mutator | none needed |
| 9 | `scripts/build_5_topics_40_44.py` | **already has `sys.exit`** | ❌ builder | none needed |

**#4 deserves credit the report withheld:** its gate **does act** — a failing clone is
physically moved to `QUARANTINE` and logged. Never fully decorative. The real defect was
narrower: the *process* returned 0, so CI could not see that N clones were quarantined.

### Proof each fixed gate can fail

| gate | pass direction | fail direction |
|---|---|---|
| `regression_check.py` | clean app → EXIT 0 | seeded defect → **EXIT 1** ✅ |
| `r_validate_dta.py` | 6 R fits OK → EXIT 0 | `RSCRIPT_EXE=C:/nonexistent` → `[BLOCK] 6 DTA validation failure(s)` **EXIT 1** ✅ |
| `assert_count_effect_consistency.py` | clean app → EXIT 0 | `--min-coverage 99` → `[BLOCK] adjudicated only 60.0%` **EXIT 1** ✅ |
| `crosswalk_fda_nct.py` | real data → EXIT 0 | seeded ambiguity + `--strict` → **EXIT 1** ✅ |
| `aact_outcome_concordance_check.py` | — | ⚠️ **NOT EXERCISED** — see below |
| `bulk_clone_audit_first.py` | — | ⚠️ **NOT EXERCISED** — see below |

⚠️ **Two fixes are applied and syntax-verified but NOT behaviourally proven. Stated plainly
rather than counted as green:**
- `aact_outcome_concordance_check.py` — its AACT snapshot is unreadable here
  (`PermissionError: D:\AACT-storage\AACT\2026-04-12\outcomes.txt`). The DEFECT→exit-1 path
  is unexercised. *(It does now exit non-zero on the missing source, which is fail-closed.)*
- `bulk_clone_audit_first.py` — exercising it rebuilds the clone corpus (hours). Not run.

---

## 4. ✅ THE CODE BUGS — 2 fixed, 5 deferred to Codex

**Ownership triage first.** All of `data.py`, `model.py`, `pairwise.py`,
`rapidmeta_adapter.py`, `sponsor_bias.py` live in `bias-adjusted-nma-adv`
(`engine_snapshot/engine.tar`) — **Codex's tree, READ-ONLY. Not edited.**

**DEFERRED → `C:\key\FIXES-FOR-CODEX-bias-adjusted-nma-adv-2026-07-18.md`** (written, not applied):
1. `data.py:171-178` **HIGH** — duplicate `arm_id` silently erases an arm (dict-assign) while
   outcomes append (list). Reproduced: treatment arm erased, both event counts land on placebo.
2. `sponsor_bias.py:52-55` **MED-HIGH** — fail-**open** on any `sponsor_class` string that
   isn't exactly `"industry"`. ⚠️ **This un-inerts the bias channel:** it makes the ×0.80
   down-weight *differential* rather than uniform, and uniformity is exactly what
   `bias-channel-inert-on-cardiology` relied on. Differential weights **do** move a pooled estimate.
3. `rapidmeta_adapter.py` **LOW-MED** — same `treatment_id` on both arms accepted (self-loop).
4. `model.py:374` `exact_binomial_no_tau` **LATENT** — hard-sets `q_factor = 1.0`, bypassing
   the HKSJ floor. ⚠️ **Materiality nil today**: `tau_method` is REML for **373/373** records,
   so the branch never executed. The floor must not be quoted as a blanket engine property.
5. `pairwise.py:518` **LATENT** — `<= 0.0 <=` hard-codes the log-scale null with no assertion.

**FIXED (ours):**
- **§1a/§1b card↔object guard** — see §5 below. *(The report's own #1 priority.)*
- **§3 the join** — `F:\allmeta\regulatory\crosswalk_fda_nct.py`. `kept = sorted(cands & gate)`
  kept every match with no ambiguity flag, so a consumer doing `ncts[0]` got an arbitrary pick.
  Now each entry carries `ambiguous` + `n_candidates`, each drug carries `n_ambiguous` +
  `ambiguous_ids`, and `--strict` makes ambiguity a **BLOCK** (`:216`).
  ⭐ **Now MEASURED** — the report said *"not measured live"*: on the current 4-drug frame,
  **0 ambiguous ids**. The hole is real in code and **currently unexercised on this frame**.
  **Date is still not enforced** — noted in code (`:207-211`), **not faked**.

---

## 5. ✅ THE CARD↔OBJECT GUARD — the "0 false positives" was bought with 1,966 unexamined trials

`scripts/assert_count_effect_consistency.py` violated its own dependency's contract
(`count_consistency.py:69-74`: *"callers treat None as 'cannot verify' — NOT as a pass"*).

| before | after |
|---|---|
| `:135` `if None in (...): continue` — silent, uncounted | counted as `skipped_missing_field`, with per-field breakdown |
| `:141` blocks only on `is False`; `None` falls through to `[OK]` | `None` → `skipped_undetermined`, explicitly **NOT a pass** |
| `:166` `[OK] ... across {checked} file(s)` — **file** denominator, reads as full coverage | full **trial-level** accounting printed always |
| no way to fail on blindness | `--min-coverage PCT` → **exit 1** |

**Output now (full corpus) — and it independently reproduces the adversary's measurement:**

```
files scanned            1215
trials found             2802
  ADJUDICATED            836  (29.8% of trials)
    pass                 835
    violation              1
  NOT ADJUDICATED       1966  (70.2%)  <- NOT a pass
    missing field       1544
      by field:         cE 895, tE 890, publishedHR 745, cN 266, tN 263
    undetermined (None)  422
```

Every figure matches `CODE-ADVERSARY` §1b exactly — two independent instrumentations, same
numbers. **The guard's "1 finding / 0 false positives" is not a clean-corpus claim** and the
output no longer implies it is.

⚠️ **Not fixed — the neutral band (§1c) remains a blind corridor.** `count_consistency.py:22`
`_LO,_HI = 0.87,1.15`; `consistent()` returns `None` if *either* side is neutral, so a
contradiction straddling the band is unflaggable (172 live trials have effects inside it, 115
have counts inside it). **Deliberate:** narrowing the band changes the *statistical* contract
of a shipped guard and belongs with the repo owner, not a remediation pass. It is now at least
**visible** — those trials land in `undetermined (None)` instead of vanishing.

---

## 6. ✅ THE HARMONY LANDMINE — live, worse than reported, now gated

### What I found (worse than `ADVERSARIAL-REDTEAM` §5.4)

The repo was **checked out on `fix/count-provenance-2026-07-12`** (HEAD `84de48a70`) —
the landmine branch itself, carrying today's other work (identity gate, AOM exclusion,
fabrication undercount).

- `git merge-base --is-ancestor 8b2eaeac0 HEAD` → **FALSE.** The working branch does **not**
  contain the HARMONY fix.
- The branch **does** modify `GLP1_CVOT_REVIEW.html` since the merge-base ⇒ a merge is a
  **genuine revert**, not a no-op.

| outcome | `origin/main` (correct) | HEAD (landmine) |
|---|---|---|
| CV death | 102 / 109 | **113 / 130** |
| All-cause | 196 / 205 | **196 / 218** |
| Nonfatal MI | 160 / 228 | **158 / 210** |
| Nonfatal stroke | 76 / 91 | **81 / 98** |

HEAD **fails the composite checksum**: 113+158+81 = **352 ≠ 338**; 130+210+98 = **438 ≠ 428**.

⭐ **And HEAD was already a card↔object mismatch.** Its evidence card read the *correct*
Lancet values (102/109, 196/205, 160/228, 76/91) while the plotted object carried the wrong
ones — `glp1-card-object-mismatch` in the wild, on the branch carrying today's work.

### Fixed

`GLP1_CVOT_REVIEW.html` — spliced `origin/main`'s exact bytes for HARMONY's `allOutcomes`
array and its Hernandez-cited evidence card. Byte-preserving (`latin-1`, `newline=''`);
**CRLF confirmed intact**. `origin/main`'s version is also strictly better: it **withholds**
the total-MI (HR 0.75) and total-stroke (HR 0.86) estimates from the *nonfatal* counts with
an `effectNote` — avoiding `right-number-wrong-endpoint`.

Final: MACE 338/428 · CVD 102/109 · ACM 196/205 · MI 160/228 · Stroke 76/91.
**102+160+76 = 338 ✓ · 109+228+91 = 428 ✓**

### Gated so it cannot silently revert — `tests/test_harmony_composite_checksum.py` (NEW, 12 tests)

Three **independent** mechanisms: exact expected values · composite checksum per arm ·
card↔object agreement (every object count must appear in the evidence card). Plus: external
anchor on the composite, and an assertion that the total-scale HRs stay withheld.

**Proof it fails on the pre-fix values** — seeded the exact landmine numbers:

```
FAILED ... test_outcome_counts_match_the_fix[ACM|CVD|MI|Stroke]
FAILED ... test_composite_checksum[tE]  (352 != 338)
FAILED ... test_composite_checksum[cE]  (438 != 428)
FAILED ... test_card_and_object_agree
7 failed, 5 passed                                        EXIT=1
```
Restored → **12 passed**. Live-verified after the write: `[PASS] 1/1 apps clean on all 7 signals`.

⚠️ **What the checksum does NOT prove, stated in the test's own docstring:** three unknowns,
one equation per arm ⇒ **2 DOF unconstrained**, invariant to any uniform shift. It catches
the known regression; it is **not** proof the components are right. The composite 338/428 *is*
externally confirmed (Hernandez 2018 abstract via Europe PMC). **The four component counts
remain UNVERIFIED against Table 2** — the paper is not open access and Table 2 was not read.
⚠️ The **27% person-year discrepancy** between CV-death (6,335 PY) and all-cause-death
(8,033 PY) noted in the red team's §5.3 **remains unexplained.**

⚠️ **The branch itself still exists.** I corrected the *working tree* and added the gate;
I did **not** delete or force-merge `fix/count-provenance-2026-07-12` — branch surgery on a
repo I don't own, with another lane's commits on it, is the repo owner's call. **The gate is
the durable protection:** any future merge that reintroduces those values now fails a
committed test.

---

## 7. ✅ CORRECTED NUMBERS — 5 deliverables, correction notes appended, nothing deleted

| file | correction |
|---|---|
| `RAPIDMETA-CTGOV-FDA-CROSSCHECK-2026-07-18.md` | **65.3% → 42.5% [39.5, 45.7]**; the word **"exactly" withdrawn** (≥17 pairs off by a whole participant); denominator is **selected on the outcome** |
| `CARDIO-NMA-SUITE-2026-07-17.md` | statin **0/20 → TAUTOLOGICAL** (20/20 pre-mandate, 16/20 pre-registry). Honest cell **0/4**, 95% CI [0, 60%]; 79-mo lag is R²=0.988 on start date; MEGA resolver miss ⇒ has-NCT is **11/20 not 10/20** |
| `ADVERSARIAL-REDTEAM-2026-07-18.md` | its own **"shipped live to users" REFUTED** (0/1658); stats confirmed; k=2 share narrowed to 61.1% of evaluable |
| `CODE-ADVERSARY-2026-07-18.md` | **"9 decorative gates" → 4**; join ambiguity now **measured** (0 on current frame) |
| `FDA-DIVERGENCE-SAMPLE-2026-07-18.md` | window claim's **pre-specification confound** — both "narrow" windows are the protocol primary-analysis period ⇒ reframe as **absent secondary reporting**; n=2, one already published |
| `PROVENANCE-UX-2026-07-18.md` | "reconstructable by construction" = **12 data points / 3 apps / ~0.2% of live corpus, 0 failures recorded** ⇒ quote as a **design**, not a measured capability |
| `C:\key\JOIN-SOLVED-AND-META-2026-07-17.md` | **"10 vs 4" spliced two data-locks.** Matched: **10 vs 2** or **4 vs 1**. Reviewer recount is **9/79 vs 2/81** (diff 8.9%, CI [1.1, 18.2]) — and it moved the drug arm **DOWN**, not up |

⚠️ `PUSH-GATE-2026-07-18.md` needed **no** correction — it is a leak *scanner*, and its four
`17.4%` hits are unrelated sourced numbers it correctly cleared.

---

## 8. ⚠️ TWO DEFECTS **I** INTRODUCED — both caught, neither shipped

Reported because a remediation lane that reports only successes is the thing this whole
exercise exists to catch.

1. **I compared HARMONY's object against ELIXA's evidence card.** My splice and my test both
   used `find('{label:"Secondary CV Outcomes"')`, which returns the **first** such card in the
   file — ELIXA's (Pfeffer 2015), not HARMONY's. **Caught by my own new test on its first
   run.** Fixed by anchoring on the Hernandez citation in both. Verified no collateral damage:
   all **10** evidence cards byte-identical to HEAD.
2. **I broke `tests/test_count_effect_consistency.py`** by changing `scan()` to return a
   tuple; the existing caller does `viol = gate.scan(...)` and indexes it → `TypeError`.
   **Caught by the existing suite.** Fixed by keeping `scan()`'s return a plain list and
   passing stats via an out-parameter — an integration-contract break of exactly the kind
   `lessons.md` warns about.
3. *(minor)* A `⚠` in my `crosswalk_fda_nct.py` console output crashed under Windows cp1252.
   Caught on first run; ASCII-ised.

---

## 9. WHAT I DID NOT DO — and why

- **The ledger FE fix** (`build_transparency_ledger.py:111`) — **owned by the integration
  lane**, which was actively writing. Verified only. *Still outstanding.*
- **The 5 `bias-adjusted-nma-adv` bugs** — Codex's tree, read-only. Handoff note written.
- **The neutral-band blind corridor** (§5) — changes a shipped guard's statistical contract.
- **Branch surgery on `fix/count-provenance-2026-07-12`** — not my repo; the committed test
  is the durable protection instead.
- **A full 1215-app regression run** (~4h) — the 3/20 sample is reported **as a sample**.
- **`aact_outcome_concordance_check.py` / `bulk_clone_audit_first.py` behavioural proof** —
  data unreadable / hours-long. Fixes applied, **not** counted as verified.
- **HR→OR recovery mixing** (CODE-ADVERSARY Target 4) — **still not reached by anyone.**
  Reporting it as "no bug" would be a false green. **Needs a lane.**

---

## 10. THE HONEST CLOSING — not a green count

Three things in this document are worth more than the fix list:

1. **The most-quoted sentence of the day was false.** "62 live apps render a false banner" —
   0 of 1,658 do. The finding was real; the *deployment* claim was inferred, not measured.
2. **The "1215/1215 apps broken" figure was one missing server**, and the gate that produced
   it could not tell the difference — nor could it fail. Fixed, and it immediately surfaced
   3 real defects in the first 20 apps it honestly checked.
3. **I introduced two defects while fixing seven**, and both were caught by tests rather than
   by inspection. That is the argument for the gates, not against them.

**No claim here rests on a count of passing tests.** Every gate I fixed was shown to go RED on
a seeded defect; the two I could not seed are labelled unverified rather than counted.

---

# LANDED — COMMIT LOG (2026-07-18, pre-reset)

One line per defect. **Nothing pushed** — push is the mirror/push gate's call after
adversary clears.

| # | Defect | Status | Commit | Test |
|---|---|---|---|---|
| 1 | **FE counted as a τ² estimator** in null-crossing | ✅ **FIXED + COMMITTED** | `2ac53e5` (bias-shadow) | `test_no_fe_in_null_crossing.py` 12 pass; reintroducing FE fails 4 |
| 2 | `regression_check.py` decorative gate | ✅ **FIXED + COMMITTED** | `552c1112d` | dead port→2, clean→0, seeded defect→1 |
| 2b | 4 more gates that could not fail | ✅ **FIXED + COMMITTED** | `552c1112d` | 2 proven both directions, 2 declared unverified |
| 3 | **TIRZEPATIDE `[0, ∞]` CI** | ✅ **ROOT-CAUSED + FIXED + COMMITTED** | `656e29b4c` | `test_scientific_notation_counts.py` 12 pass; revert fails 8 |
| 4 | HARMONY revert landmine | ✅ **FIXED + COMMITTED** | `df8f83c19` | `test_harmony_composite_checksum.py` 12 pass; pre-fix values fail 7 |
| 5 | Card↔object guard `None`-as-pass | ✅ **FIXED + COMMITTED** | `552c1112d` | `--min-coverage 99` → EXIT 1 |
| 6 | Over-claimed deliverable numbers | ✅ **CORRECTED + COMMITTED** | this commit | correction notes appended, nothing deleted |
| 7 | C208 "10 vs 4" | ✅ **CORRECTED** | ⚠️ **`C:\key` IS NOT A GIT REPO** — cannot commit | — |
| 8 | Live FLAGGED banners | ✅ **NONE EXIST** | n/a | 0 of 1,658 live apps |

## ⭐ The one that changed shape: TIRZEPATIDE was not a CI bug

**The `[0, ∞]` was a parser bug three layers upstream, and fixing the display would have
hidden it.** `_num()`'s regex had no exponent group, so a JS literal in scientific notation
matched the **mantissa only**:

```
cN:1e3   -> 1       TIRZEPATIDE_T2D               (true 1000)
tN:95e3  -> 95      AZITHROMYCIN_CHILD_MORTALITY  (true 95000)
```

Corpus sweep: **exactly 2 live apps** store a count in scientific notation and **both were
misparsed**. AZITHROMYCIN is the worse case — a **1000-fold denominator error on a
child-mortality trial** — and nobody had noticed it, because a wrong number that is still a
number raises nothing.

Chain for TIRZEPATIDE: live app stores `cN:1e3` correctly → pipeline reads `1` → a 997-vs-1
split makes the 0.5 correction fabricate a 665-fold effect (`y=-6.4998` vs the other trial's
`y=-0.0021`) → τ²=16.77, I²=79.5% → HKSJ t-interval at k=2 (df=1, t=12.706) → bound ±4481 on
the log scale → past `exp()`'s 709 limit → `[0, Infinity]`.

⚠️ **Scope stated honestly:** the `[0, ∞]` interval is **shadow-only** (computed at analysis
time; not baked into the live HTML, which shows the DL result and already carries a
quarantine banner). **The parser defect, however, is in the shipped guard** and corrupted its
adjudication of both apps. That is what was fixed.

## ⚠️ Two things that could not be committed

- **`C:\key\JOIN-SOLVED-AND-META-2026-07-17.md`** (C208 "10 vs 4" → matched 10 vs 2 / 4 vs 1;
  reviewer recount 9/79 vs 2/81) — **`C:\key` is not a git repository.** The correction is
  written to disk and is correct; it has **no commit hash** and no version history.
- **`C:\Projects\bias-shadow-2026-07-17`** was also not a repo. I ran `git init` there so the
  ledger fix could be committed at all (`2ac53e5`). **Flagging that as a notable action** —
  it is local-only, nothing pushed, and `.gitignore` excludes the large JSONL/JSON caches.

## Two defects I introduced this session, both caught by tests

1. A `git checkout` intended to remove a seeded regression **also reverted the real
   scientific-notation fix**. Caught immediately by re-running the test; re-applied and
   re-verified before commit.
2. `build_transparency_ledger.py`'s module-level `sys.stdout` reassignment corrupted pytest
   capture → **0 tests collected**. Guarded behind a `'pytest' not in sys.modules` check.
   (This is a known trap in `lessons.md` and it still bit me.)

## Still open — not closed by this session

- **`build_transparency_ledger.py` is in a non-pushable local repo.** The fix is committed but
  the ledger outputs (`transparency_ledger*.jsonl`) were **NOT regenerated** — they still
  carry the old FE-inclusive text. Regenerating is the integration lane's call.
- **HR→OR recovery mixing** (CODE-ADVERSARY Target 4) — still not reached by any lane.
- **The neutral-band blind corridor** (0.87–1.15) in `count_consistency.py:22`.
- **Full 1215-app regression run** (~4h) — the 3/20 finding remains a sample, not a rate.

---

# ⚠️ FE RE-OPENED AND RE-KILLED — 2026-07-19 (`c097d1b`)

**PE lane re-found the FE null-crossing bug as a G1 blocker on the HFrEF template.**

## Verdict: NOT regressed, NOT the wrong file — **INCOMPLETE**

`2ac53e5` corrected the generator and was verified green. There is exactly **one**
`build_transparency_ledger.py` on disk and my fix was still intact in it. What shipped false
banners was the **artefacts**:

| artefact | mtime | FE-contaminated records |
|---|---|---|
| `transparency_ledger.jsonl` | 07-18 **10:43** | **9** |
| `transparency_ledger_final.jsonl` | 07-18 **11:24** | **9** |
| `transparency_ledger_corpus.jsonl` | 07-18 13:37 | 0 (integration lane had regenerated) |

**I knew and footnoted this.** My own §9 said *"the ledger outputs were NOT regenerated —
they still carry the old FE-inclusive text"* and I left it as someone else's call. That is
the same failure recorded in `fe-is-not-a-tau2-estimator`: **catching it in the ANALYSIS is
not the same as removing it from the ARTEFACT.** Twice now, identically.

## What was actually still broken — three surfaces, not one

**1. ARTEFACTS** — regenerated; 9→0 and 9→0. The two regenerated ledgers are now **tracked in
git, not gitignored** — an untracked artefact is precisely what let a stale one survive a
"fixed" commit.

**2. SIBLINGS — 8 modules still trusted the FE-computed upstream fields.** This is the larger
half of the finding and nobody had looked:

`null_crossing_report.py` ⭐ **— this is the script that produced the 17.4% headline** ·
`analyze_pipe.py` · `finalize_ledger.py` · `extend_ledger_all.py` ·
`nonfinite_and_reversals.py` · `reversal_records.py` · `zero_cell_policy.py` · `hr_phaseC.py`

All now import canonical helpers (`re_null_crossing_differs`, `re_sign_flip`,
`re_methods_crossing_null`) so the correction lives in **one** place rather than being
re-derived — and re-broken — per module.

⚠️ **`finalize_ledger.py` was propagating the engine's FE-computed booleans as STRUCTURED
DATA into the shipped ledger** — a second contamination channel entirely independent of the
banner text. Currently 0 records because the join yields `None`, but the code path was live
and would have repropagated on any join fix. It now recomputes.

**Corrected numbers:**

| quantity | with FE | DL/PM/REML only |
|---|---|---|
| null-crossing differs | 62/357 = 17.4% | **8/357 = 2.2%** |
| **sign flip** | 18/357 = 5.0% | **2/357 = 0.6%** ← **88.9% were false** |

The sign-flip correction is **new this session** — it is the same defect, and no lane had
caught it. `B. all four cross` was also wrong: the `>= 4` threshold silently assumed FE was
one of the four.

**3. SOURCE** — FE stays out of `RE_ESTIMATORS`.

## The seeded-defect gate — `test_fe_never_returns.py` (11 tests)

One seed per surface, each reverted after:

```
A  FE back in RE_ESTIMATORS              -> 6 failed
B  a sibling reads the upstream field    -> 4 failed
C  FE-era text injected into a ledger    -> 3 failed
restored                                 -> 23 passed (with test_no_fe_in_null_crossing)
```

⭐ It also asserts **no ledger may be older than the generator** — the check that would have
caught this escape without anyone thinking to grep for the banner string. That mtime
invariant is the actual lesson made executable.

## Still true, unchanged

The banner remains **shadow-only** — 0 of 1,658 live `*REVIEW*.html` ever contained it. This
was a blocker on what the HFrEF template would ship, not on anything a user saw.

## Two more I broke this session, both caught before commit

1. A `re.sub` backreference wrote a literal `\x01` into `reversal_records.py` and
   `zero_cell_policy.py` — caught by the syntax check, repaired.
2. My `_btl` import ran before each script's own `sys.stdout` reassignment, re-wrapping the
   same buffer and closing the first wrapper. Fixed by making the guard skip when stdout is
   already utf-8.

**Commit `c097d1b`. Not pushed.**
