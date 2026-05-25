# tier_db_graph_registry — registry dependency graph vs SQL / graph oracles

Benchmark tier for **package dependency graph** workloads on synthetic registry-shaped graphs: **lidb** (recursive CTE / closure tables) vs **PostgreSQL AGE** vs optional **Kùzu** sidecar.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_graph_registry/` | Suite config, scenarios, shared schema |
| `scripts/run-db-graph-registry-bench.sh` | Entry stub (writes CI manifest) |
| `data/latest/tier-db-graph-registry.json` | CI ingest artifact |
| `schema/tier-db-graph-registry-ingest.json` | Manifest JSON Schema |
| [`catalog.toml`](../../catalog.toml) | Dashboard rows (`category = database`, `tier = 6`) |

## Scenarios

| `id` | Workload | Metric |
|------|----------|--------|
| `graph_dep_closure` | Transitive dependency closure for a package (synthetic DAG) | P95 latency (ms) |
| `graph_cycle_detect` | Cycle detection on `package_deps` edge set | P95 latency (ms) |

DDL: `benchmarks/tier_db_graph_registry/schema/graph-registry-v1.sql` — applies after [`tier_db_registry/schema/registry-v1.sql`](../../benchmarks/tier_db_registry/schema/registry-v1.sql).

**Graph generator:** prefer custom registry dep graph (Li-relevant) over full LDBC SNB; see [lidb multi-model research](https://github.com/li-langverse/roadmap/blob/main/proposals/lidb-multi-model-gpu-research.md) §G.

## Run

```bash
cd benchmarks
./scripts/run-db-graph-registry-bench.sh
# Optional timed run (when harness exists):
# BENCH_DB_GRAPH_PROFILE=nightly BENCH_DB_GRAPH_RUN_HARNESS=1 ./scripts/run-db-graph-registry-bench.sh
```

Env:

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_GRAPH_PROFILE` | `ci` | `ci` = config-only; `nightly` = P95 timing @ 10⁵ edges |
| `BENCH_DB_GRAPH_EDGES` | `100000` | Synthetic edge count for nightly |
| `POSTGRES_URL` | — | Postgres 15+ with registry + graph DDL |
| `POSTGRES_AGE` | — | AGE extension enabled for graph oracle |
| `LIDB_URL` / `lis db start` | — | **lis** profile with graph module off by default |
| `BENCH_DB_GRAPH_THRESHOLD` | `1.2` | Max lidb/oracle P95 ratio for green |

## CI ingest

1. `run-db-graph-registry-bench.sh` calls `scripts/ingest/write-tier-db-graph-registry-manifest.py`.
2. Artifact: `data/latest/tier-db-graph-registry.json` (see schema).
3. Future: `benchmarks/tier_db_graph_registry/results/latest.csv` merged into `summary.json`.

**Honesty:** Until CSV exists, dashboard shows **unknown** for graph rows — not “lidb slower than AGE.”

## Plan linkage

| PH | Deliverable |
|----|-------------|
| **PH-DB-G1** | Graph module decision — evidence from this tier |
| **PH-DB-5** | Registry OLTP baseline — [`tier-db-registry-benchmark.md`](./tier-db-registry-benchmark.md) |

Nightly runs are **optional**; PR **ci** profile validates TOML + schema paths only.

## Full suite

Not yet in `run-full-benchmark-suite.sh`. Add when `BENCH_DB_GRAPH_RUN_HARNESS=1` is stable.
