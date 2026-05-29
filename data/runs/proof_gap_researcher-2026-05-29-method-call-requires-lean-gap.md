# Proof gap researcher digest — 2026-05-29 (cycle 21)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-method-call-requires-lean-gap`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2j-f, PH-2e, PH-2f — G-oop / G-vc method `requires` Lean honesty

## Executive summary

- **Focus:** **G-oop / G-vc** — method `requires` with `self.field` access: callee VC opaque → `True` stub; call-site VCs `True` stubs after const-local fold (`w.balance = 10`, `w.take(4)`).
- **Verified:** `expr_to_lean` has no `FieldAccess` case — `self.balance >= amount` never translates (`vc_emit_lean.cpp:230-300`).
- **Verified:** Callee `vc_Wallet_take_requires_0 := True` with opaque comment; `requires_1` is real `(amount ≥ 0)`.
- **Verified:** Call-site `vc_main_call0_Wallet_take_requires_{0,1} := True` despite typecheck folding `w.balance` (`call_requires.cpp:237-248`, `786-804`).
- **Verified:** `method_call_requires_fail.li` → **E0304** on `w.take(10)` (`5 >= 10`); static gate sound for checked specimens.
- **Harness:** `method_call_requires_lean_gap.sh`; wired into `contracts_discharge_corpus.sh`.
- **lic check / build:** `lic check method_call_requires_ok.li` → exit 0; harness → ok.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| `expr_to_lean` omits `FieldAccess` | `vc_emit_lean.cpp:230-300` — `default: return nullopt` |
| Callee method requires with field → opaque True | `AutoVC.lean` — `VC requires (opaque): source expr not yet translated` |
| Method call-site requires via `emit_requires_vcs_for_call` | `vc_emit_lean.cpp:786-804` — same witnessed→True path as plain calls |
| Const-local fold for object fields | `call_requires.cpp:196-248` — `object_field_const_key` / `w.balance` |

### 2. Contract gaps

- **Callee asymmetry (worse than function calls):** `self.balance >= amount` is **not** a real Lean Prop on the method def — only `amount >= 0` is `(amount ≥ 0)`.
- **Call-site asymmetry:** Typecheck proves `10 >= 4` via folded locals; certificate emits **True** stubs, not substituted `(10 ≥ 4)` Props (same honesty class as cycle 20 function calls).
- **Manifest note overclaim risk:** `prove_lean_ok` on `method_call_requires_ok.li` passes with zero open goals while field requires are stubbed.

### 3. Trusted surface

- `trusted.lean` unchanged — gap is VC emission / `expr_to_lean`, not axiom growth.

### 4. External trust boundaries

- Closing needs **FieldAccess** in `expr_to_lean` + **P-refine** / **2j-f** call-site Props for method receivers — human-reviewed; not `trusted.lean` without approval.
- Error text shows `? >= amount` for field requires — UX/diagnostic gap adjacent to translation gap.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-vc** | `vc_emit_lean.cpp:446-450` — opaque when `expr_to_lean` fails |
| **G-vc** | `vc_emit_lean.cpp:655-660` — witnessed call-site → `True` |
| **G-oop** | `method_call_requires_ok.li:5-19` — `Wallet_take` + `w.take(4)` |
| **G-vc** (negative) | `method_call_requires_fail.li` → E0304 |
| **Harness** | `bash li-tests/tooling/method_call_requires_lean_gap.sh` → ok |
| **lic check** | `lic check li-tests/contracts_verify/method_call_requires_ok.li` → exit 0 |
| **Corpus** | `bash li-tests/tooling/contracts_discharge_corpus.sh` (includes new harness) |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — self.balance >= amount on method def emits opaque True stub, not (self.balance ≥ amount) | evidence: method_call_requires_lean_gap.sh; vc_emit_lean.cpp:446-450`
- `HYPOTHESIS: verified — amount >= 0 on same method emits real Lean Prop | evidence: AutoVC grep; method_call_requires_lean_gap.sh`
- `HYPOTHESIS: verified — w.balance=10, w.take(4) call-site requires are True stubs | evidence: method_call_requires_lean_gap.sh; vc_emit_lean.cpp:655-660`
- `HYPOTHESIS: verified — lic build + zero open goals on ok specimen | evidence: method_call_requires_lean_gap.sh`
- `HYPOTHESIS: verified — build rejects w.take(10) with E0304 | evidence: method_call_requires_fail.li; harness`
- `HYPOTHESIS: falsified — Lean certificate encodes self.balance ≥ amount at call site | evidence: grep vc_main_call0_Wallet_take_requires_0 := True`
- `HYPOTHESIS: deferred — translate FieldAccess requires + real call-site Props | evidence: expr_to_lean default branch; P-refine / 2j-f backlog`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| test(provability): method_call_requires_lean_gap regression harness | **lic** | G-oop, G-vc, research |
| feat(G-vc): expr_to_lean FieldAccess for method/object requires | **lic** | PH-2e, PH-2j-f |
| feat(G-vc): emit real Lean Props for witnessed method call-site requires | **lic** | PH-2e, PH-2f, provability |
| docs: provability-gaps G-oop — cite method field requires opaque + call-site stubs | **lic** | provability-gaps |

## Deferred

- **G-vc** caller requires lean gap (cycle 20 — function calls; not retested).
- **G-dec** vectorized-for codegen↔Lean drift (cycle 19 — not retested).
- **G-vc** vec3 field opaque VC (cycle 18 — not retested).
- **G-par** disjoint_elem executable race (cycle 16 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
