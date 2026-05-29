# Proof gap researcher digest — 2026-05-29 (cycle 16)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-disjoint-elem-executable-race`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-7b, PH-7d-c — G-par disjoint_elem executable race surface

## Executive summary

- **Focus:** **G-par** — retest `disjoint_elem(i, buf)` + `buf[0]` constant-index hole with **codegen evidence** (not just `lic check` pass).
- **Verified:** Keyword `parallel for` specimen lowers to `__li_par_false_elem_proof_0` + `call li_omp_parallel_for_i64` — **executable data race** if run (OpenMP threads all increment `buf[0]`).
- **Verified:** Decorator `@parallel for` specimen passes `lic check` but **no** `__li_par_*` and **no** omp call — latent until 7d-b elaboration.
- **Verified:** Asymmetric policy — only `disjoint_row` + `grid[0][0]` rejected (E0350); no `buf[0]` analogue (`policy_module.cpp:102-108`, `183-188`).
- **Harness:** `policy_disjoint_elem_soundness.sh` extended with E0350 diagnostic + binary omp checks; manifest wired for both false specimens.
- **Retest:** Cycles 7/10 static policy findings **confirmed** with runtime lowering evidence.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| `disjoint_row` + `grid[0][0]` → E0350 | `false_disjoint_proof.li` → `lic check` exit 1 |
| `disjoint_elem` + `buf[0]` passes check | `false_disjoint_elem_constant_index.li` → exit 0 |
| Keyword path emits OpenMP worker | `nm` → `__li_par_false_elem_proof_0`; objdump → `call li_omp_parallel_for_i64` |
| Decorator path serial (no omp call) | `false_disjoint_elem_decorator_constant_index.li` build — no `__li_par_*`, no omp call |
| Policy only checks `grid[0][0]` shape | `par_body_writes_constant_grid00` hardcodes `grid` ident (`policy_module.cpp:95-108`) |

### 2. Contract gaps

- `requires disjoint_elem(i, buf)` is **not semantically linked** to indexed writes — policy accepts constant-index mutation that contradicts the proof intent.
- **Certificate honesty:** `lic build` + Lean typecheck succeed on keyword specimen with unused `buf`/`i` warnings in AutoVC — no bounds/disjoint Prop discharge (**P-par** open).
- Decorator path shares **policy** hole but is **not yet executable** — becomes a race surface when `@parallel for` elaborates (cycle 15 proc-inherit asymmetry compounds).

### 3. Trusted surface

- `trusted.lean` unchanged (Net v1 axioms only).
- Parallel safety remains AST policy heuristics, not trusted axioms or Lean **P-par** discharge.

### 4. External trust boundaries

- Immediate mitigation: extend `policy_module.cpp` with `par_body_writes_constant_buf0` mirror of grid rule — human review for false-positive rate.
- Structural fix: Lean **P-par** proofs for structured disjoint — deferred to **PH-2f** / lic#387.
- Block 7d-b `@parallel for` lowering until constant-index policy parity with keyword `parallel for`.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-par** | `policy_module.cpp:183-188` — disjoint_row-only constant-index guard |
| **G-par** | `false_disjoint_elem_constant_index.li:8-12` |
| **G-par** | `__li_par_false_elem_proof_0` + omp call in keyword build |
| **G-dec** | `false_disjoint_elem_decorator_constant_index.li:8-11` — serial build |
| **G-par control** | `false_disjoint_proof.li` → E0350 |
| **Harness** | `bash li-tests/tooling/policy_disjoint_elem_soundness.sh` → ok |
| **lic check** | `lic check li-tests/race_shared_memory/false_disjoint_elem_constant_index.li` → exit 0 |
| **lic build** | `lic build li-tests/race_shared_memory/false_disjoint_elem_constant_index.li -o /tmp/x` → omp worker emitted |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — keyword parallel for false_disjoint_elem lowers to OpenMP (executable race) | evidence: policy_disjoint_elem_soundness.sh; __li_par_false_elem_proof_0; objdump call li_omp_parallel_for_i64`
- `HYPOTHESIS: verified — decorator @parallel for same policy hole stays serial in codegen | evidence: false_disjoint_elem_decorator build — no __li_par_*; policy_disjoint_elem_soundness.sh`
- `HYPOTHESIS: verified — disjoint_row grid[0][0] still E0350 while disjoint_elem buf[0] passes | evidence: false_disjoint_proof.li; false_disjoint_elem_constant_index.li; policy_disjoint_elem_soundness.sh`
- `HYPOTHESIS: verified — policy asymmetry is grid-only par_body_writes_constant_grid00 | evidence: policy_module.cpp:95-108`
- `HYPOTHESIS: falsified — false_disjoint_elem is check-only gap with no parallel codegen | evidence: lic build + nm/objdump on keyword specimen`
- `HYPOTHESIS: deferred — Lean P-par discharge for disjoint_elem | evidence: proof-corpus-roadmap P-par open`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| fix(G-par): reject disjoint_elem + constant buf[0] write (mirror E0350 grid rule) | **lic** | `PH-7b`, `PH-7d-c`, provability |
| test(provability): extend policy_disjoint_elem harness with OpenMP race-surface checks | **lic** | G-par, research |
| Block 7d-b @parallel for lowering until constant-index disjoint policy parity | **lic** | G-dec, G-par, security |
| feat(P-par): Lean discharge linking disjoint_elem to indexed writes | **lic** | `PH-2f`, research |
| docs: provability-gaps G-par — note executable OpenMP on keyword path | **lic** | provability-gaps |

## Deferred

- **G-par / G-dec** proc `@parallel(disjoint=)` inherit asymmetry (cycle 15 — not retested).
- **G-net** recv/send triple drift (cycle 14 — not retested).
- **G-vc** `sqrt_open_bound` P-float (cycle 6 — not retested).
- **G-bnd** guarded refinement VCs (cycle 11 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
