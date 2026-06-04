#!/usr/bin/env python3
"""PH-5b catalog honesty pass for benchmarks#266 (sub-phases B–C + lis tier-5 paths).

- Purge bogus competitive-vertical remaps (bio_*, drug_*, am_* → shared tier1/tier2 paths).
- Mark rows without a resolvable harness as catalog_lifecycle = planned.
- Align lis tier-5 scenario paths with vendor/lis-tier5 layout (no workloads/ prefix).

Run after fix-catalog-repo-field.py. Does not delete catalog rows.

Usage:
  python3 scripts/catalog/apply-catalog-audit-honesty.py --dry-run
  python3 scripts/catalog/apply-catalog-audit-honesty.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
VENDOR_LIS = ROOT / "vendor/lis-tier5"

# bio/drug competitive stubs — must not alias tier1_micro numerics paths.
VERTICAL_STUB_IDS = frozenset(
    {
        "bio_proteinmpnn",
        "bio_rfdiffusion",
        "bio_rosetta_energy",
        "bio_rotamer_packing",
        "drug_docking_diffusion",
        "drug_docking_score_vina",
        "drug_fep_alchemical",
        "drug_litl_stages",
        "drug_ml_retrain_loop",
        "am_export_gcode_3mf",
        "am_infill_grid_lines",
        "am_infill_gyroid",
        "am_offset_perimeters",
        "am_plane_mesh_intersect",
        "am_polygon_clip",
        "am_slice_layers",
        "am_support_tree",
        "am_thermal_warp",
        "am_toolpath_arcs",
    }
)

# No harness under benchmarks / vendor / lic in agent workspace — honest deferral.
PLANNED_NO_HARNESS = frozenset(
    {
        "tier0_stability",
        "ml_conv2d_forward",
        "ml_mlp_forward",
        "ml_mlp_train_step",
        "proxy_loopback",
    }
)

BENCHMARK_KEYS = (
    "id",
    "base_id",
    "category",
    "pillar",
    "package",
    "tier",
    "repo",
    "path",
    "metric",
    "threshold_ratio_cpp",
    "compare_oracle",
    "variant",
    "problem_size",
    "size_label",
    "validity_required",
    "catalog_lifecycle",
)


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


def format_benchmark(b: dict) -> str:
    lines = ["[[benchmark]]", f'id = "{b["id"]}"']
    for key in BENCHMARK_KEYS:
        if key == "id" or key not in b or b[key] is None:
            continue
        val = b[key]
        if isinstance(val, bool):
            lines.append(f"{key} = {'true' if val else 'false'}")
        elif isinstance(val, (int, float)):
            lines.append(f"{key} = {val}")
        else:
            lines.append(f'{key} = "{val}"')
    ph = b.get("ph_ids") or []
    if ph:
        lines.append("ph_ids = [" + ", ".join(f'"{p}"' for p in ph) + "]")
    return "\n".join(lines)


def lis_tier5_path(rel: str) -> str | None:
    """Return vendor-relative path when workloads/ prefix is wrong for lis-tier5."""
    if not rel.startswith("benchmarks/workloads/tier5_http/"):
        return None
    alt = rel.replace("benchmarks/workloads/tier5_http/", "benchmarks/tier5_http/", 1)
    if (VENDOR_LIS / alt).is_dir() or (VENDOR_LIS / alt).is_file():
        return alt
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    import tomllib

    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    vertical = 0
    planned = 0
    tier5 = 0

    for b in benchmarks:
        bid = b["id"]
        if bid in VERTICAL_STUB_IDS:
            b["path"] = "unknown"
            b["catalog_lifecycle"] = "planned"
            b["variant"] = "vertical_stub"
            vertical += 1
            continue

        if bid in PLANNED_NO_HARNESS:
            b["path"] = "unknown"
            b["catalog_lifecycle"] = "planned"
            planned += 1
            continue

        if str(b.get("repo")) == "lis":
            rel = str(b.get("path") or "")
            alt = lis_tier5_path(rel)
            if alt:
                b["path"] = alt
                tier5 += 1

    print(f"vertical_stub rows: {vertical}")
    print(f"planned (no harness): {planned}")
    print(f"lis tier5 path fixes: {tier5}")

    if args.dry_run and not args.write:
        return 0
    if not args.write:
        print("pass --write to update catalog.toml", file=sys.stderr)
        return 1

    header = load_header(text)
    CATALOG.write_text(
        header + "\n\n".join(format_benchmark(b) for b in benchmarks) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
