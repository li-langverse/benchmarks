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
SKIP_EXPLOITS="${SKIP_EXPLOITS:-0}"

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
if command -v clang-22 >/dev/null 2>&1; then
  export CC="${CC:-clang-22}"
  export CXX="${CXX:-clang++-22}"
elif command -v clang-18 >/dev/null 2>&1; then
  export CC="${CC:-clang-18}"
  export CXX="${CXX:-clang++-18}"
else
  export CC="${CC:-clang}"
  export CXX="${CXX:-clang++}"
fi

cd "$LIC_ROOT"
mkdir -p benchmarks/results

if [[ "$SKIP_TIER0" != "1" ]]; then
  log "tier 0 — li-tests + verify + stability"
  if ! python3 benchmarks/harness/bench.py --tier 0; then
    echo "WARN: tier0 failed (li-tests/verify) — continuing perf tiers" >&2
  fi
fi

log "tier 1+2+7 — micro + physics + registry family aliases (runs=$RUNS)"
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

log "tier 7 — algo_registry family-template aliases"
python3 benchmarks/harness/bench.py --tier 7 --runs "$RUNS" --skip-verify || {
  echo "WARN: tier7 registry aliases failed — continuing" >&2
}

log "tier 3 — ecosystem (compile, security, async)"
python3 benchmarks/harness/bench_ecosystem.py --runs "$RUNS"

if [[ "${SKIP_TIER5_HTTP:-0}" == "1" ]]; then
  log "tier 5 — HTTP multi-oracle skipped (SKIP_TIER5_HTTP=1)"
else
log "tier 5 — HTTP multi-oracle (nginx, apache, lighttpd, node, bun, li)"
export BENCH_HTTP_PROFILE="${BENCH_HTTP_PROFILE:-nightly}"
export BENCH_HTTP_ORACLES="${BENCH_HTTP_ORACLES:-nginx,apache,lighttpd,node,bun,li}"
if [[ -f "$ROOT/scripts/run-tier5-http-bench.sh" ]]; then
  "$ROOT/scripts/run-tier5-http-bench.sh" || echo "WARN: multi-oracle tier5 failed" >&2
else
  echo "WARN: missing run-tier5-http-bench.sh (sync vendor/lis-tier5)" >&2
fi

log "tier 5 — supplemental proxy_loopback (li_epoll + li c_epoll vs nginx)"
python3 "$ROOT/scripts/tier5-http-bench.py" --lic-root "$LIC_ROOT" --runs "${HTTP_BENCH_RUNS:-5}" || {
  echo "WARN: tier5 supplemental http failed" >&2
}
fi

if [[ "$SKIP_EXPLOITS" != "1" ]] && [[ -f "$ROOT/scripts/run-tier5-http-exploits.sh" ]]; then
  log "tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=${TIER5_EXPLOIT_PROFILE:-pr})"
  export TIER5_EXPLOIT_PROFILE="${TIER5_EXPLOIT_PROFILE:-pr}"
  export TIER5_EXPLOIT_LANGS="${TIER5_EXPLOIT_LANGS:-nginx,apache,li}"
  if ! "$ROOT/scripts/run-tier5-http-exploits.sh"; then
    echo "WARN: tier5 HTTP exploits had failures (see exploit_report.csv)" >&2
  fi
else
  log "tier 5 — HTTP exploits skipped (SKIP_EXPLOITS=1)"
fi

# Merge tier-5 CSV rows into lic latest.csv for ingest
python3 - <<'PY' "$ROOT" "$LIC_ROOT"
import csv
import sys
from pathlib import Path

root = Path(sys.argv[1])
lic = Path(sys.argv[2])
latest = lic / "benchmarks/results/latest.csv"
tier5_vendor = root / "vendor/lis-tier5/results/latest.csv"
tier5_extra = lic / "benchmarks/results/http_tier5.csv"

import tomllib

catalog = tomllib.loads((root / "catalog.toml").read_text(encoding="utf-8"))
http_ids = {b["id"] for b in catalog.get("benchmark", []) if b.get("category") == "http"}

header = None
rows = []
if latest.is_file():
    with latest.open(newline="") as f:
        r = csv.DictReader(f)
        header = r.fieldnames
        rows = [row for row in r if row.get("benchmark") not in http_ids]

def extend_csv(path: Path, *, supplemental: bool = False) -> None:
    global header
    if not path.is_file():
        return
    with path.open(newline="") as f:
        r = csv.DictReader(f)
        header = header or r.fieldnames
        for row in r:
            bid = row.get("benchmark") or ""
            lang = row.get("lang") or ""
            variant = row.get("variant") or ""
            metric = row.get("metric") or ""
            key = (bid, lang, variant, metric)
            if supplemental:
                if bid != "proxy_loopback":
                    continue
                if key in seen_http:
                    continue
                if lang == "li" and variant not in ("c_epoll", "li_epoll"):
                    continue
                if lang == "nginx":
                    continue
            else:
                seen_http.add(key)
            rows.append(row)

seen_http: set[tuple[str, str, str, str]] = set()
extend_csv(tier5_vendor)
extend_csv(tier5_extra, supplemental=True)
if not header:
    sys.exit(0)
with latest.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader()
    w.writerows(rows)
print(f"merged tier5 ({tier5_vendor.name if tier5_vendor.is_file() else '—'} + extra) into {latest}")
PY

cd "$ROOT"
log "ingest + summary.json"
LIC_ROOT="$LIC_ROOT" LIS_ROOT="$LIS_ROOT" ./scripts/ingest/ingest-lic.sh || true

log "benchmark status report"
./scripts/benchmark-failures-report.sh || true

log "full benchmark matrix (perf + HTTP oracles + exploits)"
python3 "$ROOT/scripts/benchmark-matrix-report.py" --json-only || true
echo "matrix: $ROOT/data/latest/benchmark-matrix.md"

log "done — see data/latest/summary.json and data/latest/benchmark-matrix.md"
