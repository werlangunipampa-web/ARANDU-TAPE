#!/usr/bin/env bash
set -euo pipefail
# Launcher relocável: não contém o nome ou HOME do computador de origem.
HUB="${XDG_DATA_HOME:-$HOME/.local/share}/arandu-lab/arandu-center/arandu-opy-hub.py"
if [[ -f "$HUB" ]]; then
  if ! pgrep -f '[a]randu-opy-hub.py' >/dev/null 2>&1; then
    nohup env GTK_THEME=Adwaita:dark python3 "$HUB" >/dev/null 2>&1 </dev/null &
  fi
elif command -v arandu-tape-confluencia >/dev/null 2>&1; then
  exec arandu-tape-confluencia
else
  echo 'ARANDU CENTER indisponível; instale o CENTER ou a Confluência.' >&2
  exit 1
fi
