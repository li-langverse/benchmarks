# Proof gap researcher digest — 2026-05-29 (cycle 9)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-mat2-codegen-drift`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2f, PH-2i, PH-7e — proof-before-perf (mat2 certificate honesty)

## Executive summary

- **Focus:** G-lean / G-math **codegen↔Lean drift** for 2×2 float `@` — closed Lean certificate vs MIR `ArrayMatMul2DF64`.
- **Verified:** AutoVC ensures use `Li.Discharge.mat2_at2_eval`, not MIR return; `_proved` cites eval-only `mat2_at2_float_spec_proved` (`AutoVC.lean:14-15`, `Discharge.lean:55-58`).
- **Verified:** No `mir_return_linked` / codegen witness in AutoVC; gap is **certificate soundness scope**, not a runtime bug on the golden fixture.
- **Added:** `mat2_codegen_lean_drift.sh` + `mat2_at2_golden_2x2.li` in **lic** — encodes gap + runtime smoke.
- **`lic check` / build:** `mat2_codegen_lean_drift.sh` → ok; golden runtime exit 0.
- **No `trusted.lean` edits** (deferred to human RFC if axiom route).
- **Prior cycles (4–8):** bounds refinement VC, parallel decorator-for, sqrt contract tier, disjoint_elem, decorator policy bypass — not retested this pass.

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Ensures discharge eval, not `return A @ B` MIR | `vc_emit_lean.cpp:355-366` → `mat2_at2_eval` in Prop |
| MIR `@` → `ArrayMatMul2DF64` IKJ/FMA | `emit.cpp:1175-1195`, `253-278` |
| Lean proof closed on eval (`rfl`) | `Discharge.lean:46-58` |

### 2. Contract gaps

- **Operational gap:** `lic build` on `linalg_mat2_at2_float_closed.li` passes with zero open VCs while codegen refinement is unproved.
- **Not a float bug (this fixture):** runtime golden `[[19,22],[43,50]]` matches eval semantics.

### 3. Trusted surface

- `trusted.lean` unchanged (Net v1 axioms only).
- `mat2_at2_eval` is in proved `Discharge.lean`, not trusted axioms.

### 4. External trust boundaries

- **G-meta** closure needs MIR↔Lean equivalence proof or reviewed trusted codegen axiom — human decision outside this agent pass.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-lean** | `build/generated/AutoVC.lean:14-15` |
| **G-math** | `Discharge.lean:46-58` |
| **G-meta** | `emit.cpp:1175`; `mat2_codegen_lean_drift.sh` |
| **Runtime** | `math_linalg/mat2_at2_golden_2x2.li` → exit 0 |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — mat2_at2 VCs certify eval semantics not MIR | evidence: mat2_codegen_lean_drift.sh; AutoVC.lean:14`
- `HYPOTHESIS: verified — no codegen witness in AutoVC | evidence: mat2_codegen_lean_drift.sh grep`
- `HYPOTHESIS: falsified — runtime 2×2 @ diverges on golden fixture | evidence: mat2_at2_golden_2x2.li exit 0`
- `HYPOTHESIS: deferred — MIR refines mat2_at2_eval | evidence: G-meta Missing`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| test(provability): mat2_at2 codegen↔Lean drift harness | **lic** | `PH-2f`, `PH-2i`, provability |
| feat(G-meta): MIR ArrayMatMul2DF64 refinement witness for 2×2 float | **lic** | `PH-2f`, research |
| Close G-lean mat2_at2_eval row when codegen witness lands | **lic** | provability-gaps |
| Extend drift harness to IKJ loop path (k>24 unroll threshold) | **lic** | `PH-7e` |

## Deferred

- FMA/reassociation divergence under `-ffp-contract=fast` (not triggered on golden integers-as-floats).
- `sqrt_open_bound` P-float (cycle 6 — not retested).
- `@parallel` / `disjoint_elem` policy holes (cycles 7–8 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
