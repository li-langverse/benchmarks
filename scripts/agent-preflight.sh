#!/usr/bin/env bash
# Deterministic preflight for Cursor agents — writes data/latest/agent-briefing.json
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
export GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"

echo "==> agent preflight (scripts only — use Cursor Automation for reasoning)"
python3 scripts/agent-briefing.py "$@"
