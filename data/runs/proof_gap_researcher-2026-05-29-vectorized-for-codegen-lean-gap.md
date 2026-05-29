# Proof gap researcher digest — 2026-05-29 (cycle 19)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-vectorized-for-codegen-lean-gap`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-7d-c, PH-2f — G-dec / P-dec `@vectorized` on `for` codegen↔Lean drift

## Executive summary

- **Focus:** **G-dec / P-dec** — `@vectorized(lanes=4)` on plain `for` lowers to `ArraySimdScope` MIR and emits **f64×4** codegen while **AutoVC** carries only trivial `True` ensures (no SIMD correctness Prop).
- **Verified:** `lower.cpp:2028-2040` wraps decorated `for` bodies with `MirOp::ArraySimdScope` on/off.
- **Verified:** `emit.cpp:1251-1257` toggles `array_simd_scope_stack`; `emit.cpp:138-142` enables packed array ops inside scope.
- **Verified:** `vectorized_for_scope_ok.li` → `mulpd` in `li_user_main`; scalar control (same file minus decorator) → `mulsd` only.
- **Verified:** AutoVC for vectorized specimen has **no** vector/simd/lanes obligations; `vc_main_ensures_0 := True` + `trivial` discharge.
- **Verified:** `lic build` + Lean typecheck **pass** — certificate overclaims scoped SIMD equivalence to scalar semantics.
- **Harness:** `vectorized_for_scope_codegen_lean_gap.sh` + scalar control specimen; wired into `contracts_discharge_corpus.sh`.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| `@vectorized` on `for` → `ArraySimdScope` MIR | `lower.cpp:2028-2040` |
| Codegen scope stack gates f64×4 array ops | `emit.cpp:138-142`, `1251-1257` |
| Scoped SIMD in loop body (`mulpd`) | `objdump li_user_main` on `vectorized_for_scope_ok.li` |
| Scalar fallback without decorator (`mulsd`) | `vectorized_for_scope_scalar_ctrl.li`; harness contrast |
| Policy validates `lanes=4` only | `policy_module.cpp:157-162`, `242-247` |
| Docs stale: fast-math guide says `@vectorized on for` parse-only | `docs/guide/fast-math-and-parallelism.md:4` vs release note 7dc |

### 2. Contract gaps

- **P-dec open:** no Lean Prop that scoped `@vectorized for` preserves scalar array semantics (element-wise `*` inside `@no_vectorize` def).
- AutoVC emits only function-level `requires`/`ensures`/`decreases` **True** stubs — no loop-body or SIMD-scope VCs.
- `lic build` certificate is honest about *function* contracts but **silent** on decorator elaboration correctness (same honesty class as codegen↔Lean drift for `sqrt_open_bound` / `vec3_dot`).

### 3. Trusted surface

- `trusted.lean` unchanged — gap is MIR/codegen + missing **P-dec** lemmas, not axiom growth.

### 4. External trust boundaries

- Closing requires **P-dec** elaboration proofs (decorator → MIR ≡ spec) + optional runtime-free SIMD equivalence lemmas — human RFC/review; not `trusted.lean` without approval.
- LLVM/CPU f64×4 behavior remains under **G-hw** axiomatic limit.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-dec** | `lower.cpp:2028-2040` — `ArraySimdScope` on decorated `for` |
| **G-dec** (codegen) | `emit.cpp:138-142`, `1251-1257` — scope stack |
| **G-dec** / **P-dec** | `vectorized_for_scope_ok.li:14-16` — scoped vectorized for |
| **G-dec** (contrast) | `vectorized_for_scope_scalar_ctrl.li` — no decorator |
| **G-lean** | AutoVC — no vector/simd rows; `vc_main_ensures_0 := True` |
| **Harness** | `bash li-tests/tooling/vectorized_for_scope_codegen_lean_gap.sh` → ok |
| **lic check** | `lic check li-tests/decorators/vectorized_for_scope_ok.li` → exit 0 |
| **Corpus** | `bash li-tests/tooling/contracts_discharge_corpus.sh` (includes new harness) |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — @vectorized on for emits ArraySimdScope and mulpd codegen inside @no_vectorize def | evidence: vectorized_for_scope_codegen_lean_gap.sh; lower.cpp:2028-2040`
- `HYPOTHESIS: verified — same program without @vectorized on for uses scalar mulsd only | evidence: vectorized_for_scope_scalar_ctrl.li; harness`
- `HYPOTHESIS: verified — AutoVC has no vectorization/SIMD correctness obligations | evidence: grep AutoVC; vectorized_for_scope_codegen_lean_gap.sh`
- `HYPOTHESIS: verified — lic build + Lean typecheck pass with trivial True ensures | evidence: vectorized_for_scope_codegen_lean_gap.sh`
- `HYPOTHESIS: falsified — P-dec discharges scoped vectorized-for equivalence in Lean today | evidence: AutoVC grep; no _proved SIMD lemmas`
- `HYPOTHESIS: falsified — fast-math guide claim that @vectorized on for is parse-only still holds | evidence: 7dc release note + mulpd objdump`
- `HYPOTHESIS: deferred — close via P-dec MIR elaboration proofs + optional SIMD≡scalar lemmas | evidence: proof-corpus-roadmap P-dec row`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| test(provability): vectorized_for_scope_codegen_lean_gap regression harness | **lic** | G-dec, research |
| feat(P-dec): Lean VCs for @vectorized for ArraySimdScope ≡ scalar semantics | **lic** | PH-7d-c, P-dec |
| docs: align fast-math guide — @vectorized on for elaborates (7dc) | **lic** | G-dec, docs |
| docs: provability-gaps G-dec — cite vectorized-for codegen↔Lean drift harness | **lic** | provability-gaps |

## Deferred

- **G-vc** vec3 field opaque VC (cycle 18 — not retested).
- **G-vc** sqrt_open_bound codegen drift (cycle 17 — not retested).
- **G-par** disjoint_elem executable race (cycle 16 — not retested).
- **G-par/G-dec** decorator-for policy bypass (cycles 8/15 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
