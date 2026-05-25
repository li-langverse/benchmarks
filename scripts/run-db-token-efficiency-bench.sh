#!/usr/bin/env bash
# Agent/LLM query-surface token efficiency — reproducible string corpus + tiktoken/heuristic.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_token_efficiency"
PROFILE="${BENCH_DB_TOKEN_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-token-efficiency-manifest.py"
VENV="$TIER_ROOT/.venv"

if [[ ! -f "$TIER_ROOT/scenarios.json" ]]; then
  echo "run-db-token-efficiency-bench: missing $TIER_ROOT/scenarios.json" >&2
  exit 1
fi

# Optional venv for tiktoken (PEP 668 safe)
if ! python3 -c "import tiktoken" 2>/dev/null; then
  if [[ ! -d "$VENV" ]]; then
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install -q tiktoken
  fi
  export PATH="$VENV/bin:$PATH"
fi

python3 "$MANIFEST_WRITER" --profile "$PROFILE"
echo "run-db-token-efficiency-bench: manifest data/latest/tier-db-token-efficiency.json"
echo "  doc: docs/ecosystem/tier-db-token-efficiency.md"
echo "  full audit: ../lidb/docs/liq-token-efficiency-audit.md"
