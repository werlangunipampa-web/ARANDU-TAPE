# Delimitação de ativos e pesquisa para o primeiro depósito

Base de inventário: commit ae48530d3895fb5401d25cf205a73e5867f681b1, 179 arquivos, 22 SVGs rastreados. Classificação funcional proposta para revisão; não é concessão de licença nem prova de titularidade.

## Recursos gráficos

| Local | Ativos | Tratamento proposto |
| --- | --- | --- |
| Confluencia/app/assets | diamond.svg, document.svg, files.svg, flower.svg, frequent.svg, memory.svg, open.svg, woven.svg | Ícones funcionais; licença compatível com software após revisão |
| Confluencia/app/assets | rios.svg, semente.svg | Elementos de navegação essenciais; distinguir representação funcional de uso como marca oficial |
| Confluencia/app/assets | papel-e1.svg | Fundo decorativo substituível; confirmar procedência e termos |
| Confluencia/app/assets | marca.svg | Identidade oficial candidata à reserva de direitos |
| Confluencia/design-reference | alca-viva.svg, flecha-amarela.svg, flecha-azul.svg, ponteiro-folha.svg | Referências locais recuperadas; confirmar origem e autorizar uso funcional |
| TOPBAR/arandu-topbar@local/assets | arandu-mark.svg | Identidade oficial candidata à reserva de direitos |
| TOPBAR/arandu-topbar@local/assets | band-arandu.svg, band-kaaguy.svg, band-tape.svg, band-trama.svg, band-yvy.svg | Grafismos decorativos; revisão cultural, procedência e termos específicos |
| Confluencia/spaces-lab/build.py | Nove SVGs gerados (oito arcos direcionais e Mestre) | Controles funcionais; não são arquivos rastreados independentes |

Total: 22 SVGs rastreados + nove gerados. O build também copia três SVGs de referência; não contá-los como novas obras. Não conceder licença de marca ou de recursos gráficos apenas com base no nome do arquivo. Confirmar o uso real e garantir que eventual substituição da identidade não quebre a execução nem restrinja direitos sobre código GPL.

## Separação do material de pesquisa

A inspeção do código público identificou módulos e documentos derivados de pesquisa. Não há conclusão de que contenham o núcleo privado completo. Para o primeiro depósito, manter em retenção conservadora os seis caminhos definidos em scripts/verificar-escopo-release.py. O contrato de ações atual é usado por app.py; sua retirada direta quebraria a aplicação. A solução proposta é substituir a dependência por um contrato público de autorização humana, independente da ontologia experimental, preservando negação por padrão e testes de segurança. Retirar a interface experimental de ECA do candidato ou substituí-la por indicação neutra de integração opcional indisponível. Manter as demais funções essenciais e revisar testes e documentação. Não acessar, copiar ou alterar repositórios privados para executar essa separação.

O contrato de intercâmbio JSON existente e o avaliador estrutural experimental não são por si sós uma ECA completa; ainda assim, ficam retidos até decisão de divulgação. A documentação constitutiva não deve ser incorporada automaticamente ao depósito. O Rust rastreado permanece sujeito a revisão própria. A retenção não altera o que já foi publicado no histórico Git, nem garante que outros arquivos não contenham informação reservada.

## Barreira de escopo

```bash
python3 scripts/verificar-escopo-release.py --commit "$(git rev-parse HEAD)"
```

A barreira usa a árvore do commit, não a pasta de trabalho. Atualmente é esperado que recuse o candidato enquanto os seis caminhos estiverem presentes. Este é um controle adicional à triagem de credenciais, não uma substituição da revisão humana. O empacotador local de revisão continua disponível para auditoria, sem autorização de distribuição. Não usar a ausência de alerta automático para liberar a release.

Consultar [política aprovada de licenciamento](POLITICA_LICENCIAMENTO_IDENTIDADE.md) e [ficha de liberação](LIBERACAO_SNAPSHOT_ZENODO.md).

## Separação implementada no candidato

O Desktop GTK4 passou a importar `action_contract.py`, contrato público independente, com lista de operações permitidas, intenção humana, confirmação e procedência quando aplicável. A interface de consulta experimental de exportações foi retirada do candidato. Os seis caminhos retidos foram excluídos da árvore desta branch, não do histórico Git; nenhum repositório privado foi aberto, modificado ou publicado. A barreira permanece ativa para impedir reintrodução acidental. Testes de autorização e independência substituem os testes experimentais na árvore pública; validação real ainda pendente. A separação por caminhos não garante ausência de todo conteúdo reservado: revisar a árvore integral antes do depósito.
