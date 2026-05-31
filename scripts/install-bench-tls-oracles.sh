#!/usr/bin/env bash
# Install optional tier-5 TLS bench oracles (caddy, traefik) on Linux/WSL.
set -euo pipefail

install_caddy() {
  if command -v caddy >/dev/null; then
    return 0
  fi
  curl -fsSL "https://caddyserver.com/api/download?os=linux&arch=amd64" -o /tmp/caddy
  chmod +x /tmp/caddy
  sudo mv /tmp/caddy /usr/local/bin/caddy
}

install_traefik() {
  if command -v traefik >/dev/null; then
    return 0
  fi
  for ver in v3.2.5 v3.1.7 v2.11.24; do
    url="https://github.com/traefik/traefik/releases/download/${ver}/traefik_${ver}_linux_amd64.tar.gz"
    if curl -fsSL -o /tmp/traefik.tgz "$url"; then
      sudo tar -xzf /tmp/traefik.tgz -C /usr/local/bin traefik
      rm -f /tmp/traefik.tgz
      return 0
    fi
  done
  return 1
}

install_caddy || true
install_traefik || echo "warn: traefik install failed (bench will skip traefik oracle)" >&2

echo "oracles: nginx=$(command -v nginx || echo missing) caddy=$(command -v caddy || echo missing) traefik=$(command -v traefik || echo missing)"
