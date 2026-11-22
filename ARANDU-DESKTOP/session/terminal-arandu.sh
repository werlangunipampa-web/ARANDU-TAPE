#!/usr/bin/env bash
# Terminal com aparência ARANDU, sem shell artificial nem execução privilegiada.
set -Eeuo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v foot >/dev/null 2>&1; then
  echo "Terminal ARANDU: Foot ausente." >&2
  exit 2
fi
exec foot -c "$HERE/foot-arandu.ini" "$@"
