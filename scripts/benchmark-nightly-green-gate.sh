#!/usr/bin/env bash
# Completion gate: progress checks + latest GitHub nightly success (optional dispatch).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/benchmark-nightly-green-progress-gate.sh"

POLL="${BENCHMARK_NIGHTLY_GATE_POLL:-1}"
DISPATCH="${BENCHMARK_NIGHTLY_GATE_DISPATCH:-0}"
MAX_WAIT_SEC="${BENCHMARK_NIGHTLY_GATE_MAX_WAIT_SEC:-900}"

if [[ "$DISPATCH" == "1" ]]; then
  echo "benchmark-nightly-green-gate: dispatching benchmark-nightly (fast)"
  gh workflow run benchmark-nightly.yml --repo li-langverse/benchmarks --ref main -f bench_profile=fast
  sleep 30
fi

if [[ "$POLL" != "1" ]]; then
  echo "benchmark-nightly-green-gate: PASS (progress only; set BENCHMARK_NIGHTLY_GATE_POLL=1 for CI check)"
  exit 0
fi

command -v gh >/dev/null 2>&1 || {
  echo "benchmark-nightly-green-gate: WARN gh missing — cannot poll CI" >&2
  exit 1
}

deadline=$(( $(date +%s) + MAX_WAIT_SEC ))
echo "benchmark-nightly-green-gate: polling nightly runs (max ${MAX_WAIT_SEC}s)"

while [[ $(date +%s) -lt $deadline ]]; do
  run_id="$(gh run list --repo li-langverse/benchmarks --workflow=benchmark-nightly.yml --branch=main --limit=1 --json databaseId,status,conclusion --jq '.[0] | select(.status=="completed") | .databaseId' 2>/dev/null || true)"
  if [[ -n "$run_id" ]]; then
    conclusion="$(gh run view "$run_id" --repo li-langverse/benchmarks --json conclusion --jq '.conclusion' 2>/dev/null || true)"
    if [[ "$conclusion" == "success" ]]; then
      publish_ok="$(gh run view "$run_id" --repo li-langverse/benchmarks --json jobs --jq '[.jobs[] | select(.name=="publish-dashboard") | .conclusion] | first' 2>/dev/null || true)"
      if [[ "$publish_ok" == "success" ]]; then
        echo "benchmark-nightly-green-gate: PASS run=$run_id publish-dashboard green"
        exit 0
      fi
      echo "benchmark-nightly-green-gate: run $run_id completed but publish-dashboard=$publish_ok" >&2
      gh run view "$run_id" --repo li-langverse/benchmarks --log-failed 2>/dev/null | tail -40 || true
      exit 1
    fi
    if [[ "$conclusion" == "failure" ]]; then
      echo "benchmark-nightly-green-gate: FAIL run=$run_id" >&2
      gh run view "$run_id" --repo li-langverse/benchmarks --log-failed 2>/dev/null | tail -40 || true
      exit 1
    fi
  fi
  sleep 60
done

echo "benchmark-nightly-green-gate: FAIL timed out waiting for green nightly" >&2
exit 1
