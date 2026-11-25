#!/usr/bin/env bash
# User-scoped preview installer; no sudo and no privileged changes.
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
for p in "$TARGET" "$BIN" "$APPS" "$AUTO"; do
  if [[ -L "$p" ]]; then echo "Destino é link simbólico: $p" >&2; exit 1; fi
  mkdir -p "$p"
done
mkdir -p "$TARGET/client"
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
# Startup is opt-in; keep autostart disabled in preview until local-version comparison exists.
echo "Prévia instalada no usuário. Abra pelo catálogo: ARANDU Atualizações."
echo "Nenhuma execução automática, aviso de update ou instalação foi habilitada."
