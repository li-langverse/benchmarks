# li-langverse/benchmarks

Aggregated **benchmark status** for the Li org. Harnesses and sources stay in each code repo (`lic/benchmarks/`, `lis/benchmarks/tier5_http/`, …).

**Dashboard:** https://li-langverse.github.io/benchmarks/ (if 404, see [SETUP_GITHUB.md](SETUP_GITHUB.md#fix-dashboard-404-live_docs_down))

**Handbook:** [docs/handbook/README.md](docs/handbook/README.md) · [plan cross-links](docs/ecosystem/plan-cross-links.md) · [benchmark honesty](docs/honesty/benchmark-dashboard.md)

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

## Registry DB OLTP (tier_db_registry)

Skeleton for **lidb vs Postgres 15+** registry publish/read P95 — see [tier-db-registry-benchmark.md](docs/ecosystem/tier-db-registry-benchmark.md).

```bash
./scripts/run-db-registry-bench.sh
```

## Agents

PR-only workflow. Do **not** duplicate `lic` harness here. See [AGENTS.md](AGENTS.md).

Human setup: [SETUP_GITHUB.md](SETUP_GITHUB.md).
