#!/usr/bin/env python3
"""Set catalog.toml repo=benchmarks when workload path exists in this repo (ADR).

Also repairs competitive-vertical rows that alias tier1_micro paths while a dedicated
tier2_physics/<id> harness exists (benchmarks#266 sub-phases A/B).

Usage:
  python3 scripts/catalog/fix-catalog-repo-field.py --dry-run
  python3 scripts/catalog/fix-catalog-repo-field.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"

VERTICAL_REMAP_IDS = frozenset(
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
    }
)

LIC_ONLY_PREFIXES = ("li-tests/", "packages/", "vendor/")


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


def load_footer(text: str) -> str:
    """Preserve [reporting] and other trailing tables after benchmarks."""
    last = text.rfind("[[benchmark]]")
    if last == -1:
        return ""
    rest = text[last:]
    end = rest.find("\n\n[")
    if end == -1:
        return ""
    return rest[end + 2 :]


def format_benchmark(b: dict) -> str:
    keys = (
        "id",
        "base_id",
        "problem_size",
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


def path_exists_in_repo(rel: str) -> bool:
    if not rel or rel == "unknown":
        return False
    p = ROOT / rel
    return p.is_dir() or p.is_file()


def is_lic_only_path(rel: str) -> bool:
    return any(rel.startswith(p) for p in LIC_ONLY_PREFIXES)


def dedicated_tier2_path(bench_id: str) -> str | None:
    rel = f"benchmarks/workloads/tier2_physics/{bench_id}"
    return rel if path_exists_in_repo(rel) else None


def apply_fixes(benchmarks: list[dict], *, verbose: bool) -> tuple[int, int, int]:
    repo_fixes = remap_fixes = am_fixes = 0
    for b in benchmarks:
        bench_id = b["id"]
        rel = str(b.get("path") or "").strip()
        repo = str(b.get("repo") or "lic")
        dedicated = dedicated_tier2_path(bench_id)

        if bench_id in VERTICAL_REMAP_IDS and dedicated:
            if rel != dedicated or repo != "benchmarks":
                if verbose:
                    print(f"  remap {bench_id}: {rel} ({repo}) -> {dedicated}")
                b["path"] = dedicated
                b["repo"] = "benchmarks"
                b["variant"] = "shared_c_kernel"
                b.pop("catalog_lifecycle", None)
                remap_fixes += 1
            continue

        if bench_id.startswith("am_") and dedicated and rel != dedicated:
            if verbose:
                print(f"  am path {bench_id}: {rel} -> {dedicated}")
            b["path"] = dedicated
            b["repo"] = "benchmarks"
            b["variant"] = "shared_c_kernel"
            am_fixes += 1
            continue

        if repo == "lic" and rel and not is_lic_only_path(rel) and path_exists_in_repo(rel):
            if verbose:
                print(f"  repo {bench_id}: lic -> benchmarks")
            b["repo"] = "benchmarks"
            repo_fixes += 1

    return repo_fixes, remap_fixes, am_fixes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.write:
        print("pass --dry-run or --write", file=sys.stderr)
        return 1

    import tomllib

    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    repo_fixes, remap_fixes, am_fixes = apply_fixes(benchmarks, verbose=True)
    print(f"repo={repo_fixes} vertical_remap={remap_fixes} am_path={am_fixes}")

    if args.write and (repo_fixes or remap_fixes or am_fixes):
        header = load_header(text)
        footer = load_footer(text)
        body = header + "\n\n".join(format_benchmark(b) for b in benchmarks) + "\n"
        if footer:
            body += "\n" + footer.rstrip() + "\n"
        CATALOG.write_text(body, encoding="utf-8")
        print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
