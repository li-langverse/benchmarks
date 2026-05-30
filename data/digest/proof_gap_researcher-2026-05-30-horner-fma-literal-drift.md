# Proof gap researcher — cycle 18 (Horner FmaFloatF64 vs Lean; literal-addend gate)

**Run:** `proof_gap_researcher-2026-05-30-horner-fma-literal-drift` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-hw**, **G-meta**, **G-math** · **PH-2f, PH-7e**  
**north_star_fit:** provable pillar — tier-1 Horner FMA codegen must not be confused with mul+add eval proved in Lean

## Executive summary

- **Focus:** `MirOp::FmaFloatF64` / `HornerFmaUnroll` always emit `llvm.fmuladd`; **`--numerically-stable` does not gate them** (unlike `ArrayMatMul2DF64`).
- **Prior witness was invalid:** `horner_fma_drift_step.li` uses **ident addend** → MIR never selects `FmaFloatF64` (`lower.cpp:350-356`).
- **New witness:** `horner_fma_drift_literal_step.li` (`acc = acc * x + -190131.7250991714`) reproduces release FMA drift vs Python mul+add eval.
- **`horner_fma_literal_lean_drift.sh` passes:** release & stable both drift (`-10872776000.067148` vs lean `-10872776000.06715`); debug matches lean.
- **Asymmetry vs mat2 (cycle 17):** matmul FMA respects `fp_numerically_stable`; Horner FMA paths do not (`emit.cpp:910-933`).
- **Tier-1 `horner_pure_li`** uses loop Horner lowering (`HornerFmaUnroll` / `HornerStepPow4`) with literal `+ 1.0` steps — same trust hole class.
- **No `trusted.lean` edits** — policy/codegen gap, not new axioms.
- **`publish_subdir`** not injected (`provability_holes` auxiliary goal).

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-meta:** `try_emit_fma_float_assign` only matches `acc * factor + <float|int lit>` (`lower.cpp:345-382`); variable addends fall through to generic mul+add stores.
- **G-hw:** `FmaFloatF64`, `HornerFmaUnroll`, `HornerStepPow4` unconditionally call `llvm.fmuladd` (`emit.cpp:910-949`) with **no** `fp_numerically_stable` branch (contrast matmul `emit.cpp:341-342`, `327-330`).
- **G-math:** Tier-1 perf row `horner_pure_li` documents FMA Horner; certificate story remains eval/mul+add unless codegen model is linked.

### 2. Contract gaps

- No closed Lean Prop for `FmaFloatF64` semantics; tier-1 bench checks runtime checksum vs Python ref, not FMA≡mul+add.
- `lic build` on witness specimens with `requires true` / `ensures true` does not capture hardware FMA drift.

### 3. Trusted surface

- No new axioms; gap is executable codegen policy vs IEEE mul-then-add model used in eval witnesses.

### 4. External trust boundaries

- Human: extend **G-meta** codegen model or gate `FmaFloatF64`/`Horner*` on `fp_numerically_stable` like matmul; document tier-1 Horner vs `--numerically-stable`.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `bash li-tests/tooling/horner_fma_literal_lean_drift.sh` | exit 0 — release/stable FMA ≠ lean; debug = lean |
| `bash li-tests/tooling/horner_fma_lean_drift.sh` | exit 0 — ident-addend negative control |
| `lic check li-tests/math_linalg/horner_fma_drift_literal_step.li` | exit 0 |

**Key file:line:**

- `compiler/mir/lower.cpp:345-382` — literal-addend gate for `FmaFloatF64`
- `compiler/mir/lower.cpp:1917-1920` — FMA assign hook on float stores
- `compiler/codegen/emit.cpp:910-949` — FMA Horner ops ignore `fp_numerically_stable`
- `compiler/codegen/emit.cpp:341-342` — matmul FMA gated (contrast)
- `li-tests/math_linalg/horner_fma_drift_literal_step.li` — true FMA witness
- `li-tests/math_linalg/horner_fma_drift_step.li` — negative control (ident addend)
- `li-tests/tooling/horner_fma_literal_lean_drift.sh` — repro harness

## Hypothesis outcomes

- **HYPOTHESIS: falsified** — `horner_fma_drift_step.li` exercises `FmaFloatF64` | evidence: ident addend rejected at `lower.cpp:350-356`; control harness
- **HYPOTHESIS: verified** — Literal addend `acc = acc * x + <float lit>` lowers to `FmaFloatF64` with release FMA drift | evidence: `horner_fma_literal_lean_drift.sh`
- **HYPOTHESIS: verified** — `--numerically-stable` does **not** disable Horner `FmaFloatF64` (unlike mat2) | evidence: stable output drifts same as release in literal harness
- **HYPOTHESIS: verified** — Debug build uses mul+add matching lean eval on literal witness | evidence: literal harness debug step
- **HYPOTHESIS: deferred** — Formal FMA-refines-mul+add in AutoVC for Horner tier-1 | evidence: **G-meta** research; no closed Horner Prop in `contracts_verify/`

## Recommended issues/PRs

1. **lic:** `[G-hw/G-meta] Gate FmaFloatF64 / HornerFmaUnroll on fp_numerically_stable` — labels: `provability`, `G-hw`, `PH-7e`
2. **lic:** Merge Horner literal FMA witness + fix ident-addend negative control — labels: `provability`, `testing`
3. **lic:** Document literal-addend requirement for FMA MIR in `provability-gaps.md` / tier-1 notes — labels: `provability`, `G-math`
4. **benchmarks:** Link cycle 18 digest in ecosystem grader provability row — labels: `provability`

## Deferred

- mat2 FMA + eval-vs-MIR (cycles 16–17)
- `sqrt_open_bound` P-float intentional open specimen
- Vec3 CallProc opaque ensures (cycles 13–15)
- `publish_subdir` whitepaper — not injected this run
