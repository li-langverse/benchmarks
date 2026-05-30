# Ecosystem audit — handbook Pages HEAD checks

**Date:** 2026-05-30

## Summary

- `scripts/ecosystem-audit.py` probes `https://li-langverse.github.io/<repo>/` for org package handbooks
- `repos_without_live_docs` and `live_docs_down` reflect live HTTP status (not a static repo list)
- Adds `metrics.repos_with_live_pages`

## Verification

After **lic** and **lis** Pages merge, re-run audit — expect `repos_without_live_docs: []`.
