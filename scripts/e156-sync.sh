#!/usr/bin/env bash
# e156-sync — one-command, conflict-safe sync for the E156 rewrite workbook.
# (POSIX/bash twin of e156-sync.ps1, for macOS/Linux/WSL and cloud agents.)
#
#   ./scripts/e156-sync.sh                 # pull, commit workbook edits, push
#   ./scripts/e156-sync.sh "did paper 42"  # custom commit message
#   ./scripts/e156-sync.sh --all           # include every changed file
#
# Commits your edits first, rebases on the remote, then pushes. On a same-line
# conflict it stops safely with your edits committed locally and explains how to
# reconcile. Repo root is derived from the script location (no hardcoded paths).
set -u
root="$(git -C "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)" rev-parse --show-toplevel 2>/dev/null)" \
  || { echo "Not inside a git clone of the e156 repo."; exit 1; }
cd "$root"
branch="$(git rev-parse --abbrev-ref HEAD)"
wb="rewrite-workbook.txt"
all=0; msg=""
for a in "$@"; do
  case "$a" in
    --all) all=1 ;;
    *) msg="$a" ;;
  esac
done
echo "e156-sync on '$branch' ($root)"

# 1) Stage + commit local edits first.
if [ "$all" -eq 1 ]; then git add -A; else git add -- "$wb"; fi
if ! git diff --cached --quiet; then
  [ -z "$msg" ] && msg="workbook: sync from $(hostname) $(date '+%Y-%m-%d %H:%M')"
  git commit -q -m "$msg"
  echo "  committed: $msg"
else
  echo "  no local changes to commit"
fi

# 2) Rebase on remote (autostash protects stray edits).
git fetch -q origin
if ! git rebase --autostash "origin/$branch" >/dev/null 2>&1; then
  git rebase --abort >/dev/null 2>&1 || true
  echo ""
  echo "CONFLICT: the same lines were edited elsewhere. Your edits are committed and SAFE."
  echo "Reconcile, then re-run e156-sync:"
  echo "    git pull --rebase            # then open $wb"
  echo "  Keep the right version of each conflicted paper — NEVER discard a 'YOUR REWRITE'"
  echo "  block. Then: git rebase --continue && ./scripts/e156-sync.sh"
  exit 2
fi

# 3) Push.
ahead="$(git rev-list --count "origin/$branch..HEAD")"
if [ "$ahead" -gt 0 ]; then
  git push -q origin "$branch" && echo "  pushed $ahead commit(s) to origin/$branch"
else
  echo "  nothing to push"
fi
echo "In sync."
