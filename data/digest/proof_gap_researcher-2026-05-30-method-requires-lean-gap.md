# Proof gap researcher — cycle 12 (G-vc method field requires Lean gap)

**Run:** `proof_gap_researcher-2026-05-30-method-requires-lean-gap` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-vc**, **G-oop** · **PH-2e, PH-2f, PH-2j-f**  
**north_star_fit:** provable pillar — method `requires self.field` must appear in Lean certificate, not only C++ fold

## Executive summary

- Method `requires` on plain params (`amount >= 0`) **emit real Lean predicates** in AutoVC.
- Method `requires` on **`self.field`** (`self.balance >= amount`) are **opaque** — `expr_to_lean` has no `FieldAccess` case.
- Opaque method requires stub to **`Prop := True`** with trivial `_proved`; certificate passes with **zero open goals** but no field math.
- Call-site method requires **witness-discharge** to `True` when const-fold succeeds (`w.balance=10`, `amount=4`); still no emitted `(balance ≥ amount)` predicate.
- **Typecheck gate works:** `method_call_requires_fail.li` rejected at compile time (**E0304**).
- Object types (`Wallet`) **erase to `Int`** in Lean VC formals — secondary codegen↔Lean drift.
- CI guard **`method_requires_lean_gap.sh`** added and wired into **`contracts_discharge_corpus.sh`**.

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-vc:** `vc_emit_lean.cpp:202-254` — `expr_to_lean` handles `Ident`, `BinOp`, `Index`, `Call(abs)` only; **`FieldAccess` returns nullopt**, triggering opaque stub path at `emit_contract_def` (~368).
- Method entry `vc_Wallet_take_requires_0` marked `/-! VC requires (opaque) -/` and defined `Prop := True` despite typecheck + const-fold knowing `10 >= 4`.

### 2. Contract gaps

- **P-ensures-witness / call-site requires:** Function-style literal discharge works (`caller_requires_ok.li`); method field requires bypass Lean translation entirely at callee entry.
- Witnessed call-site VCs (`vc_main_call0_Wallet_take_requires_* := True`) mirror function call pattern — honest for trivial discharge but **mask missing field predicates** in certificate.

### 3. Trusted surface

- Unchanged; no `trusted.lean` edits.

### 4. External trust boundaries

- Human decision: whether object-field `requires` need `LiObject`/`Wallet` Lean types vs continued `Int` erasure before field Props can close.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `./li-tests/tooling/method_requires_lean_gap.sh` | exit 0 (gap documented) |
| `lic build li-tests/contracts_verify/method_call_requires_ok.li` | exit 0; AutoVC stubs field requires |
| `lic check li-tests/contracts_verify/method_call_requires_fail.li` | exit 1, **E0304** |
| `lic build li-tests/contracts_verify/caller_requires_ok.li` | exit 0; call-site requires witnessed True (control) |

**Key file:line:**

- `compiler/verify/vc_emit_lean.cpp:202-254` — no `FieldAccess` in `expr_to_lean`
- `compiler/verify/vc_emit_lean.cpp:368-416` — opaque requires → `Prop := True` + trivial proof
- `compiler/verify/vc_emit_lean.cpp:111-138` — named object types fall through to `Int`
- `compiler/verify/call_requires.cpp:196-233` — object field const-fold for typecheck only
- `compiler/verify/call_requires.cpp:475-478` — method call-site requires check (C++ gate)
- `li-tests/contracts_verify/method_call_requires_ok.li` — repro specimen
- `li-tests/contracts_verify/method_call_requires_fail.li` — E0304 negative control

## Hypothesis outcomes

- **HYPOTHESIS: verified** — `self.field` method requires stub to `Prop := True` in AutoVC | evidence: `method_requires_lean_gap.sh`, AutoVC line 13-14
- **HYPOTHESIS: verified** — Plain param method requires emit Lean `(amount ≥ 0)` | evidence: AutoVC `vc_Wallet_take_requires_1`
- **HYPOTHESIS: verified** — Typecheck rejects bad method call before build | evidence: `lic check method_call_requires_fail.li` → E0304
- **HYPOTHESIS: verified** — Object type `Wallet` erases to `Int` in Lean VC formals | evidence: AutoVC `(self : Int)`
- **HYPOTHESIS: falsified** — Lean certificate carries `self.balance >= amount` predicate | evidence: grep AutoVC — no `balance` token
- **HYPOTHESIS: deferred** — Emit field-access Props via `LiObject` model | evidence: needs Lean object typing RFC (human)

## Recommended issues/PRs

1. **lic:** `[G-vc/G-oop] expr_to_lean FieldAccess + Wallet Lean type for method requires` — labels: `provability`, `G-vc`, `PH-2j-f`
2. **lic:** `[G-vc] Discharge.lean lemmas for object field requires at call sites` — labels: `provability`, `G-lean`
3. **lic:** Retire `method_requires_lean_gap.sh` when gap closes (mirror `bounds_refinement_lean_gap.sh` pattern)

## Deferred

- G-bnd/P-refine refinement Props (cycle 11)
- P-float `sqrt_open_bound` Lean discharge
- G-net trusted codegen drift (cycle 14 sibling)
- Non-literal method call-site requires (local/unknown args) — retest after field translation lands
