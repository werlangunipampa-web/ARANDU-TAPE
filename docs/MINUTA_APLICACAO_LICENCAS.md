# Licenças por componente — minuta de aplicação

Estrutura GPL versão 3 / CC BY 4.0 / identidade reservada aprovada pelo responsável. **Minuta, sem concessão de licença neste arquivo.** Não é um LICENSE geral, nem substitui os textos legais oficiais.

| Escopo candidato | Identificador pretendido | Condição antes de aplicar |
| --- | --- | --- |
| Código gráfico próprio, adaptadores, testes e ferramentas próprios | GPL-3.0-only (recomendação em revisão) | Confirmar variante GPL e procedência; incluir texto oficial e avisos nos arquivos |
| Documentação científica autoral revisada | CC-BY-4.0 | Confirmar textos abrangidos, atribuição e divulgação; não abranger citações ou materiais de terceiros automaticamente |
| SVGs funcionais, controles, cursores e recursos necessários | Licença compatível com código GPL; GPL-3.0-only candidata | Confirmar direitos e licença específica, inclusive arquivos gerados |
| Marca e identificação oficial | Direitos reservados; autorização específica de distribuição/uso ainda a definir | Delimitar ativos e permitir substituição da marca sem restringir direitos GPL |
| Grafismos decorativos | Pendente por ativo | Confirmar procedência, contexto cultural e permissão |
| Rust rastreado | Declaração MIT já existente em Cargo.toml | Confirmar titular e incluir aviso correspondente |
| Código ou ativos de terceiros | Licenças originais | Identificar e preservar avisos, verificar compatibilidade |
| Material de pesquisa reservado | Fora do depósito | Manter isolamento técnico e revisar histórico separadamente |

## Modelo de avisos (somente após confirmação)

Para os arquivos próprios efetivamente aprovados, inserir aviso de titularidade e identificador SPDX apropriado à sintaxe do arquivo. Não alterar shebang, codificação, schema, estrutura de SVG ou JSON para incluir comentários inválidos. Para arquivos sem comentários válidos, usar registro explícito de caminho e aviso adjacente quando apropriado. Não inserir aviso de titularidade universal sem verificar os titulares e os anos.

- Código: identificador SPDX escolhido após decisão entre GPL-3.0-only e GPL-3.0-or-later. Incluir cópia do texto oficial GPLv3 e avisos de copyright.
- Documentação: CC-BY-4.0, atribuição ao titular confirmado, link para licença e identificação de alterações quando aplicável.
- Marca: autorização específica e escopo separado, sem alegar registro de marca ou limitar direitos sobre o código GPL.

A opção GPL-3.0-only restringe a escolha de versão da licença à GPLv3; GPL-3.0-or-later permite a opção por versão posterior da FSF. A escolha não muda a necessidade de separar núcleos privados. Não colocar ambas como alternativas sem decisão.

Fontes: https://www.gnu.org/licenses/gpl-howto.html ; https://www.gnu.org/licenses/gpl-3.0.html ; https://creativecommons.org/licenses/by/4.0/legalcode .

## Condição de liberação

Aprovar escopo por caminho, titulares, licenças originais de terceiros, compatibilidade e aviso de marca. Só então aplicar os textos oficiais e os identificadores ao candidato, atualizar os metadados e validar o snapshot inteiro. O manifesto deve referir-se ao commit final, não a esta minuta. Nenhuma licença ou versão é inferida a partir de uma simples referência documental.
