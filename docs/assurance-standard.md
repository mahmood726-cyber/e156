# The e156 Assurance Standard

> *The capsule must agree with itself before asking the world to agree with it.*
> *No test, no trust. Every claim must carry its own means of being checked.*

## Why this standard exists

Without self-checking, an e156 paper can be dismissed as "too short" or "too fast". With self-checking, e156 becomes something stronger: **a short scholarly claim attached to a tested evidence object**. That is the difference between micro-publishing and audited micro-scholarship.

A conventional paper often has hidden inconsistencies — abstract says one number, results table says another, forest plot has a third, conclusion overstates the actual result, references don't match citations. Internal consistency checks catch these systematically. A human reviewer asks "does this seem reasonable?" — the internal checker asks "does this exact number appear everywhere it should, and nowhere it should not?"

This is not about replacing expert judgement. It is about removing avoidable errors before expert judgement is used, so reviewer time focuses on higher-level questions: is the clinical question worth publishing, is the interpretation fair, are the limitations honest, is the evidence useful, is the e156 wording clear.

## Four risk classes, four checks

| Risk | Built-in check |
|---|---|
| **Made-up citations** | Citation verifier (CrossRef / Semantic Scholar / OpenAlex / source PDF cascade) |
| **Data extraction errors** | Data/provenance validator (row-level source-tracing) |
| **Analysis errors** | Reproducibility test (actual rerun of the analysis pipeline) |
| **Overclaiming** | Claim-language checker |

### 1. Citation verification (essential)

Every citation in the e156 paper and capsule is checked against CrossRef, PubMed, DOI, OpenAlex, or the source PDF. The system asks:

- Does this citation exist?
- Does the DOI resolve?
- Do title/authors/year match?
- Is the cited paper actually about the claim?
- Is the citation used correctly?
- Are there duplicate or irrelevant references?
- Are any references hallucinated?

**A made-up citation is an automatic fail.**

### 2. Data checking

For each extracted number, the capsule records: `source paper → page/table/figure → extracted value → transformed value → analysis input`. Then the validator checks:

- missing values; impossible numbers; mismatched denominators
- event counts greater than sample size; duplicated study names
- inconsistent follow-up times; wrong treatment/control direction
- unit errors; impossible confidence intervals
- data not traceable to a source

This is where e156 becomes safer than long-form writing — the short claim is only allowed after the data have passed checks.

### 3. Analysis checking

The analysis reruns automatically. The test confirms:

- same pooled estimate; same confidence interval; same heterogeneity; same model choice; same sensitivity result
- dashboard matches the analysis; e156 text matches the dashboard

If the paper says OR 0.78 but the rerun gives OR 0.87, it fails.

### 4. Claim-language checking

The system flags words like *proves, confirms, eliminates, safe, effective, no difference, definitive, significant benefit*. Then it checks whether the data actually justify that language:

- high heterogeneity → conclusion must be cautious
- wide CI → conclusion must mention uncertainty
- few studies → conclusion must be limited
- observational evidence → no causal overclaim
- risk of bias concerns → no strong certainty language

This is moral protection against exaggeration, not just grammar.

## Ten internal-consistency checks

| Check | Question it asks |
|---|---|
| Paper–dashboard match | Do the numbers in the e156 match the dashboard? |
| Dashboard–analysis match | Was the dashboard generated from the same analysis output? |
| Analysis–data match | Can the result be regenerated from the stored dataset? |
| Data–provenance match | Does each extracted number trace back to a source? |
| Claim–certainty match | Is the conclusion cautious enough for the evidence? |
| Reference–citation match | Do all citations exist and match their metadata? |
| Directionality check | Is benefit/harm/control/treatment direction consistent? |
| Denominator check | Are events, totals, and sample sizes logically possible? |
| Unit check | Are units consistent across studies? |
| Version check | Does the PDF match the released capsule version? |

## Three-tier badge

The internal-consistency report is visible inside every capsule so authors, reviewers, editors, and readers can immediately see how much reassurance the object carries.

**Bronze e156 — basic reproducibility**
- data file present
- code runs
- dashboard generated
- citation links valid

**Silver e156 — audited reproducibility**
- row-level provenance
- automated tests passed
- claim matches output
- limitations checked

**Gold e156 — independent verification**
- second reviewer checked extraction
- independent rerun passed
- citation/source audit passed
- correction/version policy active

## The `assurance.json` schema

Every e156 submission folder may contain an `assurance.json` file that drives the badge rendering on the paper page. Phase 1 of the standard ships this schema and a renderer that displays the right pill if the file exists; the file is populated manually for now. Phase 2 will auto-populate from Sentinel rule verdicts (citation_cascade, claim_language, denominator_logic) and Overmind witness verdicts.

```json
{
  "tier": "bronze | silver | gold | none",
  "checks": {
    "citation_cascade":  "pass | warn | fail | not-run",
    "denominator_logic": "pass | warn | fail | not-run",
    "claim_language":    "pass | warn | fail | not-run",
    "data_file_present": "pass | fail",
    "code_runs":         "pass | fail | not-run",
    "dashboard_match":   "pass | warn | fail | not-run",
    "analysis_rerun":    "pass | warn | fail | not-run",
    "external_review":   "pass | warn | fail | not-run"
  },
  "evidence": {
    "sentinel_findings": "path/to/sentinel-findings.jsonl",
    "overmind_bundle":   "path/to/<id>.json",
    "reviewer_note":     "optional free-text or path to a markdown attestation"
  },
  "tier_rule": "bronze = (citation_cascade != fail) AND data_file_present == pass AND code_runs in (pass, not-run); silver = bronze + dashboard_match == pass AND claim_language == pass; gold = silver + analysis_rerun == pass AND external_review == pass",
  "issued_at": "ISO-8601 timestamp",
  "issued_by": "operator email or agent ID",
  "version": 1
}
```

### Tier-derivation rules

- **Bronze** requires the first four checks to pass (or be `not-run` only if `code_runs` is `not-run`).
- **Silver** additionally requires `dashboard_match == pass` and `claim_language == pass`.
- **Gold** additionally requires `analysis_rerun == pass` and `external_review == pass`.
- Any single `fail` in a contributing check forces the tier to `none` regardless of other check states. Honest under-claiming is the safer error.

### Where it lives on disk

For a project at `F:\<project>\` whose submission is in `F:\<project>\e156-submission\`:
```
F:\<project>\e156-submission\
  config.json            (existing — submission metadata)
  assurance.json         (new — tier + check verdicts)
```

For a paper rendered into the e156 board:
```
F:\e156\paper\<N>.html   (renderer reads ../<project>/e156-submission/assurance.json
                          via the resolution from rewrite-workbook.txt PATH line)
```

## What Phase 1 ships (2026-05-24)

- This document.
- The JSON schema above.
- A memory entry (`<claude-config>/projects/<project-slug>/memory/e156_assurance_standard.md`) so future sessions don't lose the vocabulary.
- Three new Sentinel rules — `citation_cascade`, `claim_language`, `denominator_logic` — that emit `pass / warn / fail` verdicts to the `checks` block.
- A small edit to `scripts/build_paper_pages.py` that renders a Bronze/Silver/Gold pill on the paper page when an `assurance.json` exists.

What Phase 1 does NOT ship: auto-population of `assurance.json` (operator hand-writes for now), the analysis-rerun check (needs cached datasets + pinned environments), the paper-dashboard value match (needs cross-format number extraction), the PDF-output match. Those are Phase 2.

## v0.3 additions (2026-05-28) — credibility for people other than the author

v0.2 (everything above) makes a capsule *agree with itself*. A capsule can be
perfectly self-consistent and still wrong, so v0.3 adds the layer that earns
*outside* trust. v0.2 semantics are unchanged; these are additive.

### Precise terminology (NISO / ACM)

The standard adopts the harmonised NISO/ACM vocabulary so methodologists read it
the same way the rest of computational science does:

- **Reproduction** = the *same* analysis artifacts (data + code) produce the
  same result. e156's `analysis_rerun` check (re-running the pipeline) and the
  `pooled_recompute` rule (re-pooling the stored `realData`) are reproduction.
- **Replication** = an *independent* team, with independently obtained
  materials, reaches a consistent finding. e156 does not claim to perform
  replication; it can only record when a replication exists.

Do not say "independent rerun" for same-artifact re-execution — that is
reproduction. Reserve "independent" for the reproduction badge below.

### Independent reproduction is an orthogonal badge, not a higher rung

The Bronze/Silver/Gold ladder measures *artifact quality* (does the object hold
together and reproduce from its own materials). **Who verified it** is a
separate axis, modelled on ACM Artifact Badging and CODECHECK: a named third
party — not the author — re-executes the capsule and signs a public,
time-stamped certificate. That is represented by the `external_review` check and
surfaced as an **"Independently Reproduced"** attestation shown *alongside* the
tier, never folded into it. Gold therefore requires the independent attestation
(`external_review == pass`), making Gold mean "someone other than the author
verified this", not "the author asserts it".

`assurance.json` gains an optional block:

```json
"independent_reproduction": {
  "reproduced": true,
  "reproducer": "name or ORCID of the third party (NOT the author)",
  "certificate": "URL or path to the signed CODECHECK-style certificate",
  "date": "ISO-8601"
}
```

### Signed badges (implemented)

A consistent badge is still forgeable by rewriting tier *and* checks together.
`scripts/assurance/sign_badge.py` binds the badge to a key holder with
HMAC-SHA256 over the canonical badge content (signature/`signed_at` excluded).
The key comes from `$E156_ASSURANCE_HMAC_KEY` or a gitignored key file and the
signer **fails closed** if no key is present — never a forgeable default
(see `rules/lessons.md` "Cryptography / Signing"). The badge gains:

```json
"signature": "HMAC-SHA256:<hex>",
"signed_at": "ISO-8601"
```

Verification (`sign_badge.py verify`) uses `hmac.compare_digest` and runs where
the key is available, not at commit time. The enforcement point is
`scripts/assurance/verify_badges.py`, run in CI with the key as a secret — it
fails the build on any forged/invalid (and, with `--require-signed`, unsigned)
badge, so the HMAC signature is load-bearing rather than decorative.

### Public verification + the GitHub pipeline (implemented)

HMAC verifies for a key holder; for *public* verifiability the
`.github/workflows/assurance.yml` workflow additionally **keyless-signs** each
badge with Sigstore `cosign` via GitHub OIDC (no key to manage). Anyone can
verify against the transparency log:

```
cosign verify-blob \
  --bundle assurance.json.cosign.bundle \
  --certificate-identity-regexp 'https://github.com/<owner>/<repo>/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  assurance.json
```

The same workflow runs the test suite (gate), resolves DOIs live against
doi.org into `doi-cache.json`, regenerates the badge (`build_assurance_jsons.py
--here`), runs the HMAC verify gate, and publishes `assurance.html` (the public
dashboard) through the repo's existing GitHub Pages. Independent reproduction
(the `external_review` / Independently-Reproduced attestation) is submitted via
the `reproduction` issue template by a third party who is not an author.

### Machine-readable research object (implemented)

`scripts/assurance/ro_crate.py` emits an RO-Crate 1.1 `ro-crate-metadata.json`
(schema.org JSON-LD) describing the capsule's parts (body, data, dashboard,
`assurance.json`, DOI, tier). This makes the capsule FAIR and tool-interoperable
instead of a private folder layout.

### Versioned DOI + correction policy

Each released capsule should carry a persistent identifier (DataCite/Zenodo
DOI). Corrections do not overwrite: a new version gets a new DOI linked to the
prior with `IsNewVersionOf` / `IsPreviousVersionOf`, and the changelog records
what changed and why. A retraction sets the capsule's status to `retracted` and
keeps the record. "Version check" (#10) is satisfied when the released PDF, the
capsule version, and the DOI version agree.

### Domain hooks (evidence-synthesis specific)

- **PRISMA 2020 / PRISMA-LSR**: the capsule carries a machine-checkable map of
  the 27 PRISMA items it satisfies; living capsules use the PRISMA-LSR flow.
- **GRADE**: the outside-note `Certainty` field uses GRADE wording
  (high/moderate/low/very-low). *(Planned)* a future `claim_language` upgrade
  will parse that structured field and flag a "high certainty" body whose
  GRADE rating is low; today `claim_language` only matches certainty *phrases*
  co-occurring with heterogeneity markers, it does not read a GRADE field.
- **RoB2 / ROBINS-I**: per-study risk-of-bias domains are recorded in
  `realData` so directionality and certainty checks can reference them.
- **PROSPERO**: a registered protocol id is recorded as a preregistration
  signal (an orthogonal practice badge, like COS "Preregistered").

## Provenance

This standard was articulated by Mahmood Ahmad (mahmood726@gmail.com) in a 2026-05-20 email and adopted into the E156 architecture on 2026-05-24. The Quranic framing — *amānah* (trust) and *muhāsabah* (self-accounting) — captures the underlying principle that the work accounts for itself before asking others to trust it.

> *The paper speaks briefly; the evidence bears witness fully.*

## See also

- `F:\e156\docs\ai-harness-breakthroughs.md` — academic grounding (arXiv citations: 2508.02994, 2605.02651, 2604.08401, 2510.18003, 2601.22297)
- `F:\Sentinel\sentinel\rules\plugins\e156_placeholder_leak.py` — the first concrete internal-consistency rule, shipped in commit `b25128b`
- `F:\e156\tests\test_no_placeholder_leak.py` — the regression-test layer of the same defense
- `F:\rapidmeta-finerenone\generate_living_ma_v13.py:42` — the `js_val()` helper that fixes the upstream None→JS leak
