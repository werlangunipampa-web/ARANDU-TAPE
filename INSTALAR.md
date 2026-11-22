# Instalar ARANDU TAPE 2.8.3 (beta)

> **Antes de começar:** trata-se de um protótipo em desenvolvimento. A instalação modifica extensões do GNOME do usuário; faça backup dos seus dados e teste em uma sessão compatível. O instalador preserva a TOPBAR já existente e faz backup da Confluência.

## Requisitos

- Distribuição Linux com **GNOME Shell**; teste realizado pelo projeto em **GNOME 46 / X11**.
- Python 3, suporte a extensões GNOME e ferramentas de compilação de esquemas GSettings.
- Bibliotecas GTK 3, GObject Introspection e Cairo para a aplicação TAPE.
- **GNOME Wayland e outras versões:** comportamento ainda não validado integralmente.
- A TOPBAR incluída possui compatibilidade específica com GNOME 46.

## Um instalador para toda a suíte

O pacote inclui **Confluência (Semente e três rios)** e **ARANDU TOPBAR**. Não é necessário executar dois instaladores. O mesmo `instalar-tudo.sh` instala/atualiza a Confluência e instala a TOPBAR quando ela ainda não existe. Uma TOPBAR já instalada é **preservada**, sem sobrescrita.

No **GNOME 46**, ambos os componentes são preparados e habilitados após o Shell reconhecer as extensões. Fora do GNOME 46, a TOPBAR histórica **não é habilitada automaticamente**; a compatibilidade gráfica ainda precisa ser desenvolvida e testada para outras versões.

Para consultar o estado dos dois componentes depois da instalação:

```bash
bash instalar-tudo.sh --status
```

## Opção 1 — baixar pelo GitHub

1. Acesse a [página do código](https://github.com/werlangunipampa-web/ARANDU-TAPE).
2. Clique em **Code → Download ZIP**.
3. Extraia o ZIP; abra um terminal dentro da pasta extraída e entre em `ARANDU-SUITE`.
4. Execute:

```bash
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
bash instalar-tudo.sh
```

## Opção 2 — baixar com Git (recomendada para atualizações)

```bash
cd ~/Downloads
git clone https://github.com/werlangunipampa-web/ARANDU-TAPE.git
cd ARANDU-TAPE/ARANDU-SUITE
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
bash instalar-tudo.sh
```

**Não execute com `sudo`.** O instalador é destinado ao perfil de usuário.

## Reiniciar o GNOME Shell

- **GNOME X11:** salve o trabalho e pressione `Alt+F2`, digite `r`, Enter.
- **GNOME Wayland:** encerre a sessão e entre novamente.

## Conferir o resultado

```bash
gnome-extensions info confluencia@arandulab
gnome-extensions info arandu-topbar@local
```

A Confluência deve exibir `ACTIVE`. No GNOME 46, a TOPBAR também deverá aparecer habilitada após reiniciar a sessão. Se o GNOME não a reconhecer imediatamente, reinicie a sessão e confira novamente.

## Ambiente limpo: janelas acima dos rios

```bash
SCHEMA_DIR="$HOME/.local/share/gnome-shell/extensions/confluencia@arandulab/schemas"
SCHEMA="org.gnome.shell.extensions.arandu-confluencia"
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" floating false
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" show-help-button true
```

A Semente central entra em repouso após 7 segundos e o medalhão de ajuda após 6 segundos; os medalhões de aplicativos continuam visíveis com os rios abertos.

## Desativar e recuperar

Para desativar apenas a navegação Confluência:

```bash
gnome-extensions disable confluencia@arandulab
```

Backups da Confluência: `~/.local/share/arandu-tape-confluencia/backups/`.

Para diagnóstico, veja [docs/COMANDOS-E-DIAGNOSTICO.md](ARANDU-SUITE/docs/COMANDOS-E-DIAGNOSTICO.md) e [instalação detalhada](ARANDU-SUITE/docs/INSTALACAO.md).

## Avisos sobre acessibilidade

A ponte D-Bus permite comandos assistivos experimentais, mas **reconhecimento de voz, rastreamento da cabeça e gestos de mãos ainda não estão disponíveis para uso final**. O sistema não deve ser tratado como tecnologia assistiva validada clinicamente ou em testes com usuários.

## Download de versões

Até que haja uma versão publicada em **Releases**, use **Code → Download ZIP** e os comandos desta página. O arquivo ZIP gerado pelo GitHub contém o código; não é um instalador de um clique.
