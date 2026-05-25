#!/usr/bin/env python3
"""Set catalog path= for algo_registry rows that have generated harness dirs in lic."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
LIC_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "lic"
REGISTRY = LIC_ROOT / "benchmarks/competitive/algo_registry.json"
TIER1 = LIC_ROOT / "benchmarks/tier1_micro"
TIER2 = LIC_ROOT / "benchmarks/tier2_physics"

FAMILY_TEMPLATE: dict[str, tuple[str, int]] = {
    "num": ("matmul_naive", 1),
    "md": ("md_lennard_jones", 2),
    "pde": ("heat_equation_2d", 2),
    "rigid": ("heat_equation_2d", 2),
    "robo": ("three_body", 2),
    "am": ("advection_diffusion_2d", 2),
    "qm": ("heat_equation_2d", 2),
    "auto": ("advection_diffusion_2d", 2),
    "bio": ("heat_equation_2d", 2),
    "drug": ("heat_equation_2d", 2),
    "viz": ("reduce_sum", 1),
}


def harness_path(bench_id: str, tier: int) -> str:
    sub = "tier1_micro" if tier == 1 else "tier2_physics"
    return f"benchmarks/{sub}/{bench_id}"


def main() -> int:
    reg = json.loads(REGISTRY.read_text())
    text = CATALOG.read_text()
    updated = 0
    for entry in reg.get("algorithms", []):
        bid = entry["name"]
        family = entry.get("family", "")
        tpl = FAMILY_TEMPLATE.get(family)
        if not tpl:
            continue
        _, tier = tpl
        path = harness_path(bid, tier)
        dir_exists = (TIER1 if tier == 1 else TIER2) / bid
        if not dir_exists.is_dir():
            continue
        pattern = rf'(id = "{re.escape(bid)}"[\s\S]*?)^path = "unknown"'
        repl = rf'\1path = "{path}"'
        new_text, n = re.subn(pattern, repl, text, count=1, flags=re.M)
        if n:
            text = new_text
            updated += 1
    CATALOG.write_text(text)
    print(f"wire-registry-paths: updated {updated} catalog rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
