# tier_db_gpu_speedup — GPU ANN speedup vs CPU at fixed accuracy

Benchmark tier measuring **speedup ratio** (GPU / CPU) for vector ANN at **fixed recall@k**, across **cuda** and **metal** profiles. Complements [`tier-db-vector-ann.md`](./tier-db-vector-ann.md) (accuracy/QPS parity).

## Layout

| Path | Role |
|------|------|
| `benchmarks/tier_db_gpu_speedup/` | Suite config, scenarios (reuses vector corpus schema) |
| `scripts/run-db-gpu-speedup-bench.sh` | Entry stub (writes CI manifest) |
| `data/latest/tier-db-gpu-speedup.json` | CI ingest artifact |
| `schema/tier-db-gpu-speedup-ingest.json` | Manifest JSON Schema |
| [`catalog.toml`](../../catalog.toml) | Dashboard rows (`category = database`, `tier = 6`) |

## Scenarios

| `id` | Corpus N | Metric |
|------|----------|--------|
| `gpu_ann_speedup_10k` | 10⁴ | speedup_ratio vs lidb CPU HNSW @ recall@10 |
| `gpu_ann_speedup_1m` | 10⁶ | speedup_ratio (nightly) |

**Gate:** registry-min profile must stay CPU-only; this tier runs only when `LI_GPU=auto|cuda|metal` and hardware is present — CI **ci** profile writes stub manifest without requiring GPU.

## Run

```bash
cd benchmarks
./scripts/run-db-gpu-speedup-bench.sh
# BENCH_DB_GPU_PROFILE=nightly LI_GPU=cuda ./scripts/run-db-gpu-speedup-bench.sh
```

Env:

| Variable | Default | Notes |
|----------|---------|-------|
| `BENCH_DB_GPU_PROFILE` | `ci` | Stub manifest on PR; `nightly` = timed speedup |
| `BENCH_DB_GPU_MIN_SPEEDUP` | `1.5` | Target ratio for promotion (research, not gate yet) |
| `LI_GPU` | `off` | Must not be required in registry-min CI |
| `LIDB_GPU_URL` | — | lidb-gpu sidecar endpoint |

## CI ingest

1. `run-db-gpu-speedup-bench.sh` → `scripts/ingest/write-tier-db-gpu-speedup-manifest.py`.
2. Artifact: `data/latest/tier-db-gpu-speedup.json`.

**Honesty:** Stub on GHA (no GPU assumption); speedup claims require nightly artifact + CSV.

## Plan linkage

| PH | Deliverable |
|----|-------------|
| **PH-DB-G2** | GPU module evidence |
| **PH-DB-G0** | ADR D4/D5/D6 decision table |

Parent research: [lidb-multi-model-gpu-research.md](https://github.com/li-langverse/roadmap/blob/main/proposals/lidb-multi-model-gpu-research.md).

## Full suite

Not in `run-full-benchmark-suite.sh` until harness ships.
