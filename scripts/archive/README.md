# scripts/archive/ — run-once fixups

These scripts were single-shot repair tools for the 2026-04-15..19 claim-board
recovery work. They encode hardcoded paper-num lists, URL remaps, and other
positional data from a specific workbook state. They **should not be re-run
as-is** on any later workbook — most will either no-op or silently misapply
against entries that have since been edited.

If you need to do something similar in the future, treat these as *reference
implementations*, not reusable tools — copy the relevant function into a new
script with a fresh hardcoded map.

Kept here for:
- audit trail (what was done to get to commit 02dfb5d)
- idempotency-bug reference (lessons.md: "Hardcoded batch lists in reusable
  scripts")
- data shape reference for resolution_plan.json / push_plan.json / hide_repo_404.json

| File | Ran | Purpose |
|---|---|---|
| `resolve_hidden_entries.py` | 2026-04-19 | Grouped the 121 hidden entries by workbook Code: URL |
| `preflight_pushes.py` | 2026-04-19 | Stat + git-state each local dir before push |
| `apply_alias_fixes.py` | 2026-04-19 (Phase A) | Rewrote 32 workbook Code URLs to resolve alias mismatches |
| `apply_fresh_pushes.py` | 2026-04-19 (Phase B) | Pushed 55 fresh dirs to new GitHub repos |
| `retry_failed_pushes.py` | 2026-04-19 | Retry loop for the 9 Phase B failures |
| `push_cross_owner.py` | 2026-04-19 | Pushed 6 other-account dirs to mahmood726-cyber |
| `unhide_after_push.py` | 2026-04-19 | Removed just-pushed nums from hide list |
| `unhide_remaining.py` | 2026-04-19 | Un-hid the final 10 with routing |
| `cleanup_workbook_final.py` | 2026-04-19 | #129/#413 URL fixes + renumbered 11 dup headers |
| `fix_final_4.py` | 2026-04-19 | Final 4 post-remap URL fixes |
| `remap_shared_dashboards.py` | 2026-04-19 | Finrenone 17-cluster → per-therapy REVIEW.html |
| `remap_broken_and_shared.py` | 2026-04-19 | 203 broken/shared dashboards → /e156/paper/N.html |
| `enable_missing_pages.py` | 2026-04-19 | Bulk-enabled Pages on 142 repos |
| `retry_429_checks.py` | 2026-04-19 | Throttled retry for verify_board_links rate-limited URLs |
