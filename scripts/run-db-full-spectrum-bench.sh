#!/usr/bin/env bash
# WP-N4: run all lidb full-spectrum audit tier stubs (exit 0, manifests under data/latest/).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
for s in \
  run-db-security-bench.sh \
  run-db-memory-bench.sh \
  run-db-parallel-bench.sh \
  run-db-audit-bench.sh \
  run-db-realtime-bench.sh; do
  chmod +x "scripts/$s"
  "./scripts/$s"
done
