# HTTP webserver — benchmark & exploit growth registry

When **li-httpd** gains a capability, extend **both** throughput benches and exploit checks before merge. Run the **full matrix** after every implementation:

```bash
cd benchmarks
LIC_ROOT=../lic ./scripts/run-full-benchmark-suite.sh
./scripts/benchmark-matrix-report.py
```

Outputs: `data/latest/benchmark-matrix.json`, `data/latest/benchmark-matrix.md`, `data/latest/summary.json`.

## Mandatory gates (agents)

| Gate | Script | Pass |
|------|--------|------|
| Full org suite | `run-full-benchmark-suite.sh` | tier 0 warn-ok; tier 1–3 run; tier 5 HTTP + exploits |
| Full matrix | `benchmark-matrix-report.py` | exit 0; review `.md` |
| Failures digest | `benchmark-failures-report.sh` | no unexpected RED on touched PH-* |

Env: `SKIP_BUILD=1`, `SKIP_TIER0=1`, `SKIP_EXPLOITS=1` only for fast iteration — **never** for merge-worthy httpd PRs.

## Feature → bench + exploit checklist

| Feature (plan milestone) | Tier-5 throughput scenario | Exploit profile | Catalog `id` |
|--------------------------|----------------------------|-----------------|--------------|
| Static 1 KiB | `static_small` | pr | `static_small` |
| Static large | `static_large` | pr | `static_large` |
| Keep-alive pipeline | `keepalive_pipelining` | pr | `keepalive_pipelining` |
| Proxy loopback | `proxy_loopback` + supplemental `tier5-http-bench.py` | pr + weaponized | `proxy_loopback` |
| LB round-robin | `lb_round_robin` | pr | `lb_round_robin` |
| LB least-conn | `lb_least_conn` | pr | `lb_least_conn` |
| LB peer down | `lb_peer_down` | pr | `lb_peer_down` |
| Rate limit 429 | `rate_limit_429` (verify_pass, li only) | `connection_flood`, `bad_method` | ci + nightly |
| TLS / HTTPS | `https_static_small` (M1.5) | TLS renegotiation / cert probes | TBD |
| SSE streaming | `sse_long_stream` (M1.5) | `leak_openai_key_in_sse` | nightly |
| HTTP/2 | `h2_multiplex` (M2) | smuggling variants | nightly |
| WebSocket | `ws_echo` (M2) | binary abuse probes | TBD |

### Adding a new throughput scenario

1. `vendor/lis-tier5/benchmarks/tier5_http/scenarios/<id>/bench.toml`
2. `vendor/lis-tier5/benchmarks/tier5_http/suite.toml` — add to `profiles.ci` and `profiles.nightly`
3. `catalog.toml` — `category = "http"`, `compare_oracle = "nginx"`, `metric = "rps"`
4. Re-run full suite + matrix report

### Adding a new exploit

1. `vendor/lis-tier5/benchmarks/tier5_http/exploits/<id>.toml`
2. `suite_exploits.toml` — add to `profiles.pr` (CI) and/or `profiles.weaponized`
3. Driver in `harness/drivers/` if new attack class
4. Re-run `./scripts/run-tier5-http-exploits.sh` (included in full suite)

## Exploit profiles

| Profile | When | Includes |
|---------|------|----------|
| `pr` (default in full suite) | Every httpd merge | slowloris, smuggling basics, path traversal, … |
| `weaponized` | Before release / security PR | + chunked bomb, cache poison, pipeline stuffing |
| `nightly` | Scheduled agent run | + CL.TE / TE.CL smuggling, SSE leak probe |

Override: `TIER5_EXPLOIT_PROFILE=weaponized TIER5_EXPLOIT_LANGS=nginx,apache,li`.

## Multi-oracle HTTP (throughput)

`BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li` — proxy/LB scenarios remain **nginx + li** only until `PROXY_ORACLES` expands in `http_oracles.py`.
