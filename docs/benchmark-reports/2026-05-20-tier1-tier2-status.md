# Local benchmark snapshot — 2026-05-20

**Machine:** Cursor workspace (`/workspace`) · **lic:** nested checkout, git `c3cad91`  
**Harness:** `python3 benchmarks/harness/bench.py --tier 1 --runs 1 --ci --out benchmarks/results/latest.csv` (run **inside `lic/`**).  
**Ingest:** `python3 scripts/ingest/build_summary.py /workspace/lic /workspace/lis` from **benchmarks** repo root.

## Tier 1 — Li vs C++ (`wall_time`, threshold 1.2×)

| Benchmark | Li (s) | C++ (s) | Ratio Li/cpp | Status |
|-----------|--------|---------|--------------|--------|
| `simd_dot` | 0.0009 | 0.0619 | **0.0145** | green |
| `horner_pure_li` | 0.0004 | 0.0010 | **0.40** | green |
| `matmul_blocked` | 0.0104 | 0.0104 | **1.00** | green |
| `matmul_naive` | 0.0026 | 0.0024 | **1.08** | green |
| `reduce_sum` | 0.3083 | 0.3087 | **0.999** | green |

**Tier counts (ingest):** tier **1** → **5 green**, **0 red** (this CSV only).

### Honesty / variance

- Single **median-of-1** CI-style run — good for smoke, not a release certificate ([benchmark-dashboard.md](../honesty/benchmark-dashboard.md)).
- Historical dashboard rows for **`horner_pure_li`** have been **red** at ~80–90× vs cpp on other commits/machines; this snapshot is **faster Li than cpp** here — treat as **environment + harness variance** until reproduced across runs ([SOTA matrix](../numerics/sota-comparison-matrix.md)).

## Tier 2 — not completed in this workspace

1. First failure: missing **`omp.h`** — resolved by installing **`libomp-dev`** on the runner image.
2. Second failure: **`rigid_body_stack`** Li build — compiler errors **`E0301`** (`extern proc` requires `requires` / `ensures`, and `raises IO`). Earlier smokes (e.g. `md_lennard_jones`, `sph_dam_break_2d`) passed verification; tier-2 CSV was **not** written for the full suite.

**Follow-up (lic):** fix `benchmarks/tier2_physics/rigid_body_stack/li/main.li` extern contracts, then re-run `bench.py --tier 2 --ci`.

## Other catalog rows

- **Tier 0** `tier0_stability`: **unknown** (no `stability.csv` in this run).
- **Tier 2** physics rows: **unknown** (no tier-2 timings in `latest.csv`).
- **HTTP / tooling:** unchanged **unknown** pending `lis` CSV and lip/lit harnesses.

## Artifacts

- CSV: `lic/benchmarks/results/latest.csv` (tier 1 only).
- Summary: `data/latest/summary.json` (regenerated from that CSV).
