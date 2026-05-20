# Agent pass: numerics research cycle (2026-05-20)

**Skill:** `research-li-numerics`  
**Mode:** Mode A — SOTA survey (no novel algorithms)  
**Dashboard:** https://li-langverse.github.io/benchmarks/  
**Bench ids:** `horner_pure_li` (red); `matmul_blocked`, `nbody_gravity`, `double_pendulum`, `wave_equation_1d`, `harmonic_oscillator_chain`, `heat_equation_2d`, `reduce_sum` (green, >1.0× cpp)  
**Evidence gate:** this file under `docs/numerics/` + repro commands below

---

## 1. Problem summary

Tier-1/2 competitive posture (**PH-5b**) vs shared C++ oracles requires pure-Li and harness paths to measure **real** hot work. The dashboard still shows one **red** micro row and seven **green** rows slightly above 1.0× cpp (all under the 1.2× catalog cap).

**Failure modes:**

| Cluster | Symptom | Root cause class |
|---------|---------|------------------|
| `horner_pure_li` | ~88.8× vs cpp | **Invalid measurement first:** `li/main.li` returns `0` without observable `acc`; LLVM `-O3` can DCE the recurrence (see [autoresearch negative](./2026-05-17-horner-pure-li-autoresearch-negative.md)). After parity, gap is **PH-7e** FMA / loop-vectorize vs `horner_core.c`. |
| Near-limit greens | 1.003–1.035× cpp | Harness / link / wrapper overhead on shared-C or thin `extern` drivers — not wrong discretizations ([near-limit SOTA](./2026-05-17-near-limit-tier12-sota.md)). |

---

## 2. SOTA survey — Learned from (2–4)

| # | Reference | What we take |
|---|-----------|--------------|
| 1 | [Numerical Recipes §5.3 — Polynomials and rational functions](https://numerical.recipes/book/bookcpdf/c5-3.pdf) | Horner multiply-add recurrence — canonical recipe for **`horner_pure_li`**; no algorithm change needed. |
| 2 | [Eigen — efficient matrix product](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html) + [BLIS — kernels how-to](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md) | Cache-blocked GEMM + register micro-kernels — maps **`matmul_blocked`**, future pure-Li `@` lowering (**G-math**, **PH-7e**). |
| 3 | Hairer–Lubich–Wanner, *Geometric Numerical Integration* ([Springer SSCM](https://link.springer.com/book/10.1007/3-540-30666-8)) | Symplectic / leapfrog lineage for **`nbody_gravity`**, **`double_pendulum`**, **`harmonic_oscillator_chain`** — preserve invariants when tuning integrator cost. |
| 4 | [LLVM loop vectorizer](https://llvm.org/docs/Vectorizers.html) + [VPlan reduction resume phis (LLVM #110004)](https://github.com/llvm/llvm-project/pull/110004) | Reduction / recurrence vectorization targets for **PH-7e** after observable accumulators; informs lic metadata on counted `while` loops. |

**Stability:** Tier-0 row `tier0_stability` remains **unknown** on dashboard — deferred to harness ingest; do not trade stability for speed on physics rows.

---

## 3. Map to Li pillars

| ID | Role |
|----|------|
| **PH-5b** | Tier-1/2 vs cpp oracle; headline red = **`horner_pure_li`**. |
| **PH-7e** | Math → SIMD / FMA / LLVM loop metadata; blocks **`horner_pure_li`**, **`reduce_sum`**, eventual pure-Li GEMM. |
| **G-math** | FMA fusion, reduction vectorization, blocked GEMM contracts in `lic` + `li-std-math`. |
| **G-par** | Outer `@parallel` / Kokkos-class policies — **after** G-math wins on near-limit rows; PETSc-class stack for future implicit PDE tiers. |

---

## 4. Implementation path (lic — contracts + bench evidence)

**P0 — measurement validity (bench_improver + lic, before codegen claims)**

1. **`horner_pure_li/li/main.li`:** Export checksum parity with `common/horner_core.c` (`g_li_horner_checksum` / `li_horner_checksum()` pattern) — e.g. `return` low bits of `acc` or `li_rt_sink_double(acc)` outside the hot loop only if semantics allow.
2. Re-run harness; confirm disassembly contains `fmul`/`fmuladd` in `_li_user_main` at `-O3`.

**P1 — PH-7e codegen (lic compiler)**

3. Fuse `acc * x + 1.0` → `llvm.fmuladd` under release + fast-math policy.
4. Lower counted `while` to LLVM-friendly induction + `loop-vectorize` metadata (match `horner_core.c` IR shape).

**P2 — near-limit cluster (harness fairness)**

5. Align `bench.py` / `LI_EXTRA_C` / `-march=native` with cpp column ([near-limit study §4](./2026-05-17-near-limit-tier12-sota.md)).
6. Shared reduction vectorization for **`reduce_sum`** alongside simd-dot / Horner track.

**Do not:** relax `threshold_ratio_cpp`; ship `sorry`/`unsafe` for speed; open novel-method PRs here → **`numerics-autoresearch`**.

**2026-05-20 lic tree check:** `LIC_ROOT/benchmarks/tier1_micro/horner_pure_li` exists; `li/main.li` still ends with `return 0` and no `acc` sink — P0 not yet landed on agent workspace branch.

---

## 5. Quality table (locked axes)

| Axis | `horner_pure_li` | Near-limit greens |
|------|------------------|-------------------|
| **Stability** | N/A (scalar FP micro) | Preserve integrator / CFL contracts per numerical policy |
| **Accuracy** | Bitwise vs C oracle after checksum parity | Oracle = shared `*_core.c` |
| **Speed** | Target ≤1.2× cpp after valid measurement + PH-7e | Target ≤1.0× cpp (optional), never above 1.2× cap |
| **Visual** | N/A tier-1 | Tier-2 GIF sanity unchanged when touching physics harness |

---

## 6. Repro — bench & dashboard

```bash
cd benchmarks
./scripts/benchmark-failures-report.sh
```

**Expected (ingest snapshot 2026-05-16):** 1 RED (`horner_pure_li` ~88.821×); 7 green rows >1.0× cpp listed in §1.

```bash
export LIC_ROOT=/path/to/lic
cd "$LIC_ROOT/benchmarks/harness"
python3 bench.py horner_pure_li --release
python3 bench.py matmul_blocked nbody_gravity reduce_sum --release

cd /path/to/benchmarks
LIC_ROOT="$LIC_ROOT" ./scripts/ingest/ingest-lic.sh
```

**Evidence checklist:**

```bash
cd benchmarks
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-20-numerics-research-agent-pass.md
```

**Linked drill-downs:** [horner codegen](./2026-05-17-horner-pure-li-codegen.md), [near-limit SOTA](./2026-05-17-near-limit-tier12-sota.md), [2026-05-17 agent pass](./2026-05-17-numerics-research-agent-pass.md).

**Plots / visuals:** Dashboard micro chart `horner_pure_li` — https://li-langverse.github.io/benchmarks/ ; optional PNG under `data/visuals/latest/` after `render-benchmark-visuals.sh`.

---

## 7. Recommended issues / PRs

| Priority | Repo | Title | Labels |
|----------|------|-------|--------|
| P0 | **lic** | `fix(bench): horner_pure_li pure_li checksum sink — valid PH-7e measurement` | `numerics-research`, PH-7e |
| P0 | **lic** | `perf(codegen): PH-7e FMA + loop metadata for pure-Li Horner (horner_pure_li)` | after P0 bench fix |
| P1 | **lic** | `perf(math): near-limit tier-1/2 harness parity (matmul_blocked, reduce_sum, nbody_gravity)` | `numerics-research` |
| P1 | **benchmarks** | Comment / link evidence on #31 — no threshold edits | `numerics-research` |
| P2 | **benchmarks** | `feat(catalog): tier-1 FFT micro-bench (FFTW roofline)` — [issue #18](https://github.com/li-langverse/benchmarks/issues/18) | `plan-needed` |

Coordinate implementation PRs with **bench_improver**; human review required before merge.

---

## 8. Deferred

- **`tier0_stability`**, **`lip_smoke`**, **`lit_smoke`**, **`keepalive_pipelining`**, **`static_small`** — unknown until ingest/harness wired.
- Novel integrators / implicit AMG / FFT implementation — **autoresearch** or separate feature issues.
- Catalog `LIC_ROOT` audit gaps in CI sandboxes without sibling **lic** checkout — [benchmarks#28](https://github.com/li-langverse/benchmarks/issues/28).
