#!/usr/bin/env bash
# User-scoped preview installer; never escalates privileges.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME/.local/share/arandu/updates"
BIN="$HOME/.local/bin"
APPS="$HOME/.local/share/applications"
AUTO="$HOME/.config/autostart"
if [[ "${EUID}" -eq 0 ]]; then echo "Não execute como root." >&2; exit 1; fi
for f in client/arandu_update_check.py client/arandu_update_app.py client/arandu_update_startup.py; do
  [[ -f "$ROOT/$f" && ! -L "$ROOT/$f" ]] || { echo "Arquivo ausente ou link: $f" >&2; exit 1; }
done
for p in "$TARGET" "$TARGET/client" "$BIN" "$APPS" "$AUTO"; do
  if [[ -L "$p" ]]; then echo "Destino é link simbólico: $p" >&2; exit 1; fi
  mkdir -p "$p"
done
install -m 0644 "$ROOT/client/arandu_update_check.py" "$TARGET/client/"
install -m 0644 "$ROOT/client/arandu_update_app.py" "$TARGET/client/"
install -m 0644 "$ROOT/client/arandu_update_startup.py" "$TARGET/client/"
cat > "$BIN/arandu-update" <<'EOF'
#!/bin/sh
exec /usr/bin/python3 "$HOME/.local/share/arandu/updates/client/arandu_update_app.py" "$@"
EOF
chmod 0755 "$BIN/arandu-update"
cat > "$APPS/arandu-update.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=ARANDU Atualizações
Comment=Consultar versões finais do ARANDU TAPE sem instalar
Exec=/usr/bin/python3 $HOME/.local/share/arandu/updates/client/arandu_update_app.py
Icon=software-update-available
Terminal=false
Categories=Settings;System;
StartupNotify=true
EOF
cat > "$AUTO/arandu-update-check.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=ARANDU Update — verificação ao iniciar
Exec=/usr/bin/python3 $HOME/.local/share/arandu/updates/client/arandu_update_startup.py
Terminal=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF
echo "Central instalada no usuário. Procure 'ARANDU Atualizações' no catálogo."
echo "Consulta somente leitura será realizada ao iniciar a sessão gráfica."
echo "Avisos na Semente e instalações permanecem desabilitados nesta prévia."
