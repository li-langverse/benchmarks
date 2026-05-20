#!/usr/bin/env bash
# Render benchmark PNGs/GIFs into data/visuals/latest/ (lic shareables + lis HTTP).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
OUT="${ROOT}/data/visuals/latest"
SHARE_SRC="${LIC_ROOT}/benchmarks/results/share"

export MPLBACKEND=Agg
mkdir -p "$OUT"
did_any=0

if [[ -d "$LIC_ROOT/benchmarks/harness" ]]; then
  echo "Rendering visuals in lic..."
  if chmod +x "${LIC_ROOT}/scripts/plot_shareables.sh" 2>/dev/null \
    && (cd "$LIC_ROOT" && ./scripts/plot_shareables.sh); then
    echo "Copying shareables to $OUT ..."
    if [[ -d "$SHARE_SRC" ]]; then
      find "$SHARE_SRC" -maxdepth 1 -type f \( -name '*.png' -o -name '*.gif' \) -exec cp -t "$OUT" {} + 2>/dev/null || true
      did_any=1
    fi
  else
    echo "skip lic shareables (plot_shareables failed — venv/mpl?)"
  fi
else
  echo "skip lic shareables (LIC_ROOT missing or no harness)"
fi

LIS_CSV="${LIS_ROOT}/results/latest.csv"
if [[ -f "$LIS_CSV" ]]; then
  echo "Plotting HTTP tier-5 from $LIS_CSV ..."
  python3 "${ROOT}/scripts/plot_http_benchmarks.py" --lis-csv "$LIS_CSV" --out "$OUT"
  did_any=1
elif [[ -f "${ROOT}/data/latest/summary.json" ]]; then
  echo "Plotting HTTP tier-5 from summary.json ..."
  python3 "${ROOT}/scripts/plot_http_benchmarks.py" --summary "${ROOT}/data/latest/summary.json" --out "$OUT"
  did_any=1
fi

if [[ "$did_any" -eq 0 ]]; then
  echo "warning: no visuals produced (set LIC_ROOT and/or LIS_ROOT)" >&2
  exit 1
fi

python3 "${ROOT}/scripts/visual-manifest.py" "$OUT"
echo "Done. See ${OUT}/manifest.json"
