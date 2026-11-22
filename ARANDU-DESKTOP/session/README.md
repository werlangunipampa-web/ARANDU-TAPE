# ARANDU Desktop 0.4 — ensaio de sessão aninhada

## Escopo real

Este ensaio executa um **compositor Wayland Sway aninhado em uma janela X11** do desktop Linux Mint existente. Uma aplicação GTK4 ARANDU executa como cliente **dentro** desse compositor. A sessão GNOME/Cinnamon do usuário, o gerenciador de login, a TOPBAR e a Confluência permanecem intactos.

**O ARANDU ainda NÃO é o compositor nem substitui uma sessão gráfica completa.** O protótipo GTK4 dentro do Sway continua sendo a interface 0.3, por enquanto. O objetivo desta fase é provar a infraestrutura de execução independente do GNOME Shell e criar base para janelas reais e integração futura com elementos de desktop/overlay.

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
- A interface 0.3 ainda não usa camada Wayland layer-shell; isso é uma investigação futura, e não deve ser anunciado como implementado.
- A leitura das janelas Sway por IPC será tratada em módulo isolado e somente sob pedido.
- Os comandos não executam `sudo`, `apt`, `pkill`, `systemctl`, nem alteram `~/.config/sway`.
- A interface e o protocolo de testes serão avaliados no VAIO antes de declarar esse marco validado.
