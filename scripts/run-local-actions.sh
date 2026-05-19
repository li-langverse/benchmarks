#!/usr/bin/env bash
# Run local CI when GitHub Actions minutes are exhausted or checks are skipped.
#
# Usage:
#   ./scripts/run-local-actions.sh              # this repo (benchmarks)
#   ./scripts/run-local-actions.sh lic          # lic: scripts/local-ci.sh
#   ./scripts/run-local-actions.sh sweep        # org PRs via li-local-ci
#   ./scripts/run-local-actions.sh sweep --repo lic --pr 57
#
# Env:
#   LI_LOCAL_CI_ROOT   path to li-local-ci clone
#   LI_ACTIONS_QUOTA_EXCEEDED=1  documents intent (merge gate prefers local-ci)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-here}"
shift || true

run_lic_local_ci() {
  local lic_root="${LI_LIC_ROOT:-$ROOT/lic}"
  if [[ ! -f "$lic_root/scripts/local-ci.sh" ]]; then
    echo "run-local-actions: missing $lic_root/scripts/local-ci.sh" >&2
    echo "  clone li-langverse/lic or set LI_LIC_ROOT" >&2
    exit 1
  fi
  echo "==> lic local-ci (mirrors GHA linux job)"
  (cd "$lic_root" && ./scripts/local-ci.sh "$@")
}

run_benchmarks_ci() {
  if [[ -f "$ROOT/scripts/ci.sh" ]]; then
    echo "==> benchmarks ci.sh"
    (cd "$ROOT" && ./scripts/ci.sh)
    return
  fi
  if [[ -f "$ROOT/scripts/agent-preflight.sh" ]]; then
    echo "==> benchmarks agent-preflight (no ci.sh)"
    (cd "$ROOT" && ./scripts/agent-preflight.sh)
    return
  fi
  echo "run-local-actions: no scripts/ci.sh or agent-preflight.sh in $ROOT" >&2
  exit 1
}

case "$MODE" in
  here|benchmarks|.)
    run_benchmarks_ci
    ;;
  lic)
    run_lic_local_ci "$@"
    ;;
  sweep)
    if [[ ! -f "$ROOT/scripts/local-ci-sweep.py" ]]; then
      echo "run-local-actions: missing local-ci-sweep.py" >&2
      exit 1
    fi
    export LI_ACTIONS_QUOTA_EXCEEDED="${LI_ACTIONS_QUOTA_EXCEEDED:-1}"
    exec python3 "$ROOT/scripts/local-ci-sweep.py" "$@"
    ;;
  all)
    run_lic_local_ci
    run_benchmarks_ci
    python3 "$ROOT/scripts/local-ci-sweep.py" --limit 3 "$@" || true
    ;;
  -h|--help)
    sed -n '2,16p' "$0"
    exit 0
    ;;
  *)
    if [[ -d "$ROOT/$MODE" && -f "$ROOT/$MODE/scripts/local-ci.sh" ]]; then
      LI_LIC_ROOT="$ROOT/$MODE" run_lic_local_ci "$@"
    elif [[ -d "$ROOT/../$MODE/scripts" ]]; then
      LI_LIC_ROOT="$ROOT/../$MODE" run_lic_local_ci "$@"
    else
      echo "unknown target: $MODE (try: here, lic, sweep, all)" >&2
      exit 2
    fi
    ;;
esac

echo "run-local-actions: ok"
