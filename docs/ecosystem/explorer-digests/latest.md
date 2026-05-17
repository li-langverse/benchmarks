# Ecosystem explorer digest
Generated: 2026-05-17T08:42Z
## Missing std modules (benchmarks expectations)
- **std.io** (PH-IO-4): CSV/file ingest without Python
- **std.csv** (PH-IO-4): Benchmark CSV parsing in Li
- **std.summary** (PH-IO-7): Build data/latest/summary.json in Li
- **std.plot** (PH-IO-5): Static dashboard without Node/Vite

## HPC comparison highlights
- **Eigen** (partial): Pure-Li SIMD matmul vs Eigen/MKL; sparse support
- **Kokkos** (missing): Execution model + memory spaces for tier-2 physics
- **PETSc** (missing): Implicit solvers, AMG, distributed meshes
- **FFTW** (missing): Add micro FFT bench + std/signal or vendor hook
- **OpenMP** (partial): Document parallel loop lowering vs OpenMP runtime
- **HPX** (missing): Async/game physics scheduling

## Suggested web / Reddit searches
- [reddit] site:reddit.com (r/ProgrammingLanguages OR r/Compilers OR r/HPC OR r/cpp) systems programming language HPC SIMD ownership
- [reddit] site:reddit.com r/HPC Kokkos vs OpenMP performance portability 2024..2026
- [web] PETSc Kokkos integration best practices PDE solver stack
- [web] Eigen BLAS GEMM optimization techniques constexpr compile time
- [web] new programming languages memory safety performance C++ alternative 2025

## Recommended actions
- **P1** Implement missing std modules in lic (PH-IO track)
- **P2** Extend benchmarks catalog from HPC rubric
- **P2** Sync agent-kit versions across repos
- **P2** Run web/Reddit searches (see web_search_queries); file issues with label explorer-finding
