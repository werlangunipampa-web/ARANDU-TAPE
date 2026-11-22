# ARANDU Desktop 0.6.2 — inicialização estável e lançador interno

**Desenvolvimento:** Rafhael Brum Werlang  
**Origem:** ARANDU TAPE / Linux Mint / GNOME 46, com preservação da interface existente.

## O que é hoje

Uma **aplicação GTK4 própria** que agora reutiliza os **SVG originais** `rios.svg`, `semente.svg`, `memory.svg`, `open.svg` e `frequent.svg` e `geometria.json` da Confluência. A Semente, os três Rios, o botão de aplicativos instalados e as informações de autoria funcionam em uma janela GTK4 independente do GNOME Shell. Funciona **sobre** GNOME ou Cinnamon, mas **não depende das APIs internas do GNOME Shell**.

**Ainda não é** ambiente de sessão, gerenciador de janelas, compositor, desktop alternativo no login, observador de janelas, sistema cognitivo conectado ou substituto do Linux Mint.

## Iniciar no Linux Mint

No terminal (sem sudo, assumindo clone existente):

```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
git pull --ff-only
cd ARANDU-DESKTOP
python3 -m unittest discover -s tests -v
python3 app.py
```

Se faltar GTK4, instalar apenas as bibliotecas oficiais da distribuição, **com consentimento do usuário**:

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-4.0
```

Também pode iniciar com `bash ARANDU-DESKTOP/rodar-arandu-desktop.sh` a partir da raiz do clone. O script não instala pacotes, não cria serviços, não altera a sessão de login e não executa comandos privilegiados.

## Limitações da visualização 0.2

O gráfico usa um canvas nativo de 1200 × 500 px com rolagem em telas menores. Os quinze medalhões representam **posições gráficas**, sem dados de aplicativos associados. O layout deve ser visualmente testado na máquina antes de se declarar compatível com dimensionamento/HiDPI. Os ativos SVG permanecem no diretório original, evitando duplicação; a organização das pastas do repositório deve ser mantida.

## Rust (núcleo experimental isolado)

```bash
cd ARANDU-DESKTOP/rust-core
cargo test
```

O crate Rust contém somente os contratos reversíveis de seleção/recolhimento e uma ponte ECA desabilitada. A interface GTK4 **ainda usa o modelo equivalente em Python**. Integração Python ↔ Rust é marco futuro; não afirmar que já existe.

## Direitos e privacidade

- A listagem de **aplicativos instalados** é solicitada pelo usuário. Isso **não é** listagem de janelas abertas.
- O Rio Abertos aguarda adaptador de janelas autorizado. Memória e Frequentes não armazenam informações nesta versão.
- O laboratório cognitivo **ARANDU ECA** permanece isolado e não é importado.
- A abertura de um aplicativo requer clicar nele.
- Não instalar extensões, não substituir sessão, não modificar GSettings.
- O ARANDU TAPE (Confluência) continua operando normalmente.

## Evolução planejada

1. Validar o protótipo gráfico no Linux Mint e correção da Confluência 3.2.3.
2. Separar geometria/renderização do modelo de navegação, revisar acessibilidade e identidade.
3. Criar adaptador opcional, seguro e somente leitura para janelas, com permissões explícitas.
4. Adicionar testes de integração e transporte Rust ↔ GUI. Medir latência e consumo.
5. Criar sessão ARANDU opcional com compositor comprovado, reversão para GNOME/Cinnamon e suporte a Wayland/Xwayland.
6. Somente depois, integrar projeções ECA somente leitura com validação ontológica.

**Critério de aceite:** nunca chamar o aplicativo GTK de um 'compositor' nem chamar testes unitários de 'validação da sessão Linux real'.

Veja também `ARANDU-SUITE/docs/PLANO-DIRETOR-E-VERSOES.md`.

## Ajuste 0.2.1 (22/11/2026)

A captura da versão 0.2 no VAIO mostrou os Rios cortados verticalmente porque o painel informativo expandia até ocupar o espaço do canvas. A 0.2.1 usa uma geometria proporcional de 900 × 375, reduz o painel informativo e adiciona teste de enquadramento. **Publicada, mas ainda não validada na sessão GTK4 real após a correção.**

## Novo marco 0.3.0 (22/11/2026)

- **Rios adaptativos:** conserva o SVG e as posições originais da Confluência e adapta o canvas entre 48% e 100% conforme a largura disponível, com ajuste periódico somente enquanto a tela está visível.
- **Painel contextual retrátil:** as informações não ocupam permanentemente a metade da janela. Botão `Mostrar/ocultar informações`.
- **Aplicativos instalados:** clique no botão correspondente para exibir nos quinze medalhões os primeiros resultados alfabéticos reais de `Gio.AppInfo.get_all()`. É possível buscar por nome. Nenhuma relação falsa com janelas abertas.
- **Confirmação antes de abrir:** clicar num medalhão apresenta nome e botão `Abrir aplicativo`. Não executa nenhum aplicativo com apenas a seleção do medalhão.
- **Proteção ECA:** modo isolado por padrão; Memória, Frequentes e Abertos permanecem visuais sem provedor de janelas ou registro de frequência.
- **Versão 0.2.1 preservada no Git:** se houver regressão visual, permanecer na versão anterior até corrigir.

**Status:** publicada no GitHub. Testes escritos, mas execução real e validação no Linux Mint ainda pendentes.

## ARANDU Desktop 0.5 — abertura e foco na sessão Sway (laboratório)

O aplicativo GTK4 ainda é uma janela dentro do Sway; **não existe camada layer-shell ou compositor ARANDU próprio**. O botão **Janelas da sessão Sway** consulta `swaymsg get_tree` somente no laboratório, quando acionado. A própria janela ARANDU é excluída. Medalhões exibem janelas verificadas e pedem confirmação antes de executar `swaymsg [con_id=N] focus`, com ID validado novamente imediatamente antes do comando. Não é possível selecionar janelas do GNOME hospedeiro.

Em `sway.config.in`, **Super+Enter** executa o Foot (terminal) dentro do Sway para teste. `Super+Tab` alterna janelas; `Ctrl+Alt+Shift+Q` sai do compositor aninhado. O Rio da Memória, Frequentes e a ECA permanecem isolados.

**Ainda falta validar graficamente** no VAIO a seleção, confirmação e retorno ao Foot. A operação IPC é síncrona com timeout de 3 segundos e pode causar pausa breve em erro de comunicação; não monitorar continuamente. A versão anterior permanece no histórico Git.

## Revisão 0.5.1 — observação do VAIO

No VAIO em 22/11/2026, 25 testes Python e 2 Rust passaram e a janela ARANDU abriu no Sway aninhado, **mas a captura ainda não confirmou foco entre duas janelas**. Apareceram avisos transitórios do wlroots (`xdg_surface`) e GDK sobre reposicionamento de pop-ups. Não há evidência de travamento fatal; evitar mascarar avisos. `Ctrl+C` gerou `Pipe quebrado` porque terminou abruptamente o compositor.

A interface 0.5.1 oferece o botão **Abrir Foot no Sway** somente dentro do laboratório, por clique explícito; não usa `shell=True`, nem executa comandos como root. Depois de abrir o Foot, volte ao ARANDU com **Super+Tab** dentro do Sway, clique **Janelas da sessão Sway**, observe os nomes reais e selecione/confirme o medalhão Foot. A tecla Super pode ser interceptada pelo GNOME hospedeiro: o botão de abertura evita depender desse atalho para criar a segunda janela. Saia pelo atalho de encerramento do Sway, não por `Ctrl+C`.

## Revisão 0.5.2 — navegação efetiva e retorno explícito

Após a abertura comprovada de ARANDU e Foot lado a lado, melhoramos o caminho para validar **troca de foco entre janelas existentes**. Na sessão Sway:
1. Clique **Abrir Foot no Sway** para criar a segunda janela.
2. Com foco no Sway, pressione **Ctrl+Alt+A** para retornar ao ARANDU. Se o gerenciador de atalhos hospedeiro interceptar, use as abas Sway.
3. Clique diretamente no rótulo/medalhão **ABERTOS** (ou no botão **Janelas da sessão Sway**), que agora solicita a árvore real de janelas Sway.
4. Use o medalhão Foot ou a lista acessível de seleção de janelas. Clique **Focar esta janela** para mudar o foco.
5. Volte com **Ctrl+Alt+A** e valide o retorno, sem abrir outro Foot.

São mantidos os testes de segurança (sem janelas do GNOME, sem ECA e sem execução de comandos recebidos de títulos). O Sway ainda é compositor de terceiros dentro de janela GNOME. **Código publicado, teste físico 0.5.2 pendente.**

## Laboratório 0.6.1 — tela cheia e múltiplas saídas

`bash ARANDU-DESKTOP/session/start-nested.sh` executa **uma saída virtual** aninhada. Opcionalmente, `bash ARANDU-DESKTOP/session/start-nested.sh --outputs=2` ou `--outputs=3` solicita até 3 saídas **virtuais** do backend X11. Não são equivalentes a detectar ou configurar fisicamente 2-3 monitores do VAIO.

No laboratório, `Ctrl+Alt+A` alterna exibir/ocultar a janela ARANDU flutuante por scratchpad do Sway; não é uma superfície layer-shell transparente. O botão `Tela cheia` expande/recolhe a própria janela ARANDU, enquanto `Telas do ARANDU` lista as saídas informadas via IPC e permite mover a janela por nome enumerado.

A leitura de saídas é sob demanda. Sway permanece o compositor efetivo; ARANDU ainda é cliente GTK4. O GNOME hospedeiro, TOPBAR e ECA não são alterados. **Código e testes publicados; comportamento de 0.6.1 ainda depende de teste real no VAIO.** As opções de monitor preferido/foco/janela ativa da Confluência GNOME ainda não foram integralmente portadas.

## Correção 0.6.2 — iniciar e trabalhar de dentro do ARANDU

O 0.6.1 introduziu regra `for_window` de scratchpad automático que pode ocultar o ARANDU e interromper a experiência de abertura de programas. A 0.6.2 **restaura o lançamento visível como aba normal** no Sway aninhado e retorna ao ARANDU por `Ctrl+Alt+A`. O scratchpad automático foi desativado. `Super+Shift+Espaço` ainda permite flutuação manual.

Na própria janela ARANDU há atalhos explícitos **Arquivos (Nemo)** e **Terminal (Foot)**. Executam apenas programas conhecidos instalados no Mint, por clique e sem `shell=True`; não criam serviços persistentes nem modificam GNOME. O botão existente `Aplicativos instalados` e medalhões permanece com seleção seguida de confirmação.

**Nota de integração:** aplicativos de instância única, como gerenciadores de arquivos, podem ser redirecionados à sessão GNOME hospedeira; precisamos observar no VAIO se o Nemo aparece dentro do Sway antes de alegar integração completa. O Foot é o primeiro teste controlado. Testar uma saída virtual; tela cheia e saídas múltiplas permanecem opções experimentais.

**Status:** correção publicada, testes unitários ainda não executados no VAIO após o update. Não temos sessão de login ARANDU nem motor Rust ligado à interface GTK.

## ARANDU no seletor de login — ensaio independente (a validar no VAIO)

A sessão opcional **ARANDU Desktop (Experimental)** usa o compositor Sway Wayland REAL e a GUI GTK4 atual. **Não é um compositor próprio, não é GNOME e ainda não tem integração completa com áudio, redes, portais, notificações, travamento de tela nem todos os serviços do Mint.** O laboratório aninhado continua disponível.

**Primeiro**, no GNOME, sem privilégios:
```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
git pull --ff-only
python3 -m unittest discover -s ARANDU-DESKTOP/tests -v
bash -n ARANDU-DESKTOP/session/login/{start-login.sh,manage-login.sh}
bash ARANDU-DESKTOP/session/login/manage-login.sh --check
```
**Opcional, somente se os testes passarem e o usuário quiser ver a opção no login**:
```bash
sudo bash ARANDU-DESKTOP/session/login/manage-login.sh --install
```
O instalador cria somente `/usr/local/bin/arandu-login-session` e `/usr/share/wayland-sessions/arandu-desktop-lab.desktop` com marcador de propriedade, não altera sessão padrão, configuração do LightDM ou GNOME, nem reinicia o sistema. Na tela de login, selecionar **ARANDU Desktop (Experimental)** manualmente; selecionar o GNOME como antes é sempre possível.

Na sessão ARANDU, `Ctrl+Alt+A` volta à janela dos Rios, `Super+Enter` abre Foot e `Ctrl+Alt+Shift+Q` encerra Sway e retorna ao login (atalho disponível mesmo que a GUI não abra, desde que o compositor esteja operacional). Em caso de compositor bloqueado, tentar alternar para um TTY com Ctrl+Alt+F3 e voltar ao login de forma manual, sem comandos de recuperação arriscados; manter acesso a outro ambiente antes de mudar o login.

Para **remover somente a opção ARANDU**, ainda no GNOME:
```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
sudo bash ARANDU-DESKTOP/session/login/manage-login.sh --remove
```
A opção de login aponta para o caminho absoluto **deste clone**: não apagar/mover a pasta até remover ou reinstalar a entrada. Não habilitar login automático para o ARANDU enquanto experimental. O instalador recusa sobrescrever sessão/launcher que não tenham marcador ARANDU.

**Estado:** scripts e testes publicados no GitHub, sem teste físico da sessão nativa no VAIO. Os 34 testes relatados foram da versão 0.6.1 **aninhada**, não validam LightDM, seat, DRM, entrada ou a inicialização nativa.
