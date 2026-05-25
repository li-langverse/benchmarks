# tier_db_vector_ann — ANN recall@k and QPS

Compare **lidb** CPU HNSW vs **Faiss** CPU vs optional **lidb-gpu** on synthetic embedding corpora (N = 10⁴, 10⁶).

## Scenarios

| Scenario | Corpus | Metric |
|----------|--------|--------|
| `ann_recall_at_10_10k` | 10⁴ | recall@10 |
| `ann_qps_10k` | 10⁴ | queries/sec |
| `ann_recall_at_10_1m` | 10⁶ | recall@10 (nightly) |

## Run (stub)

```bash
./scripts/run-db-vector-ann-bench.sh
```

**PH-DB-8**, **PH-DB-G2** — [tier-db-vector-ann.md](../../docs/ecosystem/tier-db-vector-ann.md).
