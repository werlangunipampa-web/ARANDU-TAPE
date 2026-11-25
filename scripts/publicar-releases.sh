#!/usr/bin/env bash
set -Eeuo pipefail
# A antiga automação conjunta arquivaria um snapshot não aprovado no Zenodo.
# Manter o histórico deste arquivo no Git; não criar releases automaticamente.
echo "Publicação histórica desativada: use docs/PUBLICACAO_CIENTIFICA_ZENODO.md." >&2
echo "Nenhuma release ARANDU-TAPE ou ARANDU-WEB será criada por este script." >&2
exit 2
