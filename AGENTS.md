# AGENTS.md — rules for any agent working in this repo

This file is the **source of truth** for automated contributors (Claude Code,
Codex, and any other agent), whether running on a local machine or in the cloud.
Cloud agents do **not** see anyone's personal `~/.claude` config — so the rules
that protect the rewrite workbook live here, in the repo, on purpose.

This repo is **public**: `github.com/mahmood726-cyber/e156` (default branch `master`).

---

## The rewrite workbook is the shared, multi-device artifact

`rewrite-workbook.txt` is edited from several places — the author's PCs, Claude
Code on the web, and Codex on the web — and must converge through git. **The repo
is the single source of truth.** Treat every session as collaborative:

1. **Pull before you edit.** Start from the latest `master` (`git pull --rebase`)
   so you don't build on a stale workbook.
2. **Commit + push when you finish.** A workbook edit that isn't pushed doesn't
   exist for the next device. Keep commits small and scoped to what you changed.
3. **Local machines:** run `scripts/e156-sync.ps1` (Windows) or
   `scripts/e156-sync.sh` (mac/Linux/WSL) — it pulls, commits the workbook, and
   pushes in one conflict-safe step.
4. **Cloud agents (Claude Code web / Codex web):** you already operate on the
   GitHub repo — commit your workbook edit to `master` (or open a PR that merges
   to `master`). That is what makes the rewrite show up everywhere.

### Workbook protection contract (NON-NEGOTIABLE)

Each paper entry has three parts. Respect them exactly:

1. **CURRENT BODY** — the AI-drafted version. May be updated freely **unless** the
   entry is marked `SUBMITTED: [x]` (then it is frozen — do not edit).
2. **YOUR REWRITE** — the human author's rewrite. **NEVER edit, overwrite, move,
   reflow, or delete this block** — even if it appears to violate a formatting
   rule, even while resolving a merge conflict. It is the author's record.
3. **SUBMITTED** — `[ ]` or `[x]`. **Only the human author toggles this.** Agents
   must never set it.

When **resolving a merge conflict** in the workbook: keep both sides' `YOUR
REWRITE` content intact; never resolve a conflict by discarding a rewrite block.
If two `YOUR REWRITE` edits to the *same* paper genuinely conflict, stop and
leave it for the human author rather than guessing.

### Workbook format (E156 7-sentence contract)

A body is exactly **7 sentences, ≤156 words, one paragraph**:
S1 Question · S2 Dataset · S3 Method · S4 Result (number + interval) · S5
Robustness · S6 Interpretation · S7 Boundary/limitation. One named primary
estimand; no citations/links/metadata in the body.

### Authorship rule (every submission)

Mahmood Ahmad (MA) is **never** first author and **never** last/senior author —
middle-author only (data curation / software / methodology / tooling
supervision). The student rewriter is first author; a faculty supervisor distinct
from MA is last author.

---

## Repo hygiene notes for agents

- `rewrite-workbook.txt` carries `sentinel:skip-file` + `sentinel:claim-language-allow`
  markers in its header on purpose (it intentionally contains local `PATH:` lines
  and deliberately un-hedged AI draft bodies). Do not "fix" those.
- `scripts/check_workbook_commit.py` is a guard against bundling a denominator
  sweep with substantive content edits — keep content edits and count sweeps in
  separate commits.
- Never commit hardcoded local paths in code/docs/HTML you add (`C:\Users\...`,
  `/home/...`). Derive paths at runtime.
- The flagship capsules live in `flagship/`; see `flagship/README.md`.

## Quick reference

```
# sit down:
git pull --rebase            # or: scripts/e156-sync.ps1  /  scripts/e156-sync.sh
# ... edit rewrite-workbook.txt (CURRENT BODY only; never YOUR REWRITE) ...
# finish:
scripts/e156-sync.ps1 "what you changed"      # Windows
scripts/e156-sync.sh  "what you changed"      # mac/Linux/WSL/cloud
```
