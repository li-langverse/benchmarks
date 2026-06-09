#!/usr/bin/env bash
# Dev server for benchmarks-dashboard ux-harness target (port 3100).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export LI_BENCHMARKS_DASHBOARD_PORT="${LI_BENCHMARKS_DASHBOARD_PORT:-3100}"
export NEXT_PUBLIC_BASE_PATH="${NEXT_PUBLIC_BASE_PATH:-}"
exec npm run dev -- --port "$LI_BENCHMARKS_DASHBOARD_PORT"
