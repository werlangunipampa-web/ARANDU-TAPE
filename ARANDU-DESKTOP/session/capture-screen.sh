#!/usr/bin/env bash
# Captura de tela ARANDU: por padrão somente clipboard Wayland, sem arquivo.
set -Eeuo pipefail
MODE="${1:---clipboard}"
if ! command -v grim >/dev/null 2>&1; then
  echo "ARANDU: grim não está instalado." >&2
  exit 2
fi
case "$MODE" in
  --clipboard)
    if ! command -v wl-copy >/dev/null 2>&1; then
      echo "ARANDU: wl-copy ausente. Instale wl-clipboard para Ctrl+V." >&2
      exit 2
    fi
    # PNG é entregue por pipe ao clipboard; não grava em disco.
    grim - | wl-copy --type image/png
    echo "ARANDU: captura na área de transferência. Cole com Ctrl+V."
    ;;
  --save)
    DEST="${XDG_PICTURES_DIR:-}"
    if [[ -z "$DEST" ]] && command -v xdg-user-dir >/dev/null 2>&1; then
      DEST="$(xdg-user-dir PICTURES)"
    fi
    if [[ -z "$DEST" || "$DEST" == "$HOME" ]]; then
      DEST="$HOME/Imagens"
    fi
    mkdir -p -- "$DEST"
    FILE="$DEST/ARANDU-$(date +%Y%m%d-%H%M%S)-$$.png"
    grim "$FILE"
    printf 'ARANDU: imagem salva em %s\n' "$FILE"
    ;;
  *)
    echo "Uso: capture-screen.sh [--clipboard|--save]" >&2
    exit 2
    ;;
esac
