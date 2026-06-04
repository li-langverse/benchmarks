#!/usr/bin/env python3
"""Fix catalog.toml repo field and bogus competitive-vertical path remaps (PH-5b / #266).

Sub-phase A: set ``repo = "benchmarks"`` when the path exists under this repo.
Sub-phase B: replace tier1_micro aliases on bio_/drug_ vertical ids with tier2_physics harness paths.

Usage:
  python3 scripts/catalog/fix-catalog-repo-field.py --dry-run
  python3 scripts/catalog/fix-catalog-repo-field.py --write
"""
from __future__ import annotations

import argparse
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"

# Catalog ids that incorrectly reused tier1_micro kernels (issue #266 sub-phase B).
VERTICAL_HONEST_PATHS: dict[str, str] = {
    "bio_proteinmpnn": "benchmarks/workloads/tier2_physics/bio_proteinmpnn",
    "bio_rfdiffusion": "benchmarks/workloads/tier2_physics/bio_rfdiffusion",
    "bio_rosetta_energy": "benchmarks/workloads/tier2_physics/bio_rosetta_energy",
    "bio_rotamer_packing": "benchmarks/workloads/tier2_physics/bio_rotamer_packing",
    "drug_docking_diffusion": "benchmarks/workloads/tier2_physics/drug_docking_diffusion",
    "drug_docking_score_vina": "benchmarks/workloads/tier2_physics/drug_docking_score_vina",
    "drug_fep_alchemical": "benchmarks/workloads/tier2_physics/drug_fep_alchemical",
    "drug_litl_stages": "benchmarks/workloads/tier2_physics/drug_litl_stages",
    "drug_ml_retrain_loop": "benchmarks/workloads/tier2_physics/drug_ml_retrain_loop",
}


def path_exists_under(root: Path, rel: str) -> bool:
    if not rel or rel == "unknown":
        return False
    p = root / rel
    return p.is_dir() or p.is_file()


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


def format_benchmark(b: dict) -> str:
    keys = (
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
    lines = ["[[benchmark]]", f'id = "{b["id"]}"']
    for key in keys:
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


def lis_vendor_tier5_path(rel: str) -> str | None:
    """Map ADR workloads path to vendored lis-tier5 when only vendor has harness."""
    prefix = "benchmarks/workloads/tier5_http/"
    if not rel.startswith(prefix):
        return None
    legacy = rel.replace("benchmarks/workloads/", "benchmarks/", 1)
    vendor_rel = f"vendor/lis-tier5/{legacy}"
    candidate = ROOT / vendor_rel
    if candidate.is_dir() or candidate.is_file():
        return vendor_rel
    return None


def apply_fixes(rows: list[dict]) -> tuple[int, int]:
    repo_fixes = 0
    path_fixes = 0
    for row in rows:
        bid = row["id"]
        rel = str(row.get("path", "")).strip()
        repo = str(row.get("repo", "lic"))

        vendor_path = lis_vendor_tier5_path(rel)
        if vendor_path and repo == "lis" and not path_exists_under(ROOT, rel):
            row["path"] = vendor_path
            path_fixes += 1
            continue

        if bid in VERTICAL_HONEST_PATHS:
            new_path = VERTICAL_HONEST_PATHS[bid]
            if rel != new_path and path_exists_under(ROOT, new_path):
                row["path"] = new_path
                path_fixes += 1
                row["repo"] = "benchmarks"
                repo_fixes += 1
                continue

        if rel.startswith("benchmarks/") and path_exists_under(ROOT, rel):
            if repo in ("lic", "lig", "lis") and repo != "benchmarks":
                row["repo"] = "benchmarks"
                repo_fixes += 1
    return repo_fixes, path_fixes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    text = CATALOG.read_text(encoding="utf-8")
    rows = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    repo_fixes, path_fixes = apply_fixes(rows)
    print(f"repo -> benchmarks: {repo_fixes} rows")
    print(f"vertical honest paths: {path_fixes} rows")

    if args.dry_run and not args.write:
        return 0
    if not args.write:
        print("pass --write to update catalog.toml", file=sys.stderr)
        return 1

    header = load_header(text)
    CATALOG.write_text(header + "\n\n".join(format_benchmark(b) for b in rows) + "\n", encoding="utf-8")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
