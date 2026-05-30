# Proof gap researcher — cycle 19 (P-linalg matmul loop ≡ ensures; lic#472)

**Run:** `proof_gap_researcher-2026-05-30-matmul-loop-witness-gap` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-math**, **G-lean**, **G-vc** · **PH-2e, PH-2f, PH-7e**  
**north_star_fit:** provable pillar — tier-1 `@` matmul loop codegen exists but lacks loop≡ensures witness (contrast dot4 closed slice)

## Executive summary

- **Focus:** Tier-1 `ArrayMatMul2DF64` IKJ loop path (`m,k,n > 24`) has **no** `witness_matmul*` in `vc_witness.cpp` and **no** matmul loop lemma in `Discharge.lean` — **P-linalg / lic#472** open.
- **Contrast verified:** `witness_dot4_int_loop` + `dot4_int_loop_eval_spec` close the 4-iteration dot loop; matmul has entry-level closed slices only (`mat2_entry00`, `mat2_at2_float_spec`).
- **New harness:** `matmul_loop_codegen_witness_gap.sh` + probe `matmul_25x25_at_codegen.li` (volatile sink anti-DCE) wired into `contracts_discharge_corpus.sh`.
- **HYPOTHESIS falsified (retest):** probe without `li_rt_volatile_sink_f64` retains matmul codegen — LLVM DCE'd `main` to 4 insns.
- **HYPOTHESIS falsified:** object-code `vfmadd` gate on release matmul — LLVM AVX-512 vectorizes/scatters; scalar FMA check unreliable at `-O3`.
- **Codegen↔Lean drift class:** tier-1 `matmul_naive` / blocked benches prove perf advisory only; no Lean Prop ties IKJ loop to matrix product spec.
- **No `trusted.lean` edits.**
- **`publish_subdir`** not injected (`provability_holes` auxiliary goal).

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-math / G-meta:** `ArrayMatMul2DF64` selects loop vs unrolled path at `kUnrollMax=24` (`emit.cpp:1185-1194`); 25×25 `@` forces `emit_matmul2d_ijk_loops`.
- **G-vc:** VC witness layer recognizes dot loops (`witness_dot4_int_loop_impl`, `vc_witness.cpp:459-492`) but **no** matmul IKJ loop matcher.
- **G-lean:** `Discharge.lean` has `dot4_int_loop_eval_spec` (`Discharge.lean:27-32`) and fixed-size `@` Props; **no** `matmul_loop_eval` / N×N lemma.

### 2. Contract gaps

- Closed P-linalg slices: scalar entry (`linalg_mat2_entry00_int_closed.li`), 2×2 float `@` (`mat2_at2_float_spec`), closed dot4 loop.
- **Open:** N×N float `@` with loop implementation ≡ dense product spec — blocked by witness + Lean lemma absence (lic#472).
- `@` on large tiles emits `ensures true`-style trivial VCs on `main`; no matrix-element postconditions.

### 3. Trusted surface

- No new axioms required; gap is static witness + semantic lemma backlog, not trusted-net/hardware axioms.

### 4. External trust boundaries

- Human: design `witness_matmul2d_ijk_loop` shape predicate (triple nested `for`/`while` matching `emit_matmul2d_ijk_loops`) + staged Lean `matmul_loop_eval` for small fixed N before general N.
- Human: decide whether tier-1 perf matmul certificate stays advisory until P-linalg loop slice closes.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `bash li-tests/tooling/matmul_loop_codegen_witness_gap.sh` | exit 0 — no witness; main=256 insns |
| `lic check li-tests/math_linalg/matmul_25x25_at_codegen.li` | exit 0 |
| Pre-fix probe (no volatile sink) | `main` DCE'd to xor/ret (~4 insns) |

**Key file:line:**

- `compiler/codegen/emit.cpp:1185-1194` — loop vs unroll threshold
- `compiler/codegen/emit.cpp:212-250` — `emit_matmul2d_ijk_loops` IKJ + optional FMA
- `compiler/verify/vc_witness.cpp:459-492` — dot loop witness (contrast)
- `docs/semantics/Discharge.lean:27-32` — `dot4_int_loop_eval_spec` (contrast)
- `li-tests/math_linalg/matmul_25x25_at_codegen.li` — 25×25 loop-path probe
- `li-tests/tooling/matmul_loop_codegen_witness_gap.sh` — gap gate
- `docs/verification/provability-gaps.md:58` — P-linalg partial backlog

## Hypothesis outcomes

- **HYPOTHESIS: verified** — No `witness_matmul*` in `vc_witness.cpp` | evidence: harness grep + `vc_witness.cpp` (no matches)
- **HYPOTHESIS: verified** — No matmul loop lemma in `Discharge.lean` | evidence: harness grep; only `dot4_*` / `mat2_*` lemmas
- **HYPOTHESIS: verified** — Dot4 loop closed via witness + `dot4_int_loop_eval_spec` | evidence: `vc_witness.cpp:459-492`, `Discharge.lean:32`
- **HYPOTHESIS: falsified** — Probe without volatile sink retains matmul codegen | evidence: pre-fix `main` ~4 insns; fixed with `li_rt_volatile_sink_f64(C[0][0])`
- **HYPOTHESIS: falsified** — Release 25×25 matmul object code contains `vfmadd` | evidence: 0 hits; LLVM AVX-512 `vscatterdpd` path at `-O3`
- **HYPOTHESIS: deferred** — Full N×N matmul loop ≡ ensures in AutoVC | evidence: lic#472; needs witness design + Lean lemma

## Recommended issues/PRs

1. **lic:** `[P-linalg] witness_matmul2d_ijk_loop + Discharge matmul_loop_eval (N=4 pilot)` — labels: `provability`, `G-math`, `PH-2f`, `lic#472`
2. **lic:** Merge matmul loop witness gap harness + volatile-sink probe — labels: `provability`, `testing`
3. **lic:** Update `provability-gaps.md` P-linalg row — matmul loop witness open (post-#472 design) — labels: `provability`, `G-lean`
4. **benchmarks:** Link cycle 19 digest in ecosystem grader provability row — labels: `provability`

## Deferred

- Horner FMA literal drift (cycle 18)
- mat2 FMA codegen vs Lean eval (cycles 16–17)
- `sqrt_open_bound` P-float intentional open
- Vec3 / CallProc opaque ensures (cycles 13–15)
- `publish_subdir` whitepaper — not injected this run
