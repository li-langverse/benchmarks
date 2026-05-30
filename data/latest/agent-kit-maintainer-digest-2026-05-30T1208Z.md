# Agent-kit maintainer digest — 2026-05-30

**Run:** agent_kit_maintainer · coord_platform  
**Canonical stamp:** `1.3.5+6018e18bf2ed91f4`  
**north_star_fit:** Platform governance — secure agent workflow (PR-only, hooks, ecosystem gates); supports **proof → easy → fast** via consistent Cursor policy across org repos.

---

## Executive summary

- **8 repos** flagged in briefing; **6 already merged** to `main` on GitHub earlier today; **2 open PRs** rebased and mergeable.
- Rollout failure root cause: invalid `GH_TOKEN` in agent env (gh fell back to user PAT); GraphQL rate limit blocked `gh pr list` / `gh pr create` during control-plane pass.
- **Local audit:** `python3 scripts/ensure-org-agent-kit.py --local-only` → **OK: 12, needing sync: 0** after install + `sync-agent-kit.sh` on sibling clones.
- **Remote `main` adoption pending merge:** `li-demo`, `lic` only.

---

## Canonical kit

| Field | Value |
|-------|-------|
| Version | 1.3.5 |
| Stamp | 1.3.5+6018e18bf2ed91f4 |
| Source | `roadmap/agent-kit/` |

---

## Repo rollout status

| Repo | GitHub `main` | PR | Status |
|------|---------------|-----|--------|
| benchmarks | ✅ 1.3.5 | — | ok |
| lip | ✅ 1.3.5 | — | ok |
| lis | ✅ 1.3.5 | — | ok |
| lit | ✅ 1.3.5 | — | ok |
| li-httpd | ✅ 1.3.5 | [#18](https://github.com/li-langverse/li-httpd/pull/18) merged | ok |
| li-language | ✅ 1.3.5 | [#14](https://github.com/li-langverse/li-language/pull/14) merged | ok |
| li-net | ✅ 1.3.5 | [#16](https://github.com/li-langverse/li-net/pull/16) merged | ok |
| li-std-core | ✅ 1.3.5 | [#12](https://github.com/li-langverse/li-std-core/pull/12) merged | ok |
| li-std-math | ✅ 1.3.5 | [#13](https://github.com/li-langverse/li-std-math/pull/13) merged | ok |
| roadmap | ✅ 1.3.5 | [#25](https://github.com/li-langverse/roadmap/pull/25) merged | ok (governance — human merged) |
| **li-demo** | ❌ missing kit | [#15](https://github.com/li-langverse/li-demo/pull/15) **open**, mergeable | **awaiting human merge** |
| **lic** | ⚠️ 1.3.3 drift | [#379](https://github.com/li-langverse/lic/pull/379) **open**, mergeable | **awaiting human merge** |
| li-cursor-agents | ✅ 1.3.5 (local) | — | ok |

---

## Actions taken this pass

1. Verified isolated workspace clones under `li-cursor-agents/data/workspaces/` — agent-kit install present at canonical stamp.
2. **Rebased** `chore/agent-kit-sync-*` branches onto current `main` for **li-demo** and **lic**; force-pushed with lease.
3. Confirmed open PRs exist (REST API; GraphQL rate-limited for listing).
4. Installed agent-kit locally on sibling clones missing kit; added `scripts/sync-agent-kit.sh` where absent.
5. Re-ran org audit — all 12 repos pass locally.

---

## Install failures

None — `install-agent-kit.sh` succeeded in workspace clones and local siblings.

---

## Human follow-up

- [ ] Merge [li-demo#15](https://github.com/li-langverse/li-demo/pull/15) (first kit adoption for li-demo).
- [ ] Merge [lic#379](https://github.com/li-langverse/lic/pull/379) (1.3.3 → 1.3.5).
- [ ] Fix invalid `GH_TOKEN` in `li-cursor-agents/.env` / `.env.github` so rollout agents use PAT instead of exhausting GraphQL quota on failed auth retries.
- [ ] Delete stale `chore/agent-kit-sync-*` remote branches after merges (optional hygiene).

---

## Do not (confirmed)

- Did not self-merge governance or code PRs.
- Did not weaken `agent-kit/hooks/guard-*.sh`.
- Did not commit `.env` or API keys.

---

<!-- li-agent-agent-kit-maintainer-digest-v1 -->
