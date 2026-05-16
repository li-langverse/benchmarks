# li-langverse/benchmarks

Aggregated **benchmark status** for the Li org. Harnesses and sources stay in each code repo (`lic/benchmarks/`, `lis/benchmarks/tier5_http/`, …).

**Dashboard:** https://li-langverse.github.io/benchmarks/

## Quick start

```bash
# Refresh summary from sibling lic checkout
./scripts/ingest/ingest-lic.sh

# Static dashboard (PH-IO-5 — matches GitHub Pages)
LIC_ROOT=../lic ./scripts/dashboard/render-static.sh
# Optional Vite dev (filters; not used on Pages deploy)
cd dashboard && npm install && npm run dev
```

## Add a benchmark

1. Implement in the owning repo (usually `lic`).
2. Add a `[[benchmark]]` row to [`catalog.toml`](catalog.toml).
3. Run ingest after CI produces CSV.

## Agents

PR-only workflow. Do **not** duplicate `lic` harness here. See [AGENTS.md](AGENTS.md).

Human setup: [SETUP_GITHUB.md](SETUP_GITHUB.md).
