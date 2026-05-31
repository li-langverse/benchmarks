# Proof gap researcher — cycle 37 (vec3_add component-wise field ensures)

**Run:** 2026-05-31 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i / PH-2e / PH-2j · G-vc, G-oop, G-math, G-test-verify  
**Focus:** Production `vec3_add`/`vec3_sub` per-field `==` ensures — FieldAccess + float binops in Lean emit; wrong-add soundness repro  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** `vec3_add` three component-wise ensures (`result.x == a.x + b.x`, …) — production pattern in `packages/li-math/src/lib.li:98-121`.
- **HYPOTHESIS: verified** — All three ensures emit opaque marker + `Prop := True` + `trivial`; no static return witness (ensures are not `result == …` form).
- **HYPOTHESIS: verified** — `vec3_add_bad` returning `(0,0,0)` against same field ensures still discharges with zero open goals (**soundness hole**).
- **HYPOTHESIS: verified** — `Vec3` param/result erasure to `(a : Int) (b : Int) (result : Int)` in AutoVC; no object-field Lean model.
- **HYPOTHESIS: verified** — Float `==` and `+` binops are supported in `expr_to_lean_bin` but never reached because LHS/RHS FieldAccess fails first.
- **HYPOTHESIS: verified** — Contrast cycle 33 `vec3_dot` locals witness: local-alias `result == ax*bx+…` can static-witness; per-field `result.x == …` cannot.
- **HYPOTHESIS: verified** — No `vec3_add` / `vec3_add_spec` in `Discharge.lean`; production `vec3_sub`/`vec3_scale` share same contract tier.
- **Evidence test added:** `vec3_add_field_ensures_lean_gap.sh` + `vec3_add_wrong_return.li` → `contracts_discharge_corpus.sh`.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `FieldAccess` in ensures (`result.x == a.x + b.x`) | **Missing (G-vc)** | No `FieldAccess` case in `expr_to_lean` (`vc_emit_lean.cpp:202-254`) |
| Float `==` / `+` binops | **Partial** | `expr_to_lean_bin` supports `=` / `+` (`vc_emit_lean.cpp:171-190`) but FieldAccess subexprs fail first |
| Three field ensures on one proc | **All opaque + vacuous** | AutoVC `ensures_0`…`ensures_2` — each `True` + `trivial` |
| Wrong implementation still certifies | **Soundness hole** | `vec3_add_wrong_return.li` — zeros return trivial discharge |
| No static return witness on field ensures | **Verified gap shape** | AutoVC lacks `Phase 2f: return expression matches ensures` (unlike `vec3_dot` locals) |
| Object return type erasure | **Missing (G-oop)** | `(a : Int) (b : Int) (result : Int)` — same family as cycles 33–36 |

### 2. Contract gaps

- **G-vc:** Component-wise field ensures cannot translate; certificate does **not** prove `result.x == a.x + b.x` over object fields.
- **G-oop:** No Lean field projection for `result.x` / `a.x`; bound and equality field contracts share the same opaque stub path.
- **G-math:** Production `vec3_add`, `vec3_sub`, `vec3_scale` in `li-math` all use per-field ensures — entire elementary Vec3 algebra tier is vacuous in Lean.
- **G-test-verify:** `math_linalg/vec3_ops.li` manifest `verify_ok` covers dot only; production add/sub/scale in package untested in proof corpus.
- **Contrast:** `linalg_dot4_float_closed` uses array index ensures (translatable); Vec3 object field ensures are a separate dead zone.

### 3. Trusted surface

- No `trusted.lean` edits (policy). Gap is VC emit + type erasure + contract tier honesty, not axioms.

### 4. External trust boundaries

- **Deferred:** `Li.Discharge.vec3_add_spec` + object-field Lean representation — human RFC / **P-linalg** + **G-oop**.
- **Deferred:** Opaque field ensures should fail closed (open VC) not `True+trivial` — product policy (same as cycles 35–36).
- **Deferred:** Wire production `li-math` vec3 ops into proof corpus or split manifest tier — package maintainer.

### 5. Evidence pack

| Item | Location |
|------|----------|
| No FieldAccess in expr_to_lean | `compiler/verify/vc_emit_lean.cpp:202-254` |
| Comparison/add binops supported | `compiler/verify/vc_emit_lean.cpp:171-190` |
| Opaque → True → trivial path | `compiler/verify/vc_emit_lean.cpp:367-416` |
| Vec3 → Int type erasure | `compiler/verify/vc_emit_lean.cpp:138` |
| expr_same_shape no FieldAccess | `compiler/verify/vc_witness.cpp:52-71` |
| Production vec3_add/sub field ensures | `packages/li-math/src/lib.li:98-121` |
| Field ensures specimen | `li-tests/contracts_verify/vec3_add_field_ensures.li` |
| Wrong-add soundness repro | `li-tests/contracts_verify/vec3_add_wrong_return.li` |
| Gap repro script | `li-tests/tooling/vec3_add_field_ensures_lean_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md:37,58` — open float vec3 family |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/contracts_verify/vec3_add_field_ensures.li   # exit 0
./build/compiler/lic/lic check li-tests/contracts_verify/vec3_add_wrong_return.li  # exit 0
./li-tests/tooling/vec3_add_field_ensures_lean_gap.sh                            # exit 0 PASS
```

**AutoVC excerpt (`vec3_add_field_ensures.li`):**

```
/-! VC ensures (opaque): source expr not yet translated -/
def vc_vec3_add_ensures_0 (a : Int) (b : Int) (result : Int) : Prop := True
theorem vc_vec3_add_ensures_0_proved (a : Int) (b : Int) (result : Int) : ... := trivial
… (ensures_1 … ensures_2 identical pattern)
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | Three field == ensures all opaque + True + trivial | AutoVC namespace `vec3_add` |
| **verified** | FieldAccess blocks float ==/+ translation | `expr_to_lean` default; opaque on all three |
| **verified** | Wrong add (0,0,0) still certifies | `vec3_add_bad` AutoVC — zero open goals |
| **verified** | Vec3 erasure to Int in AutoVC formals | `(a : Int) (b : Int) (result : Int)` |
| **verified** | No static return witness on field ensures | No `Phase 2f: return expression matches ensures` in namespace |
| **verified** | Production vec3_sub shares field ensures tier | `lib.li:110-120` same pattern |
| **verified** | No Discharge vec3_add spec | grep `Discharge.lean` — no vec3_add rows |
| **deferred** | Opaque field ensures should stay open | Policy — needs human issue |
| **deferred** | Real vec3_add_spec in Lean | **P-linalg** / **G-oop** RFC |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-vc: opaque FieldAccess == ensures should stay open (not True+trivial) | **lic** | `provability`, `G-vc`, `PH-2e` |
| P-linalg: `vec3_add_spec` + object field projection AutoVC for li-math vec3 algebra | **lic** | `provability`, `G-math`, `PH-2i`, `G-lean` |
| Land `vec3_add_field_ensures_lean_gap.sh` + wrong_return specimen | **lic** | `provability`, `testing` |
| G-test-verify: extend vec3 proof corpus for add/sub/scale or split manifest tier | **lic** | `provability`, `G-test-verify` |
| li-math: document vec3 field ensures as advisory until Lean wired | **lic** | `provability`, `G-math`, `package` |

**Related:** cycle 36 vec3_normalize bounds; cycle 35 vec3_cross CallProc; cycle 33 vec3_dot locals witness; lic **#472** P-linalg backlog.

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
- `vec3_scale` dedicated specimen — same FieldAccess gap; covered by production lib.li grep in script.
- `trusted.lean` — human gate only.
