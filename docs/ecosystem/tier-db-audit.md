# tier_db_audit — query log and tamper evidence

Benchmark tier for **lidb** audit trail quality: privileged queries appear in the audit log; tamper-evident chain detects modification.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_audit/` | Suite config, scenarios |
| `scripts/run-db-audit-bench.sh` | Entry stub |
| `data/latest/tier-db-audit.json` | CI ingest artifact |

## Scenarios

| `id` | Measures | Metric |
|------|----------|--------|
| `query_log_complete` | Every privileged query logged | `completeness_ratio` |
| `tamper_evidence` | Digest/chain detects log tamper | `pass_rate` |

Schema stub: `benchmarks/tier_db_audit/schema/audit-log-v1.sql`.

## Run

```bash
./scripts/run-db-audit-bench.sh
```

Env: `BENCH_DB_AUDIT_PROFILE`, `BENCH_DB_AUDIT_RUN_HARNESS`.

## Plan linkage

**WP-N4** · **PH-DB-AUD**
