# Proof gap researcher — cycle 30 (method call-site requires / FieldAccess Lean gap)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2j / PH-2e · G-oop, G-vc, G-lean  
**Focus:** OOP method `requires self.balance >= amount` — C++ call-site discharge vs opaque Lean VC  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** `Wallet_take` method contracts — field-access `requires` does not translate to Lean; call-site VCs stub `True` via C++ const folding only.
- **HYPOTHESIS: verified** — `expr_to_lean` has no `FieldAccess` case; `self.balance >= amount` emits opaque marker + `Prop := True` on proc-level VC.
- **HYPOTHESIS: verified** — plain param `requires amount >= 0` on same method **does** emit `(amount ≥ 0)` in AutoVC (asymmetric translation).
- **HYPOTHESIS: verified** — call-site `w.take(4)` after `w.balance = 10` discharges both requires as `True` + `trivial` in Lean without field semantics.
- **HYPOTHESIS: verified** — compile-time gate still rejects bad calls (`method_call_requires_fail.li` → E0304); Lean certificate would not catch a missed C++ witness.
- **Contrast:** plain function `callee(x >= 0)` emits real Lean on proc VC; literal `callee(5)` call-site still stubs `True`.
- **Evidence test added:** `method_call_requires_lean_gap.sh` → wired into `contracts_discharge_corpus.sh`.
- **`lic check` / gap script:** exit 0 on ok specimen; gap script PASS.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `expr_to_lean` FieldAccess | **Missing** — only `Call`→`abs`, `Index`, binops | `vc_emit_lean.cpp:202-254` (no FieldAccess arm) |
| Method proc `requires self.field >= n` | **Opaque + True stub** | AutoVC `vc_Wallet_take_requires_0` |
| Method proc `requires n >= 0` | **Partial Lean** | AutoVC `vc_Wallet_take_requires_1 := (amount ≥ 0)` (no `_proved`; skipped by open-goal script) |
| Call-site method requires | **C++ witness only** | `emit_requires_vcs_for_call` + `fold_const_int_locals` / `note_object_field_const_assign` |

**G-meta:** Lean certificate for `method_call_requires_ok.li` typechecks with all goals discharged via `trivial`, but field precondition is not stated in Lean.

### 2. Contract gaps

- **G-oop / P-ensures-witness:** Method `requires` on object fields are not proof obligations in Lean — only IDE/typecheck + C++ static folding at call sites.
- **G-vc:** Asymmetry vs plain function requires (translated) vs field-access requires (opaque).
- **G-test-verify:** `check-autovc-open-goals.sh` skips non-`True` proc-level `requires` lines — `vc_Wallet_take_requires_1` never flagged open.

### 3. Trusted surface

- No `trusted.lean` edits (policy). Wallet object layout is not axiomatized in Lean.

### 4. External trust boundaries

- **Deferred:** Whether OOP field requires should map to Lean `structure` fields + `Li.Wallet.balance` accessors (human RFC / PH-2j scope).
- **Deferred:** Extending `expr_to_lean` FieldAccess vs separate `Li.Discharge` method specs.

### 5. Evidence pack

| Item | Location |
|------|----------|
| abs-only Call translation | `compiler/verify/vc_emit_lean.cpp:224-231` |
| Opaque fallback on untranslated expr | `compiler/verify/vc_emit_lean.cpp:367-372` |
| Call-site requires emission | `compiler/verify/vc_emit_lean.cpp:462-507` |
| Method call wiring | `compiler/verify/vc_emit_lean.cpp:574-592` |
| Field const assign folding | `compiler/verify/call_requires.cpp:210-233`, `785-812` |
| Ok specimen | `li-tests/contracts_verify/method_call_requires_ok.li` |
| Fail specimen (E0304) | `li-tests/contracts_verify/method_call_requires_fail.li` |
| Plain control | `li-tests/contracts_verify/caller_requires_ok.li` |
| Gap repro script | `li-tests/tooling/method_call_requires_lean_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md` — **G-oop**, **G-vc** Partial |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/contracts_verify/method_call_requires_ok.li
./build/compiler/lic/lic check li-tests/contracts_verify/method_call_requires_fail.li  # exit 1 E0304
./li-tests/tooling/method_call_requires_lean_gap.sh
# corpus: ./li-tests/tooling/contracts_discharge_corpus.sh (includes method gap)
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | `expr_to_lean` lacks FieldAccess translation | `vc_emit_lean.cpp:202-254`; `method_call_requires_lean_gap.sh:27-29` |
| **verified** | `self.balance >= amount` → opaque + `Prop := True` on proc VC | AutoVC after `method_call_requires_ok.li` build |
| **verified** | `amount >= 0` on same method emits `(amount ≥ 0)` | AutoVC `vc_Wallet_take_requires_1` |
| **verified** | Call-site method requires stub `True` + `trivial` | AutoVC `vc_main_call0_Wallet_take_requires_*` |
| **verified** | Bad call rejected at typecheck (not Lean) | `method_call_requires_fail.li` → E0304 |
| **verified** | Plain `callee(x >= 0)` proc VC translates; literal call-site stubs True | `caller_requires_ok.li` AutoVC contrast |
| **deferred** | Lean `structure Wallet` + field requires in kernel | PH-2j human scope |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| `expr_to_lean`: FieldAccess + method `requires self.field` Lean emission | **lic** | `provability`, `PH-2j`, `G-oop`, `G-vc` |
| Extend `check-autovc-open-goals.sh` to flag untranslated proc `requires` (non-True, no `_proved`) | **lic** | `provability`, `G-test-verify` |
| Land `method_call_requires_lean_gap.sh` in CI corpus (local branch — lic PR) | **lic** | `provability`, `testing` |

**Related (no duplicate):** lic **#472** (P-linalg loop ≡ ensures), prior cycles on caller requires (plain function path).

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary).
- G-par parallel_disjoint script flakiness when AutoVC stale after matmul probe (corpus ordering) — separate hygiene fix.
- Full OOP trait laws / virtual dispatch (**G-oop** backlog).
- `trusted.lean` — human gate only.
