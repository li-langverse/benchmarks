#!/usr/bin/env bash
# Run lic httpd master-plan loop (delegates to lic/scripts/httpd-plan-loop.py).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC="${LIC_ROOT:-$ROOT/lic}"
if [[ ! -f "$LIC/scripts/httpd-plan-loop.py" ]]; then
  LIC="$(cd "$ROOT/../lic" 2>/dev/null && pwd || true)"
fi
if [[ ! -f "$LIC/scripts/httpd-plan-loop.py" ]]; then
  echo "error: lic checkout not found (set LIC_ROOT)" >&2
  exit 1
fi
export BENCHMARKS_ROOT="${BENCHMARKS_ROOT:-$ROOT}"
export LI_CURSOR_AGENTS_ROOT="${LI_CURSOR_AGENTS_ROOT:-$ROOT/li-cursor-agents}"
exec python3 "$LIC/scripts/httpd-plan-loop.py" "$@"
