"""Shared catalog gap classification for PH-5b honesty (competitive vertical stubs)."""
from __future__ import annotations

from pathlib import Path

COMPETITIVE_STUB_FAMILIES = frozenset({"bio", "drug", "am", "robo"})

ASPIRATIONAL_ID_PREFIXES = (
    "cfd_",
    "fea_",
    "qm_",
    "md_",
    "pde_",
    "combustion_",
    "cloth_",
    "double_",
    "heat_",
    "wave_",
    "nbody_",
    "orbit_",
    "schrodinger_",
    "ragdoll_",
    "fdtd_",
    "advection_",
    "auto_",
)


def path_stem(path: str) -> str:
    return Path(path.replace("\\", "/")).name if path else ""


def is_bogus_competitive_remap(bench_id: str, path: str) -> bool:
    """True when a competitive-vertical id points at another harness directory."""
    if not path or path in ("unknown",):
        return False
    family = bench_id.split("_", 1)[0]
    if family not in COMPETITIVE_STUB_FAMILIES:
        return False
    return path_stem(path) != bench_id


def is_aspirational_deferral(bench_id: str, path: str, *, tier: int | None = None) -> bool:
    """Tier-2 / physics-cluster rows deferred until lic harness lands."""
    if tier is not None and tier >= 2:
        return True
    if "tier2_physics" in (path or ""):
        return True
    return any(bench_id.startswith(prefix) for prefix in ASPIRATIONAL_ID_PREFIXES)


def classify_catalog_row(
    row: dict,
    *,
    lic_root: Path | None,
    bench_root: Path | None = None,
) -> str:
    """Return triage action: ok | already_planned | unknown_path | other_repo | bogus_remap | defer_planned | lic_impl | missing_both."""
    lifecycle = str(row.get("catalog_lifecycle") or "").lower()
    if lifecycle == "planned":
        return "already_planned"

    rel = str(row.get("path", "")).strip()
    if not rel or rel == "unknown":
        return "unknown_path"

    repo = str(row.get("repo", "lic"))
    if repo != "lic":
        return "other_repo"

    lic_path = (lic_root / rel) if lic_root and lic_root.is_dir() else None
    if lic_path and (lic_path.is_dir() or lic_path.is_file()):
        return "ok"

    bench_id = row["id"]
    if is_bogus_competitive_remap(bench_id, rel):
        return "bogus_remap"

    tier = row.get("tier")
    tier_n = int(tier) if tier is not None else None
    if is_aspirational_deferral(bench_id, rel, tier=tier_n):
        return "defer_planned"

    if bench_root and (bench_root / rel).is_dir():
        return "lic_impl"

    return "missing_both"


def remediation_for(action: str) -> str | None:
    """Catalog edit to apply for triage actions (None = no catalog change)."""
    if action == "bogus_remap":
        return "planned_unknown"
    if action == "defer_planned":
        return "planned_keep_path"
    return None
