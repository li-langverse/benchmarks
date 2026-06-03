#!/usr/bin/env python3
"""Refresh committed summary.json with multi-OS skip charts and catalog size labels.

Use when a full lic CSV re-ingest is unavailable locally (Windows sprint host).
"""
from __future__ import annotations

import json
import os
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


def chart_os(ch: dict) -> str:
    plat = bs.normalize_os(ch.get("os"))
    if plat != "unknown":
        return plat
    cid = str(ch.get("id") or "")
    if "@" in cid:
        return cid.split("@", 1)[1]
    return "linux"


def chart_row_from_chart(
    base: str,
    cfg: dict,
    ch: dict,
    row_by_bench: dict[str, dict],
) -> dict:
    """Build a summary row mirroring a platform chart for tier 0/1."""
    meta = bs.row_meta(cfg)
    sizes = bs.effective_size_meta(cfg, has_csv=bool(ch.get("series")))
    ref = cfg.get("compare_oracle") or (
        "postgres" if cfg.get("category") == "database" else "cpp"
    )
    existing = row_by_bench.get(base) or {}
    st = ch.get("status") or existing.get("status") or "unknown"
    if ch.get("validity_status") == "skip" or not ch.get("series"):
        st = "skip"
    series = ch.get("series") or []
    li_pt = next((s for s in series if s.get("lang") == "li"), None)
    ref_lang = ch.get("reference_lang", ref)
    ref_pt = next((s for s in series if s.get("lang") == ref_lang), None)
    sota_ref_lang = ch.get("sota_ref_lang") or ch.get("sota_lang")
    sota_ref_pt = (
        next((s for s in series if s.get("lang") == sota_ref_lang), None)
        if sota_ref_lang
        else None
    )
    metric_name = ch.get("metric") or existing.get("metric") or cfg.get("metric", "wall_time")
    li_val = li_pt.get("value") if li_pt else None
    table_sota_lang, table_sota_val = bs.table_sota_display(
        li_val,
        sota_ref_lang,
        sota_ref_pt.get("value") if sota_ref_pt else None,
        lower_is_better=bs.metric_lower_is_better(metric_name),
    )
    return {
        "benchmark": base,
        "repo": cfg.get("repo", "lic"),
        "tier": cfg.get("tier", 0),
        "category": cfg.get("category", existing.get("category", "micro")),
        "metric": metric_name,
        "li_value": li_val,
        "li_stddev": li_pt.get("stddev") if li_pt else None,
        "li_sample_runs": li_pt.get("sample_runs") if li_pt else None,
        "cpp_value": ref_pt.get("value") if ref_pt and ref_lang == "cpp" else None,
        "cpp_stddev": ref_pt.get("stddev") if ref_pt and ref_lang == "cpp" else None,
        "cpp_sample_runs": ref_pt.get("sample_runs") if ref_pt and ref_lang == "cpp" else None,
        "ratio_vs_cpp": ch.get("ratio_vs_reference"),
        "sota_ref_lang": sota_ref_lang,
        "sota_lang": table_sota_lang,
        "sota_value": table_sota_val,
        "ratio_vs_sota": ch.get("ratio_vs_sota"),
        "unit": ch.get("unit") or existing.get("unit"),
        "variant": cfg.get("variant"),
        "status": st,
        "validity_status": ch.get("validity_status")
        or existing.get("validity_status")
        or "skip",
        "validity_source": ch.get("validity_source")
        or existing.get("validity_source")
        or "platform_not_measured",
        "os": chart_os(ch),
        "ph_ids": cfg.get("ph_ids", []),
        "path": cfg.get("path", ""),
        "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
        "compare_oracle": ref,
        "ci_url": existing.get("ci_url", ""),
        "langs": series,
        **meta,
        "problem_size": ch.get("problem_size", cfg.get("problem_size")),
        "size_label": ch.get("size_label", cfg.get("size_label")),
        "base_id": ch.get("base_id", bs.chart_base_id(base, cfg)),
    }


def is_tier5_http(cfg: dict | None) -> bool:
    if not cfg:
        return False
    tier = cfg.get("tier")
    return tier in (5, "5") and str(cfg.get("category") or "").lower() == "http"


def is_stdlib_stub(cfg: dict | None) -> bool:
    if not cfg:
        return False
    return str(cfg.get("workload_class") or "").lower() == "stub" and cfg.get("tier") in (
        1,
        "1",
    )


def apply_linux_li_pending_row(row: dict) -> None:
    row["validity_status"] = "advisory"
    row["validity_source"] = row.get("validity_source") or "oracle:li:not_measured"
    row["status"] = "advisory"
    row["pending"] = True


def apply_linux_li_pending_chart(ch: dict) -> None:
    ch["validity_status"] = "advisory"
    ch["validity_source"] = ch.get("validity_source") or "oracle:li:not_measured"
    ch["status"] = "advisory"
    ch["pending"] = True


def fix_linux_unknown_http_and_stdlib(
    summary: dict,
    catalog: dict[str, dict],
) -> int:
    """Clear P0 unknown rows/charts for tier-5 HTTP + tier-1 stdlib stubs without li data."""
    changed = 0
    for row in summary.get("rows") or []:
        if bs.normalize_os(row.get("os")) != "linux":
            continue
        cfg = catalog.get(row.get("benchmark", ""))
        if not (is_tier5_http(cfg) or is_stdlib_stub(cfg)):
            continue
        if row.get("status") not in (None, "", "unknown") and row.get("validity_status") not in (
            None,
            "",
            "unknown",
        ):
            continue
        if row.get("li_value") is not None:
            continue
        apply_linux_li_pending_row(row)
        changed += 1

    for cat in (summary.get("categories") or {}).values():
        for ch in cat.get("charts") or []:
            if chart_os(ch) != "linux":
                continue
            base = chart_base_id(ch)
            cfg = catalog.get(base)
            if not (is_tier5_http(cfg) or is_stdlib_stub(cfg)):
                continue
            if ch.get("status") not in (None, "", "unknown") and ch.get(
                "validity_status"
            ) not in (None, "", "unknown"):
                continue
            if any(s.get("lang") == "li" for s in ch.get("series") or []):
                continue
            apply_linux_li_pending_chart(ch)
            changed += 1

    return changed


def expand_tier01_rows(
    summary: dict,
    catalog: dict[str, dict],
    catalog_defaults: dict,
) -> None:
    """Ensure tier 0/1 benchmarks have one summary row per catalog platform."""
    charts_by_base: dict[str, list[dict]] = defaultdict(list)
    for cat in (summary.get("categories") or {}).values():
        for ch in cat.get("charts") or []:
            charts_by_base[chart_base_id(ch)].append(ch)

    by_bench: dict[str, list[dict]] = defaultdict(list)
    for row in summary.get("rows") or []:
        by_bench[row["benchmark"]].append(row)

    expanded: list[dict] = []
    for base in sorted(by_bench.keys()):
        group = by_bench[base]
        cfg = catalog.get(base)
        if not cfg or not bs.tier_le_1(cfg):
            expanded.extend(group)
            continue
        platforms = bs.catalog_platforms(cfg, catalog_defaults)
        charts = charts_by_base.get(base, [])
        chart_by_os = {chart_os(c): c for c in charts}
        row_by_bench = {base: group[0]}
        for plat in platforms:
            existing_row = next(
                (r for r in group if (r.get("os") or "linux") == plat),
                None,
            )
            if existing_row and (
                existing_row.get("li_value") is not None
                or existing_row.get("status") not in (None, "", "unknown", "skip")
            ):
                expanded.append(existing_row)
                continue
            ch = chart_by_os.get(plat)
            if ch:
                expanded.append(chart_row_from_chart(base, cfg, ch, row_by_bench))
            else:
                skip = bs.build_platform_skip_chart(
                    base,
                    cfg,
                    plat,
                    chart_id=bs.chart_id_for_os(base, plat, multi=len(platforms) > 1),
                    multi=len(platforms) > 1,
                    validity_source=f"platform:{plat}:not_measured",
                )
                expanded.append(chart_row_from_chart(base, cfg, skip, row_by_bench))
    summary["rows"] = sorted(
        expanded, key=lambda row: (row["tier"], row["benchmark"], row.get("os", ""))
    )


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
                }
                platforms = list(bs.PLATFORM_ORDER)
                multi = True
                for plat in platforms:
                    ch = bs.build_platform_skip_chart(
                        base,
                        stub_cfg,
                        plat,
                        chart_id=bs.chart_id_for_os(base, plat, multi=multi),
                        multi=multi,
                        validity_source="catalog:non_catalog_chart",
                    )
                    charts_out.append(ch)
                    charts_by_pillar[ch.get("pillar", cat_name)].append(ch)
                continue

            platforms = bs.catalog_platforms(cfg, catalog_defaults)
            multi = len(platforms) > 1
            existing: dict[str, dict] = {}
            for ch in group:
                existing[chart_os(ch)] = ch

            for plat in platforms:
                if plat in existing:
                    ch = dict(existing[plat])
                    series = ch.get("series") or []
                    has_csv = bool(series)
                    has_li = any(s.get("lang") == "li" for s in series)
                    sizes = bs.effective_size_meta(cfg, has_csv=has_csv)
                    ch.update({k: v for k, v in sizes.items() if v is not None})
                    ch["os"] = plat
                    if ch.get("pending") or not has_csv:
                        ch["validity_status"] = "skip"
                        ch["validity_source"] = ch.get("validity_source") or "platform_not_measured"
                        ch["status"] = "skip"
                    elif has_csv and not has_li and (
                        ch.get("status") in (None, "", "unknown")
                        or ch.get("validity_status") in (None, "", "unknown")
                    ):
                        ch["validity_status"] = "advisory"
                        ch["validity_source"] = (
                            ch.get("validity_source") or "competitor_only:no_li"
                        )
                        ch["status"] = "advisory"
                    elif ch.get("validity_status") in (None, "", "unknown"):
                        row = row_by_bench.get(base)
                        if row and row.get("validity_status") in ("pass", "fail", "skip", "advisory"):
                            ch["validity_status"] = row["validity_status"]
                            ch["validity_source"] = row.get("validity_source") or "summary.row"
                    if ch.get("status") in (None, "", "unknown") and ch.get("validity_status") == "skip":
                        ch["status"] = "skip"
                    charts_out.append(ch)
                    charts_by_pillar[ch.get("pillar", "numerics")].append(ch)
                    continue

                skip = bs.build_platform_skip_chart(
                    base,
                    cfg,
                    plat,
                    chart_id=bs.chart_id_for_os(base, plat, multi=multi),
                    multi=multi,
                    validity_source=f"platform:{plat}:not_measured",
                )
                charts_out.append(skip)
                charts_by_pillar[skip["pillar"]].append(skip)

        new_categories[cat_name] = {
            **cat_data,
            "charts": sorted(charts_out, key=lambda c: c["id"]),
        }

    for r in rows:
        cfg = catalog.get(r["benchmark"])
        if not cfg:
            continue
        has_csv = r.get("li_value") is not None
        sizes = bs.effective_size_meta(cfg, has_csv=has_csv)
        r.update({k: v for k, v in sizes.items() if v is not None})
        measured_status = r.get("status") in ("green", "yellow", "red", "advisory")
        if bs.tier_le_1(cfg) and r.get("pending") and not measured_status:
            r["validity_status"] = "skip"
            r["validity_source"] = r.get("validity_source") or "catalog:pending"
            r["status"] = "skip"
        elif bs.tier_le_1(cfg) and r.get("li_value") is None and r.get("status") in (None, "", "unknown"):
            r["validity_status"] = "skip"
            r["validity_source"] = r.get("validity_source") or "catalog:pending"
            r["status"] = "skip"
        elif r.get("status") in (None, "", "unknown") and r.get("validity_status") == "skip":
            r["status"] = "skip"

    summary["categories"] = new_categories
    summary["pillars"] = bs.build_pillars(dict(charts_by_pillar))
    summary["generated_at"] = datetime.now(timezone.utc).isoformat()
    os_values = sorted(
        {
            chart_os(ch)
            for cat in new_categories.values()
            for ch in cat.get("charts", [])
            if ch.get("os")
        }
    )
    reporting = summary.setdefault("reporting", {})
    reporting["os_values"] = os_values
    reporting["size_labels"] = sorted(
        {
            str(ch["size_label"])
            for cat in new_categories.values()
            for ch in cat.get("charts", [])
            if ch.get("size_label")
        }
    )
    expand_tier01_rows(summary, catalog, catalog_defaults)
    fix_linux_unknown_http_and_stdlib(summary, catalog)
    return summary


def main() -> int:
    if not SUMMARY.is_file():
        print(f"missing {SUMMARY}", file=sys.stderr)
        return 1
    catalog = bs.load_catalog()
    catalog_defaults = bs.load_catalog_defaults()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if os.environ.get("REFRESH_HTTP_STDlib_ONLY", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        changed = fix_linux_unknown_http_and_stdlib(summary, catalog)
        SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(
            f"refresh-dashboard-completeness: http/stdlib-only patched {SUMMARY} "
            f"({changed} rows/charts)"
        )
        return 0

    refreshed = refresh(summary, catalog, catalog_defaults)
    SUMMARY.write_text(json.dumps(refreshed, indent=2) + "\n", encoding="utf-8")
    charts = sum(len(c.get("charts", [])) for c in refreshed.get("categories", {}).values())
    print(f"refresh-dashboard-completeness: wrote {SUMMARY} ({charts} charts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
