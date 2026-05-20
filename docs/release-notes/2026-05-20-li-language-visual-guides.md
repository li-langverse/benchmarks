# Li language docs: naming, class sketch, decorator cards

## Summary

Added `docs/language/` with PascalCase-vs-camelCase guidance, an illustrative class/visibility example, execution-decorator intro grounded in `lic`’s `std/execution/decorators.li`, and two **shareable PNG** cards under `docs/language/assets/`.

## Agent continuation

1. **Read:** `docs/language/README.md`, `style-types-and-classes.md`, `execution-decorators-intro.md`.
2. **Run:** N/A (docs + static images only).
3. **Then:** When `lic` ships real class syntax, replace the **illustrative** snippet with a conformance-tested example and link `li-tests` paths.
4. **Blocked on:** `lic` parser/keyword choices (`pub` vs `public`) and OOP phase landing — benchmarks docs stay descriptive.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Language docs | `docs/language/README.md`, `style-types-and-classes.md`, `execution-decorators-intro.md` | Style table, visibility cheat sheet, decorator list from upstream `decorators.li` |
| Shareables | `docs/language/assets/*.png` | Two 1080×1080 cards for social posts |
| Handbook | `docs/handbook/README.md` | Link to `docs/language/` |

## Not changed

- `lic` compiler, `catalog.toml`, ingest scripts, CI workflows.
- Dashboard / numerics study content.
- Normative grammar remains in `lic`; illustrative class block is explicitly labeled draft.

## Breaking / Security / Performance / Downstream

| Topic | Status |
|-------|--------|
| **Breaking** | N/A |
| **Security** | N/A — static docs and PNGs only |
| **Performance** | N/A — large PNGs in git (~3MB total); compress or move to CDN if size becomes an issue |
| **Downstream** | Social posts can deep-link to raw GitHub PNG URLs or copy from `docs/language/assets/` |
