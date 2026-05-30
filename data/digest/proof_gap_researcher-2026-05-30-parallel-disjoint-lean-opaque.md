# Proof gap researcher — cycle 25 (G-par disjoint Lean opaque stubs)

**Run:** `proof_gap_researcher-2026-05-30-parallel-disjoint-lean-opaque` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-par**, **P-par** · **PH-7b, PH-7d-c, PH-2f** (lic **#387**)  
**north_star_fit:** provable pillar — parallel disjointness must appear in Lean certificate, not only policy heuristics

## Executive summary

- `parallel for` `requires disjoint_row` / `invariant row_ok` emit **`Prop := True`** with **`trivial`** discharge and `/-! VC … (opaque) -/` comments — no disjoint semantics in certificate.
- Root cause: `expr_to_lean` **Call** branch translates only **`abs`**; `disjoint_elem`, `disjoint_row`, `row_ok` are untranslated (`vc_emit_lean.cpp:224-231`).
- **No** disjoint definitions in `Core.lean` or `Discharge.lean` — P-par Lean corpus absent (complements cycles 3/7 policy holes).
- `@parallel(disjoint=disjoint_elem)` on `def` **without** loop-level `requires` emits **no** `_par0_requires_*` VC at all (`parallel_def_disjoint_inherit.li`).
- `check-autovc-open-goals.sh` passes — certificate looks closed while disjointness is not encoded (**G-test-verify** honesty).
- CI guard **`parallel_disjoint_lean_opaque_gap.sh`** added; wired into **`contracts_discharge_corpus.sh`**.
- Policy still catches some bad patterns (cycles 3/7); Lean layer is separate backlog for #387.

## Deliverable / findings

### 1. Compiler / semantics gaps

- Parallel loop contracts reach AutoVC via `_parN` suffix (`vc_emit_lean.cpp:642-648`) but untranslatable exprs fall through to default **`prop = "True"`** (`367-373`, `411-416`).
- Decorator-inherited disjoint is **policy-only** (`policy_module.cpp:174-176`); not injected into `par_contracts` for VC emission.

### 2. Contract gaps

- **G-par / P-par:** User-facing `requires disjoint_*` is syntactic proof surface today; Lean certificate does not carry disjoint Prop.
- **Contrast:** `mat2_at2_float_spec` and `dot4` loop witness paths show how discharge *should* wire — no parallel analogue exists.

### 3. Trusted surface

- Unchanged; no `trusted.lean` edits.

### 4. External trust boundaries

- Human issue **lic#387** — catalog G-par Lean obligations (`disjoint_elem_spec`, array index disjointness) before `trusted.lean` / `Core.lean` growth.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/parallel_disjoint_lean_opaque_gap.sh` | exit 0 |
| `./li-tests/tooling/contracts_discharge_corpus.sh` | exit 0 |
| `lic build li-tests/race_shared_memory/good_disjoint_parallel.li` | exit 0; `vc_good_parallel_par0_requires_0 : Prop := True` |
| `lic build li-tests/decorators/parallel_def_disjoint_inherit.li` | exit 0; no `par0_requires` VC |
| `lic check li-tests/race_shared_memory/good_disjoint_parallel.li` | exit 0 |

**Key file:line:**

- `compiler/verify/vc_emit_lean.cpp:224-231` — Call → only `abs` translated
- `compiler/verify/vc_emit_lean.cpp:343-373, 411-416` — opaque → `True` + `trivial`
- `compiler/verify/vc_emit_lean.cpp:642-648` — `_parN` loop contract walk
- `compiler/types/policy_module.cpp:174-181` — disjoint required at policy, not Lean
- `build/generated/AutoVC.lean` (good_disjoint_parallel) — opaque requires/invariant stubs
- `li-tests/race_shared_memory/good_disjoint_parallel.li` — specimen with explicit disjoint_row + row_ok

## Hypothesis outcomes

- **HYPOTHESIS: verified** — `disjoint_row`/`row_ok` parallel requires emit `Prop := True` with trivial proof | evidence: `parallel_disjoint_lean_opaque_gap.sh`
- **HYPOTHESIS: verified** — `expr_to_lean` does not translate disjoint builtins | evidence: `vc_emit_lean.cpp:224-231`
- **HYPOTHESIS: verified** — No disjoint semantics in `Core.lean`/`Discharge.lean` | evidence: script grep + manual read
- **HYPOTHESIS: verified** — Decorator-inherited disjoint emits no par requires VC | evidence: `parallel_def_disjoint_inherit.li` AutoVC grep
- **HYPOTHESIS: falsified** — Open AutoVC goals flag disjoint stub gap | evidence: `check-autovc-open-goals.sh` exit 0 on good_disjoint_parallel
- **HYPOTHESIS: deferred** — Policy soundness for `grid[i][0]` / `buf[0]` | evidence: cycles 3/7; separate from Lean layer

## Recommended issues/PRs

1. **lic:** `[#387 / G-par] Add Discharge.disjoint_elem_spec + emit from vc_emit_lean for par requires` — labels: `provability`, `G-par`, `P-par`
2. **lic:** Inject decorator `@parallel(disjoint=…)` into AutoVC as synthetic par requires | labels: `provability`, `G-par`, `7d-c`
3. **lic:** Retire `parallel_disjoint_lean_opaque_gap.sh` when Lean Props wired | labels: `provability`, `G-test-verify`

## Deferred

- lic#472 P-linalg dot4 Discharge wiring (cycle 24)
- Policy constant-index holes (cycles 3/7) — compile_fail manifest when AST guard extended
- `matmul_loop_codegen_witness_gap.sh` — llvm-dis infra
