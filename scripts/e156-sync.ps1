<#
e156-sync - one-command, conflict-safe sync for the E156 rewrite workbook.

Run it when you SIT DOWN (to get the latest) and when you FINISH (to push):
    .\scripts\e156-sync.ps1                 # pull, commit workbook edits, push
    .\scripts\e156-sync.ps1 "did paper 42"  # custom commit message
    .\scripts\e156-sync.ps1 -All            # include every changed file, not just the workbook

It commits your edits first, then rebases on the remote, then pushes. If the
SAME lines were changed on another machine or by a cloud agent, it stops safely
with your edits committed locally (nothing lost) and tells you how to reconcile.
No hardcoded paths - repo root is derived from the script location.
#>
param(
  [string]$Message,
  [switch]$All
)
$ErrorActionPreference = 'Stop'

$root = (& git -C $PSScriptRoot rev-parse --show-toplevel 2>$null)
if (-not $root) { Write-Host "Not inside a git clone of the e156 repo." -ForegroundColor Red; exit 1 }
Set-Location $root
$branch = (& git rev-parse --abbrev-ref HEAD).Trim()
$wb = 'rewrite-workbook.txt'
Write-Host "e156-sync on '$branch'  ($root)" -ForegroundColor Cyan

# 1) Stage + commit local edits FIRST so the rebase can replay them cleanly.
if ($All) { & git add -A } else { & git add -- $wb }
$staged = (& git diff --cached --name-only)
if ($staged) {
  if (-not $Message) {
    $Message = "workbook: sync from $env:COMPUTERNAME " + (Get-Date -Format 'yyyy-MM-dd HH:mm')
  }
  & git commit -q -m $Message
  Write-Host "  committed: $Message" -ForegroundColor Green
  Write-Host ("  files: " + ($staged -join ', '))
} else {
  Write-Host "  no local changes to commit"
}

# 2) Bring in remote work (rebase keeps history linear; autostash protects stray edits).
& git fetch -q origin
& git rebase --autostash "origin/$branch" 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
  & git rebase --abort 2>$null | Out-Null
  Write-Host ""
  Write-Host "CONFLICT: the same lines were edited elsewhere (another PC or a cloud agent)." -ForegroundColor Yellow
  Write-Host "Your edits are committed locally and SAFE." -ForegroundColor Yellow
  Write-Host "Reconcile, then re-run e156-sync:"
  Write-Host "    git pull --rebase            # then open $wb"
  Write-Host "  Keep the correct version of each conflicted paper - NEVER discard a"
  Write-Host "  'YOUR REWRITE' block. Resolve, 'git rebase --continue', then e156-sync."
  exit 2
}

# 3) Push whatever is ahead of the remote.
$ahead = [int](& git rev-list --count "origin/$branch..HEAD")
if ($ahead -gt 0) {
  & git push -q origin $branch
  if ($LASTEXITCODE -ne 0) { Write-Host "push failed - run 'git push' to see the error." -ForegroundColor Red; exit 1 }
  Write-Host "  pushed $ahead commit(s) to origin/$branch" -ForegroundColor Green
} else {
  Write-Host "  nothing to push"
}
Write-Host "In sync." -ForegroundColor Cyan
