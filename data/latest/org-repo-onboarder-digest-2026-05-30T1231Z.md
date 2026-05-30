# Org repo onboarder digest — 2026-05-30T1231Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T12:31Z` · CI audit `2026-05-30T12:22Z` · agent-kit audit `2026-05-30T12:31Z` · briefing `2026-05-30T12:07Z`

## Executive summary

- **Discovery (refreshed):** `github=35` `known=35` **`new=0`** **`stale=0`** via `gh repo list` — all org repos are now in the known set (CI + agent-kit audit union). **Discovery phase complete.**
- **Onboarding phase shift:** The 22 repos flagged at 12:05Z are no longer *new*; they remain **incomplete** on agent-kit (20 missing kit locally, 1 no local clone). CI gate is green for all audited product repos.
- **Agent-kit is the sole blocker:** 20 repos **`missing_kit`** @ canonical stamp `1.3.5+6018e18bf2ed91f4`; **`lic-docs`** not auditable (`missing_local_clone`). No `register_in_catalog` until kit PRs merge.
- **No stale catalog entries** — `stale_known_repos` is `[]`; no archive/delete candidates without human approval.
- **Highest-risk incomplete onboarding:** `lidb` (control-plane DB / PH-DB-0), `studio` / `studio.ai` (PH-GD blockers), `proof-library` (provable pillar), `net.httpd` (httpd mirror).
- **Highest-risk unclassified (placement TBD):** `store.realtime`, `mmo`, `world`, domain `sim.*` / `physics.*` mirrors — need `package_architect` after kit wave.
- **North star fit:** proof-first (`proof-library`, `lidb`) → easy/ai-first (`studio`, `studio.ai`, `ui`, `lic-docs`) → domain sim mirrors — **no catalog add before CI + agent-kit green**.
- **Audit gaps:** `li-cursor-agents` is in discovery known set but **absent from `org-repo-ci-audit.json`**; stale `lidb` WP-H0 note still in CI audit policy (default branch is now `main`).

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 35 |
| Known (catalog + audits) | 35 |
| **New** | **0** |
| **Stale known** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

**Progress since 12:05Z:** known set grew from 13 → 35 as CI audit (`repos_ok`: 34) and agent-kit audit (`repos_needing_sync` + `repos_ok`) expanded coverage. Zero net-new GitHub repos appeared.

### New repos (classification + handoffs)

*None this pass.* All 35 GitHub repos are in the known set.

### Incomplete onboarding (formerly new — agent-kit / placement / catalog)

| Repo | Script class | **Confirmed class** | Priority | CI on `main` | Agent-kit | Recommended handoffs |
|------|--------------|---------------------|:--------:|:------------:|:---------:|----------------------|
| `lidb` | unclassified | **candidate_official** (PH-DB-0) | P0 | ✓ | missing | `agent_kit_maintainer` → `sync_agent_kit`; `package_architect` → `placement_review`; `docs_maintainer` → `live_docs_smoke`; `code_implementer` → `register_in_catalog` |
| `lic-docs` | unclassified | **candidate_official** (handbook) | P0 | ✓ | no local clone | clone → kit → docs → placement → catalog |
| `net.httpd` | unclassified | **official_mirror** | P0 | ✓ | missing | kit → docs → catalog (skip placement) |
| `studio` | unclassified | **core_tooling** (PH-GD) | P0 | ✓ | missing | kit → docs → catalog |
| `studio.ai` | unclassified | **core_tooling** (ai-first) | P0 | ✓ | missing | kit → docs → catalog |
| `proof-library` | unclassified | **core_tooling** (provable) | P1 | ✓ | missing | kit → docs → catalog |
| `li-local-ci` | candidate_official | **core_tooling** | P1 | ✓ | missing | kit → docs → catalog |
| `sim` | unclassified | **core_tooling** (PH-SIM) | P1 | ✓ | missing | kit → docs → catalog |
| `ui` | unclassified | **core_tooling** | P1 | ✓ | missing | kit → docs → catalog |
| `render` | unclassified | **core_tooling** (PH-GD) | P1 | ✓ | missing | kit → docs → catalog |
| `li-gui` | candidate_official | candidate_official | P2 | ✓ | missing | kit → docs → placement → catalog |
| `store.realtime` | unclassified | unclassified | P2 | ✓ | missing | kit → docs → **placement_review** → catalog |
| `sim.scientific` | unclassified | unclassified | P2 | ✓ | missing | kit → docs → placement → catalog |
| `world` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `mmo` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.robotics` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.automotive` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.drug_design` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.additive` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `physics.runtime` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `physics.custom` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `research-findings` | unclassified | unclassified | P3 | ✓ (exempt) | missing | kit → docs → placement → catalog |

**Onboarding pipeline:** ~~`ci_maintainer`~~ (CI done) → **`agent_kit_maintainer`** → `docs_maintainer` → [`package_architect` if unclassified/candidate] → `code_implementer` (`register_in_catalog` only after kit green). Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

### Stale catalog entries

*None.* `stale_known_repos` is `[]`. No archive/delete without human sign-off.

### Handoff queue (control plane)

**Wave P0 — platform / PH-GD blockers**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | secure / PH-DB-0 |
| `agent_kit_maintainer` | `lic-docs` | `sync_agent_kit` | easy — handbook (clone first) |
| `agent_kit_maintainer` | `net.httpd` | `sync_agent_kit` | secure / web |
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | ai-first / PH-GD |
| `package_architect` | `lidb` | `placement_review` | secure / PH-DB-0 |
| `package_architect` | `lic-docs` | `placement_review` | easy — lic vs standalone docs |
| `docs_maintainer` | `lic-docs` | `live_docs_smoke` | easy |
| `docs_maintainer` | `studio` | `live_docs_smoke` | PH-GD |
| `ci_maintainer` | `li-cursor-agents` | `add_ci_yml` | platform — absent from CI audit scope |

**Wave P1 — core product / tooling**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | platform |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | PH-GD |
| `docs_maintainer` | `sim` | `live_docs_smoke` | PH-SIM |
| `docs_maintainer` | `ui` | `live_docs_smoke` | easy |

**Wave P2 — candidate / placement**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `li-gui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `store.realtime` | `sync_agent_kit` | secure / infra TBD |
| `agent_kit_maintainer` | `sim.scientific` | `sync_agent_kit` | PH-SIM |
| `package_architect` | `li-gui` | `placement_review` | easy |
| `package_architect` | `store.realtime` | `placement_review` | secure |

**Wave P3 — domain sim / physics / research (batch after P0–P2)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `sim.robotics` | `sync_agent_kit` | robotics / PH-SIM |
| `agent_kit_maintainer` | `sim.automotive` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `sim.drug_design` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `sim.additive` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `physics.runtime` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `physics.custom` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `world` | `sync_agent_kit` | PH-GD |
| `agent_kit_maintainer` | `mmo` | `sync_agent_kit` | gaming |
| `agent_kit_maintainer` | `research-findings` | `sync_agent_kit` | research |
| `package_architect` | `sim.robotics` | `placement_review` | robotics |
| `package_architect` | `sim.scientific` | `placement_review` | PH-SIM |

**Deferred catalog step (21 repos — enqueue after kit PRs merge)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `code_implementer` | `*` (21 incomplete) | `register_in_catalog` | ecosystem — after agent-kit gates |

**Existing known-repo hygiene (parallel — briefing heap)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `docs_maintainer` | `lic` | `live_docs_smoke` | easy — `repos_without_live_docs` / Pages down |
| `org_repo_onboarder` | `benchmarks` | `embed_discovery_in_briefing` | platform — wire `org_new_repos_discovery` into `agent-briefing.py` |
| `ci_maintainer` | `benchmarks` | `clear_stale_audit_notes` | platform — remove resolved `lidb` WP-H0 gate from CI audit |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `lidb` | chore(agent-kit): install roadmap agent-kit @ 1.3.5 | `agent-kit`, `platform`, `PH-DB-0` |
| `lic-docs` | chore(agent-kit): install roadmap agent-kit + docs smoke | `agent-kit`, `docs`, `easy` |
| `net.httpd` | chore(agent-kit): sync org agent-kit for httpd mirror | `agent-kit`, `secure`, `platform` |
| `studio` | chore(agent-kit): install roadmap agent-kit @ 1.3.5 | `agent-kit`, `PH-GD`, `easy` |
| `studio.ai` | chore(agent-kit): install roadmap agent-kit @ 1.3.5 | `agent-kit`, `ai-first`, `PH-GD` |
| `proof-library` | chore(onboard): agent-kit for proof library | `agent-kit`, `provable` |
| `sim` | chore(agent-kit): sync li-sim core to canonical stamp | `agent-kit`, `PH-SIM` |
| `ui` | chore(agent-kit): sync li-ui package agent-kit | `agent-kit`, `easy` |
| `render` | chore(agent-kit): sync li-render agent-kit | `agent-kit`, `PH-GD` |
| `store.realtime` | chore(onboard): agent-kit + placement review | `agent-kit`, `platform` |
| `li-cursor-agents` | chore(ci): add ci.yml to control-plane repo | `ci`, `platform` |
| `lic` | chore(docs): restore GitHub Pages live docs | `docs`, `easy` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform`, `agent-kit` |
| `benchmarks` | chore(org): clear stale `lidb` WP-H0 note in CI audit | `platform`, `ci` |
| `roadmap` | chore(governance): apply branch protection to newly CI-enabled repos | `ecosystem-governance` |

## Deferred

- **`code_implementer` / `register_in_catalog`** for 21 incomplete repos — blocked until agent-kit PRs merge.
- **`ci_maintainer` / `add_ci_yml`** for the 22-repo wave — **done on GitHub**; remaining CI work is audit-scope expansion (`li-cursor-agents`) and stale policy cleanup.
- **Stale catalog pruning** — none identified.
- **Bulk P3 sim/physics wave** — defer agent-kit fan-out until P0–P1 complete to avoid swarming domain mirrors ahead of `studio` / `lidb`.
- **`docs_maintainer` live Pages** for `lic` — separate heap task (`repos_without_live_docs`: 1, Pages down).
- **Merge program / pr_branch_opener** — out of scope (`--skip-slow` briefing).
- **New repo discovery** — no action until a repo appears on GitHub outside the known set.

## Error

None this pass. Discovery refresh succeeded: `github=35 known=35 new=0 stale=0`.
