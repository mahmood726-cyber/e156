# CODE ADVERSARY — 2026-07-18

**Lane:** code/gate red team (decorrelated from `ADVERSARIAL-REDTEAM`, which attacks findings).
**Mandate:** attack the machinery; find the bug that ships a wrong number.
**Mode:** VERIFY/ATTACK ONLY. No file in any repo was modified. `bias-adjusted-nma-adv`
source was read from a snapshot extracted to scratchpad; the original tarball is untouched.

**Vendors:** Claude (this lane) + Codex/openai (`codex-cli 0.144.1`, one confirming run).
agy not used. Codex independently confirmed Target 1 via a *different* breaking input —
noted inline. First Codex run returned 0 bytes (lane failure); the retry succeeded.

---

## Scoreboard — ranked by (ships-a-wrong-number) × (likelihood)

| # | Target | Verdict | Severity | Vendor |
|---|--------|---------|----------|--------|
| 1 | Card↔object guard — `None` treated as pass | **BUG** | **HIGH** | Claude + Codex |
| 2 | Card↔object guard — 70.2% of corpus silently unadjudicated | **BUG (quantified)** | **HIGH** | Claude |
| 3 | Adapter — duplicate `arm_id` silently overwrites arm | **BUG (reproduced)** | **HIGH** | Claude |
| 4 | `sponsor_bias` — fail-OPEN on unrecognized sponsor class | **BUG** | **MED-HIGH** | Claude |
| 5 | `regression_check.py` — cannot fail | **DECORATIVE (proven)** | **MED** | Claude |
| 6 | Join — no ambiguity check, no date component | **BUG** | **MED** | Claude |
| 7 | Adapter — same `treatment_id` on both arms accepted | **BUG (reproduced)** | **LOW-MED** | Claude |
| 8 | Null-crossing detector | **SOUND** (2 attacks failed) | — | Claude |
| 9 | HR→OR recovery mixing | **NOT REACHED** | — | — |

**Decorative gates found: 9** — `regression_check.py` (proven by execution) + 8 further
scripts that emit `[BLOCK]`/`GATE:`/`ship-gate` language with no `sys.exit` anywhere.

---

## TARGET 1 — the card↔object guard

The file named in the brief (`check_card_object_consistency.py`) **does not exist** on
either drive. The shipped guard is `F:\rapidmeta-finerenone\scripts\assert_count_effect_consistency.py`
(171 lines) over the contract module `scripts/count_consistency.py`. Findings below are
against those.

The guard is genuinely well-built — real `sys.exit(main(...))`, real CLI args, fail-closed
on parser drift, quoted/unquoted key tolerance, leading-dot decimals. It is **not** the
`regression_check.py` pattern. Its defect is the opposite kind: it is strict about what it
checks and silent about what it doesn't.

### 1a — BUG (HIGH): the ship-gate violates its own dependency's documented contract

`count_consistency.py:69-74` states the contract explicitly:

> `None` — undetermined (missing counts/effect, non-ratio measure, or either side lands in
> the neutral band); **callers treat None as "cannot verify" — NOT as a pass.**

The ship-gate does exactly the forbidden thing:

- `assert_count_effect_consistency.py:137` — `if None in (tE,tN,cE,cN,pubHR): continue`
  (silent skip, no record, no counter)
- `assert_count_effect_consistency.py:141` — `if cc.consistent(...) is False:` — so `None`
  is not a violation
- `assert_count_effect_consistency.py:166` — falls through to
  `print(f"[OK] no count/effect contradictions across {checked} file(s) scanned")`

`checked` is `len(paths)` — **files**, not trials. The gate's success line reports the
denominator of files scanned, which reads as full coverage, while the trial-level
denominator it actually adjudicated is never printed.

**Codex (openai) reached the identical verdict independently**, citing
`count_consistency.py:69-74` vs `assert_count_effect_consistency.py:135-136,166`, and
verified it by execution. Verdict: contract violation, cross-vendor confirmed.

### 1b — BUG (HIGH): quantified — the guard adjudicates 29.8% of the corpus

I ran the guard's own parser as a library over all 1215 live `*_REVIEW.html` in
`F:\rapidmeta-finerenone` and instrumented what it decides vs. skips:

```
FILES SCANNED:                   1215
trials found in realData:        2802
  CHECKED_pass                    835
  CHECKED_violation                 1
  SKIPPED_missing_field          1544
  SKIPPED_undetermined (None)     422
      -> effect in neutral band   172
      -> counts in neutral band   115
      -> non-ratio measure        120
      -> other                     15

ACTUALLY ADJUDICATED:  836/2802 =  29.8%
SILENTLY UNVERIFIED : 1966/2802 =  70.2%

missing-field breakdown: tE 890, cE 895, publishedHR 745, tN 263, cN 266
```

**This is the answer to the brief's question.** The guard's "0 false positives / 1 finding"
is purchased with **1966 trials it never evaluated and never counted**. The 1544
missing-field skips are dominated by *arm-event fields missing while an effect is present*
(tE 890, cE 895) — which is precisely the "count beside a total HR" shape the brief asked
me to quantify. Those trials cannot be flagged by construction, and nothing in the output
tells an operator they were skipped.

**Mitigating fact (reported to avoid overclaiming):** the *generator*-side helper
`count_consistency.orient_to_effect` is strict — on an unverifiable input it returns
`'blank'` and nulls all four counts, so a card generated through it never displays
unverifiable counts. But `orient_to_effect` has exactly **one** production caller:
`scripts/bulk_clone_audit_first.py:202`. Cards produced by any other generator path in
`scripts/` are backed only by the permissive ship-gate. So the exposure is real but bounded
by generator provenance, which I did not enumerate.

### 1c — BUG (MED): the neutral band is a permanent blind corridor

`count_consistency.py:22` — `_LO, _HI = 0.87, 1.15`. `side()` returns `0` inside that band,
and `consistent()` returns `None` whenever *either* side is neutral. So a genuine
card↔object contradiction that straddles the band is unflaggable. Both vendors produced a
breaking input, by different routes:

**Claude's input** (counts neutral, effect directional):
```
tE=114, tN=1000, cE=100, cN=1000   -> impliedRR = 1.1400, side = 0
published effect HR = 0.86         -> side = -1
cc.consistent(...) = None          -> gate stays silent
```
Card shows 14% *more* events on treatment; object plots a 14% *benefit*. Gate: `[OK]`.

**Codex's input** (counts directional, effect neutral):
```
tE=43, tN=100, cE=50, cN=100, measure='RR', effect=1.14
counts imply RR 0.86 (protective); effect 1.14 (harmful)
cc.consistent(...) = None          -> gate stays silent
```

172 live trials have their effect inside this band and 115 have their counts inside it.

Note `orient_to_effect` *does* blank Claude's input (returns `'blank'`) — again, the
generator is strict where the gate is permissive.

---

## TARGET 2 — bias engine `bias-adjusted-nma-adv` (READ-ONLY)

Source recovered from `C:\Projects\bias-shadow-2026-07-17\engine_snapshot\engine.tar`
(the `src/` beside it is empty). Extracted to scratchpad; tarball untouched.

### 2a — null-crossing detector: **SOUND**

`pairwise.py:518-522`:
```python
methods_crossing_null = tuple(
    item.method for item in passed
    if item.ci_low is not None and item.ci_high is not None and item.ci_low <= 0.0 <= item.ci_high
)
```

Two attacks, both failed:

1. **False-fire via `None` CI inflating the denominator.** Hypothesis: a fit with
   `status=="passed"` but `ci_low=None` would inflate `len(passed)` without being able to
   join `methods_crossing_null`, firing "Null-crossing status differs" spuriously.
   **Refuted:** `pairwise.py:477` sets `ci_low=None` only in the *failed* branch;
   `pairwise.py:490-493` always sets `ci_low=float(result.ci_low)` when `status="passed"`.
   The `None` guard is unreachable for passed items. No false fire.
2. **Missed crossing.** The predicate is exact and total over passed items.

**Latent (not a bug today):** `<= 0.0 <=` hard-codes the *log*-scale null. Nothing asserts
the scale. It is internally consistent — `pairwise.py:281` builds the CI as
`estimate - critical*se`, a normal approximation only valid on the log scale — but the
invariant is undocumented and unasserted. Any future caller passing ratio-scale effects
would silently invert every significance verdict. Worth an assertion; not a live defect.

### 2b — `sponsor_bias.py`: **BUG (MED-HIGH)** — fail-open on a registered trial

The brief asked whether fail-closed holds on every path. It does not.

`sponsor_bias.py:52-55`:
```python
if meta["sponsor_class"] == "industry":
    return 1.0
return 0.0            # <-- the fail-OPEN branch
```

`sponsor_class` is matched by **exact string equality** after `.strip().lower()`. Any value
that is not literally `"industry"` returns `0.0` = zero bias risk. Real registry values
that miss: `"Industry/Other"`, `"INDUSTRY_COLLAB"`, `"Pharma"`, `"industry sponsor"`,
`""`, `"unknown"`, and AACT's `OTHER`, `NETWORK`, `INDIV`, `FED`, `UNKNOWN`.

**The inversion is the finding.** An *unregistered* trial returns `1.0` (fail-closed,
`sponsor_bias.py:47-49`). A trial that IS registered with an unrecognized class string
returns `0.0`. So **registering a trial with a sloppy sponsor string is safer for the
sponsor than not registering it at all** — the guard rewards bad metadata.

**Why this ships a wrong number.** Per `bias-channel-inert-on-cardiology`, a *uniform*
industry `×0.80` is inert on point estimates — every study down-weighted equally cancels in
the weighted mean. This bug destroys that protection: it makes the down-weight
**differential**, applying `×0.80` to trials whose class string happens to match and `×1.00`
to otherwise-identical industry trials whose string doesn't. Differential weights *do* move
the pooled estimate. The bug converts a provably inert channel into an actively biased one,
in the direction of favouring whichever industry trials have untidy metadata.

`adjust_doi_welton_quality` (`sponsor_bias.py:69-71`) then applies the miss straight into
the quality weight. Attrition side is fine: an unregistered trial yields `LAR=1.0` → the
full `0.30` penalty (fail-closed, correct). `calculate_attrition_ratio`'s
`meta["randomized"] == 0` branch is dead — `register_trial_flow:23` already rejects
non-positive `randomized`.

### 2c — `rapidmeta_adapter.py`: **BUG (HIGH)** — malformed input becomes a wrong 2×2

The adapter is otherwise a good fail-closed gate: schema-version pinned, `events > n`
rejected, bools rejected as ints, negative ints rejected, non-digit strings rejected,
protocol-only source types rejected, `analysis_id` required when ambiguous. Those all held
under attack.

**It does not check `arm_id` uniqueness.** `data.py:171-178`, `add_arm` assigns into a dict
keyed `(study_id, arm_id)` — a duplicate **silently overwrites**. But `add_outcome_ad`
(`data.py:180+`) **appends to a list**. The two diverge. Reproduced:

```
INPUT (passes every adapter check):
  arms: [ {arm_id:"A", treatment_id:"drug",    n:100, events:10},
          {arm_id:"A", treatment_id:"placebo", n:100, events:50} ]

RESULT: ACCEPTED -> arms=1  outcome_records=2
  arm:     ('S1','A')  treatment=placebo  n=100      <-- drug arm ERASED
  outcome: A value=10.0
  outcome: A value=50.0                              <-- both events on the placebo arm
```

The treatment arm is gone. Both event counts now attach to a single arm labelled
`placebo`. Any downstream per-arm aggregation reads 60/100 for placebo and nothing for
drug. This is exactly the brief's "plausible-but-wrong 2×2 slipping the fail-closed gate" —
it passes `len(arms) >= 2`, passes `events <= n`, and emerges structurally corrupt.
Severity HIGH: silent, direction-changing, and no error is raised at any layer.

**Fix shape (not applied — read-only lane):** reject duplicate `(study_id, arm_id)` in
`add_arm`, and assert `len(dataset.arms) == len(arms)` in the adapter after the loop.

**SOUND under attack:** `n=0` is correctly rejected downstream —
`ValidationError: Arm sample size 'n' must be > 0.` The adapter itself permits it
(`_required_non_negative_int`), but `data.py` fails closed. Defense-in-depth held here.

### 2d — adapter: **BUG (LOW-MED)** — self-comparison accepted

Same reproduction harness:
```
arms: [ {arm_id:"A", treatment_id:"drug", n:100, events:10},
        {arm_id:"B", treatment_id:"drug", n:100, events:50} ]
-> ACCEPTED, arms=2, both treatment_id="drug"
```
A contrast of a treatment against itself enters the network. In an NMA this creates a
self-loop with a large spurious "effect" (10/100 vs 50/100) attributed to a single node.
No check on `treatment_id` multiplicity within a study.

### 2e — zero-cell 0.5 correction: **SOUND**

`count_consistency.py:44-47`. Applied **only** when exactly one arm has zero events;
genuine double-zero returns `None`. Uses Haldane-Anscombe `((tE+0.5)/(tN+1))` — i.e. the
denominator is corrected too, which is the correct form. It is not applied when no cell is
zero, so it does not bias OR toward 1 on complete tables. It is applied symmetrically to
whichever arm is zero, so it does not select which arm looks favorable. Attack failed.

---

## TARGET 3 — the join (`crosswalk_fda_nct.py`)

`F:\allmeta\regulatory\crosswalk_fda_nct.py` (188 lines). The brief's `refmatch.py` at
`F:\allmeta\oa68k\refmatch.py` is a *citation* matcher (surname/year), not the NCT↔FDA
join — different component.

**Compound+code IS enforced, and well.** `drug_nct_set` (line 96) is a real validation gate
using name-union-MeSH via `nct_resolve`, and its docstring anticipates exactly the attack I
was sent to run ("a generic protocol token 'C109' matches an unrelated trial's secondary
id"). Cross-drug collisions are caught: `rejected_by_gate` is populated and printed. This
target is more defended than the brief assumed.

**BUG (MED) — two residual holes:**

1. **No ambiguity check.** Line 163: `kept = sorted(cands & gate)`. If one protocol id
   resolves to **multiple** NCTs that *all* pass the drug gate, every one of them is kept:
   `cw[pid] = {"ncts": kept, ...}`. There is no `len(kept) == 1` assertion, no ambiguity
   flag, and no rejection. Downstream consumers taking `ncts[0]` get an arbitrary pick.
   This is "unambiguous is not correct" one step worse — **ambiguous and not marked as
   such**. The drug gate cannot disambiguate *within* a drug's own programme (a phase-2 and
   its extension sharing a token both pass).

2. **Date is not enforced anywhere.** The brief asked whether compound+code+**date** is
   enforced at every call site. `date`/`year` appears nowhere in the resolution path. The
   join is compound+code only. Combined with (1), a within-drug token collision has no
   remaining discriminator.

Token floor is `len(tok) >= 4` (lines 53, 89) — so 4-char tokens like `C208`, `C209` and
bare numeric cores like `0104` (stripped from `GS-US-292-0104` by `variants()`) are live
match keys.

**Not measured live.** The two JSON outputs present in that directory (`avandia.json`,
`rosi_probe.json`) do not carry the `crosswalk` structure, so I could not count how many
real protocol ids currently resolve to >1 NCT. The finding is confirmed by reading, not by
corpus measurement — flagged as such deliberately.

---

## TARGET 4 — HR→OR recovery mixing: **NOT REACHED**

I did not locate the integration lane's HR→OR recovery code within this session, so I am
**not** reporting a verdict. Treating this as "no bug found" would be a false green.

One relevant data point: `rapidmeta_adapter.py:76` hard-rejects anything but
`measure_type == "binary"`, so the *adapter* path cannot admit an HR-native estimate
alongside recovered counts. That closes one route; it says nothing about the recovery
pipeline itself. **This target needs a second pass.**

---

## TARGET 5 — the regression gate: **DECORATIVE, PROVEN BY EXECUTION**

`F:\rapidmeta-finerenone\scripts\regression_check.py` (127 lines). The HARMONY lane's
report is correct and I reproduced it end-to-end.

**Proof — full scale, on the real repo.** I ran the unmodified script in place against
`F:\rapidmeta-finerenone` with no server listening on `localhost:8787`, i.e. the worst
possible outcome: every app in the live corpus failing even to load.

```
Regression checking 1215 apps
page_errors:          1215/1215     <-- EVERY app failed
no_trials:               0/1215
zero_included:           0/1215
no_rob_banner:           0/1215
wrong_protocol_link:     0/1215
no_webr_tag:             0/1215
pool_broken:             0/1215
fully_ok:                0/1215     <-- NOTHING passed
stderr: 0 bytes
EXIT=0
```

**0/1215 healthy, 1215/1215 broken, empty stderr, exit 0.** The script has no `sys.exit`, no
`raise`, no `main()`, and no non-zero path anywhere in 127 lines. It is structurally
incapable of failing. This is `green-count-is-the-defect` in its purest form: the gate that
"passed" at 0/1522 fully-ok did not pass — it merely finished.

(A bounded n=2 scratchpad replication gave the identical result before this full run
completed. The full-corpus run above is the primary evidence.)

Three further defects in the same file:

- **Scope misreported ~23×.** Docstring line 2 says "all 53 apps"; line 32 globs
  `*_REVIEW.html`, which is **1215** files in the live repo — confirmed by the run above,
  which self-reports "Regression checking 1215 apps". The HARMONY lane measured the healthy
  path (with a server, 2 page loads + ~4.5s of waits per app) at ~4h, which is why
  `SKIP_REGRESSION=1` gets used. My run was fast only because `ERR_CONNECTION_REFUSED`
  returns immediately — the failure path is not representative of runtime.
- **Dead `SKIP` set.** Line 30 defines `SKIP = {...}` and it is **never referenced**. The
  names in it wouldn't match the `*_REVIEW.html` glob anyway. Dead code implying a filter
  that does not exist.
- **No CLI args.** Cannot be scoped to one app, which is the direct cause of the skip-flag
  workflow.
- **Writes `/tmp/regression_results.json`** (line 125) — a POSIX path on a Windows repo.

**Severity scoping (honest).** `F:\rapidmeta-finerenone\.git\hooks\` contains **no hooks at
all** — not this script, not Sentinel. So this gate is not wired into pre-push, and its
practical harm is *false assurance to a human operator reading its output*, not a broken CI
blocker. That absence is itself worth flagging: the live corpus repo has **zero pre-push
enforcement**, and Sentinel — described in `rules.md` as active in ≥10 repos — is not
installed here.

### The other 8 decorative gates

Scripts in `scripts/` that emit `[BLOCK]` / `GATE:` / `ship-gate` language while containing
no `sys.exit` on any path:

```
aact_outcome_concordance_check.py     adjudicator.py
build_5_topics_40_44.py               bulk_clone_audit_first.py
claims.py                             count_consistency.py
inject_claim_button.py                r_validate_dta.py
```

`count_consistency.py` is a library, so its inclusion is expected — the CLI wrapper holds
the exit. The others print blocking language from a process that always returns 0. I did
not verify each is *intended* as a gate rather than a report; the count of scripts that
**claim** to block and **cannot** is **9 including `regression_check.py`**.

A broader sweep (any `*check*`/`*audit*`/`*gate*` script with no `sys.exit`) returns 40+,
but most of those are genuinely reports and I am not counting them as gates — that would be
the inflated number, not the true one.

---

## What I could not break

Reported so the coverage is legible, per the brief's "if you find nothing, your attack was
too soft" instruction — these are attacks that ran and **failed**:

- Null-crossing detector: 2 attacks, both refuted at source (§2a).
- Zero-cell 0.5 correction: symmetric, conditional, denominator-corrected (§2e).
- Adapter `n=0`: rejected by `data.py` even though the adapter permits it (§2c).
- Adapter type confusion: bools, floats, negatives, non-digit strings all rejected.
- Adapter `events > n`: rejected (control case, confirmed the harness was live).
- Cross-drug token collision in the join: caught by a real, well-reasoned drug gate (§3).
- The card↔object guard's *parser*: fails closed on parser drift (non-empty `realData`
  parsing 0 entries is a COVERAGE violation, not a pass) — a genuinely good design.

---

## Recommended order of repair

1. **§1a/§1b** — make the ship-gate print the *trial* denominator and treat `None` as
   `UNVERIFIED`, not pass. Today's `[OK] ... across 1215 file(s)` covers 29.8% of trials.
   This is one print statement away from being honest, and it is the single highest-value
   fix on this list.
2. **§2c** — reject duplicate `(study_id, arm_id)` in `data.py:add_arm`. Silent arm erasure
   with a direction flip is the worst failure mode found.
3. **§2b** — `sponsor_bias` must fail closed on any unrecognized `sponsor_class`, or
   normalize against an explicit AACT class vocabulary. Currently it un-inerts a channel
   that was safe precisely because it was uniform.
4. **§5** — give `regression_check.py` a `sys.exit(1)` and `argparse`, or delete it. A gate
   that cannot fail is worse than no gate: it produces a green line in a log.
5. **§3** — assert `len(kept) == 1` or emit an `ambiguous` flag; add year as a third
   discriminator.
6. **§4** — second pass required; not attacked.

**No green count is claimed anywhere in this report.** Every BUG above has a reproducing
input or a cited unreachable path; every SOUND verdict names the attack that failed.

---

## ⚠️ CORRECTION 2026-07-18 (REMEDIATION lane) — "9 decorative gates" is **4**

This report's headline count is **over-stated by ~2×**, and the report itself flagged the
risk: *"I did not verify each is intended as a gate rather than a report."* That verification
has now been done, file by file. **Honest count of scripts that claim to block and cannot: 4.**

| # | file | claims to block? | verdict |
|---|---|---|---|
| 1 | `regression_check.py` | yes (proven by execution) | ✅ **GENUINE — fixed** |
| 2 | `aact_outcome_concordance_check.py` | line 1: *"6th ship-gate"* | ✅ **GENUINE — fixed** |
| 3 | `r_validate_dta.py` | prints `[FAIL]`, counts `n_fail` | ✅ **GENUINE — fixed** |
| 4 | `bulk_clone_audit_first.py` | `# --- Triple ship-gate ---` | ⚠️ **PARTIAL — fixed** |
| 5 | `adjudicator.py` | no — hit was a `PROPAGATE:` print | ❌ **not a gate** |
| 6 | `claims.py` | **no blocking language at all** | ❌ **library** |
| 7 | `count_consistency.py` | library; report already conceded | ❌ **library** |
| 8 | `inject_claim_button.py` | **no blocking language at all** | ❌ **mutator** |
| 9 | `build_5_topics_40_44.py` | **already has `sys.exit`**; docstring merely *references* running a ship-gate afterwards | ❌ **builder** |

**#4 deserves partial credit the report did not give it.** `bulk_clone_audit_first.py`'s
triple ship-gate **does act** — a failing clone is physically moved to `QUARANTINE` and
logged. It was never fully decorative. Its real defect was narrower: the *process* always
returned 0, so a CI step could not tell that N clones had been quarantined. Fixed by
surfacing `qfail`/`err`/`build_none` in the exit code.

⭐ **This correction does not weaken the report's central finding.** `regression_check.py`
was decorative, was proven so by execution at full scale, and the proof stands. Over-counting
the *number* of such gates is the same species of error the report exists to catch — a count
asserted from a grep whose scope was not verified — so it is corrected here rather than
quietly carried.

### One further correction, in the report's favour

§3's join finding was reported as **"Not measured live."** It has now been measured:
`crosswalk_fda_nct.py` run over its current 4-drug frame resolves **0 ambiguous protocol
ids** — every resolved id maps to exactly one gate-passing NCT. **The hole is real in code
and currently unexercised on this frame.** It is now flagged (`ambiguous`, `n_candidates`
per entry) and blockable (`--strict`), so a consumer can no longer take `ncts[0]` from an
ambiguous set silently. Date is still **not** enforced — noted in code, not faked.

---

# APPENDIX — PUSH-GATE SEEDED-DEFECT RE-ATTACK (2026-07-18, final round)

**Rule:** a fix clears ONLY if my seeded defect makes the check **FAIL**. A check that passes
the happy path but does not block the bad case is decorative and does not clear.
**Mode:** VERIFY-ONLY. Seeding done on scratchpad copies; no repo file modified.

## PASS/FAIL TABLE

| Fix claimed | Seeded defect | Check blocks it? | Verdict |
|---|---|---|---|
| **HARMONY C208-class number correction** + `tests/test_harmony_composite_checksum.py` | `allOutcomes[]` CVD `102/109`→`113/130`, ACM `196/205`→`196/218` | **YES — 5 tests fail, exit 1** | ✅ **PUSH-ELIGIBLE** |
| **`regression_check.py` gate** | page-error injected into a real app | **YES — exit 1**, plus exit 2 on zero-match | ✅ **PUSH-ELIGIBLE** (condition below) |
| **Guard denominator fix** | n/a — reporting fix, verified by output | true exit 1; honest denominator | ✅ **PUSH-ELIGIBLE** |
| **FE banner drop** | k=2 wide-CI record; FE excludes null, DL/PM/REML all cross | **NO — still FLAGS "estimator-sensitive"** | ⛔ **NOT ELIGIBLE — not landed** |
| **TIRZEPATIDE CI** | n/a — inspected live file | `hrLCI:65.15 / hrUCI:82.51` still shipped | ⛔ **NOT ELIGIBLE — not landed** |
| **3 ex-decorative gates** (`aact_outcome_concordance_check`, `bulk_clone_audit_first`, `r_validate_dta`) | not seeded (time) | `sys.exit(main())` added, mtime 14:11 | ⚠️ **NOT CLEARED — untested** |

---

## ✅ HARMONY checksum test — PUSH-ELIGIBLE (the strongest fix of the round)

Values on HEAD are now correct, and the new 179-line test **bites**. I copied the test plus
the app into scratchpad (`APP = Path(__file__).resolve().parents[1] / "GLP1_CVOT_REVIEW.html"`,
so a scratchpad tree redirects it cleanly) and re-seeded the exact original defect,
byte-preserving (`latin-1`, `newline=""`):

```
SEEDED: CVD 102/109 -> 113/130 ; ACM 196/205 -> 196/218

FAILED test_outcome_counts_match_the_fix[ACM]
FAILED test_outcome_counts_match_the_fix[CVD]
FAILED test_composite_checksum[tE]
FAILED test_composite_checksum[cE]
FAILED test_card_and_object_agree          <-- the card↔object detector fires
5 failed, 7 passed        pytest exit = 1
```

Both checksum arms fail **and** `test_card_and_object_agree` fires — the test catches the
defect class by two independent routes, not one. Baseline on the fixed file: `12 passed`.

*(My seeding script asserted the replacement was not a no-op and would have aborted with
exit 9 — guarding against the `re-sub-silent-noop` trap, where a find/replace on an absent
needle reports success having changed nothing.)*

---

## ⛔ FE banner drop — NOT LANDED, and I have the reproducing case

`C:\Projects\bias-shadow-2026-07-17\build_transparency_ledger.py` mtime **10:43** — untouched
this round. Line **112** still iterates `for m in ('FE', 'DL', 'PM', 'REML')`, line **121**
repeats the four-tuple, and the flag string still reads *"the four conventions DISAGREE"*.

**Seeded k=2 wide-CI record** — FE (which ignores τ², so is narrower by construction)
excludes the null; all three random-effects conventions cross it:

```
FE   est -0.22  CI [-0.40, -0.04]  tau2 0.00   <- excludes null
DL   est -0.22  CI [-0.60,  0.16]  tau2 0.09   <- crosses
PM   est -0.22  CI [-0.64,  0.20]  tau2 0.11   <- crosses
REML est -0.22  CI [-0.62,  0.18]  tau2 0.10   <- crosses
```

Run through `estimator_decision()`:

```
WITH FE (current code):
  "FLAGGED - the four conventions DISAGREE on whether the effect crosses the null
   (crossing under: DL, PM, REML). Read this pooled result as estimator-sensitive."

WITH FE DROPPED (the claimed fix):
  "none - all four conventions agree the interval crosses the null (not significant)."
```

**The flag is driven entirely by FE.** Every random-effects convention agrees; only the
fixed-effect estimator dissents, and it dissents *by construction* because it ignores
heterogeneity. This is exactly the brief's disqualifying case — a k=2 wide-CI result labelled
"estimator-sensitive" when no random-effects estimator disagrees. **NOT FIXED.**

⚠️ **Bug the fixer will otherwise ship:** the two "all four conventions" strings at lines
121–124 are hard-coded. Dropping FE leaves three, and the message becomes false. **Fix the
string with the loop, or the fix ships a wrong count in user-visible copy.**

---

## ⛔ TIRZEPATIDE CI — NOT LANDED

`TIRZEPATIDE_ARDS_AUTO_FULL_REVIEW.html`, mtime **Jul 14** (untouched this round), still ships:
```
hrLCI:65.1542   hrUCI:82.5058
hrLCI:67.5193   hrUCI:78.7807
```
**A hazard-ratio CI cannot be [65.15, 82.51].** These are almost certainly percentages written
into ratio fields (a 73.8% [65.2, 82.5] shape). Any pooling that reads `hrLCI/hrUCI` as a
ratio interval will produce a nonsense weight — this is a live wrong-number defect on the
clickable surface, not cosmetic. **BLOCKED.**

---

## ⚠️ The three ex-decorative gates — exit added, NOT CLEARED

`aact_outcome_concordance_check.py`, `bulk_clone_audit_first.py`, `r_validate_dta.py` — all
gained `sys.exit(main())` at mtime 14:11 (and `bulk_clone_audit_first.py` gained argparse).
**I did not seed-test them and they therefore do not clear.** Adding `sys.exit(main())` proves
a non-zero path *exists*; it does not prove `main()` ever *returns* non-zero on a bad input —
which is precisely the distinction this whole lane is about. **Each needs: seed the defect it
claims to catch, confirm exit ≠ 0.** Until then they are "exit present, bite unproven."

The remaining 5 of my original 9 decorative gates are untouched.

---

## PUSH-ELIGIBLE SET

**Clear to push:** HARMONY correction + checksum test · `regression_check.py` (conditional:
gitignore `regression_results.json`, which `--json-out` still defaults inside the repo and
`git check-ignore` confirms is untracked) · guard denominator fix.

**Blocked:** FE banner drop (reproducing false-flag above) · TIRZEPATIDE CI (live nonsense
ratio bounds) · 3 gates (untested) · 5 gates (untouched) · the 7 code bugs from the main
report (none landed).

**Also still standing from the push-gate round:** do not claim corpus health — the fixed gate
found 5 genuinely defective apps in 50 with a server up.

**Score: 3 of 6 claimed fixes push-eligible.** Two are demonstrably not landed despite being
claimed, and one is untested. I did not clear anything on inspection alone — every clear here
has a seeded defect that made the check fail.
