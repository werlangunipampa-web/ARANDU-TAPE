#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$ROOT/verificar.py"
[[ -f "$ROOT/TOPBAR/arandu-topbar@local/metadata.json" ]] || { echo 'Não vou chamar de instalador completo sem a TOPBAR.' >&2; exit 2; }
DEST="$(dirname "$ROOT")/ARANDU-SUITE-completo-GNOME.tar.gz"
# Exclui arquivos de desenvolvimento/cache e conteúdo não necessário.
tar -czf "$DEST" --exclude='__pycache__' --exclude='*.pyc' -C "$(dirname "$ROOT")" "$(basename "$ROOT")"
sha256sum "$DEST"
echo "Pacote gerado: $DEST"
