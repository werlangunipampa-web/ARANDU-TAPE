# Arandu Tape · Confluência 2.1.0

Três rios se encontram na Semente. **Memória** retoma janelas recentes e arquivos. **Abertos** traz uma janela específica para a frente, inclusive em outra área de trabalho. **Frequentes** aproxima da Semente os aplicativos que tu mais usas. Os pequenos ícones nos medalhões identificam os aplicativos da máquina.

## Instalar na tua conta

Leva o instalador `Arandu-Tape-2.1.0.run` em um pendrive. Abre um terminal na pasta do arquivo e executa:

```sh
bash Arandu-Tape-2.1.0.run
```

Se preferires o ZIP com o código-fonte, extrai a pasta **Arandu-Tape**, abre um terminal dentro dela e executa `sh instalar.sh`. O instalador usa a tua conta e a instalação principal funciona offline com as dependências disponíveis. Depois, abre **Atividades** e procura **Arandu Tape**. Na primeira instalação da extensão, pode ser necessário encerrar a sessão, entrar novamente e ativar **Arandu Tape · Confluência** em **Extensões**. No mapa, **GNOME conectado** indica que a janela conversou com o Shell.

## Comparar duas máquinas que já têm Arandu

Na pasta do instalador, executa o diagnóstico em cada máquina antes de instalar:

```sh
bash Arandu-Tape-2.1.0.run --diagnostico
```

Pelo ZIP, usa `sh identificar-arandu.sh`. O inventário lê a distribuição, o tipo de sessão, a versão do GNOME, a identificação e a versão das extensões Arandu encontradas. O resultado aparece apenas no terminal. Ele omite nomes de arquivos pessoais e títulos das janelas.

Esta edição usa o identificador **confluencia@arandulab**. O identificador histórico é **arandu-tape@arandulab**. As duas extensões podem ser instaladas na mesma conta. Se aparecerem duas Sementes, podes desativar a anterior temporariamente em **Extensões**. Quando o esquema antigo está disponível, o aplicativo lê uma vez os aplicativos recentes e as contagens de uso compatíveis. Cada computador conserva seu próprio histórico.

## Usar o mapa

| Ação | Como fazer |
| --- | --- |
| Ver um rio | Clica no nome do rio ou no cartão correspondente. |
| Abrir um item | Clica no medalhão ou no item da lista. Passa o ponteiro para ler o título. |
| Mover o desenho | Segura e arrasta a Semente. O painel da Semente inclui **Centralizar mapa**. |
| Descobrir aplicativos | Abre **Aplicativos** no rodapé. |
| Escolher um arquivo | Em **Memória**, usa **Abrir arquivo**. |
| Buscar ou dar um comando | Usa **Ctrl+K**. Experimenta “abrir memória” ou “ir para o relatório”. Quando há vários resultados, escolhe na lista. |
| Navegar pelo teclado | **Ctrl+1**, **Ctrl+2** e **Ctrl+3** abrem os rios. **Tab** ou as setas percorrem os medalhões. **Enter** abre. **Esc** volta. **/** ou **F1** abre os comandos. |
| Abrir o mapa de outro aplicativo | Com a extensão ativa, usa **Super+Shift+T** ou o ícone da Semente no painel superior. |
| Escolher a aparência | No botão de preferências, escolhe **Papel**, **Luz suave** ou **Alto contraste**. **Baixa visão** amplia letras e medalhões. |

O mapa mostra até cinco itens por rio. Em janelas compactas, ele reduz o número de medalhões e mantém a lista completa acessível pelo nome do rio. Numa conta nova, os rios crescem à medida que tu abres aplicativos e alternas as janelas. Um medalhão de rio sem ícone de aplicativo abre a lista.

Com a extensão ativa, a Semente também aparece na área de trabalho. Ao passar o ponteiro sobre ela, os rios se abrem. Um clique abre o mapa, um arraste move a composição. Se os ícones da área de trabalho cobrirem a Semente, abre seu menu no painel superior e escolhe **Mostrar Semente sobre as janelas**. O mesmo menu permite devolvê-la à área de trabalho.

## Compatibilidade

| Ambiente | Comportamento |
| --- | --- |
| GNOME Shell 40–44 | O instalador prepara a extensão no formato clássico do GJS. |
| GNOME Shell 45–51, incluindo 46 | O instalador prepara a extensão em módulos JavaScript. Em Wayland, ativa a extensão para listar e focar as janelas da sessão. |
| Outras versões do GNOME | O aplicativo independente oferece mapa, busca, arquivos recentes, lançador e contagem de usos feitos nele. A integração do Shell depende de uma variante para a versão instalada. |
| Sessão X11 com libwnck3 | O aplicativo lê e ativa janelas enquanto está em execução, inclusive em um desktop como o Xfce. |
| Hardware e dependências | Código interpretado em Python 3.8+ e GJS. Requer GTK 3.22+, PyGObject, Pycairo, GIO e o leitor SVG do GdkPixbuf. A extensão usa `glib-compile-schemas`. |

As versões 40–51 são alvos previstos pelo código e pelo empacotamento. A execução gráfica deste pacote foi testada em Debian 13, X11 e Xfce. A extensão precisa de teste em sessão GNOME real para confirmar o comportamento de cada versão e distribuição.

Se o instalador informar dependências ausentes, no Ubuntu ou Debian usa:

```sh
sudo apt install python3 python3-gi python3-cairo gir1.2-gtk-3.0 librsvg2-common libwnck-3-0 libglib2.0-bin
```

No Fedora, os pacotes correspondentes são `python3-gobject python3-cairo gtk3 librsvg2 libwnck3 glib2`. No Arch ou Manjaro, são `python-gobject python-cairo gtk3 librsvg libwnck3 glib2`. O acesso administrativo serve para instalar as dependências do sistema. O aplicativo é instalado como usuário comum.

## Voz opcional

Os comandos digitados funcionam desde a primeira abertura. Para usar o microfone, prepara um ambiente local do Vosk. O comando abaixo usa o Python do sistema. No Debian ou Ubuntu pode ser necessário o pacote `python3-venv`.

```sh
voz="${XDG_DATA_HOME:-$HOME/.local/share}/arandu-tape-confluencia/voz-venv"
python3 -m venv "$voz"
"$voz/bin/python" -m pip install vosk
```

Baixa e extrai o modelo **vosk-model-small-pt-0.3** para português brasileiro na página [Modelos Vosk](https://alphacephei.com/vosk/models). Em **Aparência e acessibilidade**, escolhe a pasta do modelo que contém o diretório `am`. O capturador pode ser `parec` ou `arecord`. Em **Comandos**, clica em **Ouvir comando**, fala “meus frequentes” e aguarda. A gravação começa por solicitação, processa uma frase localmente e termina após até oito segundos de escuta. **Esc** cancela. O pacote não contém o modelo acústico.

## Manutenção

A partir da mesma pasta do instalador:

```sh
bash Arandu-Tape-2.1.0.run --autoteste
bash Arandu-Tape-2.1.0.run --ativar
bash Arandu-Tape-2.1.0.run --restaurar
bash Arandu-Tape-2.1.0.run --desinstalar
```

Com a pasta extraída, os mesmos argumentos funcionam em `sh instalar.sh`. **Restaurar** recupera a edição Confluência imediatamente anterior a uma reinstalação. **Desinstalar** remove o programa, os atalhos e a nova extensão. Os dados da conta e a edição histórica continuam disponíveis.

Com os caminhos padrão do Linux, o programa fica em `~/.local/share/arandu-tape-confluencia/programa`, o comando em `~/.local/bin/arandu-tape-confluencia` e o estado em `~/.local/state/arandu-tape-confluencia`. A extensão conserva sua memória nas preferências do GNOME. O botão **Limpar histórico** nas preferências limpa os registros do Arandu. O aplicativo respeita a opção de privacidade do GNOME para lembrar itens recentes.

## Sobre a arte

A composição usa como referência a prancha **Navegação que Nasce da Essência** e as versões **Identidade Visual da Confluência** e **Referência Desktop** do projeto Arandu. Os percursos tramados e os medalhões são desenhos vetoriais. O fundo claro reutiliza o grafismo vetorial da edição E1. A pequena paisagem no cabeçalho é um detalhe da prancha fornecida. Os títulos, contagens e ícones dos aplicativos vêm da máquina em uso.

## Atualização 2.1 — diagnósticos e portabilidade

Antes de instalar em outra máquina, executa `bash Arandu-Tape-2.1.0.run --preflight`.
O comando mostra distribuição, sessão X11/Wayland, GNOME, dependências, estado da instalação e reconhecimento da extensão.
`--verificar-rios` roda contratos automatizados de abertura/foco, memória, frequentes e integração com o Shell simulado; **não substitui** um teste gráfico em GNOME real.
`--backup` arquiva os componentes **Confluência** atualmente gerenciados em `~/.local/share/arandu-tape-confluencia/backups` (modo privado), sem incluir/modificar a TOPBAR histórica.
Em atualizações, o instalador gera automaticamente uma cópia antes da troca. A operação `--restaurar` permanece disponível para a edição imediatamente anterior.
A Confluência oferece **seu próprio ícone no painel superior** quando a extensão estiver ativada. Isso **não modifica** o botão da extensão ARANDU TOPBAR antiga; incorporar Confluência ao menu da TOPBAR histórica exigiria revisão/alteração separada daquele código.
Em Wayland, sem extensão ativa, o catálogo e as funções independentes funcionam, mas o foco e a relação de janelas de outros programas são limitados pelo compositor.
Se `gnome-extensions info confluencia@arandulab` disser que não existe após instalar, encerra a sessão GNOME normalmente, entra novamente e verifica `gnome-extensions list`. A instalação do aplicativo pode funcionar mesmo antes desse reconhecimento.


## 2.2.0 — Geometria adaptativa GNOME

Na sobreposição da área de trabalho, a camada vetorial agora acompanha a área útil de cada monitor, em vez de ocupar apenas 1200 × 500 pixels. Semente, medalhões e legendas reposicionam-se a partir da geometria disponível quando o monitor muda. A TOPBAR histórica não é alterada. Testar visualmente nas sessões X11 e Wayland antes de considerar compatibilidade homologada.

## 2.2.1 — Rio e medalhões na mesma geometria

A arte dos três rios é recalculada em SVG para a área útil do monitor a partir da Semente. Os medalhões e os rótulos usam a mesma geometria de cada rio. Os três percursos alcançam as bordas esquerda, superior e direita. A TOPBAR histórica permanece intocada. Teste gráfico no GNOME necessário.
