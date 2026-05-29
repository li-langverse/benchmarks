# Proof gap researcher digest — 2026-05-29 (cycle 11)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-bounds-refinement-guard-vc`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f, PH-3 — bounds/refinement before release (G-bnd)

## Executive summary

- **Focus:** **G-bnd / P-refine** — refinement-typed indices and guarded call-site proofs pass typecheck, but Lean AutoVC and codegen omit real bounds obligations.
- **Verified:** `index_refinement.li` builds with `vc_get_requires_0 := True` and plain `i : Int` (`AutoVC.lean:12-13`); `get` codegen has no `li_bounds_fail` call.
- **Verified (new):** `refinement_guard_ok.li` path-proves `NonNeg` at typecheck (`if n >= 0: callee(n)`) yet AutoVC emits `vc_caller_guarded_call0_callee_refine_0 := True` — certificate does not encode the guard predicate.
- **Verified:** Raw `int` array index still rejected (E0201 on `cwe787_dyn_index.li`); literal refinement violation rejected (E0305 on `refinement_call_fail.li`).
- **Harness:** `bounds_refinement_lean_gap.sh` extended for guarded call-site stub; run → ok.
- **Retest:** `sqrt_open_bound_contract_tier.sh` → ok (G-vc P-float still intentionally open).
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Refinement param lowers to plain `int` in Lean VC | `AutoVC.lean:12` — `vc_get_requires_0 (a : LiArray Int 10) (i : Int) : Prop := True` |
| Codegen `get` uses stack spill + indexed load, no bounds trap | `objdump -d get @ 0x1240`; no `li_bounds_fail` in disassembly |
| `li_bounds_fail` declared but unused in codegen | `emit.cpp:1275` — symbol linked from `li_rt.c:16` only |
| Typecheck blocks raw `int` index | `cwe787_dyn_index.li` → E0201 (`typecheck.cpp:1211-1215`) |

### 2. Contract gaps

- **Param refinement:** `Index10` on `get(i: Index10)` does not emit `0 <= i ∧ i < 10` in AutoVC — all requires/ensures stubbed `True`.
- **Call-site refinement (literal):** `refinement_call_ok.li` → witnessed VC `True` (`vc_emit_lean.cpp:550-551`).
- **Call-site refinement (guarded):** `refinement_guard_ok.li` → typecheck uses path facts for `callee(n)` inside `if n >= 0`, but Lean still emits `vc_caller_guarded_call0_callee_refine_0 := True` with `trivial` proof — **P-refine** gap for conditional witnesses.
- **`lic build` certificate:** `index_refinement.li` and `refinement_guard_ok.li` both pass full build + Lean typecheck with zero open goals despite missing bounds Props.

### 3. Trusted surface

- `trusted.lean` unchanged (Net/IO axioms only, `docs/semantics/trusted.lean:1-41`).
- Bounds gap is compiler VC emission, not trusted axiom growth.

### 4. External trust boundaries

- Closing **P-refine** requires Lean lemmas in `Discharge.lean` for refinement predicates and path-sensitive call-site VCs — human-reviewed, not `trusted.lean` expansion.
- LLVM `inbounds` GEP is not wired for refinement indices today; unsound FFI/cast bypass is out of scope for this specimen.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-bnd** | `index_refinement.li:1-8` → `AutoVC.lean:12-13` |
| **G-bnd** | `emit.cpp:1275`; `objdump get` — no `li_bounds_fail` |
| **G-vc** / **P-refine** | `refinement_guard_ok.li:15-16` → `AutoVC.lean:31-32` |
| **G-vc** / **P-refine** | `vc_emit_lean.cpp:550-551` — witnessed → `prop = "True"` |
| **G-bnd** (negative) | `lic check li-tests/cve_patterns/cwe787_dyn_index.li` → E0201 |
| **G-vc** (retest) | `bash li-tests/tooling/sqrt_open_bound_contract_tier.sh` → ok |
| **Harness** | `bash li-tests/tooling/bounds_refinement_lean_gap.sh` → ok |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — Index10 param builds with AutoVC requires := True and i : Int | evidence: AutoVC.lean:12-13; bounds_refinement_lean_gap.sh`
- `HYPOTHESIS: verified — codegen get does not call li_bounds_fail | evidence: objdump get @ 0x1240; bounds_refinement_lean_gap.sh`
- `HYPOTHESIS: verified — guarded if-branch refinement passes lic check but Lean VC is True stub | evidence: refinement_guard_ok.li exit 0; AutoVC.lean:31-32; bounds_refinement_lean_gap.sh`
- `HYPOTHESIS: falsified — dynamic int index compiles | evidence: cwe787_dyn_index.li E0201`
- `HYPOTHESIS: falsified — lic build emits li_bounds_fail on refinement-indexed access | evidence: emit.cpp declares only; objdump`
- `HYPOTHESIS: deferred — Lean certificate encodes path-sensitive NonNeg guard | evidence: vc_emit_lean.cpp:550-551; P-refine open`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| feat(P-refine): emit real Lean Props for refinement params (Index10 bounds) | **lic** | `PH-2e`, `PH-2f`, provability |
| feat(P-refine): path-sensitive call-site refinement VCs (guarded NonNeg) | **lic** | `PH-2e`, research |
| test(provability): extend bounds_refinement_lean_gap for guarded refine stub | **lic** | G-bnd, research |
| docs: align provability-gaps G-bnd row with guarded refinement_guard_ok specimen | **lic** | provability-gaps |
| feat(G-bnd): wire li_bounds_fail or proved inbounds GEP for dynamic refinement lowering | **lic** | `PH-3`, numerics |

## Deferred

- **G-par / G-dec** `@parallel` decorator-for mut/borrow policy bypass (`parallel_decorator_policy_capture_gap.sh` — not retested in depth this pass).
- **G-par** `disjoint_elem` + `buf[0]` hole (cycle 10 — not retested).
- **G-meta** mat2 MIR↔Lean codegen drift (cycle 9 — not retested).
- **G-vc** `sqrt_open_bound` P-float closure (retested — still open).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
