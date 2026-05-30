# Proof gap researcher — cycle 29 (matmul loop ≡ ensures / codegen witness)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i / PH-7e · G-lean, G-vc, G-math, G-meta  
**Focus:** Tier-1 `ArrayMatMul2DF64` IKJ loop path — codegen exists; no `witness_matmul*` / no `matmul_loop_eval_spec`; AutoVC trivial on probe  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** N×N `@` via `ArrayMatMul2DF64` lowers to IKJ loops (`emit_matmul2d_ijk_loops`) with FMA gated on `fp_numerically_stable`, but the proof stack has **no** loop≡ensures witness (unlike partial `witness_dot4_int_loop`).
- **HYPOTHESIS: verified** — `vc_witness.cpp` has `witness_dot4_int_loop` but **no** `witness_matmul*`; `Discharge.lean` has `dot4_int_loop_eval_spec` but **no** `matmul*_loop_eval`.
- **HYPOTHESIS: verified** — `matmul_25x25_at_codegen.li` builds with runtime init + `li_rt_volatile_sink_f64`; AutoVC is **main-only** `Prop := True` (no matmul postcondition).
- **HYPOTHESIS: falsified (retest)** — prior harness used `llvm-dis` on ELF + dead-store DCE; fixed probe (runtime `x` walk + sink) and **objdump** `li_user_main` FMA checks.
- **Contrast:** `linalg_mat2_at2_float_closed.li` wires `Li.Discharge.mat2_at2_float_spec`; `linalg_dot4_int_loop_open.li` has loop witness → `True` stub (G-vc honesty gap, cycle 24).
- **Evidence test repaired + wired:** `matmul_loop_codegen_witness_gap.sh` → `contracts_discharge_corpus.sh`.
- **`lic check` / gap script:** exit 0; gap script PASS.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `ArrayMatMul2DF64` loop lowering | **Codegen** — IKJ loops when `m,k,n > 24` or `m*k*n > 4096` | `emit.cpp:1317-1322` |
| FMA vs mul+add | **Codegen** — `llvm.fmuladd` only when `!fp_numerically_stable` | `emit.cpp:231-247` |
| Loop ≡ closed-form `ensures` | **Missing** | no `witness_matmul*` in `vc_witness.cpp` |
| Semantic eval lemma | **Missing** | no `matmul*_loop_eval` in `Discharge.lean` |
| Tier-1 `matmul_naive` | **Perf slice only** — user `C = A @ B` with `ensures result == 0` on `main` | `benchmarks/tier1_micro/matmul_naive/li/main.li` |

**G-meta note:** Executable matmul path is not linked to any Lean Prop on the 25×25 probe (AutoVC trivial).

### 2. Contract gaps

- No `contracts_verify/linalg_matmul_*_loop_open.li` analogue to `linalg_dot4_int_loop_open.li` for N×N matmul.
- **P-linalg (#472):** dot loop has static witness (stubs `True`); matmul has **no witness at all** — strictly wider codegen↔proof drift for tier-1 benches.

### 3. Trusted surface

- No `trusted.lean` edits (policy). Matmul uses compiler-emitted loops + `li_rt` sink only.

### 4. External trust boundaries

- **Deferred:** Whether tier-1 matmul should gain a closed 4×4 / 8×8 specimen before general N×N loop proof (human product decision).
- **Deferred:** Float associativity for IKJ+FMA vs naive triple loop (**G-hw**, **P-float**).

### 5. Evidence pack

| Item | Location |
|------|----------|
| Loop vs unroll threshold | `compiler/codegen/emit.cpp:1317-1326` |
| FMA gate in IKJ loops | `compiler/codegen/emit.cpp:231-247` |
| MIR `@` → `ArrayMatMul2DF64` | `compiler/mir/lower.cpp:1602-1619` |
| Dot loop witness (contrast) | `compiler/verify/vc_witness.cpp:459-492`, `528-529` |
| Dot loop eval lemma (contrast) | `docs/semantics/Discharge.lean:27-32` |
| Mat2 closed spec (contrast) | `docs/semantics/Discharge.lean:38-58` |
| Codegen probe | `li-tests/math_linalg/matmul_25x25_at_codegen.li` |
| Gap repro script | `li-tests/tooling/matmul_loop_codegen_witness_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md` — **G-math**, **G-lean** Partial; P-linalg loop dot open |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/math_linalg/matmul_25x25_at_codegen.li
./li-tests/tooling/matmul_loop_codegen_witness_gap.sh
# corpus hook: ./li-tests/tooling/contracts_discharge_corpus.sh (includes matmul gap)
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | No `witness_matmul*` in `vc_witness.cpp` | `grep witness_matmul` empty; `matmul_loop_codegen_witness_gap.sh:16-18` |
| **verified** | No `matmul_loop_eval` lemma in `Discharge.lean` | `grep matmul.*loop` empty; contrast `dot4_int_loop_eval_spec:32` |
| **verified** | 25×25 `@` probe emits trivial AutoVC only | `build/generated/AutoVC.lean` — `vc_main_ensures_0 … := True` only |
| **verified** | Release path uses `vfmadd`; `--numerically-stable` uses `mulsd` not FMA | `matmul_loop_codegen_witness_gap.sh` objdump on `li_user_main` |
| **falsified (retest)** | `llvm-dis` on `-o` ELF + unused `C` detects loop FMA | DCE + wrong artifact type; fixed probe + objdump |
| **deferred** | `matmul_naive` bench proc-level `ensures` on `C = A @ B` | Needs specimen design; blocked on P-linalg scope |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| P-linalg: `witness_matmul2d_loop` + `matmul2d_loop_eval_spec` (parity with dot4) | **lic** | `provability`, `PH-2i`, `G-vc`, `G-lean`, `P-linalg` |
| Add `linalg_matmul_loop_open.li` + manifest tier honesty for tier-1 `@` | **lic** | `provability`, `G-test-verify` |
| Wire `matmul_loop_codegen_witness_gap.sh` in CI corpus (done locally — land via lic PR) | **lic** | `provability`, `testing` |

**Existing (no duplicate):** lic **#472** (P-linalg loop ≡ ensures), lic **#461** (provability-gaps doc hygiene).

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `li-cursor-agents/src/research-goals/researcher-factory.ts`).
- Full N×N float `@` Lean Props (**P-float**).
- Blocked matmul tier-1 perf row (ecosystem audit yellow `matmul_naive`) — separate bench_improver focus.
- `trusted.lean` — human gate only.
