#!/usr/bin/env bash
# One command: build lic → run GPU suite → create data/gpu-contributions/<slug>/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
SUBMIT="$ROOT/scripts/ingest/submit-gpu-contribution.sh"

usage() {
  cat <<'EOF'
Usage: donate-gpu-chip.sh <chip-slug> ["GPU label"]

  chip-slug    e.g. nvidia-rtx-3090-linux, apple-m1-macos
  GPU label    optional — auto-detected from nvidia-smi / system_profiler when omitted

Env:
  LIC_ROOT           lic checkout (default: ../lic)
  SKIP_LIC_BUILD=1   skip ./scripts/build.sh when lic binary exists
  GPU_CHIP_UPDATE=1  refresh an existing contribution folder (re-run suite + replace JSON)
  CONTRIBUTOR_GITHUB, ANONYMOUS_OK=1, PRIMARY_BACKEND, HOST_OS, CPU_MODEL

Example (everything in one shot):
  ./scripts/donate-gpu-chip.sh nvidia-rtx-3090-linux

  CONTRIBUTOR_GITHUB=you ./scripts/donate-gpu-chip.sh apple-m1-macos "Apple M1 Pro"
EOF
}

if [[ $# -lt 1 ]]; then usage; exit 1; fi

SLUG="$1"
LABEL="${2:-}"

resolve_lic_root() {
  if [[ -d "$LIC_ROOT" ]]; then
    return 0
  fi
  for candidate in "$ROOT/../lic" "$ROOT/../lic-gpu-bench-5b3a"; do
    if [[ -d "$candidate" ]]; then
      LIC_ROOT="$candidate"
      export LIC_ROOT
      return 0
    fi
  done
  echo "ERROR: lic not found — set LIC_ROOT to your li-langverse/lic checkout" >&2
  exit 1
}

detect_cpu_model() {
  if [[ -n "${CPU_MODEL:-}" ]]; then
    return 0
  fi
  if [[ -r /proc/cpuinfo ]]; then
    CPU_MODEL="$(awk -F: '/model name/{print $2; exit}' /proc/cpuinfo | sed 's/^[ \t]*//')"
  elif [[ "$(uname -s)" == Darwin ]]; then
    CPU_MODEL="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || true)"
  fi
  export CPU_MODEL
}

detect_gpu_label() {
  if [[ -n "$LABEL" ]]; then
    return 0
  fi
  if command -v nvidia-smi >/dev/null 2>&1; then
    LABEL="$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1 | sed 's/^[ \t]*//')"
  elif [[ "$(uname -s)" == Darwin ]]; then
    LABEL="$(system_profiler SPDisplaysDataType 2>/dev/null | awk -F: '/Chipset Model/{print $2; exit}' | sed 's/^[ \t]*//')"
  fi
  if [[ -z "$LABEL" ]]; then
    echo "ERROR: could not detect GPU name — pass label as second argument" >&2
    exit 1
  fi
}

lic_binary() {
  local bin="$LIC_ROOT/build/compiler/lic/lic"
  if [[ -x "$bin" ]]; then
    echo "$bin"
    return 0
  fi
  if [[ -x "$LIC_ROOT/lic" ]]; then
    echo "$LIC_ROOT/lic"
    return 0
  fi
  return 1
}

ensure_lic_built() {
  if lic_binary >/dev/null 2>&1; then
    if [[ "${SKIP_LIC_BUILD:-}" == "1" ]]; then
      return 0
    fi
  fi
  if [[ ! -x "$LIC_ROOT/scripts/build.sh" ]]; then
    echo "ERROR: $LIC_ROOT/scripts/build.sh missing" >&2
    exit 1
  fi
  echo "donate-gpu-chip: building lic in $LIC_ROOT …"
  (cd "$LIC_ROOT" && ./scripts/build.sh)
}

run_gpu_suite() {
  echo "donate-gpu-chip: running GPU suite on this machine …"
  if [[ -x "$LIC_ROOT/scripts/bench-lig-gpu-suite.sh" ]]; then
    (cd "$LIC_ROOT" && ./scripts/bench-lig-gpu-suite.sh)
    return 0
  fi
  if [[ -x "$LIC_ROOT/scripts/bench-full-gpu-suite.sh" ]]; then
    (cd "$LIC_ROOT" && ./scripts/bench-full-gpu-suite.sh)
    return 0
  fi
  local harness="$LIC_ROOT/benchmarks/harness/lig_gpu_suite_report.py"
  local lic_bin
  lic_bin="$(lic_binary)"
  if [[ -f "$harness" ]]; then
    mkdir -p "$LIC_ROOT/benchmarks/results"
    python3 "$harness" \
      --lic "$lic_bin" \
      --out "$LIC_ROOT/benchmarks/results/lig-gpu-suite-latest.json"
    return 0
  fi
  echo "ERROR: no GPU suite harness in $LIC_ROOT (need bench-lig-gpu-suite.sh or lig_gpu_suite_report.py)" >&2
  exit 1
}

maybe_refresh_existing() {
  local dest="$ROOT/data/gpu-contributions/$SLUG"
  if [[ ! -d "$dest" ]]; then
    return 0
  fi
  if [[ "${GPU_CHIP_UPDATE:-}" != "1" ]]; then
    echo "ERROR: $dest exists — set GPU_CHIP_UPDATE=1 to refresh timings in place" >&2
    exit 1
  fi
  echo "donate-gpu-chip: updating existing contribution $SLUG …"
  cp "$LIC_ROOT/benchmarks/results/lig-gpu-suite-latest.json" "$dest/"
  if [[ -f "$LIC_ROOT/benchmarks/results/lig-gpu-suite-honest.json" ]]; then
    cp "$LIC_ROOT/benchmarks/results/lig-gpu-suite-honest.json" "$dest/"
  fi
  python3 "$ROOT/scripts/ingest/validate-gpu-contribution.py" "$SLUG"
  python3 "$ROOT/scripts/ingest/build-lig-gpu-matrix.py"
  echo ""
  echo "Updated $dest — commit and push your PR."
  exit 0
}

resolve_lic_root
detect_cpu_model
detect_gpu_label
maybe_refresh_existing
ensure_lic_built
run_gpu_suite

export LIC_ROOT CPU_MODEL
exec "$SUBMIT" "$SLUG" "$LABEL"
