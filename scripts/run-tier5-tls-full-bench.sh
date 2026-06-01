#!/usr/bin/env bash
# Full tier-5 HTTPS benches (wrk + openssl s_time, cert matrix).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
LI_HTTPD_BIN="${LI_HTTPD_BIN:-$LIC_ROOT/build/li-httpd}"

export LIC_ROOT
export LI_HTTPD_BIN
export BENCH_HTTP_PROFILE="${BENCH_HTTP_PROFILE:-nightly}"
export BENCH_TLS_ORACLES="${BENCH_TLS_ORACLES:-nginx,apache,lighttpd,caddy,traefik,li}"
export BENCH_HTTP_ORACLES="${BENCH_HTTP_ORACLES:-nginx,apache,lighttpd,caddy,node,bun,li}"

echo "==> TLS oracle deps"
if [[ -x "$ROOT/scripts/install-bench-tls-oracles.sh" ]]; then
  bash "$ROOT/scripts/install-bench-tls-oracles.sh"
fi

for bin in openssl wrk nginx; do
  if ! command -v "$bin" >/dev/null; then
    echo "run-tier5-tls-full-bench: missing required $bin on PATH" >&2
    exit 1
  fi
done

if [[ ! -x "$LI_HTTPD_BIN" ]]; then
  echo "run-tier5-tls-full-bench: LI_HTTPD_BIN not executable: $LI_HTTPD_BIN" >&2
  exit 1
fi

echo "==> tier-5 HTTP nightly (includes https_static + https_tls_matrix)"
"$ROOT/scripts/run-tier5-http-bench.sh"

echo "==> matrix report"
python3 "$ROOT/scripts/benchmark-matrix-report.py"

echo "==> TLS rows (grep https)"
grep -E '^https_' "$ROOT/vendor/lis-tier5/results/latest.csv" | head -80 || true

echo "run-tier5-tls-full-bench: ok"
