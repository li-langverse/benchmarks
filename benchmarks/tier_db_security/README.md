# tier_db_security — Security

Full-spectrum **lidb** audit benchmark tier (WP-N4 stub). Harness compares **lidb** vs **PostgreSQL 15+** where applicable.

## Scenarios

| Scenario | Measures | Primary metric |
|----------|----------|----------------|
| `injection_blocked` | SQL injection attempts must fail closed | `pass_rate` (ratio) |
| `rls_bypass_blocked` | RLS bypass / privilege escalation attempts blocked | `pass_rate` (ratio) |

## Run (stub)

```bash
cd benchmarks
./scripts/run-db-security-bench.sh
cat data/latest/tier-db-security.json
```

Env: `BENCH_DB_SECURITY_PROFILE=ci|nightly`, `POSTGRES_URL`, `LIDB_URL`.

## CI ingest

Manifest: `data/latest/tier-db-security.json` — see [`schema/tier-db-security-ingest.json`](../../schema/tier-db-security-ingest.json).

Doc: [tier-db-security.md](../../docs/ecosystem/tier-db-security.md).
