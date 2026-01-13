#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./swarm/setup-manager.sh <ADVERTISE_IP>
#
# Exemple:
#   ./swarm/setup-manager.sh 31.207.36.148

ADVERTISE_IP="${1:-}"
if [[ -z "$ADVERTISE_IP" ]]; then
  echo "Usage: $0 <ADVERTISE_IP>" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker n'est pas installé (commande 'docker' introuvable)." >&2
  exit 1
fi

echo "==> Initialisation Swarm (manager) avec advertise-addr=${ADVERTISE_IP}"
docker swarm init --advertise-addr "${ADVERTISE_IP}" || true

echo "==> Ouverture firewall (si ufw est disponible)"
if command -v ufw >/dev/null 2>&1; then
  # Swarm
  ufw allow 2377/tcp || true
  ufw allow 7946/tcp || true
  ufw allow 7946/udp || true
  ufw allow 4789/udp || true
  # App
  ufw allow 80/tcp || true
  ufw allow 443/tcp || true
else
  cat <<'EOF'
UFW non détecté. Assure-toi d'ouvrir ces ports (au minimum) :
- 2377/tcp  : Swarm cluster management
- 7946/tcp+udp : communication inter-nodes
- 4789/udp  : overlay networks
- 80/tcp    : HTTP (front)
EOF
fi

echo "==> Token worker (à utiliser sur le worker) :"
docker swarm join-token worker

echo "==> Nœuds Swarm :"
docker node ls

