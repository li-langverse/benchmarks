# Tier-1 FFT micro-bench catalog + lic harness (PH-5b / REQ-BENCH-FFT-1)

> **Issue:** [#18](https://github.com/li-langverse/benchmarks/issues/18) · **Repo:** li-langverse/benchmarks (+ **lic** harness)  
> **Vision:** **fast**, **provable** (numerics honesty) · **Learned from:** [master plan PH-5b](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md), [2026-05-30-fft-vendor-rubrics-ph5b.md](./2026-05-30-fft-vendor-rubrics-ph5b.md), [numerics research methodology](../../numerics/research-methodology.md), [explorer digest 2026-05-30](../explorer-digests/2026-05-30-gaps.md)

## Goal

Ship a tier-1 FFT wall-time benchmark with **FFTW (or vendor) reference oracle** and **pure_li** variant, ingested into the benchmarks dashboard with `ratio_vs_cpp` ≤ 1.2× gate. Catalog row exists; **harness implementation stays in lic** per org rule.

## Non-goals

- Weakening `threshold_ratio_cpp` to greenwash FFT.
- Implementing VkFFT/cuFFT crossover in **benchmarks** repo ([#51](https://github.com/li-langverse/benchmarks/issues/51), [#52](https://github.com/li-langverse/benchmarks/issues/52) — covered by vendor rubric plan).
- GPU tier in v1 (CPU FFTW reference + pure_li only).

## Dependencies

| ID | Owner | Notes |
|----|-------|-------|
| **PH-5b** | lic | Tier-1 numerics micro-benches |
| **PH-7e** | lic | SIMD/parallel lowering for pure_li FFT loop |
| **G-math** | lic | Float/array contracts before perf claims |
| `fft_1d_fixed` catalog | benchmarks | `catalog_lifecycle = planned` until harness measured |

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | **lic:** `benchmarks/tier1_micro/fft_1d_fixed/` — C++ FFTW reference + `pure_li` kernel, `bench.py` registration | `./bench.py --tier 1 --filter fft_1d_fixed` exits 0 on Linux CI |
| B | **benchmarks:** set `catalog_lifecycle` → `active`; verify `path` resolves under `LIC_ROOT` | `plan-completion-audit` catalog_gaps = 0 for row |
| C | Ingest: CSV → `summary.json` row with `validity_status=measured` | `check-summary-measurement-coverage.py` passes |
| D | Dashboard: tier-1 numerics card shows FFT row; near-threshold watch only | No threshold edits |
| E | `competitive/verticals.toml` FFT honesty line (if applicable) | Documented vs FFTW roofline |

## Tests / benches

| Asset | Location |
|-------|----------|
| Bench id | `fft_1d_fixed` |
| Catalog | `benchmarks/catalog.toml` |
| Harness | `lic/benchmarks/tier1_micro/fft_1d_fixed` (**not** copied to benchmarks) |
| Tier | 1 · `threshold_ratio_cpp = 1.2` |
| li-tests | Follow existing tier-1 micro pattern in lic |

## Provability

- **G-math:** Partial until FFT contracts (length, alignment) are stated in Li source; do not claim “proved FFT” without register update.
- Explorer rubrics #51, #52: track in [2026-05-30-fft-vendor-rubrics-ph5b.md](./2026-05-30-fft-vendor-rubrics-ph5b.md) — not blocking v1 CPU FFTW row.

## Rollout

1. **lic** PR: harness + tier-1 bench (implementation agent after `plan-approved`).
2. **benchmarks** PR: flip `catalog_lifecycle`, refresh ingest/summary on nightly or manual full suite.
3. Close #18; link #51/#52 as follow-up research.

## Human-only

- FFTW dev package on CI runners (document in lic bench README if new system dep).
- Maintainer **`plan-approved`** before harness PR.
