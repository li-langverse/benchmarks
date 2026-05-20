#!/usr/bin/env bash
# Run tier-5 HTTP throughput harness (multi-oracle wrk).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HARNESS="$ROOT/vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py"
PROFILE="${BENCH_HTTP_PROFILE:-ci}"
ORACLES="${BENCH_HTTP_ORACLES:-nginx,apache,lighttpd,li}"

if [[ ! -f "$HARNESS" ]]; then
  echo "run-tier5-http-bench: missing $HARNESS (sync vendor/lis-tier5)" >&2
  exit 1
fi

LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
LI_HTTPD_BIN="${LI_HTTPD_BIN:-$LIC_ROOT/build/li-httpd}"
if [[ ! -x "$LI_HTTPD_BIN" ]] && [[ -x "$ROOT/../lic/build/li-httpd" ]]; then
  LI_HTTPD_BIN="$ROOT/../lic/build/li-httpd"
fi

export LI_HTTPD_BIN
export BENCH_HTTP_ORACLES="$ORACLES"

python3 "$HARNESS" --profile "$PROFILE"
test -s "$ROOT/vendor/lis-tier5/results/latest.csv"
echo "run-tier5-http-bench: ok (profile=$PROFILE, oracles=$ORACLES)"
