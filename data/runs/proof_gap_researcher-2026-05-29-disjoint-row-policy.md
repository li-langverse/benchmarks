# proof_gap_researcher — 2026-05-29 (G-par disjoint_row policy)

**Run:** `proof_gap_researcher-2026-05-29-disjoint-row` · **Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f

Full digest: [lic session](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/research-sessions/provability_holes-cycle3-disjoint-row-policy.md) · [whitepaper](https://github.com/li-langverse/research-findings/tree/main/whitepapers/2026-05/provability_holes/prov-r0-cycle3-disjoint-row-policy-gap)

---

## Executive summary

- **Focus:** **G-par** — `policy_module` only rejects `disjoint_row` when the parallel body writes **`grid[0][0]`**, not **`grid[i][0]`** (loop-indexed row).
- **Soundness hole verified in-repo:** `disjoint_row_writes_row_i.li` passes `lic check`; `false_disjoint_proof.li` still correctly fails with **E0350**.
- **Contract tier (retest):** `sqrt_open_bound.li` fails `lic build` without `--allow-open-vc`; `LI_ALLOW_OPEN_VC` env is ignored (`main.cpp:243-244`).
- **New CI guard:** `policy_disjoint_row_soundness.sh` documents the gap until policy is fixed (then script fails to prompt manifest flip).
- **Register updated:** `provability-gaps.md` **G-par** row cites the specimen and guard script.
- **Trusted surface:** unchanged — no `trusted.lean` edits; Net v1 axioms only (`trusted.lean:20-39`).
- **Codegen↔Lean:** not in scope this step (cycle 2 mat2 drift documented separately).
- **Tests:** `race_shared_memory` suite **8/0** pass including new `compile_open_ok` manifest entry.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-par partial:** `check_stmt_parallel` at `policy_module.cpp:183-188` calls `par_body_writes_constant_grid00`, which only matches literal index `0` on `grid`, not `grid[i][…]` when `i` is the parallel loop index.
- Parallel iterations writing the same column `grid[*][0]` are a **data race**; `disjoint_row(i, grid)` does not justify it.

### 2. Contract gaps

- **G-lean / open VC:** strict CLI-only downgrade confirmed (see hypotheses below).
- **G-vc:** `sqrt_open_bound` remains intentionally open; unchanged.

### 3. Trusted surface

- `lic/docs/semantics/trusted.lean` — IO/Net axioms only; no parallel/disjoint axioms added (human-approved RFC required for growth).

### 4. External trust boundaries

- Fixing `disjoint_row` semantics may need a **Lean spec** in `Discharge.lean` (deferred); policy fix is in-scope for `lic` without `trusted.lean` change.

### 5. Evidence pack

| G-* | Repro |
|-----|--------|
| **G-par** | `lic check li-tests/race_shared_memory/disjoint_row_writes_row_i.li` → exit 0 |
| **G-par** (contrast) | `lic check li-tests/race_shared_memory/false_disjoint_proof.li` → E0350 |
| **G-lean** | `lic build li-tests/contracts_verify/sqrt_open_bound.li` → exit 1 without flag |

### Hypothesis outcomes

- `HYPOTHESIS: verified — disjoint_row + grid[i][0] is accepted by lic check | evidence: disjoint_row_writes_row_i.li exit 0`
- `HYPOTHESIS: verified — disjoint_row + grid[0][0] is rejected | evidence: false_disjoint_proof.li E0350, policy_module.cpp:183-188`
- `HYPOTHESIS: verified — open VC requires --allow-open-vc on CLI | evidence: sqrt_open_bound build exit 1; LI_ALLOW_OPEN_VC warned and ignored`
- `HYPOTHESIS: falsified — policy rejects all unsound disjoint_row bodies | evidence: row-i specimen compiles`
- `HYPOTHESIS: deferred — Lean-backed disjoint_row soundness | evidence: no Discharge lemma; G-par Partial`

## Recommended issues/PRs

| Repo | Title | Labels |
|------|-------|--------|
| `lic` | fix(G-par): reject disjoint_row when body writes grid[i][…] not only grid[0][0] | `area:compiler`, `provability`, `G-par` |
| `lic` | research(provability): cycle 3 disjoint_row policy gap + CI guard | `research`, `provability_holes` |

## Deferred

- Lean `disjoint_row` / `disjoint_elem` semantics and **G-meta** MIR preservation (cycle 2 mat2).
- `sqrt_open_bound` / **P-float** closure.
- Full `contracts_discharge_corpus.sh` on this devbox (`discharge_trivial_lean` witness comment drift — pre-existing).
