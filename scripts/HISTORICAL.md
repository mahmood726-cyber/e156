# `scripts/` — historical one-shot tools (read before editing)

The `scripts/` directory mixes **active generators** (the ones called by `.github/workflows/rapidmeta-sync.yml` or any future `run_full_cycle.py`) with **historical one-shot scripts** that were run once for a specific batch addition and committed for provenance. Audit 2026-05-24 catalogs the latter so you don't mistake them for active orchestration.

## Active generators (called by automation)

| Script | What it does | Called by |
|---|---|---|
| `build_students_page.py` | Renders `students.html` from `rewrite-workbook.txt` | `.github/workflows/rapidmeta-sync.yml` |
| `build_paper_pages.py` | Renders `paper/<N>.html` per entry | `.github/workflows/rapidmeta-sync.yml` |
| `build_library.py` | Renders `e156-library.html` | Manual + planned orchestration |
| `generate_rapidmeta_entries.py` | Appends new RapidMeta review entries | `.github/workflows/rapidmeta-sync.yml` |
| `check_workbook_commit.py` | Pre-commit guard | `.git/hooks/pre-commit` |
| `install_pre_commit.ps1` | Hook installer | Manual one-time |

## Historical one-shots (DO NOT re-run without operator approval)

These scripts were run once for a specific batch addition. They contain hardcoded project lists and assume the workbook state at the time of the run. Re-running them today would either error or produce duplicate entries.

| Script | What it did | When | Why it's still here |
|---|---|---|---|
| `add_missing_projects.py` | Added 7 specific new projects + created submission folders + protocols + dashboards | 2026-04-07 | Provenance / template reference for adding multi-artifact projects |
| `append_missing_projects.py` | Appended 29 missing projects to workbook | 2026-04-03 | Provenance of the 29-project bulk addition |
| `scan_missing_projects.py` | Scanned the 29 missing project dirs and extracted body input for `append_missing_projects.py` | 2026-04-23 (last edit) | Companion to `append_missing_projects.py`; kept together |
| `scan_and_generate.py` | Scanned zero-body project directories and generated E156 body templates | 2026-04-03 | Predates the rapidmeta-finerenone weekly sync; superseded by `generate_rapidmeta_entries.py` for the rapidmeta family |
| `add_new_projects.py` | Earlier variant of the add-projects flow | 2026-04-23 | Predates `add_missing_projects.py`; kept for diff reference |
| `fix_12_stuck.py`, `fix_remaining.py`, `fix_sentences.py`, `trim_overcount.py`, `temp_validate_13.py`, `write_new_bodies.py`, `insert_bodies.py` | One-shot body-text repair scripts from prior cleanup waves | various | Provenance of past content fixes |
| `split_for_phone.py`, `merge-rewrite.py` | Phone-friendly workbook chunking + post-merge cleanup | 2026-05-16 | Used during the May phone-rewrite session |

**Rule of thumb**: if a script name starts with `add_`, `append_`, `scan_`, `fix_`, `trim_`, `temp_`, `write_new_`, `insert_`, `merge-`, or has a number in its name, treat it as historical until proven otherwise. The active generators all start with `build_`, `generate_`, `check_`, or `install_`.

## Why not delete them?

1. **Provenance**: a future audit may want to see exactly what was added in each batch. The script + git history of the script encodes that.
2. **Templates**: the next "add N new projects" task can crib from the most recent `add_missing_projects.py` rather than reinventing.
3. **Reproducibility**: if a SHIP cert later needs to verify the workbook history, these scripts document the deltas.

## Refactor candidates (Phase 2)

If the `scripts/` directory grows beyond ~30 files:

- Move all historical one-shots into `scripts/historical/<date>-<purpose>.py` to make the active surface obvious.
- Add a `scripts/active/` symlink layer so workflows reference stable paths even if files move.
- Auto-generate this `HISTORICAL.md` from git log metadata + a `# active: false` header convention.

Not Phase 1 work.
