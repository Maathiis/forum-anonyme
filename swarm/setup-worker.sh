#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./swarm/setup-worker.sh <TOKEN> <MANAGER_IP>
#
# Exemple:
#   ./swarm/setup-worker.sh "SWMTKN-..." 31.207.36.148

TOKEN="${1:-}"
MANAGER_IP="${2:-}"

if [[ -z "$TOKEN" || -z "$MANAGER_IP" ]]; then
  echo "Usage: $0 <TOKEN> <MANAGER_IP>" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker n'est pas installé (commande 'docker' introuvable)." >&2
  exit 1
fi

echo "==> Ouverture firewall (si ufw est disponible)"
if command -v ufw >/dev/null 2>&1; then
  ufw allow 7946/tcp || true
  ufw allow 7946/udp || true
  ufw allow 4789/udp || true
  # (optionnel) si tu exposes en mode host sur worker
  ufw allow 80/tcp || true
else
  cat <<'EOF'
UFW non détecté. Assure-toi d'ouvrir ces ports (au minimum) :
- 7946/tcp+udp : communication inter-nodes
- 4789/udp  : overlay networks
- 80/tcp    : HTTP si tu publies des ports en mode host sur le worker
EOF
fi

echo "==> Join Swarm (worker) vers ${MANAGER_IP}:2377"
docker swarm join --token "${TOKEN}" "${MANAGER_IP}:2377"

