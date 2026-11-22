#!/usr/bin/env bash
set -euo pipefail
# Abre o TAPE em máquinas novas; preserva as configurações da extensão histórica.
if command -v arandu-tape-confluencia >/dev/null 2>&1; then
  exec arandu-tape-confluencia
fi
LEGACY="${XDG_DATA_HOME:-$HOME/.local/share}/arandu-lab/arandu-rivers/arandu-riversctl"
if [[ -x "$LEGACY" ]]; then exec "$LEGACY" toggle; fi
echo 'ARANDU TAPE não instalado.' >&2
exit 1
