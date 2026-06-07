#!/usr/bin/env bash
# Completion gate: progress checks + latest GitHub nightly success (optional dispatch).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/benchmark-nightly-green-progress-gate.sh"

POLL="${BENCHMARK_NIGHTLY_GATE_POLL:-1}"
DISPATCH="${BENCHMARK_NIGHTLY_GATE_DISPATCH:-0}"
MAX_WAIT_SEC="${BENCHMARK_NIGHTLY_GATE_MAX_WAIT_SEC:-900}"

_resolve_gate_branch() {
  if [[ -n "${BENCHMARK_NIGHTLY_GATE_BRANCH:-}" ]]; then
    echo "$BENCHMARK_NIGHTLY_GATE_BRANCH"
    return
  fi
  if [[ -n "${LI_REPO_WORKFLOW_BRANCH:-}" ]]; then
    echo "$LI_REPO_WORKFLOW_BRANCH"
    return
  fi
  local branch
  branch="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
  if [[ -n "$branch" && "$branch" != "HEAD" && "$branch" != "main" && "$branch" != "master" ]]; then
    echo "$branch"
    return
  fi
  echo "main"
}

GATE_BRANCH="$(_resolve_gate_branch)"
GATE_REF="${BENCHMARK_NIGHTLY_GATE_REF:-$GATE_BRANCH}"

_gh_rate_limit_wait() {
  local reset now wait_sec cap
  reset="$(gh api rate_limit --jq '.resources.core.reset' 2>/dev/null || true)"
  [[ -n "$reset" && "$reset" =~ ^[0-9]+$ ]] || return 0
  now="$(date +%s)"
  wait_sec=$(( reset - now + 5 ))
  (( wait_sec > 0 )) || return 0
  cap=$(( MAX_WAIT_SEC / 4 ))
  (( cap < 120 )) && cap=120
  (( wait_sec > cap )) && wait_sec="$cap"
  echo "benchmark-nightly-green-gate: REST rate limit — sleeping ${wait_sec}s (core reset @${reset})" >&2
  sleep "$wait_sec"
}

_gh_retry() {
  local attempt=0
  while (( attempt < 4 )); do
    if "$@"; then
      return 0
    fi
    if gh api rate_limit --jq '.resources.core.remaining' 2>/dev/null | grep -qx '0'; then
      _gh_rate_limit_wait
    else
      sleep $(( 15 * (attempt + 1) ))
    fi
    attempt=$(( attempt + 1 ))
  done
  return 1
}

if [[ "$DISPATCH" == "1" ]]; then
  echo "benchmark-nightly-green-gate: dispatching benchmark-nightly (fast) ref=$GATE_REF"
  _gh_retry gh workflow run benchmark-nightly.yml --repo li-langverse/benchmarks --ref "$GATE_REF" -f bench_profile=fast
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
echo "benchmark-nightly-green-gate: polling nightly runs branch=$GATE_BRANCH (max ${MAX_WAIT_SEC}s)"

_poll_latest_run_id() {
  gh run list --repo li-langverse/benchmarks --workflow=benchmark-nightly.yml --branch="$GATE_BRANCH" --limit=1 \
    --json databaseId,status,conclusion \
    --jq '.[0] | select(.status=="completed") | .databaseId' 2>/dev/null || true
}

while [[ $(date +%s) -lt $deadline ]]; do
  run_id="$(_poll_latest_run_id)"
  if [[ -z "$run_id" ]] && gh api rate_limit --jq '.resources.core.remaining' 2>/dev/null | grep -qx '0'; then
    _gh_rate_limit_wait
    run_id="$(_poll_latest_run_id)"
  fi
  if [[ -n "$run_id" ]]; then
    conclusion="$(gh run view "$run_id" --repo li-langverse/benchmarks --json conclusion --jq '.conclusion' 2>/dev/null || true)"
    if [[ "$conclusion" == "success" ]]; then
      if [[ "$GATE_BRANCH" == "main" ]]; then
        publish_ok="$(gh run view "$run_id" --repo li-langverse/benchmarks --json jobs --jq '[.jobs[] | select(.name=="publish-dashboard") | .conclusion] | first' 2>/dev/null || true)"
        if [[ "$publish_ok" == "success" ]]; then
          echo "benchmark-nightly-green-gate: PASS run=$run_id publish-dashboard green"
          exit 0
        fi
        echo "benchmark-nightly-green-gate: run $run_id completed but publish-dashboard=$publish_ok" >&2
      else
        merge_ok="$(gh run view "$run_id" --repo li-langverse/benchmarks --json jobs --jq '[.jobs[] | select(.name | test("bench-(linux|macos|windows)-merge")) | .conclusion] | all(. == "success")' 2>/dev/null || true)"
        if [[ "$merge_ok" == "true" ]]; then
          echo "benchmark-nightly-green-gate: PASS run=$run_id branch=$GATE_BRANCH merge jobs green (publish-dashboard runs on main only)"
          exit 0
        fi
        echo "benchmark-nightly-green-gate: run $run_id branch=$GATE_BRANCH merge jobs incomplete" >&2
      fi
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
