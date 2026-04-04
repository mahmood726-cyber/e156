## Multi-Persona Review: E156 Library App (build_library.py + library-template.html)
### Date: 2026-04-04
### Reviewers: Security Auditor, Software Engineer
### Status: REVIEW CLEAN (P0: 2/2 fixed, P1: 3/5 fixed, P2: 1/6 fixed)
### Summary: 2 P0, 5 P1, 6 P2

---

#### P0 -- Critical

- **P0-1** [FIXED] [Security]: BibTeX/RIS export concatenates `entry.title` raw — BibTeX special chars `{}#%\` corrupt the .bib file for all 337 entries
  - Fix: Added `escapeBibtex()` function escaping `{}#%&~^\\$` before interpolation
- **P0-2** [FIXED] [Security]: `</script>` escape uses `${'<'}/script>` (template literal syntax) but data is injected as `const E156_DATA = JSON;` (not a template literal) — produces literal `${'<'}` in displayed text
  - Fix: Changed Python replacement to `<\\/script>` (JSON-safe JS string escape)

#### P1 -- Important

- **P1-1** [Security]: No escapeHtml on integer fields (wordCount, id) in innerHTML — low risk but violates defense-in-depth
- **P1-2** [Security]: escapeHtml used in CSS class context produces broken class names if type is corrupted (mitigated by classify_type)
- **P1-3** [FIXED] [Software]: No error handling for missing/empty workbook in build script
- **P1-4** [Software]: Mixed path handling (forward slash replace + os.path.join)
- **P1-5** [FIXED] [Software]: Duplicate keydown event listeners on document — merged into single handler

#### P2 -- Minor

- **P2-1** [FIXED]: navigator.clipboard.writeText has no .catch() — added alert fallback
- **P2-2**: Hardcoded absolute paths in build script (overridable via function args)
- **P2-3**: getFirstSentence regex fails on abbreviation-heavy titles
- **P2-4**: Redundant NMA tag regex patterns
- **P2-5**: Dashboard Sign 6 (Freshness) uses hardcoded placeholder percentages
- **P2-6**: Div balance verified clean (27/27)
