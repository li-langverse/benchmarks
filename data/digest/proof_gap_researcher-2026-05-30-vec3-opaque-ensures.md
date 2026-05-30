# Proof gap researcher — cycle 13 (G-vc vec3 opaque ensures)

**Run:** `proof_gap_researcher-2026-05-30-vec3-opaque-ensures` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-vc**, **P-linalg** · **PH-2e, PH-2f, PH-2i**  
**north_star_fit:** provable pillar — float linalg `ensures` must carry dot-product math in Lean, not `Prop := True`

## Executive summary

- `vec3_dot` ensures with **FieldAccess** (`a.x * b.x + …`) are **opaque** in AutoVC — `expr_to_lean` has no `FieldAccess` case.
- Untranslatable ensures **default to `Prop := True`** with trivial `_proved`; certificate passes with **zero open goals**.
- **`return 0.0`** with field-dot ensures still **`lic build` succeeds** — no typecheck or Lean rejection (soundness hole).
- Body-local ensures (`ax * bx + …` matching return shape) discharge via **static return witness** — also stubs `True` without param↔result math.
- **`Vec3` erases to `Int`** in Lean VC formals — same object-type drift as method requires (cycle 12).
- CI guard **`vec3_dot_ensures_lean_gap.sh`** added; wired into **`contracts_discharge_corpus.sh`**.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-vc:** `vc_emit_lean.cpp:343` initializes `prop = "True"`; when `expr_to_lean` fails (~371), prop stays True instead of failing build or leaving an open goal.
- **G-math / P-linalg:** `packages/li-math/src/lib.li:136` ensures references body locals out of VC scope; `li-tests/math_linalg/vec3_ops.li` uses FieldAccess — both paths certify without dot math.

### 2. Contract gaps

- **P-linalg float Props:** No Lean predicate linking `result` to `a.x * b.x + a.y * b.y + a.z * b.z`; `Discharge.lean` has mat2 lemmas only.
- Static return witness (`vc_witness.cpp:537`) matches syntactic shape only — does not prove field reads equal param fields.

### 3. Trusted surface

- Unchanged; no `trusted.lean` edits.

### 4. External trust boundaries

- Human decision: introduce `LiObject`/`Vec3` Lean record + field-access translation before closing float linalg Props.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/vec3_dot_ensures_lean_gap.sh` | exit 0 (gap documented) |
| `lic build li-tests/math_linalg/vec3_ops.li` | exit 0; opaque ensures + True stub |
| `lic build li-tests/contracts_verify/vec3_dot_wrong_return.li` | exit 0; wrong return certifies |
| `lic check li-tests/contracts_verify/vec3_dot_wrong_return.li` | exit 0 (no E0303/E0304) |
| `lic build li-tests/contracts_verify/vec3_dot_locals_ensures.li` | exit 0; static witness True |

**Key file:line:**

- `compiler/verify/vc_emit_lean.cpp:202-254` — no `FieldAccess` in `expr_to_lean`
- `compiler/verify/vc_emit_lean.cpp:343-372` — default True + opaque fallback
- `compiler/verify/vc_witness.cpp:537-538` — `expr_same_shape` return witness
- `packages/li-math/src/lib.li:134-145` — body-local names in ensures
- `li-tests/contracts_verify/vec3_dot_wrong_return.li` — soundness repro
- `li-tests/math_linalg/vec3_ops.li` — FieldAccess ensures specimen

## Hypothesis outcomes

- **HYPOTHESIS: verified** — FieldAccess ensures emit opaque comment + `Prop := True` | evidence: `vec3_dot_ensures_lean_gap.sh`, AutoVC grep
- **HYPOTHESIS: verified** — Wrong return (`0.0`) still builds with field-dot ensures | evidence: `lic build vec3_dot_wrong_return.li` exit 0
- **HYPOTHESIS: verified** — Body-local ensures discharge via static return witness to True | evidence: AutoVC witness comment on `vec3_dot_locals_ensures.li`
- **HYPOTHESIS: verified** — Vec3 params erase to Int in Lean formals | evidence: AutoVC `(a : Int) (b : Int)`
- **HYPOTHESIS: falsified** — Lean certificate carries dot-product predicate | evidence: grep AutoVC — no `*` field math beyond True stub
- **HYPOTHESIS: deferred** — Emit Vec3 struct + field Props in Lean | evidence: needs LiObject Lean typing RFC (human)

## Recommended issues/PRs

1. **lic:** `[G-vc/P-linalg] expr_to_lean FieldAccess + Vec3 Lean type for float ensures` — labels: `provability`, `G-vc`, `PH-2i`
2. **lic:** `[G-vc] Fail or open-goal opaque ensures instead of default True` — labels: `provability`, `G-lean`
3. **lic:** `[P-linalg] Discharge.lean vec3_dot_spec + link li-math lib.li ensures` — labels: `provability`, `G-math`
4. **lic:** Retire `vec3_dot_ensures_lean_gap.sh` when gap closes; flip `vec3_dot_wrong_return.li` to `compile_fail`

## Deferred

- Method field requires (cycle 12 sibling)
- G-bnd/P-refine refinement Props (cycle 11)
- P-float `sqrt_open_bound` Lean discharge
- `vec3_cross` / `vec3_len` ensures — same FieldAccess pattern
