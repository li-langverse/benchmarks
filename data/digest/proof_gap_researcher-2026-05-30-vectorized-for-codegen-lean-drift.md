# Proof gap researcher — cycle 22 (`@vectorized for` codegen↔Lean drift; G-dec / G-meta)

**Run:** `proof_gap_researcher-2026-05-30-vectorized-for-codegen-lean-drift` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-dec**, **G-meta**, **G-vc**, **G-math** · **PH-7d, PH-2f**  
**north_star_fit:** provable pillar — `@vectorized(lanes=4) for` enables f64×4 array binop codegen under `@no_vectorize`, but no Lean witness ties SIMD lowering to scalar element-wise spec

## Executive summary

- **Focus:** Phase **7d-c** `@vectorized for` emits paired `ArraySimdScope` MIR (`lower.cpp:2125-2137`); codegen uses f64×4 gather/binop/scatter when scope stack active (`emit.cpp:1208-1215`, `1434-1443`).
- **New harness:** `vectorized_for_codegen_lean_drift.sh` + probes `vectorized_for_binop_codegen_probe.li` / `no_vectorize_binop_codegen_probe.li` — anti-DCE via `li_rt_sqrt` init + `volatile_sink`; gates `vmulpd` vs `vmulsd` in `li_user_main`.
- **HYPOTHESIS verified:** `@no_vectorize` + `@vectorized for` retains **2× `vmulpd`**; scalar contrast has **4× `vmulsd`**, **0× `vmulpd`**.
- **HYPOTHESIS verified:** No `witness_vectorized*` in `vc_witness.cpp`; no SIMD/array-binop eval lemma in `Discharge.lean` (contrast `dot4_int_loop_eval_spec`).
- **HYPOTHESIS verified:** `lic verify vectorized_for_scope_ok.li` reports **`mir_vectorized_proc=0`** — for-level decorator invisible to def-level MIR telemetry.
- **HYPOTHESIS falsified:** Constant-init `vectorized_for_scope_ok.li` (no sink on `z`) retains SIMD — LLVM const-folds binop; probe needs runtime `li_rt_sqrt` values.
- **No `trusted.lean` edits.**
- **`publish_subdir`** not injected (`provability_holes` auxiliary goal).

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-dec:** `@vectorized(lanes=4) for` lowers to `ArraySimdScope` push/pop around loop body (`mir.hpp:75-76`, `lower.cpp:2125-2137`).
- **G-math / G-meta:** `ArrayBinOpF64` selects f64×4 path when `array_simd_enabled()` (`emit.cpp:139-143`, `1208-1215`); scoped stack overrides `@no_vectorize` default-off (`emit.cpp:1834` sets `enable_array_simd = !fn.no_vectorize`).
- **G-meta Missing:** No Lean Prop equating f64×4 lowered binop to element-wise scalar spec on `LiArray Float 4`.

### 2. Contract gaps

- **7d-c closed slice (parse + MIR + codegen):** `vectorized_for_scope_ok.li` compiles; execution_resources smoke forbids `li_parallel_for_i64` conflation.
- **Open:** `witness_array_binop_f64x4_scope` + `array_binop_f64x4_eval_spec` (P-dec / P-linalg SIMD) — no AutoVC linkage.
- **Telemetry honesty:** `mir_vectorized_proc` counts **def-level** `@vectorized` only (`mir.cpp:7-14`); for-scope decorator not reflected in verify line for `vectorized_for_scope_ok.li`.

### 3. Trusted surface

- No new axioms; gap is witness + semantic lemma backlog plus codegen telemetry, not trusted-net/hardware axioms.

### 4. External trust boundaries

- Human: design SIMD-scope witness predicate matching `ArraySimdScope` + 4-wide binop pattern before claiming `@vectorized for` is Lean-closed.
- Human: extend verify telemetry (`mir_vectorized_for` or MIR insn count) so for-scope decorators are auditable without objdump.
- Human: decide whether default-on array SIMD outside `@no_vectorize` stays perf-advisory until **G-meta** slice exists.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `bash li-tests/tooling/vectorized_for_codegen_lean_drift.sh` | exit 0 — vec_vmulpd=2 scalar_vmulpd=0 scalar_vmulsd=4 |
| `lic check li-tests/codegen/vectorized_for_binop_codegen_probe.li` | exit 0 |
| `lic check li-tests/codegen/no_vectorize_binop_codegen_probe.li` | exit 0 |
| `lic verify li-tests/decorators/vectorized_for_scope_ok.li` | mir_vectorized_proc=0 |
| `lic verify li-tests/decorators/vectorized_dot_proc_ok.li` | mir_vectorized_proc=1 |

**Key file:line:**

- `compiler/mir/lower.cpp:2125-2137` — `@vectorized for` → `ArraySimdScope`
- `compiler/codegen/emit.cpp:139-143` — scope stack gates SIMD
- `compiler/codegen/emit.cpp:1208-1215` — f64×4 element-wise binop
- `compiler/verify/vc_witness.cpp` — no `witness_vectorized*` (contrast `witness_dot4_int_loop_impl:518`)
- `docs/semantics/Discharge.lean:27-33` — `dot4_int_loop_eval_spec` (contrast)
- `li-tests/codegen/vectorized_for_binop_codegen_probe.li` — anti-DCE SIMD probe
- `li-tests/tooling/vectorized_for_codegen_lean_drift.sh` — codegen gap gate
- `docs/verification/provability-gaps.md:39` — **G-dec Partial** (MIR telemetry; Lean **P-dec** open)

## Hypothesis outcomes

- **HYPOTHESIS: verified** — No `witness_vectorized*` in `vc_witness.cpp` | evidence: harness grep
- **HYPOTHESIS: verified** — No SIMD binop eval lemma in `Discharge.lean` | evidence: harness grep
- **HYPOTHESIS: verified** — `@vectorized for` under `@no_vectorize` emits `vmulpd` | evidence: harness vec_vmulpd=2
- **HYPOTHESIS: verified** — `@no_vectorize` without for-scope uses scalar `vmulsd` | evidence: harness scalar_vmulsd=4, scalar_vmulpd=0
- **HYPOTHESIS: verified** — For-scope `@vectorized` not in `mir_vectorized_proc` | evidence: verify `vectorized_for_scope_ok.li` → 0
- **HYPOTHESIS: falsified** — Constant-init `vectorized_for_scope_ok.li` retains SIMD at `-O3` | evidence: objdump `li_user_main` sinks constants only (const-fold)
- **HYPOTHESIS: deferred** — SIMD scope ≡ scalar element-wise in AutoVC | evidence: needs witness design + P-dec lemma

## Recommended issues/PRs

1. **lic:** Merge vectorized-for drift harness + probes; wired in `contracts_discharge_corpus.sh` — labels: `provability`, `G-dec`, `testing`
2. **lic:** `[P-dec] witness_array_binop_f64x4_scope + Discharge array_binop_f64x4_eval (4-wide pilot)` — labels: `provability`, `G-vc`, `PH-7d`
3. **lic:** Add `mir_vectorized_for` (or `ArraySimdScope` count) to `lic verify` telemetry — labels: `provability`, `G-dec`
4. **lic:** Update `provability-gaps.md` **G-dec** row — 7d-c codegen closed slice vs Lean open — labels: `provability`, `G-lean`
5. **lic:** Remove duplicate Proof-db appendix blocks (`provability-gaps.md`, lic#461) — labels: `provability`
6. **benchmarks:** Link cycle 22 digest in ecosystem grader provability row — labels: `provability`

## Deferred

- matmul IKJ / blocked loop witness (cycles 19–20 / lic#472)
- Horner FMA literal drift (cycle 21)
- mat2 FMA codegen vs Lean eval (cycles 16–17)
- `sqrt_open_bound` P-float intentional open
- Vec3 / CallProc opaque ensures (cycles 13–15)
- `publish_subdir` whitepaper — not injected this run
