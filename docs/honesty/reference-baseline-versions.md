# Reference baseline versions (HPC SOTA cadence)

Normative policy for **which upstream releases** the benchmarks org cites when comparing Li to reference C++ and competitive HPC stacks. Keeps **≤1.2× cpp** tier-1 claims credible as Eigen, Kokkos, PETSc, and Chapel ship on active 2025–2026 release trains.

**Related:** [benchmark-dashboard.md](./benchmark-dashboard.md) (ratio axes + validity) · [research-methodology.md](../numerics/research-methodology.md) · [ecosystem-explorer.md](../ecosystem/ecosystem-explorer.md)

**Issues:** [benchmarks#27](https://github.com/li-langverse/benchmarks/issues/27) · **PH-5b**, **PH-7e**, **G-math**

---

## Scope

| In scope | Out of scope |
|----------|----------------|
| Documented **SOTA reference pins** for tier-1/2 `compare_oracle = cpp` rows | CMake/package-manager pins in **lic** reference builds (separate implement issue after policy lands) |
| **When to bump** pins after upstream major/minor releases | Lowering `threshold_ratio_cpp` or weakening validity gates |
| **Competitive context** for Kokkos/PETSc/Chapel (methodology, not compile-time deps today) | Adding Chapel as a catalog language row (optional; deferred) |
| **Agent tooling parity** rubric (Chapel CLS / `chplcheck` vs Li Vision-LLM) | Language syntax comparisons |

Most tier-1 numerics rows today use **hand-written C** or **NR-style C++** in `lic/benchmarks/common/*`, not vendor-linked Eigen/Kokkos binaries. The pin table below is the **honest SOTA anchor** for studies, explorer digests, and future vendor-shim oracles — not a claim that every cpp row links these libraries at compile time.

---

## Pin table (seed — 2026-06-08)

Maintain this table when refreshing policy. Columns:

| Library | Pinned version | Role in org benches | Release URL | `last_reviewed` |
|---------|----------------|---------------------|-------------|-----------------|
| **Eigen** | **5.0.0** (2025-09-30) | BLAS-facing numerics SOTA; blocked GEMM / expression-template folklore for `matmul_blocked`, Horner studies | [Eigen releases](https://libeigen.gitlab.io/releases/) · [5.0 notes](https://libeigen.gitlab.io/releases/5.0/) | 2026-06-08 |
| **Kokkos** | **4.6.02** (2025-07; SYCL production) | Portable execution / memory-space rubric for **PH-7e** / **G-par**; handoff from [lic#110](https://github.com/li-langverse/lic/issues/110) | [Kokkos releases](https://kokkos.org/about/releases/) · [CHANGELOG](https://github.com/kokkos/kokkos/blob/develop/CHANGELOG.md) | 2026-06-08 |
| **PETSc** | **3.23** (2025-03-28) | Future implicit PDE / KSP–SNES stacks; tier-2 explicit FD rows cite LeVeque + PETSc manual for scalable path | [PETSc changes](https://petsc.org/release/changes/) · [3.23 notes](https://petsc.org/release/changes/323/) | 2026-06-08 |
| **Chapel** | **2.8** (2025-09; HPSF productivity axis) | Competitive **language + tooling** context only — not a `compare_oracle` today | [Chapel 2.8 announcement](https://chapel-lang.org/blog/posts/announcing-chapel-2-8/) · [releases](https://github.com/chapel-lang/chapel/releases) | 2026-06-08 |

**Patch-line rule:** stay on the latest **patch** within the pinned minor line (e.g. Kokkos 4.6.x) without a full policy PR; record the patch in explorer digests.

**Major/minor bump:** open a **benchmarks** docs PR updating this table within **30 calendar days** of the upstream release announcement affecting cited SOTA URLs or ABI (e.g. Eigen 5.x → 6.x, PETSc 3.23 → 3.24 with GPU/Kokkos view changes).

---

## Bump cadence

| Trigger | Owner | Action |
|---------|-------|--------|
| **Quarterly** (Jan / Apr / Jul / Oct) | `ecosystem_explorer` or `docs_maintainer` | Run `ecosystem-explorer.py --write-digest docs/ecosystem/explorer-digests/YYYY-MM-DD-explorer.md`; diff pin table vs upstream release pages |
| **Major or minor upstream release** | Same + `numerics_researcher` when numerics SOTA shifts | Mandatory table update **≤30 days**; link release notes in PR body |
| **lic reference build adopts vendor lib** | **lic** harness PR | Mirror pin here; cite **lic** commit/CMake flag — do not silently drift |
| **Dashboard perf claim** | Ingest maintainer | Cite pinned row in release notes: “green at *r* vs cpp on commit *sha*, validity pass, pins per [reference-baseline-versions.md](./reference-baseline-versions.md)” |

Command:

```bash
cd benchmarks
LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py \
  --write-digest docs/ecosystem/explorer-digests/$(date -u +%Y-%m-%d)-explorer.md
```

---

## Reference C++ builds (today)

| Tier | Typical oracle | Linked vendor libs today | Pin applies as |
|------|----------------|--------------------------|----------------|
| **Tier-1 micro** | `common/*_core.c`, NR-style C++ | Usually **none** (shared C kernels) | Methodology + future `@`/BLIS/Eigen oracles |
| **Tier-2 physics** | Explicit FD / symplectic C++ | **none** | PETSc/Kokkos for **future** implicit/distributed rows |
| **Tier-5 HTTP** | `nginx` (not cpp) | N/A | See [benchmark-dashboard.md](./benchmark-dashboard.md) |

When **lic** adds optional Eigen/MKL/Kokkos CMake flags (same pattern as FFTW opt-in in [FFT vendor rubrics](../ecosystem/plans/2026-05-30-fft-vendor-rubrics-ph5b.md)), the **pinned version** in this doc is the CI default unless `README` documents an intentional skip.

---

## Agent tooling parity (benchmark *tooling*, not syntax)

Future catalog or competitive rows may compare **agent-facing diagnostics**, not language syntax. Use this rubric so claims stay honest.

| Axis | Chapel stack | Li stack | Honest comparison |
|------|--------------|----------|-------------------|
| **Static analysis / lint for agents** | Chapel Language Server (CLS), [`chplcheck`](https://chapel-lang.org/docs/tools/chplcheck/chplcheck.html) | **`lic check --format=json`**, **`lic diagnose`** ([Vision-LLM spec](https://github.com/li-langverse/lic/blob/main/docs/superpowers/specs/2026-05-16-li-llm-first-design.md)) | Compare **structured output**, exit codes, and CI gate hooks — not “which language reads nicer” |
| **Proof posture** | Chapel proof story ≠ `lic build` Lean certificates | **`lic build` = proof certificate** (north star) | Do **not** claim tooling parity implies proof parity |
| **Bench row type** | Tooling smoke / export contract | Tooling smoke / JSON diagnostics | Label `variant = async_stub` or dedicated tooling tier; **no** tier-1 HPC threshold |
| **Differentiation** | Mature HPC IDE integrations | JSON-first agent handover, swarm preflight | Document in competitive/registry notes; cite this section in issues |

**Deferred:** a dedicated tooling benchmark row — file only after both sides expose stable machine-readable contracts in CI (see **lic** Vision-LLM tracker in [plan-cross-links.md](../ecosystem/plan-cross-links.md)).

---

## Proof vs performance

- Updating pins **does not** close any **G-*** row in [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md).
- A refreshed Eigen/Kokkos release **does not** by itself justify catalog threshold changes.
- Green dashboard rows remain **measurements** — see [benchmark-dashboard.md](./benchmark-dashboard.md).

---

## Learned from (policy sources)

1. [Eigen 5.0 release](https://libeigen.gitlab.io/releases/5.0/) — SemVer, C++17+, BLAS ABI shifts  
2. [Kokkos releases](https://kokkos.org/about/releases/) — 4.x→5.x capability checklist for execution spaces  
3. [PETSc release changes](https://petsc.org/release/changes/) — GPU/Kokkos view integration cadence  
4. [Chapel 2.8](https://chapel-lang.org/blog/posts/announcing-chapel-2-8/) — HPSF / quarterly language releases  
5. Explorer digest [2026-05-17](../ecosystem/explorer-digests/2026-05-17-explorer.md) · [2026-05-26](../ecosystem/explorer-digests/2026-05-26-explorer.md)
