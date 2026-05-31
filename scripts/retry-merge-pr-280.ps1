# Retry merging benchmarks PR #280 until merged or max attempts.
# Usage: .\scripts\retry-merge-pr-280.ps1 [-IntervalMinutes 30] [-MaxAttempts 48]
param(
  [int]$IntervalMinutes = 30,
  [int]$MaxAttempts = 48,
  [int]$PrNumber = 280
)

$ErrorActionPreference = "Continue"
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $repoRoot

$envFile = Join-Path (Split-Path $repoRoot -Parent) ".env.github"
if (-not (Test-Path $envFile)) {
  $envFile = "C:\Users\Julian\Documents\Programming\li\.env.github"
}
if (Test-Path $envFile) {
  Get-Content $envFile | ForEach-Object {
    if ($_ -match '^GH_TOKEN=(.+)$') { $env:GH_TOKEN = $matches[1].Trim('"').Trim("'") }
  }
}

$log = Join-Path $repoRoot "results\retry-merge-pr-$PrNumber.log"
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null

function Write-Log([string]$msg) {
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
  Write-Host $line
  Add-Content -Path $log -Value $line
}

Write-Log "Starting merge retries for PR #$PrNumber every $IntervalMinutes min (max $MaxAttempts)"

for ($i = 1; $i -le $MaxAttempts; $i++) {
  $view = gh pr view $PrNumber --json state,mergedAt 2>&1
  if ($LASTEXITCODE -ne 0) {
    Write-Log "attempt $i`: gh pr view failed: $view"
  } else {
    $j = $view | ConvertFrom-Json
    if ($j.state -eq "MERGED" -or $j.mergedAt) {
      Write-Log "PR #$PrNumber already merged."
      exit 0
    }
  }

  Write-Log "attempt $i`: merging..."
  $out = gh api --method PUT "repos/li-langverse/benchmarks/pulls/$PrNumber/merge" -f merge_method=squash 2>&1 | Out-String
  if ($LASTEXITCODE -ne 0) {
    $out2 = gh pr merge $PrNumber --squash 2>&1 | Out-String
    if ($LASTEXITCODE -eq 0) { $out = $out2 } else { $out = "$out`n$out2" }
  }
  if ($LASTEXITCODE -eq 0) {
    Write-Log "PR #$PrNumber merged successfully."
    exit 0
  }

  Write-Log "attempt $i` failed: $($out.Trim())"
  if ($i -lt $MaxAttempts) {
    Write-Log "sleeping $IntervalMinutes minutes..."
    Start-Sleep -Seconds ($IntervalMinutes * 60)
  }
}

Write-Log "Gave up after $MaxAttempts attempts."
exit 1
