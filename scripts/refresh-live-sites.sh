#!/usr/bin/env bash
# Refresh benchmarks + roadmap GitHub Pages without Actions (local build + gh-pages push).
set -euo pipefail

BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROADMAP_ROOT="$(cd "$BENCH_ROOT/../roadmap" && pwd)"
LIC_ROOT="${LIC_ROOT:-$BENCH_ROOT/../lic}"
SKIP_BENCH="${SKIP_BENCH:-0}"
SKIP_ROADMAP="${SKIP_ROADMAP:-0}"

find_with_github_env() {
  for d in "$LIC_ROOT" "$BENCH_ROOT/../li"; do
    if [[ -x "$d/scripts/with-github-env.sh" ]]; then
      export WITH_GITHUB_ENV="$d/scripts/with-github-env.sh"
      return 0
    fi
  done
  return 1
}

echo "==> benchmarks: ingest + relative summary (cpp reference)"
cd "$BENCH_ROOT"
if [[ "$SKIP_BENCH" != "1" ]]; then
  if [[ -d "$LIC_ROOT" ]]; then
    LIC_ROOT="$LIC_ROOT" LIS_ROOT="${LIS_ROOT:-$BENCH_ROOT/../lis}" ./scripts/ingest/ingest-lic.sh
  else
    echo "WARN: LIC_ROOT missing — using existing data/latest/summary.json" >&2
  fi
fi

echo "==> benchmarks: deploy Pages"
"$BENCH_ROOT/scripts/deploy-pages-local.sh" --build

if [[ "$SKIP_ROADMAP" != "1" && -d "$ROADMAP_ROOT" ]]; then
  echo "==> roadmap: regenerate snapshot markdown"
  cd "$ROADMAP_ROOT"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    chmod +x scripts/regenerate-development-overview-md.py
    python3 scripts/regenerate-development-overview-md.py
    ./scripts/refresh-development-overview.sh || true
  else
    echo "WARN: gh not authed — skip roadmap md regen; edit docs/development-overview.md manually" >&2
  fi
  echo "==> roadmap: deploy Pages"
  "$ROADMAP_ROOT/scripts/deploy-pages-local.sh" --build
fi

find_with_github_env || true
echo ""
echo "Done."
echo "  Benchmarks: https://li-langverse.github.io/benchmarks/"
echo "  Overview:   https://li-langverse.github.io/roadmap/development-overview/"
