#!/usr/bin/env bash
# Run the full Li org benchmark suite and refresh dashboard summary (agents: run after every implementation).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
PROFILE="${BENCH_PROFILE:-full}"
RUNS="${BENCH_RUNS:-3}"
SKIP_BUILD="${SKIP_BUILD:-0}"
SKIP_TIER0="${SKIP_TIER0:-0}"

log() { echo "==> $*"; }

if [[ ! -d "$LIC_ROOT" ]]; then
  echo "LIC_ROOT=$LIC_ROOT missing — clone li-langverse/lic next to benchmarks" >&2
  exit 1
fi

export LIC_ROOT LIS_ROOT LI_REPO_ROOT="$LIC_ROOT"
export PATH="$LIC_ROOT/build/compiler/lic:$PATH"

if [[ "$SKIP_BUILD" != "1" ]]; then
  log "setup lic + li-httpd"
  "$ROOT/scripts/setup-lic-for-bench.sh"
fi

export LIC="$LIC_ROOT/build/compiler/lic/lic"
export LI_HTTPD_BIN="$LIC_ROOT/build/li-httpd"
export CC="${CC:-clang-18}"
export CXX="${CXX:-clang++-18}"

cd "$LIC_ROOT"
mkdir -p benchmarks/results

if [[ "$SKIP_TIER0" != "1" ]]; then
  log "tier 0 — li-tests + verify + stability"
  if ! python3 benchmarks/harness/bench.py --tier 0; then
    echo "WARN: tier0 failed (li-tests/verify) — continuing perf tiers" >&2
  fi
fi

log "tier 1+2 — micro + physics (runs=$RUNS)"
python3 - <<'PY' "$RUNS" "$LIC_ROOT"
import os, sys
from pathlib import Path

runs = int(sys.argv[1])
lic = Path(sys.argv[2])
os.chdir(lic)
sys.path.insert(0, "benchmarks/harness")
from bench import TIER1_BENCHES, TIER2_BENCHES, run_tier_benches, run_benchmark, read_csv, write_csv, merge_rows, RESULTS

out = RESULTS / "latest.csv"
merged = read_csv(out)
failed: list[str] = []

def run_specs(label: str, specs):
    global merged
    for spec in specs:
        try:
            rows = run_benchmark(spec, runs=runs)
            merged = merge_rows(merged, rows, benchmark=spec.name)
            write_csv(out, merged)
            print(f"ok {spec.name}", flush=True)
        except Exception as exc:
            failed.append(spec.name)
            print(f"WARN skip {spec.name}: {exc}", file=sys.stderr, flush=True)

run_specs("tier-1", TIER1_BENCHES)
run_specs("tier-2", TIER2_BENCHES)
if failed:
    print(f"tier12: {len(failed)} skipped: {', '.join(failed)}", file=sys.stderr)
print(f"updated {out}")
PY

log "tier 3 — ecosystem (compile, security, async)"
python3 benchmarks/harness/bench_ecosystem.py --runs "$RUNS" || { echo "tier3 failed" >&2; exit 1; }

log "tier 5 — HTTP (static_small, keepalive_pipelining, proxy_loopback)"
python3 "$ROOT/scripts/tier5-http-bench.py" --lic-root "$LIC_ROOT" --runs "${HTTP_BENCH_RUNS:-5}" || {
  echo "WARN: tier5 http failed" >&2
}

# Merge HTTP rows into lic latest.csv for ingest
python3 - <<'PY' "$LIC_ROOT"
import csv
import sys
from pathlib import Path

lic = Path(sys.argv[1])
latest = lic / "benchmarks/results/latest.csv"
http = lic / "benchmarks/results/http_tier5.csv"
header = None
rows = []
if latest.is_file():
    with latest.open(newline="") as f:
        r = csv.DictReader(f)
        header = r.fieldnames
        rows = [row for row in r if row.get("benchmark") not in {
            "static_small", "keepalive_pipelining", "proxy_loopback"
        }]
if http.is_file():
    with http.open(newline="") as f:
        r = csv.DictReader(f)
        header = header or r.fieldnames
        rows.extend(list(r))
if not header:
    sys.exit(0)
with latest.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader()
    w.writerows(rows)
print(f"merged http into {latest}")
PY

cd "$ROOT"
log "ingest + summary.json"
LIC_ROOT="$LIC_ROOT" LIS_ROOT="$LIS_ROOT" ./scripts/ingest/ingest-lic.sh || true

log "benchmark status report"
./scripts/benchmark-failures-report.sh || true

log "done — see data/latest/summary.json"
