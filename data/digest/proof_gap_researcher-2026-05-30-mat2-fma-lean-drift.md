# Proof gap researcher — cycle 17 (G-hw/G-meta FMA vs Lean mat2_at2_eval)

**Run:** `proof_gap_researcher-2026-05-30-mat2-fma-lean-drift` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-hw**, **G-meta**, **G-lean**, **G-math** · **PH-2f, PH-2i, PH-7e**  
**north_star_fit:** provable pillar — `lic build` Lean certificate must not imply release FMA codegen ≡ `mat2_at2_eval`

## Executive summary

- **Focus:** release `llvm.fmuladd` on 2×2 `ArrayMatMul2DF64` vs Lean `mat2_at2_eval` (mul-then-add IEEE model).
- **`mat2_fma_lean_drift.sh` passes:** release FMA prints `-12100672307.438484`; Lean eval `-12100672307.438477` (~7e-6 ULP-scale gap on one cell).
- **`--numerically-stable` / debug** codegen uses `FAdd(FMul)` and **matches** Lean eval on the same fixture.
- **`Discharge.lean:46-52`** defines `mat2_at2_eval` as sequential `*` then `+`; no FMA axiom — certificate is mul+add semantics only.
- **AutoVC** for `linalg_mat2_at2_float_closed.li` discharges via `Li.Discharge.mat2_at2_eval` (`vc_emit_lean.cpp:355-410`) — **not** MIR FMA.
- **`mat2_codegen_lean_drift.sh`** chains FMA witness; documents eval-vs-MIR + FMA soundness hole for tier-1 release builds.
- **No `trusted.lean` edits** — gap is policy/codegen (`fp_numerically_stable`), not new axioms.
- **`publish_subdir`** not injected (`provability_holes` auxiliary goal).

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-meta:** Executable 2×2 `@` lowers to `MirOp::ArrayMatMul2DF64` → `emit_matmul_aik_fma_j` uses `fmuladd` when `!fp_numerically_stable` (`emit.cpp:216-227`, `327-330`, `1440-1466`).
- **G-hw:** IEEE allows `(a*b)+c ≠ fma(a,b,c)`; witness cell `C[0][0] = A[0][0]*B[0][0] + A[0][1]*B[1][0]` with adversarial magnitudes in `mat2_fma_drift_rt.c:4-6`.
- Debug / `--numerically-stable` release: `fma_fn == nullptr` → `FAdd(FMul)` path matches Lean (`mat2_fma_lean_drift.sh` steps 3–4, 6–7).

### 2. Contract gaps

- **P-linalg:** Closed `mat2_at2_float_spec` proves eval semantics; **no** Prop that release FMA codegen refines `mat2_at2_eval`.
- `lic build` on closed specimen still **zero open goals** while release FMA can diverge — certificate scope is eval-only (extends cycle 16 eval-vs-MIR gap).

### 3. Trusted surface

- No new trusted axioms; `mat2_at2_float_spec_proved` (`Discharge.lean:55-58`) is definitional on mul+add eval.
- **`--numerically-stable`** (`main.cpp:555-556`, `compile.cpp:34`) is the user/toolchain escape hatch to align codegen with eval proof.

### 4. External trust boundaries

- Human: document in **G-hw** / tier-1 perf policy whether release `@` claims must use `--numerically-stable` or a future `mir_fp_model=` witness linking FMA to eval.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/mat2_fma_lean_drift.sh` | exit 0 — FMA≠lean; stable/debug=lean |
| `./li-tests/tooling/mat2_codegen_lean_drift.sh` | exit 0 — AutoVC uses `mat2_at2_eval`; FMA sub-harness ok |
| `lic check li-tests/math_linalg/mat2_at2_fma_drift_cell.li` | exit 0 |
| `lic build li-tests/contracts_verify/linalg_mat2_at2_float_closed.li` | exit 0; AutoVC `vc_mat2_at2_ensures_0` → `mat2_at2_eval` |

**Key file:line:**

- `docs/semantics/Discharge.lean:46-58` — mul+add `mat2_at2_eval`
- `compiler/codegen/emit.cpp:216-227` — FMA vs mul-add in matmul inner
- `compiler/codegen/emit.cpp:327-330` — FMA gated by `!fp_numerically_stable`
- `compiler/verify/vc_emit_lean.cpp:355-410` — discharge to eval, not codegen
- `li-tests/math_linalg/mat2_fma_drift_rt.c:4-6` — volatile adversarial fixtures
- `li-tests/math_linalg/mat2_at2_fma_drift_cell.li` — sparse 2×2 `@` witness
- `li-tests/tooling/mat2_fma_lean_drift.sh` — repro harness
- `docs/verification/provability-gaps.md:36` — `mat2_at2_eval` vs MIR still open

## Hypothesis outcomes

- **HYPOTHESIS: verified** — Release default matmul uses `fmuladd` when `!fp_numerically_stable` | evidence: `emit.cpp:223-224`, `mat2_fma_lean_drift.sh` REL≠LEAN
- **HYPOTHESIS: verified** — `--numerically-stable` release matches Lean mul+add on witness | evidence: `mat2_fma_lean_drift.sh` STABLE=LEAN
- **HYPOTHESIS: verified** — Lean `mat2_at2_eval` is mul-then-add, not FMA | evidence: `Discharge.lean:49-52`
- **HYPOTHESIS: verified** — AutoVC closed mat2 specimen discharges eval only | evidence: `mat2_codegen_lean_drift.sh`, `vc_mat2_at2_ensures_0`
- **HYPOTHESIS: falsified** — `lic build` certificate implies release FMA `@` matches proved semantics for all float inputs | evidence: FMA drift harness; eval-only Lean Prop
- **HYPOTHESIS: deferred** — Formal FMA-refines-mul-add lemma or codegen model flag in AutoVC | evidence: **G-meta** research; human policy on tier-1 release

## Recommended issues/PRs

1. **lic:** `[G-hw/G-meta] Document release `@` vs `--numerically-stable` for proved linalg` — labels: `provability`, `G-hw`, `PH-2f`
2. **lic:** Merge `research/provability-cycle17-mat2-fma-lean-drift-2026-05-30` (FMA witness + `mat2_codegen_lean_drift` chain) — labels: `provability`, `testing`
3. **lic:** `[G-meta] Optional AutoVC tag when release FMA enabled on float matmul` — labels: `provability`, `G-meta`, `PH-7e`
4. **roadmap/benchmarks:** Cross-link tier-1 perf strict mode with numerically-stable FP policy — labels: `provability`, `PH-7e`

## Deferred

- MIR↔eval refinement (cycle 16) — orthogonal to FMA ordering
- `sqrt_open_bound` P-float intentional open specimen
- Vec3 CallProc opaque ensures (cycles 13–15)
- `publish_subdir` whitepaper — not injected this run
