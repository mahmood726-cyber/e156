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

function Invoke-GitNative {
  param(
    [Parameter(Mandatory)][string[]]$GitArgs,
    [switch]$AllowFailure
  )
  # Git writes normal progress/status messages to stderr. Under Stop semantics,
  # PowerShell can promote those messages to errors even when Git exits 0.
  $prevEAP = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $output = @(& git @GitArgs 2>&1 | ForEach-Object { $_.ToString() })
    $exitCode = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $prevEAP
  }
  $global:LASTEXITCODE = 0
  if (($exitCode -ne 0) -and (-not $AllowFailure)) {
    if ($output) { $output | ForEach-Object { Write-Host "  $_" } }
    Write-Host "git $($GitArgs -join ' ') failed ($exitCode)" -ForegroundColor Red
    exit 1
  }
  [pscustomobject]@{ ExitCode = $exitCode; Lines = $output }
}

# 1) Stage + commit local edits FIRST so the rebase can replay them cleanly.
if ($All) { & git add -A } else { & git add -- $wb }
$staged = (& git diff --cached --name-only)
if ($staged) {
  if (-not $Message) {
    $Message = "workbook: sync from $env:COMPUTERNAME " + (Get-Date -Format 'yyyy-MM-dd HH:mm')
  }
  Invoke-GitNative -GitArgs @('commit','-q','-m',$Message) | Out-Null
  Write-Host "  committed: $Message" -ForegroundColor Green
  Write-Host ("  files: " + ($staged -join ', '))
} else {
  Write-Host "  no local changes to commit"
}

# 2) Bring in remote work (rebase keeps history linear; autostash protects stray edits).
Invoke-GitNative -GitArgs @('fetch','-q','origin') | Out-Null
$rebase = Invoke-GitNative -GitArgs @('rebase','--autostash',"origin/$branch") -AllowFailure
if ($rebase.ExitCode -ne 0) {
  Invoke-GitNative -GitArgs @('rebase','--abort') -AllowFailure | Out-Null
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
  $push = Invoke-GitNative -GitArgs @('push','-q','origin',$branch) -AllowFailure
  if ($push.ExitCode -ne 0) { Write-Host "push failed - run 'git push' to see the error." -ForegroundColor Red; exit 1 }
  Write-Host "  pushed $ahead commit(s) to origin/$branch" -ForegroundColor Green
} else {
  Write-Host "  nothing to push"
}
Write-Host "In sync." -ForegroundColor Cyan
