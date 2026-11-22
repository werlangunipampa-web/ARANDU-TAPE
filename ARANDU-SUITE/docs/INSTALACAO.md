# Instalação e recuperação

## Requisitos

GNOME Shell; Python 3; ferramentas GNOME `gnome-extensions` e `glib-compile-schemas`; dependências GTK3, GI e Cairo usadas no TAPE. O script `--preflight` identifica componentes ausentes.

## Instalação sem privilégios de administrador

```bash
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
bash instalar-tudo.sh
```

O instalador preserva a TOPBAR existente e faz backup da Confluência. A extensão será instalada em `~/.local/share/gnome-shell/extensions/confluencia@arandulab`.

## Conferir

```bash
gnome-extensions info confluencia@arandulab
gnome-extensions info arandu-topbar@local
```

Em GNOME X11, após salvar os trabalhos: `Alt+F2`, `r`, Enter. Em Wayland, encerre a sessão e entre novamente. Não use `sudo`.

## Configuração da camada e do botão de ajuda

```bash
SCHEMA_DIR="$HOME/.local/share/gnome-shell/extensions/confluencia@arandulab/schemas"
SCHEMA="org.gnome.shell.extensions.arandu-confluencia"
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" floating false
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" show-help-button true
```

`floating=false` configura os rios na camada da área de trabalho. O comportamento visual real depende do GNOME e precisa ser conferido.

## Reversão

Localize os backups em `~/.local/share/arandu-tape-confluencia/backups/` e consulte as opções do instalador da Confluência (`bash Confluencia/instalar.sh --help`). Os arquivos da TOPBAR histórica não devem ser sobrescritos. Para desativar apenas a Confluência: `gnome-extensions disable confluencia@arandulab`.

## Distribuições e versões

Não há garantia de suporte universal. Testar primeiro no GNOME 46 / X11 e validar separadamente cada versão e Wayland, com atenção à hierarquia de janelas, atalhos e D-Bus.
