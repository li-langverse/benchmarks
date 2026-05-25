#!/usr/bin/env python3
"""Measure character and token counts for tier_db_token_efficiency scenarios."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TIER_ROOT = Path(__file__).resolve().parent
SCENARIOS_PATH = TIER_ROOT / "scenarios.json"
BASELINE_SURFACE = "sql"
COMPARE_SURFACES = ("liq", "prisma", "drizzle", "supabase_js", "postgrest", "graphql")

_ENCODER = None
_ENCODER_NAME = "unknown"


def _load_encoder():
    global _ENCODER, _ENCODER_NAME
    try:
        import tiktoken

        _ENCODER = tiktoken.get_encoding("cl100k_base")
        _ENCODER_NAME = "tiktoken_cl100k_base"
        return
    except ImportError:
        pass
    _ENCODER = None
    _ENCODER_NAME = "heuristic_words_x_1.3"


def count_tokens(text: str) -> int:
    if _ENCODER is not None:
        return len(_ENCODER.encode(text))
    words = len(re.findall(r"\S+", text))
    return max(1, round(words * 1.3))


def count_chars(text: str) -> int:
    return len(text)


def delta_pct(baseline: int, value: int) -> float | None:
    if baseline <= 0:
        return None
    return round(100.0 * (value - baseline) / baseline, 1)


def compression_ratio(baseline: int, value: int) -> float | None:
    if value <= 0:
        return None
    return round(baseline / value, 3)


def scenario_metrics(scenario: dict) -> dict:
    queries: dict[str, str] = dict(scenario.get("queries") or {})
    if "liq_2step" in queries and "liq" not in queries:
        queries["liq"] = queries["liq_2step"]

    measured: dict[str, dict] = {}
    for surface, text in queries.items():
        if not isinstance(text, str) or not text.strip():
            continue
        measured[surface] = {
            "chars": count_chars(text),
            "tokens": count_tokens(text),
            "text_preview": text[:120] + ("…" if len(text) > 120 else ""),
        }

    sql_tokens = measured.get(BASELINE_SURFACE, {}).get("tokens")
    row: dict = {
        "id": scenario["id"],
        "domain": scenario.get("domain"),
        "intent": scenario.get("intent"),
        "safety_note": scenario.get("safety_note"),
        "surfaces": measured,
    }
    if sql_tokens:
        for surface in (*COMPARE_SURFACES, "liq_2step"):
            if surface not in measured:
                continue
            tok = measured[surface]["tokens"]
            row.setdefault("vs_sql", {})[surface] = {
                "delta_pct": delta_pct(sql_tokens, tok),
                "compression_ratio": compression_ratio(sql_tokens, tok),
            }
    return row


def build_report(scenarios_doc: dict) -> dict:
    rows = [scenario_metrics(s) for s in scenarios_doc["scenarios"]]
    sql_tot = sum(r["surfaces"].get("sql", {}).get("tokens", 0) for r in rows)
    liq_tot = sum(r["surfaces"].get("liq", {}).get("tokens", 0) for r in rows)
    summary = {
        "scenario_count": len(rows),
        "sql_tokens_total": sql_tot,
        "liq_tokens_total": liq_tot,
        "liq_vs_sql_delta_pct_total": delta_pct(sql_tot, liq_tot),
        "liq_vs_sql_compression_total": compression_ratio(sql_tot, liq_tot),
    }
    by_surface: dict[str, list[int]] = {}
    for r in rows:
        for surf, m in r["surfaces"].items():
            by_surface.setdefault(surf, []).append(m["tokens"])
    summary["median_tokens_by_surface"] = {
        s: sorted(v)[len(v) // 2] for s, v in sorted(by_surface.items())
    }
    return {
        "encoder": _ENCODER_NAME,
        "baseline_surface": BASELINE_SURFACE,
        "scenarios": rows,
        "summary": summary,
    }


def main() -> int:
    _load_encoder()
    doc = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    report = build_report(doc)
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    payload = json.dumps(report, indent=2) + "\n"
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8")
        print(f"wrote {out_path} (encoder={_ENCODER_NAME}, scenarios={report['summary']['scenario_count']})")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
