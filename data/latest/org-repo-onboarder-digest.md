# Org repo onboarder digest — 2026-05-30T0229Z

**Agent:** `org_repo_onboarder` · **Source:** proactive sweep · discovery `2026-05-30T02:29Z` · CI audit `2026-05-30T02:14Z` · agent-kit audit `2026-05-30T02:29Z` · briefing `2026-05-30T02:05Z`

## Executive summary

- **Discovery (refreshed):** `github=34` `known=33` **`new=1`** **`stale=0`** — one net-new org repo detected: **`li-gui`**.
- **Highest-risk new repo:** **`li-gui`** (`candidate_official`) — on GitHub since 2026-05-25, not in catalog/known set; no local clone, no agent-kit, catalog registration blocked until CI + kit path complete.
- **No stale catalog entries** — all 33 known repos still exist on GitHub; no archive/delete candidates this cycle.
- **li-gui live posture:** `main` default; **`ci.yml`** + **`ecosystem-upstream.yml`** present on GitHub (CI audit rate-limited — treat as verify, not greenfield bootstrap); open PR [#2](https://github.com/li-langverse/li-gui/pull/2) (deps bump) **CI red**.
- **Platform hygiene (existing):** `lidb` gated on non-`main` default (`feat/ph-db-2-liorm-liq`); **29** repos missing/drifted agent-kit; canonical stamp `1.3.5+6018e18bf2ed91f4`.
- **CI audit caveat:** `org-repo-ci-audit.json` hit GitHub API rate limits — **29** repos marked `audit_incomplete`; re-run audit before treating CI posture as authoritative.
- **Control plane:** security queue already includes `security:repo:li-gui`; **no** `org_repo_onboarding` rows yet — onboarder recommends enqueue below.
- **North star:** `li-gui` placement review gates **easy** (GUI/onboarding UX) + **provable** package mirror discipline — defer perf until proof CI green.

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 34 |
| Known (audits + core list) | 33 |
| **New** | **1** |
| **Stale known** | **0** |

Preflight artifacts: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

**Note:** `agent-briefing.py` does not yet embed `org_new_repos_discovery` in `agent-briefing.json` — use discovery JSON directly until preflight hook lands.

### New repos (classification + handoffs)

| Repo | Classification | CI (live) | Agent-kit | Recommended handoffs |
|------|----------------|-----------|-----------|----------------------|
| **`li-gui`** | **`candidate_official`** | `ci.yml` present on `main` (verify green); PR #2 red | `missing_local_clone` / no `.cursor/rules` on GitHub | `ci_maintainer` → verify; `agent_kit_maintainer` → sync; `docs_maintainer` → live docs smoke; `package_architect` → placement review; `code_implementer` → catalog (after CI + kit) |

**Classification rationale:** `li-gui` matches `classify_new_repo()` — `li-*` prefix, not in `core_tooling` or `official_mirror` lists. GitHub description: *"Li package mirror (li-gui)"* — likely official PKG mirror (alongside `ui`, `render`); needs `package_architect` confirmation vs experimental fork.

### Onboarding plan — `li-gui`

Downstream agents own isolated clone PRs; onboarder does **not** open PRs or edit sibling working trees.

| Step | Agent | Action | Notes |
|------|-------|--------|-------|
| 1 | `ci_maintainer` | `verify_ci_yml` | Workflows exist on `main`; confirm org policy compliance + fix PR #2 red CI |
| 2 | `agent_kit_maintainer` | `sync_agent_kit` | Clone workspace first (`missing_local_clone`); install canonical stamp `1.3.5+6018e18bf2ed91f4` |
| 3 | `docs_maintainer` | `live_docs_smoke` | Handbook / Pages path for GUI package mirror |
| 4 | `package_architect` | `placement_review` | Official PKG vs experimental; record via `record_placement_decision` |
| 5 | `code_implementer` | `register_in_catalog` | **After** steps 1–2 green — add to org catalog / work-queue targets |

### Stale catalog entries

*None this cycle.* No archive/delete without human approval.

### Catalog sync (reference classification buckets)

| Bucket | Repos |
|--------|-------|
| **core_tooling** | `lic`, `li-language`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap`, `li-cursor-agents` |
| **official_mirror** | `li-net`, `li-httpd`, `li-std-core`, `li-std-math`, `li-demo`, `net.httpd` |
| **candidate_official** | **`li-gui`**, `li-local-ci`, `lidb` |
| **unclassified** (domain packages) | `proof-library`, `sim*`, `physics.*`, `render`, `studio`, `studio.ai`, `ui`, `world`, `mmo`, `store.realtime`, `research-findings` |

### Existing-repo hygiene (not “new repo”)

| Repo / scope | Agent | Action | Notes |
|--------------|-------|--------|-------|
| 29 repos | `agent_kit_maintainer` | `sync_agent_kit` | 26 `missing_kit`, 3 `drift` (`lic`, `lis`, `roadmap`) |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | Set default branch `main` before enforcing `ci.yml` on default |
| `research-findings` | — | — | CI-exempt per org policy |

### Handoff queue (control plane)

**New-repo onboarding (`org_repo_onboarding`):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `li-gui` | `verify_ci_yml` | platform / secure — confirm CI before catalog |
| `agent_kit_maintainer` | `li-gui` | `sync_agent_kit` | ai-first — isolated clone + canonical kit |
| `docs_maintainer` | `li-gui` | `live_docs_smoke` | easy — GUI mirror handbook path |
| `package_architect` | `li-gui` | `placement_review` | provable — official PKG vs experimental |
| `code_implementer` | `li-gui` | `register_in_catalog` | ecosystem — after CI + kit (blocked until then) |

**Existing hygiene (retain from prior heap):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `lidb` | `wp_h0_main_default` | platform / secure |
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` | drift |
| `agent_kit_maintainer` | `lis` | `sync_agent_kit` | drift |
| `agent_kit_maintainer` | `roadmap` | `sync_agent_kit` | drift |
| `agent_kit_maintainer` | `li-demo` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-httpd` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-language` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-net` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-std-core` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-std-math` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | missing_kit (after WP-H0) |
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable surface |
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `world` | `sync_agent_kit` | missing_kit |

*(Remaining `missing_kit` repos from `org-agent-kit-audit.json` — enqueue via heap `agent_kit_maintainer` batch.)*

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `li-gui` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `chore`, `onboarding` |
| `li-gui` | fix(ci): resolve PR #2 check failure (actions/checkout bump) | `ci`, `dependencies` |
| `li-gui` | docs: live Pages smoke for li-gui package mirror | `docs`, `onboarding` |
| `benchmarks` | feat(package_architect): placement decision for li-gui | `placement`, `onboarding` |
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci` |
| `lic` | chore(agent-kit): align cursor stamp to canonical | `agent-kit`, `drift` |
| `proof-library` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `chore`, `provable` |

*(Do not self-merge. Route red CI on open PRs to `bug_fixer` / `ci_maintainer`.)*

## Deferred

- **Catalog registration for `li-gui`:** blocked until CI verified green + agent-kit PR merged.
- **Catalog pruning:** no stale entries; no archive/delete without human sign-off.
- **CI audit refresh:** re-run `org-repo-ci-audit` after GitHub rate limit resets (29 repos `audit_incomplete`).
- **Briefing preflight hook:** wire `discover-new-org-repos.py` into `agent-briefing.py` so `org_new_repos_discovery` embeds in `agent-briefing.json`.
- **`docs_maintainer` heap task:** 8 repos without live Pages — separate from onboarder registration.
- **Merge program / pr_branch_hygiene:** out of onboarder scope this run.
