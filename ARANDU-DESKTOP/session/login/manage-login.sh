#!/usr/bin/env bash
# Instala SOMENTE um seletor opcional de sessão, sem alterar a sessão padrão.
# Usar --check sem sudo; --install/--remove apenas com sudo explícito.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
START="$ROOT/session/login/start-login.sh"
TARGET="/usr/local/bin/arandu-login-session"
ENTRY="/usr/share/wayland-sessions/arandu-desktop-lab.desktop"
MARKER="X-ARANDU-Managed=true"
ACTION="${1:---check}"
case "$ACTION" in --check|--install|--remove) ;; *)
  echo "Uso: bash manage-login.sh --check | sudo bash manage-login.sh --install | sudo bash manage-login.sh --remove" >&2
  exit 2;; esac

if [[ "$ACTION" == "--check" ]]; then
  echo "=== ARANDU: PRÉ-VERIFICAÇÃO DE LOGIN ==="
  echo "Caminho: $ROOT"
  for exe in sway swaymsg python3 foot; do
    command -v "$exe" || true
  done
  python3 -c "import gi;gi.require_version('Gtk','4.0');from gi.repository import Gtk; print('GTK4 OK')" || true
  if [[ -e "$ENTRY" ]]; then grep -F "$MARKER" "$ENTRY" || true; fi
  echo "O teste real de Wayland requer encerrar a sessão atual e selecionar ARANDU no login."
  echo "Nada foi instalado ou modificado."
  exit 0
fi

if (( EUID != 0 )); then
  echo "ARANDU: use sudo EXPLICITAMENTE apenas para --install/--remove." >&2
  exit 2
fi

if [[ "$ACTION" == "--install" ]]; then
  [[ -r "$START" && -r "$ROOT/app.py" ]] || { echo "Fontes do ARANDU ausentes." >&2; exit 2; }
  for exe in sway swaymsg python3; do
    command -v "$exe" >/dev/null || { echo "Falta $exe. Instalação recusada." >&2; exit 2; }
  done
  python3 -c "import gi;gi.require_version('Gtk','4.0');from gi.repository import Gtk" >/dev/null || {
    echo "GTK4 indisponível; instalação recusada." >&2; exit 2; }
  if [[ -e "$ENTRY" ]] && ! grep -qF "$MARKER" "$ENTRY"; then
    echo "Existe outra sessão nesse caminho; não sobrescrever." >&2; exit 2
  fi
  if [[ -e "$TARGET" ]] && ! grep -qF "ARANDU_MANAGED_LOGIN_WRAPPER" "$TARGET"; then
    echo "Já existe outro launcher nesse caminho; não sobrescrever." >&2; exit 2
  fi
  install -d -m 0755 /usr/share/wayland-sessions /usr/local/bin
  TMP="$(mktemp)"
  trap 'rm -f -- "$TMP"' EXIT
  {
    echo '#!/usr/bin/env bash'
    echo '# ARANDU_MANAGED_LOGIN_WRAPPER'
    printf 'exec /bin/bash %q\n' "$START"
  } > "$TMP"
  install -m 0755 "$TMP" "$TARGET"
  cat > "$ENTRY" <<'DESKTOP'
[Desktop Entry]
Name=ARANDU Desktop (Experimental)
Comment=Semente e Rios do ARANDU sobre Sway; sessão opcional
Exec=/usr/local/bin/arandu-login-session
TryExec=/usr/local/bin/arandu-login-session
Type=Application
DesktopNames=sway
X-ARANDU-Managed=true
DESKTOP
  chmod 0644 "$ENTRY"
  echo "ARANDU registrado como opção experimental no login."
  echo "Sessão padrão do GNOME/Mint NÃO foi alterada."
elif [[ "$ACTION" == "--remove" ]]; then
  if [[ -e "$ENTRY" ]]; then
    grep -qF "$MARKER" "$ENTRY" || { echo "Sessão não gerenciada pelo ARANDU; recusa." >&2; exit 2; }
    rm -f -- "$ENTRY"
  fi
  if [[ -e "$TARGET" ]]; then
    grep -qF "ARANDU_MANAGED_LOGIN_WRAPPER" "$TARGET" || { echo "Launcher não gerenciado; recusa." >&2; exit 2; }
    rm -f -- "$TARGET"
  fi
  echo "Opção ARANDU retirada do login. GNOME/Mint permanece intacto."
fi
