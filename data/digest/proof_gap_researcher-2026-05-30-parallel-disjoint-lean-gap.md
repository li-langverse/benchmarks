# Proof gap researcher — cycle 31 (G-par parallel disjoint Lean opaque stubs)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-7b / PH-7d-c / PH-2f · G-par, G-vc, G-dec, G-test-verify  
**Focus:** `parallel for` disjoint contracts (`disjoint_row`, `disjoint_elem`, `row_ok`) — AST policy vs Lean certificate  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** G-par — parallel iteration independence is enforced by **AST policy heuristics**, not Lean; AutoVC stubs all disjoint `requires` / `invariant` to `Prop := True` + `trivial`.
- **HYPOTHESIS: verified** — `expr_to_lean` Call handler translates only `abs()`; `disjoint_*` / `row_ok` fall through to opaque marker + `True`.
- **HYPOTHESIS: verified** — `good_disjoint_parallel.li` (`disjoint_row` + `row_ok`) and `parallel_with_disjoint.li` (`disjoint_elem`) both emit opaque par-loop VCs; no disjoint text in AutoVC.
- **HYPOTHESIS: verified** — `false_disjoint_proof.li` rejected at **policy** (E0350), not Lean — certificate would not catch a missed heuristic.
- **HYPOTHESIS: verified** — `@parallel(disjoint=disjoint_elem)` on proc does **not** inherit into nested loop VCs (`parallel_def_disjoint_inherit.li` — only `decreases` emitted).
- **HYPOTHESIS: verified** — `Core.lean` / `Discharge.lean` contain **no** disjoint semantics; manifest marks `good_disjoint_parallel` / `parallel_with_disjoint` as **`verify_ok`** despite trivial Lean.
- **Evidence extended:** `parallel_disjoint_lean_opaque_gap.sh` now covers decorator `disjoint_elem` path; script PASS.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `expr_to_lean` disjoint builtins | **Missing** — abs-only Call arm | `vc_emit_lean.cpp:224-231` |
| Par-loop `requires disjoint_*` | **Opaque + True stub** | AutoVC `vc_*_par0_requires_0` |
| Par-loop `invariant row_ok` | **Opaque + True stub** | AutoVC `vc_good_parallel_par0_invariant_0` |
| Decorator `@parallel(disjoint=...)` inherit | **Not wired to loop VCs** | `parallel_def_disjoint_inherit.li` AutoVC |
| Lean disjoint model | **Absent** | no matches in `Core.lean`, `Discharge.lean` |

**G-dec:** Decorator parse + policy present; MIR proc tags and Lean G-par discharge remain open (lic **#387**).

### 2. Contract gaps

- **G-par / P-par:** Safety relies on `policy_module.cpp` pattern checks (e.g. E0350 `disjoint_row` vs `grid[0][0]` write), not proof obligations in Lean.
- **G-vc:** Opaque fallback path identical to method-field requires gap (cycle 30) — untranslated Call → `True` + `trivial`.
- **G-test-verify:** `good_disjoint_parallel.li` and `parallel_with_disjoint.li` tiered **`verify_ok`** in `manifest.toml` while AutoVC carries no disjoint predicates.

### 3. Trusted surface

- No `trusted.lean` edits (policy). OpenMP runtime threading is outside Lean certificate scope.

### 4. External trust boundaries

- **Deferred:** Formal disjoint memory model in Lean (`Li.Discharge.disjoint_elem` etc.) — human RFC / PH-7d scope.
- **Deferred:** Whether decorator-inherited disjoint should auto-emit loop `requires` VCs (7d-c policy vs proof split).

### 5. Evidence pack

| Item | Location |
|------|----------|
| abs-only Call translation | `compiler/verify/vc_emit_lean.cpp:224-231` |
| Opaque contract fallback | `compiler/verify/vc_emit_lean.cpp:367-372` |
| AST disjoint policy (E0350) | `compiler/types/policy_module.cpp:183-188` |
| Prelude disjoint builtins | `compiler/types/prelude.cpp:36-37` |
| Explicit disjoint_row specimen | `li-tests/race_shared_memory/good_disjoint_parallel.li` |
| False proof (E0350) | `li-tests/race_shared_memory/false_disjoint_proof.li` |
| Decorator disjoint_elem | `li-tests/decorators/parallel_with_disjoint.li` |
| Inherit gap specimen | `li-tests/decorators/parallel_def_disjoint_inherit.li` |
| Gap repro script | `li-tests/tooling/parallel_disjoint_lean_opaque_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md` — **G-par** Partial |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/race_shared_memory/good_disjoint_parallel.li          # exit 0
./build/compiler/lic/lic check li-tests/race_shared_memory/false_disjoint_proof.li            # exit 1 E0350
./build/compiler/lic/lic build li-tests/race_shared_memory/good_disjoint_parallel.li -o /dev/null
./build/compiler/lic/lic build li-tests/decorators/parallel_with_disjoint.li -o /dev/null
./li-tests/tooling/parallel_disjoint_lean_opaque_gap.sh                                       # exit 0 PASS
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | `expr_to_lean` has no disjoint Call translation | `vc_emit_lean.cpp:224-231`; gap script static grep |
| **verified** | `disjoint_row` / `row_ok` par contracts → opaque + `True` | AutoVC lines 19-24 after `good_disjoint_parallel` build |
| **verified** | `disjoint_elem` decorator path same stub behavior | AutoVC lines 19-21 after `parallel_with_disjoint` build |
| **verified** | Bad disjoint proof caught by policy, not Lean | `false_disjoint_proof.li` → E0350 at `policy_module.cpp:183-188` |
| **verified** | Decorator inherit does not emit par requires VC | `parallel_def_disjoint_inherit.li` — no `par0_requires` in AutoVC |
| **verified** | No disjoint semantics in Lean semantics package | grep `Core.lean`, `Discharge.lean` — zero matches |
| **verified** | Manifest `verify_ok` overclaims for disjoint specimens | `manifest.toml:444-445`, `46-47` vs trivial AutoVC |
| **deferred** | Lean `disjoint_elem`/`disjoint_row` Props + discharge theorems | PH-7d / lic **#387** human scope |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-par: wire `disjoint_elem`/`disjoint_row`/`row_ok` into `expr_to_lean` + `Discharge.lean` | **lic** | `provability`, `PH-7d`, `G-par`, `#387` |
| Emit decorator-inherited `@parallel(disjoint=...)` as loop `requires` VCs | **lic** | `provability`, `PH-7d-c`, `G-dec` |
| Downgrade `good_disjoint_parallel` / `parallel_with_disjoint` to `verify_open_ok` until Lean wired | **lic** | `G-test-verify`, `li-tests` |
| Land extended `parallel_disjoint_lean_opaque_gap.sh` (decorator path) | **lic** | `provability`, `testing` |

**Related:** lic **#387** (PH-7d MIR proc tags + G-par Lean), cycle 30 method requires FieldAccess gap (same opaque pipeline).

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
- Full structured `disjoint=` proofs vs substring heuristics in legacy `policy.cpp` exploit corpus.
- `trusted.lean` — human gate only.
