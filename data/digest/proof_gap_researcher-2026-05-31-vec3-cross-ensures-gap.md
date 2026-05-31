# Proof gap researcher — cycle 35 (vec3_cross CallProc+FieldAccess ensures)

**Run:** 2026-05-31 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i / PH-2e / PH-2j · G-vc, G-oop, G-math, G-test-verify  
**Focus:** Production `vec3_cross` ensures — object constructor `vec3(...)` + FieldAccess in RHS; wrong-return soundness repro  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** `vec3_cross` ensures `result == vec3(a.y * b.z - …, …)` — CallProc constructor + FieldAccess arithmetic (deferred from cycle 34).
- **HYPOTHESIS: verified** — Ensures emit opaque marker + `Prop := True` + `trivial`; no static return witness comment.
- **HYPOTHESIS: verified** — `vec3_cross_bad` returning `vec3(0,0,0)` against cross-product ensures still discharges with zero open goals (**soundness hole**).
- **HYPOTHESIS: verified** — `Vec3` params/result erasure to `(a : Int) (b : Int) (result : Int)` in AutoVC; no object-field Lean model.
- **HYPOTHESIS: verified** — `expr_to_lean` has no `FieldAccess` case and no `vec3` Call handler (`vc_emit_lean.cpp:230-300`).
- **HYPOTHESIS: verified** — Per-field `vec3_add` ensures (`result.x == …`) also opaque stubs — not component-wise static witnesses.
- **HYPOTHESIS: verified** — No `vec3_cross` / `vec3_spec` in `Discharge.lean`; `manifest.toml` tiers `math_linalg/vec3_ops.li` as `verify_ok` (**G-test-verify** honesty gap).
- **Evidence test added:** `vec3_cross_ensures_lean_gap.sh` + three `contracts_verify` specimens → `contracts_discharge_corpus.sh`.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `Call` to user constructor in ensures | **Missing (G-vc)** | `expr_to_lean` Call: only `abs`, disjoint_* helpers (`vc_emit_lean.cpp:252-277`) |
| `FieldAccess` in ensures RHS | **Missing (G-vc)** | No `FieldAccess` case in `expr_to_lean` default → `nullopt` |
| Whole-object `result == vec3(...)` | **Opaque + vacuous** | AutoVC `VC ensures (opaque)` + `Prop := True` + `_proved := trivial` |
| Wrong implementation still certifies | **Soundness hole** | `vec3_cross_wrong_return.li` — same trivial discharge |
| Object equality in ensures | **Missing (G-oop)** | No struct equality in Lean emit; contrast array `@` closed specimens |

### 2. Contract gaps

- **G-vc:** Cross-product ensures cannot translate; certificate does **not** prove `result == cross(a,b)` over object fields.
- **G-oop:** Per-field ensures on `result.x`/`result.y`/`result.z` (`vec3_add`) also opaque — component contracts do not link to return object semantics in Lean.
- **G-math:** Production `packages/li-math/src/lib.li:149-154` — same CallProc+FieldAccess pattern as specimen; included in `math_linalg/vec3_ops.li` compile tests with `verify_ok` manifest tier.
- **P-linalg:** Open float `vec3_dot` family extends to `vec3_cross` whole-object ensures; no `Li.Discharge.vec3_cross_spec`.

### 3. Trusted surface

- No `trusted.lean` edits (policy). Gap is VC emit + type erasure, not axioms.
- Nested `vec3` constructor callee emits separate call-site requires VCs (all `True` + trivial) — does not propagate cross math to caller ensures.

### 4. External trust boundaries

- **Deferred:** `Li.Discharge.vec3_cross_spec` + object constructor/equality Lean model — human RFC / **P-linalg** + **G-oop** joint pass.
- **Deferred:** Opaque whole-object ensures should fail closed (open VC) like `sqrt_open_bound` — product policy decision.

### 5. Evidence pack

| Item | Location |
|------|----------|
| No FieldAccess in expr_to_lean | `compiler/verify/vc_emit_lean.cpp:230-300` |
| Opaque → True → trivial path | `compiler/verify/vc_emit_lean.cpp:445-524` |
| Vec3 → Int type erasure | `compiler/verify/vc_emit_lean.cpp:138` |
| Production vec3_cross | `packages/li-math/src/lib.li:149-154` |
| Cross-product specimen | `li-tests/contracts_verify/vec3_cross_call_ensures.li` |
| Wrong-return soundness repro | `li-tests/contracts_verify/vec3_cross_wrong_return.li` |
| Per-field ensures contrast | `li-tests/contracts_verify/vec3_add_field_ensures.li` |
| Gap repro script | `li-tests/tooling/vec3_cross_ensures_lean_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md:37,58,68` — open float vec3 family |
| Manifest honesty | `li-tests/manifest.toml:878-879` — `vec3_ops.li` `verify_ok` |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/contracts_verify/vec3_cross_call_ensures.li      # exit 0
./build/compiler/lic/lic check li-tests/contracts_verify/vec3_cross_wrong_return.li     # exit 0
./build/compiler/lic/lic check li-tests/contracts_verify/vec3_add_field_ensures.li      # exit 0
./li-tests/tooling/vec3_cross_ensures_lean_gap.sh                                     # exit 0 PASS
```

**AutoVC excerpt (`vec3_cross_call_ensures.li`):**

```
/-! VC ensures (opaque): source expr not yet translated -/
def vc_vec3_cross_ensures_0 (a : Int) (b : Int) (result : Int) : Prop := True
theorem vc_vec3_cross_ensures_0_proved ... := trivial
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | vec3_cross ensures opaque + True + trivial | AutoVC namespace `vec3_cross` |
| **verified** | No static return witness on cross ensures | Absence of `Phase 2f: return expression matches ensures` in `vec3_cross` namespace |
| **verified** | Wrong return still certifies (soundness hole) | `vec3_cross_bad` AutoVC — same trivial discharge |
| **verified** | Vec3 erasure to Int in AutoVC formals | `(a : Int) (b : Int) (result : Int)` |
| **verified** | Per-field vec3_add ensures also opaque | Three `VC ensures (opaque)` rows; all `Prop := True` |
| **verified** | No Discharge vec3_cross spec | grep `Discharge.lean` — no vec3_cross rows |
| **verified** | manifest verify_ok ≠ semantic proof | `manifest.toml:878-879` + vacuous chain |
| **deferred** | Opaque object ensures should stay open | Policy — needs human issue |
| **deferred** | Real `vec3_cross_spec` in Lean | **P-linalg** / **G-oop** RFC |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-vc: opaque object-constructor ensures should stay open (not True+trivial) | **lic** | `provability`, `G-vc`, `PH-2e` |
| P-linalg: `vec3_cross` Discharge spec + object equality AutoVC wiring | **lic** | `provability`, `G-math`, `PH-2i`, `G-lean` |
| Land `vec3_cross_ensures_lean_gap.sh` + contracts_verify specimens | **lic** | `provability`, `testing` |
| G-test-verify: annotate `vec3_ops.li` until cross/dot chain proved | **lic** | `provability`, `G-test-verify` |
| G-oop: per-field `result.x` ensures need Lean field model or open VC | **lic** | `provability`, `G-oop`, `PH-2j` |

**Related:** cycle 33 vec3_dot FieldAccess; cycle 34 vec3_len CallProc chain; lic **#472** P-linalg loop witness backlog.

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
- `vec3_normalize` weak bound ensures (`result.x >= -1.0` …) — separate float bound VC pass.
- `trusted.lean` — human gate only.
