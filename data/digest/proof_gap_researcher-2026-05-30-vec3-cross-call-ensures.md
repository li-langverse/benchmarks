# Proof gap researcher — cycle 15 (G-vc vec3_cross CallProc+FieldAccess ensures)

**Run:** `proof_gap_researcher-2026-05-30-vec3-cross-call-ensures` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-vc**, **P-linalg** · **PH-2e, PH-2f, PH-2i**  
**north_star_fit:** provable pillar — `vec3_cross` / Vec3-return `ensures` must not certify via `Prop := True` stubs

## Executive summary

- `vec3_cross` ensures `result == vec3(a.y*b.z - …, …)` combine **CallProc** + **FieldAccess** + **BinOp** — all untranslated in `expr_to_lean`.
- Opaque ensures default to **`Prop := True`**; certificate has **zero open goals** with no cross-product predicate.
- **`return vec3(0,0,0)`** under cross-product ensures still **`lic build` succeeds** — soundness hole (Vec3-return sibling to cycles 13–14).
- **`Vec3` erases to `Int`** for params and `result` in Lean VC formals — no component-wise `result.x` typing.
- **`vec3_add` per-field ensures** (`result.x == a.x + b.x`, …) are **also opaque** — falsifies “component ensures witness locally” without FieldAccess translation.
- Production mirror: `packages/li-math/src/lib.li:146-151` `vec3_cross` uses the same CallProc ensures pattern.
- CI guard **`vec3_cross_ensures_lean_gap.sh`** added; wired into **`contracts_discharge_corpus.sh`**.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-vc:** `expr_to_lean` has no `FieldAccess` or general `Call` cases (`vc_emit_lean.cpp:224-232`, `252-254`); composite `vec3(...)` ensures hit opaque path (`368-372`).
- **`expr_same_shape`** does not compare `Call` trees (`vc_witness.cpp:52-71`); return/ensures syntactic match witness does **not** apply to `vec3_cross`.
- **`witness_direct_call_inherits_callee_ensures`** does not link `result == vec3(...)` to `vec3` callee field ensures (`result.x == x`) — shape mismatch.

### 2. Contract gaps

- **P-linalg:** No Lean bridge from `vec3_cross` ensures to per-component cross formulas; `Discharge.lean` has mat2 lemmas only.
- **P-linalg (retest):** Per-field `vec3_add` ensures are opaque True stubs too — not a mitigation path until FieldAccess + object `result` typing land.

### 3. Trusted surface

- Unchanged; no `trusted.lean` edits.

### 4. External trust boundaries

- Human decision: `LiObject`/`Vec3` Lean record + `expr_to_lean` for FieldAccess and struct-return `ensures` before closing float linalg Props.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/vec3_cross_ensures_lean_gap.sh` | exit 0 |
| `lic build --no-lean-verify li-tests/contracts_verify/vec3_cross_call_ensures.li` | exit 0; opaque `vc_vec3_cross_ensures_0` |
| `lic build --no-lean-verify li-tests/contracts_verify/vec3_cross_wrong_return.li` | exit 0; wrong return certifies |
| `lic check li-tests/contracts_verify/vec3_cross_wrong_return.li` | exit 0 (no E0303/E0304) |
| `lic build --no-lean-verify li-tests/contracts_verify/vec3_add_field_ensures.li` | exit 0; three opaque field ensures |

**Key file:line:**

- `compiler/verify/vc_emit_lean.cpp:138` — named types (Vec3) → `Int`
- `compiler/verify/vc_emit_lean.cpp:224-254` — no FieldAccess/Call in `expr_to_lean`
- `compiler/verify/vc_emit_lean.cpp:368-372` — opaque ensures → True
- `compiler/verify/vc_witness.cpp:52-71` — `expr_same_shape` no `Call`/`FieldAccess`
- `compiler/verify/vc_witness.cpp:504-522` — callee ensures inheritance requires shape match
- `packages/li-math/src/lib.li:146-151` — production `vec3_cross`
- `li-tests/contracts_verify/vec3_cross_wrong_return.li` — soundness repro

**AutoVC excerpt (`vec3_cross`):**

```lean
/-! VC ensures (opaque): source expr not yet translated -/
def vc_vec3_cross_ensures_0 (a : Int) (b : Int) (result : Int) : Prop := True
```

## Hypothesis outcomes

- **HYPOTHESIS: verified** — `vec3_cross` CallProc+FieldAccess ensures emit opaque + `Prop := True` | evidence: `vec3_cross_ensures_lean_gap.sh`, AutoVC `vc_vec3_cross_ensures_0`
- **HYPOTHESIS: verified** — Wrong `vec3(0,0,0)` return still builds | evidence: `lic build vec3_cross_wrong_return.li` exit 0
- **HYPOTHESIS: verified** — Vec3 params/result erase to `Int` in Lean | evidence: AutoVC `(a : Int) (b : Int) (result : Int)`
- **HYPOTHESIS: falsified** — Static return-shape witness discharges `vec3_cross` | evidence: no `Phase 2f: return expression` in `vec3_cross` namespace
- **HYPOTHESIS: falsified** — `witness_direct_call_inherits_callee_ensures` links cross ensures to `vec3` field ensures | evidence: `result == vec3(...)` vs `result.x == x` shape mismatch
- **HYPOTHESIS: falsified (retest)** — Per-field `vec3_add` ensures witness without FieldAccess translation | evidence: three opaque `VC ensures` comments on `vec3_add`
- **HYPOTHESIS: deferred** — Emit Vec3 struct + field/call Props in Lean | evidence: needs LiObject Lean typing RFC (human)

## Recommended issues/PRs

1. **lic:** `[G-vc/P-linalg] expr_to_lean FieldAccess + Call for Vec3 ensures` — labels: `provability`, `G-vc`, `PH-2i`
2. **lic:** `[G-vc] Vec3 Lean type for object returns (not Int erasure)` — labels: `provability`, `G-vc`, `PH-2f`
3. **lic:** `[G-vc] Reject build when ensures opaque but return wrong (vec3_cross_wrong_return)` — labels: `provability`, `G-lean`
4. **lic:** Retire `vec3_cross_ensures_lean_gap.sh` when gap closes; flip `vec3_cross_wrong_return.li` to `compile_fail`

## Deferred

- CallProc float ensures (`vec3_len_sq`, `vec3_len`) — cycles 14–15 sibling root cause
- FieldAccess float dot (`vec3_dot`) — cycle 13
- Method field requires Lean gap (cycle 12)
- G-bnd/P-refine refinement Props (cycle 11)
- `publish_subdir` whitepaper — not injected this run (`provability_holes` auxiliary goal)
