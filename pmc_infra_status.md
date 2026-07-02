# PMC Infrastructure Status — synthesis-medicine.org
Generated: 2026-06-24

---

## What was fixed automatically (this session)

### 1. JATS XML repair — 114/114 files rewritten, all well-formed

Backup location: `/var/www/files_jats_backup_20260624/` (on droplet)

| Metric | Before | After |
|---|---|---|
| Files with clean `<issn>` element | 0 | 114 |
| Files with clean `<article-id doi>` element | 0 | 114 |
| Files with real `<aff>` affiliations | 0 | 112 |
| Files with `<ref-list>` | 0 | 95 |
| ORCID placeholder comments removed | 114 | done |
| Well-formed XML (validated) | 114 | 114 |

**Articles with real affiliations now: 112/114**

Still missing affiliations (authors must supply):
- #24 (Insight) — solo author, no affiliation in OJS
- #25 (Insight) — solo author, no affiliation in OJS

**Articles with ref-lists now: 95/114**

Breakdown: 83 from OJS citations DB (articles 1–159) + 12 from original source JATS
packages (articles 160–171, which already carried complete galleys from local output
directories). Articles 160–171 were restored to their original source JATS after the
repair run attempted to add DB-sourced data on top of already-complete files.

Still zero refs (19 articles — editorial curation required):
- Synthesis: #3, #9, #23, #29, #30, #31, #41, #45, #50, #53, #68, #88, #92, #93, #107, #108
- Insight: #24, #25
- Gnosis: #19

Note: 3 of the restored 160–171 files retain a `0000-0000` ISSN placeholder (native to
their source-package JATS templates, not a comment). These will resolve on the next repair
run once a real ISSN is entered in OJS.

### 2. DOI plugin enabled for Synthēsis

`journal_settings` change on journal_id=1:
- `enableDois`: 0 → **1** (DOI assignment now active in editorial workflow)
- `doiPrefix`: 10.66040 (unchanged — was already configured)
- `automaticDoiDeposit`: 0 (unchanged — no Crossref deposits triggered automatically)
- `doiCreationTime`: copyEditCreationTime (unchanged)
- `enabledDoiTypes`: ["publication"] (unchanged)

Effect: editors can now assign DOIs to submissions via the OJS dashboard.
No DOIs have been deposited to Crossref; that step requires Mahmood's action (see below).

---

## What still needs Mahmood's action

### A. ISSN registration (BLOCKS PMC deposit for all 114 articles)

Submit applications at https://portal.issn.org/ for all 5 journals.
Full per-journal details, form fields, and URLs: `F:\E156\pmc_issn_applications.md`

Priority order:
1. **Synthesis** — ready now (publisher set, 100 articles, first issue Nov 2025)
2. **Insight** — fix publisher field in OJS first (currently "Greater Accra Regional Hospital")
3. **Gnosis** — populate publisher in OJS first (currently blank)
4. **Sapience** — populate publisher in OJS first (currently blank)
5. **Hikmah** — populate publisher in OJS first (currently blank); only 1 article so far

After receiving ISSNs: enter each in OJS (Journal Settings → Online ISSN) and re-run
the JATS repair script (`/tmp/jats_repair.py`) to fill `<issn pub-type="epub">` across all galleys.

Typical turnaround: 2–4 weeks at ISSN International. Free for online journals.

---

### B. Crossref membership + DOI deposit (BLOCKS PMC deposit)

No DOIs are assigned to any of the 114 articles yet.

Steps:
1. **Join Crossref** as a member at https://www.crossref.org/membership/
   - Requires publisher entity (Perfervid Consultancy Services)
   - Annual membership fee applies (tiered by article volume; typically $275–$550 USD/yr for small publishers)
2. **Register DOIs** for all existing 114 articles (one-time batch deposit via Crossref OJS plugin)
   - In OJS: Plugins → Crossref → deposit settings; enter Crossref username/password
   - Submit batch XML deposit via the plugin (already enabled for Synthesis)
3. **DOI prefix for other 4 journals**: you need a DOI prefix per publisher (not per journal); 10.66040 can cover all 5 journals under Perfervid Consultancy Services — confirm this with Crossref before applying for additional prefixes.

Once Crossref credentials are in OJS, the plugin can deposit all 114 articles in one batch.
Do NOT enable `automaticDoiDeposit` until credentials are confirmed — that setting is currently 0.

---

### C. Author affiliations for 2 articles

Submissions #24 and #25 (both Insight) have no affiliation on record anywhere.
Email the authors to supply institutional affiliation, then enter it in OJS
(Submission → Workflow → Contributors → Edit) and re-run the repair script.

---

### D. Zero-reference curation (19 articles, Tier C)

These 19 articles have no citations in the OJS citations table and no recoverable
source JATS package with a ref-list. They need editorial curation before PMC will index them.

Submissions: #3, #9, #19, #23, #24, #25, #29, #30, #31, #41, #45, #50, #53, #68, #88, #92, #93, #107, #108

Recommended action: for each, ask the corresponding author to supply a reference list,
enter the references via OJS (Submission → References), then re-run the repair script.
Note: submissions #24 and #25 also need affiliations (item C above).

---

### E. PMC journal application (after A + B complete)

Apply at https://www.ncbi.nlm.nih.gov/pmc/pub/addjournal/

NLM requires: registered ISSN, registered DOIs on ≥1 year of articles, JATS XML
galleys, preservation deposit, and at least 12 months of regular publication.
Synthesis will meet article-volume and duration thresholds by late 2026.
Expect 6–18 months for NLM review.

---

## PMC-readiness scorecard (post-repair state)

| Blocker | Status |
|---|---|
| JATS XML galley present | ✅ 114/114 |
| `<aff>` affiliations in JATS | ✅ 112/114 (2 need author input) |
| `<ref-list>` in JATS | ✅ 95/114 (19 need editorial curation) |
| ISSN registered | ❌ Application not yet submitted |
| DOI assigned to articles | ❌ Crossref membership needed |
| JATS `<issn>` filled | ⏳ Waiting on ISSN (will auto-fill on repair re-run) |
| JATS `<article-id doi>` filled | ⏳ Waiting on DOIs (will auto-fill on repair re-run) |
| Preservation deposit (PMC/CLOCKSS) | ❌ Not yet |
| PMC journal application | ❌ Waiting on ISSN + DOIs |

The two steps that unblock everything: **ISSN registration** and **Crossref membership**.
Both require Mahmood to act; neither can be automated.
