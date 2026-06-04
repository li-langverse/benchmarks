# Launch benchmark nightly (Windows / MSYS2 UCRT64) on the desktop — mirrors GHA bench-windows.
param(
    [ValidateSet("windows", "build-only")]
    [string]$Profile = "windows",
    [switch]$InstallMsys2
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$MsysRoot = if ($env:MSYS2_ROOT) { $env:MSYS2_ROOT } else { "C:\msys64" }
$Shell = Join-Path $MsysRoot "msys2_shell.cmd"

function Ensure-Msys2 {
    if (Test-Path $Shell) { return }
    if (-not $InstallMsys2) {
        throw "MSYS2 not found at $MsysRoot. Install: winget install MSYS2.MSYS2  then re-run with -InstallMsys2"
    }
    Write-Host "==> Installing MSYS2 via winget..."
    winget install --id MSYS2.MSYS2 -e --accept-package-agreements --accept-source-agreements
    if (-not (Test-Path $Shell)) { throw "MSYS2 install finished but $Shell missing" }
}

function Convert-ToMsysPath([string]$WinPath) {
    $p = (Resolve-Path $WinPath).Path
    if ($p -match '^([A-Za-z]):\\(.*)$') {
        return ('/{0}/{1}' -f $matches[1].ToLower(), ($matches[2] -replace '\\', '/'))
    }
    return ($p -replace '\\', '/')
}

function Invoke-Ucrt64 {
    $unixRoot = Convert-ToMsysPath $Root
    $cmd = @"
export MSYSTEM=UCRT64
export PATH=/ucrt64/bin:`$PATH
pacman -Sy --noconfirm --needed mingw-w64-ucrt-x86_64-toolchain mingw-w64-ucrt-x86_64-cmake mingw-w64-ucrt-x86_64-ninja mingw-w64-ucrt-x86_64-python mingw-w64-ucrt-x86_64-llvm mingw-w64-ucrt-x86_64-clang 2>/dev/null || true
cd '$unixRoot' && chmod +x scripts/*.sh scripts/lib/*.sh 2>/dev/null || true
bash ./scripts/run-nightly-local.sh $Profile
"@
    & $Shell -ucrt64 -defterm -no-start -c $cmd
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Ensure-Msys2
Write-Host "==> Running nightly local profile=$Profile in MSYS2 UCRT64"
Invoke-Ucrt64
