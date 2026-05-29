# proof_gap_researcher — 2026-05-29 (G-bnd refinement Lean stub)

**Run:** `proof_gap_researcher-2026-05-29-bounds-refinement` · **Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f

Full digest: [lic session](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/research-sessions/provability_holes-cycle4-bounds-refinement-vc.md) · [whitepaper](https://github.com/li-langverse/research-findings/tree/main/whitepapers/2026-05/provability_holes/prov-r0-cycle4-bounds-refinement-vc-gap)

---

## Executive summary

- **Focus:** **G-bnd** / **P-refine** — refinement-typed indices (`Index10`) pass `lic build` but Lean AutoVC uses plain `Int` and `Prop := True`; codegen has no `li_bounds_fail`.
- **Typecheck fence verified:** raw `int` array index rejected (`cwe787_dyn_index.li` → E0201).
- **Soundness gap verified:** `index_refinement.li` AutoVC does not encode `0 <= i < 10`; `get` disassembly has no bounds call.
- **Call-site refinement:** `refinement_call_ok.li` emits `vc_caller_call0_callee_refine_0 := True` when witnessed (`vc_emit_lean.cpp:550-551`).
- **Doc drift fixed:** `provability-gaps.md` no longer implies `li_bounds_fail` may run today.
- **CI guard:** `bounds_refinement_lean_gap.sh` documents gap until real Lean bounds land.
- **Contract tier (retest):** `sqrt_open_bound.li` build exit 1 without `--allow-open-vc`.
- **Trusted surface:** unchanged — no `trusted.lean` edits.

## Deliverable / findings

### 1. Compiler / semantics gaps

- Refinement indices compile to unchecked LLVM GEP (`emit.cpp:896-922`).
- `li_bounds_fail` exists in `li_rt` but is **not** emitted from user `get` (`objdump` + guard script).

### 2. Contract gaps

- Proc-param refinements not translated to Lean (`AutoVC.lean` lines 12-13).
- Witnessed call-site refinements forced to `True` in `vc_emit_lean.cpp:550-551`.

### 3. Trusted surface

- `lic/docs/semantics/trusted.lean` — IO/Net axioms only.

### 4. External trust boundaries

- **P-refine** closure needs `Discharge.lean` lemmas (human review), not new trusted axioms.

### 5. Evidence pack

| G-* | Repro |
|-----|--------|
| **G-bnd** | `bash li-tests/tooling/bounds_refinement_lean_gap.sh` → ok |
| **G-vc** | `grep vc_get_requires_0 build/generated/AutoVC.lean` after `index_refinement` build |
| **G-bnd** | `lic check li-tests/cve_patterns/cwe787_dyn_index.li` → E0201 |
| **G-lean** | `lic build li-tests/contracts_verify/sqrt_open_bound.li` → exit 1 |

### Hypothesis outcomes

- `HYPOTHESIS: verified — refinement Index10 builds with AutoVC requires := True | evidence: AutoVC.lean:12-13`
- `HYPOTHESIS: verified — get does not call li_bounds_fail | evidence: bounds_refinement_lean_gap.sh`
- `HYPOTHESIS: falsified — codegen emits li_bounds_fail for refinement access | evidence: emit.cpp declare-only`
- `HYPOTHESIS: falsified — dynamic int index compiles | evidence: cwe787_dyn_index E0201`
- `HYPOTHESIS: verified — witnessed call-site refine VC is True | evidence: refinement_call_ok AutoVC; vc_emit_lean.cpp:550-551`
- `HYPOTHESIS: deferred — inbounds GEP is sufficient safety | evidence: no Lean bound proof path`

## Recommended issues/PRs

| Repo | Title | Labels |
|------|-------|--------|
| `lic` | feat(G-bnd/P-refine): emit refinement bounds to AutoVC and Discharge | `area:compiler`, `provability`, `G-bnd`, `PH-2e` |
| `lic` | research(provability): cycle 4 bounds refinement Lean gap + guard | `research`, `provability_holes` |
| `research-findings` | whitepaper prov-r0-cycle4-bounds-refinement-vc-gap | `research`, `provability_holes` |

## Deferred

- **G-par** disjoint_row policy (cycle 3 whitepaper; lic PR pending).
- **G-meta** mat2 MIR vs `mat2_at2_eval` (cycle 2).
- **P-float** `sqrt_open_bound` closure.
- Split **G-test-verify** `prove_lean_ok` manifest outcome.
