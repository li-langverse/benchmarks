# Proof gap researcher digest — 2026-05-29 (cycle 15)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-proc-disjoint-decorator-asymmetry`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-7b, PH-7d-c — G-par / G-dec proc disjoint inheritance honesty

## Executive summary

- **Focus:** **G-par / G-dec** — proc-level `@parallel(disjoint=)` inheritance asymmetry between `parallel for` and `@parallel` on plain `for`.
- **Verified:** `policy_module.cpp:171-172` returns early unless `stmt.kind == ParallelFor`; `proc_has_parallel_disjoint` never consulted for `Stmt::For`.
- **Verified:** `@parallel(disjoint=disjoint_elem)` on `def` satisfies nested `parallel for` without per-loop disjoint (`parallel_def_disjoint_inherit.li` → ok).
- **Verified:** Same proc decorator does **not** satisfy or enforce policy on nested `@parallel for` without loop-level disjoint — passes `lic check` (hole).
- **Verified:** Proc-level disjoint + `@parallel for` + outer `var` mutation still passes — capture guard also skips `Stmt::For` (`policy_module.cpp:200-203`).
- **Harness:** `parallel_def_disjoint_inherit_decorator_gap.sh` + two new decorator specimens; manifest updated.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Policy only on `ParallelFor` AST node | `policy_module.cpp:171-172`, `200-203` |
| Proc disjoint wired via `walk_stmts(..., proc_disjoint)` | `policy_module.cpp:257-260` |
| `@parallel for` is `Stmt::For` — early return before disjoint/capture checks | `check_stmt_parallel` / `check_stmt_parallel_capture` |
| Nested `parallel for` without proc disjoint rejected E0320 | harness temp specimen → exit 1 |

### 2. Contract gaps

- **Documented 7d partial:** release notes claim proc `@parallel(disjoint=)` inherits to nested `parallel for` only — **not** to decorated `for` (`2026-05-22-7d-7e-bench-parallel.md:17`).
- **Semantic hole:** Authors may assume proc-level disjoint covers all parallel loops in the body; `@parallel for` path bypasses both disjoint requirement and mut-capture guard.
- **Elaboration gap (related):** `@parallel for` stays serial (`parallel_decorator_for_elaboration_gap.sh`) — policy bypass is currently latent but will become a race surface when 7d-b lowers decorator-for.

### 3. Trusted surface

- No change to `trusted.lean` (Net v1 axioms unchanged).
- Gap is AST policy routing, not trusted axiom drift.

### 4. External trust boundaries

- Fix requires **lic** `policy_module.cpp` to run parallel guards on decorated `for` (or reject `@parallel for` until elaboration) — human review under **lic#387** / PH-7d-c.
- When decorator-for lowers to OpenMP, unsound specimens (`parallel_def_disjoint_decorator_mut_capture.li`) become executable races — prioritize before 7d-b ship.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-par** | `policy_module.cpp:171-176` — `proc_has_parallel_disjoint` only on `ParallelFor` |
| **G-par** | `policy_module.cpp:200-203` — capture guard same early return |
| **G-par** | `parallel_def_disjoint_inherit.li` — proc→keyword inherit (control) |
| **G-par** / **G-dec** | `parallel_def_disjoint_inherit_decorator_for.li` — proc disjoint + `@parallel for` passes |
| **G-par** / **G-dec** | `parallel_def_disjoint_decorator_mut_capture.li` — mut capture passes |
| **Harness** | `bash li-tests/tooling/parallel_def_disjoint_inherit_decorator_gap.sh` → ok |
| **Related** | `bash li-tests/tooling/parallel_decorator_policy_capture_gap.sh` → ok |
| **lic check** | `lic check li-tests/decorators/parallel_def_disjoint_inherit_decorator_for.li` → exit 0 |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — proc @parallel(disjoint=) satisfies nested parallel for without loop disjoint | evidence: parallel_def_disjoint_inherit.li; parallel_def_disjoint_inherit_decorator_gap.sh`
- `HYPOTHESIS: verified — proc disjoint does not apply to nested @parallel for (Stmt::For early return) | evidence: policy_module.cpp:171-172; parallel_def_disjoint_inherit_decorator_for.li exit 0`
- `HYPOTHESIS: verified — proc disjoint does not enable capture guard on @parallel for | evidence: policy_module.cpp:200-203; parallel_def_disjoint_decorator_mut_capture.li exit 0`
- `HYPOTHESIS: verified — nested parallel for without proc disjoint still fails E0320 | evidence: harness temp specimen exit 1`
- `HYPOTHESIS: falsified — proc disjoint causes E0320 on @parallel for without loop disjoint | evidence: parallel_def_disjoint_inherit_decorator_for.li lic check exit 0`
- `HYPOTHESIS: deferred — extend proc inherit to decorated for when 7d-b elaborates | evidence: requires policy_module refactor + compile_fail specimens; lic#387`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| feat(G-par/G-dec): apply proc_disjoint + capture guards to @parallel `for` | **lic** | `PH-7d`, G-par, G-dec, lic#387 |
| test(provability): proc disjoint inherit asymmetry harness | **lic** | G-par, research |
| docs: provability-gaps — proc inherit scope (keyword vs decorator-for) | **lic** | provability-gaps |
| Block 7d-b decorator-for lowering until policy parity with parallel for | **lic** | G-dec, security |

## Deferred

- **G-net** recv/send triple drift (cycle 14 — not retested).
- **G-test-verify** manifest `verify_ok` split (cycle 13 — not retested).
- **G-vc** `sqrt_open_bound` P-float (cycle 6 — not retested).
- **G-par** `disjoint_elem` + `buf[0]` constant-index hole (cycle 10 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
