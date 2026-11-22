#!/usr/bin/env bash
# ARANDU 0.4 — apenas filho da sessão Wayland experimental Sway.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export GDK_BACKEND=wayland
export ARANDU_SESSION_LAB=1
exec python3 app.py
