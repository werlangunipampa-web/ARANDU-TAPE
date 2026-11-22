#!/usr/bin/env bash
# ARANDU Desktop 0.4 — compositor Sway ANINHADO dentro do desktop atual.
# Não instala pacotes, não edita ~/.config, não registra sessão no login.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CFG="$ROOT/session/sway.config.in"
LAUNCH="$ROOT/session/launch-arandu.sh"
if [[ -z "${DISPLAY:-}" ]]; then
    echo "ERRO: inicie a partir da sessão gráfica X11 do Linux Mint." >&2
    exit 2
fi
if ! command -v sway >/dev/null 2>&1; then
    echo "Sway não instalado. Experimento opcional: sudo apt install sway" >&2
    exit 2
fi
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 não encontrado." >&2
    exit 2
fi
if ! python3 -c "import gi; gi.require_version('Gtk','4.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "GTK4 ausente: verifique python3-gi e gir1.2-gtk-4.0." >&2
    exit 2
fi
python3 -m unittest discover -s "$ROOT/tests" -v
TMP="$(mktemp -d -t arandu-nested.XXXXXXXX)"
chmod 700 "$TMP"
cleanup(){ rm -rf -- "$TMP"; }
trap cleanup EXIT
export ARANDU_SESSION_CONFIG="$TMP/config"
export ARANDU_SESSION_LAUNCH="$LAUNCH"
python3 - "$CFG" "$ARANDU_SESSION_CONFIG" "$LAUNCH" <<'PY'
import pathlib, shlex, sys
source, destination, executable = map(pathlib.Path, sys.argv[1:])
template = source.read_text(encoding='utf-8')
assert template.count('__ARANDU_LAUNCHER__') == 1
# 'exec' de Sway invoca uma linha de comando; protegemos o caminho com shlex.
command = '/bin/bash ' + shlex.quote(str(executable))
destination.write_text(template.replace('__ARANDU_LAUNCHER__', command), encoding='utf-8')
destination.chmod(0o600)
PY
echo "=== ARANDU 0.4 · COMPOSITOR ANINHADO (NÃO INSTALAÇÃO) ==="
echo "O Sway abre como uma janela do GNOME e executa o ARANDU GTK4 dentro dela."
echo "Para sair: Ctrl+Alt+Shift+Q (dentro do Sway), ou feche a janela aninhada."
echo "GNOME, TOPBAR, Confluência, dados ECA e login NÃO são alterados."
# Force X11 nested; do not touch the system compositor or DRM devices.
# No shell-wide environment modifications survive termination of this script.
export WLR_BACKENDS=x11
export WLR_LIBINPUT_NO_DEVICES=1
export WLR_X11_OUTPUTS=1
exec_sway_status=0
sway -c "$ARANDU_SESSION_CONFIG" || exec_sway_status=$?
exit "$exec_sway_status"
