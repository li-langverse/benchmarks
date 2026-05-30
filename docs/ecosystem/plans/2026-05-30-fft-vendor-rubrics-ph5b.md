# FFT vendor rubrics — gearshifft + VkFFT crossover (PH-5b / G-math)

> **Issues:** [benchmarks#51](https://github.com/li-langverse/benchmarks/issues/51), [#52](https://github.com/li-langverse/benchmarks/issues/52)  
> **Parent plan:** [2026-05-18-tier1-fft-microbench.md](./2026-05-18-tier1-fft-microbench.md) · [#18](https://github.com/li-langverse/benchmarks/issues/18)  
> **Repo:** li-langverse/benchmarks (policy + catalog) + **lic** (harness oracles)  
> **Vision:** **Fast** (roofline honesty), **Provable** (deterministic size grid before pure-Li claims)  
> **Learned from:** [gearshifft](https://github.com/mpicbg-scicomp/gearshifft), [UTK FFT vendor study (ICL-UTK-1079-2018)](https://icl.utk.edu/files/publications/2018/icl-utk-1079-2018.pdf), [FFTW vs cuFFT crossover notes](https://gist.github.com/pentschev/9e7c50c1321d2b7c067d), [research-methodology.md](../../numerics/research-methodology.md)

## Goal

Document **vendor-agnostic FFT measurement policy** for the tier-1 `fft_1d_fixed` catalog row so Li benchmarks compare against CPU (FFTW), vendor GPU (cuFFT/rocFFT), and optional portable GPU (VkFFT) with explicit crossover sizes — without inventing harness in **benchmarks** or weakening `threshold_ratio_cpp`.

## Non-goals

- Implementing pure-Li FFT before baseline oracles exist (defer to **lic** numerics after rubric lands).
- Adding new org repos or copying **lic** harness into **benchmarks**.
- Weakening tier-1 advisory bar (≤1.2× C++) to green incomplete kernels.
- Cron-scheduled ingest or Actions `schedule:` changes.

## Dependencies

- **PH-5b** — tier-1 micro harness ownership in **lic**.
- **PH-7e** — optional `pure_li` variant only after measurement validity matches `horner_pure_li` lessons.
- **benchmarks#18** — catalog row + base harness plan (draft PR #136).
- **PH-IO-7** — ingest columns align when `std.summary` ships ([#53](https://github.com/li-langverse/benchmarks/issues/53), **lic#13**).

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | **Numerics study** `docs/numerics/studies/2026-05-30-fft-vendor-crossover.md` — size grid, oracle tiers, crossover N≈2¹⁶ heuristic | Study merged; cites gearshifft + UTK |
| B | Extend **#18** catalog metadata: oracle columns (`fftw`, `cufft`/`rocfft`, optional `vkfft`) documented in plan-cross-links | Dashboard ingest schema documented |
| C | **lic** harness PR: C++ reference + FFTW link; optional CMake flags for vendor libs (same pattern as MKL opt-in) | `bench.py --tier 1` includes `fft_1d_fixed` |
| D | gearshifft policy pointer in study — use as **external** multi-vendor sanity check, not vendored dep | No submodule in org repos without human checklist |
| E | Close explorer rubrics #51/#52; route pure-Li FFT to `numerics_researcher` only after A–C green | `ecosystem-explorer` no longer suggests FFT vendor gap |

## Oracle tiers (#51 gearshifft alignment)

| Tier | Oracle | Role | Notes |
|------|--------|------|-------|
| T0 | Hand-written C++ DFT reference | Correctness ceiling (small N) | tier-0 spot checks |
| T1 | **FFTW** | CPU baseline for `ratio_vs_cpp` | Required on Linux CI |
| T2 | **cuFFT** or **rocFFT** | Vendor GPU roofline | Optional CI; document skip reason |
| T3 | **VkFFT** | Portable GPU path (#52) | Optional; compare at documented crossover sizes |
| T4 | **gearshifft** | External multi-vendor sweep | Citation + manual repro, not CI hard-dep |

**Size grid (initial):** N ∈ {256, 1024, 4096, 16384, 65536, 262144} for 1D complex-to-complex; document when GPU oracle expected to win (community heuristic: ~N≥65536 for cuFFT vs FFTW on datacenter GPUs — validate per runner).

## Tests / benches

- **lic:** `benchmarks/tier1_micro/fft_1d_fixed/` + `bench.py --tier 1`.
- **benchmarks:** ingest after **lic** PR; `ecosystem-audit.py` tier-1 row not **unknown**.
- **li-tests:** none until pure-Li path exists.
- No CVE row (no new attack surface in rubric doc).

## Provability

- **G-math** — remains **Partial**; FFT bench supplies perf evidence only, not proof closure.
- **G-gpu** — stays **Missing** until `@gpu` proofs exist; optional GPU oracle columns are measurement-only.
- Do not mark any **G-*** row **Done** from rubric documentation alone.

## Rollout

1. Merge this plan PR (benchmarks) → maintainer adds **`plan-approved`** on #51, #52.
2. Merge numerics study (sub A) on **benchmarks**.
3. **lic** harness PR (sub C) — separate repo, blocked on #18 catalog row.
4. Remove `plan-needed` on #51/#52 when study + parent #18 plan approved.

## Human-only

- Approve optional vendor library installs on CI runners (FFTW apt; CUDA/ROCm for GPU oracles).
- Confirm gearshifft is reference-only (no license/submodule without [governance](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/governance.md) checklist).

## Deferred to numerics_researcher

- Pure-Li FFT kernel and PH-7e SIMD lowering.
- Autoresearch on Li-specific FFT fusion — requires algorithm note per [research-methodology.md](../../numerics/research-methodology.md).
