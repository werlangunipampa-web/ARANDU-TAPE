# ARANDU SUITE 3.0 — TOPBAR unificada (prévia experimental)

## Arquitetura

O comando `ARANDU-SUITE/instalar-tudo.sh` administra dois componentes:

- **Confluência:** Semente, três rios, medalhões e ponte de comandos assistivos.
- **ARANDU TOPBAR:** identidade visual da barra superior.

A TOPBAR continua uma extensão GNOME separada, para respeitar o carregamento e a desativação de extensões do Shell. O **instalador é único** e não pede duas instalações ao usuário.

## Seleção por versão

| GNOME Shell | TOPBAR | Ativação |
|---|---|---|
| 46 | Histórico 6.6.1.2 preservado | Como atualmente, após reiniciar o GNOME |
| 45, 47–51 | Variante ESM defensiva, experimental | Somente com `--experimental-topbar` |
| 40–44 | Sem variante TOPBAR validada | Não ativar automaticamente |
| Versões futuras | Não confirmadas | Validar antes de instalar |

A variante moderna vive em `TOPBAR/modern/`. O instalador **não modifica** o código histórico sob `TOPBAR/arandu-topbar@local/`. Uma TOPBAR já instalada é preservada no destino.

**Importante:** indicar uma versão em `metadata.json` não comprova compatibilidade. As APIs internas do GNOME podem mudar mesmo em versões que suportam módulos ES. A matriz acima indica uma estratégia de construção e testes, não uma certificação.

## Como instalar

```bash
cd ~/Downloads/ARANDU-TAPE
git pull --ff-only
cd ARANDU-SUITE
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
bash instalar-tudo.sh
```

Depois de reiniciar a sessão:

```bash
bash instalar-tudo.sh --status
```

Para **testes controlados** num GNOME moderno diferente de 46, use uma conta/sessão de teste sem TOPBAR histórica previamente instalada:

```bash
bash instalar-tudo.sh --experimental-topbar
```

Reinicie a sessão. O instalador não substitui automaticamente uma TOPBAR existente por outra variante.

## Barra que se oculta automaticamente

No modo automático, a Confluência aguarda aproximadamente **8 segundos** depois que o ponteiro deixa o painel. A barra permanece visível enquanto um menu do painel estiver aberto ou um controle do painel tiver foco de teclado.

Para garantir tempo ilimitado durante testes ou uso assistivo:

```bash
SCHEMA_DIR="$HOME/.local/share/gnome-shell/extensions/confluencia@arandulab/schemas"
SCHEMA="org.gnome.shell.extensions.arandu-confluencia"
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" panel-mode visible
```

## Segurança e recuperação

- Não execute como `sudo`.
- Preserve backups e dados pessoais.
- Se houver problemas, use `gnome-extensions disable arandu-topbar@local` para desligar a barra sem desinstalar a Confluência.
- Em GNOME X11 use `Alt+F2`, `r` após salvar os trabalhos; em Wayland encerre e reabra a sessão.
- A barra da Confluência pode permanecer visível em `panel-mode visible`.
- Nenhum recurso de voz/câmera é ligado automaticamente.

## Testes pendentes

Verificar GNOME 45, 47, 48, 49, 50 e 51 em sessão real, X11/Wayland quando suportado, segurança de foco, restaurar estilo do painel, teclas assistivas e retorno da barra após atualização. Esses testes são necessários antes de habilitar por padrão em outros ambientes.

## Separação funcional no GNOME 46 (revisão)

No painel GNOME 46, o botão **ARANDU** abre a grade nativa de aplicativos do GNOME via `Main.overview.showApps()`. O botão **◈ RIOS** envia `AssistiveCommand('seed:toggle')` à Confluência pela sessão D-Bus, expandindo ou recolhendo os rios sem abrir outra janela. São funções deliberadamente distintas. Se Confluência não estiver ativa, RIOS avisa que a extensão precisa ser habilitada.

**Cuidado ao atualizar:** o código da TOPBAR no GitHub mudou, mas uma TOPBAR já instalada não é sobrescrita pelo instalador unificado (proteção intencional). Para aplicar a revisão a uma máquina com a extensão instalada, guardar cópia de `extension.js`, validar a sintaxe do arquivo fonte e copiá-lo somente para o caminho da TOPBAR instalada. Desabilitar/habilitar somente `arandu-topbar@local`; se o GNOME 46 conservar módulo antigo em memória, terminar a sessão e entrar novamente. Não remover a TOPBAR nem a Confluência e não reativar extensões históricas.

## Preferências visuais recuperadas no GNOME 46

A extensão TOPBAR histórica passa a fornecer `prefs.js` baseado em GTK4/Libadwaita, com editor dos valores de GSettings originais: grafismo (`arandu`, `yvy`, `kaaguy`, `tape`, `trama`), paleta (`terra`, `mate`, `cinza`), altura, opacidade, cápsula do relógio e visibilidade do botão ARANDU.

No painel, o botão de **engrenagem**, ao lado de RIOS, abre a janela. Alternativamente, usar `gnome-extensions prefs arandu-topbar@local`.

Atualização existente: copiar **somente** `extension.js` e `prefs.js` para `~/.local/share/gnome-shell/extensions/arandu-topbar@local/` depois de criar backup. Nenhuma alteração no esquema é necessária; não sobrescrever os valores salvos e não executar instalador unificado para esse ajuste. Reiniciar a sessão gráfica depois de salvar trabalhos para carregar a versão nova da extensão.

**Validação pendente:** janela de preferências e engrenagem ainda não foram testadas visualmente no VAIO; testes de sintaxe JavaScript não equivalem a teste GTK/Adwaita. Caso as preferências não abram, verificar `journalctl --user -b` e restaurar arquivos do backup.
