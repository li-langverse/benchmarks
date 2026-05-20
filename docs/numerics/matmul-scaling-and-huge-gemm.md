# GEMM scaling: small / medium / huge matrices (SOTA survey)

**Audience:** **lic** harness authors, **benchmarks** catalog maintainers, `bench_improver`, PH-5b / PH-7e.  
**Companion:** [SOTA comparison matrix](./sota-comparison-matrix.md) · [research-methodology](./research-methodology.md).

---

## 1. Regimes

| Regime | Typical N (double GEMM) | Dominant cost | Li harness today |
|--------|-------------------------|----------------|------------------|
| **Small** | N ≲ 256 | Setup, branches, L1 residency | `matmul_naive_n128`, `matmul_blocked_n128` |
| **Medium** | 256–512 | L2/L3 blocking quality | `matmul_naive` (N=256), `matmul_blocked` (N=512) |
| **Large single-node** | 1k–4k | RAM bandwidth, TLB, cache hierarchy | `matmul_blocked_n1024` |
| **Huge / “extreme”** | ≫ 4k, or N² ≫ RAM | **Out-of-core**, **distributed**, **mixed precision** | **Not** in tier-1 micro harness yet — needs dedicated track |

---

## 2. Techniques (literature → engineering)

### Single-node fast GEMM

1. **Cache blocking (Goto/BLIS)** — 3/4/5 nested loops; `mc×kc×nc` panels; register micro-kernel (e.g. 4×4 or 8×8 double) to maximize FMA reuse (**Eigen**, **BLIS**, **OpenBLAS**).
2. **Packing A & B** — copy tiles into contiguous buffers to avoid TLB thrash and enable SIMD (`A_pack`, `B_pack` in BLIS).
3. **Loop order / `i,k,j` vs `i,j,k`** — match memory layout (row-major Li vs col-major BLAS) to minimize strided access.
4. **Autotuning block sizes** — ATLAS/BLIS historically search `NB` per machine.

### Asymptotic improvements (less common at small N)

5. **Strassen–Winograd** — O(N^2.807); wins only for **very large** N; numerical stability trade-offs; used in some distributed frameworks.

### Huge matrices (don’t fit RAM or want parallel)

6. **2D / 2.5D SUMMA / Cannon** — block-cyclic decomposition over MPI ranks; minimizes communication volume for `C = A B`.
7. **Out-of-core (OOC)** — disk-backed tiles; double-buffer panels (**ScaLAPACK** `PDGEMM` patterns, **Elemental** history).
8. **GPU + CPU pipeline** — cuBLAS/rocBLAS for device GEMM; host overlap with streams (exascale practice in Kokkos + vendor BLAS).
9. **Mixed precision** — TensorCore FP16 accumulate FP32; iterative refinement (Haidar et al.) for backward error — **policy** required before claiming accuracy.

### Measurement

10. **N-sweeps** — publish `T(N)` table; fit roofline (`min(β_peak, π_bandwidth)`); report **GFLOPS** and **% of peak**.
11. **Warmup + median** — org `bench.py` already discards one warmup; huge runs may need **multiple medians** across cold cache.

---

## 3. Org harness mapping (this change set)

| Catalog `id` | Role |
|----------------|------|
| `matmul_naive_n128` | Small **O(N³)** naive baseline (N=128) |
| `matmul_naive` | Medium-small naive (N=256) |
| `matmul_blocked_n128` | Small **blocked** (128³) — cache behavior differs from 512 |
| `matmul_blocked` | Medium blocked (512³, BK=64) |
| `matmul_blocked_n1024` | Large single-node blocked (1024³) — stress bandwidth + compile |

**Beyond 1024:** add **OOC / MPI / GPU** benchmarks under a new tier or `bench_ecosystem.py` track — do not pretend `tier1_micro` static stack allocation is “exascale”.

---

## 4. References (starting points)

- BLIS / Goto: [FLAME BLIS](https://github.com/flame/blis), “Anatomy of high-performance matrix multiplication” (Goto & van de Geijn).
- Roofline: Williams, Waterman, Patterson.
- Distributed GEMM: SUMMA (van de Geijn & Watts), ScaLAPACK `PDGEMM` notes.
- Strassen: Higham, “Accuracy and Stability of Numerical Algorithms” (chapters on fast matrix multiply).

---

*Update when new N rows or out-of-core harness land.*
