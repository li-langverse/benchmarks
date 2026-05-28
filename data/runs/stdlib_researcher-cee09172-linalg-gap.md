# stdlib_researcher — session `cee09172` — `gap_vs_sota` (linear algebra)

**Goal:** `stdlib_ecosystem` · **north_star_fit:** ecosystem, scientific_computing, hpc · **PH:** 2i, 7e, AL-10, AL-11

**Artifacts:**
- `lic/docs/ecosystem/stdlib-research/cycle-1-gap-vs-sota-linalg.md`
- `research-findings/whitepapers/2026-05/stdlib_ecosystem/std-r0-cycle1-linalg-gap/README.md`

**Key finding:** Dense LA is in the **compiler prelude**, not `lic/std/math`. Missing `packages/linalg`, `std.tensor`, LAPACK-class APIs; `simd_dot` bench still uses extern C kernel; strict tier-1 perf incomplete.

**Next:** cycle 1 complete — see `stdlib_researcher-cee09172-synthesize.md`.
