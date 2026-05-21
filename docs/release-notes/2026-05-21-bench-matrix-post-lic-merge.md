# Benchmark matrix refresh after lic #153/#156 merge

## Summary

Refreshed tier-5 HTTP CSV and `data/latest/benchmark-matrix.*` after merging lic proxy epoll fix and E0360 ptr ABI guard; `proxy_loopback,li` shows verified RPS (~9.1k req/s quick profile).

## Agent continuation

1. **Read** `vendor/lis-tier5/results/latest.csv`, `data/latest/benchmark-matrix.md`.
2. **Run** full `./scripts/run-full-benchmark-suite.sh` (or `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`) after pinning `LI_HTTPD_BIN` to lic `main` ≥ `21e17a6`.
3. **Then** merge benchmarks PR #65; ingest if publishing dashboard rows.
4. **Blocked on** human merge-approved on benchmarks PR; full multi-oracle nightly for complete grid.

## Changed

| Area | Evidence |
|------|----------|
| CSV | `vendor/lis-tier5/results/latest.csv` — `proxy_loopback,li,release,8,rps,9120.95,req/s` |
| Matrix | `data/latest/benchmark-matrix.json`, `.md`, `docs/ecosystem/http-server-rps-matrix.md` |
| lic | `li-langverse/lic` `main` @ `21e17a6` (PR #153 + #156) |

## Not changed

- `catalog.toml` scenario definitions.
- Tier-5 exploit matrix (separate script).
- lic compiler source (merged upstream).

## Breaking

N/A

## Security

N/A

## Performance

Quick wrk proxy_loopback: **li ~0.17× nginx** on same 5s profile (nginx backend in harness).

## Downstream

- Dashboard ingest: `./scripts/ingest/ingest-lic.sh` when publishing Pages.
