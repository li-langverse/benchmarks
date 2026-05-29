# proof_gap_researcher — 2026-05-29 (G-dec @parallel on plain `for`)

**Run:** `proof_gap_researcher-2026-05-29-parallel-decorator-for` · **Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f, PH-7d

Full digest: [lic session](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/research-sessions/provability_holes-cycle5-parallel-decorator-for.md) · [whitepaper](https://github.com/li-langverse/research-findings/tree/main/whitepapers/2026-05/provability_holes/prov-r0-cycle5-parallel-decorator-for-gap)

---

## Executive summary

- **Focus:** **G-dec / 7d-b** — `@parallel` on plain `for` parses as serial `Stmt::For`; no `OmpParallelFor` / `__li_par_*` worker (contrast `parallel for` keyword).
- **Elaboration gap verified:** `parallel_decorator_for_elaboration_gap.sh` — decorator-for binary has no omp call in `li_user_main`.
- **Policy gap verified:** `@parallel` on `for` without `disjoint=` passes `lic check` (`parallel_decorator_on_for_no_disjoint.li`).
- **Contrast:** `@vectorized` on `for` **does** emit `ArraySimdScope` (`lower.cpp:2028-2040`).
- **Parser split:** `parallel for` → `ParallelFor` (`parser.cpp:787-841`); `@parallel` + `for` → `For` (`parser.cpp:843-846`).
- **Register updated:** `provability-gaps.md` **G-dec** row cites guard + specimens.
- **Trusted surface:** unchanged — no `trusted.lean` edits.
- **Retest (contract tier):** `sqrt_open_bound.li` still fails build without `--allow-open-vc` (unchanged).

## Deliverable / findings

### 1. Compiler / semantics gaps

- Decorator-first syntax suggests parallelism; MIR/codegen runs a serial counted loop.
- `li_omp_parallel_for_i64` may appear in `.symtab` from `li_rt` link but is **not** called from user `main` path for decorator-for.

### 2. Contract gaps

- Parallel disjoint policy not applied to decorated `for` (`policy_module.cpp:171-172`).

### 3. Trusted surface

- `lic/docs/semantics/trusted.lean` — IO/Net axioms only.

### 4. External trust boundaries

- OpenMP runtime in `li_rt` is trusted execution substrate; gap is **elaboration**, not new axioms.

### 5. Evidence pack

| G-* | Repro |
|-----|--------|
| **G-dec** | `bash li-tests/tooling/parallel_decorator_for_elaboration_gap.sh` → ok |
| **G-dec** | `lic check li-tests/decorators/parallel_decorator_on_for_serial.li` → exit 0 |
| **G-dec** | `lic check li-tests/decorators/parallel_decorator_on_for_no_disjoint.li` → exit 0 |
| **G-lean** (retest) | `lic build li-tests/contracts_verify/sqrt_open_bound.li` → exit 1 without flag |

### Hypothesis outcomes

- `HYPOTHESIS: verified — @parallel on plain for stays serial in codegen | evidence: parallel_decorator_for_elaboration_gap.sh`
- `HYPOTHESIS: verified — parallel for keyword lowers to OpenMP | evidence: parallel_float_zero __li_par_main_0`
- `HYPOTHESIS: verified — @parallel on for without disjoint passes check | evidence: parallel_decorator_on_for_no_disjoint.li`
- `HYPOTHESIS: falsified — @parallel on for emits __li_par_* | evidence: nm/objdump on serial specimen`
- `HYPOTHESIS: deferred — Lean VCs for decorator-for | evidence: no AutoVC par hooks on For stmt`

## Recommended issues/PRs

| Repo | Title | Labels |
|------|-------|--------|
| `lic` | feat(G-dec/7d-b): elaborate @parallel on for to ParallelFor / OmpParallelFor | `area:compiler`, `provability`, `G-dec`, `PH-7d` |
| `lic` | fix(G-dec): policy-check disjoint on @parallel decorated for loops | `area:compiler`, `provability`, `G-dec` |
| `lic` | research(provability): cycle 5 parallel decorator-for gap + CI guard | `research`, `provability_holes` |
| `research-findings` | whitepaper prov-r0-cycle5-parallel-decorator-for-gap | `research`, `provability_holes` |

## Deferred

- **G-par** disjoint_row `grid[i][0]` policy (cycle 3).
- **G-bnd** refinement Lean bounds (cycle 4).
- **G-meta** mat2 codegen drift (cycle 2).
- **P-float** `sqrt_open_bound` closure.
