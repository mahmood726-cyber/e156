# Workbook header (frozen reference — do not edit)

_Index: rewrite-PHONE-INDEX.md | Next: rewrite-PHONE-001.md_

This is the original workbook header (lines 1-92). It contains submission
instructions and authorship rules. Read it before rewriting any entry.
Editing this file has no effect on the merge — only YOUR REWRITE blocks
in rewrite-PHONE-001.md..019.md are picked up.

```
E156 REWRITE WORKBOOK
sentinel:skip-file
(Sentinel marker above: this workbook intentionally contains C:\Users\... PATH:
lines pointing to each project's local source directory — they're metadata,
not code. The marker keeps Sentinel from emitting ~16 P0 hardcoded-path
BLOCKs every push.)

DENOMINATOR CONVENTION (added 2026-05-06 after review-findings P1-5):
  Each entry header is `[N/total]` where N = ordinal insertion index and
  `total` = current portfolio size as of the most recent reconcile sweep.
  Older entries are back-rewritten on milestone boundaries (rather than
  preserving their insertion-time denominator) to keep
  reconcile_counts.py from flagging "WORKBOOK DRIFT". The pre-commit
  guard (scripts/check_workbook_commit.py) blocks commits that bundle a
  denominator sweep with substantive content edits to existing entries.

======================================================================

INSTRUCTIONS:
- Replace text under YOUR REWRITE with your body (at most 156 words, 7 sentences)
- S1=Question S2=Dataset S3=Method S4=Result(number+interval) S5=Robustness S6=Interpretation S7=Boundary(limitation)
- Leave YOUR REWRITE blank to keep current version
- Run: python C:/E156/scripts/apply_rewrites.py          (validate)
- Run: python C:/E156/scripts/apply_rewrites.py --apply (apply)

AUTHORSHIP RULE (mandatory for every submission):
- Mahmood Ahmad (MA) must NEVER be listed as first author and NEVER as
  last (senior) author. The student rewriter is first author. Last/senior
  author must be a faculty supervisor or co-investigator distinct from MA.
  MA's position is middle-author only (e.g. role: data curation, software,
  methodology, supervision-of-tooling). This applies to every paper in
  this workbook regardless of contribution depth.

HOW TO SUBMIT TO ◆ SYNTHĒSIS (OJS step-by-step):

Journal: ◆ Synthēsis     URL: https://www.synthesis-medicine.org/index.php/journal
Section: per-paper (Methods Note / Short Meta-Analysis / Brief Update — see your card)
Length: submit the 156-word E156 body verbatim (journal ceiling is 400w; we don't pad).

Step 1 — Prepare the .docx file
  - Microsoft Word .docx, A4 page, 1.5 line spacing, 2.5 cm margins.
  - Font: 11-pt Calibri OR 12-pt Times New Roman (consistent throughout).
  - Order: Title · Authors + ORCIDs + affiliations · Body (the 156-word
    E156 rewrite, 7 sentences, pasted verbatim from YOUR REWRITE — do
    NOT pad toward the journal's 400-word ceiling; the micro-paper
    length is the point of the format) · References (Vancouver/numeric, NLM
    journal abbreviations, DOI without URL prefix; up to 6 authors then
    "et al.") · Data availability · Ethics · Funding · Competing
    interests (use the editorial-board statement from this workbook
    verbatim) · CRediT contributions · AI disclosure · Copyright line:
    "© The Author(s) 2026. CC BY 4.0."

Step 2 — Register / login
  - Register: https://www.synthesis-medicine.org/index.php/journal/user/register
    (use ORCID where possible; pick a strong password; tick Author role).
  - Login:    https://www.synthesis-medicine.org/index.php/journal/login

Step 3 — Start the OJS submission wizard
  - From your dashboard click "New Submission" (top right).
  - 5-step OJS wizard:
      (1) Start         — pick the Section name listed in YOUR card's
                          "Target journal: ◆ Synthēsis" block above
                          (one of: Methods Note, Short Meta-Analysis, or
                          Brief Update — section is preassigned per
                          paper, you don't need to reason about it).
                          Language English; tick all 5 submission-
                          checklist items; agree to CC-BY-4.0 + privacy.
      (2) Upload File   — upload the .docx; component: "Article Text".
      (3) Enter Metadata — paste the title; paste YOUR REWRITE (the
                          156-word body) verbatim as the abstract — the
                          E156 7-sentence structure IS the abstract, no
                          shortening needed; add 4-6 keywords; add ALL
                          contributors with ORCIDs and
                          affiliations IN ORDER (you = first;
                          Mahmood Ahmad = middle; faculty supervisor =
                          last/senior); paste the Vancouver references.
      (4) Confirmation  — review and click "Finish Submission".
      (5) Next Steps    — note the submission ID shown on screen.

Step 4 — Confirm submission on the student board
  - Open https://mahmood726-cyber.github.io/e156/students.html
  - Find your card → click "✓ Confirm submission" → paste the OJS
    submission ID (or DOI once minted) → submit. Card flips to SUBMITTED.

Fallback: if OJS is down, email submissions@synthes.is with the .docx
attached and the line "RE: E156 Methods Note submission, paper #N".

Total projects: 921 (6 duplicate pairs deduplicated, 5 gap-filling projects 2026-04-09, 13 portfolio gap projects 2026-04-10, +1 GuidelineLag 2026-04-14, +1 SGLT2i-HFpEF benchmark demo 2026-04-15 [FAIL branch], +1 precision-sweep E156 2026-04-15, +1 dissonance-field-synthesis 2026-04-15, +1 ARAC 2026-04-28 [v0.9.0; 5/5 RGS metrics + 3 user-facing artifacts], +1 outcome-switching-ma-hf 2026-04-30 [v0.2.1; n=22, 21/22 drift, DIAMOND outcome-content change is headline], +1 Tiba 2026-05-06 [v0.1.0; Pan-African federation; diagnostic Methods Note + constructive companion]) [see --- ENTRY N --- blocks for entries 473-478]

SUBMITTED: [ ]

======================================================================
```
