#!/usr/bin/env bash
# Run benchmark-nightly core steps locally (same commands as GHA bench-* jobs).
# Usage:
#   ./scripts/run-nightly-local.sh linux          # full Linux tiers (WSL or native Linux)
#   ./scripts/run-nightly-local.sh windows        # MSYS2 UCRT64 core (tier1 + tier2-md)
#   ./scripts/run-nightly-local.sh macos          # core tiers (on macOS only)
#   ./scripts/run-nightly-local.sh build-only     # setup-lic-for-bench only (fast compile check)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_PARENT="$(cd "$ROOT/.." && pwd)"
if [[ -z "${LIC_ROOT:-}" ]]; then
  if [[ -d "$ROOT/lic" ]]; then
    LIC_ROOT="$ROOT/lic"
  elif [[ -d "$REPO_PARENT/lic" ]]; then
    LIC_ROOT="$REPO_PARENT/lic"
  fi
fi
if [[ -z "${LIS_ROOT:-}" ]]; then
  if [[ -d "$ROOT/lis" ]]; then
    LIS_ROOT="$ROOT/lis"
  elif [[ -d "$REPO_PARENT/lis" ]]; then
    LIS_ROOT="$REPO_PARENT/lis"
  fi
fi
PROFILE="${1:-}"

if [[ -z "$PROFILE" ]]; then
  echo "usage: $0 {linux|windows|macos|build-only}" >&2
  exit 2
fi

if [[ ! -d "${LIC_ROOT:-}" ]]; then
  echo "missing lic checkout (set LIC_ROOT or clone into benchmarks/lic or ../lic)" >&2
  exit 1
fi
if [[ ! -d "${LIS_ROOT:-}" ]]; then
  echo "missing lis checkout (set LIS_ROOT or clone into benchmarks/lis or ../lis)" >&2
  exit 1
fi

export LIC_ROOT LIS_ROOT LI_REPO_ROOT="$LIC_ROOT"
cd "$ROOT"
chmod +x scripts/*.sh scripts/lib/*.sh 2>/dev/null || true
chmod +x "$LIC_ROOT"/scripts/*.sh 2>/dev/null || true

run_windows_patch() {
  if [[ -x "$ROOT/scripts/patch-lic-msys-windows.sh" ]]; then
    ./scripts/patch-lic-msys-windows.sh
  fi
}

run_core_tiers() {
  rm -f results/latest.csv results/tier-*.csv
  ./scripts/run-benchmark-ci-nightly.sh tier tier1
  ./scripts/run-benchmark-ci-nightly.sh tier tier2-md
  ./scripts/finalize-nightly-os-csv.sh results
  echo "OK results/latest.csv ($(wc -l < results/latest.csv) lines)"
}

case "$PROFILE" in
  build-only)
    case "$(uname -s)" in
      MINGW*|MSYS*|CYGWIN*|Windows*)
        run_windows_patch
        export LLVM_DIR="${LLVM_DIR:-/ucrt64/lib/cmake/llvm}"
        export PATH="/ucrt64/bin:${PATH}"
        export CC=clang CXX=clang++
        ;;
    esac
    ./scripts/setup-lic-for-bench.sh
    ;;
  windows)
    case "$(uname -s)" in
      MINGW*|MSYS*|CYGWIN*|Windows*) ;;
      *)
        echo "windows profile requires MSYS2 UCRT64 shell (not $(uname -s))" >&2
        echo "  From PowerShell: .\\scripts\\run-nightly-local.ps1" >&2
        exit 1
        ;;
    esac
    test -f /ucrt64/lib/cmake/llvm/LLVMConfig.cmake
    export LLVM_DIR="${LLVM_DIR:-/ucrt64/lib/cmake/llvm}"
    export MSYSTEM=UCRT64
    export PATH="/ucrt64/bin:$PATH"
    export CC=clang CXX=clang++
    run_windows_patch
    ./scripts/setup-lic-for-bench.sh
    run_core_tiers
    ;;
  macos)
    case "$(uname -s)" in
      Darwin*) ;;
      *)
        echo "macos profile requires Darwin (not $(uname -s))" >&2
        exit 1
        ;;
    esac
    ./scripts/setup-lic-for-bench.sh
    run_core_tiers
    ;;
  linux)
    case "$(uname -s)" in
      Linux*) ;;
      *)
        echo "linux profile requires Linux (use WSL: wsl -d Ubuntu-24.04 -- ...)" >&2
        exit 1
        ;;
    esac
    ./scripts/setup-lic-for-bench.sh
    for g in tier0 tier1 tier2-md tier2-mech tier2-pde tier3 tier5 tier5-exploits tier7-0 tier7-1 tier7-2; do
      ./scripts/run-benchmark-ci-nightly.sh tier "$g" || true
    done
    ./scripts/merge-benchmark-tier-csvs.sh results
    echo "OK merged $(wc -l < results/latest.csv) lines in results/latest.csv"
    ;;
  *)
    echo "unknown profile: $PROFILE" >&2
    exit 2
    ;;
esac
