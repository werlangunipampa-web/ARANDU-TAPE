# Histórico de mudanças

Identificadores abaixo são marcos de componentes no código e documentação, não releases GitHub/Zenodo confirmadas. Não há DOI confirmado. Datas e evidências de marcos antigos devem ser consultadas nas notas originais.

## Em desenvolvimento — candidato à primeira release científica

- Metadados CITATION.cff e apresentação Sobre o ARANDU.
- Política de separação da interface pública e pesquisa privada.
- Auditoria preliminar, inventário de procedência e triagem de snapshot.
- Substituição da fotografia sem origem comprovada por paisagem procedural no candidato; validação gráfica pendente.
- Desativação do script legado de publicação conjunta sem revisão.
- Manuais, matriz de versões, índice, Design Core e fundamentação pública.
- Documentação de privacidade, segurança, contribuição, acessibilidade e apresentação em inglês.
- Padrão do temporizador dos Rios alterado para desligado; escolha explícita e preferências salvas preservadas. Testes de contrato acrescentados; validação real pendente.
- Painel da Semente com informações sob demanda e acesso aos avisos/calendário e controles nativos. Ocultação própria da barra suspensa até equivalência dos indicadores; removida sondagem de 300 ms. Testes reais pendentes.
- Espelhamento passivo de sinais nativos na Semente, sem captura de dispositivos nem armazenamento de notificações. Ausência de sinal não comprova inatividade. Validação real e visibilidade independente ainda pendentes.
- Etiqueta passiva de sinais em camada própria quando suportada, com posicionamento por menor sobreposição à janela ativa e fallback; sem alteração da posição persistida da Semente. Validação gráfica pendente.
- Representação compacta e reversível da Semente em cantos de menor sobreposição, sem alterar a âncora manual dos Rios. Ação explícita reabre navegação; validação gráfica pendente.
- Contrato puro de gestos Alça Viva e Flechas, com testes de intenção; reserva superior nativa em Desktop GTK4, mapa GTK3 e Opy. Não constitui integração de gestos com GNOME ou Sway; validação visual e sincronização com a implementação local pendentes.
- Laboratório GNOME 46 opt-in: oito flechas contextuais de redimensionamento, prévia e Flecha Mestre azul; CI aprovada em c8e16cd. Validação real pendente.
- Evolução local documentada separadamente: Nove Flechas, Contorno Vivo, Movimento Suave, Presença Viva e Nitidez Viva; não incluída automaticamente na release. Ver [registro](docs/EVOLUCAO_ESPACOS_VIVOS.md).
- Pendências: revisão de divulgação, direitos e licença, validação real e aprovação do snapshot.

## Confluência / Suíte GNOME

- 3.2.3-beta: estado identificado no gerador da extensão; integração multimonitor em desenvolvimento.
- 3.1: painel de acessibilidade na Semente, prévia.
- 3.0: variante TOPBAR multiversão experimental e diagnóstico assistivo.
- 2.9: varredura por acionador com confirmação.
- 2.8.3 e anteriores: navegação por Rios, repouso visual, integração de extensões e instalador.

Consultar [notas da suíte](ARANDU-SUITE/README.md), [roteiro](ARANDU-SUITE/docs/ROADMAP.md) e [versões](docs/ESTADO_E_VERSOES.md).

## ARANDU Desktop GTK4

- 0.7.7: adaptadores de interface, Tupã e adaptação experimental.
- 0.7.5: Terminal ARANDU baseado em Foot e fluxo de atualização consentido.
- 0.7.2–0.7.4: indicadores essenciais e atualizações, observação de desempenho.
- 0.7.0: Opy.
- 0.5–0.6: laboratório Sway, janelas e avaliação de sessão.
- 0.2–0.3: visualização GTK4 e navegação por aplicativos.

Consultar [histórico Desktop](ARANDU-DESKTOP/README.md). Cada marco conserva suas próprias limitações; existência no código não comprova validação gráfica.

## Regra de novas entradas

Registrar versão do componente, data real, SHA, mudanças, correções, incompatibilidades, testes executados, ambiente, recuperação e referência à release/DOI somente quando confirmados. Não reutilizar identificadores para snapshots diferentes.
