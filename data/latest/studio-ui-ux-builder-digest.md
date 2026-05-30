# Studio UI/UX builder — proactive sweep digest

**Generated:** 2026-05-30T01:04Z  
**Workflow repo:** `lic` (`cursor/studio-ui-ux-plan-loop`)  
**Worktree:** `lic-studio-ui` (synced to `origin/cursor/studio-ui-ux-plan-loop`)

## Executive summary

- Completed plan-loop slice **`studio-ux-12-world-studio-demo-linux-audit`**: Linux non-mock `world-studio-demo` ux-harness audit wired into gates and capture.
- Extended **`li-cursor-agents/ux-harness`** `web_gui` adapter with `agentic_ai` SOTA refs (`cursor-agent`, `linear-app`, `github-copilot-workspace`) and real journey payloads for fixture probes.
- **`./scripts/studio-ui-ux-plan-gates.sh`** passes (build skipped): bench registry, panel_switch 95ms, memory 0.46 MiB, harness audit OK.
- Capture dry run exit **0**; GitHub publish skipped (dry + API rate limit on `agent-repo-workflow prepare`).
- Briefing preflight refreshed: ecosystem audit green, 6 red numerics rows, 9 agent-kit drift repos, security_cwe_audit JSON flake.
- Native SDL capture still gap-documented (`libsdl2` missing on host); HTML mocks remain labeled fallback.
- PH-UX gates pass on **simulate** hooks — honest `native_pixels: false` in bench JSON.
- Next gap backlog: wgpu viewport grid (UX-01), native vs mock honesty (UX-12), `gui_ux_tester` workflow_repo routing.

## Studio UI/UX iteration

- **todo:** `studio-ux-12-world-studio-demo-linux-audit`
- **UX dimensions:** UX-01 2.2 viewport SDL stub · UX-02 2.8 timeline · UX-03 2.8 inspector · UX-04 2.5 palette · UX-05 3 profiles · UX-06 2.4 agent chrome+harness SOTA · UX-07 3 empty states · UX-08 2 error mock · UX-09 3 keyboard · UX-10 3.2 a11y tokens · UX-11 3 loading · UX-12 2.4 Linux harness pass · UX-13 2.5 bench honest · UX-14 2.8 mock labeling
- **PH-UX gates:** viewport_fps_target **60** (simulate, meets) · panel_switch_ms **95** (<100) · particle tiers md_1k/10k/100k **simulate meets**
- **Capture:** `./scripts/studio-ui-ux-capture-progress.sh` exit **0** (dry); issue **#182** — publish deferred (rate limit / dry)
- **Bench:** `load_ms=0.11`, `md_particles` tiers simulate @ 60/60/30 fps, `memory_mib` peak **0.46** (budget 512)
- **Regressions:** none vs `studio-ux-11` (UX-06 +0.1, UX-12 +0.2 from harness closure)

## Deliverable / findings

| Area | Result |
|------|--------|
| Harness | `studio-ui-ux-verify-harness-audit.py` runs `world-studio-demo` on Linux without `--mock` |
| Capture | Non-mock on Linux when `STUDIO_UI_UX_HARNESS_MOCK≠1` |
| SOTA | Cursor agent overview, Linear, Copilot refs in ux audit JSON |
| Gates | All green with `STUDIO_UI_UX_GATES_SKIP_BUILD=1` |

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| `feat(studio-ui): Linux world-studio-demo harness audit (studio-ux-12)` | `lic` | `li-swarm`, `studio-ui`, `agent:studio_ui_ux_builder` |
| `fix(ux-harness): agentic SOTA refs for world-studio-demo fixture UX` | `li-cursor-agents` | `ux-harness`, `agent:studio_ui_ux_builder` |
| `chore(agent-kit): sync 9 drifted org repos to kit 1.3.5` | multi | `agent-kit` |
| `gap: UX-01 full li-render wgpu viewport grid` | `lic` | `studio-ui`, `PH-UX` |
| `gap: gui_ux_tester workflow_repo → lic-studio-ui ux-harness` | `li-cursor-agents` | `studio-ui` |

## Deferred

- GitHub capture upload to issue #182 / release `studio-ui-ux-progress` (API rate limit; re-run without `STUDIO_UI_UX_CAPTURE_DRY`)
- Playwright/axe extended audit on `world-studio-demo` HTML
- Native Xvfb/SDL pixels when `libsdl2` available
- `httpd` / tier5 (out of loop scope)
- Wave-2 gap orchestrator items (`gap-ux-studio-wave2-*`)
