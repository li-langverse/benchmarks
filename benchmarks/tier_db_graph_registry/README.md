# tier_db_graph_registry — registry dependency graph benchmarks

Compare **lidb** graph queries (CTE / closure) against **PostgreSQL AGE** and optional **Kùzu** on synthetic `package_deps` graphs aligned with registry DDL.

## Scenarios

| Scenario | Workload | Primary metric |
|----------|----------|----------------|
| `graph_dep_closure` | Transitive deps from a root package | P95 latency (ms) |
| `graph_cycle_detect` | Cycle detection on edge set | P95 latency (ms) |

## Profiles

| Profile | Timing | When |
|---------|--------|------|
| `ci` | off | PR smoke |
| `nightly` | on @ 10⁵ edges | Scheduled / manual |

## Schema

- [`schema/graph-registry-v1.sql`](schema/graph-registry-v1.sql) — `package_deps` on top of registry tables
- Base DDL: [`../tier_db_registry/schema/registry-v1.sql`](../tier_db_registry/schema/registry-v1.sql)

## Run (stub)

```bash
cd benchmarks
./scripts/run-db-graph-registry-bench.sh
cat data/latest/tier-db-graph-registry.json
```

## CI ingest

Manifest: `data/latest/tier-db-graph-registry.json` — [`schema/tier-db-graph-registry-ingest.json`](../../schema/tier-db-graph-registry-ingest.json).

**PH-DB-G1** — see [tier-db-graph-registry.md](../../docs/ecosystem/tier-db-graph-registry.md).
