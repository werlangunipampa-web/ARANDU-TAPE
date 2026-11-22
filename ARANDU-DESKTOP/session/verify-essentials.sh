#!/usr/bin/env bash
# Diagnóstico não destrutivo de funções essenciais ARANDU.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== ARANDU · VERIFICAÇÃO ESSENCIAL ==="
echo "Sessão declarada: ${XDG_SESSION_DESKTOP:-desconhecida}"
echo "Protocolo declarado: ${XDG_SESSION_TYPE:-desconhecido}"
for tool in python3 swaymsg firefox nemo foot grim wl-copy wl-paste; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'OK       %s\n' "$tool"
  else
    printf 'PENDENTE %s\n' "$tool"
  fi
done
python3 -m compileall -q "$ROOT"
python3 -m unittest discover -s "$ROOT/tests" -q
bash -n "$ROOT/session/capture-screen.sh"
bash -n "$ROOT/session/login/start-login.sh"
bash -n "$ROOT/session/start-nested.sh"
if [[ -n "${SWAYSOCK:-}" ]] && command -v swaymsg >/dev/null 2>&1; then
  if swaymsg -r -t get_version >/dev/null 2>&1; then
    echo "Sway IPC: OK"
  else
    echo "Sway IPC: INDISPONÍVEL"
  fi
else
  echo "Sway IPC: fora da sessão ARANDU (esperado no GNOME)."
fi
echo "Nota: testes contratuais não substituem teste real de Print, Alt+Tab ou fechamento."
echo "GNOME e configurações de login não foram alterados."
