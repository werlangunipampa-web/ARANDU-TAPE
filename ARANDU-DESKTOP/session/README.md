# ARANDU Desktop — laboratório Sway aninhado

## Escopo real

Este ensaio executa um **compositor Wayland Sway aninhado em uma janela X11** do desktop Linux Mint existente. Uma aplicação GTK4 ARANDU executa como cliente **dentro** desse compositor. O script de sessão aninhada não registra login nem altera a configuração da TOPBAR ou Confluência; ações explícitas realizadas pelo usuário dentro do laboratório podem afetar seus aplicativos e dados.

**O ARANDU ainda NÃO é o compositor nem substitui uma sessão gráfica completa.** O aplicativo iniciado é o código GTK4 presente no clone (0.7.7 no candidato documentado). Os números 0.3 e 0.4 nos registros históricos e nas mensagens legadas do script não são a versão atual do aplicativo. O objetivo desta fase é provar a infraestrutura de execução independente do GNOME Shell e criar base para janelas reais e integração futura com elementos de desktop/overlay.

## Pré-requisitos (Linux Mint X11)

- `sway` instalado no sistema.
- `python3`, `python3-gi`, `gir1.2-gtk-4.0`.
- Driver e compositor com suporte a backend X11 do wlroots. Nem todo driver/GPU é compatível com esse modo.

O script **não instala nada**, mas se o Sway não estiver disponível, mostra uma instrução de instalação manual. Nada é iniciado automaticamente no login.

## Execução

```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
git pull --ff-only
bash ARANDU-DESKTOP/session/start-nested.sh
```

Pode encerrar a sessão experimental com **Ctrl+Alt+Shift+Q**, com o foco na janela Sway, ou fechando a janela Sway. Isso não encerra o GNOME.

## Limites

- A presença do Sway no sistema é necessária, mas não o torna desktop oficial.
- ECA/Seed G4 permanecem desconectadas, sem migrações.
- O compositor não executa como root, não cria arquivos em `/usr/share/wayland-sessions` e não altera o display manager.
- Não anunciar suporte layer-shell ou compositor próprio sem implementação e evidência específicas.
- O código atual possui adaptador IPC local para janelas Sway, com validação e ação explícita; testar na sessão real.
- Os comandos não executam `sudo`, `apt`, `pkill`, `systemctl`, nem alteram `~/.config/sway`.
- A interface e o protocolo de testes serão avaliados no VAIO antes de declarar esse marco validado.

## Histórico: validação real no VAIO — 22/11/2026

Os registros abaixo descrevem marcos anteriores, não a validação da versão candidata atual.

A captura mostrou o compositor `wlroots - X11-1` aberto **como janela dentro do GNOME**, com o cliente ARANDU GTK4 0.3 executando na tela aninhada. A saída do terminal mostrou **19 testes Python aprovados**. Confirmada a primeira execução gráfica aninhada no VAIO; **não** significa que a sessão ARANDU esteja pronta para login nem que gerencie janelas pela própria interface.

O GTK apresentou aviso `Gtk-CRITICAL: gtk_scrolled_window_set_min_content_height: assertion ... failed`. Corrigido no código do laboratório ao substituir os limites conflitantes por `set_size_request(-1, h)`; o rótulo Frequentes também foi deslocado para permanecer dentro do canvas. Essas correções **ainda precisam ser executadas e confirmadas no VAIO**.

Próximos testes: redimensionar janela Sway; selecionar um programa por medalhão e confirmar a abertura; garantir que nada execute sem confirmação; usar Ctrl+Alt+Shift+Q para voltar ao GNOME. Não instalar sessão ARANDU na tela de login nesta fase.

## Teste em duas janelas — revisão após 0.5.1

O VAIO confirmou por captura a presença simultânea de **ARANDU e Foot dentro do Sway**. Isso valida a criação da segunda janela, **não ainda** a seleção/ativação por medalhão. O Sway distribuiu ambas lado a lado, reduzindo a área do ARANDU e cortando os Rios. Ajustado `workspace_layout tabbed` na configuração **temporária** do laboratório para evitar a divisão horizontal; o usuário alterna as abas com `Super+Tab` dentro do Sway.

Teste de aceitação: iniciar laboratório novamente, usar o botão **Abrir Foot no Sway**, alternar para ARANDU e selecionar **Janelas da sessão Sway**. O Foot deve ser listado. Selecionar medalhão e clicar **Focar esta janela** deve trazer a aba Foot ao primeiro plano. Não alterar layout do GNOME nem arquivos de configuração permanentes.

**Status:** correção publicada, ainda não confirmada na máquina. A captura anterior comprova duas janelas reais, não a troca por medalhão.


Consulte [estado e versões](../../docs/ESTADO_E_VERSOES.md) e [manual Desktop](../README.md) antes de qualquer ensaio. O login nativo é um procedimento separado e não faz parte deste comando.
