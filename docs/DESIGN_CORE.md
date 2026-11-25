# ARANDU — Design Core | DC-001

**Revisão 0.1 — 24/11/2026.** Especificação pública proposta para revisão; não certifica que todos os controles existam no snapshot. Complementa a arquitetura, sem publicar a ontologia constitutiva ou a implementação dos núcleos privados.

## 1. Finalidade

Uma interface limpa, rápida, reconhecível, acessível e coerente. A complexidade aparece quando é necessária; a pessoa controla as ações. O ambiente deve permanecer utilizável sem IA, sensores ou serviços de pesquisa.

## 2. Identidade visual e tokens

A paleta abaixo registra valores já encontrados no GTK4, no mapa GTK3, no Shell e no terminal. Não implica que exista um sistema único de tokens implementado; sua unificação é uma tarefa posterior. Não substituir variantes sensoriais por mera uniformidade cromática.

| Papel | Cor de referência | Origem |
| --- | --- | --- |
| Fundo floresta | #14221D | GTK4 / Foot |
| Superfície | #1A2E26 | GTK4 / Foot |
| Texto claro | #E9EEE7 | GTK4 |
| Texto secundário | #ADC0B3 | GTK4 |
| Dourado de contorno | #B9AD84 | GTK4 |
| Foco selecionado | #FFE1A0 | Shell |
| Papel / texto | #F8F5ED / #282E29 | Mapa GTK3 |
| Alto contraste | #101311 / #FFFDFA | Mapa GTK3 |
| Destaque alto contraste | #FFE399 | Mapa GTK3 |

Fontes atuais: [app.py](../ARANDU-DESKTOP/app.py), [style.css](../ARANDU-SUITE/Confluencia/shell/style.css), [mapview.py](../ARANDU-SUITE/Confluencia/app/mapview.py), [Foot](../ARANDU-DESKTOP/session/foot-arandu.ini).

**Diretriz tipográfica:** texto da interface legível e ajustável, monoespaçada no terminal, serifada apenas onde o mapa editorial a emprega. Não exigir fontes proprietárias nem usar cor como único sinal de estado. Testar contraste, leitura e foco em cada combinação efetivamente usada.

## 3. Gramática visual e espacial

| Elemento | Função e regra | Estado |
| --- | --- | --- |
| Semente Adaptativa | Ponto de orientação, navegação e avisos; pequena em repouso; expansão por intenção | Semente pública existente; acesso aos menus nativos e espelhamento experimental de sinais GNOME; cobertura independente ainda pendente |
| Rios | Memória, Abertos e Frequentes; trajetórias e medalhões estáveis; alternar seleção sem fechar os demais rios | Implementação pública existente; padrão de inatividade corrigido no candidato, validação real pendente |
| Medalhões | Identificar e selecionar item real; foco perceptível; não ativar somente pela aproximação | Implementado parcialmente, varia por adaptador |
| Opy | Encontro de janelas, seleção e retorno ao trabalho | Protótipo GTK4/Sway; validar |
| Alça Viva | Gestos de janela e recuperação da orientação | Diretriz autoral; verificar integração com o snapshot público |
| Flechas dos Espaços Vivos | Azul ↗ para Imersão; amarela ↘ para redimensionar com prévia | Diretriz autoral; verificar integração |
| Folha Digital | Ponteiro em folha verde, contorno verde-escuro, nervura dourada | Diretriz visual; verificar Xcursor e compatibilidade |
| Terminal ARANDU | Foot configurado na paleta do ambiente | Configuração existente; testar sessão |

### Contrato de comportamento

- Aproximar o ponteiro revela controles; nunca executa, fecha ou redimensiona por si só.
- Rios não se recolhem por mera inatividade por padrão: o candidato altera `navigation-idle-ms` de 10000 para 0. O menu conserva 0/10/30/60 s; 0 desativa. Preferências já gravadas são preservadas. A saída do modo de navegação ao devolver o foco ao aplicativo, clicar fora, cancelar ou ativar um item permanece: não é recolhimento por tempo. O temporizador opcional não deve interromper varredura. Validar o comportamento real antes de declarar conformidade.
- Flecha azul no canto superior direito aponta para fora e para cima; amarela no canto inferior direito para fora e para baixo. Ocultas em repouso; a amarela apresenta prévia antes de concluir alteração.
- Alça Viva: diagonal superior para encerrar (respeitar cancelamento e diálogo de salvamento); para cima no centro para Imersão; para baixo no centro para recolher ao Rio; duplo clique para tela cheia. Título discreto aparece ao aproximar. Ações distintas com limiares e recuperação verificáveis; não eliminar meios acessíveis de controle.
- Cabeçalho Vivo em janelas reais: reservar ao menos 52 px lógicos como diretriz inicial, ampliar se necessário, sem cobrir conteúdo nem controles próprios; reservar região inferior para redimensionamento. Aplicável a interfaces abertas pela Semente, nativas e integradas, respeitando limites técnicos de cada compositor.
- Painéis transitórios (Opy, Confluência, menus e agenda): linguagem equivalente para recolher/fechar o painel, sem encerrar a aplicação de origem. Escape e teclado disponíveis; não duplicar controles.
- A Semente deve evitar obstrução da janela ativa; reposicionamento deve respeitar área útil e monitores. Não interceptar cliques em outras aplicações. O candidato implementa este princípio primeiro na etiqueta passiva de sinais, independente da camada dos Rios quando suportada. O reposicionamento automático da própria Semente interativa ainda é uma meta.
- Privacidade: indicação persistente e acessível de câmera, microfone, gravação e compartilhamento quando efetivamente ativos. Não retirar os indicadores originais do sistema enquanto a substituição não for comprovadamente equivalente. No candidato, a Confluência suspende sua própria ocultação da barra e elimina a sondagem de 300 ms destinada a esse controle. Extensões externas não são alteradas; não garantir visibilidade se houver conflito. Não inventar estado de sensores.

## 4. Acessibilidade e variantes sensoriais

Foco visível, escala ajustável, alto contraste, redução de animação, navegação por teclado e cancelamento. A versão pública possui preferências de escala 85–120%, varredura experimental 2/3,5/5 s e acionador global configurável entre as opções oferecidas pelo painel. Não equivale a suporte a qualquer acionador físico, voz ou gesto. Modalidades futuras devem expressar as mesmas intenções, com consentimento e alternativa sem sensores.

## 5. Cultura e procedência

A identidade busca diálogo respeitoso com referências Guarani. Formas e nomes devem ser contextualizados; não atribuir autenticidade tradicional a grafismos autorais nem reproduzir elementos culturalmente restritos. Revisar terminologia e usos com interlocutores Guarani antes de formular afirmações culturais específicas. Registrar procedência e direitos de cada recurso gráfico; este manual não concede licença.

## 6. Aceite de cada interface

- Testar repouso, aproximação, seleção, ação, cancelamento e retorno ao foco.
- Conferir sobreposição, arraste e prévia em resoluções, escalas e múltiplos monitores; teclado sem mouse; contraste e modo econômico.
- Garantir que fechar um painel não fecha janela subjacente; recuperar Semente e Rios sem perda de trabalho.
- Testar presença e precisão de indicadores de privacidade; impedir captura não solicitada.
- Medir latência, CPU/RAM e custo em repouso antes/depois sob condições comparáveis.
- Registrar versão, commit, ambiente, evidências e limitações. Não declarar implementação apenas porque o contrato foi escrito.

O Design Core é uma referência de engenharia pública, subordinada aos limites de privacidade e à política de separação de pesquisa. Mudanças futuras devem documentar divergências e critérios de aceite.
