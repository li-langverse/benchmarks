# lic ↔ benchmarks httpd compatibility

## Which `lic` checkout for tier-5 HTTP?

| `lic` branch / `main` | `build/li-httpd` | Tier-5 wrk RPS | Routing tests |
|----------------------|------------------|----------------|---------------|
| **`origin/main`** (2026-05-21) | Stub `tcp_*` + `li_rt_httpd` oracle | **Not representative** — do not tune RPS gates on main alone |
| **`cursor/httpd-masterplan-54aa`** | Full epoll proxy/static (`runtime/li_rt_net.c`) | **Use for** `run-full-benchmark-suite.sh`, `httpd-masterplan-step.sh` |

Another agent may advance **`lic` `main`** (routing loader, `lic httpd validate-config`, math-linalg). Rebase the httpd perf branch before claiming bench regressions.

## Commands

```bash
# Full HTTP perf + exploits (canonical today)
LIC_ROOT=/path/to/lic  # checkout cursor/httpd-masterplan-54aa
cd benchmarks
SKIP_BUILD=0 ./scripts/run-full-benchmark-suite.sh
python3 scripts/benchmark-matrix-report.py
```

```bash
# Config-only on latest main
cd lic && ./build/compiler/lic/lic httpd validate-config packages/li-httpd/examples/rate_limit.toml
```

## Merge gate

When epoll `li-httpd` lands on `lic` `main`, re-run step-0 baseline and drop the branch pin in agent notes.
