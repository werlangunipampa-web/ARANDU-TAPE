# ARANDU — Guia público de acessibilidade

A navegação busca permitir diferentes formas de interação com o mesmo conjunto de intenções. É um protótipo, não tecnologia assistiva clinicamente validada. Os recursos abaixo referem-se à Confluência GNOME; não presumir equivalência no Desktop GTK4/Sway.

## Navegação por teclado

| Atalho padrão | Ação |
| --- | --- |
| Super+Alt+1 | Rio Memória |
| Super+Alt+2 | Rio Abertos |
| Super+Alt+3 | Rio Frequentes |
| Super+Alt+seta esquerda/direita | Anterior/próximo medalhão |
| Super+Alt+Enter | Ativar |
| Super+Alt+0 | Cancelar seleção |
| Super+Shift+T | Abrir mapa |
| Super+Alt+B | Recuperar painel, quando compatível |
| Super+Alt+Espaço | Iniciar varredura / confirmar seleção |

Atalhos podem conflitar com o desktop. Consulte as configurações e preserve meio de cancelamento.

## Preferências

Abra o painel de acessibilidade pelo botão direito na Semente ou menu da Confluência. Há escala de medalhões 85/100/120%, alto contraste, velocidade de varredura 2/3,5/5 s e opção de acionador Super+Alt+Espaço ou Super+Alt+S. Inicie lentamente, observe foco, confirme apenas quando desejar abrir e cancele com Super+Alt+0. O temporizador da varredura não abre aplicativos; o recolhimento por inatividade não deve interferir durante a varredura. Para manter os rios abertos, escolha a opção de nunca recolher por tempo.

## Modalidades e limites

- A ponte D-Bus aceita comandos de vocabulário limitado, não código arbitrário. Aceitação do comando não comprova efeito.
- O mapa GTK3 tem reconhecimento experimental de frase curta com Vosk, iniciado por pedido, se modelo e gravador estiverem instalados. Não equivale a voz contínua, controle integral do desktop nem reconhecimento validado. Esc pode encerrar a escuta no mapa.
- Rastreamento de cabeça, mãos e combinação de sensores continuam propostas; não obrigar câmera ou microfone.
- Opy, Alça Viva, flechas contextuais e indicadores unificados devem manter alternativas por teclado, cancelamento, foco e ausência de sobreposição. Não declarar essas diretrizes entregues em todos os ambientes.

## Protocolo de aceitação

Testar com teclado sem mouse; iniciar/parar varredura; verificar acionador adaptado; navegar e recuperar foco; verificar tamanho, contraste, resolução e múltiplos monitores; evitar perda de trabalho ao cancelar ou fechar; medir erros, esforço, tempo e ativações involuntárias. Com participação de pessoas, assegurar consentimento, acessibilidade do protocolo e revisão ética quando aplicável. Não generalizar resultados de um único equipamento.

Guias detalhados: [painel](../ARANDU-SUITE/docs/PAINEL-ACESSIBILIDADE.md), [varredura](../ARANDU-SUITE/docs/VARREDURA-2.9.md), [arquitetura](../ARANDU-SUITE/docs/ARQUITETURA-E-ACESSIBILIDADE.md), [Design Core](DESIGN_CORE.md), [privacidade](PRIVACIDADE.md).
