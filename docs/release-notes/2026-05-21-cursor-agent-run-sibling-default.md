# cursor-agent-run: sibling li-cursor-agents default

**Repo:** benchmarks  
**Audience:** agents, local SDK users

## Summary

- `scripts/cursor-agent-run.sh` now resolves **li-cursor-agents** like `agent-briefing.py`: prefer sibling `../li-cursor-agents` when `package.json` exists, else `./li-cursor-agents`; `LI_CURSOR_AGENTS_ROOT` still wins.
- Clearer error message with both clone locations.
- [tooling-catalog.md](../ecosystem/tooling-catalog.md) + [cursor-agent-architecture.md](../ecosystem/cursor-agent-architecture.md) updated; [game-dev](../game-dev/README.md) linked from tooling catalog philosophy table.

## Test plan

- [ ] `bash -n scripts/cursor-agent-run.sh`
- [ ] With only `../li-cursor-agents` present, `./scripts/cursor-agent-run.sh --help` or `--mock` reaches node (if deps built).
