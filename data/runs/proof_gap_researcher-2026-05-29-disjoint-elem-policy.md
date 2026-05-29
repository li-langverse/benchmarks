# Proof gap researcher digest — 2026-05-29 (cycle 10)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-disjoint-elem-policy`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-7b, PH-7d-c — parallel disjointness before perf (G-par)

## Executive summary

- **Focus:** **G-par** — `disjoint_elem(i, buf)` does not justify every iteration writing `buf[0]`; policy only special-cases `disjoint_row` + `grid[0][0]`.
- **Verified:** `false_disjoint_elem_constant_index.li` (`parallel for`) still passes `lic check` (exit 0); control `false_disjoint_proof.li` still fails E0350.
- **Verified:** New specimen `false_disjoint_elem_decorator_constant_index.li` (`@parallel` on plain `for`) also passes `lic check` — same soundness hole on decorator path (**G-dec** interaction).
- **Root cause:** `check_stmt_parallel` rejects only `contract_uses_disjoint_row` + `par_body_writes_constant_grid00` (`policy_module.cpp:183-188`); no `buf[0]` analogue for `disjoint_elem`.
- **Harness:** `policy_disjoint_elem_soundness.sh` extended; run → ok.
- **No `trusted.lean` edits.**
- **Prior cycle 9 (mat2 codegen drift)** not retested this pass.

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| `disjoint_row` + `grid[0][0]` rejected (E0350) | `false_disjoint_proof.li` → `lic check` exit 1 |
| `disjoint_elem` + `buf[0]` accepted on `parallel for` | `false_disjoint_elem_constant_index.li` → exit 0 |
| `@parallel(disjoint=disjoint_elem)` `for` + `buf[0]` accepted | `false_disjoint_elem_decorator_constant_index.li` → exit 0 |
| Policy asymmetry | `policy_module.cpp:71-108`, `183-188` — only `par_body_writes_constant_grid00` |

### 2. Contract gaps

- Loop `requires disjoint_elem(i, buf)` is **syntax-checked** (prelude name) but **not semantically linked** to indexed writes in the body (no Lean **P-par** discharge).
- Decorator `disjoint=` on `Stmt::For` does not route through `check_stmt_parallel` (`policy_module.cpp:171-172` returns early for non-`ParallelFor`).

### 3. Trusted surface

- `trusted.lean` unchanged (Net v1 axioms only; `docs/semantics/trusted.lean:1-41`).
- Parallel safety is **policy heuristics**, not trusted axioms.

### 4. External trust boundaries

- Fixing the hole needs either **structured disjoint proofs** (Lean **P-par**) or a policy extension mirroring `grid[0][0]` detection for `buf[0]` — human RFC for false-positive rate on legitimate patterns.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-par** | `policy_module.cpp:183-188` |
| **G-par** | `false_disjoint_elem_constant_index.li:8-12` |
| **G-dec** | `false_disjoint_elem_decorator_constant_index.li:8-11` |
| **G-par control** | `false_disjoint_proof.li` → E0350 |
| **Harness** | `bash li-tests/tooling/policy_disjoint_elem_soundness.sh` → ok |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — disjoint_elem + buf[0] on parallel for passes lic check | evidence: lic check false_disjoint_elem_constant_index.li exit 0`
- `HYPOTHESIS: verified — disjoint_row + grid[0][0] still rejected | evidence: false_disjoint_proof.li E0350; policy_disjoint_elem_soundness.sh`
- `HYPOTHESIS: verified — decorator-for path shares constant-index hole | evidence: false_disjoint_elem_decorator_constant_index.li exit 0; policy_disjoint_elem_soundness.sh`
- `HYPOTHESIS: falsified — policy rejects all constant-index buf writes under disjoint_elem | evidence: policy_module.cpp only checks grid[0][0] for disjoint_row`
- `HYPOTHESIS: deferred — Lean proves iteration independence for disjoint_elem | evidence: G-par Partial; P-par open`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| fix(G-par): reject disjoint_elem + constant buf[0] write (mirror E0350 grid rule) | **lic** | `PH-7b`, `PH-7d-c`, provability |
| test(provability): decorator-for false_disjoint_elem constant index | **lic** | G-par, research |
| feat(P-par): Lean discharge for structured disjoint_elem proofs | **lic** | `PH-2f`, research |
| docs: align provability-gaps G-par row with buf[0] decorator specimen | **lic** | provability-gaps |

## Deferred

- **G-meta** mat2 MIR↔Lean refinement (cycle 9).
- **G-vc** `sqrt_open_bound` P-float contract tier (cycle 6 — not retested).
- **G-bnd** refinement AutoVC `True` stub (cycle 4 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
