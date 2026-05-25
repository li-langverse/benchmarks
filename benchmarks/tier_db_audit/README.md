# tier_db_audit — Audit

Full-spectrum **lidb** audit benchmark tier (WP-N4 stub). Harness compares **lidb** vs **PostgreSQL 15+** where applicable.

## Scenarios

| Scenario | Measures | Primary metric |
|----------|----------|----------------|
| `query_log_complete` | Every privileged query appears in audit log | `completeness_ratio` (ratio) |
| `tamper_evidence` | Log chain / digest detects tamper | `pass_rate` (ratio) |

## Run (stub)

```bash
cd benchmarks
./scripts/run-db-audit-bench.sh
cat data/latest/tier-db-audit.json
```

Env: `BENCH_DB_AUDIT_PROFILE=ci|nightly`, `POSTGRES_URL`, `LIDB_URL`.

## CI ingest

Manifest: `data/latest/tier-db-audit.json` — see [`schema/tier-db-audit-ingest.json`](../../schema/tier-db-audit-ingest.json).

Doc: [tier-db-audit.md](../../docs/ecosystem/tier-db-audit.md).
