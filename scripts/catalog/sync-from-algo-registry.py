#!/usr/bin/env python3
"""Append catalog.toml stubs from lic competitive/algo_registry.json.

Each registry algorithm not already represented in the catalog gets a
[[benchmark]] row (path ``unknown`` until a harness dir exists). Existing
harness-backed ids are linked via CATALOG_ID_ALIASES and tier1/tier2 path
detection under LIC_ROOT.

Usage:
  python3 scripts/catalog/sync-from-algo-registry.py --dry-run
  python3 scripts/catalog/sync-from-algo-registry.py --write
  LIC_ROOT=../lic python3 scripts/catalog/sync-from-algo-registry.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
DEFAULT_LIC = ROOT.parent / "lic"

# Registry name -> existing catalog id (do not duplicate stubs).
CATALOG_ID_ALIASES: dict[str, str] = {
    "num_matmul_naive": "matmul_naive",
    "num_matmul_blocked": "matmul_blocked",
    "num_dot_axpy": "simd_dot",
    "md_lj_cutoff_mic": "md_lennard_jones",
    "nbody_pairwise_gravity": "nbody_gravity",
    "pde_heat_explicit_2d": "heat_equation_2d",
    "pde_wave_1d_cfl": "wave_equation_1d",
}

TIER2_PATH_ALIASES: dict[str, str] = dict(CATALOG_ID_ALIASES)

FAMILY_META: dict[str, dict[str, object]] = {
    "num": {"category": "micro", "pillar": "numerics", "tier": 1},
    "md": {"category": "physics", "pillar": "physics", "tier": 2},
    "pde": {"category": "physics", "pillar": "physics", "tier": 2},
    "rigid": {"category": "physics", "pillar": "physics", "tier": 2},
    "qm": {"category": "physics", "pillar": "physics", "tier": 2},
    "drug": {"category": "physics", "pillar": "physics", "tier": 2},
    "bio": {"category": "physics", "pillar": "physics", "tier": 2},
    "ml": {"category": "micro", "pillar": "numerics", "tier": 1},
    "am": {"category": "tooling", "pillar": "tooling", "tier": 3},
    "viz": {"category": "micro", "pillar": "graphics", "tier": 1},
    "robo": {"category": "physics", "pillar": "physics", "tier": 2},
    "auto": {"category": "physics", "pillar": "physics", "tier": 2},
}

TIER2_GAP_IDS = (
    "three_body_pure",
    "schrodinger_1d_barrier",
    "ragdoll_chain",
    "orbit_two_body",
    "fdtd_waveguide_2d",
)

MARKER_BEGIN = "# --- algo_registry sync"
MARKER_END = "# --- end algo_registry sync"


def load_catalog_ids(catalog_text: str) -> set[str]:
    import tomllib

    data = tomllib.loads(catalog_text)
    return {b["id"] for b in data.get("benchmark", [])}


def load_registry(lic_root: Path) -> list[dict]:
    path = lic_root / "benchmarks/competitive/algo_registry.json"
    if not path.is_file():
        raise SystemExit(f"missing algo_registry: {path}")
    data = json.loads(path.read_text())
    return list(data.get("algorithms") or [])


def stem_candidates(name: str) -> list[str]:
    out = [name]
    if "_" in name:
        prefix, rest = name.split("_", 1)
        if prefix in FAMILY_META:
            out.append(rest)
    return out


def resolve_path(name: str, lic_root: Path) -> str:
    alias_dir = TIER2_PATH_ALIASES.get(name, name)
    tier2 = lic_root / "benchmarks/tier2_physics"
    tier1 = lic_root / "benchmarks/tier1_micro"
    for stem in stem_candidates(name):
        for base, label in ((tier2, "tier2_physics"), (tier1, "tier1_micro")):
            if (base / stem).is_dir():
                return f"benchmarks/{label}/{stem}"
    if (tier2 / alias_dir).is_dir():
        return f"benchmarks/tier2_physics/{alias_dir}"
    if (tier1 / alias_dir).is_dir():
        return f"benchmarks/tier1_micro/{alias_dir}"
    return "unknown"


def catalog_id_for_registry(name: str, catalog_ids: set[str]) -> str | None:
    cid = CATALOG_ID_ALIASES.get(name, name)
    if cid in catalog_ids or name in catalog_ids:
        return None
    return cid


def format_block(
    *,
    bench_id: str,
    meta: dict[str, object],
    path: str,
    variant: str | None = None,
) -> str:
    lines = [
        "",
        "[[benchmark]]",
        f'id = "{bench_id}"',
        f'category = "{meta["category"]}"',
        f'pillar = "{meta["pillar"]}"',
        'package = "lic"',
        f'tier = {meta["tier"]}',
        'repo = "lic"',
        f'path = "{path}"',
        'metric = "wall_time"',
        "threshold_ratio_cpp = 1.2",
        'ph_ids = ["PH-5b"]',
        "validity_required = true",
    ]
    if variant:
        lines.append(f'variant = "{variant}"')
    return "\n".join(lines)


def build_registry_stubs(lic_root: Path, catalog_ids: set[str]) -> list[str]:
    blocks: list[str] = []
    for entry in load_registry(lic_root):
        name = str(entry.get("name") or "").strip()
        if not name:
            continue
        cid = catalog_id_for_registry(name, catalog_ids)
        if cid is None:
            continue
        family = name.split("_", 1)[0] if "_" in name else "num"
        meta = FAMILY_META.get(family) or {
            "category": "micro",
            "pillar": "numerics",
            "tier": 1,
        }
        path = resolve_path(name, lic_root)
        variant = "algo_registry" if path == "unknown" else None
        blocks.append(
            format_block(bench_id=cid, meta=meta, path=path, variant=variant)
        )
        catalog_ids.add(cid)
    return blocks


def build_tier2_gap_stubs(lic_root: Path, catalog_ids: set[str]) -> list[str]:
    blocks: list[str] = []
    tier2 = lic_root / "benchmarks/tier2_physics"
    for bench_id in TIER2_GAP_IDS:
        if bench_id in catalog_ids:
            continue
        if not (tier2 / bench_id).is_dir():
            print(f"warn: tier2 gap dir missing: {bench_id}", file=sys.stderr)
        meta = FAMILY_META["md"]
        path = f"benchmarks/tier2_physics/{bench_id}"
        blocks.append(format_block(bench_id=bench_id, meta=meta, path=path))
        catalog_ids.add(bench_id)
    return blocks


def strip_existing_sync_section(text: str) -> str:
    if MARKER_BEGIN not in text:
        return text.rstrip() + "\n"
    start = text.index(MARKER_BEGIN)
    end = text.find(MARKER_END, start)
    if end == -1:
        return text[:start].rstrip() + "\n"
    end = text.index("\n", end) + 1 if "\n" in text[end:] else len(text)
    return text[:start].rstrip() + "\n"


def append_sync_section(text: str, blocks: list[str]) -> str:
    if not blocks:
        return text
    base = strip_existing_sync_section(text)
    today = date.today().isoformat()
    header = (
        f"\n{MARKER_BEGIN} ({today}) — stubs from "
        "lic/benchmarks/competitive/algo_registry.json; path unknown until harness wired\n"
    )
    footer = f"\n{MARKER_END}\n"
    return base + header + "\n".join(blocks) + footer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lic-root",
        type=Path,
        default=Path(__import__("os").environ.get("LIC_ROOT", str(DEFAULT_LIC))),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--no-tier2-gaps", action="store_true")
    args = parser.parse_args()
    lic_root: Path = args.lic_root.resolve()
    if not lic_root.is_dir():
        raise SystemExit(f"LIC_ROOT not found: {lic_root}")

    catalog_text = CATALOG.read_text()
    catalog_ids = load_catalog_ids(catalog_text)
    before = len(catalog_ids)

    blocks = build_registry_stubs(lic_root, catalog_ids)
    if not args.no_tier2_gaps:
        blocks.extend(build_tier2_gap_stubs(lic_root, catalog_ids))

    added = len(catalog_ids) - before
    print(f"catalog before: {before}")
    print(f"stubs to add: {len(blocks)} (unique ids +{added})")
    print(f"catalog after: {len(catalog_ids)}")

    if args.dry_run and not args.write:
        return 0
    if not args.write:
        print("pass --write to update catalog.toml", file=sys.stderr)
        return 1

    CATALOG.write_text(append_sync_section(catalog_text, blocks))
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
