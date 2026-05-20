# Li language docs: editor-style highlighted code PNGs

## Summary

Added `docs/language/` with real `lic` / benchmarks `.li` examples, **`scripts/render-li-code-image.py`** (Pygments `LiLexer` + Pillow editor chrome), and three **syntax-highlighted code screenshots** — not marketing poster cards.

## Agent continuation

1. **Read:** `docs/language/README.md`, `style-types-and-classes.md`, `execution-decorators-intro.md`.
2. **Run:** `pip install -r scripts/requirements-docs-visual.txt && python3 scripts/render-li-code-image.py --all`.
3. **Then:** extend `LiLexer` in the render script when new keywords ship; keep `docs/language/examples/*.li` synced with `lic` `li-tests` paths.
4. **Blocked on:** full IDE-quality highlighting in `lic` itself — this repo only documents/shares via Pygments for now.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Language docs | `docs/language/README.md`, `style-types-and-classes.md`, `execution-decorators-intro.md` | Real `type … = object` + `@parallel` text from `lic` tests |
| Examples | `docs/language/examples/*.li` | Vendored from `lic` encapsulation/decorators + benchmarks ingest |
| Renderer | `scripts/render-li-code-image.py`, `scripts/requirements-docs-visual.txt` | Editor-style PNG export (~30 KiB each) |
| Shareables | `docs/language/assets/li-code-*-editor.png` | Three highlighted screenshots |
| Handbook | `docs/handbook/README.md` | Link to `docs/language/` |

## Not changed

- `lic` compiler, `catalog.toml`, ingest scripts, CI workflows.
- Dashboard / numerics study content.
- `lic` compiler lexer / IDE LSP highlighting — shareables use Pygments in benchmarks only.

## Breaking / Security / Performance / Downstream

| Topic | Status |
|-------|--------|
| **Breaking** | N/A |
| **Security** | N/A — static docs and PNGs only |
| **Performance** | N/A — PNGs ~30 KiB each after editor render (replaces ~3 MB marketing cards) |
| **Downstream** | Social posts can deep-link to raw GitHub PNG URLs or copy from `docs/language/assets/` |
