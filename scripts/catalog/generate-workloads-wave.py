#!/usr/bin/env python3
"""Generate workloads under benchmarks/workloads from algo_registry family templates."""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKLOADS = ROOT / "benchmarks" / "workloads"

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
    "ml": ("matmul_naive", 1),
}


def tier_sub(tier: int) -> str:
    return "tier1_micro" if tier == 1 else "tier2_physics"


def main() -> int:
    lic = Path(os.environ.get("LIC_ROOT", ROOT.parent / "lic"))
    reg_path = lic / "benchmarks/competitive/algo_registry.json"
    if not reg_path.is_file():
        print(f"missing {reg_path}", file=sys.stderr)
        return 1
    reg = json.loads(reg_path.read_text())
    created = 0
    skipped = 0
    for algo in reg.get("algorithms", []):
        name = algo.get("name", "")
        family = algo.get("family", "")
        if family not in FAMILY_TEMPLATE:
            skipped += 1
            continue
        template_id, tier = FAMILY_TEMPLATE[family]
        sub = tier_sub(tier)
        src = WORKLOADS / sub / template_id
        dst = WORKLOADS / sub / name
        if dst.is_dir():
            skipped += 1
            continue
        if not src.is_dir():
            print(f"skip {name}: no template {src}", file=sys.stderr)
            skipped += 1
            continue
        shutil.copytree(src, dst)
        created += 1
    print(f"created={created} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
