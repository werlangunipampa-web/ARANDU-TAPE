#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOP="$HOME/.local/share/gnome-shell/extensions/arandu-topbar@local"
TOP_SRC="$ROOT/TOPBAR/arandu-topbar@local"
BACK="$HOME/.local/share/arandu-suite/backups"
SHELL_MAJOR="$(gnome-shell --version 2>/dev/null | grep -oE '[0-9]+' | head -1 || true)"
case "${1:-}" in
  --preflight)
    command -v gnome-shell >/dev/null || { echo 'GNOME Shell não encontrado.' >&2; exit 2; }
    echo 'ARANDU SUITE 2.9.0 | Pré-verificação'
    gnome-shell --version
    echo "Sessão: ${XDG_SESSION_TYPE:-desconhecida}"
    echo 'Confluência:'; bash "$ROOT/Confluencia/instalar.sh" --preflight
    if [[ -f "$TOP_SRC/metadata.json" ]]; then echo 'TOPBAR incorporada: SIM'; else echo 'TOPBAR incorporada: NÃO; instalador parcial'; fi
    if [[ -f "$TOP/metadata.json" ]]; then echo 'TOPBAR local existente: SIM (será preservada)'; else echo 'TOPBAR local existente: NÃO'; fi
    if [[ "$SHELL_MAJOR" != "46" ]]; then echo "AVISO: TOPBAR histórica é específica do GNOME 46; não será habilitada automaticamente no GNOME ${SHELL_MAJOR:-desconhecido}."; fi
    exit 0;;
  --verificar)
    python3 "$ROOT/verificar.py"; exit $?;;
  --status)
    echo 'ARANDU SUITE | Estado das extensões'
    for extension in confluencia@arandulab arandu-topbar@local; do
      gnome-extensions info "$extension" 2>&1 || true
    done
    exit 0;;
  --instalar|"") ;;
  *) echo 'Uso: bash instalar-tudo.sh [--preflight|--verificar|--status|--instalar]' >&2; exit 2;;
esac
command -v gnome-shell >/dev/null || { echo 'GNOME Shell não encontrado. Instalação interrompida.' >&2; exit 2; }
python3 "$ROOT/verificar.py"
# Evita anunciar uma instalação unificada incompleta no GNOME 46.
if [[ "$SHELL_MAJOR" == "46" && ! -f "$TOP/metadata.json" && ! -f "$TOP_SRC/metadata.json" ]]; then
  echo 'ERRO: TOPBAR ausente do sistema e do pacote. Instalação cancelada antes de alterar a Confluência.' >&2
  exit 2
fi
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
  if [[ "$SHELL_MAJOR" == "46" ]]; then
    if [[ ! -f "$STAGE/schemas/org.gnome.shell.extensions.arandu-topbar.gschema.xml" ]]; then
      echo 'ERRO: esquema da TOPBAR ausente do pacote.' >&2; exit 2
    fi
    command -v glib-compile-schemas >/dev/null || { echo 'ERRO: glib-compile-schemas não encontrado.' >&2; exit 2; }
    glib-compile-schemas "$STAGE/schemas"
  fi
  # Instala somente quando não existe TOPBAR no destino.
  if [[ ! -e "$TOP" ]]; then mv -- "$STAGE" "$TOP"; trap - EXIT; fi
  echo 'TOPBAR incorporada instalada. É necessário iniciar nova sessão GNOME.'
else
  echo 'AVISO: TOPBAR não incluída. A Confluência foi instalada; para instalador completo, executa incorporar-topbar.sh na máquina original.'
fi
if command -v gnome-extensions >/dev/null; then
  gnome-extensions enable confluencia@arandulab 2>/dev/null || true
  # TOPBAR original oferece somente suporte ao GNOME 46; não ativá-la fora dessa versão.
  if [[ "$SHELL_MAJOR" == "46" && -f "$TOP/metadata.json" ]]; then
    gnome-extensions enable arandu-topbar@local 2>/dev/null || true
  else
    echo 'TOPBAR: ativação automática omitida fora do GNOME 46.'
  fi
fi
echo
echo 'ARANDU SUITE | Instalação unificada concluída.'
echo 'Componentes: Confluência (rios) + TOPBAR (identidade visual).'
echo 'Em GNOME X11, salve o trabalho e recarregue o Shell (Alt+F2, r, Enter).'
echo 'Em GNOME Wayland, encerre a sessão e entre novamente.'
echo 'Após reiniciar, confira: bash instalar-tudo.sh --status'
