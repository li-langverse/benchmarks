# shellcheck shell=bash
# Resolve python for benchmark scripts (Windows GHA often exposes `python` only).
bench_python() {
  if command -v python3 >/dev/null 2>&1; then
    python3 "$@"
    return
  fi
  if command -v python >/dev/null 2>&1; then
    python "$@"
    return
  fi
  echo "bench-python: python3 or python required" >&2
  return 127
}
