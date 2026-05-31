# Proof gap researcher — cycle 36 (vec3_normalize weak bound ensures)

**Run:** 2026-05-31 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i / PH-2e / PH-2j · G-vc, G-oop, G-hw, G-test-verify  
**Focus:** Production `vec3_normalize` per-axis `[-1,1]` bound ensures — FieldAccess + float comparison in Lean emit; wrong-bounds soundness repro  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** `vec3_normalize` six weak bound ensures (`result.x >= -1.0` … `result.z <= 1.0`) — deferred from cycle 35.
- **HYPOTHESIS: verified** — FieldAccess on `result.x` blocks `expr_to_lean`; all six ensures emit opaque marker + `Prop := True` + `trivial`.
- **HYPOTHESIS: verified** — `vec3_normalize_bad` returning `vec3(2.0, 2.0, 2.0)` against same bounds still discharges with zero open goals (**soundness hole**).
- **HYPOTHESIS: verified** — `Vec3` param/result erasure to `(a : Int) (result : Int)` in AutoVC; no object-field Lean model.
- **HYPOTHESIS: verified** — Contrast `sqrt_open_bound`: float `abs(...)` translates without FieldAccess; bound ensures fail on field access, not on float ops.
- **HYPOTHESIS: verified** — Weak per-axis bounds do not encode unit-length normalization (`||v||=1`); even a closed bounds proof would not prove correct normalize semantics.
- **HYPOTHESIS: verified** — No `vec3_normalize` / `normalize_spec` in `Discharge.lean`; production contracts in `packages/li-math/src/lib.li:164-171`.
- **Evidence test added:** `vec3_normalize_bound_ensures_lean_gap.sh` + two `contracts_verify` specimens → `contracts_discharge_corpus.sh`.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `FieldAccess` in ensures (`result.x >= …`) | **Missing (G-vc)** | No `FieldAccess` case in `expr_to_lean` (`vc_emit_lean.cpp:202-254`) |
| Float comparison ops (`>=`, `<=`) | **Partial** | `expr_to_lean_bin` supports `≥`/`≤` (`vc_emit_lean.cpp:181-188`) but LHS FieldAccess fails first |
| Six bound ensures on one proc | **All opaque + vacuous** | AutoVC `ensures_0`…`ensures_5` — each `True` + `trivial` |
| Wrong implementation still certifies | **Soundness hole** | `vec3_normalize_wrong_bounds.li` — `vec3(2,2,2)` trivial discharge |
| Object return type erasure | **Missing (G-oop)** | `(a : Int) (result : Int)` — same as vec3_cross cycle 35 |

### 2. Contract gaps

- **G-vc:** Per-axis bound ensures cannot translate; certificate does **not** prove components lie in `[-1,1]`.
- **G-oop:** No Lean field projection for `result.x`; bound contracts on object fields are vacuous stubs.
- **G-hw / P-float:** Production normalize uses `li_rt_sqrt` (trusted FP seam) but bound ensures omit sqrt/div semantics entirely — weaker than `sqrt_open_bound` which at least emits real `Float.abs` Props (intentionally open).
- **G-math:** `vec3_normalize` name implies unit vector; contracts only bound axis magnitudes — **spec honesty gap** even if Lean wired field access.
- **G-test-verify:** `math_linalg/vec3_ops.li` manifest `verify_ok` covers dot only; production normalize in `li-math` untested in proof corpus.

### 3. Trusted surface

- No `trusted.lean` edits (policy). Gap is VC emit + type erasure + weak contract tier, not axioms.
- `li_rt_sqrt` in production path is extern/trusted; specimen avoids sqrt to isolate bound-ensures emit gap.

### 4. External trust boundaries

- **Deferred:** Real `vec3_normalize_spec` (unit length or zero-vector) in `Discharge.lean` — human RFC / **P-float** + **G-oop**.
- **Deferred:** Opaque field-bound ensures should fail closed (open VC) like `sqrt_open_bound` — product policy.
- **Deferred:** Strengthen production contracts from weak bounds to `||result||=1 ∨ zero` — package author + proof backlog.

### 5. Evidence pack

| Item | Location |
|------|----------|
| No FieldAccess in expr_to_lean | `compiler/verify/vc_emit_lean.cpp:202-254` |
| Comparison binops supported | `compiler/verify/vc_emit_lean.cpp:181-188` |
| Opaque → True → trivial path | `compiler/verify/vc_emit_lean.cpp:367-416` |
| Vec3 → Int type erasure | `compiler/verify/vc_emit_lean.cpp:138` |
| Production vec3_normalize bounds | `packages/li-math/src/lib.li:164-171` |
| Bound ensures specimen | `li-tests/contracts_verify/vec3_normalize_bound_ensures.li` |
| Wrong-bounds soundness repro | `li-tests/contracts_verify/vec3_normalize_wrong_bounds.li` |
| Gap repro script | `li-tests/tooling/vec3_normalize_bound_ensures_lean_gap.sh` |
| Contrast open float VC | `li-tests/contracts_verify/sqrt_open_bound.li` |
| G-* register | `docs/verification/provability-gaps.md:37,56` — open float / vec3 family |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/contracts_verify/vec3_normalize_bound_ensures.li   # exit 0
./build/compiler/lic/lic check li-tests/contracts_verify/vec3_normalize_wrong_bounds.li  # exit 0
./li-tests/tooling/vec3_normalize_bound_ensures_lean_gap.sh                            # exit 0 PASS
```

**AutoVC excerpt (`vec3_normalize_bound_ensures.li`):**

```
/-! VC ensures (opaque): source expr not yet translated -/
def vc_vec3_normalize_ensures_0 (a : Int) (result : Int) : Prop := True
theorem vc_vec3_normalize_ensures_0_proved (a : Int) (result : Int) : ... := trivial
… (ensures_1 … ensures_5 identical pattern)
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | Six bound ensures all opaque + True + trivial | AutoVC namespace `vec3_normalize` |
| **verified** | FieldAccess blocks float comparison translation | `expr_to_lean` default; opaque markers on all six |
| **verified** | Wrong bounds (2,2,2) still certifies | `vec3_normalize_bad` AutoVC — zero open goals |
| **verified** | Vec3 erasure to Int in AutoVC formals | `(a : Int) (result : Int)` |
| **verified** | Float comparisons work without FieldAccess | `sqrt_open_bound` uses `Float.abs` (open, not True stub) |
| **verified** | Weak bounds ≠ unit-length normalize semantics | Contract tier analysis; no `||v||=1` in ensures |
| **verified** | No Discharge normalize spec | grep `Discharge.lean` — no vec3_normalize rows |
| **deferred** | Opaque field bounds should stay open | Policy — needs human issue |
| **deferred** | Real normalize spec in Lean | **P-float** / **G-oop** RFC |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-vc: opaque FieldAccess bound ensures should stay open (not True+trivial) | **lic** | `provability`, `G-vc`, `PH-2e` |
| P-float: `vec3_normalize` unit-length Discharge spec + field projection AutoVC | **lic** | `provability`, `G-math`, `PH-2i`, `G-lean` |
| Land `vec3_normalize_bound_ensures_lean_gap.sh` + contracts_verify specimens | **lic** | `provability`, `testing` |
| G-test-verify: extend vec3 proof corpus or split manifest tier for normalize | **lic** | `provability`, `G-test-verify` |
| li-math: strengthen vec3_normalize contracts (unit length / zero vector) | **lic** | `provability`, `G-math`, `package` |

**Related:** cycle 35 vec3_cross; cycle 33 vec3_dot; cycle 34 vec3_len CallProc; lic **#472** P-linalg backlog.

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
- Production `li_rt_sqrt` path FP proof — separate **P-float** pass with `sqrt_open_bound` corpus.
- `trusted.lean` — human gate only.
