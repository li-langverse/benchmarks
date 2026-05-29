# CI maintainer digest — proactive sweep (2026-05-29)

**Run:** `ci_maintainer-1780078740366`  
**Agent:** `ci_maintainer` (proactive ecosystem sweep)  
**North star fit:** ecosystem platform gate — provable CI on every product repo before merge (`PH-8p`, easy onboarding)

## Executive summary

- Refreshed `org-repo-ci-audit.json` and `ecosystem-audit.json`; **0 repos missing `ci.yml` on default branch** per canonical audit.
- **31 org repos OK**, **1 gated** (`lidb`), **0 audit-incomplete**, **0 PRs opened** this run (nothing to roll out).
- `ecosystem-audit.json` still flags **`research-findings`** as missing CI — intentionally **exempt** in `ensure-org-repo-ci.py` (research archive, not a product mirror).
- `lidb` has `ci.yml` on its feature default branch (`feat/ph-db-2-liorm-liq`) but is **gated on WP-H0** (human must set default branch to `main` first).
- Sampled live workflows on `main`: job IDs align with audit hints (`lip`→`bootstrap`, `li-demo`→`check`, `lic`→`build-and-test`).
- Branch protection uses org **rulesets** (`Li: protected branches`); legacy branch-protection API returns 404 — token lacks org-level ruleset read.
- **33 open PRs with failing CI** (ecosystem-audit) — out of scope for ci_maintainer rollout but blocks merge queue hygiene.
- No open PRs labeled `ecosystem-ci` from prior maintainer runs.

## Deliverable / findings

### Preflight (`ensure-org-repo-ci.py`)

```
OK: 31  missing: 0  gated: 1  incomplete: 0
  GATED lidb (default=feat/ph-db-2-liorm-liq): WP-H0: set default branch to main before requiring ci.yml on default
```

| Category | Count | Repos |
|----------|------:|-------|
| OK (`ci.yml` on default) | 31 | benchmarks, li-demo, li-gui, li-httpd, li-language, li-local-ci, li-net, li-std-core, li-std-math, lic, lip, lis, lit, mmo, net.httpd, physics.*, render, roadmap, sim*, store.realtime, studio*, ui, world |
| Exempt | 1 | research-findings |
| Gated (non-main default) | 1 | lidb |
| Missing CI | 0 | — |

Policy reference: `roadmap/docs/ecosystem/repo-ci-required.md`  
Template: `lic/scripts/templates/github-repo/ci.yml`

### Ecosystem audit cross-check

- `repos_missing_ci_main`: **1** — only `research-findings` (no `.github/workflows/` on `main`; GitHub API 404).
- `ensure-org-repo-ci.py` treats `research-findings` as **EXEMPT** alongside `li-cursor-agents` ignore list — audits are aligned by design; ecosystem metric is informational.

### Branch protection / required checks

Spot-checked live `ci.yml` job IDs vs `latest_check_job()` hints:

| Repo | Primary job on `main` | Audit hint |
|------|----------------------|------------|
| lip | `bootstrap` | `bootstrap` ✓ |
| li-demo | `check` | `check` ✓ |
| lic | `build-and-test` | `build-and-test` ✓ |
| sim.scientific | `changes` (path filter) + downstream | `check` (package default) |

`lip` ruleset **"Li: protected branches"** is active (repo-level). Org rulesets not readable with current PAT scope.

### Actions taken

- Ran `python3 scripts/ensure-org-repo-ci.py` (refresh audit JSON).
- Ran `python3 scripts/ecosystem-audit.py` (refresh ecosystem signals).
- **No isolated clone CI rollouts** — zero repos in `repos_missing_ci`.
- Opened digest PR on `benchmarks` (this file).

## Recommended issues/PRs

| Title | Repo | Labels | Notes |
|-------|------|--------|-------|
| WP-H0: set lidb default branch to `main` | lidb | governance, ecosystem-ci | Prerequisite before enforcing `ci.yml` on default; ci_maintainer can follow with branch-protection alignment |
| Align ecosystem-audit exempt list with org-repo-ci-audit | benchmarks | maintenance | Stop counting `research-findings` in `missing_ci_on_main` or document intentional delta |
| Fix failing PR CI (33 open) | various | bug, ci | P0 from ecosystem-audit `recommended_actions`; blocks Dependabot/agent-kit merges |

## Deferred

- **lidb WP-H0** — human governance; ci_maintainer blocked until default branch is `main`.
- **research-findings CI** — exempt research archive; add CI only if org policy changes.
- **Branch protection verification at scale** — needs PAT with org ruleset read or manual admin audit per repo.
- **lic CI hardening** (WP-C1–C6) — Docker CI image, reusable `package-ci`, LLVM 22 alignment — separate ci_maintainer lic specialist pass.
- **benchmarks duplicate CI jobs** (WP-E1) — throughput optimization, not missing-CI gate.
