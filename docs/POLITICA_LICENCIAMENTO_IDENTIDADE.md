# Política de licenciamento e identidade — decisão de projeto

## Estrutura aprovada pelo responsável

O responsável declarou o caráter pessoal e independente do ARANDU TAPE e aprovou a seguinte estrutura de licenciamento durante a preparação da primeira publicação científica:

| Escopo | Decisão de projeto |
| --- | --- |
| Código próprio do ambiente gráfico público | GNU GPL versão 3 |
| Documentação científica autoral autorizada | Creative Commons Atribuição 4.0 Internacional (CC BY 4.0) |
| Núcleos de aprendizagem significativa e algoritmos experimentais privados | Não distribuir; manter em repositórios privados separados |
| Identidade visual e marca ARANDU | Direitos reservados, com permissões específicas de uso |
| Componentes de terceiros | Preservar licenças e avisos originais; não relicenciar por inferência |
| Rust público com declaração MIT preexistente | Preservar a declaração; confirmar procedência e aviso aplicável |

A aprovação acima é uma decisão de estrutura. Este documento não é texto de concessão de licença, não licencia retroativamente o repositório inteiro e não autoriza a publicação de uma release. A opção GPL-3.0-only versus GPL-3.0-or-later ainda precisa ser definida expressamente; a autorização e compatibilidade de cada componente também precisam ser confirmadas.

## Distinção entre marca e interface funcional

A marca, os elementos de identificação oficial e eventuais materiais gráficos promocionais não devem ser confundidos com os recursos necessários à execução do software. A reserva de direitos sobre a marca não deve impedir o exercício das permissões concedidas pela GPL para o código que ela abrange. Não reivindicar registro de marca sem comprovação.

Proposta técnica para aprovação: licenciar os recursos gráficos funcionais próprios (ícones de operações, controles, cursores e elementos indispensáveis à interface) sob termos compatíveis com a distribuição e modificação do ambiente gráfico; preservar separadamente a identidade oficial, com possibilidade de substituição por identificadores neutros em versões modificadas. Esta delimitação é proposta, não permissão já concedida. Inventariar os ativos individualmente antes da distribuição; confirmar direitos sobre grafismos e contribuições de terceiros.

## Implementação futura

1. Resolver a titularidade e procedência dos materiais.
2. Definir a variante GPL e a licença dos recursos gráficos funcionais.
3. Delimitar caminhos abrangidos pelas licenças e separar o conteúdo experimental reservado.
4. Incluir textos oficiais de licença, avisos e atribuições, sem remover avisos de terceiros.
5. Validar a consistência entre o repositório, o CITATION.cff e os metadados Zenodo. Não aplicar uma licença geral incompatível com a composição real.
6. Submeter a composição e o SHA definitivo à aprovação de release.

Referências normativas: https://www.gnu.org/licenses/gpl-3.0.html ; https://creativecommons.org/licenses/by/4.0/ .

A separação pública/privada exige isolamento técnico: reserva de direitos não torna confidencial material já disponível em repositório público. A remoção de um arquivo da árvore atual não remove automaticamente o histórico. Não copiar, abrir ou publicar repositórios privados para atender à release.
