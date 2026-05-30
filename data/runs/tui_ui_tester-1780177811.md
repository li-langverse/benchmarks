# tui_ui_tester run `tui_ui_tester-1780177811`

**Started:** 2026-05-30T21:50Z · **Source:** proactive · **Status:** complete

## Executive summary

- Org preflight `ui-audit.json` still **docs-only** (`lic-docs`); TUI requires proactive `data/latest-tui-ui-run/`.
- **`tui-app-fixture` fails** — `read -r` timeout; harness crashes uncaught (`TimeoutExpired` @ 30s).
- **Piped stdin workaround** captures 97 B ANSI frame (exit 0) — layout auditable once harness injects input.
- **`tui-gen-fixture` passes** — Unicode box frame (31 cols); harness omits stdout artifact on pass ([#48](https://github.com/li-langverse/li-cursor-agents/issues/48)).
- **UTF-8 mojibake** on em dash in `tui-demo.sh` title ([#49](https://github.com/li-langverse/li-cursor-agents/issues/49)).
- **No production Li TUI** in catalog; org repo `ui` awaits agent-kit before onboarding.
- **Control plane:** 10+ prior runs today ended `error`; this pass completes digest + remediation manifest.
- **SOTA refs:** Textual Pilot, Ratatui insta, VHS `.tape` for terminal visual audit.

## Deliverable / findings

See full tables: `docs/ecosystem/ux-digests/2026-05-30-tui-ui.md`

**Evidence:** `data/latest-tui-ui-run/ui-audit.json` (2026-05-30T21:50Z)

## Recommended issues/PRs

P1: [#30](https://github.com/li-langverse/li-cursor-agents/issues/30), [#48](https://github.com/li-langverse/li-cursor-agents/issues/48), harness TimeoutExpired fix, benchmarks preflight TUI merge  
P2: [#49](https://github.com/li-langverse/li-cursor-agents/issues/49), ANSI theme contrast helper, lic TUI export spec

## Deferred

Production Li TUI, `ui` repo audit, `tui_ux_tester` rubric, VHS CI, org preflight merge, merge PRs / GHA cron.
