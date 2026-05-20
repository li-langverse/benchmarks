#!/usr/bin/env bash
# Delegate to li-cursor-agents (Cursor SDK local runner).
# Default search order matches scripts/agent-briefing.py: sibling ../li-cursor-agents, then ./li-cursor-agents.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PARENT="$(cd "$ROOT/.." && pwd)"
if [[ -n "${LI_CURSOR_AGENTS_ROOT:-}" ]]; then
  AGENTS_ROOT="$LI_CURSOR_AGENTS_ROOT"
else
  if [[ -f "$PARENT/li-cursor-agents/package.json" ]]; then
    AGENTS_ROOT="$PARENT/li-cursor-agents"
  else
    AGENTS_ROOT="$ROOT/li-cursor-agents"
  fi
fi

if [[ ! -f "$AGENTS_ROOT/package.json" ]]; then
  echo "error: li-cursor-agents not found (expected package.json)." >&2
  echo "  Clone next to this repo: git clone https://github.com/li-langverse/li-cursor-agents $PARENT/li-cursor-agents" >&2
  echo "  Or under benchmarks: git clone https://github.com/li-langverse/li-cursor-agents $ROOT/li-cursor-agents" >&2
  echo "  Or set LI_CURSOR_AGENTS_ROOT to the clone path." >&2
  exit 1
fi

if [[ ! -d "$AGENTS_ROOT/dist" ]]; then
  echo "==> building li-cursor-agents"
  (cd "$AGENTS_ROOT" && npm ci && npm run build)
fi

export BENCHMARKS_ROOT="$ROOT"
exec node "$AGENTS_ROOT/dist/cli/run-agent.js" --benchmarks "$ROOT" "$@"
