#!/usr/bin/env bash
# Render lic benchmark PNGs/GIFs into benchmarks/data/visuals/latest/ (for Cursor Automations + PR links).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
OUT="${ROOT}/data/visuals/latest"
SHARE_SRC="${LIC_ROOT}/benchmarks/results/share"

if [[ ! -d "$LIC_ROOT/benchmarks/harness" ]]; then
  echo "error: lic not found at $LIC_ROOT (set LIC_ROOT)" >&2
  exit 1
fi

export MPLBACKEND=Agg
echo "Rendering visuals in lic..."
chmod +x "${LIC_ROOT}/scripts/plot_shareables.sh"
(cd "$LIC_ROOT" && ./scripts/plot_shareables.sh)

mkdir -p "$OUT"
echo "Copying shareables to $OUT ..."
find "$SHARE_SRC" -maxdepth 1 -type f \( -name '*.png' -o -name '*.gif' \) -exec cp -t "$OUT" {} +

python3 "${ROOT}/scripts/visual-manifest.py" "$OUT"
echo "Done. See ${OUT}/manifest.json"
