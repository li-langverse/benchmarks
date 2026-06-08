# HPC reference library release cadence (bench policy)

> **Issue:** [benchmarks#27](https://github.com/li-langverse/benchmarks/issues/27)  
> **Digest:** [2026-05-17-explorer.md](./explorer-digests/2026-05-17-explorer.md)  
> **Vision:** **proof → easy → fast** — keep `≤1.2× cpp` claims credible by pinning SOTA reference stacks and refreshing citations on a schedule.  
> **PH / G- linkage:** **PH-5b** (tier-1 micro harness), **PH-7e** (pure-Li codegen), **G-math**, **G-par** (Kokkos-class execution spaces).

## Goal

Document **baseline library versions** used (or planned) for reference C++ builds and **when to bump** them so org benchmarks and numerics studies cite current HPC release trains — without weakening [benchmark honesty](../honesty/benchmark-dashboard.md) or inventing harness code in **benchmarks** (harness stays in **lic**).

## Reference C++ baseline today

| Layer | Pin | Where enforced |
|-------|-----|----------------|
| **Language** | **C++17** minimum for catalog `compare_oracle = cpp` drivers | **lic** harness (`-std=c++17`); tier-1/tier-2 `cpp/` drivers |
| **Compiler flags** | `-O3 -march=native` (or CI-equivalent `-march=x86-64-v3` when documented) | **lic** `bench.py`; [competitive registry](../../benchmarks/workloads/competitive/registry.toml) `cpp_openmp` |
| **Numerics oracle** | Hand-written **`common/*_core.c`** kernels (NR/Eigen/BLIS *patterns*, not vendor-linked yet) | `benchmarks/workloads/*/common/` in this repo |
| **Vendor libraries** | **Not linked** in default tier-1/tier-2 CI today | Optional future **lic** CMake flags (MKL, FFTW) per [FFT vendor rubrics](./plans/2026-05-30-fft-vendor-rubrics-ph5b.md) |

**Honesty rule:** A **green** dashboard row compares Li to the **catalog oracle** (usually shared C or native C++), not to “latest Eigen on CRAN.” When a row adopts a vendor oracle, update this table **and** `catalog.toml` `compare_oracle` / release notes in the same PR.

## Version pins (SOTA refresh targets)

Review **quarterly** (or within **30 days** of a semver-major upstream release). Update the **Pinned** column and `last_reviewed` in [competitive registry](../../benchmarks/workloads/competitive/registry.toml).

| Library | Role in Li org | Pinned baseline (2026-06) | Official cadence | Bump when |
|---------|----------------|----------------------------|------------------|-----------|
| **Eigen** | Dense LA SOTA; future optional C++ oracle for `matmul_*` | **5.0.0** (2025-09-30); maintain **3.4.1** note for legacy BLAS ABI docs | [Releases index](https://libeigen.gitlab.io/releases/) | New **major/minor** with BLAS ABI or C++ std shift; before claiming “matches Eigen 5.x” in studies |
| **Kokkos** | Capability checklist for **PH-7e** / **G-par** lowering | **4.6+** production; track **5.x** on [releases page](https://kokkos.org/about/releases/) | ~2×/year feature releases | New execution-space / backend milestone tied to [lic#15](https://github.com/li-langverse/lic/issues/15); update explorer rubric |
| **PETSc** | Future implicit PDE / KSP stack reference | **3.23+** docs floor; cite **3.25.x** Kokkos integration in studies | [Changes index](https://petsc.org/release/changes/) | GPU/Kokkos view API changes affecting cited exascale patterns; before **lic** FFI/shim work ([lic#28](https://github.com/li-langverse/lic/issues/28)) |
| **Chapel** | HPC productivity competitor (watch track) | **2.8** ([announcement](https://chapel-lang.org/blog/posts/announcing-chapel-2-8/)); **2.0** stability baseline | ~2×/year | HPSF / language comparison docs; **not** a blocking bench oracle |

### Eigen-specific notes

- **5.0** introduces semver and **C++17** minimum; `EIGEN_USE_BLAS` return-type changes affect micro-benchmark oracles — re-run tier-1 `matmul_*` validity if linking Eigen in **lic**.
- Until Eigen is an optional harness dep, numerics studies cite Eigen for **algorithm blocking** only ([near-limit tier-1 SOTA](../numerics/studies/2026-05-17-near-limit-tier12-sota.md)).

### Kokkos / PETSc coupling

Exascale practice couples **PETSc** KSP/SNES with **Kokkos** device views — isolate sync points and profile GPU timelines ([explorer digest](./explorer-digests/2026-05-17-explorer.md)). Li gap: no distributed mesh / AMG story yet; pins here inform **roadmap** and **lic#14** / **lic#15**, not current CSV ratios.

## When to bump (checklist)

1. **Semver-major** upstream release for any row in the table above.
2. **Quarterly** `ecosystem_explorer` pass — compare pins to [explorer JSON](../../data/latest/ecosystem-explorer.json) `hpc_libraries` + web queries.
3. Before a **release note** or blog claims “SOTA parity” with a named library version.
4. When **lic** adds or changes a vendor-linked reference driver (MKL, FFTW, Eigen, PETSc shim).
5. After **CI image** or runner OS upgrade that changes default system packages — document skip reason if pin unchanged.

**Do not bump** only to green a red `pure_li` row — that is **lic** codegen work (**PH-7e**), not reference retuning.

## AI / agent tooling parity (not language syntax)

Benchmark **tooling** competition is separate from Chapel-vs-Li **language** benches:

| Surface | Chapel / HPC stack | Li org |
|---------|-------------------|--------|
| Static analysis / lint for agents | **Chapel Language Server (CLS)**; **`chplcheck`** CLI | **`lic check --format=json`**, **`lic diagnose`** (Vision-LLM) |
| Agent handover | Chapel compiler diagnostics (text) | Structured JSON + [`diagnostic-v1`](https://github.com/li-langverse/lic/blob/main/docs/superpowers/specs/2026-05-16-li-llm-first-design.md) schema |
| Proof gate | Chapel type/check modes (not Lean certificates) | **`lic build`** proof certificate — do not conflate lint green with **G-*** closure |

**Policy:** When comparing “AI-first” stacks in explorer digests or competitive reviews, cite **tooling parity** (JSON diagnostics, agent ingest, CI smoke) — not Chapel syntax or PGAS semantics. Track Vision-LLM completion in master plan; see [plan-cross-links](./plan-cross-links.md) **Vision-LLM** row.

## Non-goals

- Vendoring Eigen/Kokkos/PETSc into **benchmarks** or **lic** without human governance checklist.
- Adding Chapel/Kokkos harness columns before `plan-approved` catalog rows.
- Weakening `threshold_ratio_cpp` or validity gates to absorb upstream speedups.
- Cron-scheduled GitHub Actions for version polling (manual + explorer automation only).

## Related

| Doc / issue | Role |
|-------------|------|
| [benchmark-dashboard.md](../honesty/benchmark-dashboard.md) | Ratio axes, validity, variant honesty |
| [research-methodology.md](../numerics/research-methodology.md) | SOTA survey citations |
| [competitive/registry.toml](../../benchmarks/workloads/competitive/registry.toml) | `last_reviewed` stamps per ecosystem |
| [lic#33](https://github.com/li-langverse/lic/issues/33) | Eigen BLAS ABI in **lic** harness |
| [lic#15](https://github.com/li-langverse/lic/issues/15) | Kokkos-class lowering |
| [lic#28](https://github.com/li-langverse/lic/issues/28) | PETSc–Kokkos vs Li parallel model |

## Agents

On explorer runs that touch HPC rubric: read this policy before filing duplicate “pin Eigen” issues. Update **Pinned baseline** and registry `last_reviewed` in the same PR when bumps are justified.
