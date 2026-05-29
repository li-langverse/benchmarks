# TUI UI tester digest — 2026-05-29 (proactive cycle 3)

**Agent:** `tui_ui_tester` · **Source:** proactive ecosystem sweep  
**Preflight:** `data/latest/ui-audit.json` (docs-only); TUI harness → `data/latest-tui-ui-run/ui-audit.json`  
**north_star_fit:** Easy pillar — terminal surfaces for `lic` diagnostics and agent workflows must be readable and automatable before perf work; proof-first (`lic build` certificates), no `unsafe` UI shortcuts. **PH:** PH-2i-adjacent-tooling, Vision-LLM.

---

## Executive summary

- Org **`ui-audit.json` preflight** audits **`lic-docs` only** — zero `surface:tui` targets in briefing snapshot (coord gap).
- **`tui-app-fixture` fails** — `read -r` blocks non-TTY harness (`TimeoutExpired` @ 30s); **piped stdin passes** (exit 0, capture refreshed).
- **`tui-gen-fixture` passes** — Unicode box frame (31 cols), no ANSI color, deterministic stdout.
- **Harness gap:** `run_audit.py` **crashes** on timeout instead of returning `fail` + `harness_error` (regression vs manual JSON).
- **No frame artifacts** — TUI adapter sets `artifacts: []`; no VHS/PTY PNG or ANSI contrast scan.
- **Remediation:** [#30](https://github.com/li-langverse/li-cursor-agents/issues/30) (P1, open) — non-interactive fixture.
- **Org catalog:** no production `surface:tui` repos in `ux-targets.json` beyond fixtures; `ui` repo is GUI, not terminal.
- **Control plane:** prior `tui_ui_tester` runs today mostly `error`; current run completes digest + artifacts.

---

## Deliverable / findings

### Preflight (`ui_audit`)

| Signal | Value |
|--------|--------|
| Briefing `data/latest/ui-audit.json` | 1 target (`lic-docs`), 0 failing — **TUI not in org preflight** |
| TUI re-run `data/latest-tui-ui-run/ui-audit.json` | 2 targets, **1 failing** (`tui-app-fixture`) |
| `tui-app-fixture` | **fail** — `TimeoutExpired` @ 30s (harness); piped demo OK |
| `tui-gen-fixture` | pass, `fixture_exit_code: 0` |
| Artifacts (harness) | none (`mode: fixture`) |
| Pixel / contrast | stub metrics only |

### Terminal frame review (fixture demos)

**`tui-app-fixture` (`tui-demo.sh`)** — capture: `captures/tui-app-piped.txt`

| Check | Result | Severity |
|-------|--------|----------|
| Non-interactive CI | Blocks on `read -r` ×2 without stdin | **P1** |
| ANSI layout | Clear + home (`ESC[2J` `ESC[H`); 3 content lines, max 56 cols | OK (minimal) |
| Color contrast | No fg/bg colors | N/A |
| Layout density | Sparse single-column prompts | P2 (fixture) |
| Help path | Text-only mock — not exercised in harness | P2 |

**`tui-gen-fixture` (`tui-gen-demo.sh`)** — capture: `captures/tui-gen.txt`

| Check | Result | Severity |
|-------|--------|----------|
| Exit code | 0 | OK |
| Box drawing | `┌─┐│└` frame, 31 cols, 5 lines | OK |
| ANSI color | None | P2 when real generator lands |
| Density | Readable stub panel | OK |
| Narrow terminal | No wrap/truncation test | P2 |

### SOTA reference (terminal UI)

| Source | URL | Takeaway for Li |
|--------|-----|-----------------|
| Textual testing | https://textual.textualize.io/guide/testing/ | Inject input via pilot — never block CI on `read` |
| Ratatui | https://ratatui.rs/ | Buffer + widget layout; snapshot tests |
| VHS | https://github.com/charmbracelet/vhs | `.tape` recordings for visual audit artifacts |
| WCAG contrast | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | ≥4.5:1 when color is used |

### Remediation issues

| Issue | Priority | Status |
|-------|----------|--------|
| [#30](https://github.com/li-langverse/li-cursor-agents/issues/30) tui-app-fixture blocks on read in non-interactive harness | P1 | Open (filed prior cycle) |

---

## Recommended issues/PRs

| Priority | Repo | Title | Labels |
|----------|------|-------|--------|
| P1 | `li-cursor-agents` | **[ui-audit] tui-app-fixture blocks on read in non-interactive harness** ([#30](https://github.com/li-langverse/li-cursor-agents/issues/30)) | `ui-audit`, `surface:tui`, `ready-for-implement` |
| P1 | `li-cursor-agents` | **feat(ux-harness): catch TimeoutExpired + stdout artifact for TUI fixtures** | `ui-audit`, `surface:tui` |
| P1 | `li-cursor-agents` | **feat(ux-harness): TUI frame capture (stdout dump or VHS) + baseline diff** | `ui-audit`, `surface:tui` |
| P1 | `benchmarks` | **chore(preflight): include `tui-app-fixture` + `tui-gen-fixture` in `ui-ux-audit` / briefing** | `ui-audit` |
| P2 | `li-cursor-agents` | **feat(ux-targets): register org TUI repos when `lic` CLI TUI ships** | `ui-audit`, `surface:tui` |
| P2 | `li-cursor-agents` | **test(tui-gen): ANSI theme tokens + contrast check helper** | `ui-audit`, `surface:tui` |

**Suggested implementers:** `code_implementer` (harness/fixtures); `agent_kit_maintainer` (preflight wiring).

---

## Deferred

- **Production Li TUI apps** — no org targets until REPL/studio terminal UX lands in `lic`.
- **`tui_ux_tester` journey rubric** — blocked on stable non-interactive `tui-app-fixture`.
- **VHS / Playwright-terminal** — needs maintainer approval for CI deps.
- **Merge failed PRs** — out of scope (swarm policy).
- **WCAG contrast on monochrome fixtures** — apply when real color themes exist.

---

## Artifacts

- Preflight JSON: `benchmarks/data/latest/ui-audit.json`
- TUI re-run JSON: `benchmarks/data/latest-tui-ui-run/ui-audit.json`
- Captures: `benchmarks/data/latest-tui-ui-run/captures/`
- Remediation manifest: `benchmarks/data/latest-tui-ui-run/remediation_manifest.json`
- Harness: `python3 li-cursor-agents/ux-harness/run_audit.py --target tui-app-fixture --mode ui` (per target; wildcard unsupported)
