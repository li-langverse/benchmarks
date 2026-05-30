# Proof gap researcher — cycle 24 (P-linalg dot4 loop ensures True stub)

**Run:** `proof_gap_researcher-2026-05-30-dot4-loop-ensures-stub` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-vc**, **G-lean**, **P-linalg** · **PH-2i, PH-2f** (#472)  
**north_star_fit:** provable pillar — loop implementations must appear in Lean certificate, not only C++ witnesses

## Executive summary

- `witness_dot4_int_loop` recognizes the 4-iteration `while` dot shape in `vc_witness.cpp` but AutoVC still emits **`vc_dot4_int_loop_ensures_0 : Prop := True`**.
- `Discharge.lean` defines `dot4_int_spec` / `dot4_loop_eval` / `dot4_int_loop_eval_spec` (rfl) — **not referenced** from generated AutoVC.
- **Contrast:** `linalg_mat2_at2_float_closed.li` wires **`Li.Discharge.mat2_at2_float_spec`** in AutoVC (`vc_emit_lean.cpp:401-406`).
- Filename suffix `_open` means **P-loop backlog** (ensures absent from certificate), **not** open Lean goals — `check-autovc-open-goals.sh` passes.
- CI guard **`dot4_loop_ensures_lean_stub_gap.sh`** added; wired into **`contracts_discharge_corpus.sh`**.
- Tier-1 IKJ matmul (`matmul_loop_codegen_witness_gap.sh`) still needs `llvm-dis` on this host — deferred infra fix.

## Deliverable / findings

### 1. Compiler / semantics gaps

- Static loop witness checks MIR/source shape only; no codegen↔Lean link for loop eval vs closed-form `ensures`.

### 2. Contract gaps

- **G-vc / P-linalg:** Witnessed `ensures` contracts collapse to `prop = "True"` when `contract_witnessed_trivial` (`vc_emit_lean.cpp:351-354, 411-416`) except `mat2` discharge path.
- Closed-form `dot4_int` (no loop) has the **same** True stub — certificate does not carry `dot4_int_spec` either.

### 3. Trusted surface

- Unchanged; no `trusted.lean` edits.

### 4. External trust boundaries

- Human issue **lic#472** — wire loop/matmul specimens like mat2 `@` before claiming P-linalg closed.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/dot4_loop_ensures_lean_stub_gap.sh` | exit 0 |
| `lic build li-tests/contracts_verify/linalg_dot4_int_loop_open.li` | exit 0; ensures `Prop := True` |
| `lic build li-tests/contracts_verify/linalg_mat2_at2_float_closed.li` | exit 0; `mat2_at2_float_spec` in AutoVC |
| `lic check li-tests/contracts_verify/linalg_dot4_int_loop_open.li` | exit 0 |

**Key file:line:**

- `compiler/verify/vc_witness.cpp:459-492` — `witness_dot4_int_loop_impl`
- `compiler/verify/vc_emit_lean.cpp:351-354, 391-393, 411-416` — witnessed → True; loop comment only
- `compiler/verify/vc_emit_lean.cpp:401-406` — mat2 contrast (`mat2_at2_float_spec`)
- `docs/semantics/Discharge.lean:24-32` — `dot4_int_spec`, `dot4_int_loop_eval_spec` (unused by AutoVC)
- `li-tests/contracts_verify/linalg_dot4_int_loop_open.li` — specimen + `_open` comment

## Hypothesis outcomes

- **HYPOTHESIS: verified** — Loop dot witness emits `ensures Prop := True` | evidence: `dot4_loop_ensures_lean_stub_gap.sh`
- **HYPOTHESIS: verified** — `Discharge.dot4_int_loop_eval_spec` not linked in AutoVC | evidence: AutoVC grep + script
- **HYPOTHESIS: falsified** — `_open` suffix means open AutoVC goals | evidence: `check-autovc-open-goals.sh` exit 0
- **HYPOTHESIS: verified** — mat2 `@` is the reference wiring for #472 | evidence: `vc_mat2_at2_ensures_0` uses `Li.Discharge.mat2_at2_float_spec`
- **HYPOTHESIS: deferred** — matmul IKJ loop witness gap CI | evidence: `matmul_loop_codegen_witness_gap.sh` fails without `llvm-dis`

## Recommended issues/PRs

1. **lic:** `[#472 / P-linalg] Emit `dot4_int_spec a b (dot4_loop_eval a b)` for loop witness` — labels: `provability`, `G-vc`, `G-math`
2. **lic:** Extend witness to tier-1 `ArrayMatMul2DF64` (mirror mat2) — labels: `provability`, `P-linalg`
3. **lic:** Retire `dot4_loop_ensures_lean_stub_gap.sh` when AutoVC links Discharge

## Deferred

- `matmul_loop_codegen_witness_gap.sh` — objdump fallback when `llvm-dis` absent
- G-bnd refinement True stub (cycle 11)
- `sqrt_open_bound` P-float discharge
