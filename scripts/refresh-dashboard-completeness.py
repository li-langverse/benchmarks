#!/usr/bin/env python3
"""Refresh committed summary.json with multi-OS skip charts and catalog size labels.

Use when a full lic CSV re-ingest is unavailable locally (Windows sprint host).
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"

sys.path.insert(0, str(ROOT / "scripts/ingest"))
import build_summary as bs  # noqa: E402


def chart_base_id(ch: dict) -> str:
    bid = str(ch.get("base_id") or ch.get("id") or "")
    return bid.split("@", 1)[0]


def refresh(summary: dict, catalog: dict[str, dict], catalog_defaults: dict) -> dict:
    rows = summary.get("rows") or []
    row_by_bench = {r["benchmark"]: r for r in rows}

    new_categories: dict[str, dict] = {}
    charts_by_pillar: dict[str, list[dict]] = defaultdict(list)

    for cat_name, cat_data in (summary.get("categories") or {}).items():
        charts_out: list[dict] = []
        by_base: dict[str, list[dict]] = defaultdict(list)
        for ch in cat_data.get("charts") or []:
            by_base[chart_base_id(ch)].append(ch)

        for base, group in sorted(by_base.items()):
            cfg = catalog.get(base)
            if not cfg:
                stub_cfg = {
                    "id": base,
                    "category": cat_name,
                    "tier": 99,
                    "platforms": list(bs.REQUIRED_PLATFORMS),
                }
                platforms = list(bs.REQUIRED_PLATFORMS)
                multi = True
                for plat in platforms:
                    ch = bs.build_skip_os_chart(
                        base,
                        stub_cfg,
                        plat=plat,
                        validity_status="skip",
                        validity_source="catalog:non_catalog_chart",
                        chart_id=bs.chart_id_for_os(base, plat, multi=multi),
                    )
                    charts_out.append(ch)
                    charts_by_pillar[ch.get("pillar", cat_name)].append(ch)
                continue
            platforms = bs.platforms_for_cfg(cfg, catalog_defaults)
            multi = len(platforms) > 1
            existing: dict[str, dict] = {}
            for ch in group:
                plat = bs.display_os(ch.get("os"))
                if not plat or plat == "unknown":
                    cid = str(ch.get("id") or "")
                    plat = cid.split("@", 1)[1] if "@" in cid else "linux"
                existing[plat] = ch
            validity_status, validity_source = bs.pending_validity(cfg)
            if base in row_by_bench:
                row = row_by_bench[base]
                row_vs = row.get("validity_status")
                if row_vs in ("pass", "fail", "skip", "advisory"):
                    validity_status = row_vs
                    validity_source = row.get("validity_source") or validity_source
                elif row.get("pending") or row.get("li_value") is None:
                    validity_status, validity_source = bs.pending_validity(cfg)

            for plat in platforms:
                if plat in existing:
                    ch = dict(existing[plat])
                    sizes = bs.effective_size_meta(cfg)
                    ch.update({k: v for k, v in sizes.items() if v is not None})
                    ch["os"] = plat
                    if ch.get("validity_status") not in ("pass", "fail", "skip", "advisory"):
                        ch["validity_status"] = validity_status
                        ch["validity_source"] = validity_source
                    if ch.get("status") not in ("green", "yellow", "red", "skip"):
                        ch["status"] = "skip" if ch.get("pending") else ch.get("status", "unknown")
                    if ch.get("pending") and ch.get("status") == "unknown":
                        ch["status"] = "skip"
                    charts_out.append(ch)
                    charts_by_pillar[ch.get("pillar", "numerics")].append(ch)
                    continue
                if any(existing.values()):
                    ref_chart = next(iter(existing.values()))
                    vs = ref_chart.get("validity_status") or validity_status
                    vsrc = ref_chart.get("validity_source") or validity_source
                    if vs in (None, "", "unknown") and ref_chart.get("series"):
                        vs, vsrc = validity_status, validity_source
                    skip = bs.build_skip_os_chart(
                        base,
                        cfg,
                        plat=plat,
                        validity_status="skip",
                        validity_source=f"platform:{plat}:not_measured",
                        chart_id=bs.chart_id_for_os(base, plat, multi=multi),
                        catalog_defaults=catalog_defaults,
                    )
                    charts_out.append(skip)
                    charts_by_pillar[skip["pillar"]].append(skip)
                else:
                    for ch in group:
                        patched = dict(ch)
                        sizes = bs.effective_size_meta(cfg)
                        patched.update({k: v for k, v in sizes.items() if v is not None})
                        patched["os"] = bs.display_os(patched.get("os"))
                        if patched.get("pending"):
                            patched["validity_status"] = validity_status
                            patched["validity_source"] = validity_source
                            patched["status"] = "skip"
                        charts_out.append(patched)
                        charts_by_pillar[patched.get("pillar", "numerics")].append(patched)

        new_categories[cat_name] = {
            **cat_data,
            "charts": sorted(charts_out, key=lambda c: c["id"]),
        }

    for r in rows:
        cfg = catalog.get(r["benchmark"])
        if not cfg:
            continue
        sizes = bs.effective_size_meta(cfg)
        r.update({k: v for k, v in sizes.items() if v is not None})
        if cfg and r.get("validity_status") not in ("pass", "fail", "skip", "advisory"):
            if r.get("pending") or r.get("li_value") is None:
                vs, vsrc = bs.pending_validity(cfg)
                r["validity_status"] = vs
                r["validity_source"] = vsrc
                r["status"] = "skip"
        if r.get("status") in (None, "", "unknown") and r.get("validity_status") == "skip":
            r["status"] = "skip"

    summary["categories"] = new_categories
    summary["pillars"] = bs.build_pillars(dict(charts_by_pillar))
    summary["generated_at"] = datetime.now(timezone.utc).isoformat()
    os_values = sorted(
        {
            bs.display_os(ch.get("os"))
            for cat in new_categories.values()
            for ch in cat.get("charts", [])
            if ch.get("os")
        }
    )
    reporting = summary.setdefault("reporting", {})
    reporting["os_values"] = os_values
    size_labels = sorted(
        {str(ch["size_label"]) for cat in new_categories.values() for ch in cat.get("charts", []) if ch.get("size_label")}
    )
    reporting["size_labels"] = size_labels
    return summary


def main() -> int:
    if not SUMMARY.is_file():
        print(f"missing {SUMMARY}", file=sys.stderr)
        return 1
    catalog = bs.load_catalog()
    catalog_defaults = bs.load_catalog_defaults()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    refreshed = refresh(summary, catalog, catalog_defaults)
    SUMMARY.write_text(json.dumps(refreshed, indent=2) + "\n", encoding="utf-8")
    charts = sum(len(c.get("charts", [])) for c in refreshed.get("categories", {}).values())
    print(f"refresh-dashboard-completeness: wrote {SUMMARY} ({charts} charts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
