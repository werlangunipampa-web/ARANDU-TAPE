#!/usr/bin/env bash
# ARANDU Desktop 0.1: apenas inicia aplicativo GTK4; não substitui login.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
command -v python3 >/dev/null || { echo "Python 3 não disponível"; exit 1; }
echo "ARANDU Desktop 0.1 — testes do núcleo isolado"
python3 -m unittest discover -s "$ROOT/tests" -v
echo "Iniciando laboratório gráfico (não modifica GNOME/Cinnamon)"
cd "$ROOT"
exec python3 app.py
