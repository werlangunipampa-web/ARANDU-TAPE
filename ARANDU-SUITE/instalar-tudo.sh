#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOP="$HOME/.local/share/gnome-shell/extensions/arandu-topbar@local"
TOP_SRC="$ROOT/TOPBAR/arandu-topbar@local"
BACK="$HOME/.local/share/arandu-suite/backups"
TOP_MODERN="$ROOT/TOPBAR/modern"
ENABLE_EXPERIMENTAL=0
SHELL_MAJOR="$(gnome-shell --version 2>/dev/null | grep -oE '[0-9]+' | head -1 || true)"
case "${1:-}" in
  --preflight)
    command -v gnome-shell >/dev/null || { echo 'GNOME Shell não encontrado.' >&2; exit 2; }
    echo 'ARANDU SUITE 3.2.1 beta | Pré-verificação'
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
  --experimental-topbar)
    ENABLE_EXPERIMENTAL=1;;
  --instalar|"") ;;
  *) echo 'Uso: bash instalar-tudo.sh [--preflight|--verificar|--status|--instalar|--experimental-topbar]' >&2; exit 2;;
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
# Variante moderna apenas em GNOME 45 a 51, não em GNOME 40-44.
TOP_SUPPORTED=0
if [[ "$SHELL_MAJOR" == "46" ]]; then TOP_SUPPORTED=1; fi
if [[ "$SHELL_MAJOR" =~ ^[0-9]+$ ]] && (( SHELL_MAJOR >= 45 && SHELL_MAJOR <= 51 )); then TOP_SUPPORTED=1; fi
if [[ "$ENABLE_EXPERIMENTAL" == "1" && "$SHELL_MAJOR" != "46" && "$TOP_SUPPORTED" != "1" ]]; then
  echo 'ERRO: TOPBAR experimental restrita a GNOME 45-51.' >&2
  exit 2
fi
if [[ -f "$TOP/metadata.json" ]]; then
  echo 'TOPBAR histórica já instalada: preservada integralmente.'
elif [[ "$TOP_SUPPORTED" == "1" && -f "$TOP_SRC/metadata.json" ]]; then
  mkdir -p "$(dirname "$TOP")" "$BACK"
  STAGE="$(mktemp -d "$(dirname "$TOP")/.arandu-topbar-stage.XXXXXXXX")"
  trap 'rm -rf -- "$STAGE"' EXIT
  cp -a "$TOP_SRC/." "$STAGE/"
  chmod 755 "$STAGE"
  if [[ "$SHELL_MAJOR" != "46" ]]; then
    # Mantém íntegra a TOPBAR 6.6.1.2 no repositório.
    # Em GNOME diferente de 46 usa apenas uma cópia de instalação da variante moderna.
    if [[ ! -f "$TOP_MODERN/extension.js" || ! -f "$TOP_MODERN/metadata.json" ]]; then
      echo 'ERRO: variante moderna da TOPBAR não está no pacote.' >&2
      exit 2
    fi
    cp "$TOP_MODERN/extension.js" "$STAGE/extension.js"
    cp "$TOP_MODERN/metadata.json" "$STAGE/metadata.json"
  fi
  # Compila o esquema em todas as variantes, antes da instalação atômica.
  {
    if [[ ! -f "$STAGE/schemas/org.gnome.shell.extensions.arandu-topbar.gschema.xml" ]]; then
      echo 'ERRO: esquema da TOPBAR ausente do pacote.' >&2; exit 2
    fi
    command -v glib-compile-schemas >/dev/null || { echo 'ERRO: glib-compile-schemas não encontrado.' >&2; exit 2; }
    glib-compile-schemas "$STAGE/schemas"
  }
  # Instala somente quando não existe TOPBAR no destino.
  if [[ ! -e "$TOP" ]]; then mv -- "$STAGE" "$TOP"; trap - EXIT; fi
  echo 'TOPBAR incorporada instalada. É necessário iniciar nova sessão GNOME.'
else
  echo 'TOPBAR não instalada: esta versão GNOME não possui variante TOPBAR validada, ou o pacote está incompleto.'
fi
if command -v gnome-extensions >/dev/null; then
  gnome-extensions enable confluencia@arandulab 2>/dev/null || true
  # TOPBAR original oferece somente suporte ao GNOME 46; não ativá-la fora dessa versão.
  # Não habilita código histórico do GNOME 46 em outros GNOMEs.
  TOP_COMPATIBLE=0
  if [[ "$SHELL_MAJOR" == "46" ]]; then TOP_COMPATIBLE=1; fi
  if [[ "$ENABLE_EXPERIMENTAL" == "1" && "$SHELL_MAJOR" != "46" ]]; then
    if grep -q "Variante GNOME 45+" "$TOP/metadata.json" 2>/dev/null; then
      TOP_COMPATIBLE=1
    else
      echo "AVISO: TOPBAR já instalada não é a variante moderna; preservada e não habilitada."
    fi
  fi
  if [[ -f "$TOP/metadata.json" && "$TOP_COMPATIBLE" == "1" ]]; then
    gnome-extensions enable arandu-topbar@local 2>/dev/null || true
  else
    echo 'TOPBAR: GNOME fora do 46. Para testar a variante moderna (experimental),'
    echo 'use bash instalar-tudo.sh --experimental-topbar numa sessão de testes.'
  fi
fi
echo
echo 'ARANDU SUITE | Instalação unificada concluída.'
echo 'Componentes: Confluência (rios) + TOPBAR (identidade visual).'
echo 'Em GNOME X11, salve o trabalho e recarregue o Shell (Alt+F2, r, Enter).'
echo 'Em GNOME Wayland, encerre a sessão e entre novamente.'
echo 'Após reiniciar, confira: bash instalar-tudo.sh --status'
