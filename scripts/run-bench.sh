#!/usr/bin/env bash
# Run harness/bench.py from the benchmarks repo (workloads live here; LIC_ROOT = toolchain).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export BENCHMARKS_ROOT="${BENCHMARKS_ROOT:-$ROOT}"
export LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
export LI_REPO_ROOT="${LI_REPO_ROOT:-$LIC_ROOT}"
export PYTHONPATH="$ROOT/harness${PYTHONPATH:+:$PYTHONPATH}"
export BENCHMARKS_CSV="${BENCHMARKS_CSV:-$ROOT/results/latest.csv}"
mkdir -p "$(dirname "$BENCHMARKS_CSV")"
exec python3 "$ROOT/harness/bench.py" "$@"
