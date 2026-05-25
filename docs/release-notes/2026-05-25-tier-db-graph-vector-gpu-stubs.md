# Tier-6 lidb graph / vector / GPU benchmark stubs (PH-DB-G0)

## Summary

Adds **tier_db_graph_registry**, **tier_db_vector_ann**, and **tier_db_gpu_speedup** skeletons with docs, catalog rows, CI manifest writers, and GHA stub manifest step — per [lidb multi-model GPU research](https://github.com/li-langverse/roadmap/blob/main/proposals/lidb-multi-model-gpu-research.md) §G.

## Agent continuation

1. **Read:** `docs/ecosystem/tier-db-graph-registry.md`, `tier-db-vector-ann.md`, `tier-db-gpu-speedup.md`; parent branch docs for `tier_db_registry`.
2. **Run:** `chmod +x scripts/run-db-*-bench.sh && ./scripts/run-db-graph-registry-bench.sh && ./scripts/run-db-vector-ann-bench.sh && ./scripts/run-db-gpu-speedup-bench.sh` — expect stub JSON under `data/latest/tier-db-*.json`.
3. **Then:** Implement harnesses in **lidb**; merge CSV into ingest when `BENCH_DB_*_RUN_HARNESS=1` is stable; stack on `feat/tier-db-registry` or rebase this branch.
4. **Blocked on:** `lidb` repo + PH-DB-G0 human ADR sign-off; GPU nightly needs hardware (not GHA-required).

## Changed

| Area | Paths |
|------|-------|
| Docs | `docs/ecosystem/tier-db-graph-registry.md`, `tier-db-vector-ann.md`, `tier-db-gpu-speedup.md` |
| Suites | `benchmarks/tier_db_graph_registry/`, `tier_db_vector_ann/`, `tier_db_gpu_speedup/` |
| Run stubs | `scripts/run-db-graph-registry-bench.sh`, `run-db-vector-ann-bench.sh`, `run-db-gpu-speedup-bench.sh` |
| Manifest writers | `scripts/ingest/write-tier-db-{graph-registry,vector-ann,gpu-speedup}-manifest.py` |
| Schemas | `schema/tier-db-{graph-registry,vector-ann,gpu-speedup}-ingest.json` |
| Catalog | `catalog.toml` — 7 new tier-6 rows (PH-DB-G1, PH-DB-8, PH-DB-G2) |
| CI | `.github/workflows/ci.yml` — tier-6 manifest stub step |
| Packages | `ecosystem-packages.toml` — future CSV paths for lidb |
| Cross-links | `docs/ecosystem/plan-cross-links.md` |

## Not changed

- **lidb** engine, **lis** profiles, **lip** registry API — benchmarks-only stubs.
- **`tier_db_registry` harness** — unchanged on parent `feat/tier-db-registry`; this branch extends G0 gaps only.
- **`summary.json` merge** — manifests not merged into dashboard rows until CSV exists.
- **roadmap** ADR text — link from benchmarks; governance PR separate.

## Breaking

N/A — additive catalog rows; stub manifests only.

## Security

N/A — no runtime DB or GPU in CI; `LI_GPU=off` by default.

## Performance

N/A — no measured rows; honesty rule matches `tier-db-registry-benchmark.md`.

## Downstream

- **roadmap** `lidb-multi-model-gpu-research.md` — cite these paths in PH-DB-G0 PR.
- **li-cursor-agents** — control-plane migration unchanged.
