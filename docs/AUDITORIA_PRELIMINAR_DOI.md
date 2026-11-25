# Auditoria preliminar de publicação científica — ARANDU TAPE

Data: 24/11/2026 (America/Sao_Paulo)
Snapshot examinado: `72ff2b2a863e1cb8a885abfe8c3b2a3444d1ebc3`
Estado: **BLOQUEADO PARA RELEASE CIENTÍFICA** até conclusão das verificações.

## Evidências verificadas

- Árvore Git completa enumerada: 133 arquivos, sem submódulos ou links simbólicos identificados. Ausência de arquivo LICENSE/COPYING/NOTICE identificado por nome. A inspeção de conteúdo foi amostral, não uma auditoria exaustiva de segurança.
- PR #2 incorporado à main. CI GTK4 e ARANDU SUITE do snapshot concluídos com sucesso: [Desktop](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45514815895), [Suite](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45514815898). CI não comprova execução gráfica real.
- O núcleo Rust experimental declara MIT em Cargo.toml, mas falta identificar titularidade e avisos aplicáveis.
- A interface ECA examinada usa exportação JSON escolhida pelo usuário e estruturas experimentais locais. Não foi encontrada importação direta do núcleo privado nesses arquivos. O aplicativo importa essas interfaces locais; isso não prova independência de todos os componentes ou ausência de exposição de pesquisa.
- Há código e documentação de contratos derivados de pesquisas que precisam de revisão específica de divulgação. Não ampliar o conteúdo público antes de aprovar essa revisão.
- SVGs da Semente, Rios e marca examinados não forneceram identificação de licença/autoria suficiente. A fotografia paisagem.jpg aparece no histórico inicial e é usada na renderização de mapview.py; sua origem não foi comprovada. Não remover o arquivo isoladamente sem adaptar e testar o mapa.
- TOPBAR possui histórico de desenvolvimento, mas isso não comprova integralmente a titularidade do código e dos grafismos.
- A publicação histórica em scripts/publicar-releases.sh usa uma tag beta fixa e target main. Não usar para depósito científico; uma release precisa apontar para um snapshot aprovado, não para a ponta móvel da branch.
- CITATION.cff existe. Autoria, eventuais colaboradores e titularidade institucional ainda devem ser confirmados. A integração Zenodo foi informada pelo responsável, não verificada por acesso autenticado.

## Matriz de decisão

| Grupo | Decisão inicial | Evidência ainda necessária |
| --- | --- | --- |
| Interface gráfica Confluência/GTK4 e instaladores | Candidato público | Procedência, licença, testes reais |
| Recursos gráficos SVG e fotografia | Pendente | Autor/origem, permissão ou substituição autorizada |
| TOPBAR | Pendente | Autoria, licenças e avisos |
| Rust público | Candidato público | Confirmar declaração MIT e titularidade |
| Adaptadores de IA/ECA e contratos locais | Revisão individual | Distinguir interface pública de informação experimental restrita |
| Núcleos de pesquisa privados | Excluir do depósito | Verificar o snapshot integral e não copiar código privado |
| Documentação e metadados | Candidato público | Revisar divulgação e autoria/licença |
| Credenciais, dados pessoais, memória viva | Proibido | Varredura integral de segurança e revisão humana |

## Portão de liberação

- [ ] Confirmar autores, colaboradores e titularidade institucional.
- [ ] Confirmar origem e direitos de redistribuição de cada recurso gráfico e código incorporado.
- [ ] Escolher licença da interface após revisão de compatibilidade e preservar avisos de terceiros.
- [ ] Revisar conteúdo integral e separar material experimental não autorizado.
- [ ] Validar funcionamento sem núcleos privados, inclusive sem credenciais de IA, e testar a interface no ambiente real.
- [ ] Reexecutar CI no commit candidato e registrar os resultados.
- [ ] Conferir os arquivos do snapshot e aprovar explicitamente a release.
- [ ] Publicar a release e confirmar o DOI efetivamente gerado pelo Zenodo.

Não há autorização de licença ou de depósito decorrente deste relatório. A origem registrada no Git não substitui comprovação de direitos.
