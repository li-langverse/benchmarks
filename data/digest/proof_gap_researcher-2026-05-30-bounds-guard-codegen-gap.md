# Proof gap researcher — cycle 23 (G-bnd bounds guard; refinement VC strip)

**Run:** `proof_gap_researcher-2026-05-30-bounds-guard-codegen-gap` · **Date:** 2026-05-30  
**Goal:** `provability_holes` (auxiliary — no `publish_subdir`) · **Focus:** **G-bnd**, **G-vc**, **P-refine** · **PH-2e, PH-2f**  
**north_star_fit:** provable pillar — refinement-typed indices rely on typecheck + unchecked codegen; Lean callee VCs do not carry bounds

## Executive summary

- **Focus:** Refinement-typed array indices (`Index10`, `Idx8`) — contract tier vs codegen vs Lean drift for **G-bnd** / **P-refine**.
- **Codegen verified:** `emit.cpp` declares `li_bounds_fail` but never emits a call; `get_cell` uses unchecked indexed load (objdump).
- **Callee VC verified:** `index_refinement.li` AutoVC lowers `Index10` → `Int` with `Prop := True` stubs (`vc_emit_lean.cpp:147-150`).
- **Call-site VC verified:** Literal arg `3` at `get_cell(g, 3)` emits open bounds Prop `(0 ≤ 3) ∧ (3 < 8)` without `_proved` (not auto-closed).
- **Typecheck gate verified:** `cwe787_dyn_index.li` still rejected (`compile_fail` — dynamic `int` index).
- **New harness:** `bounds_guard_codegen_gap.sh` + `index_bounds_call_refine_probe.li`; wired into `contracts_discharge_corpus.sh`.
- **No `trusted.lean` edits.**
- **`publish_subdir`** not injected this run.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-bnd:** Safety for refinement indices is compile-time only (typecheck + refinement param tracking in `typecheck.cpp:1203-1215`). MIR/codegen emits `CreateInBoundsGEP` / stack indexed load with **no** runtime guard.
- **G-meta (local):** If a refinement-typed value reaches codegen without a valid proof path, behavior is LLVM inbounds/UB — not `li_bounds_fail`.
- Phase 3 plan still lists dynamic index → `li_bounds_fail` as open (`phase-03-mir-codegen.md:53`).

### 2. Contract gaps

- **Callee tier:** `requires true` / `ensures result == a[i]` on `get` with `Index10` param — AutoVC does **not** include `0 ≤ i < 10` in Props (all `True` + trivial).
- **Call-site tier:** Non-witnessed literal refinement at call emits real bounds Prop but leaves it **open** (no `Discharge` lemma, no static witness).
- **P-refine** backlog confirmed: refinement in signatures stripped for Lean; bounds live only in call-site VCs when literals do not static-discharge.

### 3. Trusted surface

- No new axioms. Gap is VC emission policy + missing runtime/codegen bounds story, not `trusted.lean`.

### 4. External trust boundaries (human decision if outside lic)

- Human: whether release builds should emit `li_bounds_fail` for **unproved** dynamic indices until **P-bnd** closes, or stay compile-time-only.
- Human: add `Discharge` lemmas / witnesses to close call-site refine VCs for literal indices (or witness fold in `vc_emit_lean.cpp:546-551`).
- Human: emit callee param refinement predicates in AutoVC (not only call-site) before claiming index proofs in **2f**.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `bash li-tests/tooling/bounds_guard_codegen_gap.sh` (from `lic/`) | exit 0 — PASS |
| `lic check li-tests/contracts_verify/index_bounds_call_refine_probe.li` | exit 0 |
| `objdump -d` on `good_bounded_index` build | `get_cell` — no `call` to `li_bounds_fail`; indexed `mov` only |

**Key file:line:**

- `compiler/codegen/emit.cpp:1275` — `li_bounds_fail` declare only (no `CreateCall` in compiler tree)
- `compiler/codegen/emit.cpp:891-922` — array load/store: inbounds GEP, no bounds branch
- `compiler/verify/vc_emit_lean.cpp:147-150` — refinement → base Lean type (bounds dropped)
- `compiler/types/typecheck.cpp:1195-1215` — constant / refinement index gate
- `li-tests/contracts_verify/index_refinement.li` — callee specimen
- `li-tests/contracts_verify/index_bounds_call_refine_probe.li` — call-site refine probe
- `li-tests/tooling/bounds_guard_codegen_gap.sh` — gap gate
- `docs/verification/provability-gaps.md:41,77` — **G-bnd** partial

## Hypothesis outcomes

- **HYPOTHESIS: verified** — Codegen never calls `li_bounds_fail` for refinement indices | evidence: harness + `emit.cpp` grep; objdump `get_cell`
- **HYPOTHESIS: verified** — Callee AutoVC strips `Index10` to `Int` with `True` stubs | evidence: `AutoVC.lean` after `index_refinement.li` build; `vc_emit_lean.cpp:147-150`
- **HYPOTHESIS: verified** — Call-site literal refine emits bounds Prop without auto-proof | evidence: `index_bounds_call_refine_probe.li` → `vc_main_call0_get_cell_refine_0`
- **HYPOTHESIS: falsified** — All refinement VCs are `True` stubs | evidence: call-site `refine_0` encodes `(0 ≤ 3) ∧ (3 < 8)` open
- **HYPOTHESIS: verified** — Dynamic unproven index rejected at typecheck | evidence: `cwe787_dyn_index.li` manifest `compile_fail`
- **HYPOTHESIS: deferred** — Release path omits `li_bounds_fail` for proved indices only | evidence: no refinement predicate in callee Lean; **P-bnd** open

## Recommended issues/PRs

1. **lic:** `[P-refine/P-bnd] Callee AutoVC carry IndexN bounds + codegen bounds guard policy` — labels: `provability`, `G-bnd`, `G-vc`, `PH-2e`
2. **lic:** Merge bounds guard gap harness + call refine probe — labels: `provability`, `testing`
3. **lic:** Close literal call-site refine VCs via static witness fold or `Discharge` lemma — labels: `provability`, `G-vc`
4. **lic:** Update `provability-gaps.md` **G-bnd** row — codegen omits runtime guard (post-harness) — labels: `provability`, `PH-2f`

## Deferred

- P-linalg matmul loop witness (cycle 19, lic#472)
- Horner FMA / tier-1 codegen drift (cycles 18–22)
- `sqrt_open_bound` P-float intentional open
- `publish_subdir` whitepaper — not injected (`provability_holes` auxiliary)
