# HPC reference library release cadence policy

## Summary

Adds bench policy for **Eigen / Kokkos / PETSc / Chapel** version pins, quarterly bump triggers, and **AI tooling parity** (Chapel CLS / `chplcheck` vs Vision-LLM / `lic diagnose`) — closes [benchmarks#27](https://github.com/li-langverse/benchmarks/issues/27).

## Changed

| Area | Path |
|------|------|
| Policy | `docs/ecosystem/hpc-reference-library-cadence.md` |
| Cross-links | `docs/handbook/README.md`, `docs/honesty/benchmark-dashboard.md`, `docs/ecosystem/plan-cross-links.md`, `docs/ecosystem/ecosystem-explorer.md` |
| Registry | `benchmarks/workloads/competitive/registry.toml` (`last_reviewed`, cadence notes) |

## PH / vision

**PH-5b**, **PH-7e**, **G-math**, **G-par** — keeps SOTA citations and `≤1.2× cpp` claims honest; no harness or threshold changes.

## Breaking

N/A — documentation only.
