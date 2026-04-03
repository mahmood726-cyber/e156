# E156 Production Lane Status

Date: 2026-03-28

## Goal

Make the active E156 workflow explicit as:

1. papers
2. protocols and disclosure
3. HTML dashboards
4. multi-persona reviews
5. reviewed release artifacts

## Current Repository State

- Framework and spec assets exist under `docs/`, `templates/`, and `scripts/`.
- Example source JSON files: `5`
- Generated output JSON files: `8`
- Generated output HTML files: `8`
- Validation JSON files: `4`
- Review JSON files: `4`
- Review summary JSON files: `4`

## Verification Lane

The active verification commands are now:

1. local framework tests via `pytest -q -p no:cacheprovider tests/test_smoke.py`
2. generated cross-repo smoke tests via `python3 scripts/run_generated_smoke_tests.py`
3. combined verification report via `python3 scripts/run_verification_suite.py`
4. full maintenance cycle via `python3 scripts/run_maintenance_cycle.py`

The combined suite writes `verification-report.json` at the repo root and is intended to be the one-command post-repair check after audit or batch-generation work. The full maintenance cycle refreshes `audit-report.json`, reruns verification, and writes a top-level `maintenance-report.json` readiness summary.

For narrower iteration, the audit, verification, and maintenance runners now accept repeated `--project` filters plus optional caps such as `--limit` or `--max-generated`. The generated smoke-test runner also accepts `--jobs`, and verification or maintenance can pass that through with `--generated-jobs`. Example: `python3 scripts/run_maintenance_cycle.py --project ctgov --max-generated 5 --generated-jobs 4 --audit-report /tmp/e156-ctgov-audit.json --verification-report /tmp/e156-ctgov-verification.json --out /tmp/e156-ctgov-maintenance.json`.

## Current Review Gates

- `reduced-dose-doacs-vte-demo`: `pass`
- `clinical-ma`: `pass`
- `fragility-atlas`: `pass`
- `metarep`: `pass`

## Repository Assets By Stage

### Papers

- `examples/*.json`
- `output/json/*.json`
- `scripts/generate_submission.py`
- `scripts/build_e156_batch.py`

### Protocols And Disclosure

- `scripts/add_protocols_and_disclosure.py`
- optional `Protocol` field in the E156 spec

### HTML Dashboards

- `templates/e156_interactive_template.html`
- `templates/e156_editorial_template.html`
- `scripts/build_e156_bundle.py`
- `scripts/generate_dashboards.py`
- `output/html/*.html`
- `index.html`

### Multi-Persona Reviews

- `templates/multipersona_review_prompt.md`
- `templates/multipersona_review_template.json`
- `scripts/review_e156.py`
- `reviews/*.review.json`
- `reviews/*.summary.json`

## Immediate Operational Interpretation

- The E156 repo already supports the full lane end to end.
- The starter review backlog for the four tracked release artifacts is now cleared.
- The bottleneck is no longer framework design or review scaffolding; it is selecting the next article candidates to move through the lane.
- Protocol and disclosure support exists as a script, but that stage should be treated as part of the normal release lane rather than a late cleanup step.
- Dashboards are already first-class outputs and should be generated before review so reviewers assess the real publication bundle.
- The canonical output tree is now synchronized across base JSON, reviewed JSON, validation files, base HTML, reviewed HTML, and review summaries.

## Recommended Next Execution Order

1. Freeze or revise the next target article JSON.
2. Generate `protocol.md` and disclosure fields.
3. Build the dashboard HTML.
4. Complete the five-persona review JSON.
5. Attach review summary and rebuild reviewed HTML.
6. Promote only items with review gate `pass`.
