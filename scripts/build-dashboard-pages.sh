#!/usr/bin/env bash
# Build dashboard-next static export for GitHub/GitLab Pages (same steps as pages.yml).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/check-reporting-platforms.py
python3 scripts/check-summary-skip-budget.py
python3 scripts/check-summary-measurement-quality.py
python3 scripts/check-dashboard-invariants.py

cd dashboard-next
export NEXT_PUBLIC_BASE_PATH=""
npm ci
npm run build
mkdir -p out/latest
for f in summary.json release-index.json benchmark-matrix.json; do
  if [[ -f "../data/latest/$f" ]]; then
    cp "../data/latest/$f" "out/latest/"
  fi
done
echo "benchmarks.lilangverse.xyz" > out/CNAME
cd ..
chmod +x scripts/check-dashboard-static-routes.sh
./scripts/check-dashboard-static-routes.sh
test -s dashboard-next/out/index.html
PAGES_DIR="${PAGES_OUTPUT_DIR:-public}"
rm -rf "$PAGES_DIR"
cp -a dashboard-next/out "$PAGES_DIR"
test -s "$PAGES_DIR/index.html"
echo "build-dashboard-pages: OK ($PAGES_DIR)"
