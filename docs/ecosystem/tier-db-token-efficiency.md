# tier_db_token_efficiency — agent query surface token audit

Benchmark tier comparing **LLM-authored** query representations for the Li registry (`001_registry.sql` / `registry-v1`) and control-plane (`agent_runs`, MCP introspection). This tier measures **tokens in context**, not database latency.

**Full audit (tables, appendices, grammar recommendations):** [`lidb/docs/liq-token-efficiency-audit.md`](https://github.com/li-langverse/lidb/blob/main/docs/liq-token-efficiency-audit.md)

## Executive summary

| Finding | Evidence |
|---------|----------|
| **liq reduces agent-authored tokens ~36% vs hand SQL** across 18 scenarios | `sql_tokens_total=629`, `liq_tokens_total=405`, encoder `tiktoken_cl100k_base` ([`data/latest/tier-db-token-efficiency.json`](../../data/latest/tier-db-token-efficiency.json)) |
| **Median per scenario:** liq **24** vs SQL **32** (−25%) | Same manifest `summary.median_tokens_by_surface` |
| **PostgREST URLs** are often smallest on wire (**median 23**) but lack compile-time safety and hide auth/RPC bodies | See `insert_publish`, `yank_package` rows |
| **Prisma/Drizzle** snippets run **+10% to +110%** vs SQL for the same intent | Representative `findMany` / `db.select` chains in corpus |
| **Compiled liq→SQL is not shorter** — catalog-qualified emission is **~2×** hand SQL today | Measured `agent_runs` example in lidb audit §2.4 |
| **Semantic gaps:** JOIN, `GROUP BY`, multi-statement publish counted honestly | `join_publisher_package`, `count_agent_runs_by_status` |

**Honesty:** Corpus strings are **representative** snippets (not copied from a single app repo). Counts are **measured** from frozen `scenarios.json` via `compute_tokens.py`. ORM/Supabase lines exclude import blocks; PostgREST excludes `Authorization` headers.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_token_efficiency/scenarios.json` | Frozen query corpus (18 scenarios × 7 surfaces) |
| `benchmarks/tier_db_token_efficiency/compute_tokens.py` | Token/char measurement |
| `scripts/run-db-token-efficiency-bench.sh` | CI entry (optional `.venv` + tiktoken) |
| `scripts/ingest/write-tier-db-token-efficiency-manifest.py` | Writes manifest |
| `data/latest/tier-db-token-efficiency.json` | Ingest artifact |
| `schema/tier-db-token-efficiency-ingest.json` | Manifest schema |

## Methodology (short)

1. **Baseline:** Postgres-shaped **raw SQL** with `$n` / named params (no string interpolation).
2. **liq:** Strings from [`lidb/docs/liq-spec.md`](https://github.com/li-langverse/lidb/blob/main/docs/liq-spec.md) and [`liq/README.md`](https://github.com/li-langverse/lidb/blob/main/liq/README.md); validated samples compiled with `lidb/liq/compiler.py` where applicable.
3. **Competitors:** One representative **Prisma**, **Drizzle**, **Supabase JS**, **PostgREST** path, and **Hasura-style GraphQL** per scenario.
4. **Tokenizer:** `tiktoken` `cl100k_base` when available; else `words × 1.3` (documented in manifest `encoder`).
5. **Metric:** `tokens` per surface; `delta_pct` vs SQL; `compression_ratio = sql_tokens / surface_tokens`.

## Master matrix (measured 2026-05-25)

| Scenario | SQL | liq | Δ% vs SQL | Prisma | Supabase JS | PostgREST | GraphQL |
|----------|-----|-----|-----------|--------|-------------|-----------|---------|
| `list_packages_limit_20` | 20 | 18 | -10.0% | 42 | 31 | 21 | 24 |
| `get_package_version_by_name_version` | 53 | 31 | -41.5% | 52 | 55 | 42 | 44 |
| `insert_publish_with_attestation` | 78 | 39 | -50.0% | 55 | 66 | 26 | 41 |
| `join_publisher_package` | 45 | 18 | -60.0% | 35 | 35 | 27 | 29 |
| `filter_tenant_publisher_rls` | 35 | 23 | -34.3% | 46 | 36 | 23 | 24 |
| `agent_runs_order_started_at` | 29 | 25 | -13.8% | 51 | 50 | 35 | 33 |
| `vector_search_stub` | 24 | 18 | -25.0% | 31 | 23 | 12 | 31 |
| `yank_package` | 52 | 24 | -53.8% | 34 | 22 | 15 | 39 |
| `schema_introspection_mcp` | 35 | 11 | -68.6% | 27 | 21 | 23 | 22 |
| `bulk_read_pagination_cursor` | 39 | 34 | -12.8% | 44 | 43 | 36 | 73 |
| `list_package_versions_for_package` | 28 | 27 | -3.6% | 29 | 42 | 33 | 39 |
| `update_publisher_display_name` | 21 | 18 | -14.3% | 30 | 31 | 14 | 37 |
| `blocklist_lookup_by_name` | 23 | 23 | +0.0% | 20 | 32 | 27 | 30 |
| `count_agent_runs_by_status` | 20 | 9 | -55.0% | 38 | 17 | 9 | 18 |
| `insert_agent_run_stub` | 41 | 29 | -29.3% | 41 | 31 | 8 | 23 |
| `read_attestations_for_version` | 26 | 25 | -3.8% | 25 | 35 | 32 | 38 |
| `delete_yanked_flag_update` | 28 | 27 | -3.6% | 24 | 38 | 21 | 33 |
| `describe_table_agent_runs_mcp` | 32 | 6 | -81.2% | 16 | 16 | 15 | 21 |

**Caveat:** `join_publisher_package` liq row is **single-table** (`read packages …`); full join semantics need `liq_2step` (~34 tokens) or future `read … with publishers` (see lidb audit).

## Safety surface (summary)

| Surface | Injection risk | Agent repeatability |
|---------|----------------|---------------------|
| **SQL** | High if LLM concatenates literals; mitigated by read-only validators / MCP allowlists | High expressivity; verbose |
| **liq** | Low for idents (catalog-bound); values via `$param` only | High for subset; fails closed on unknown tables |
| **Prisma/Drizzle** | Low when using typed clients; raw SQL escape hatches risky | Medium — boilerplate grows with projections |
| **Supabase JS** | Medium — string column lists; server enforces RLS | High for CRUD; weak for complex joins |
| **PostgREST** | Medium — URL encoding; filter injection if mis-encoded | High for simple filters; poor for multi-step publish |
| **GraphQL** | Medium — deep queries; schema-bound | Medium — verbose for mutations with variables |

## Run

```bash
cd benchmarks
./scripts/run-db-token-efficiency-bench.sh
# Manifest: data/latest/tier-db-token-efficiency.json
```

Env: `BENCH_DB_TOKEN_PROFILE=ci` (default).

## Plan linkage

| PH | Deliverable |
|----|-------------|
| **PH-DB-2** | liq grammar + compiler + security harness |
| **PH-DB-5** | RLS / tenant scenarios in corpus |
| **WP-N4** | Benchmark matrix CI ingest |

## Agent continuation

1. **Read:** this file; [`lidb/docs/liq-token-efficiency-audit.md`](https://github.com/li-langverse/lidb/blob/main/docs/liq-token-efficiency-audit.md); `benchmarks/tier_db_token_efficiency/scenarios.json`
2. **Run:** `./scripts/run-db-token-efficiency-bench.sh` — refresh `data/latest/tier-db-token-efficiency.json`
3. **Then:** After liq grammar changes, update scenario strings + re-run; consider dashboard row when `catalog.toml` entry lands
4. **Blocked on:** catalog/dashboard wiring — optional follow-up PR
