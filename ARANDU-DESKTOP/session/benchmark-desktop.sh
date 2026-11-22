#!/usr/bin/env bash
# Benchmark comparativo reproduzível, sem instalar programas nem registrar serviços.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
case "${1:-}" in
  arandu|gnome|cinnamon|outro) PROFILE="$1";;
  *) echo "Uso: bash benchmark-desktop.sh arandu|gnome|cinnamon|outro [replicação 1..10]" >&2; exit 2;;
esac
REPEAT="${2:-1}"
[[ "$REPEAT" =~ ^([1-9]|10)$ ]] || { echo "Replicação deve ser 1..10" >&2; exit 2; }
CURRENT="${XDG_SESSION_DESKTOP:-unknown}"
case "$PROFILE" in
  arandu) [[ "$CURRENT" == "arandu" ]] || { echo "Sessão atual: $CURRENT; escolha ARANDU para baseline nativo." >&2; exit 2; };;
  gnome) [[ "$CURRENT" == "gnome" ]] || { echo "Sessão atual: $CURRENT; escolha GNOME." >&2; exit 2; };;
  cinnamon) [[ "$CURRENT" == "cinnamon" ]] || { echo "Sessão atual: $CURRENT; escolha Cinnamon." >&2; exit 2; };;
  outro) :;;
esac
# Relatórios criados no diretório do usuário; nunca publica dados automaticamente.
TARGET="$HOME/ARANDU-BENCHMARKS"
mkdir -p -- "$TARGET"
chmod 700 -- "$TARGET"
STAMP="$(date +%Y%m%d-%H%M%S)"
FILE="$TARGET/${PROFILE}-${STAMP}-r${REPEAT}.json"
echo "=== ARANDU COMPARADOR DE AMBIENTES ==="
echo "Sessão: $CURRENT | perfil: $PROFILE | repetição: $REPEAT"
echo "Faça ensaios com os mesmos aplicativos, resolução, alimentação e tempo após login."
echo "Amostras: 10 | intervalo: 1 s | não realiza carga forçada."
python3 "$ROOT/benchmark.py" --measure --count 10 --interval 1 --save "$FILE"
echo "Resultado: $FILE"
echo "Para comparar dois arquivos: python3 $ROOT/benchmark.py --compare ARQUIVO_A.json ARQUIVO_B.json"
