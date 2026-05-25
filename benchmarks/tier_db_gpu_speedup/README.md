# tier_db_gpu_speedup — GPU vs CPU ANN speedup

Measures **speedup_ratio** = GPU QPS / CPU QPS at fixed recall@10. Uses same corpus schema as [`tier_db_vector_ann`](../tier_db_vector_ann/).

## Scenarios

| Scenario | Corpus | Metric |
|----------|--------|--------|
| `gpu_ann_speedup_10k` | 10⁴ | speedup_ratio |
| `gpu_ann_speedup_1m` | 10⁶ | speedup_ratio (nightly) |

## Run (stub)

```bash
./scripts/run-db-gpu-speedup-bench.sh
```

**PH-DB-G2** — [tier-db-gpu-speedup.md](../../docs/ecosystem/tier-db-gpu-speedup.md).
