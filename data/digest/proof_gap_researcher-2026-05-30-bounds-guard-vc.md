# Proof gap researcher — cycle 11 (G-bnd guarded refinement VC stub)

**Run:** `proof_gap_researcher-2026-05-30-bounds-guard-vc` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-bnd**, **P-refine** · **PH-2e, PH-2f**  
**north_star_fit:** provable pillar — bounds must be in Lean/codegen, not only C++ witnesses

## Executive summary

- Refinement index types (`Index10`, `NonNeg`) **typecheck** array access; plain `int` index **rejected** (E0201).
- AutoVC **erases** refinement to `Int` with **`Prop := True`** — no `0 <= i < 10` in Lean certificate.
- **Guarded** branch discharge (`if n >= 0: callee(n)`) also collapses call-site refine VC to **`True`** stub.
- Codegen: **`getelementptr inbounds` only**; **`li_bounds_fail` never called** (declare-only in IR).
- Contract tier retest: **`sqrt_open_bound`** still blocks default `lic build` (open VC gate works).
- CI guard **`bounds_refinement_lean_gap.sh`** landed and wired into **`contracts_discharge_corpus.sh`**.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-bnd:** No runtime bounds trap in codegen; safety relies entirely on typecheck + InBounds GEP UB semantics if typecheck is wrong.

### 2. Contract gaps

- **G-vc / P-refine:** `vc_emit_lean.cpp:546-551` witnesses satisfied refinements as `True` instead of emitting predicates like `n >= 0`.
- Proc-param refinement (`Index10`) not converted to entry VCs at all (`lean_type_name` strips refinement wrapper).

### 3. Trusted surface

- Unchanged; no `trusted.lean` edits.

### 4. External trust boundaries

- Human RFC for release bounds policy (debug trap vs proof-only) — see worktree `bounds-release-path.md`.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/bounds_refinement_lean_gap.sh` | exit 0 (gap documented) |
| `lic check li-tests/cve_patterns/cwe787_dyn_index.li` | exit 1, E0201 |
| `lic build li-tests/contracts_verify/sqrt_open_bound.li` | exit 1 (open VC) |
| `lic build li-tests/contracts_verify/refinement_guard_ok.li` | exit 0; AutoVC refine stub True |

**Key file:line:**

- `compiler/verify/vc_emit_lean.cpp:100-101` — refinement stripped in Lean type names
- `compiler/verify/vc_emit_lean.cpp:546-551` — witnessed refine → `True`
- `compiler/codegen/emit.cpp:916-922` — inbounds GEP, no bounds_fail call
- `compiler/types/typecheck.cpp:1203-1211` — compile-time index gate

## Hypothesis outcomes

- **HYPOTHESIS: verified** — Index10 erases to Int in AutoVC | evidence: `bounds_refinement_lean_gap.sh`
- **HYPOTHESIS: verified** — Guarded refine VC stubs True | evidence: AutoVC `vc_caller_guarded_call0_callee_refine_0`
- **HYPOTHESIS: verified** — No runtime li_bounds_fail in IR | evidence: `last_emit.ll`
- **HYPOTHESIS: falsified** — Lean carries index bound Props | evidence: AutoVC grep
- **HYPOTHESIS: verified (retest)** — sqrt_open_bound blocks default build | evidence: `lic build` exit 1

## Recommended issues/PRs

1. **lic:** `[G-bnd/P-refine] Emit real refinement Props to AutoVC` — labels: `provability`, `G-bnd`
2. **lic:** `[G-bnd] Discharge.lean index lemmas + ensures `a[i]` link` — labels: `provability`, `G-vc`
3. **lic:** Retire `bounds_refinement_lean_gap.sh` when gap closes

## Deferred

- G-net proxy seam (cycle 10 sibling branch)
- P-float sqrt_open_bound Lean discharge
- Release-mode IR bounds audit (worktree only)
