#!/usr/bin/env bash
# Build dashboard-next static export, stage data/latest artifacts, serve locally for demo recording.
# Does not record video — prints macOS / QuickTime / ffmpeg hints.
set -euo pipefail

BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DASH="$BENCH_ROOT/dashboard-next"
OUT="$DASH/out"
PORT="${DEMO_PORT:-4321}"
HOST="${DEMO_HOST:-127.0.0.1}"
BASE_URL="http://${HOST}:${PORT}/benchmarks/"

echo "==> Li benchmarks dashboard demo prep"
echo "    repo: $BENCH_ROOT"

if [[ ! -d "$DASH" ]]; then
  echo "error: missing dashboard-next at $DASH" >&2
  exit 1
fi

echo "==> install + build (dashboard-next)"
cd "$DASH"
if [[ -f package-lock.json ]]; then
  npm ci
else
  npm install
fi
npm run build

echo "==> copy ingest artifacts into static export"
mkdir -p "$OUT/latest"
for f in summary.json release-index.json benchmark-matrix.json proof-posture.json; do
  src="$BENCH_ROOT/data/latest/$f"
  if [[ -f "$src" ]]; then
    cp "$src" "$OUT/latest/"
    echo "    copied $f"
  else
    echo "    skip (missing): data/latest/$f"
  fi
done

hist="$BENCH_ROOT/data/history/index.json"
if [[ -f "$hist" ]]; then
  mkdir -p "$OUT/history"
  cp "$hist" "$OUT/history/index.json"
  echo "    copied data/history/index.json"
else
  echo "    skip (missing): data/history/index.json"
fi

echo ""
echo "==> Recording guide"
echo "    Open: $BASE_URL"
echo "    Script: docs/dashboard/demo-video-script.md"
echo "    Storyboard: docs/dashboard/demo-storyboard.html"
echo ""
echo "    Dev alternative (hot reload):"
echo "      cd dashboard-next && npm run dev"
echo "      open http://localhost:3000/benchmarks/"
echo ""
echo "    macOS capture (pick one):"
echo "      • QuickTime Player → File → New Screen Recording"
echo "      • Cursor IDE browser → walk beats without producing a file"
if command -v ffmpeg >/dev/null 2>&1; then
  echo "      • ffmpeg (list displays): ffmpeg -f avfoundation -list_devices true -i \"\""
  echo "      • ffmpeg example (screen index may differ):"
  echo "        ffmpeg -f avfoundation -framerate 30 -capture_cursor 1 -i \"1:none\" -pix_fmt yuv420p ~/Desktop/li-benchmarks-demo.mp4"
else
  echo "      • ffmpeg: not installed (brew install ffmpeg for CLI capture)"
fi
echo ""
echo "==> serve static export (Ctrl+C to stop)"
echo "    cd $OUT && python3 -m http.server $PORT --bind $HOST"
echo ""

cd "$OUT"
exec python3 -m http.server "$PORT" --bind "$HOST"
