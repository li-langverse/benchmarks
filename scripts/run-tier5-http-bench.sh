#!/usr/bin/env bash
# Run tier-5 HTTP throughput harness (multi-oracle wrk).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HARNESS="$ROOT/vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py"
# ``ci`` profile has timing=false (TOML-only); use ``nightly`` for wrk RPS rows.
PROFILE="${BENCH_HTTP_PROFILE:-nightly}"
ORACLES="${BENCH_HTTP_ORACLES:-nginx,apache,lighttpd,node,bun,li}"
export BENCH_PROXY_ORACLES="${BENCH_PROXY_ORACLES:-nginx,apache,lighttpd,caddy,li}"

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
export LIC_ROOT
export BENCH_HTTP_ORACLES="$ORACLES"
export BENCH_HTTP_QUICK_SEC="${BENCH_HTTP_QUICK_SEC:-}"

python3 "$HARNESS" --profile "$PROFILE" --csv "$ROOT/vendor/lis-tier5/results/latest.csv"
test -s "$ROOT/vendor/lis-tier5/results/latest.csv"
echo "run-tier5-http-bench: ok (profile=$PROFILE, oracles=$ORACLES)"
