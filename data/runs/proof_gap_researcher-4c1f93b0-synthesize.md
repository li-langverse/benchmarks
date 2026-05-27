# proof_gap_researcher — session `4c1f93b0` — `synthesize_step`

**Goal:** `provability_holes` · **north_star_fit:** PH-2e, PH-2f  
**Status:** cycle 1 complete  
**Artifact:** `lic/docs/ecosystem/research-sessions/provability_holes-cycle.md`  
**Whitepaper:** `research-findings/whitepapers/2026-05/provability_holes/prov-r0-cycle1-proof-gap-digest/`

## Executive summary

- Consolidated proof-gap digest (compiler, contracts, trusted, external boundaries, evidence pack).
- Tier B blocked by `Discharge.lean` duplicate `sqrt_open_bound_spec`; Tier A false-ensures hole encoded in `li-tests/`.
- Published whitepaper PROV-R0-1; no `trusted.lean` edits.

## Deliverable / findings

Full five-section digest in lic session file and research-findings README. Key verified hypotheses: build ≠ certificate; Discharge dup blocks lake; manifest duplicate keys; false ensures at Tier A.

## Recommended issues/PRs

See session file § synthesize — priority: Discharge dedupe, `run_all.sh` repair, register markdown dedup, manifest key CI guard.

## Deferred

G-meta, loop decreases, mat2 trusted/MIR, prove_lean_ok batch after run_all repair.
