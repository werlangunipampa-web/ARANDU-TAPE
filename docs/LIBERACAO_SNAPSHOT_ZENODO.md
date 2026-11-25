# Ficha de liberação do snapshot científico — Zenodo

Estado: **BLOQUEADO — rascunho para decisão de titularidade, licença e aceite.** Data de preparação: 24/11/2026. Não é autorização jurídica, registro Zenodo nem DOI.

## Escopo da primeira versão

Distribuir somente o ambiente gráfico público, documentação aprovada, testes e interfaces expressamente revisadas. Não distribuir os núcleos privados, a Foundation inteira, históricos pessoais, memória viva, credenciais ou arquivos de trabalho. O snapshot deverá funcionar sem os núcleos privados e sem credenciais de IA. A release arquivada é identificada por tag e SHA; não usar uma referência móvel de branch.

Evidência de preparação: head e82a20a5b1c2da5d60a1ce5b26b306e1f3b82668; 173 arquivos regulares na árvore; CI Desktop/Suite aprovada; 105 testes Python e triagem com zero bloqueantes e dez referências para revisão humana no merge da CI. O head definitivo será posterior a esse registro e exige repetir a validação.

## Titularidade: dados a confirmar pelo responsável

- Autores e contribuições efetivas, inclusive colaborativas e código de terceiros.
- Relação da criação com atribuições, projetos e recursos institucionais; financiamento, equipamentos, infraestrutura e acordos envolvidos.
- Manifestação da instituição ou titular competente quando aplicável, conforme [inventário e fontes legais](INVENTARIO_PROCEDENCIA_LICENCIAMENTO.md).
- Procedência dos ativos gráficos recuperados, desenvolvimento assistido por ferramentas e contribuições incorporadas.
- Aprovação expressa para redistribuição e licenciamento de cada grupo.

Não inferir titularidade pessoal ou institucional por profissão, nome no Git ou autoria da pesquisa. Os campos ficam pendentes até confirmação factual.

## Opções de licença para decisão (não concedidas)

| Grupo | Proposta | Condição |
| --- | --- | --- |
| Código gráfico próprio | GPL-3.0-only ou GPL-3.0-or-later, a decidir | Autoridade dos titulares e compatibilidade de todo código combinado |
| Documentação autoral própria | CC-BY-4.0, a decidir | Autorização específica; excluir informação reservada |
| Rust com declaração MIT | Preservar declaração existente | Confirmar titular e aviso de licença aplicável |
| SVGs e outros ativos | Determinar licença e alcance por grupo | Procedência e direitos confirmados; não licenciar materiais de terceiros por inferência |
| Dependências externas | Licenças originais | Inventariar versões e avisos quando efetivamente redistribuídos |

A licença copyleft pode proteger a liberdade das versões redistribuídas do código que ela abrange; não é mecanismo para manter confidencial um núcleo já distribuído. O isolamento técnico e a análise de integração são essenciais. Não combinar licenças presumindo compatibilidade. Uma vez aprovada a decisão, adicionar os textos e avisos pertinentes, delimitar escopos e validar metadados. Não inserir LICENSE geral ou SPDX nos arquivos antes da autorização.

O Zenodo exige informação de licença e sua interface de depósito tem CC BY 4.0 como padrão. Não aceitar esse padrão por descuido. O serviço admite múltiplas licenças quando software e documentação têm termos distintos. Se for necessário usar .zenodo.json, manter coerência com CITATION.cff e os avisos do repositório: na importação GitHub, .zenodo.json prevalece sobre CFF. Conferir o registro resultante, não presumir que a integração resolveu os direitos. Fontes: https://help.zenodo.org/docs/deposit/describe-records/licenses/ e https://help.zenodo.org/docs/github/describe-software/.

## Checklist de aceite

- [ ] Identificar SHA definitivo, tag inédita, versão e componentes efetivamente presentes.
- [ ] Confirmar titulares, colaboradores e eventual autorização institucional.
- [ ] Aprovar divulgação das referências de pesquisa; comprovar ausência de núcleos privados no snapshot.
- [ ] Confirmar procedência de código, imagens, estilos, grafismos e dependências.
- [ ] Aprovar licenças e incluir textos/avisos apropriados.
- [ ] Validar CITATION.cff e metadados, sem DOI fictício, autoria ou afiliação presumidas.
- [ ] Executar triagem de segurança e revisão humana do arquivo integral; conferir conteúdo gerado quando distribuído.
- [ ] Aprovar CI, teste gráfico real e recuperação; comprovar independência de IA/núcleos privados.
- [ ] Registrar desempenho e limitações sem reivindicar melhorias não medidas.
- [ ] Revisar arquivo fonte da release, aprovar publicação explicitamente e confirmar integração Zenodo.
- [ ] Publicar release e verificar DOI da versão, licença, autoria, arquivos e SHA de origem.

## Registro final (a preencher)

Versão/tag: pendente. SHA definitivo: pendente. Titulares/autorização: pendente. Licenças e escopos: pendentes. Evidências reais: pendentes. Aprovação: não concedida. DOI: não atribuído/confirmado.

Não executar scripts de publicação enquanto houver pendências. A aprovação da documentação e da CI não concede automaticamente autorização de depósito.

## Composição verificável

O [procedimento de reprodutibilidade](REPRODUTIBILIDADE_RELEASE.md) produz manifesto SHA-256 e TAR local de revisão a partir de SHA integral. Identificador global proposto: v0.1.0-scientific; ainda não aprovado nem criado. Arquivo de revisão não é release e não substitui a revisão do arquivo efetivamente arquivado pelo Zenodo.
