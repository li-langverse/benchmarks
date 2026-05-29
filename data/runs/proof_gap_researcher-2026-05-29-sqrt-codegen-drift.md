# Proof gap researcher digest — 2026-05-29 (cycle 17)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-sqrt-codegen-drift`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f — G-vc / P-float codegen↔Lean ensures drift

## Executive summary

- **Focus:** **G-vc / P-float** — retest `sqrt_open_bound.li` for **codegen↔Lean drift**: open `Float.abs` ensures in AutoVC vs bare `li_rt_sqrt` LLVM (no runtime witness).
- **Verified:** `vc_sqrt_open_ensures_0` emits real `Float.abs ((result * result) - x) < 1e-12` with **no** `_proved` theorem (`vc_emit_lean.cpp:411-417`).
- **Verified:** `lic build --allow-open-vc` produces `sqrt_open` that `call li_rt_sqrt` and returns — **no** `li_bounds_fail` / `li_panic` / contract hooks in disassembly.
- **Verified:** Extern `li_rt_sqrt` has `ensures true` — no callee-return linkage VC; only `requires True` trivial proof.
- **Verified:** `lic check` passes (exit 0) without VC emission — check tier ≠ certificate (`main.cpp:603-613` build-only open-VC gate).
- **Retest:** Contract tier + verify CLI order harnesses still ok (cycles 6/12).
- **Harness:** `sqrt_open_bound_codegen_drift.sh` added; wired into `contracts_discharge_corpus.sh`.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Open ensures in Lean, bare return in codegen | `sqrt_open` disassembly: `call li_rt_sqrt` only; no postcondition runtime check |
| Non-trivial ensures omit `_proved` | `vc_emit_lean.cpp:411-417` — only `prop == "True"` or mat2 paths get theorems |
| `lic check` skips open-VC counting | `lic check sqrt_open_bound.li` → exit 0; build without `--allow-open-vc` → exit 1 |
| `LI_ALLOW_OPEN_VC` env ignored | `main.cpp:243-244`; contract tier harness |

### 2. Contract gaps

- User `ensures abs(result * result - x) < 1e-12` lowers to Lean Prop but **never** reaches runtime or Lean discharge.
- `--allow-open-vc` build is **executable** with unproved float accuracy claim — dev downgrade bypasses Lean gate, not semantics.
- Extern callee `ensures true` — no `mir_return_linked` VC tying `li_rt_sqrt` return to caller bound (`AutoVC.lean:16-17`).
- **Certificate tier split:** manifest `verify_open_ok` documents intentional open; IDE `lic check` still green (misleading for authors).

### 3. Trusted surface

- `trusted.lean` unchanged; `Discharge.lean:60-61` keeps `sqrt_open_bound_placeholder : True`.
- Gap is VC emission + codegen (no runtime contract layer), not axiom growth.

### 4. External trust boundaries

- `li_rt_sqrt` → glibc `sqrt` (`li_rt.c:87`) — IEEE/FP behavior is external until **P-float** lemmas in `Discharge.lean`.
- Closing requires Lean discharge + optional runtime ensures codegen — **not** `trusted.lean` axiom without RFC.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-vc** / **P-float** | `sqrt_open_bound.li:9` — `ensures abs(result * result - x) < 1e-12` |
| **G-vc** | `vc_emit_lean.cpp:224-228` — `abs` → `Float.abs` in Lean |
| **G-vc** | `vc_emit_lean.cpp:411-417` — no `_proved` for non-True ensures |
| **G-vc** (codegen) | `sqrt_open @ 0x1240` → `call li_rt_sqrt`; no contract hooks |
| **G-lean** | `AutoVC.lean:13` — open `vc_sqrt_open_ensures_0` |
| **G-test-verify** | `sqrt_open_bound_verify_cli_order.sh` → ok (flags-before-file hole) |
| **Harness** | `bash li-tests/tooling/sqrt_open_bound_codegen_drift.sh` → ok |
| **Corpus** | `bash li-tests/tooling/contracts_discharge_corpus.sh` → ok |
| **lic check** | `lic check li-tests/contracts_verify/sqrt_open_bound.li` → exit 0 |
| **lic build** | `lic build li-tests/contracts_verify/sqrt_open_bound.li -o /dev/null` → exit 1 |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — open Float.abs ensures has no runtime witness in sqrt_open codegen | evidence: sqrt_open_bound_codegen_drift.sh; objdump sqrt_open`
- `HYPOTHESIS: verified — vc_sqrt_open_ensures_0 has no _proved theorem while build --allow-open-vc ships binary | evidence: AutoVC.lean:13; sqrt_open_bound_codegen_drift.sh`
- `HYPOTHESIS: verified — extern li_rt_sqrt ensures true emits no callee-return linkage VC | evidence: AutoVC.lean:16-17; sqrt_open_bound.li:2-5`
- `HYPOTHESIS: verified — lic check passes while default lic build fails on open VC | evidence: lic check exit 0; sqrt_open_bound_contract_tier.sh`
- `HYPOTHESIS: verified — verify CLI flags-before-file still false-passes strict-lean | evidence: sqrt_open_bound_verify_cli_order.sh`
- `HYPOTHESIS: falsified — allow-open-vc build emits runtime abs/error check for ensures | evidence: objdump sqrt_open; sqrt_open_bound_codegen_drift.sh`
- `HYPOTHESIS: deferred — close via P-float lemmas in Discharge.lean | evidence: proof-corpus-roadmap P-float open; no trusted.lean edit`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| feat(P-float): discharge vc_sqrt_open_ensures_0 via Float.abs + sqrt error lemmas | **lic** | `PH-2f`, G-vc, P-float |
| feat(G-vc): mir_return_linked VC for extern callee ensures on sqrt_open_bound | **lic** | `PH-2e`, G-vc |
| fix(G-test-verify): lic verify accept flags before path (sqrt_open_bound strict-lean) | **lic** | G-test-verify |
| test(provability): sqrt_open_bound_codegen_drift regression harness | **lic** | G-vc, research |
| docs: provability-gaps G-vc — note codegen↔Lean ensures drift on allow-open-vc builds | **lic** | provability-gaps |

## Deferred

- **G-par** proc disjoint + decorator-for asymmetry (cycle 15 — not retested).
- **G-par** `disjoint_elem` + `buf[0]` executable race (cycle 16 — not retested).
- **G-net** recv/send triple drift (cycle 14 — not retested).
- **G-bnd** guarded refinement VCs (cycle 11 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
