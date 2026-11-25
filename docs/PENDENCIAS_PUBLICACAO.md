# Decisões pendentes para publicação científica

Registro de preparação, 24/11/2026. Nenhuma autorização é presumida.

## Evidência técnica

O head 22cb0e75b5131514a81d7715c22b1ac77d0d06c8 passou nas duas suítes de CI: [Desktop](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45536765024) e [Suite](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45536765033). O log do merge de CI d8262026f62b03e8acc4df2530b935ae083b4132 registra 109 testes Python, quatro testes de reprodutibilidade aprovados (incluídos nos 109), 177 entradas, zero indicadores bloqueantes e dez referências de pesquisa. A validação CFF 1.2.0 foi acrescentada à CI em commit posterior; consultar a execução do head definitivo. Nenhum desses resultados comprova teste gráfico ou autorização de direitos.

## Revisão de divulgação

Os seguintes caminhos foram sinalizados por busca textual. A classificação abaixo é proposta de encaminhamento, não autorização de divulgação nem revisão integral do conteúdo.

| Caminho | Encaminhamento |
| --- | --- |
| ARANDU-DESKTOP/README.md | Revisar descrições e exemplos; retirar detalhes internos desnecessários |
| ARANDU-DESKTOP/app.py | Delimitar interfaces públicas e testar uso sem serviços privados |
| ARANDU-DESKTOP/docs/CONTRATO-ONTOLOGICO-TRANSVERSAL.md | Revisão autoral específica: distinguir princípios públicos de material reservado |
| ARANDU-DESKTOP/eca_experiments.py | Verificar se código e exemplos são exclusivamente públicos e sintéticos |
| ARANDU-DESKTOP/ontology_contract.py | Revisar regras públicas e dependências; não suprimir sem teste |
| ARANDU-DESKTOP/tests/test_login_contract.py | Revisar fixtures e referências internas |
| ARANDU-DESKTOP/tests/test_ontology_contract.py | Revisar fixtures e regras reproduzidas |
| ARANDU-DESKTOP/tests/test_session_contract.py | Revisar fixtures e referências internas |
| docs/INVENTARIO_PROCEDENCIA_LICENCIAMENTO.md | Referência documental; manter apenas informação autorizada |
| scripts/auditar-snapshot.py | Padrões de triagem; não são evidência de inclusão do núcleo privado |

A presença de palavras-chave não significa vazamento. A ausência de alertas não significa que todo o conteúdo pode ser divulgado. Revisar também caminhos não sinalizados. Não copiar arquivos de pesquisa privados para resolver a revisão.

## Decisões do responsável

1. Confirmar autoria, colaboradores, titularidade e eventual necessidade de manifestação institucional. Descrever os fatos sobre vínculo e recursos sem inferência.
2. Aprovar a divulgação dos componentes e contratos públicos, ou indicar quais devem ser separados.
3. Escolher a licença após revisão de direitos e compatibilidade: GPL-3.0-only ou GPL-3.0-or-later é proposta para código gráfico; CC BY 4.0 é proposta para documentação. Definir ativos gráficos e preservar licenças de terceiros.
4. Aprovar ou substituir o identificador global proposto v0.1.0-scientific.
5. Executar os ensaios reais do candidato e confirmar independência de núcleos/credenciais privadas.
6. Aprovar explicitamente o SHA final e conferir o registro efetivamente depositado.

Campos de autorização e identificação permanecem na [ficha de liberação](LIBERACAO_SNAPSHOT_ZENODO.md). Nenhuma publicação é realizada por este registro.
