#!/usr/bin/env python3
"""Sync catalog.toml paths from benchmarks workloads (ADR) and optional legacy lic tree.

Primary scan: ``benchmarks/workloads/tier*`` under this repo (benchmarks-only ADR).
Legacy ``LIC_ROOT/benchmarks/tier*`` is opt-in via ``--include-legacy-lic`` (deprecated).
Sets ``path`` and ``repo=benchmarks`` when a harness dir exists under workloads.
Optionally regenerates ``data/latest/summary.json`` when ``results/latest.csv`` exists.

Usage:
  python3 scripts/catalog/sync-paths-from-lic-tree.py --dry-run
  python3 scripts/catalog/sync-paths-from-lic-tree.py --write
  LIC_ROOT=../lic python3 scripts/catalog/sync-paths-from-lic-tree.py --write --include-legacy-lic
"""
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
DEFAULT_LIC = ROOT.parent / "lic"
DEFAULT_LIS = ROOT.parent / "lis"
INGEST = ROOT / "scripts/ingest/build_summary.py"
CSV_REL = Path("results/latest.csv")

SKIP_PATH_PREFIXES = (
    "li-tests/",
    "vendor/",
    "benchmarks/tier5_http/harness/",
    "benchmarks/viewport/",
    "benchmarks/ml/",
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


def load_sync_registry_module():
    path = Path(__file__).parent / "sync-from-algo-registry.py"
    spec = importlib.util.spec_from_file_location("sync_from_algo_registry", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def scan_harness_index(
    lic_root: Path | None,
    bench_root: Path | None = None,
    *,
    include_legacy_lic: bool = False,
) -> dict[str, str]:
    """Map harness directory stem -> catalog path (benchmarks/workloads/... preferred)."""
    index: dict[str, str] = {}
    bench_root = bench_root or ROOT
    sources: list[tuple[Path, str]] = []
    workloads = bench_root / "benchmarks" / "workloads"
    if workloads.is_dir():
        sources.append((workloads, "benchmarks/workloads"))
    if include_legacy_lic and lic_root is not None:
        legacy = lic_root / "benchmarks"
        if legacy.is_dir():
            sources.append((legacy, "benchmarks"))
    if not sources:
        return index

    for bench, prefix in sources:
        for tier in sorted(bench.glob("tier*")):
            if not tier.is_dir():
                continue
            label = tier.name
            if label == "tier5_http":
                scen = tier / "scenarios"
                if scen.is_dir():
                    for child in sorted(scen.iterdir()):
                        if child.is_dir():
                            rel = f"{prefix}/tier5_http/scenarios/{child.name}"
                            index.setdefault(child.name, rel)
                continue
            for child in sorted(tier.iterdir()):
                if child.is_dir():
                    rel = f"{prefix}/{label}/{child.name}"
                    index.setdefault(child.name, rel)

        for sub in ("ml", "viewport"):
            pkg = bench / sub
            if not pkg.is_dir():
                continue
            for child in sorted(pkg.iterdir()):
                if child.is_dir():
                    rel = f"{prefix}/{sub}/{child.name}"
                    index.setdefault(child.name, rel)
    return index


def registry_dir_stems(sync_mod) -> dict[str, str]:
    """catalog id -> registry harness dir name (reverse of CATALOG_ID_ALIASES)."""
    out: dict[str, str] = {}
    for registry_name, catalog_id in sync_mod.CATALOG_ID_ALIASES.items():
        out.setdefault(catalog_id, registry_name)
    return out


def path_exists(rel: str, *, bench_root: Path, lic_root: Path | None) -> bool:
    """True when rel exists under benchmarks repo or legacy lic root."""
    if rel.startswith("benchmarks/"):
        return (bench_root / rel).is_dir() or (bench_root / rel).is_file()
    if lic_root is not None:
        return (lic_root / rel).is_dir() or (lic_root / rel).is_file()
    return False


def lookup_path(
    bench_id: str,
    base_id: str | None,
    *,
    bench_root: Path,
    lic_root: Path | None,
    harness_index: dict[str, str],
    sync_mod,
) -> str | None:
    """Return relative catalog path when harness dir exists, else None."""
    candidates: list[str] = []
    lookup = base_id or bench_id
    candidates.append(lookup)
    candidates.append(bench_id)
    reg = registry_dir_stems(sync_mod)
    if lookup in reg:
        candidates.append(reg[lookup])
    if bench_id in reg:
        candidates.append(reg[bench_id])
    for stem in sync_mod.stem_candidates(lookup):
        candidates.append(stem)
    for stem in sync_mod.stem_candidates(bench_id):
        candidates.append(stem)

    seen: set[str] = set()
    for name in candidates:
        if not name or name in seen:
            continue
        seen.add(name)
        rel = harness_index.get(name)
        if rel and path_exists(rel, bench_root=bench_root, lic_root=lic_root):
            return rel
        if lic_root is not None:
            resolved = sync_mod.resolve_path(name, lic_root)
            if resolved != "unknown" and path_exists(
                resolved, bench_root=bench_root, lic_root=lic_root
            ):
                return resolved
    return None


def path_is_managed(path: str) -> bool:
    if not path or path == "unknown":
        return True
    return not any(path.startswith(p) for p in SKIP_PATH_PREFIXES)


def sync_catalog_paths(
    benchmarks: list[dict],
    *,
    bench_root: Path,
    lic_root: Path | None,
    harness_index: dict[str, str],
    sync_mod,
) -> list[tuple[str, str, str]]:
    fixes: list[tuple[str, str, str]] = []
    for b in benchmarks:
        if b.get("catalog_lifecycle") == "planned" or b.get("variant") == "vertical_stub":
            continue
        cur = str(b.get("path") or "unknown")
        if not path_is_managed(cur):
            continue
        new = lookup_path(
            b["id"],
            b.get("base_id"),
            bench_root=bench_root,
            lic_root=lic_root,
            harness_index=harness_index,
            sync_mod=sync_mod,
        )
        if not new or cur == new:
            continue
        if cur != "unknown" and path_exists(cur, bench_root=bench_root, lic_root=lic_root):
            continue
        fixes.append((b["id"], cur, new))
        b["path"] = new
        if new.startswith("benchmarks/workloads/"):
            b["repo"] = "benchmarks"
    return fixes


def rebuild_summary(lic_root: Path, lis_root: Path) -> int:
    csv_path = ROOT / CSV_REL
    if not csv_path.is_file():
        csv_path = lic_root / Path("benchmarks/results/latest.csv")
    if not csv_path.is_file():
        print(f"skip summary rebuild: missing {csv_path}", file=sys.stderr)
        return 0
    if not INGEST.is_file():
        raise SystemExit(f"missing ingest script: {INGEST}")
    cmd = [
        sys.executable,
        str(INGEST),
        str(lic_root),
        str(lis_root),
    ]
    print("run:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lic-root",
        type=Path,
        default=Path(__import__("os").environ.get("LIC_ROOT", str(DEFAULT_LIC))),
    )
    parser.add_argument(
        "--lis-root",
        type=Path,
        default=Path(__import__("os").environ.get("LIS_ROOT", str(DEFAULT_LIS))),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--rebuild-summary",
        action="store_true",
        help="run build_summary.py when latest.csv exists (default with --write)",
    )
    parser.add_argument(
        "--include-legacy-lic",
        action="store_true",
        help="also scan LIC_ROOT/benchmarks (deprecated; workloads ADR is canonical)",
    )
    args = parser.parse_args()
    lic_root = args.lic_root.resolve()
    lis_root = args.lis_root.resolve()
    lic_usable = lic_root.is_dir()
    workloads = ROOT / "benchmarks" / "workloads"
    if not workloads.is_dir() and not lic_usable:
        raise SystemExit(
            f"no workloads under {workloads} and LIC_ROOT not found: {lic_root}"
        )
    if args.include_legacy_lic and not lic_usable:
        raise SystemExit(f"--include-legacy-lic but LIC_ROOT not found: {lic_root}")
    lic_for_scan = lic_root if (args.include_legacy_lic and lic_usable) else None
    if args.include_legacy_lic and lic_usable:
        print(
            "warn: --include-legacy-lic scans deprecated lic/benchmarks; "
            "prefer benchmarks/workloads only",
            file=sys.stderr,
        )

    import tomllib

    sync_mod = load_sync_registry_module()
    text = CATALOG.read_text()
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    harness_index = scan_harness_index(
        lic_for_scan, bench_root=ROOT, include_legacy_lic=args.include_legacy_lic
    )
    sources = "benchmarks/workloads"
    if args.include_legacy_lic and lic_usable:
        sources += " + legacy lic"
    print(f"harness dirs indexed: {len(harness_index)} ({sources})")

    fixes = sync_catalog_paths(
        benchmarks,
        bench_root=ROOT,
        lic_root=lic_for_scan if lic_usable else None,
        harness_index=harness_index,
        sync_mod=sync_mod,
    )
    print(f"paths to update: {len(fixes)}")
    for bench_id, old, new in fixes[:20]:
        print(f"  {bench_id}: {old} -> {new}")
    if len(fixes) > 20:
        print(f"  ... and {len(fixes) - 20} more")

    if args.dry_run and not args.write:
        return 0
    if not args.write:
        print("pass --write to update catalog.toml", file=sys.stderr)
        return 1

    header = load_header(text)
    CATALOG.write_text(header + "\n\n".join(format_benchmark(b) for b in benchmarks) + "\n")
    print(f"wrote {CATALOG}")

    do_summary = args.rebuild_summary or args.write
    if do_summary:
        if lic_usable:
            rc = rebuild_summary(lic_root, lis_root)
            if rc != 0:
                return rc
        else:
            print("skip summary rebuild: LIC_ROOT not available", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
