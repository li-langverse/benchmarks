#!/usr/bin/env python3
"""Explore Li ecosystem gaps: std/libs, ingest tooling, catalog vs HPC SOTA, external signals.

Writes data/latest/ecosystem-explorer.json with structured findings and suggested
web/Reddit search queries for Cursor agents (no network calls by default).

Usage:
  python3 scripts/ecosystem-explorer.py
  LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py --write-digest docs/ecosystem/explorer-digests/latest.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/ecosystem-explorer.json"

# Modules referenced by benchmarks ingest/dashboard (may not exist on lic@main yet).
# Import surface uses short names (`import io`); on disk lic still maps these to std/* paths.
EXPECTED_STD_MODULES = [
    {
        "module": "io",
        "ph_id": "PH-IO-4",
        "why": "CSV/file ingest without Python",
        "refs": ["scripts/ingest/csv_ingest_smoke.li"],
    },
    {
        "module": "csv",
        "ph_id": "PH-IO-4",
        "why": "Benchmark CSV parsing in Li",
        "refs": ["scripts/ingest/csv_ingest_smoke.li"],
    },
    {
        "module": "summary",
        "ph_id": "PH-IO-7",
        "why": "Build data/latest/summary.json in Li",
        "refs": ["scripts/ingest/build_summary.li"],
    },
    {
        "module": "plot",
        "ph_id": "PH-IO-5",
        "why": "Static dashboard without Node/Vite",
        "refs": ["scripts/dashboard/render_dashboard.li"],
    },
]

# HPC / numerics ecosystems to compare (static rubric — agent enriches via web search).
HPC_LIBRARIES = [
    {
        "id": "eigen",
        "name": "Eigen",
        "domain": "dense/sparse LA",
        "capabilities": ["GEMM", "decompositions", "expression templates"],
        "li_status": "partial",
        "li_analog": "li-std-math, lic tier-1 matmul benches",
        "gap_hint": "Pure-Li SIMD matmul vs Eigen/MKL; sparse support",
    },
    {
        "id": "kokkos",
        "name": "Kokkos",
        "domain": "performance portability",
        "capabilities": ["parallel_for", "views", "GPU backends"],
        "li_status": "missing",
        "li_analog": "std/execution decorators (minimal)",
        "gap_hint": "Execution model + memory spaces for tier-2 physics",
    },
    {
        "id": "petsc",
        "name": "PETSc",
        "domain": "PDE / scalable solvers",
        "capabilities": ["KSP", "SNES", "DM", "time integrators"],
        "li_status": "missing",
        "li_analog": "physics packages (stubs); shared C cores in benches",
        "gap_hint": "Implicit solvers, AMG, distributed meshes",
    },
    {
        "id": "fftw",
        "name": "FFTW",
        "domain": "FFT",
        "capabilities": ["1D/2D/3D FFT", "plans"],
        "li_status": "missing",
        "li_analog": "none in catalog",
        "gap_hint": "Add micro FFT bench + std/signal or vendor hook",
    },
    {
        "id": "openmp",
        "name": "OpenMP",
        "domain": "shared-memory parallelism",
        "capabilities": ["parallel loops", "tasks", "offload"],
        "li_status": "partial",
        "li_analog": "LLVM codegen; no first-class Li pragma surface",
        "gap_hint": "Document parallel loop lowering vs OpenMP runtime",
    },
    {
        "id": "hpx",
        "name": "HPX",
        "domain": "async tasking",
        "capabilities": ["futures", "distributed"],
        "li_status": "missing",
        "li_analog": "none",
        "gap_hint": "Async/game physics scheduling",
    },
    {
        "id": "raja",
        "name": "RAJA",
        "domain": "loop abstractions",
        "capabilities": ["policy-based loops", "GPU"],
        "li_status": "missing",
        "li_analog": "bench harness only",
        "gap_hint": "Portable kernel policies in Li",
    },
    {
        "id": "sundials",
        "name": "SUNDIALS",
        "domain": "ODE/DAE",
        "capabilities": ["BDF", "Adams", "sensitivity"],
        "li_status": "partial",
        "li_analog": "tier-2 integrators (Euler, symplectic stubs)",
        "gap_hint": "Stiff ODE suites for physics tiers",
    },
    {
        "id": "hypre",
        "name": "hypre",
        "domain": "preconditioners / AMG",
        "capabilities": ["BoomerAMG", "parallel CSR"],
        "li_status": "missing",
        "li_analog": "none",
        "gap_hint": "Large-scale PDE path",
    },
    {
        "id": "stdpar",
        "name": "C++ std::execution",
        "domain": "parallel algorithms",
        "capabilities": ["par_unseq", "sender/receiver"],
        "li_status": "partial",
        "li_analog": "std/execution/decorators.li",
        "gap_hint": "Map decorators to real codegen policies",
    },
]

LANGUAGE_IMPROVEMENT_HEURISTICS = [
    {
        "id": "stdlib-surface",
        "signal": "std/* module count << ingest/dashboard imports",
        "action": "Prioritize PH-IO modules (import io, csv, summary, plot) in lic",
    },
    {
        "id": "pure-li-benches",
        "signal": "horner_pure_li or tier-1 still red/yellow",
        "action": "Compiler/codegen (PH-7e), not catalog threshold tweaks",
    },
    {
        "id": "python-fallback",
        "signal": "ingest-lic.sh still falls back to build_summary.py",
        "action": "Ship std/summary; keep Python as parity gate only",
    },
    {
        "id": "shared-c-kernels",
        "signal": "physics tier-2 variant shared_c_kernel",
        "action": "Plan pure-Li physics kernels per GAME_DEV.md",
    },
    {
        "id": "agent-kit-drift",
        "signal": "expected-agent-kit-version mismatch across repos",
        "action": "Bump roadmap agent-kit; sync-agent-kit.sh",
    },
]

REDDIT_SUBREDDITS = [
    "ProgrammingLanguages",
    "Compilers",
    "HPC",
    "cpp",
    "rust",
    "scientificcomputing",
]

ORG_MIRROR_REPOS = [
    "li-net",
    "li-httpd",
    "li-std-core",
    "li-std-math",
    "li-demo",
]


def gh_json(args: list[str]) -> list[dict] | dict | None:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def lic_root() -> Path:
    env = Path(os.environ.get("LIC_ROOT", ROOT / "lic"))
    if env.is_dir():
        return env
    return ROOT / "lic"


def scan_std_modules(lic: Path) -> list[str]:
    std = lic / "std"
    if not std.is_dir():
        return []
    mods: list[str] = []
    for path in std.rglob("*.li"):
        rel = path.relative_to(std).with_suffix("")
        parts = list(rel.parts)
        if parts:
            mods.append("std." + ".".join(parts))
    return sorted(set(mods))


def scan_lic_packages(lic: Path) -> list[str]:
    pkg = lic / "packages"
    if not pkg.is_dir():
        return []
    names = []
    for child in sorted(pkg.iterdir()):
        if child.is_dir() and (child / "li.toml").is_file():
            names.append(child.name)
    return names


def scan_std_imports_in_repo(root: Path) -> dict[str, list[str]]:
    """Collect `import <name>` lines from repo .li files (short names + legacy std.*)."""
    imports: dict[str, set[str]] = {}
    pat = re.compile(r"^\s*import\s+([A-Za-z_][A-Za-z0-9_.]*)\s*$", re.MULTILINE)
    for path in root.rglob("*.li"):
        if "lic/" in str(path) and root == ROOT:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in pat.finditer(text):
            mod = m.group(1)
            imports.setdefault(mod, set()).add(str(path.relative_to(root)))
    return {k: sorted(v) for k, v in sorted(imports.items())}


def std_module_present(modules_on_disk: list[str], want: str) -> bool:
    """Resolve import surface name (e.g. io, csv) against lic std/*.li scan (std.dotted)."""
    candidates: list[str] = []
    if want.startswith("std."):
        candidates.append(want)
    else:
        candidates.append("std." + want)
        candidates.append(want)
    for c in candidates:
        needle = c.replace(".", "/")
        for m in modules_on_disk:
            if m == c or m.replace(".", "/") == needle:
                return True
        if any(m.startswith(c + ".") for m in modules_on_disk):
            return True
    return False


def missing_std_report(modules_on_disk: list[str]) -> list[dict]:
    out = []
    for spec in EXPECTED_STD_MODULES:
        present = std_module_present(modules_on_disk, spec["module"])
        if not present:
            out.append({**spec, "status": "missing"})
        else:
            out.append({**spec, "status": "present"})
    return out


def parse_catalog() -> dict:
    path = ROOT / "catalog.toml"
    if not path.is_file() or tomllib is None:
        return {"error": "catalog.toml missing or tomllib unavailable"}
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    benches = data.get("benchmark", [])
    by_cat: dict[str, int] = {}
    by_tier: dict[int, int] = {}
    variants: dict[str, int] = {}
    for b in benches:
        cat = b.get("category", "unknown")
        by_cat[cat] = by_cat.get(cat, 0) + 1
        tier = int(b.get("tier", 0))
        by_tier[tier] = by_tier.get(tier, 0) + 1
        v = b.get("variant", "default")
        variants[v] = variants.get(v, 0) + 1
    suggested_gaps = []
    if by_cat.get("physics", 0) < 8:
        suggested_gaps.append("Expand physics tier-2 coverage (fluids, AMR, FFT) vs HPC suites")
    if "fft" not in " ".join(b.get("id", "") for b in benches):
        suggested_gaps.append("No FFT micro-bench — compare FFTW/FFmpeg signal path")
    if variants.get("pure_li", 0) < 3:
        suggested_gaps.append("Increase pure_li variant rows for PH-7e codegen proof")
    return {
        "total": len(benches),
        "by_category": by_cat,
        "by_tier": {str(k): v for k, v in by_tier.items()},
        "variants": variants,
        "suggested_catalog_gaps": suggested_gaps,
    }


def search_open_gap_issues() -> list[dict]:
    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        return []
    items = gh_json(
        [
            "search",
            "issues",
            "--owner",
            "li-langverse",
            "ecosystem-gap",
            "state:open",
            "--json",
            "repository,number,title,url",
            "--limit",
            "20",
        ]
    )
    if not items:
        return []
    out = []
    for it in items:
        repo = it.get("repository", {})
        name = repo.get("nameWithOwner", repo.get("name", "?"))
        out.append(
            {
                "repo": name,
                "number": it.get("number"),
                "title": it.get("title"),
                "url": it.get("url"),
            }
        )
    return out


def web_search_queries(focus: str | None) -> list[dict]:
    base = focus or "systems programming language HPC SIMD ownership"
    queries = [
        {
            "channel": "reddit",
            "query": f"site:reddit.com ({' OR '.join('r/' + s for s in REDDIT_SUBREDDITS[:4])}) {base}",
            "why": "Community pain points, language comparisons, library wishes",
        },
        {
            "channel": "reddit",
            "query": "site:reddit.com r/HPC Kokkos vs OpenMP performance portability 2024..2026",
            "why": "HPC portability expectations for Li execution model",
        },
        {
            "channel": "web",
            "query": "PETSc Kokkos integration best practices PDE solver stack",
            "why": "Stack gaps for physics/PDE packages",
        },
        {
            "channel": "web",
            "query": "Eigen BLAS GEMM optimization techniques constexpr compile time",
            "why": "Numerics / matmul roadmap vs li-std-math",
        },
        {
            "channel": "web",
            "query": "new programming languages memory safety performance C++ alternative 2025",
            "why": "Language design trends (ownership, verifiers, JIT/AOT)",
        },
        {
            "channel": "web",
            "query": "FFTW vs vendor FFT library benchmark roofline",
            "why": "Missing FFT catalog row",
        },
        {
            "channel": "github",
            "query": "org:llvm llvm-project parallel loop IR OpenMP",
            "why": "Codegen parity for std/execution",
        },
    ]
    return queries


def agent_kit_versions() -> dict:
    versions = []
    roots = [
        ROOT,
        ROOT / "roadmap",
        ROOT / "lic",
        ROOT / "lip",
        ROOT / "lit",
        ROOT.parent / "li",
    ]
    seen: set[Path] = set()
    for repo_dir in roots:
        if not repo_dir.is_dir():
            continue
        resolved = repo_dir.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        p = repo_dir / "scripts/expected-agent-kit-version"
        if p.is_file():
            versions.append(
                {
                    "path": str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),
                    "version": p.read_text(encoding="utf-8").strip(),
                }
            )
    uniq = {v["version"] for v in versions}
    drift = len(uniq) > 1
    return {"entries": versions, "drift": drift, "canonical_hint": "run ensure-org-agent-kit.py"}


def build_digest_md(report: dict) -> str:
    lines = [
        f"# Ecosystem explorer digest\n",
        f"Generated: {report['generated_at']}\n",
        "## Missing PH-IO modules (`import io`, `csv`, `summary`, `plot`)\n",
    ]
    for m in report.get("missing_std_modules", []):
        if m.get("status") == "missing":
            lines.append(f"- **{m['module']}** ({m['ph_id']}): {m['why']}\n")
    lines.append("\n## HPC comparison highlights\n")
    for lib in report.get("hpc_libraries", [])[:6]:
        if lib.get("li_status") in ("missing", "partial"):
            lines.append(
                f"- **{lib['name']}** ({lib['li_status']}): {lib.get('gap_hint', '')}\n"
            )
    lines.append("\n## Suggested web / Reddit searches\n")
    for q in report.get("web_search_queries", [])[:5]:
        lines.append(f"- [{q['channel']}] {q['query']}\n")
    lines.append("\n## Recommended actions\n")
    for a in report.get("recommended_actions", []):
        lines.append(f"- **{a['priority']}** {a['action']}\n")
    return "".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Li ecosystem explorer")
    parser.add_argument("--write-digest", type=Path, default=None, help="also write markdown digest")
    parser.add_argument("--focus", default=None, help="narrow web search queries")
    args = parser.parse_args()

    lic = lic_root()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    std_mods = scan_std_modules(lic) if lic.is_dir() else []
    packages = scan_lic_packages(lic) if lic.is_dir() else []
    imports = scan_std_imports_in_repo(ROOT)
    missing_std = missing_std_report(std_mods)
    catalog = parse_catalog()

    physics_pkgs = [p for p in packages if "physics" in p]
    core_mirrors = set(ORG_MIRROR_REPOS)
    unmirrored_physics = [p for p in physics_pkgs if p not in core_mirrors]

    gap_issues = search_open_gap_issues()
    kit = agent_kit_versions()

    recommended = []
    miss = [m for m in missing_std if m["status"] == "missing"]
    if miss:
        recommended.append(
            {
                "priority": "P1",
                "action": "Implement missing std modules in lic (PH-IO track)",
                "modules": [m["module"] for m in miss],
            }
        )
    if catalog.get("suggested_catalog_gaps"):
        recommended.append(
            {
                "priority": "P2",
                "action": "Extend benchmarks catalog from HPC rubric",
                "gaps": catalog["suggested_catalog_gaps"],
            }
        )
    if kit.get("drift"):
        recommended.append(
            {
                "priority": "P2",
                "action": "Sync agent-kit versions across repos",
                "versions": kit.get("entries"),
            }
        )
    recommended.append(
        {
            "priority": "P2",
            "action": "Run web/Reddit searches (see web_search_queries); file issues with label explorer-finding",
            "note": "Use Cursor web search or manual review — script does not scrape Reddit",
        }
    )

    report = {
        "generated_at": now,
        "lic_root": str(lic),
        "lic_present": lic.is_dir(),
        "std_modules_on_disk": std_mods,
        "missing_std_modules": missing_std,
        "std_imports_in_benchmarks": imports,
        "lic_packages": packages,
        "physics_packages": physics_pkgs,
        "org_mirror_repos": ORG_MIRROR_REPOS,
        "packages_without_org_mirror": unmirrored_physics[:15],
        "catalog": catalog,
        "hpc_libraries": HPC_LIBRARIES,
        "language_improvement_heuristics": LANGUAGE_IMPROVEMENT_HEURISTICS,
        "open_ecosystem_gap_issues": gap_issues,
        "agent_kit": kit,
        "web_search_queries": web_search_queries(args.focus),
        "reddit_subreddits": REDDIT_SUBREDDITS,
        "recommended_actions": recommended,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")

    if args.write_digest:
        args.write_digest.parent.mkdir(parents=True, exist_ok=True)
        args.write_digest.write_text(build_digest_md(report), encoding="utf-8")
        print(f"wrote {args.write_digest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
