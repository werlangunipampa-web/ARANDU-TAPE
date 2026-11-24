# Publicação científica e preservação do ARANDU TAPE

## Escopo
Este procedimento complementa a política A0. GitHub é a fonte de desenvolvimento; Zenodo arquiva releases publicadas após revisão. Commits e tags isolados não são depósitos científicos. A conexão foi informada como habilitada pelo responsável; confirmar no painel Zenodo.

## Portão de publicação (obrigatório)
- Confirmar autoria, contribuições, ORCID (se informado) e titularidade com a política institucional aplicável.
- Revisar direitos e licenças de todo o snapshot, inclusive ARANDU-SUITE/TOPBAR, SVGs e imagens, dependências, código Python/JavaScript/Rust, e elementos culturais. Registrar procedência, condições de redistribuição e avisos. Ausência de LICENSE não equivale a licença livre. Não atribuir licença global até a revisão.
- Excluir chaves, dados pessoais, estado vivo da Semente, capturas privadas e arquivos de pesquisa restritos; não incluir repositórios privados.
- Validar CITATION.cff (cffconvert --validate) e confirmar os metadados de autoria.
- Executar CI e testes locais no GNOME 46/X11 e nos demais ambientes efetivamente declarados; documentar limitações e reversão.
- Confirmar quais componentes e versões pertencem ao snapshot (ARANDU Desktop GTK4 e Confluência têm versionamentos próprios); registrar commit SHA e notas de versão. Não reutilizar o nome de uma versão antiga para código novo.
- Revisar o arquivo-fonte que o GitHub disponibiliza para a release; não presumir que anexos binários sejam arquivados pelo Zenodo.
- Aprovar explicitamente a release antes de torná-la pública. Não executar scripts históricos de publicação automática de beta enquanto essa revisão estiver pendente.

## Arquivamento
1. Integrar o PR aprovado à main e publicar uma release do commit validado em https://github.com/werlangunipampa-web/ARANDU-TAPE/releases/new.
2. Conferir o processamento em https://zenodo.org/account/settings/github/ e abrir o registro resultante.
3. Verificar DOI da versão e, quando fornecido, DOI de todas as versões, arquivos, autoria, licença e correspondência com o commit. Não declarar DOI inexistente ou não verificado.
4. Atualizar README e metadados da interface com os identificadores confirmados, preservando o vínculo exato entre cada DOI e o snapshot arquivado. Não mostrar o DOI da versão anterior como se fosse da compilação nova. Um commit posterior à release pode apresentar o DOI geral, mas não deve alegar ser o snapshot arquivado.
5. Repetir apenas para releases aprovadas. Manter a integração nativa, sem tokens de Zenodo no código, sem publicar cada commit e sem alterar depósitos científicos anteriores.

Referências: https://help.zenodo.org/docs/github/enable-repository/ ; https://help.zenodo.org/docs/github/describe-software/citation-file/ ; https://help.zenodo.org/docs/github/archive-software/github-upload/

## Estado inicial
Nenhuma release foi encontrada no repositório durante a preparação. DOI ainda não confirmado. Autoria, titularidade, licenças e validação gráfica permanecem pendentes. A seção Sobre exibe essa condição; os links são abertos somente sob ação do usuário.
