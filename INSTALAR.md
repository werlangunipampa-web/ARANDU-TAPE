# Instalar e testar ARANDU TAPE — Confluência 3.2.3-beta

> **Antes de começar:** trata-se de um protótipo em desenvolvimento. A instalação modifica extensões do GNOME do usuário; faça backup dos seus dados e teste em uma sessão compatível. O instalador preserva a TOPBAR já existente e faz backup da Confluência.

## Escolher o componente

Este guia trata da suíte GNOME, não do aplicativo GTK4 ou do login Sway experimental. Para esses caminhos, consulte [ARANDU Desktop](ARANDU-DESKTOP/README.md). O identificador legado 2.8.2 do instalador não corresponde à versão atual da extensão.

## Requisitos

- Distribuição Linux com **GNOME Shell**; teste realizado pelo projeto em **GNOME 46 / X11**.
- Python 3, suporte a extensões GNOME e ferramentas de compilação de esquemas GSettings.
- Bibliotecas GTK 3, GObject Introspection e Cairo para a aplicação TAPE.
- **GNOME Wayland e outras versões:** comportamento ainda não validado integralmente.
- A TOPBAR incluída possui compatibilidade específica com GNOME 46.

## Um instalador para toda a suíte

O pacote inclui **Confluência (Semente e três rios)** e **ARANDU TOPBAR**. Não é necessário executar dois instaladores. O mesmo `instalar-tudo.sh` instala/atualiza a Confluência e instala a TOPBAR quando ela ainda não existe. Uma TOPBAR já instalada é **preservada**, sem sobrescrita.

No **GNOME 46**, o instalador tenta habilitar os componentes após preparar os arquivos; confira o estado real depois de reiniciar a sessão. Nos GNOME 45 e 47–51, a variante moderna da TOPBAR pode ser instalada, mas sua habilitação exige a opção explícita `--experimental-topbar` e testes. Não sobrescreve TOPBAR já existente. GNOME 40–44 possui variante Confluência, sem TOPBAR moderna.

Para consultar o estado dos dois componentes depois da instalação:

```bash
bash instalar-tudo.sh --status
```

## Opção 1 — baixar o código pelo GitHub

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

Confira se a Confluência foi ativada e se a TOPBAR está no estado desejado. Uma tentativa de habilitação pode falhar; não presuma sucesso apenas pela mensagem do instalador. Se o GNOME não a reconhecer imediatamente, reinicie a sessão e confira novamente.

## Ambiente limpo: janelas acima dos rios

```bash
SCHEMA_DIR="$HOME/.local/share/gnome-shell/extensions/confluencia@arandulab/schemas"
SCHEMA="org.gnome.shell.extensions.arandu-confluencia"
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" floating false
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" show-help-button true
```

A Semente central entra em repouso visual após 7 segundos e o medalhão de ajuda após 6 segundos. Separadamente, o temporizador de navegação da versão pública tem padrão de 10 segundos. Para manter os rios abertos por intenção, selecione **Rios: nunca recolher por tempo** no menu ARANDU TAPE; confira a configuração e o comportamento na sua sessão. A diretriz-alvo está no [Design Core](docs/DESIGN_CORE.md).

## Desativar e recuperar

Para desativar apenas a navegação Confluência:

```bash
gnome-extensions disable confluencia@arandulab
```

Backups da Confluência: `~/.local/share/arandu-tape-confluencia/backups/`.

Para diagnóstico, veja [docs/COMANDOS-E-DIAGNOSTICO.md](ARANDU-SUITE/docs/COMANDOS-E-DIAGNOSTICO.md) e [instalação detalhada](ARANDU-SUITE/docs/INSTALACAO.md).

## Avisos sobre acessibilidade

A ponte D-Bus permite comandos assistivos experimentais. O mapa GTK3 oferece reconhecimento local de uma frase curta sob ação explícita, com Vosk e dependências opcionais instaladas. Voz contínua, rastreamento da cabeça e gestos de mãos ainda não estão validados para uso final. O sistema não deve ser tratado como tecnologia assistiva validada clinicamente ou em testes com usuários.

## Download de versões

Enquanto não houver release aprovada, o clone Git é recomendado para desenvolvimento e auditoria de snapshot. O ZIP gerado pelo GitHub contém o código, não o histórico Git nem um instalador de um clique. A triagem científica exige um clone Git. Consulte [estado e versões](docs/ESTADO_E_VERSOES.md) e [publicação científica](docs/PUBLICACAO_CIENTIFICA_ZENODO.md).


Consulte [acessibilidade](docs/ACESSIBILIDADE.md) e [privacidade](docs/PRIVACIDADE.md) antes de usar os recursos opcionais.
