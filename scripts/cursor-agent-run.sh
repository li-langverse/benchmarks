#!/usr/bin/env bash
# Delegate to li-cursor-agents (Cursor SDK local runner).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_ROOT="${LI_CURSOR_AGENTS_ROOT:-$ROOT/li-cursor-agents}"

if [[ ! -f "$AGENTS_ROOT/package.json" ]]; then
  echo "error: clone li-cursor-agents next to benchmarks:" >&2
  echo "  git clone https://github.com/li-langverse/li-cursor-agents $AGENTS_ROOT" >&2
  exit 1
fi

if [[ ! -d "$AGENTS_ROOT/dist" ]]; then
  echo "==> building li-cursor-agents"
  (cd "$AGENTS_ROOT" && npm ci && npm run build)
fi

export BENCHMARKS_ROOT="$ROOT"
exec node "$AGENTS_ROOT/dist/cli/run-agent.js" --benchmarks "$ROOT" "$@"
