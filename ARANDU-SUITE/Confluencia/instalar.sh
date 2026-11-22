#!/bin/sh
set -eu
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
for py in "${ARANDU_PYTHON:-}" /usr/bin/python3 python3; do
    [ -n "$py" ] || continue
    if "$py" -c 'import sys, cairo, gi; gi.require_version("Gtk","3.0"); from gi.repository import Gtk,Gio,GdkPixbuf; assert sys.version_info >= (3,8)' 2>/dev/null; then
        exec "$py" "$base/instalador.py" "$@"
    fi
done
for py in /usr/bin/python3 python3; do
    if "$py" -c 'import sys; assert sys.version_info >= (3,8)' 2>/dev/null; then exec "$py" "$base/instalador.py" "$@"; fi
done
echo "Instala Python 3.8 ou superior e executa este instalador novamente." >&2
exit 1
