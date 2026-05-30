# Proof gap researcher — cycle 33 (vec3_dot FieldAccess opaque ensures)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i / PH-2e / PH-2j · G-vc, G-oop, G-math, G-test-verify  
**Focus:** Float `vec3_dot` ensures — FieldAccess opaque in AutoVC; Vec3 type erasure; local-alias witness without field semantics  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** `vec3_dot` float ensures (`provability-gaps.md` G-vc “opaque vec3_dot-style returns”; P-linalg open float `vec3_dot`).
- **HYPOTHESIS: verified** — Field-access ensures (`a.x * b.x + …`) emit opaque marker + `Prop := True` + `trivial` discharge; no Lean field semantics.
- **HYPOTHESIS: verified** — `lean_type_name` erases module `Vec3` object params to `(a : Int) (b : Int)` in AutoVC formals.
- **HYPOTHESIS: verified** — `expr_to_lean` has no `FieldAccess` branch (`vc_emit_lean.cpp:202-254`); contrast `abs` Call handler only.
- **HYPOTHESIS: verified** — `packages/li-math` local-alias pattern (`ax * bx + …`) static-witnesses to `True` without linking locals to `a.x`/`b.x`.
- **HYPOTHESIS: verified** — No `vec3_dot` / `vec3_spec` in `Discharge.lean`; contrast `dot4_int_spec` + `linalg_dot4_float_closed`.
- **HYPOTHESIS: verified** — `manifest.toml` tiers `math_linalg/vec3_ops.li` as `verify_ok` despite opaque ensures (**G-test-verify** honesty gap).
- **Evidence test added:** `vec3_dot_opaque_ensures_gap.sh` → `contracts_discharge_corpus.sh`.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `FieldAccess` in VC Lean emit | **Missing (G-vc)** | `expr_to_lean` default → `nullopt`; no `FieldAccess` case |
| `Vec3` object type in AutoVC | **Erased to Int** | `lean_type_name` Named fallback `return "Int"` (`vc_emit_lean.cpp:138`) |
| `vec3_dot` semantic spec | **Missing (P-linalg)** | Zero `vec3` rows in `Discharge.lean` |
| Static witness on locals | **Shape-only** | `expr_same_shape` lacks `FieldAccess`; locals pattern bypasses field proof |

### 2. Contract gaps

- **G-vc:** Field-access ensures cannot translate; certificate uses vacuous `True` with opaque comment (field pattern) or static witness comment (locals pattern) — neither proves `result == dot(a, b)` over object fields.
- **G-oop:** Same `FieldAccess` gap family as cycle 30 `method_call_requires_lean_gap.sh` — object field refs in contracts are C++-witnessed or opaque, not Lean.
- **G-math:** Production `packages/li-math/src/lib.li:134-145` uses local-alias ensures (`ax * bx + …`) — certificate does not mention `a.x`/`b.x` linkage.
- **Contrast:** `linalg_dot4_float_closed.li` gets prelude `dot()` return witness with translatable array/index ensures.

### 3. Trusted surface

- No `trusted.lean` edits (policy). Gap is VC emit + type erasure, not axioms.

### 4. External trust boundaries

- **Deferred:** `Li.Discharge.vec3_dot_spec` + object-field Lean model — human RFC / **P-linalg** research scope.
- **Deferred:** `lean_type_name` for user `object` types — needs struct representation in Lean semantics.

### 5. Evidence pack

| Item | Location |
|------|----------|
| FieldAccess ensures opaque emit | `compiler/verify/vc_emit_lean.cpp:343-372` |
| Vec3 → Int type erasure | `compiler/verify/vc_emit_lean.cpp:111-138` |
| No FieldAccess in expr_to_lean | `compiler/verify/vc_emit_lean.cpp:202-254` |
| expr_same_shape no FieldAccess | `compiler/verify/vc_witness.cpp:52-71` |
| Production local-alias ensures | `packages/li-math/src/lib.li:134-145` |
| Field-access specimen | `li-tests/contracts_verify/linalg_vec3_dot_float_opaque.li` |
| Local-alias witness specimen | `li-tests/contracts_verify/linalg_vec3_dot_float_locals_witness.li` |
| Existing math_linalg test | `li-tests/math_linalg/vec3_ops.li` |
| Gap repro script | `li-tests/tooling/vec3_dot_opaque_ensures_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md:37,58,85` — open float `vec3_dot` |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/contracts_verify/linalg_vec3_dot_float_opaque.li   # exit 0
./build/compiler/lic/lic check li-tests/contracts_verify/linalg_vec3_dot_float_locals_witness.li  # exit 0
./li-tests/tooling/vec3_dot_opaque_ensures_gap.sh                                         # exit 0 PASS
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | Field-access vec3 ensures opaque + True stub | AutoVC after `linalg_vec3_dot_float_opaque.li` build |
| **verified** | Vec3 params erasure `(a : Int) (b : Int)` | Same AutoVC namespace `vec3_dot` |
| **verified** | No FieldAccess in expr_to_lean | grep `vc_emit_lean.cpp` — abs-only Call branch |
| **verified** | Local-alias pattern static-witnesses, still True | AutoVC `return expression matches ensures (static witness)` on locals specimen |
| **verified** | No vec3 spec in Discharge | grep `docs/semantics/Discharge.lean` |
| **verified** | manifest `verify_ok` ≠ semantic proof | `manifest.toml` `vec3_ops.li` + zero open goals via trivial |
| **deferred** | Real `vec3_dot_float_spec` in Lean | **P-linalg** / object semantics RFC |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-vc: translate `FieldAccess` in `expr_to_lean` for object ensures | **lic** | `provability`, `G-vc`, `PH-2e`, `G-oop` |
| P-linalg: `Li.Discharge.vec3_dot_spec` + wire AutoVC like `dot4_int_spec` | **lic** | `provability`, `G-math`, `PH-2i`, `G-lean` |
| Stop erasing user `object` types to `Int` in AutoVC formals | **lic** | `provability`, `G-vc`, `PH-2f` |
| Land `vec3_dot_opaque_ensures_gap.sh` + contracts_verify specimens | **lic** | `provability`, `testing` |
| Align li-math `vec3_dot` ensures to field-based contract + Lean spec | **lic** | `provability`, `G-math`, `packages/li-math` |

**Related:** cycle 30 method `requires` FieldAccess gap; cycle 32 mat2 eval vs MIR; `linalg_dot4_float_closed` contrast control.

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
- `vec3_cross` / `vec3_len` CallProc ensures chains (same FieldAccess + `li_rt_sqrt` family).
- `trusted.lean` — human gate only.
