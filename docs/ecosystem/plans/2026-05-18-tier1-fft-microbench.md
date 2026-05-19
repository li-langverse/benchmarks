# Tier-1 FFT micro-bench catalog row (PH-5b / PH-7e)

> **Issue:** [benchmarks#18](https://github.com/li-langverse/benchmarks/issues/18)  
> **Repo:** li-langverse/benchmarks (catalog) + **lic** (harness implementation)  
> **Vision:** **Fast** (roofline evidence), **Provable** (deterministic size params)  
> **Learned from:** [ecosystem-explorer.md](../ecosystem-explorer.md), [explorer digest 2026-05-17](../explorer-digests/2026-05-17-explorer.md), [FFTW bench community repos](https://github.com/project-gemmi/benchmarking-fft), [master plan PH-5b](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)

## Goal

Add a **tier-1** catalog row and **lic** harness kernel comparing Li vs C++ vs FFTW (or vendor MKL when available) for a fixed 1D/2D FFT size grid—closing the explorer rubric gap (**FFTW: missing**) without duplicating harness in **benchmarks**.

## Non-goals

- Full `std/signal` or vendor FFI in Li (defer to lic package plan).
- Weakening thresholds to pass before Li FFT path exists.
- Cron-scheduled ingest.

## Dependencies

- **PH-5b** — tier-1 micro harness patterns (`benchmarks/tier1_micro/*`).
- **PH-7e** — optional `pure_li` variant row once codegen path exists.
- **lic** issue for kernel implementation (file after catalog row merged).

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | `catalog.toml` row `fft_1d_fixed` (tier 1, `repo = "lic"`, path under `benchmarks/tier1_micro/`) | Row merged in **benchmarks** |
| B | **lic** harness: `benchmarks/tier1_micro/fft_1d_fixed/` + C++ oracle + FFTW link (CMake opt-in) | `bench.py --tier 1` includes id |
| C | Ingest + dashboard: ratio vs C++ baseline; document MKL optional column in numerics study | `data/latest/summary.json` has row |
| D | Update **tooling-catalog.md** + **roadmap** agent-kit explorer rubric: FFTW → **partial** | Ecosystem-gap label removable |

## Tests / benches

- **lic:** `benchmarks/harness/bench.py --tier 1` includes `fft_1d_fixed`.
- **benchmarks:** ingest smoke after **lic** PR lands; `ecosystem-audit.py` no longer suggests FFT gap.
- Sizes: e.g. N ∈ {256, 1024, 4096} — fixed for reproducibility.

## Provability

- **G-math** — stays **Partial** until Li-native FFT has proof story; bench is perf evidence only.
- No **trusted.lean** changes in this plan.

## Rollout

1. **benchmarks** PR: catalog + this plan (draft).
2. **lic** PR: harness + oracle (blocked on `plan-approved` for #18).
3. Numerics study optional: `docs/numerics/studies/2026-05-18-fft-tier1.md`.

## Human-only

- FFTW/MKL install on CI runners (apt packages or cached libs) — confirm org Actions budget.
