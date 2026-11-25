# Ficha de depósito científico — rascunho, não publicar

## Metadados propostos

- Título: ARANDU TAPE: Adaptive Desktop Environment
- Tipo: Software
- Autor registrado em CITATION.cff: Rafhael Brum Werlang; confirmar contribuições e titularidade antes do depósito.
- Repositório: https://github.com/werlangunipampa-web/ARANDU-TAPE
- Idiomas da documentação: português e inglês.
- Versão, data de publicação e SHA: preencher somente com o snapshot final aprovado.
- ORCID, afiliação, financiamento e colaboradores: confirmar; não inferir.
- Licença: pendente de autorização e verificação de compatibilidade. GPL-3.0 permanece proposta para a interface, não licença concedida. Conferir o campo obrigatório no Zenodo, inclusive qualquer valor padrão.
- DOI: ainda não atribuído.

## Descrição em português (proposta)

ARANDU TAPE é um ambiente gráfico experimental para Linux que investiga alternativas de organização espacial e interação humano-computador inspiradas em princípios da aprendizagem significativa. A interface explora a Semente Adaptativa, a navegação por Rios, a organização de espaços e a acessibilidade por ações explícitas. O repositório contém componentes para GNOME e um protótipo GTK4, além de documentação de arquitetura, privacidade e validação. Os Espaços Vivos incluem um laboratório opcional de operações de janela com controles contextuais em oito direções e uma Flecha Mestre de maximização. Os testes automatizados verificam contratos e construção; o comportamento e o desempenho em ambientes gráficos reais exigem avaliação complementar. Os núcleos experimentais privados não fazem parte do escopo pretendido do depósito.

## English description (proposed)

ARANDU TAPE is an experimental Linux desktop environment exploring spatial organization and human–computer interaction inspired by meaningful learning principles. Its interface explores an Adaptive Seed, River-based navigation, spatial organization and accessibility through explicit user actions. The repository contains GNOME components, a GTK4 prototype, and documentation covering architecture, privacy and validation. Living Spaces includes an optional window-operation laboratory with contextual eight-direction resizing controls and a Master Arrow for maximization. Automated tests verify contracts and builds; real-world graphical behavior and performance require further evaluation. Private experimental research kernels are outside the intended scope of the deposit.

Keywords: Linux; GNOME; human–computer interaction; accessibility; meaningful learning; adaptive interfaces; spatial interaction.

## Controle de publicação

Usar CITATION.cff como fonte de metadados, evitando duplicação com .zenodo.json enquanto não houver necessidade de campos específicos. Segundo o [Zenodo](https://help.zenodo.org/docs/github/describe-software/citation-file/), se ambos existirem, .zenodo.json prevalece integralmente. Validar CFF antes da publicação. Não inserir uma licença por padrão ou inventar versão/DOI.

| Verificação | Situação |
| --- | --- |
| Snapshot público de evidência | c8e16cd4f8a510e1625eb35c434253a591a8ec4b; ambas CIs aprovadas |
| Patches locais posteriores | [Registro separado](EVOLUCAO_ESPACOS_VIVOS.md); não pertencem automaticamente ao snapshot |
| PR de revisão | [#3](https://github.com/werlangunipampa-web/ARANDU-TAPE/pull/3), rascunho |
| Direitos, licença e divulgação | Pendentes |
| Teste real e independência dos núcleos | Pendentes de comprovação integral |
| Release GitHub | Nenhuma encontrada em 24/11/2026 |
| Conexão autenticada Zenodo | Informada pelo responsável; não verificada |
| DOI | Não confirmado |

Quando o snapshot final for aprovado: validar CFF, scanner e CI, revisar todo o arquivo de release, registrar SHA exato, completar licença e titularidade, confirmar a integração Zenodo, publicar a release e verificar o registro efetivo. Não reutilizar a tag de outro snapshot. Não criar release apenas para testar a integração.

## Referências operacionais

- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://help.zenodo.org/docs/deposit/describe-records/licenses/
- https://help.zenodo.org/docs/github/enable-repository/

Este rascunho não é uma licença, um depósito, um DOI ou uma aprovação de publicação. Revisar a descrição conforme o conteúdo efetivamente distribuído.
