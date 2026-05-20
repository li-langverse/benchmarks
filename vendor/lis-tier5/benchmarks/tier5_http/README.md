# Tier-5 HTTP benchmarks (`li-httpd` · nginx oracle)

## What runs today

`harness/bench_http.py` validates each scenario’s `bench.toml`, then — when `nginx` and `wrk` are on `PATH` — starts **stock nginx** in a private prefix serving `fixtures/static/`, runs **wrk**, and writes **`results/latest.csv`** (same column schema as `lic` bench exports).

Profiles come from `suite.toml`:

| Profile   | Timing | wrk duration (typical) |
|-----------|--------|-------------------------|
| `ci`      | off    | capped (default 3s via `BENCH_HTTP_QUICK_SEC`) |
| `nightly` | on     | uses `[load].duration_sec` from each scenario |

Scenarios in `suite.toml` **ci** / **nightly**: `static_small`, `keepalive_pipelining`, `static_large` (GET `/file.bin`, 1 MiB fixture auto-generated).

`lang=li` throughput rows are **not** emitted until a `li-httpd` binary is wired in; set `LI_HTTPD_BIN` only as a placeholder hook for future work.

## Exploit harness (security)

`harness/exploit_http.py` runs TOML-driven attacks from `exploits/` against **nginx** (oracle) and **li-httpd** on loopback only.

| Tier | Examples |
|------|----------|
| A/B | slowloris, oversized line, duplicate Content-Length |
| **C** | `reverse_shell_canary` (localhost callback sink), `sensitive_file_read`, `shellshock_user_agent`, `privilege_path_escalation`, `command_injection_path`, `host_header_ssrf` |

Tier **C** probes RCE / reverse-shell / priv-esc *classes* — they do **not** deploy real shells or dial external hosts.

```bash
LI_HTTPD_BIN=/path/to/lic/build/li-httpd \
  python3 benchmarks/tier5_http/harness/exploit_http.py --profile pr
# Oracles: nginx + apache2 + li-httpd
TIER5_EXPLOIT_LANGS=nginx,apache,li ./scripts/run-tier5-http-exploits.sh
# Nightly adds CL.TE / TE.CL smuggling probes
TIER5_EXPLOIT_PROFILE=nightly TIER5_EXPLOIT_LANGS=nginx,apache,li \
  python3 benchmarks/tier5_http/harness/exploit_http.py --profile nightly
cat ../results/exploit_report.csv
```

**CI:** Benchmarks `ci.yml` builds `li-httpd` and runs `./scripts/run-tier5-http-exploits.sh` with `TIER5_EXPLOIT_LANGS=nginx,apache,li` (requires `apache2` package).

## Quick commands (from lis repo root)

```bash
# TOML-only / harness rows (no nginx)
python3 benchmarks/tier5_http/harness/bench_http.py --profile ci --no-bench

# Full nginx + wrk (install deps first, Linux example)
sudo apt-get install -y nginx wrk
python3 benchmarks/tier5_http/harness/bench_http.py --profile ci
cat results/latest.csv
```

Single scenario:

```bash
python3 benchmarks/tier5_http/harness/bench_http.py static_small --profile nightly
```

## Downstream ingest

The **benchmarks** repo merges `lis/results/latest.csv` when building `data/latest/summary.json` (`compare_oracle = "nginx"` for tier-5 HTTP rows in `catalog.toml`).
