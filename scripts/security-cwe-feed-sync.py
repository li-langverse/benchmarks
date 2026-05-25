#!/usr/bin/env python3
"""Sync MITRE CWE Top 25 snapshot vs lic cve-catalog — delta for security_auditor briefing."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/security-cwe-feed.json"
DELTA_OUT = ROOT / "data/latest/security-cwe-feed-delta.json"
PREV = ROOT / "data/latest/security-cwe-feed-prev.json"
LIC = Path(os.environ.get("LIC_ROOT", ROOT.parent / "lic"))
CATALOG = LIC / "security" / "cve-catalog.json"

# MITRE 2023 CWE Top 25 (stable baseline; web fetch may refresh ordering)
CWE_TOP_25_BASELINE = [
    "CWE-787",
    "CWE-79",
    "CWE-89",
    "CWE-416",
    "CWE-78",
    "CWE-20",
    "CWE-125",
    "CWE-22",
    "CWE-352",
    "CWE-434",
    "CWE-862",
    "CWE-476",
    "CWE-287",
    "CWE-190",
    "CWE-502",
    "CWE-77",
    "CWE-119",
    "CWE-798",
    "CWE-918",
    "CWE-306",
    "CWE-362",
    "CWE-269",
    "CWE-94",
    "CWE-863",
    "CWE-276",
]


def fetch_top25_web() -> list[str] | None:
    """Best-effort fetch; returns None on failure."""
    url = os.environ.get(
        "CWE_TOP25_URL",
        "https://cwe.mitre.org/data/definitions/699/699.json",
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    ids: list[str] = []
    if isinstance(data, dict):
        for key in ("Weaknesses", "weaknesses", "entries"):
            block = data.get(key)
            if isinstance(block, list):
                for row in block[:40]:
                    if not isinstance(row, dict):
                        continue
                    wid = row.get("ID") or row.get("id") or row.get("CWE_ID")
                    if wid:
                        ids.append(f"CWE-{wid}" if not str(wid).startswith("CWE") else str(wid))
                if ids:
                    return ids[:25]
    return None


def catalog_cwes() -> set[str]:
    if not CATALOG.is_file():
        return set()
    try:
        doc = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    entries = doc if isinstance(doc, list) else doc.get("entries") or []
    found: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        for key in ("cwe", "cwe_id", "CWE", "cwe_ids"):
            val = entry.get(key)
            if isinstance(val, list):
                for v in val:
                    if v:
                        found.add(normalize_cwe(str(v)))
            elif val:
                found.add(normalize_cwe(str(val)))
    return found


def normalize_cwe(raw: str) -> str:
    m = re.search(r"CWE[- ]?(\d+)", raw, re.I)
    return f"CWE-{m.group(1)}" if m else raw.strip()


def main() -> int:
    web_top = fetch_top25_web()
    top25 = web_top or CWE_TOP_25_BASELINE
    feed_source = "mitre_top25_web" if web_top else "mitre_top25_baseline"
    in_catalog = catalog_cwes()
    missing_in_catalog = [c for c in top25 if c not in in_catalog]
    new_vs_prev: list[str] = []
    if PREV.is_file():
        try:
            prev_doc = json.loads(PREV.read_text(encoding="utf-8"))
            prev_set = set(prev_doc.get("top25") or [])
            new_vs_prev = [c for c in top25 if c not in prev_set]
        except (OSError, json.JSONDecodeError):
            pass

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    feed = {
        "generated_at": stamp,
        "synced_at": stamp,
        "source": feed_source,
        "catalog_path": str(CATALOG) if CATALOG.is_file() else None,
        "top25": top25,
        "catalog_cwe_count": len(in_catalog),
        "top25_missing_in_catalog": missing_in_catalog,
        "summary": {
            "top25_count": len(top25),
            "missing_in_catalog": len(missing_in_catalog),
            "new_vs_previous_sync": len(new_vs_prev),
        },
    }
    delta = {
        "generated_at": stamp,
        "new_cwes": new_vs_prev,
        "missing_in_catalog": missing_in_catalog,
        "catalog_gaps_hint": [
            {"cwe": c, "reason": "CWE Top 25 not represented in cve-catalog.json"}
            for c in missing_in_catalog[:15]
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.is_file():
        OUT.replace(PREV)
    OUT.write_text(json.dumps(feed, indent=2) + "\n", encoding="utf-8")
    DELTA_OUT.write_text(json.dumps(delta, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {OUT} top25={len(top25)} missing_in_catalog={len(missing_in_catalog)} "
        f"new_vs_prev={len(new_vs_prev)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
