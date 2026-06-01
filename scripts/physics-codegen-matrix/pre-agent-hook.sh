#!/usr/bin/env bash
# Source before code_implementer when running physics-codegen-matrix goal-directed loop.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BENCHMARKS_ROOT="${BENCHMARKS_ROOT:-$ROOT}"
SCRIPT="$ROOT/scripts/physics-codegen-matrix/export-next-cell-instruction.mjs"
if [[ ! -f "$SCRIPT" ]]; then
  exit 0
fi
if [[ "${LI_SKIP_PHYSICS_CODEGEN_CELL_PROMPT:-}" == "1" ]]; then
  exit 0
fi
# Only auto-inject when goal file targets this sprint (or explicit enable).
goal="${LI_PROOF_EXPLORER_GOAL_FILE:-}${LI_AGENT_GOAL_FILE:-}"
if [[ "$goal" != *physics-codegen-matrix* && "${PHYSICS_CODEGEN_AUTO_CELL_PROMPT:-}" != "1" ]]; then
  exit 0
fi
# Skip when caller already injected a cell prompt (e.g. run-matrix-live extraInstruction).
if [[ -n "${LI_AGENT_EXTRA_INSTRUCTION:-}" ]] && [[ "$LI_AGENT_EXTRA_INSTRUCTION" == *"tier2_physics/"* ]]; then
  exit 0
fi
export PHYSICS_CODEGEN_LANG="${PHYSICS_CODEGEN_LANG:-li}"
export PHYSICS_CODEGEN_ARM="${PHYSICS_CODEGEN_ARM:-A}"
eval "$(BENCHMARKS_ROOT="$BENCHMARKS_ROOT" node "$SCRIPT" --export-env)"
