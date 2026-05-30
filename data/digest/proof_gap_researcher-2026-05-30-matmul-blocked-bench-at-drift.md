# Proof gap researcher — cycle 20 (tier-1 matmul_blocked bench↔`@` codegen drift)

**Run:** `proof_gap_researcher-2026-05-30-matmul-blocked-bench-at-drift` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-math**, **G-lean**, **G-vc** · **PH-2i, PH-2f, PH-7e**  
**north_star_fit:** provable pillar — tier-1 matmul_blocked perf row must not be confused with proved `ArrayMatMul2DF64 @` lowering

## Executive summary

- **Focus:** Tier-1 `matmul_blocked` bench on cycle-19 base uses **hand-written blocked while loops** with **zero `@`**; perf branch aligns bench to `C = A @ B` + `use_blocked_512` in `emit.cpp`.
- **New harness:** `matmul_blocked_bench_at_drift.sh` + probe `matmul_512x512_at_codegen.li` — forward-looking gate (bench must use `@` iff blocked `@` wired).
- **HYPOTHESIS verified:** No `witness_matmul*` in `vc_witness.cpp`; blocked/IKJ `@` paths both lack loop≡ensures witness (extends cycle 19 / lic#472).
- **HYPOTHESIS verified:** On current branch, 512×512 `@` lowers via IKJ loops (`emit_matmul2d_ijk_loops`); tier-1 bench never exercises `@`.
- **HYPOTHESIS verified:** Perf branch (`perf/bench-improver-matmul-tier1-green-20260530`) wires `use_blocked_512` and switches bench to `C = A @ B` — bench↔codegen alignment fix in flight, proof gap remains.
- **Stale-binary trap falsified:** Pre-rebuild `lic` emitted `mm_blk_*` labels from an older binary; rebuild required before codegen inspection.
- **No `trusted.lean` edits.**
- **`publish_subdir`** not injected (`provability_holes` auxiliary goal).

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-math:** `ArrayMatMul2DF64` on cycle-19 base: `use_loops` → IKJ for 512×512 `@` (`emit.cpp:1185-1190`); no `use_blocked_512` tile path.
- **G-math (perf branch):** `m==k==n==512` selects `emit_matmul2d_blocked_ijk` (`emit.cpp:1467-1475` on perf branch) — separate codegen class from IKJ and from manual bench loops.
- **G-vc / G-lean:** No matmul loop or blocked-tile witness in `vc_witness.cpp`; no `matmul_*_eval` lemma in `Discharge.lean` beyond fixed 2×2 slices.

### 2. Contract gaps

- Tier-1 `matmul_blocked` ≤1.2× C++ proves **manual loop** performance, not `@` postconditions.
- Closed P-linalg slices remain: dot4 loop, mat2 entry, mat2 `@` 2×2 float — **open:** N×N `@` (IKJ or blocked) ≡ dense product spec (lic#472).
- `@` on 512×512 emits trivial `ensures true`-style VCs on `main`; no matrix-element postconditions.

### 3. Trusted surface

- No new axioms; gap is witness + semantic lemma backlog plus bench↔codegen honesty, not trusted-net/hardware axioms.

### 4. External trust boundaries

- Human: merge perf branch bench `@` alignment before claiming tier-1 matmul_blocked exercises `@` lowering.
- Human: design `witness_matmul2d_blocked_ijk` (tile loop shape) + staged Lean lemma after lic#472 IKJ pilot.
- Human: decide whether blocked `@` tier-1 certificate stays advisory until P-linalg slice closes.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `bash li-tests/tooling/matmul_blocked_bench_at_drift.sh` | exit 0 — manual bench (no `@`); 512 `@` probe main=95 insns |
| `bash li-tests/tooling/matmul_loop_codegen_witness_gap.sh` | exit 0 — cycle 19 IKJ probe main=256 insns |
| `lic check li-tests/math_linalg/matmul_512x512_at_codegen.li` | exit 0 |
| `grep -c '@' benchmarks/tier1_micro/matmul_blocked/li/main.li` | 0 (cycle-19 base); 1 on perf branch line 98 |

**Key file:line:**

- `benchmarks/tier1_micro/matmul_blocked/li/main.li:98-126` — manual blocked loops (cycle-19 base; no `@`)
- `compiler/codegen/emit.cpp:1185-1190` — IKJ vs unroll threshold (cycle-19 base)
- `compiler/codegen/emit.cpp:1467-1475` — `use_blocked_512` (perf branch only)
- `compiler/verify/vc_witness.cpp` — no `witness_matmul*` (contrast `witness_dot4_int_loop`)
- `docs/semantics/Discharge.lean:27-33` — dot4 loop closed slice (contrast)
- `li-tests/math_linalg/matmul_512x512_at_codegen.li` — 512×512 `@` probe
- `li-tests/tooling/matmul_blocked_bench_at_drift.sh` — bench↔codegen alignment gate

## Hypothesis outcomes

- **HYPOTHESIS: verified** — Tier-1 `matmul_blocked` on cycle-19 base has no `@` operator | evidence: `grep -c '@'` → 0; harness
- **HYPOTHESIS: verified** — No `witness_matmul*` in `vc_witness.cpp` | evidence: harness grep
- **HYPOTHESIS: verified** — 512×512 `@` probe retains codegen with volatile sink | evidence: `matmul_blocked_bench_at_drift.sh` main=95 insns
- **HYPOTHESIS: verified** — Perf branch aligns bench (`C = A @ B`) with `use_blocked_512` emit | evidence: `git show perf/bench-improver-matmul-tier1-green-20260530:...`
- **HYPOTHESIS: falsified** — Stale `lic` binary reflects current `emit.cpp` blocked wiring | evidence: pre-rebuild IR had `mm_blk_*`; source has no `use_blocked_512`; rebuild required
- **HYPOTHESIS: deferred** — Blocked `@` loop ≡ ensures in AutoVC | evidence: lic#472; needs witness after IKJ pilot

## Recommended issues/PRs

1. **lic:** Merge perf branch `matmul_blocked` `C = A @ B` + blocked emit; keep `matmul_blocked_bench_at_drift.sh` green — labels: `provability`, `G-math`, `PH-7e`
2. **lic:** `[P-linalg] witness_matmul2d_blocked_ijk (512 pilot)` — labels: `provability`, `G-math`, `lic#472`
3. **lic:** Update `provability-gaps.md` G-math row — tier-1 blocked bench↔`@` alignment note — labels: `provability`, `G-lean`
4. **lic:** Remove duplicate Proof-db appendix blocks (`provability-gaps.md:70-76`, `:198-200`) — labels: `provability`, `lic#461`
5. **benchmarks:** Link cycle 20 digest in ecosystem grader provability row — labels: `provability`

## Deferred

- matmul IKJ loop witness (cycle 19 / lic#472)
- Horner FMA literal drift (cycle 18)
- mat2 FMA codegen vs Lean eval (cycles 16–17)
- `sqrt_open_bound` P-float intentional open
- Vec3 / CallProc opaque ensures (cycles 13–15)
- `publish_subdir` whitepaper — not injected this run
