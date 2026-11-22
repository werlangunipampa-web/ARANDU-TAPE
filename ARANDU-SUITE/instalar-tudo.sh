#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOP="$HOME/.local/share/gnome-shell/extensions/arandu-topbar@local"
TOP_SRC="$ROOT/TOPBAR/arandu-topbar@local"
BACK="$HOME/.local/share/arandu-suite/backups"
case "${1:-}" in
  --preflight)
    command -v gnome-shell >/dev/null || { echo 'GNOME Shell não encontrado.' >&2; exit 2; }
    echo 'ARANDU SUITE 2.8.3 | Pré-verificação'
    gnome-shell --version
    echo "Sessão: ${XDG_SESSION_TYPE:-desconhecida}"
    echo 'Confluência:'; bash "$ROOT/Confluencia/instalar.sh" --preflight
    if [[ -f "$TOP_SRC/metadata.json" ]]; then echo 'TOPBAR incorporada: SIM'; else echo 'TOPBAR incorporada: NÃO; instalador parcial'; fi
    if [[ -f "$TOP/metadata.json" ]]; then echo 'TOPBAR local existente: SIM (será preservada)'; else echo 'TOPBAR local existente: NÃO'; fi
    exit 0;;
  --verificar)
    python3 "$ROOT/verificar.py"; exit $?;;
  --instalar|"") ;;
  *) echo 'Uso: bash instalar-tudo.sh [--preflight|--verificar|--instalar]' >&2; exit 2;;
esac
command -v gnome-shell >/dev/null || { echo 'GNOME Shell não encontrado. Instalação interrompida.' >&2; exit 2; }
python3 "$ROOT/verificar.py"
# Primeiro atualiza a Confluência (tem backup/transação própria).
bash "$ROOT/Confluencia/instalar.sh"
# TOPBAR histórica: não sobrescrever nem desativar sem autorização específica.
if [[ -f "$TOP/metadata.json" ]]; then
  echo 'TOPBAR histórica já instalada: preservada integralmente.'
elif [[ -f "$TOP_SRC/metadata.json" ]]; then
  mkdir -p "$(dirname "$TOP")" "$BACK"
  STAGE="$(mktemp -d "$(dirname "$TOP")/.arandu-topbar-stage.XXXXXXXX")"
  trap 'rm -rf -- "$STAGE"' EXIT
  cp -a "$TOP_SRC/." "$STAGE/"
  chmod 755 "$STAGE"
  # Instala somente quando não existe TOPBAR no destino.
  if [[ ! -e "$TOP" ]]; then mv -- "$STAGE" "$TOP"; trap - EXIT; fi
  echo 'TOPBAR incorporada instalada. É necessário iniciar nova sessão GNOME.'
else
  echo 'AVISO: TOPBAR não incluída. A Confluência foi instalada; para instalador completo, executa incorporar-topbar.sh na máquina original.'
fi
if command -v gnome-extensions >/dev/null; then
  gnome-extensions enable confluencia@arandulab 2>/dev/null || true
  # TOPBAR original oferece somente suporte ao GNOME 46; não ativá-la fora dessa versão.
  SHELL_MAJOR="$(gnome-shell --version | grep -oE '[0-9]+' | head -1 || true)"
  if [[ "$SHELL_MAJOR" == "46" && -f "$TOP/metadata.json" ]]; then
    gnome-extensions enable arandu-topbar@local 2>/dev/null || true
  else
    echo 'TOPBAR: ativação automática omitida fora do GNOME 46.'
  fi
fi
echo 'Instalação concluída. Verifica os dois estados com gnome-extensions info. Reinicia a sessão se o GNOME ainda não reconhecer alguma extensão.'
