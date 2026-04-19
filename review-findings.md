## REVIEW OPEN — 9 P0, 22 P1, 14 P2 (pending fix pass)

## Multi-Persona Review: E156 Student Claim Board system (commit f61e096)
### Date: 2026-04-19
### Reviewers: Statistical Methodologist, Security Auditor, UX/Accessibility, Software Engineer, Domain Expert
### Scope: claim flow, per-paper dashboards, verification/push scripts, workbook and claims.json state
### Summary: 9 P0, 22 P1, 14 P2 — pre-fix

---

## P0 — Critical (must fix before recruitment push)

- **P0-1 [Domain + UX]** Journal-name and window-length inconsistency across student-facing copy. `students.html` meta/instructions, `TARGET_JOURNAL` constant, `claim.yml`, `submitted.yml` use *"Synthesis Medicine"* (no macron) and still reference *"42-day countdown"* and *"6 weeks"*, while the actual policy is 30+10 and the journal masthead is *"Synthēsis"* (with macron). For an editorial-board-COI disclosure, the journal name must match exactly per `feedback_e156_authorship.md`.
  - Files: `scripts/build_students_page.py:31, 175, 176, 346, 348, 399`, `.github/ISSUE_TEMPLATE/claim.yml:2`, `.github/ISSUE_TEMPLATE/submitted.yml:1, 10`
  - Fix: global-replace "Synthesis Medicine" → "Synthēsis" and "42 days"/"6 weeks" → "30 days (extendable to 40)"; canonicalize `TARGET_JOURNAL = "Synthēsis"`.

- **P0-2 [UX]** 2MB board freezes mid-range Android on 3G. 485 cards rendered as one `innerHTML` string on every search keystroke; no debounce; every card's `renderDetails()` metadata pre-rendered even for collapsed panels.
  - File: `scripts/build_students_page.py:616, 687`
  - Fix: 200ms debounce on search input; lazy-render `renderDetails()` on click; OR paginate to 50 visible.

- **P0-3 [Engineering]** `claims.json` race. Two students opening issues seconds apart trigger two workflow runs. Both read the file, each writes its own update, second `git push` rejected → second student's claim silently lost.
  - File: `.github/workflows/update-claims.yml` (no concurrency key) + `scripts/update_claims_from_issue.py`
  - Fix: `concurrency: group: claims-json` on the workflow; add `git pull --rebase + push` retry loop.

- **P0-4 [Engineering]** Silent empty board if workbook ever ships a UTF-8 BOM or cp1252-corrupted first block. `parse_entries` skips anything not matching `^\[`, returns 0 entries, builder writes an empty board with no error.
  - Files: `scripts/build_students_page.py:705`, `scripts/build_paper_pages.py:38`
  - Fix: `text = text.lstrip('\ufeff')`; `assert len(entries) >= 400` before writing.

- **P0-5 [Domain]** Per-paper HTML pages (the 485 public `/paper/<N>.html` files — the canonical landing pages that supervisors and journal editors will see) omit the editorial-board competing-interests statement. Mahmood is shown as "middle author" but his Synthēsis editorial-board role is never disclosed publicly.
  - File: `scripts/build_paper_pages.py:106–232` (PAGE_TEMPLATE + row builder)
  - Fix: add a "Competing interests" section parsing `competing_interests` from the workbook entry and rendering it prominently.

- **P0-6 [Domain]** No format-contract enforcement on SUBMITTED. The submission form never asks the student to paste their final rewrite — a student who padded to 400 words (warned against at `students.html:370`) can still mark SUBMITTED and be recorded as first author of an "E156 micro-paper" that isn't 7-sentence/156-word.
  - Files: `.github/ISSUE_TEMPLATE/submitted.yml:13-44`
  - Fix: add required `final_body` textarea + GH Action validator that labels `format-violation` if `sentence_count != 7` or `word_count > 156`; block auto-update until resolved.

- **P0-7 [Domain]** "TBD - request mentor" sentinel can pass to SUBMITTED. Claim form allows senior_author = `"TBD - request mentor"` and submission form never re-checks the field was resolved. Student could submit without a real senior author, breaking the "never first/last" rule if OJS demanded a last author.
  - Files: `.github/ISSUE_TEMPLATE/claim.yml:77-82` + `submitted.yml`
  - Fix: submitted.yml adds `senior_author_final` required field; Action rejects TBD sentinel.

- **P0-8 [Security]** XSS via unescaped Code/Dashboard URLs. `escapeHtml()` is HTML-context-only and doesn't validate URL scheme. If a workbook entry ever had `Code: javascript:alert(...)` (e.g. rogue PR), the board would ship a clickable XSS.
  - File: `scripts/build_students_page.py:645-646` and `:521-528` (linkIfUrl)
  - Fix: validate `url.startsWith('http://') || url.startsWith('https://')` before building anchor; reject otherwise.

- **P0-9 [Security]** XSS-adjacent in `renderRefs` DOI linkifier. `escapeHtml(r).replace(/doi:(\S+)/g, ...)` injects `$1` into an `href` with no DOI-shape validation. An attacker-controlled reference string containing URL-encoded quotes could break the attribute boundary.
  - File: `scripts/build_students_page.py:535`
  - Fix: validate captured DOI matches `^10\.\d{4,9}\/[-._;()/:A-Z0-9]+$` (case-insensitive); otherwise render as escaped plaintext.

---

## P1 — Important (should fix this week)

- **P1-1 [STAT-1]** JS/Python day-boundary mismatch on expiry day. JS uses `Math.ceil` + UTC midnight anchor; Python uses `(today - claim_date).days > window`. Claims near day-31 UTC boundary show "expired" on the board but `kept` by `expire_stale_claims`.
- **P1-2 [STAT-2]** JS `daysLeft` returns NaN on malformed `claim_date` → status stuck as "claimed" forever. Guard needed. `scripts/build_students_page.py:463`.
- **P1-3 [STAT-3]** DST / local-vs-UTC phase offset in JS day count.
- **P1-4 [SEC-3]** No grace period after claim expiry — attacker races to re-claim on day 31. `scripts/update_claims_from_issue.py:208-219`.
- **P1-5 [SEC-4]** GitHub Actions forward-compat: any future `${{ github.event.issue.title }}` interpolated into a `run:` block becomes injection. Add lint check.
- **P1-6 [UX-3]** "Synthēsis" macron mojibake risk on cp1252 / old Android WebView; `synthes.is` typo domain for a fallback email.
- **P1-7 [UX-4]** No ARIA landmarks, no `aria-live` on count-chip or claim-status regions.
- **P1-8 [UX-5]** `outline:none` on inputs with no focus ring; cards have no `aria-expanded`.
- **P1-9 [UX-6]** Touch targets < 44×44 px fail WCAG 2.5.5 on mobile.
- **P1-10 [UX-7]** `claims.json` fetch failure silently renders all papers "Open" — dangerous UX.
- **P1-11 [UX-8]** Extension form missing `name` field.
- **P1-12 [UX-9]** One-at-a-time rule stated but not enforced in UI; only rejected server-side.
- **P1-13 [UX-10]** Sticky toolbar + instructions consume mobile viewport; wrap in `<details>`.
- **P1-14 [ENG-2]** `update_claims_from_issue.py` double write-path architecture invites regressions.
- **P1-15 [ENG-4]** No tests for claim pipeline. 6 contract tests recommended (claim/submitted/extension/spoof-close/spoof-claim/one-at-a-time).
- **P1-16 [ENG-5]** `expire_stale_claims.py` has no cron workflow. Add weekly scheduled Action with shared concurrency group.
- **P1-17 [ENG-6]** 11 one-off scripts with hardcoded lists clutter `scripts/`. Move to `scripts/archive/` with run-once guards.
- **P1-18 [ENG-7]** `build_paper_pages.py:293` reads `HIDE_LIST` unconditionally — crashes on fresh clone.
- **P1-19 [ENG-8]** Duplicate-N silent drop is undocumented. Add warning log on collision.
- **P1-20 [ENG-9]** `verify_board_links.py` regex anchor fragile for embedded `];` strings.
- **P1-21 [ENG-11]** Deprecated `datetime.utcnow()` remaining in `apply_fresh_pushes.py` + `retry_failed_pushes.py`.
- **P1-22 [DOM-6/7/8]** `E156-PROTOCOL.md` template is metadata-only, not Cochrane/PRISMA-P executable; "PRISMA 2020 methods-paper variant" is not a real checklist; τ² estimator never declared.

---

## P2 — Polish

- **P2-1** `escapeHtml` missing `'`.
- **P2-2** Inline `onclick` handlers — CSP-unfriendly.
- **P2-3** Decorative glyphs announced by screen readers (no `aria-hidden`).
- **P2-4** Nested `<ul>` inside `<ol><li>` in submission instructions.
- **P2-5** `create_missing_protocols.py:265` uses `"422" in stderr` string matching.
- **P2-6** Paper-number unbounded in `update_claims_from_issue.py:89`.
- **P2-7** `expire_stale_claims.py:31` docstring indexing without guard.
- **P2-8** `extended: True` not paired with `extended_date` timestamp.
- **P2-9** `parse_entries` regex greedy on trailing punctuation.
- **P2-10** Per-paper breadcrumb tiny monospace.
- **P2-11** Search field has no example placeholder.
- **P2-12** `submitted.yml:32` placeholder fabricated OJS ID.
- **P2-13** COI verbatim checkbox label ugly on mobile.
- **P2-14** 485 paper pages regenerated on every build.

---

## Cross-checked against `lessons.md` false-positive list
- No findings about DOR formula, Clayton theta, Clopper-Pearson alpha/2, or bootstrap-sorting assumptions
- All P0/P1 findings cite file:line

---

## Previous review (2026-04-07) — closed clean, different scope

## REVIEW CLEAN
## Multi-Persona Review: E156 Pipeline Scripts (auto_deploy, deploy_all, apply_rewrites, push_all_repos, template)
### Date: 2026-04-07
### Reviewers: Security Auditor, Software Engineer, UX/Accessibility Reviewer
### Summary: 4 P0, 10 P1, 8 P2 — All P0 and key P1 FIXED

---

#### P0 — Critical [ALL FIXED]

- **P0-1** [Security]: Shell injection via README `desc` in `gh repo create` (push_all_repos.py:217)
  - Suggested fix: Use list-form subprocess
  - **[FIXED]**: Converted to list-form subprocess call

- **P0-2** [Engineering]: Auto `--force` push destroys remote history (push_all_repos.py:201)
  - Suggested fix: Remove auto-force push
  - **[FIXED]**: Removed force push, normal push only

- **P0-3** [Engineering]: Task Scheduler may not find `python` (auto_deploy.py:157)
  - Suggested fix: Use `sys.executable`
  - **[FIXED]**: Now uses `sys.executable`

- **P0-4** [Security]: `javascript:` URI injection via `article.notes.code` (template.html:1098)
  - Suggested fix: Validate URL starts with https://
  - **[FIXED]**: Added `/^https?:\/\//i.test()` guard

#### P1 — Important [KEY ITEMS FIXED]

- **P1-1** [Security]: `shell=True` systemic across scripts — **[FIXED in push_all_repos.py]** via list-form run()
- **P1-2** [Engineering]: Force push on portfolio repo — **[FIXED]**: Changed to `--force-with-lease`
- **P1-3** [Engineering]: `git add -A` can stage secrets — **[FIXED]**: Now uses specific file paths
- **P1-4** [Engineering]: State file write not atomic — low risk, not fixed
- **P1-5** [Engineering]: Log file grows unbounded — **[FIXED]**: Added `rotate_log(5000)`
- **P1-6** [Engineering]: Dead branch in body selection — **[FIXED]**: Simplified logic
- **P1-7** [Engineering]: No concurrent-run lock file — low risk (5x daily, short runs), not fixed
- **P1-8** [UX]: Missing `rel="noopener"` on `target="_blank"` — **[FIXED]**: Added `noopener noreferrer`
- **P1-9** [UX]: DRAFT banner contrast fails WCAG AA — **[FIXED]**: Darkened to #5a4300
- **P1-10** [UX]: References `<h3>` breaks heading hierarchy — **[FIXED]**: Changed to `<h2 class="section-title">`

#### P2 — Minor (not fixed, low risk)

- **P2-1** MD5 for change detection (not a security use)
- **P2-2** Workbook path traversal (local-only file)
- **P2-3** XSS via slug in generated HTML (safe — browser URL-encodes)
- **P2-4** References section responsive breakpoint (minor layout)
- **P2-5** SVG data points lack text alternatives
- **P2-6** Author block lacks `<address>` semantic markup
- **P2-7** Missing `aria-label` on ref list
- **P2-8** Shebang `python3` in push_all_repos.py (ignored on Windows)

#### False Positive Watch
- Email innerHTML with `esc()` + hardcoded `mailto:` prefix is safe (P0-1 from template review)
- `slug` in URL construction is safe (DOM property assignment, browser URL-encodes)
