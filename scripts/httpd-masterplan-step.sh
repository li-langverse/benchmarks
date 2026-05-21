#!/usr/bin/env bash
# Run full benchmarks + matrix after a master-plan step; append to progress log.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STEP="${1:?usage: httpd-masterplan-step.sh <step-id> <short note>}"
NOTE="${2:-}"
LOG="${HTTPD_PROGRESS_LOG:-$ROOT/data/latest/httpd-masterplan-progress.md}"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"

mkdir -p "$(dirname "$LOG")"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
  echo ""
  echo "## Step: $STEP — $TS"
  echo ""
  [[ -n "$NOTE" ]] && echo "$NOTE" && echo ""
  echo '```bash'
  echo "# full suite (fast flags optional: SKIP_BUILD=1 if lic built)"
  echo "LIC_ROOT=$LIC_ROOT SKIP_BUILD=\${SKIP_BUILD:-1} SKIP_TIER0=\${SKIP_TIER0:-1} \\"
  echo "  BENCH_RUNS=\${BENCH_RUNS:-1} HTTP_BENCH_RUNS=\${HTTP_BENCH_RUNS:-2} \\"
  echo "  $ROOT/scripts/run-full-benchmark-suite.sh"
  echo '```'
  echo ""
} >>"$LOG"

export LIC_ROOT
export SKIP_BUILD="${SKIP_BUILD:-1}"
export SKIP_TIER0="${SKIP_TIER0:-1}"
export BENCH_RUNS="${BENCH_RUNS:-1}"
export HTTP_BENCH_RUNS="${HTTP_BENCH_RUNS:-2}"

if ! "$ROOT/scripts/run-full-benchmark-suite.sh" >>"$LOG" 2>&1; then
  echo "WARN: suite had errors (see log)" >>"$LOG"
fi

python3 "$ROOT/scripts/benchmark-matrix-report.py" --json-only >>"$LOG" 2>&1 || true
"$ROOT/scripts/benchmark-failures-report.sh" >>"$LOG" 2>&1 || true

{
  echo ""
  echo "### Matrix excerpt"
  echo '```'
  head -45 "$ROOT/data/latest/benchmark-matrix.md" 2>/dev/null || echo "(no matrix)"
  echo '```'
  echo ""
} >>"$LOG"

echo "httpd-masterplan-step: appended $STEP to $LOG"
