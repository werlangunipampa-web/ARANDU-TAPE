# Publicação científica e preservação do ARANDU TAPE

## Escopo
Este procedimento complementa a política A0. GitHub é a fonte de desenvolvimento; Zenodo arquiva releases publicadas após revisão. Commits e tags isolados não são depósitos científicos. A conexão foi informada como habilitada pelo responsável; confirmar no painel Zenodo.

## Decisão de escopo público e privado (24/11/2026)

O responsável pelo projeto confirmou a preferência por disponibilizar publicamente o ambiente gráfico ARANDU e preservar os núcleos experimentais privados. Esta separação é uma regra para releases, depósitos Zenodo e evolução arquitetural.

| Escopo | Política |
| --- | --- |
| Ambiente gráfico, Semente visual, Rios, Opy, Alça Viva, acessibilidade, instalação e documentação | Candidatos à publicação após revisão de procedência, segurança, licenciamento e testes. |
| ECA, núcleos cognitivos experimentais, algoritmos internos de pesquisa e demais laboratórios privados | Permanecem privados; sem sincronização, inclusão em releases ou depósitos Zenodo automáticos. |
| Interfaces de integração, contratos públicos e exemplos sintéticos | Publicáveis somente após revisão explícita; devem funcionar sem expor implementação privada ou dados reais. |
| Dados pessoais, estado vivo da Semente, tokens, credenciais e backups | Nunca integrar ao arquivo público. |

A separação é também técnica: o ambiente gráfico distribuído deve poder funcionar sem os núcleos privados. Integrações opcionais devem ser desacopladas por interfaces documentadas, com consentimento e alternativas locais. Não importar, copiar nem tornar públicos repositórios privados para atender uma release. Avaliar a compatibilidade de licenças e o eventual caráter de obra combinada antes de distribuir qualquer integração.

O Zenodo arquiva o snapshot do repositório público associado à release; a revisão deve abranger a árvore completa desse snapshot, não apenas os instaladores. Se houver conteúdo experimental impróprio para publicação no repositório atual, bloquear o depósito até separar esse conteúdo. A GPL-3.0 para a interface gráfica segue como proposta, não como licença concedida; manter avisos e licenças existentes, incluindo a declaração MIT do núcleo Rust experimental, após confirmar sua procedência. A escolha final da licença, a titularidade institucional e os direitos de terceiros permanecem pendentes.

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

## Triagem automatizada e publicação controlada

Executar no clone completo, sem credenciais adicionais:

```bash
python3 scripts/auditar-snapshot.py --ref HEAD
```

O scanner lê a árvore Git do commit, não arquivos não rastreados nem repositórios privados. Detecta padrões comuns de credenciais, caminhos restritos, binários, links simbólicos/submódulos, ponteiros LFS e arquivos grandes. Referências de pesquisa são listadas para revisão humana; não são automaticamente consideradas vazamentos. A triagem também roda em teste de contrato da CI Desktop. Não é garantia de ausência de segredos (especialmente no histórico), nem autorização jurídica ou de publicação. Nenhum valor de credencial é impresso.

O script legado `scripts/publicar-releases.sh` foi desativado integralmente porque publicava os dois projetos em sequência sem um portão de revisão. Não altera o repositório ARANDU-WEB; a publicação desse projeto passa a depender de procedimento próprio. Não existe automação com autoridade para publicar uma release ainda não aprovada.

Antes da publicação, preencher e aprovar o checklist de titularidade, direitos, revisão de pesquisa e teste real associado ao SHA candidato. Selecionar a tag/commit validado, nunca a ponta móvel de main. Só então publicar a release pelo GitHub. A integração Zenodo é posterior e automática se habilitada; nenhum token deve ser armazenado no código.
