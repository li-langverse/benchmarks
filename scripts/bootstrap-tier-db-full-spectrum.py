#!/usr/bin/env python3
"""One-shot scaffold for WP-N4 tier_db_* full-spectrum stubs (idempotent)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TIERS: list[dict] = [
    {
        "dir": "tier_db_security",
        "slug": "security",
        "artifact": "tier-db-security.json",
        "schema_sql": "security-audit-v1.sql",
        "scenarios": [
            ("injection_blocked", "pass_rate", "ratio", "SQL injection attempts must fail closed"),
            ("rls_bypass_blocked", "pass_rate", "ratio", "RLS bypass / privilege escalation attempts blocked"),
        ],
        "suite_include": ["injection_blocked", "rls_bypass_blocked"],
        "ph_ids": '["WP-N4", "PH-DB-SEC"]',
        "workload_kind": "security_probe",
    },
    {
        "dir": "tier_db_memory",
        "slug": "memory",
        "artifact": "tier-db-memory.json",
        "schema_sql": "memory-baseline-v1.sql",
        "scenarios": [
            ("rss_idle", "rss_mb", "mb", "Process RSS after cold start (idle)"),
            ("rss_peak_load", "rss_mb", "mb", "Peak RSS under sustained read/write load"),
        ],
        "suite_include": ["rss_idle", "rss_peak_load"],
        "ph_ids": '["WP-N4", "PH-DB-MEM"]',
        "workload_kind": "memory_profile",
    },
    {
        "dir": "tier_db_parallel",
        "slug": "parallel",
        "artifact": "tier-db-parallel.json",
        "schema_sql": "parallel-load-v1.sql",
        "scenarios": [
            ("concurrent_readers", "ops_per_sec", "ops", "Scalable concurrent SELECT throughput"),
            ("concurrent_writers", "ops_per_sec", "ops", "Scalable concurrent INSERT/UPDATE throughput"),
        ],
        "suite_include": ["concurrent_readers", "concurrent_writers"],
        "ph_ids": '["WP-N4", "PH-DB-PAR"]',
        "workload_kind": "parallel_load",
    },
    {
        "dir": "tier_db_audit",
        "slug": "audit",
        "artifact": "tier-db-audit.json",
        "schema_sql": "audit-log-v1.sql",
        "scenarios": [
            ("query_log_complete", "completeness_ratio", "ratio", "Every privileged query appears in audit log"),
            ("tamper_evidence", "pass_rate", "ratio", "Log chain / digest detects tamper"),
        ],
        "suite_include": ["query_log_complete", "tamper_evidence"],
        "ph_ids": '["WP-N4", "PH-DB-AUD"]',
        "workload_kind": "audit_verify",
    },
    {
        "dir": "tier_db_realtime",
        "slug": "realtime",
        "artifact": "tier-db-realtime.json",
        "schema_sql": "realtime-channel-v1.sql",
        "scenarios": [
            ("ws_publish_latency", "latency_p95", "ms", "WebSocket publish→client delivery P95"),
        ],
        "suite_include": ["ws_publish_latency"],
        "ph_ids": '["WP-N4", "PH-DB-RT"]',
        "workload_kind": "realtime_ws",
    },
]


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def suite_toml(include: list[str]) -> str:
    inc = ", ".join(f'"{s}"' for s in include)
    return f"""[default]
include = [{inc}]
timing = false

[profiles.ci]
include = [{inc}]
timing = false

[profiles.nightly]
include = [{inc}]
timing = true
"""


def defaults_toml(schema_sql: str) -> str:
    return f"""[schema]
migration = "schema/{schema_sql}"
postgres_min_version = "15"

[engines]
lidb = "lis db start --profile audit-min"
postgres = "psql"

[load]
warmup_iters = 50
measure_iters = 500
clients = 8

[targets]
threshold_ratio_vs_postgres = 1.0

[metrics]
primary = "pass_rate"
unit = "ratio"
lower_is_better = false
"""


def bench_toml(name: str, kind: str, metric: str, unit: str, note: str) -> str:
    return f"""name = "{name}"

[workload]
kind = "{kind}"
notes = "{note}"

[verify]
min_rows = 1

[load]
metric = "{metric}"
unit = "{unit}"
"""


def tier_readme(tier_dir: str, title: str, scenarios: list, doc_link: str, run_script: str, artifact: str) -> str:
    rows = "\n".join(f"| `{s[0]}` | {s[3]} | `{s[1]}` ({s[2]}) |" for s in scenarios)
    return f"""# {tier_dir} — {title}

Full-spectrum **lidb** audit benchmark tier (WP-N4 stub). Harness compares **lidb** vs **PostgreSQL 15+** where applicable.

## Scenarios

| Scenario | Measures | Primary metric |
|----------|----------|----------------|
{rows}

## Run (stub)

```bash
cd benchmarks
./scripts/{run_script}
cat data/latest/{artifact}
```

Env: `BENCH_DB_{tier_dir.upper().replace('tier_db_', '')}_PROFILE=ci|nightly`, `POSTGRES_URL`, `LIDB_URL`.

## CI ingest

Manifest: `data/latest/{artifact}` — see [`schema/tier-db-{tier_dir.replace('tier_db_', '')}-ingest.json`](../../schema/tier-db-{tier_dir.replace('tier_db_', '')}-ingest.json).

Doc: [{doc_link}](../../docs/ecosystem/tier-db-{tier_dir.replace('tier_db_', '')}.md).
"""


def main() -> int:
    for t in TIERS:
        tier_dir = t["dir"]
        root = ROOT / "benchmarks" / tier_dir
        w(root / "suite.toml", suite_toml(t["suite_include"]))
        w(root / "defaults.toml", defaults_toml(t["schema_sql"]))
        w(
            root / "schema" / t["schema_sql"],
            f"-- {tier_dir} stub schema (WP-N4)\n-- Harness applies before load; align with lidb migrations.\nSELECT 1;\n",
        )
        for sid, metric, unit, note in t["scenarios"]:
            w(
                root / "scenarios" / sid / "bench.toml",
                bench_toml(sid, t["workload_kind"], metric, unit, note),
            )
        slug = t["slug"]
        w(
            root / "README.md",
            tier_readme(
                tier_dir,
                slug.replace("_", " ").title(),
                t["scenarios"],
                f"tier-db-{slug}.md",
                f"run-db-{slug}-bench.sh",
                t["artifact"],
            ),
        )
    print("bootstrap-tier-db-full-spectrum: wrote tier suites under benchmarks/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
