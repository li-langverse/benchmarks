# Proof gap researcher — cycle 16 (G-lean/G-math mat2_at2_eval vs MIR codegen)

**Run:** `proof_gap_researcher-2026-05-30-mat2-codegen-lean-drift` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-lean**, **G-math**, **G-meta**, **G-trust** · **PH-2f, PH-2i, PH-7e**  
**north_star_fit:** provable pillar — `lic build` certificate for 2×2 `@` must not overclaim codegen correctness

## Executive summary

- AutoVC for `linalg_mat2_at2_float_closed.li` discharges via **`Li.Discharge.mat2_at2_eval`** — a hand-written Lean function, not MIR.
- **`ArrayMatMul2DF64`** is what `return A @ B` lowers to (`lower.cpp:1110`, `emit.cpp:1175-1195`); no Lean lemma links MIR matmul to `mat2_at2_eval`.
- Certificate is **zero open goals** while **G-meta** (compiler ≡ semantics) remains open — semantic proof does not cover executable codegen.
- Runtime golden **`mat2_at2_golden_2x2.li`** confirms codegen matches eval on one integer-valued fixture; not a general refinement proof.
- FMA vs mul-add ordering in codegen (`emit.cpp:232-247`) can diverge from Lean `mat2_at2_eval` on non-exact float inputs — **G-hw** adjacent.
- **`witness_mat2_int_at2_spec`** name is misleading — triggers on float `@` specimens (`vc_witness.cpp:415-424`).
- CI guard **`mat2_codegen_lean_drift.sh`** re-added (cycle 9 branch never merged); wired into **`contracts_discharge_corpus.sh`**.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-meta:** Lean proves `mat2_at2_float_spec A B (mat2_at2_eval A B)` (`Discharge.lean:55-58`); executable path uses `MirOp::ArrayMatMul2DF64` with IJK loops or unrolled FMA (`emit.cpp:1175-1195`, `232-247`).
- **G-lean:** `lic build` on closed mat2 specimen passes Lean typecheck with **no open VCs** — certificate attests eval semantics only.
- Lowering: 2×2 float `@` in return position → `ArrayMatMul2DF64` with dims m=2,k=2,n=2 (`lower.cpp:1095-1118`).

### 2. Contract gaps

- **P-linalg:** Closed slice is **spec-level** (`mat2_at2_float_spec` + `mat2_at2_eval`); no `mir_return_linked=` witness for `@` lowering.
- `vc_emit_lean.cpp:355-366` routes mat2 ensures to `Li.Discharge.mat2_at2_eval A B`, bypassing opaque-ensures path.

### 3. Trusted surface

- No `trusted.lean` axiom for `ArrayMatMul2DF64`; gap documented in release notes (`2026-05-22-mat2-float-spec-closed.md:12`).
- `Discharge.lean` has no `mat2_at2_mir_refines_eval` theorem — intentional deferral to **G-trust** / codegen witness RFC.

### 4. External trust boundaries

- Human decision: add MIR↔Lean refinement lemma (or trusted codegen axiom) before claiming end-to-end `@` proof; FP associativity policy (`fp_numerically_stable`) affects FMA path.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/mat2_codegen_lean_drift.sh` | exit 0 |
| `lic build li-tests/contracts_verify/linalg_mat2_at2_float_closed.li` | exit 0; AutoVC uses `mat2_at2_eval` |
| `lic check li-tests/math_linalg/mat2_at2_golden_2x2.li` | exit 0 |
| `lic build --no-lean-verify li-tests/math_linalg/mat2_at2_golden_2x2.li -o /tmp/mat2_golden && /tmp/mat2_golden` | exit 0 |

**Key file:line:**

- `docs/semantics/Discharge.lean:46-58` — `mat2_at2_eval`, closed spec proof
- `compiler/verify/vc_emit_lean.cpp:355-410` — mat2 discharge → eval not MIR
- `compiler/mir/lower.cpp:1109-1117` — `@` → `ArrayMatMul2DF64`
- `compiler/codegen/emit.cpp:1175-1195` — codegen matmul (loops/unrolled)
- `compiler/codegen/emit.cpp:232-247` — FMA when `!fp_numerically_stable`
- `docs/verification/provability-gaps.md:36` — `mat2_at2_eval` trusted vs MIR `@` still open
- `li-tests/math_linalg/mat2_at2_golden_2x2.li` — runtime smoke
- `li-tests/tooling/mat2_codegen_lean_drift.sh` — certificate-vs-codegen guard

**AutoVC excerpt:**

```lean
def vc_mat2_at2_ensures_0 ... : Prop :=
  Li.Discharge.mat2_at2_float_spec A B (Li.Discharge.mat2_at2_eval A B)
theorem vc_mat2_at2_ensures_0_proved ... :=
  Li.Discharge.mat2_at2_float_spec_proved A B
```

## Hypothesis outcomes

- **HYPOTHESIS: verified** — AutoVC discharges 2×2 `@` via `mat2_at2_eval`, not MIR | evidence: `mat2_codegen_lean_drift.sh`, AutoVC grep
- **HYPOTHESIS: verified** — MIR lowers 2×2 float `@` to `ArrayMatMul2DF64` | evidence: `lower.cpp:1110`, `emit.cpp:1175`
- **HYPOTHESIS: verified** — No Lean/MIR refinement lemma in `Discharge.lean` or `trusted.lean` | evidence: grep; release note blocked item
- **HYPOTHESIS: verified** — Runtime golden matches eval on fixture C=[[19,22],[43,50]] | evidence: `mat2_at2_golden_2x2.li` exit 0
- **HYPOTHESIS: falsified** — `lic build` certificate implies codegen-correct `@` for all inputs | evidence: eval-only Lean Prop; single golden fixture
- **HYPOTHESIS: deferred** — Formal MIR↔eval refinement proof | evidence: needs **G-trust** codegen witness RFC (human)

## Recommended issues/PRs

1. **lic:** `[G-meta/G-trust] MIR ArrayMatMul2DF64 refines mat2_at2_eval — Lean lemma or trusted axiom` — labels: `provability`, `G-meta`, `PH-2f`
2. **lic:** `[G-math] mir_return_linked witness for @ lowering (2×2 float)` — labels: `provability`, `G-math`, `PH-2i`
3. **lic:** Merge `mat2_codegen_lean_drift.sh` + golden into main CI — labels: `provability`, `testing`
4. **lic:** Rename `witness_mat2_int_at2_spec` → `witness_mat2_at2_spec` (float+int) — labels: `provability`, `cleanup`

## Deferred

- Vec3 CallProc/FieldAccess opaque ensures (cycles 13–15) — sibling **G-vc** class
- P-float `sqrt_open_bound` intentional open specimen
- FMA ordering vs Lean eval on non-exact float matrices — **G-hw** / numerics policy
- `publish_subdir` whitepaper — not injected this run (`provability_holes` auxiliary goal)
