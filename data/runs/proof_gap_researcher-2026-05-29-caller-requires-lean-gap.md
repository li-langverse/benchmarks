# Proof gap researcher digest — 2026-05-29 (cycle 20)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-caller-requires-lean-gap`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f — G-vc / G-lean call-site requires witness honesty

## Executive summary

- **Focus:** **G-vc / G-lean** — call-site callee `requires` witness folding (literal, const-local, path-guard) discharges to **`Prop := True`** stubs in AutoVC while callee defs keep real `(x ≥ 0)` Props.
- **Verified:** `caller_requires_local_ok.li` (`var y = 5; callee(y)`) → `vc_caller_local_call0_callee_requires_0 := True` + `trivial`; callee keeps `vc_callee_requires_0 (x : Int) : Prop := (x ≥ 0)`.
- **Verified:** Literal `callee(5)` and guarded `if n >= 0: callee(n)` share the same True-stub call-site pattern; all three pass `lic build` + zero open Lean goals.
- **Verified:** Typecheck still rejects bad calls (`caller_requires_fail.li` → E0304; conditional `y = -1` after guard → E0304) — static gate sound for checked specimens.
- **Harness:** `caller_requires_local_lean_gap.sh` + new `caller_requires_guarded_ok.li`; wired into `contracts_discharge_corpus.sh`.
- **Falsified:** Lean certificate encodes `(y ≥ 0)` / `(n ≥ 0)` at call sites today.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Call-site requires witness → `prop = "True"` when statically discharged | `vc_emit_lean.cpp:480-485` — `witnessed` branch |
| Const-local folding for requires check | `call_requires.cpp:235-252`, `786-801` — `fold_const_int_locals` / assign tracking |
| Path-guard `assum_nonneg_ints` from `if n >= 0` | `call_requires.cpp:395-417`, `814-821` |
| Typecheck rejects negative literal call | `caller_requires_fail.li` → E0304 (`call_requires.cpp:434-449`) |
| Typecheck rejects conditional negative reassignment | `/tmp/caller_requires_cond_reassign.li` → E0304 |

### 2. Contract gaps

- **Callee def vs call-site asymmetry:** `vc_callee_requires_0` is a real `(x ≥ 0)` Prop; call-site VCs are **`True` stubs** even when typecheck proved the witness (literal, `y = 5`, or `if n >= 0` guard).
- **Certificate honesty:** `lic build` reports zero open goals because witnessed call-site requires never emit real `(arg ≥ 0)` Props — same honesty class as refinement guard stubs (cycle 11) but for **`requires`** not refinement types.
- **Non-witnessed path:** guarded caller with `ensures result >= 0` leaves **open** `vc_caller_guarded_ensures_0` (ensures, not requires) — call-site requires still stubbed True.

### 3. Trusted surface

- `trusted.lean` unchanged — gap is VC emission (`emit_requires_vcs_for_call`), not axiom growth.

### 4. External trust boundaries

- Closing requires **P-refine** / **2f** lemmas that emit real substituted Props `(y ≥ 0)` at call sites and path-sensitive discharge — human-reviewed; not `trusted.lean` without approval.
- Witness folding is intentionally partial per provability-gaps “literal / const-local discharge” — gap is certificate **overclaims** full Lean proof of call-site obligations.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-vc** | `vc_emit_lean.cpp:462-503` — `emit_requires_vcs_for_call` |
| **G-vc** | `call_requires.cpp:380-393` — `folded_discharged_by_proof_facts` |
| **G-lean** | `caller_requires_local_ok.li` → AutoVC call-site True stub |
| **G-vc** | `caller_requires_guarded_ok.li:15-16` — path-guard call |
| **G-vc** (negative) | `caller_requires_fail.li` → E0304 |
| **Harness** | `bash li-tests/tooling/caller_requires_local_lean_gap.sh` → ok |
| **lic check** | `lic check li-tests/contracts_verify/caller_requires_guarded_ok.li` → exit 0 |
| **Corpus** | `bash li-tests/tooling/contracts_discharge_corpus.sh` (includes new harness) |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — const-local y=5 call-site requires emits True stub while callee keeps (x ≥ 0) | evidence: caller_requires_local_lean_gap.sh; AutoVC grep`
- `HYPOTHESIS: verified — literal callee(5) and guarded if n>=0 share True-stub call-site VCs | evidence: caller_requires_local_lean_gap.sh`
- `HYPOTHESIS: verified — lic build + zero open goals on all three witnessed specimens | evidence: caller_requires_local_lean_gap.sh; check-autovc-open-goals.sh`
- `HYPOTHESIS: verified — typecheck rejects callee(-1) and conditional y=-1 after init | evidence: caller_requires_fail.li E0304; /tmp/caller_requires_cond_reassign.li`
- `HYPOTHESIS: falsified — Lean AutoVC encodes (y ≥ 0) or (n ≥ 0) at call sites | evidence: grep vc_*_call0_callee_requires_0 := True`
- `HYPOTHESIS: deferred — emit real substituted call-site requires Props in Lean | evidence: vc_emit_lean.cpp:484-485 witnessed→True; P-refine backlog`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| test(provability): caller_requires_local_lean_gap regression harness | **lic** | G-vc, research |
| feat(G-vc): emit real Lean Props for witnessed call-site callee requires | **lic** | PH-2e, PH-2f, provability |
| docs: provability-gaps G-vc — cite call-site True stub vs callee (x ≥ 0) asymmetry | **lic** | provability-gaps |
| feat(P-refine): path-sensitive call-site requires linked to if-guard facts | **lic** | PH-2e, research |

## Deferred

- **G-dec** vectorized-for codegen↔Lean drift (cycle 19 — not retested).
- **G-vc** vec3 field opaque VC (cycle 18 — not retested).
- **G-vc** sqrt_open_bound P-float (cycle 17 — not retested).
- **G-par** disjoint_elem executable race (cycle 16 — not retested).
- **G-bnd** refinement param stubs (cycle 11 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
