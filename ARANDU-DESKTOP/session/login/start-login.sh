#!/usr/bin/env bash
# Ponto de entrada apenas para sessão escolhida no login, sem modificar o Mint.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="$ROOT/session/login/sway-login.config.in"
LAUNCH="$ROOT/session/launch-arandu.sh"
CAPTURE="$ROOT/session/capture-screen.sh"
OPY="$ROOT/opy.py"

if [[ "${EUID}" -eq 0 ]]; then
  echo "ARANDU: não execute uma sessão gráfica como root." >&2
  exit 2
fi
for tool in sway python3 swaymsg; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "ARANDU: dependência ausente: $tool. Retorne ao GNOME." >&2
    exit 2
  fi
done
if ! python3 -c "import gi;gi.require_version('Gtk','4.0');from gi.repository import Gtk" >/dev/null 2>&1; then
  echo "ARANDU: GTK4/Python indisponível. Retorne ao GNOME." >&2
  exit 2
fi
if [[ ! -r "$SOURCE" || ! -r "$LAUNCH" ]]; then
  echo "ARANDU: arquivos da sessão não encontrados. Retorne ao GNOME." >&2
  exit 2
fi
if [[ -z "${XDG_RUNTIME_DIR:-}" || ! -d "$XDG_RUNTIME_DIR" ]]; then
  echo "ARANDU: XDG_RUNTIME_DIR não está disponível nesta sessão." >&2
  exit 2
fi

# Ao contrário do Sway aninhado, deixar o compositor descobrir backend/seat reais.
unset WLR_BACKENDS WLR_X11_OUTPUTS WLR_LIBINPUT_NO_DEVICES ARANDU_SESSION_CONFIG
export XDG_CURRENT_DESKTOP=sway
export XDG_SESSION_DESKTOP=arandu
export XDG_SESSION_TYPE=wayland
export ARANDU_SESSION_LAB=1
export GDK_BACKEND=wayland

TMP="$(mktemp -d -t arandu-login.XXXXXXXX)"
chmod 700 "$TMP"
trap 'rm -rf -- "$TMP"' EXIT
CONFIG="$TMP/sway.config"
python3 - "$SOURCE" "$CONFIG" "$LAUNCH" "$CAPTURE" "$OPY" <<'PY'
import pathlib, shlex, sys
source, dest, launch, capture, opy = map(pathlib.Path, sys.argv[1:])
template = source.read_text(encoding="utf-8")
if (template.count("__ARANDU_LAUNCHER__") != 1 or
        template.count("__ARANDU_CAPTURE__") != 1 or
        template.count("__ARANDU_CAPTURE_SAVE__") != 1 or
        template.count("__ARANDU_OPY__") != 1):
    raise SystemExit("ARANDU: marcador de comando inválido")
capture_cmd = "/bin/bash " + shlex.quote(str(capture))
template = template.replace("__ARANDU_LAUNCHER__", "/bin/bash " + shlex.quote(str(launch)))
template = template.replace("__ARANDU_CAPTURE_SAVE__", capture_cmd + " --save")
template = template.replace("__ARANDU_CAPTURE__", capture_cmd + " --clipboard")
template = template.replace("__ARANDU_OPY__", "/usr/bin/python3 " + shlex.quote(str(opy)))
dest.write_text(template, encoding="utf-8")
dest.chmod(0o600)
PY

echo "ARANDU Login: sessão experimental Sway. Ctrl+Alt+Shift+Q encerra."
# NUNCA executar sudo, alterar login manager ou GNOME aqui.
status=0
sway -c "$CONFIG" || status=$?
exit "$status"
