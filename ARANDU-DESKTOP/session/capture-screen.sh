#!/usr/bin/env bash
# Captura explícita de tela no ARANDU/Sway. Sem sudo, sem telemetria.
set -Eeuo pipefail
if ! command -v grim >/dev/null 2>&1; then
  echo "ARANDU: ferramenta grim não encontrada." >&2
  exit 2
fi
DEST="${XDG_PICTURES_DIR:-}"
if [[ -z "$DEST" ]]; then
  if command -v xdg-user-dir >/dev/null 2>&1; then
    DEST="$(xdg-user-dir PICTURES)"
  fi
fi
if [[ -z "$DEST" || "$DEST" == "$HOME" ]]; then
  DEST="$HOME/Imagens"
fi
mkdir -p -- "$DEST"
FILE="$DEST/ARANDU-$(date +%Y%m%d-%H%M%S)-$$.png"
grim "$FILE"
printf 'ARANDU: captura salva em %s\n' "$FILE"
if command -v notify-send >/dev/null 2>&1; then
  notify-send "ARANDU · Captura de tela" "Imagem salva em $(basename -- "$FILE")" || true
fi
