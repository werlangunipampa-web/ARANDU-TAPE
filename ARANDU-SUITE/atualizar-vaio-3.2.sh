#!/usr/bin/env bash
# ARANDU SUITE 3.2 — atualização integrada GNOME 46/X11.
# Atualiza Confluência e somente os arquivos modificados da TOPBAR.
# Preserva TOPBAR existente, extensões históricas e preferências do usuário.
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-shell/extensions"
TOP="$EXT/arandu-topbar@local"
TOP_SRC="$ROOT/TOPBAR/arandu-topbar@local"
BACK="$HOME/ARANDU-BACKUP-INTEGRADO-$(date +%Y%m%d-%H%M%S)"
echo "ARANDU — atualização integrada (GNOME 46/X11)"
if [[ "$(gnome-shell --version 2>/dev/null)" != "GNOME Shell 46.0" ]]; then
    echo "ERRO: procedimento validado somente para GNOME Shell 46.0." >&2
    exit 2
fi
if [[ "${XDG_SESSION_TYPE:-}" != "x11" ]]; then
    echo "ERRO: é necessário testar esta atualização em sessão X11." >&2
    exit 2
fi
if ! command -v node >/dev/null || ! command -v glib-compile-schemas >/dev/null; then
    echo "ERRO: node e glib-compile-schemas precisam estar disponíveis." >&2
    exit 2
fi
echo "=== Verificação antes de modificar arquivos ==="
bash -n "$ROOT/instalar-tudo.sh"
node --check "$ROOT/TOPBAR/arandu-topbar@local/extension.js"
node --check "$ROOT/TOPBAR/arandu-topbar@local/prefs.js"
node "$ROOT/Confluencia/tests/shell-contract.cjs"
glib-compile-schemas --strict --dry-run "$ROOT/Confluencia/shell"
bash "$ROOT/instalar-tudo.sh" --verificar
echo "=== Backup das extensões atuais ==="
mkdir -p "$BACK"
for id in confluencia@arandulab arandu-topbar@local; do
    if [[ -d "$EXT/$id" ]]; then
        cp -a "$EXT/$id" "$BACK/"
        echo "Salvo: $id"
    fi
done
echo "=== Instalando/atualizando Confluência ==="
bash "$ROOT/instalar-tudo.sh"
if [[ ! -f "$TOP/metadata.json" ]]; then
    echo "ERRO: TOPBAR não instalada; não há arquivos a atualizar." >&2
    exit 1
fi
echo "=== Atualizando código e preferências da TOPBAR ==="
# O instalador unificado não sobrescreve uma TOPBAR existente.
# Copiar somente estes dois arquivos mantém identidade visual, CSS, assets e esquema.
install -m 0644 "$TOP_SRC/extension.js" "$TOP/extension.js"
install -m 0644 "$TOP_SRC/prefs.js" "$TOP/prefs.js"
node --check "$TOP/extension.js"
node --check "$TOP/prefs.js"
echo "=== Concluído ==="
echo "Backup: $BACK"
echo "Extensões históricas preservadas."
echo "Salve os trabalhos, encerre a sessão GNOME e entre novamente."
echo "Depois confira: gnome-extensions info confluencia@arandulab"
echo "               gnome-extensions info arandu-topbar@local"
