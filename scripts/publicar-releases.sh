#!/usr/bin/env bash
set -Eeuo pipefail
OWNER="werlangunipampa-web"
DIR="${1:-$HOME/Downloads/ARANDU-PUBLICACAO}"
TAPE="$DIR/ARANDU-TAPE-2.8.3-GITHUB-PRONTO.zip"
WEB="$DIR/ARANDU-WEB-0.1.0-GITHUB-PRONTO.zip"
for cmd in gh unzip; do
  command -v "$cmd" >/dev/null || { echo "Instale gh e unzip: sudo apt install gh unzip" >&2; exit 1; }
done
gh auth status >/dev/null 2>&1 || { echo "Execute gh auth login" >&2; exit 1; }
for file in "$TAPE" "$WEB"; do
  test -s "$file" || { echo "Arquivo não encontrado: $file" >&2; exit 1; }
  unzip -tq "$file" >/dev/null
done
publish() {
  local repo="$1" tag="$2" title="$3" pkg="$4" notes="$5"
  if gh release view "$tag" -R "$OWNER/$repo" >/dev/null 2>&1; then
    echo "Release existente: $OWNER/$repo $tag; não será sobrescrita."
    return
  fi
  gh release create "$tag" "$pkg" -R "$OWNER/$repo" --target main --title "$title" --notes "$notes" --prerelease
  echo "Publicado: https://github.com/$OWNER/$repo/releases/tag/$tag"
}
publish ARANDU-TAPE v2.8.3-beta "ARANDU TAPE 2.8.3 — beta GNOME" "$TAPE" "Pacote beta. Extraia; cd ARANDU-SUITE; bash instalar-tudo.sh --preflight; bash instalar-tudo.sh --verificar; bash instalar-tudo.sh. Leia INSTALAR.md. Compatibilidade multi-GNOME em avaliação."
publish ARANDU-WEB v0.1.0-beta "ARANDU WEB 0.1.0 — teste Firefox" "$WEB" "Extensão Firefox experimental sem assinatura. Carregue extension/manifest.json em about:debugging#/runtime/this-firefox para uso temporário. Veja INSTALAR.md."
