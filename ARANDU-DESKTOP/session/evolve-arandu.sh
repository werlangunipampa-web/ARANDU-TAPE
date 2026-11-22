#!/usr/bin/env bash
# Evolução do ARANDU a partir do próprio desktop, nunca uma atualização automática.
# Não altera GNOME, compositor ativo, gerenciador de login ou ECA.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
ACTION="${1:---check}"
case "$ACTION" in --check|--update) ;; *) echo "Uso: evolve-arandu.sh --check|--update" >&2; exit 2;; esac
cd "$ROOT"
command -v git >/dev/null 2>&1 || { echo "Git não encontrado." >&2; exit 2; }
[[ -d .git ]] || { echo "Diretório não é clone Git." >&2; exit 2; }
echo "=== ARANDU · CENTRO DE EVOLUÇÃO ==="
echo "Branch: $(git branch --show-current)"
echo "Commit atual: $(git rev-parse --short HEAD)"
echo "Mudanças locais:"
git status --short
if [[ "$ACTION" == "--check" ]]; then
  echo "Nenhuma alteração executada. Consulte atualizações quando desejar."
  exit 0
fi
if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "Recusado: atualizações apenas no branch main." >&2; exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Recusado: há mudanças locais ou arquivos não rastreados. Preservamos tudo." >&2
  exit 2
fi
printf '\nAtualizar código do ARANDU do origin/main?\n'
printf 'Isso não reinicia aplicações nem instala pacotes do Linux.\n'
printf 'Digite ATUALIZAR para prosseguir: '
read -r CONFIRM
if [[ "$CONFIRM" != "ATUALIZAR" ]]; then
  echo "Cancelado."
  exit 0
fi
PREVIOUS="$(git rev-parse HEAD)"
mkdir -p "$HOME/.local/share/arandu"
umask 077
printf '%s\n' "$PREVIOUS" > "$HOME/.local/share/arandu/ultimo-commit-anterior.txt"
git pull --ff-only origin main
echo "=== TESTES APÓS ATUALIZAÇÃO ==="
python3 -m compileall -q ARANDU-DESKTOP
python3 -m unittest discover -s ARANDU-DESKTOP/tests -q
bash -n ARANDU-DESKTOP/session/login/start-login.sh
bash -n ARANDU-DESKTOP/session/start-nested.sh
bash -n ARANDU-DESKTOP/session/terminal-arandu.sh
echo "Código atualizado e testes concluídos. Interface aberta precisa ser reiniciada manualmente."
echo "Commit anterior registrado em ~/.local/share/arandu/ultimo-commit-anterior.txt"
