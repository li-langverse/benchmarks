# Proof gap researcher — cycle 14 (G-vc vec3_len CallProc ensures)

**Run:** `proof_gap_researcher-2026-05-30-vec3-len-call-ensures` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-vc**, **P-linalg**, **P-float** · **PH-2e, PH-2f, PH-2i**  
**north_star_fit:** provable pillar — `vec3_len_sq` / `vec3_len` must not certify via CallProc ensures stubs

## Executive summary

- `ensures result == vec3_dot(a, a)` with `return vec3_dot(a, a)` is **opaque** (Call expr in ensures), not static return-shape witness.
- Opaque CallProc ensures default to **`Prop := True`**; certificate has **zero open goals** but no dot linkage.
- **`return 0.0`** under `ensures result == vec3_dot(a, a)` still **`lic build` succeeds** — soundness hole (same class as cycle 13 field-dot).
- **`vec3_len`** with `ensures result == li_rt_sqrt(vec3_len_sq(a))` is opaque; no `sqrt_open_bound`-class abs predicate in AutoVC.
- **`witness_direct_call_inherits_callee_ensures`** does not apply — caller/callee ensures shapes differ (`result == call` vs `result == field math`).
- Production mirror: `packages/li-math/src/lib.li` `vec3_len_sq` / `vec3_len` use the same CallProc pattern.
- CI guard **`vec3_len_ensures_lean_gap.sh`** added; wired into **`contracts_discharge_corpus.sh`**.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-vc:** `expr_to_lean` has no `Call` case (except `abs`); `ensures result == vec3_dot(...)` triggers opaque comment + `Prop := True` (`vc_emit_lean.cpp:224-232`, `368-372`).
- **Retest (cycle 13 deferred):** CallProc ensures are **not** discharged via `expr_same_shape` return witness (`vc_witness.cpp:52-71` — `Call` falls through `default: false`).
- Unreachable-only procs omitted from AutoVC when `main` does not call them (build emits VCs only for reachable procs from entry).

### 2. Contract gaps

- **P-linalg:** No Lean bridge from `vec3_len_sq` ensures to `vec3_dot` callee ensures; call-site `requires` stub `True` only.
- **P-float:** `vec3_len` nested `li_rt_sqrt(vec3_len_sq(a))` stays opaque — distinct from `sqrt_open_bound.li` (which keeps abs VC open) but same certificate weakness (True stub).

### 3. Trusted surface

- Unchanged; no `trusted.lean` edits.

### 4. External trust boundaries

- Human decision: inherit callee ensures in Lean when return is direct call (`witness_direct_call_inherits_callee_ensures`) vs require translated CallProc Props.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/vec3_len_ensures_lean_gap.sh` | exit 0 |
| `lic build --no-lean-verify li-tests/contracts_verify/vec3_len_sq_call_ensures.li` | exit 0; opaque `vec3_len_sq_ensures` |
| `lic build --no-lean-verify li-tests/contracts_verify/vec3_len_sq_wrong_return.li` | exit 0; wrong return certifies |
| `lic check li-tests/contracts_verify/vec3_len_sq_wrong_return.li` | exit 0 (no E0303/E0304) |
| `lic build --no-lean-verify li-tests/contracts_verify/vec3_len_sqrt_call_ensures.li` | exit 0; opaque `vec3_len_ensures` |

**Key file:line:**

- `compiler/verify/vc_emit_lean.cpp:224-232` — `Call` untranslated except `abs`
- `compiler/verify/vc_emit_lean.cpp:368-372` — opaque ensures → True
- `compiler/verify/vc_witness.cpp:504-522` — `witness_direct_call_inherits_callee_ensures` (shape match on full ensures expr)
- `compiler/verify/vc_witness.cpp:52-71` — `expr_same_shape` no `Call`
- `packages/li-math/src/lib.li:152-163` — production `vec3_len_sq` / `vec3_len`
- `li-tests/contracts_verify/vec3_len_sq_wrong_return.li` — soundness repro

## Hypothesis outcomes

- **HYPOTHESIS: verified** — CallProc in ensures (`result == vec3_dot(a,a)`) emits opaque + `Prop := True` | evidence: `vec3_len_ensures_lean_gap.sh`, AutoVC `vc_vec3_len_sq_ensures_0`
- **HYPOTHESIS: verified** — Wrong literal return still builds | evidence: `lic build vec3_len_sq_wrong_return.li` exit 0
- **HYPOTHESIS: verified** — Nested `li_rt_sqrt(vec3_len_sq(a))` ensures opaque True | evidence: AutoVC `vc_vec3_len_ensures_0`
- **HYPOTHESIS: falsified** — Static return-shape witness discharges `vec3_len_sq` | evidence: no `Phase 2f: return expression` in `vec3_len_sq` namespace
- **HYPOTHESIS: falsified** — `witness_direct_call_inherits_callee_ensures` links `vec3_len_sq` to `vec3_dot` math | evidence: ensures shapes differ; opaque path used
- **HYPOTHESIS: deferred** — Emit CallProc Props + callee ensures inheritance in Lean | evidence: needs `expr_to_lean` Call + LiObject/Vec3 typing (human)

## Recommended issues/PRs

1. **lic:** `[G-vc/P-linalg] expr_to_lean for CallProc ensures + callee ensures inheritance` — labels: `provability`, `G-vc`, `PH-2i`
2. **lic:** `[G-vc] Reject build when ensures opaque but return not shape-matched (wrong_return)` — labels: `provability`, `G-lean`
3. **lic:** `[P-float] vec3_len sqrt chain — link to sqrt_open_bound or open goal` — labels: `provability`, `P-float`
4. **lic:** Retire `vec3_len_ensures_lean_gap.sh` when gap closes; flip `vec3_len_sq_wrong_return.li` to `compile_fail`

## Deferred

- Cycle 13 field-access `vec3_dot` opaque ensures (sibling; same True-stub root cause)
- Method field requires Lean gap (cycle 12)
- G-bnd/P-refine refinement Props (cycle 11)
- `vec3_cross` Vec3-return ensures (FieldAccess + struct literal)
