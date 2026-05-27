# proof_gap_researcher — session `4c1f93b0` — `contract_tier`

**Goal:** `provability_holes` · **north_star_fit:** PH-2e, PH-2f  
**Artifact:** `lic/docs/ecosystem/research-sessions/provability_holes-cycle.md`

## Key findings

- Manifest duplicate `outcome` keys silently downgraded Tier C tests (fixed 3 blocks).
- Added `proof_gaps/false_ensures_still_builds.li` — Tier A passes `lic check`; `--allow-open-vc` ships exit 42 with `ensures result == 0`.
- `run_all.sh` syntax-broken on branch; direct `lic` commands used for verification.

See lic session file for full digest, hypotheses, and commands.
