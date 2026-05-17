# Study: Near-threshold tier-1/2 rows (SOTA survey cluster)

**Date:** 2026-05-17  
**Mode:** SOTA survey (Mode A)  
**Rows:** `ratio_vs_cpp` ∈ (1.0, 1.2] — green on dashboard but above cpp reference

| Benchmark | Tier | Ratio vs cpp | PH | Variant |
|-----------|------|--------------|-----|---------|
| matmul_blocked | 1 | 1.035 | PH-5b | shared C (`LI_EXTRA_C`) |
| nbody_gravity | 2 | 1.035 | PH-5b | shared C |
| double_pendulum | 2 | 1.032 | PH-5b | shared C |
| wave_equation_1d | 2 | 1.024 | PH-5b | shared C |
| harmonic_oscillator_chain | 2 | 1.018 | PH-5b | shared C |
| heat_equation_2d | 2 | 1.004 | PH-5b | shared C |
| reduce_sum | 1 | 1.003 | PH-5b | shared C |

**Note:** Li drivers for these rows are thin `extern` wrappers (e.g. `matmul_blocked/li/main.li` calls `li_matmul_blocked_kernel()`). Gaps are **FFI + link flags + call overhead**, not missing integrators in Li source.

---

## Learned from (by cluster)

### A — Blocked GEMM (`matmul_blocked`)

| Reference | Takeaway |
|-----------|----------|
| [Goto & van de Geijn, TOMS 2008](https://www.cs.utexas.edu/~flame/pubs/GotoTOMS.pdf) | Cache-blocked `ijk`/`ikj` with micro-panel size `BK=64` — already in `matmul_blocked_core.c` |
| [BLIS TOMS 2014](https://www.cs.utexas.edu/~flame/pubs/blis2_toms_rev3.pdf) | Pack + rank-k micro-kernel; Li does not reimplement — ensure **identical** `-O3 -march=native` link as cpp |
| [FLAME GEMM tutorial](https://github.com/flame/how-to-optimize-gemm) | 3–5% gaps often from **extra indirection** or missing LTO across `lic` driver boundary |

**Li path:** PH-5b harness parity — audit `LI_EXTRA_C` link line, LTO, `noinline` on kernel only.

### B — N-body (`nbody_gravity`)

| Reference | Takeaway |
|-----------|----------|
| [Phantom-GRAPE (2013)](https://ui.adsabs.harvard.edu/abs/2013NewA...19...74T/abstract) | SIMD force kernels; org oracle is already C — match compile flags |
| [SimdNBodyKernels](https://github.com/markstock/SimdNBodyKernels) | Reference for future **pure-Li** SIMD path (PH-7e), not current shared-kernel row |

### C — Hamiltonian / wave / heat / pendulum

| Reference | Takeaway |
|-----------|----------|
| [Hairer, Lubich, Wanner — geometric integration](https://archive-ouverte.unige.ch/unige:12277) | Symplectic / Verlet for long-time energy — oracle `*_core.c` already chosen |
| [LeVeque — FVM for hyperbolic PDEs](https://faculty.washington.edu/rjl/fdmbook/) | CFL-limited explicit schemes — wave_1d / heat_2d cores implement stable stencils |
| [Hairer course notes — Störmer–Verlet](https://unige.ch/~hairer/poly_geoint/week2.pdf) | `double_pendulum` — keep integrator in C oracle; Li wrapper overhead only |

**Li path:** PH-5b — no discretization change; optional `params.toml` audit only if tier-0 energy drift appears.

### D — Reduction (`reduce_sum`)

| Reference | Takeaway |
|-----------|----------|
| **Numerical Recipes** §parallel reduction / compensated summation | Oracle uses straightforward sum; 0.3% gap → link/LTO, not Kahan rewrite |
| **Eigen** `redux` / vectorized reduction patterns | Future PH-7e if pure-Li reduction bench is added |

---

## Map to Li tracks

| Track | Near-threshold work |
|-------|---------------------|
| **PH-5b** | Harness link parity, ingest, tier-0 stability for physics |
| **PH-7e** | Deferred until pure-Li variants replace `LI_EXTRA_C` |
| **G-math** | `matmul_blocked` / future `A @ B` lowering when pure-Li matmul lands |
| **G-par** | Optional OpenMP on shared cores — only with **G-par** proof, not string heuristics |

---

## Recommended actions (lic, low risk)

1. **Single audit PR** — normalize `lic build` release flags + LTO for all `LI_EXTRA_C` tier-1/2 drivers; re-run `bench.py --tier 12`.
2. **Per-bench only if still >1.05×** — inspect `extern` call ABI (zero-cost wrapper vs indirect).
3. **Do not** relax `threshold_ratio_cpp` (1.2) for cosmetic green.

**PR title (if one umbrella fix):** `perf(bench): PH-5b — align LI_EXTRA_C release/LTO with cpp oracle (near-threshold tier-1/2)`

---

## Quality table

| Axis | Current | Action |
|------|---------|--------|
| Stability | tier-0 green (physics) | keep locked |
| Speed | 1.003–1.035× cpp | aim ≤1.0× via link/harness |
| Accuracy | oracle cores | no change |
| Memory | — | — |

---

## Verdict

SOTA numerics already live in `common/*_core.c`. Near-threshold rows need **bench_improver / PH-5b harness**, not new algorithms. File one **lic** tracking issue; batch evidence after single harness PR.
