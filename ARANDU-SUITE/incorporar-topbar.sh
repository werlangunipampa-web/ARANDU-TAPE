#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$HOME/.local/share/gnome-shell/extensions/arandu-topbar@local"
TARGET="$ROOT/TOPBAR/arandu-topbar@local"
[[ -f "$SOURCE/metadata.json" && -f "$SOURCE/extension.js" ]] || { echo 'TOPBAR histórica não encontrada nesta máquina.' >&2; exit 2; }
python3 - "$SOURCE/metadata.json" <<'PY'
import json,sys
p=json.load(open(sys.argv[1])); assert p.get('uuid')=='arandu-topbar@local', 'UUID inesperado'
print('Identificada:',p.get('name'), '| versão',p.get('version'))
PY
[[ ! -e "$TARGET" ]] || { echo 'TOPBAR já incorporada. Para evitar sobrescrita, operação cancelada.' >&2; exit 2; }
mkdir -p "$(dirname "$TARGET")"
cp -a "$SOURCE" "$TARGET"
find "$TARGET" -name '__pycache__' -type d -prune -exec rm -rf '{}' +
find "$TARGET" -type f \( -name '*.log' -o -name '*.pyc' \) -delete
python3 "$ROOT/verificar.py"
echo 'TOPBAR incluída neste diretório. Antes de distribuir, revisa os arquivos para remover dados pessoais ou segredos.'
echo 'Executa: bash empacotar.sh'
