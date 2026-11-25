# Preparação reproduzível do código-fonte para Zenodo

## Identificação da versão

Proposta de identificação da primeira publicação científica: `v0.1.0-scientific`, a confirmar pelo responsável antes de criar uma tag. Trata-se de um identificador global experimental distinto dos números internos da Confluência, Desktop e TOPBAR. Não é uma versão publicada, nem substitui a identificação dos componentes. A versão escolhida deve ser registrada no CITATION.cff somente após decisão e revisão do escopo. Um novo commit altera o snapshot e exige repetir a verificação.

## Gerar pacote local de revisão

A partir de um clone completo e separado, com Git e Python 3 disponíveis, obter o SHA integral do candidato aprovado para revisão:

```bash
git rev-parse HEAD
python3 scripts/auditar-snapshot.py --ref SHA_INTEGRAL
python3 scripts/preparar-snapshot.py --commit SHA_INTEGRAL --output "$HOME/arandu-revisao-cientifica"
cd "$HOME/arandu-revisao-cientifica"
sha256sum -c SHA256SUMS
```

Substituir SHA_INTEGRAL pelo identificador de 40 caracteres; o diretório de saída deve ser novo e seu pai deve existir. O utilitário não aceita branch, HEAD ou SHA abreviado. Bloqueia indicadores da triagem, mas apenas lista referências que exigem revisão humana. O destino é local: nenhum upload, release, tag, token, instalação ou alteração de permissões dos arquivos-fonte.

| Arquivo | Conteúdo |
| --- | --- |
| manifest.json | SHA do commit e da árvore, caminho, modo Git, tamanho, blob Git e SHA-256 de cada arquivo; referências de revisão |
| source-review.tar | Arquivo TAR local dos blobs rastreados, em ordem determinística, sem metadados pessoais de proprietário ou horário de criação |
| SHA256SUMS | Hashes dos dois arquivos anteriores |

O TAR é não comprimido, com mtime/uid/gid fixos e prefixo derivado do commit. Não inclui .git, conteúdo não rastreado, modificações locais não commitadas, dependências instaladas, ZIPs locais ou arquivos gerados fora do commit. Não é byte a byte o ZIP automático do GitHub. A igualdade de conteúdo pode ser conferida contra os hashes do manifesto, respeitando eventuais metadados de empacotamento e caminhos de raiz diferentes.

## Reprodutibilidade e evidências

Os testes em `ARANDU-DESKTOP/tests/test_release_manifest.py` verificam a geração repetida, integridade de cada membro do TAR, checksums, recusa de sobrescrita, exclusão de mudanças locais e bloqueio de caminhos sensíveis em repositório sintético. Não validam execução gráfica nem concedem licença. O script é para revisão local do repositório público; não executar em repositórios privados.

Antes da release final: completar [ficha de liberação](LIBERACAO_SNAPSHOT_ZENODO.md), revisar todos os arquivos e referências de pesquisa, confirmar titularidade/licenças, executar CI e validação real, verificar a versão e SHA, validar CITATION.cff, comparar o arquivo efetivamente distribuído com o manifesto e aprovar explicitamente a release. A integração nativa GitHub–Zenodo pode arquivar o pacote fonte gerado pelo GitHub, não necessariamente este TAR local nem anexos. Não publicar o pacote de revisão automaticamente. Após o depósito, verificar DOI, arquivos, licença e versão efetiva.

Nenhuma tag, licença ou release é criada por este procedimento.
