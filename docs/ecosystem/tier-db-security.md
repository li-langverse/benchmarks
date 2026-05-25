# tier_db_security — injection and RLS bypass probes

Benchmark tier for **lidb** security audit: SQL injection must fail closed; row-level security bypass attempts must not succeed.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_security/` | Suite config, scenarios, stub schema |
| `scripts/run-db-security-bench.sh` | Entry stub (writes CI manifest) |
| `data/latest/tier-db-security.json` | CI ingest artifact |
| `schema/tier-db-security-ingest.json` | Manifest JSON Schema |
| [`catalog.toml`](../../catalog.toml) | Dashboard rows (`category = security`, `tier = 6`) |

## Scenarios

| `id` | Measures | Metric |
|------|----------|--------|
| `injection_blocked` | Parameterized / escaped SQL injection probes | `pass_rate` |
| `rls_bypass_blocked` | Cross-tenant / elevated-role RLS bypass attempts | `pass_rate` |

DDL stub: `benchmarks/tier_db_security/schema/security-audit-v1.sql`.

## Run

```bash
cd benchmarks
./scripts/run-db-security-bench.sh
# Or all WP-N4 tiers:
./scripts/run-db-full-spectrum-bench.sh
```

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_SECURITY_PROFILE` | `ci` | `ci` = config-only; `nightly` = timed probes |
| `BENCH_DB_SECURITY_RUN_HARNESS` | `0` | Set `1` when **lidb** harness lands |
| `POSTGRES_URL` / `LIDB_URL` | — | Both engines with identical policies |

## CI ingest

1. `run-db-security-bench.sh` → `write-tier-db-security-manifest.py`.
2. Artifact: `data/latest/tier-db-security.json`.

**Honesty:** `status: stub` until harness emits CSV — dashboard must not imply green security posture.

## Plan linkage

| ID | Deliverable |
|----|-------------|
| **WP-N4** | Full-spectrum lidb audit tiers |
| **PH-DB-SEC** | Security probe harness in **lidb** |
