# tier_db_vector_ann — registry / agent ANN recall and QPS

Benchmark tier for **vector ANN** on registry- and agent-scale corpora: **lidb** CPU HNSW vs **Faiss** CPU vs optional **lidb-gpu** at fixed recall@k.

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_vector_ann/` | Suite config, scenarios, corpus schema |
| `scripts/run-db-vector-ann-bench.sh` | Entry stub (writes CI manifest) |
| `data/latest/tier-db-vector-ann.json` | CI ingest artifact |
| `schema/tier-db-vector-ann-ingest.json` | Manifest JSON Schema |
| [`catalog.toml`](../../catalog.toml) | Dashboard rows (`category = database`, `tier = 6`) |

## Scenarios

| `id` | Corpus N | Metric |
|------|----------|--------|
| `ann_recall_at_10_10k` | 10⁴ | recall@10 (fixed k) |
| `ann_qps_10k` | 10⁴ | queries/sec @ recall@10 ≥ target |
| `ann_recall_at_10_1m` | 10⁶ | recall@10 (nightly only) |

Default embedding dim **128** (agent/registry search hypothesis in PH-DB-8 research).

Schema: `benchmarks/tier_db_vector_ann/schema/vector-ann-v1.sql`.

## Run

```bash
cd benchmarks
./scripts/run-db-vector-ann-bench.sh
# BENCH_DB_VECTOR_PROFILE=nightly BENCH_DB_VECTOR_RUN_HARNESS=1 ./scripts/run-db-vector-ann-bench.sh
```

Env:

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_VECTOR_PROFILE` | `ci` | `ci` = config-only; `nightly` = timed recall/QPS |
| `BENCH_DB_VECTOR_DIM` | `128` | Embedding dimension |
| `BENCH_DB_VECTOR_RECALL_TARGET` | `0.95` | Minimum recall@10 vs Faiss CPU oracle |
| `FAISS_INDEX` | — | Faiss CPU baseline index path |
| `LIDB_URL` | — | lidb with PH-DB-8 vector index |
| `LIDB_GPU_URL` | — | Optional lidb-gpu sidecar (not registry-min) |

## CI ingest

1. `run-db-vector-ann-bench.sh` → `scripts/ingest/write-tier-db-vector-ann-manifest.py`.
2. Artifact: `data/latest/tier-db-vector-ann.json`.

**Honesty:** No ANN perf claim in roadmap ADRs until CSV ingested.

## Plan linkage

| PH | Deliverable |
|----|-------------|
| **PH-DB-8** | Vector index in lidb |
| **PH-DB-G2** | GPU ANN optional module |

## Full suite

Not in `run-full-benchmark-suite.sh` until harness ships.
