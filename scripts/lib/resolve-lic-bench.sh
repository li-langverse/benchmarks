#!/usr/bin/env bash
# Resolve built lic compiler binary (lic vs lic.exe on MSYS2 UCRT).
resolve_lic_bench_bin() {
  local root="${1:-${LIC_ROOT:-}}"
  local dir="$root/build/compiler/lic"
  if [[ -x "$dir/lic.exe" ]]; then
    echo "$dir/lic.exe"
  elif [[ -x "$dir/lic" ]]; then
    echo "$dir/lic"
  else
    echo "$dir/lic"
  fi
}

export_lic_bench_paths() {
  local root="${1:-${LIC_ROOT:-}}"
  export LIC_ROOT="$root"
  export LI_REPO_ROOT="$root"
  export PATH="$root/build/compiler/lic:$PATH"
  export LIC="$(resolve_lic_bench_bin "$root")"
  export LI_HTTPD_BIN="$root/build/li-httpd"
}
