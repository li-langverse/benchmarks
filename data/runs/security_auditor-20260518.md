# Security auditor pass — li-langverse org sweep

**Run:** `security:org:sweep` · **Generated:** 2026-05-18T22:30Z  
**Catalog:** `lic/security/cve-catalog.json` (39 entries)  
**Preflight:** `benchmarks/scripts/security-cwe-audit.py` → `data/latest/security-cwe-audit.json`

**North star:** secure + provable — no `trusted.lean` changes; exploit tests unchanged.

---

## Executive summary

- Ran CVE/CWE org audit against `lic/security/cve-catalog.json` (39 rows); **0 required `li_test` gaps** after excluding `asan_target` / `not_applicable` mitigations.
- **8 / 9** org repos in audit scope lack a `security-gate` or `cve-catalog` workflow on GitHub (`lic` has `cve-catalog.yml`).
- Opened **li-demo#4** adding downstream `security-gate.yml` (runs `lic/scripts/ci-security.sh`).
- **lic#46** (in flight) adds the same template to all `lic/packages/*` mirrors; merge before rolling to remaining standalone repos.
- **benchmarks#34** carries the `security-cwe-audit.py` preflight fix (`gh --jq` JSONDecodeError); audit JSON refreshed on branch.
- **Attack-surface PRs** `lic#40` / `lic#47` (lexer/codegen) touch parse surface without new `li-tests/security/*` or lexer security rows — **comment / gate** before merge.
- **5 catalog rows** with `li_test: null` and `not_applicable` (nginx/http_future) — tracked, no Li test required until HTTP stack ships.
- **5 rows** with `li_test: null` and `asan_target` — covered by `lic` `memory.yml` / ASan jobs, not `li-tests/security/*`.

---

## Deliverable / findings

### CWE → repo → action

| CWE | Repo | Action |
|-----|------|--------|
| CWE-120 (parser/check class) | **lic** | Covered — `cve-catalog.yml` + `li-tests/security/deeply_nested_calls.li`, `pathological_generics.li` |
| CWE-78, CWE-88 | **lic** | Covered — `li-tests/security/codegen_path_injection.sh` |
| CWE-125, CWE-787, CWE-676, … | **lic** | Covered — `li-tests/cve_patterns/*`; ASan-null rows → `memory.yml` |
| CWE-787 (nginx/http_future) | **lic** | Deferred — `li_mitigation=not_applicable` until HTTP server in Li |
| CWE-120 | **li-demo** | **workflow** — PR [#4](https://github.com/li-langverse/li-demo/pull/4) `security-gate.yml` |
| CWE-120 | **li-httpd**, **li-net** | **workflow** — roll `security-gate.yml` (after lic#46) |
| CWE-120 | **lip**, **lit**, **lis** | **workflow** — roll `security-gate.yml` |
| CWE-120 | **benchmarks** | **workflow** — roll `security-gate.yml`; merge preflight **#34** |
| CWE-120 | **li-cursor-agents** | **workflow** — roll `security-gate.yml` (agent orchestration, no Li src) |
| CWE-120 | **lic#40**, **lic#47** | **review** — lexer/codegen PRs without CVE test delta; require `run_security.sh` green |

### Catalog gaps (`li_test` null)

| CVE | CWE | `li_mitigation` | Action |
|-----|-----|-----------------|--------|
| CVE-2022-37434 | CWE-787 | asan_target | ASan job — no new `li-tests/security/*` |
| CVE-2023-0286 | CWE-125 | asan_target | ASan job |
| CVE-2023-4863 | CWE-787 | asan_target | ASan job |
| CVE-2019-1010022 | CWE-676 | asan_target | ASan job |
| CVE-2015-0235 | CWE-787 | asan_target | ASan job |
| CVE-2013-2028 | CWE-787 | not_applicable | Issue when HTTP stack lands |
| CVE-2017-7529 | CWE-125 | not_applicable | Issue when HTTP stack lands |
| CVE-2021-23017 | CWE-787 | not_applicable | Issue when HTTP stack lands |

### PR URLs (implemented this run)

| Repo | PR | Change |
|------|-----|--------|
| li-demo | https://github.com/li-langverse/li-demo/pull/4 | `security-gate.yml` |
| benchmarks | https://github.com/li-langverse/benchmarks/pull/34 | `security-cwe-audit.py` preflight (existing) |
| lic | https://github.com/li-langverse/lic/pull/46 | Package mirror `security-gate.yml` template (existing) |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| `chore(security): roll security-gate.yml to lip/lit/lis/benchmarks/li-httpd/li-net/li-cursor-agents` | each repo | `security`, `agent-kit` |
| `security: require run_security.sh on lexer/codegen PRs (CVE-LLVM-PARSER-CLASS / CWE-120)` | lic | `security`, `governance` |
| `plan-needed: HTTP/nginx CVE rows when li-httpd parses requests` | roadmap | `security`, `plan-needed` |
| Merge **benchmarks#34** then wire `security_cwe_audit` into briefing (remove `--skip-slow` gap) | benchmarks | `ci` |

---

## Deferred

- Bulk workflow rollout to 7 remaining repos (single agent-kit rollout after **lic#46** merges).
- New `li-tests/security/*` for `asan_target` catalog rows (intentionally ASan-scoped).
- `trusted.lean` / exploit test changes — human-only per swarm mandate.
- `li-language`, `roadmap`, `li-local-ci` — out of `ORG_REPOS` audit list; add when org mirror policy extends.
