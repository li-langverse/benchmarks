#!/usr/bin/env bash
# Fail if any catalog row in summary.json is red.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUMMARY="$ROOT/data/latest/summary.json"
[[ -f "$SUMMARY" ]] || { echo "missing $SUMMARY — run ingest-lic.sh first" >&2; exit 1; }
python3 - "$SUMMARY" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
red = [r["benchmark"] for r in data["rows"] if r["status"] == "red"]
if red:
    print("regression check failed:", ", ".join(red), file=sys.stderr)
    sys.exit(1)
print("regression check ok:", len(data["rows"]), "rows")
PY
