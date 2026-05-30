## Summary

## Ecosystem-first

- [ ] Used [tooling-catalog](docs/ecosystem/tooling-catalog.md) / org scripts — **or** linked **`ecosystem-gap`** issue: #___

## Release notes (required)

Policy: https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/release-notes.md

Link: `docs/release-notes/YYYY-MM-DD-<slug>.md` (skill **write-li-release-notes**)

- [ ] **CHANGELOG.md** `## [Unreleased]` updated
- [ ] Dated `docs/release-notes/` with **Agent continuation** + **Not changed**

## Test plan

- [ ] CI green on PR

## GPU chip donation (if applicable)

- [ ] One folder under `data/gpu-contributions/<chip-slug>/` only — one physical machine
- [ ] `python3 scripts/ingest/validate-gpu-contribution.py` passes
- [ ] No hand-edited timings; suite re-run on donor hardware
- [ ] See [gpu-chip-contributions.md](docs/ecosystem/gpu-chip-contributions.md)
