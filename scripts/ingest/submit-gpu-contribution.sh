#!/usr/bin/env bash
# Scaffold a GPU chip contribution PR from lic benchmark results.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"

usage() {
  cat <<'EOF'
Usage: submit-gpu-contribution.sh <chip-slug> "<GPU label>"

  chip-slug   e.g. nvidia-rtx-3090-linux, apple-m1-macos
  GPU label   e.g. "NVIDIA GeForce RTX 3090"

Env: LIC_ROOT, CONTRIBUTOR_GITHUB, ANONYMOUS_OK=1, PRIMARY_BACKEND, HOST_OS, CPU_MODEL

Example:
  LIC_ROOT=../lic ./scripts/ingest/submit-gpu-contribution.sh \\
    nvidia-rtx-3090-linux "NVIDIA GeForce RTX 3090"
EOF
}

if [[ $# -lt 2 ]]; then usage; exit 1; fi

SLUG="$1"
LABEL="$2"
DEST="$ROOT/data/gpu-contributions/$SLUG"

if [[ ! "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "ERROR: chip-slug must be lowercase alphanumeric with hyphens" >&2
  exit 1
fi
if [[ -d "$DEST" ]]; then
  echo "ERROR: $DEST already exists" >&2
  exit 1
fi

SUITE="$LIC_ROOT/benchmarks/results/lig-gpu-suite-latest.json"
HONEST="$LIC_ROOT/benchmarks/results/lig-gpu-suite-honest.json"
if [[ ! -f "$SUITE" ]]; then
  echo "ERROR: Run GPU suite in lic: cd \$LIC_ROOT && ./scripts/bench-lig-gpu-suite.sh" >&2
  exit 1
fi

HOST_OS="${HOST_OS:-}"
case "$(uname -s)" in
  Linux) HOST_OS="${HOST_OS:-Linux}" ;;
  Darwin) HOST_OS="${HOST_OS:-macOS}" ;;
  *) HOST_OS="${HOST_OS:-$(uname -s)}" ;;
esac

PRIMARY_BACKEND="${PRIMARY_BACKEND:-}"
if [[ -z "$PRIMARY_BACKEND" ]]; then
  case "$SLUG" in
    *apple*|*m1*|*m2*|*m3*|*m4*) PRIMARY_BACKEND=metal ;;
    *amd*|*rocm*|*rx-*) PRIMARY_BACKEND=hip ;;
    *) PRIMARY_BACKEND=cuda ;;
  esac
fi

VENDOR=other
case "$SLUG" in
  nvidia-*|*rtx*|*gtx*) VENDOR=nvidia ;;
  amd-*|*rx-*|*rocm*) VENDOR=amd ;;
  apple-*|*m1*|*m2*|*m3*|*m4*) VENDOR=apple ;;
esac

mkdir -p "$DEST"
cp "$SUITE" "$DEST/lig-gpu-suite-latest.json"
HAS_HONEST=false
if [[ -f "$HONEST" ]]; then
  cp "$HONEST" "$DEST/lig-gpu-suite-honest.json"
  HAS_HONEST=true
fi

if [[ "${ANONYMOUS_OK:-}" == "1" ]]; then
  GITHUB_JSON='"anonymous_ok": true'
elif [[ -n "${CONTRIBUTOR_GITHUB:-}" ]]; then
  GITHUB_JSON="\"github\": \"${CONTRIBUTOR_GITHUB}\""
else
  echo "WARN: Set CONTRIBUTOR_GITHUB or ANONYMOUS_OK=1" >&2
  GITHUB_JSON='"anonymous_ok": true'
fi

SUBMITTED="$(date -u +%Y-%m-%d)"
python3 - "$DEST/contribution.json" "$SLUG" "$LABEL" "$VENDOR" "$HOST_OS" "$PRIMARY_BACKEND" \
  "$SUBMITTED" "$GITHUB_JSON" "${CPU_MODEL:-}" "$HAS_HONEST" <<'PY'
import json, sys
from pathlib import Path

dest, slug, label, vendor, host_os, backend, submitted, github_json, cpu_model, has_honest = sys.argv[1:11]
contributor = json.loads("{" + github_json + "}")
hardware = {"gpu_name": label}
if cpu_model:
    hardware["cpu_model"] = cpu_model
artifacts = {"lig_gpu_suite": "lig-gpu-suite-latest.json"}
if has_honest == "true":
    artifacts["lig_gpu_honest"] = "lig-gpu-suite-honest.json"
manifest = {
    "schema": "benchmarks/gpu-chip-contribution/v1",
    "chip_slug": slug,
    "label": label,
    "vendor": vendor,
    "host_os": host_os,
    "primary_backend": backend,
    "contributor": contributor,
    "hardware": hardware,
    "artifacts": artifacts,
    "submitted_at": submitted,
    "notes": "Community GPU chip donation — see docs/ecosystem/gpu-chip-contributions.md",
}
Path(dest).write_text(json.dumps(manifest, indent=2) + "\n")
PY

python3 "$ROOT/scripts/ingest/validate-gpu-contribution.py" "$SLUG"
python3 "$ROOT/scripts/ingest/build-lig-gpu-matrix.py"
echo "Created $DEST — open PR with data/gpu-contributions/$SLUG/"
