#!/usr/bin/env python3
"""Classify catalog.toml path gaps for PH-5b (implement / defer / fix_path).

Writes data/latest/catalog-gap-triage.json.

Env:
  LIC_ROOT — lic checkout (default: ../lic)
"""
from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from catalog.catalog_honesty import triage_catalog  # noqa: E402

CATALOG = ROOT / "catalog.toml"
OUT = ROOT / "data/latest/catalog-gap-triage.json"


def main() -> int:
    if not CATALOG.is_file():
        print(f"missing {CATALOG}", file=sys.stderr)
        return 1
    rows = tomllib.loads(CATALOG.read_text(encoding="utf-8")).get("benchmark", [])
    report = triage_catalog(rows)
    report["schema"] = "benchmarks/catalog-gap-triage/v1"
    report["catalog"] = str(CATALOG)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    s = report["summary"]
    print(
        f"wrote {OUT} "
        f"(ok={s.get('ok', 0)} fix_repo={s.get('fix_repo', 0)} "
        f"fix_path={s.get('fix_path', 0)} defer={s.get('defer_planned', 0)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
