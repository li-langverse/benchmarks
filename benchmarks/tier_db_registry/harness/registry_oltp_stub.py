#!/usr/bin/env python3
"""Local registry OLTP stub — validate tier config; optional SQLite timing dry-run.

Does not require lidb or Postgres. Nightly profile with --run-timing exercises the
same SQL paths against SQLite for harness plumbing only (not P95 parity evidence).
"""
from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import statistics
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path

TIER_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_IDS = (
    "registry_publish",
    "registry_read_by_name",
    "registry_read_latest",
)
POSTGRES_SCHEMA = TIER_ROOT / "schema/registry-v1.sql"
SQLITE_SCHEMA = TIER_ROOT / "schema/registry-sqlite-v1.sql"
SEED_FIXTURE = TIER_ROOT / "fixtures/seed.toml"
RESULTS_CSV = TIER_ROOT / "results/latest.csv"


@dataclass(frozen=True)
class SeedData:
    publisher: str
    package: str
    versions: list[tuple[str, str, float, str]]
    attestation_kind: str
    attestation_payload: str


def load_seed() -> SeedData:
    raw = tomllib.loads(SEED_FIXTURE.read_text(encoding="utf-8"))
    versions = [tuple(row) for row in raw["versions"]["rows"]]
    return SeedData(
        publisher=raw["publisher"]["name"],
        package=raw["package"]["name"],
        versions=versions,
        attestation_kind=raw["attestation"]["kind"],
        attestation_payload=raw["attestation"]["payload_json"],
    )


def validate_tier_layout() -> list[str]:
    errors: list[str] = []
    for rel in ("suite.toml", "defaults.toml"):
        if not (TIER_ROOT / rel).is_file():
            errors.append(f"missing {rel}")
    if not POSTGRES_SCHEMA.is_file():
        errors.append("missing schema/registry-v1.sql")
    if not SQLITE_SCHEMA.is_file():
        errors.append("missing schema/registry-sqlite-v1.sql")
    if not SEED_FIXTURE.is_file():
        errors.append("missing fixtures/seed.toml")
    for sid in SCENARIO_IDS:
        bench = TIER_ROOT / "scenarios" / sid / "bench.toml"
        if not bench.is_file():
            errors.append(f"missing scenario {sid}/bench.toml")
            continue
        data = tomllib.loads(bench.read_text(encoding="utf-8"))
        if data.get("name") != sid:
            errors.append(f"{sid}: name mismatch in bench.toml")
        if "load" not in data or data["load"].get("metric") != "latency_p95":
            errors.append(f"{sid}: expected load.metric = latency_p95")
    suite = tomllib.loads((TIER_ROOT / "suite.toml").read_text(encoding="utf-8"))
    for sid in SCENARIO_IDS:
        if sid not in suite.get("default", {}).get("include", []):
            errors.append(f"suite.toml default.include missing {sid}")
    return errors


def open_sqlite() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript(SQLITE_SCHEMA.read_text(encoding="utf-8"))
    conn.row_factory = sqlite3.Row
    return conn


def seed_registry(conn: sqlite3.Connection, seed: SeedData) -> int:
    conn.execute(
        "INSERT INTO publishers (name) VALUES (?)",
        (seed.publisher,),
    )
    pub_id = conn.execute(
        "SELECT id FROM publishers WHERE name = ?", (seed.publisher,)
    ).fetchone()["id"]
    conn.execute(
        "INSERT INTO packages (name, publisher_id) VALUES (?, ?)",
        (seed.package, pub_id),
    )
    pkg_id = conn.execute(
        "SELECT id FROM packages WHERE name = ?", (seed.package,)
    ).fetchone()["id"]
    last_pv_id = 0
    for version, proof, coverage, tree in seed.versions:
        conn.execute(
            """
            INSERT INTO package_versions
              (package_id, version, proof_digest, coverage_pct, tree_digest)
            VALUES (?, ?, ?, ?, ?)
            """,
            (pkg_id, version, proof, coverage, tree),
        )
        last_pv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            """
            INSERT INTO attestations (package_version_id, kind, payload)
            VALUES (?, ?, ?)
            """,
            (last_pv_id, seed.attestation_kind, seed.attestation_payload),
        )
    conn.commit()
    return int(pkg_id)


def publish_once(conn: sqlite3.Connection, seed: SeedData, n: int) -> None:
    suffix = f"-{n}"
    conn.execute(
        "INSERT OR IGNORE INTO publishers (name) VALUES (?)",
        (seed.publisher + suffix,),
    )
    pub_id = conn.execute(
        "SELECT id FROM publishers WHERE name = ?",
        (seed.publisher + suffix,),
    ).fetchone()["id"]
    pkg_name = f"{seed.package}{suffix}"
    conn.execute(
        "INSERT INTO packages (name, publisher_id) VALUES (?, ?)",
        (pkg_name, pub_id),
    )
    pkg_id = conn.execute(
        "SELECT id FROM packages WHERE name = ?", (pkg_name,)
    ).fetchone()["id"]
    ver = f"0.0.{n}"
    conn.execute(
        """
        INSERT INTO package_versions
          (package_id, version, proof_digest, coverage_pct, tree_digest)
        VALUES (?, ?, ?, ?, ?)
        """,
        (pkg_id, ver, f"sha256:proof{n}", 90.0, f"sha256:tree{n}"),
    )
    pv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute(
        """
        INSERT INTO attestations (package_version_id, kind, payload)
        VALUES (?, ?, ?)
        """,
        (pv_id, seed.attestation_kind, seed.attestation_payload),
    )
    conn.commit()


def read_by_name_once(conn: sqlite3.Connection, seed: SeedData) -> None:
    conn.execute(
        "SELECT id, name, publisher_id, created_at FROM packages WHERE name = ? LIMIT 1",
        (seed.package,),
    ).fetchone()


def read_latest_once(conn: sqlite3.Connection, seed: SeedData) -> None:
    conn.execute(
        """
        SELECT pv.id, pv.version, pv.proof_digest, pv.published_at
        FROM package_versions pv
        JOIN packages p ON p.id = pv.package_id
        WHERE p.name = ?
        ORDER BY pv.published_at DESC
        LIMIT 1
        """,
        (seed.package,),
    ).fetchone()


def p95_ms(samples_ms: list[float]) -> float:
    if not samples_ms:
        return 0.0
    if len(samples_ms) == 1:
        return samples_ms[0]
    ordered = sorted(samples_ms)
    idx = max(0, int(round(0.95 * (len(ordered) - 1))))
    return ordered[idx]


def time_scenario(
    fn,
    *,
    warmup: int,
    measure: int,
) -> tuple[float, float]:
    for _ in range(warmup):
        fn()
    samples: list[float] = []
    for _ in range(measure):
        t0 = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - t0) * 1000.0)
    return statistics.median(samples), p95_ms(samples)


def run_timing(
    *,
    profile: str,
    warmup: int,
    measure: int,
) -> list[dict]:
    seed = load_seed()
    rows: list[dict] = []
    if profile == "ci":
        warmup = min(warmup, 5)
        measure = min(measure, 20)
    for sid in SCENARIO_IDS:
        conn = open_sqlite()
        seed_registry(conn, seed)
        counter = {"n": 0}

        def run_once() -> None:
            if sid == "registry_publish":
                counter["n"] += 1
                publish_once(conn, seed, counter["n"])
            elif sid == "registry_read_by_name":
                read_by_name_once(conn, seed)
            else:
                read_latest_once(conn, seed)

        p50, p95 = time_scenario(run_once, warmup=warmup, measure=measure)
        conn.close()
        rows.append(
            {
                "benchmark": sid,
                "lang": "sqlite_stub",
                "metric": "latency_p95",
                "value": round(p95, 4),
                "unit": "ms",
                "variant": "registry_oltp",
                "p50_ms": round(p50, 4),
            }
        )
    return rows


def write_csv(rows: list[dict]) -> Path:
    RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["benchmark", "lang", "metric", "value", "unit", "variant"]
    with RESULTS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return RESULTS_CSV


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", default="ci", choices=("ci", "nightly"))
    ap.add_argument(
        "--validate-only",
        action="store_true",
        help="Check suite/scenarios/schema/fixtures (CI dry-run)",
    )
    ap.add_argument(
        "--run-timing",
        action="store_true",
        help="SQLite stub timings → results/latest.csv (not lidb/postgres parity)",
    )
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--measure", type=int, default=1000)
    ap.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional harness summary JSON for manifest writer",
    )
    args = ap.parse_args()

    errors = validate_tier_layout()
    if errors:
        for e in errors:
            print(f"registry_oltp_stub: {e}", file=__import__("sys").stderr)
        return 1

    if args.validate_only:
        conn = open_sqlite()
        seed_registry(conn, load_seed())
        conn.close()
        print(
            f"registry_oltp_stub: OK (profile={args.profile}, "
            f"scenarios={len(SCENARIO_IDS)}, schema=sqlite+postgres paths)"
        )
        return 0

    if not args.run_timing:
        print("registry_oltp_stub: validation OK (use --run-timing for SQLite dry-run)")
        return 0

    rows = run_timing(
        profile=args.profile, warmup=args.warmup, measure=args.measure
    )
    csv_path = write_csv(rows)
    print(f"registry_oltp_stub: wrote {csv_path} ({len(rows)} rows, engine=sqlite_stub)")

    if args.json_out:
        payload = {
            "engine_mode": "sqlite_local_stub",
            "profile": args.profile,
            "results_csv": str(csv_path.relative_to(TIER_ROOT.parent.parent)),
            "rows": rows,
            "ph_ids": ["PH-DB-5"],
            "ph_dependencies": ["PH-DB-1", "PH-DB-4"],
            "notes": "SQLite stub only — replace with lidb vs Postgres 15+ for PH-DB-5 evidence",
        }
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"registry_oltp_stub: wrote {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
