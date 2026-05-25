# li-langverse/benchmarks

Aggregated **benchmark status** for the Li org. Harnesses and sources stay in each code repo (`lic/benchmarks/`, `lis/benchmarks/tier5_http/`, …).

**Dashboard:** https://li-langverse.github.io/benchmarks/ (if 404, see [SETUP_GITHUB.md](SETUP_GITHUB.md#fix-dashboard-404-live_docs_down))

**Handbook:** [docs/handbook/README.md](docs/handbook/README.md) · [plan cross-links](docs/ecosystem/plan-cross-links.md) · [benchmark honesty](docs/honesty/benchmark-dashboard.md)

**Dashboard architecture:** [docs/dashboard/ARCHITECTURE.md](docs/dashboard/ARCHITECTURE.md) · [invariants (CI)](docs/dashboard/INVARIANTS.md) · [coverage gaps](docs/dashboard/coverage-gap-analysis.md) · [design system](docs/dashboard/design-system.md)

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

## lidb research tiers (PH-DB-G0 stubs)

| Tier | Doc | Run |
|------|-----|-----|
| `tier_db_graph_registry` | [tier-db-graph-registry.md](docs/ecosystem/tier-db-graph-registry.md) | `./scripts/run-db-graph-registry-bench.sh` |
| `tier_db_vector_ann` | [tier-db-vector-ann.md](docs/ecosystem/tier-db-vector-ann.md) | `./scripts/run-db-vector-ann-bench.sh` |
| `tier_db_gpu_speedup` | [tier-db-gpu-speedup.md](docs/ecosystem/tier-db-gpu-speedup.md) | `./scripts/run-db-gpu-speedup-bench.sh` |

CI writes stub manifests under `data/latest/tier-db-*.json` (no GPU required on GHA).

## lidb full-spectrum audit (WP-N4 stubs)

| Tier | Measures | Doc | Run |
|------|----------|-----|-----|
| `tier_db_security` | injection blocked, RLS bypass | [tier-db-security.md](docs/ecosystem/tier-db-security.md) | `./scripts/run-db-security-bench.sh` |
| `tier_db_memory` | RSS idle, peak under load | [tier-db-memory.md](docs/ecosystem/tier-db-memory.md) | `./scripts/run-db-memory-bench.sh` |
| `tier_db_parallel` | concurrent readers/writers | [tier-db-parallel.md](docs/ecosystem/tier-db-parallel.md) | `./scripts/run-db-parallel-bench.sh` |
| `tier_db_audit` | query log, tamper evidence | [tier-db-audit.md](docs/ecosystem/tier-db-audit.md) | `./scripts/run-db-audit-bench.sh` |
| `tier_db_realtime` | WS publish→client latency | [tier-db-realtime.md](docs/ecosystem/tier-db-realtime.md) | `./scripts/run-db-realtime-bench.sh` |

All five: `./scripts/run-db-full-spectrum-bench.sh`

## Agents

PR-only workflow. Do **not** duplicate `lic` harness here. See [AGENTS.md](AGENTS.md).

Human setup: [SETUP_GITHUB.md](SETUP_GITHUB.md).
