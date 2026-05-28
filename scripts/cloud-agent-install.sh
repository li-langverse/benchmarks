#!/usr/bin/env bash
# Cursor Cloud "install / update" entrypoint — safe under set -u (no LLVM_DIR=$LLVM_DIR bug).
# Configure the Cloud Agent environment install script as:
#   bash /agent/repos/benchmarks/scripts/cloud-agent-install.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "$ROOT/scripts/update-cloud-agent-env.sh" "$@"
