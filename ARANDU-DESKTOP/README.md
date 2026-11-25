# ARANDU Desktop 0.7.7 — protótipo GTK4

**Desenvolvimento identificado no projeto:** Rafhael Brum Werlang.  
**Estado:** experimental, com testes automatizados; validação gráfica da versão candidata pendente.

## Escopo atual

Aplicação GTK4 independente das APIs do GNOME Shell, que reutiliza os recursos visuais da Confluência (Semente, Rios, medalhões e geometria). Pode executar como janela do desktop existente ou como cliente de um laboratório Sway. O Sway é o compositor de terceiros, não um compositor ARANDU.

Na interface há navegação por aplicativos instalados; os adaptadores para consultar e agir sobre janelas Sway só operam no modo de laboratório autorizado. Opy, indicadores locais, Terminal ARANDU (Foot) e Centro de Atualizações têm escopo experimental. Não anunciar um ambiente independente de produção, nem capacidade assistiva validada. Recursos locais não sincronizados não fazem parte do snapshot público.

## Iniciar sem alterar a sessão atual

Use um clone Git completo, necessário também aos testes de triagem do snapshot. A partir da raiz do repositório:

```bash
git status --short --branch
python3 -m unittest discover -s ARANDU-DESKTOP/tests -v
bash ARANDU-DESKTOP/rodar-arandu-desktop.sh
```

O script não instala pacotes nem registra uma sessão de login. Caso faltem bibliotecas GTK4, consulte os pacotes oficiais da distribuição; em Mint, as dependências básicas são `python3-gi` e `gir1.2-gtk-4.0`. A instalação desses pacotes no sistema exige ação administrativa separada. O aplicativo pode ser iniciado diretamente com `python3 ARANDU-DESKTOP/app.py` quando as dependências estiverem presentes.

## Testar Sway opcionalmente

Leia o [manual do laboratório](session/README.md). Em uma sessão X11 compatível, use `bash ARANDU-DESKTOP/session/start-nested.sh`. Salve o trabalho; saia do laboratório com Ctrl+Alt+Shift+Q. Não selecione a sessão experimental no login antes de verificar o funcionamento e o retorno seguro ao GNOME.

## Arquitetura, pesquisa e privacidade

- A aplicação não deve depender da implementação de núcleos privados.
- Tupã usa opções de IA escolhidas pela pessoa; nenhuma conta, conversa, chave ou memória privada é integrada automaticamente. Não compartilhe credenciais nem exportações privadas.
- Os adaptadores experimentais de pesquisa são interfaces locais; não constituem motor cognitivo validado.
- O crate Rust local implementa contratos mínimos de navegação e ponte desabilitada. A aplicação GTK utiliza o modelo Python; não anunciar integração Python/Rust concluída. Testes separados: `cargo test --manifest-path ARANDU-DESKTOP/rust-core/Cargo.toml` (com Rust instalado).
- Adaptação e ações sobre a sessão exigem consentimento conforme o contrato de interface.

Consulte [versões e evidências](../docs/ESTADO_E_VERSOES.md), [publicação científica](../docs/PUBLICACAO_CIENTIFICA_ZENODO.md) e [índice](../docs/README.md). Nenhum DOI da versão foi confirmado.

## Histórico de desenvolvimento

As seções seguintes são registros cronológicos, não instruções atuais de instalação. Identificadores, testes e limitações descritos em cada marco pertencem à época correspondente. Para executar hoje, prefira as instruções acima e a matriz de versões. A versão inicial 0.2 usava canvas 1200 × 500, medalhões gráficos sem associação a aplicativos e modelo Python; esses limites mudaram nos marcos posteriores.

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

## Print Screen → Ctrl+V no ChatGPT (sessão ARANDU Wayland)

Após `sudo apt install grim wl-clipboard`, **Print Screen** captura o monitor/saída padrão via `grim -` e envia um PNG diretamente a `wl-copy --type image/png` (área de transferência temporária). **Não há arquivo persistente por padrão** nem sincronização com Semente, Memória ou ECA. **Shift+Print** salva PNG na pasta Imagens explicitamente. O usuário decide onde colar, com `Ctrl+V`; a captura não é enviada à rede automaticamente.

Para ativar sem sair da sessão real Sway, executar no Foot **após git pull**:
```bash
sudo apt install wl-clipboard
swaymsg 'bindsym Print exec /bin/bash /home/oem/Downloads/ARANDU-TAPE-COMPLETO/ARANDU-DESKTOP/session/capture-screen.sh --clipboard'
swaymsg 'bindsym Shift+Print exec /bin/bash /home/oem/Downloads/ARANDU-TAPE-COMPLETO/ARANDU-DESKTOP/session/capture-screen.sh --save'
```
O caminho acima é específico do VAIO oem: em outras máquinas usar o caminho absoluto do próprio clone. Novas sessões recebem os atalhos a partir dos modelos de configuração instalados no repositório. O compositor precisa estar rodando e `SWAYSOCK` válido. Se `wl-copy` não existir, instalar `wl-clipboard` primeiro. Em sessões de múltiplos monitores, `grim -` segue o comportamento de captura padrão do compositor.

## Observatório de Desempenho — versão 0.6.3

Na GUI ARANDU, clicar **Desempenho** para obter uma fotografia local de RAM (MemAvailable, estimativa sem cache recuperável), swap, carga média do sistema em 1/5/15 minutos e processos ordenados por RSS. Clicar **Medir novamente** para atualizar. Sem vigilância em segundo plano, sem transmissão ou registro automático. **Load average não é porcentagem de CPU; RSS pode contabilizar memória compartilhada em diversos processos.**

Para preparar uma comparação entre sessões do mesmo computador, usar o Foot:
```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
python3 ARANDU-DESKTOP/performance.py
# Salvar APENAS se desejar, em arquivo privado e novo:
python3 ARANDU-DESKTOP/performance.py --save "$HOME/arandu-baseline.json"
```
Em cada sessão (ARANDU, GNOME, Cinnamon etc.), medir no mesmo VAIO, após igual período de inicialização, com mesmos programas abertos e carga semelhante. A coleta no terminal permite amostras de sessões diferentes, mas **não separa automaticamente o consumo exclusivo do ambiente gráfico do sistema todo**; comparar apenas MemAvailable e RSS isolados não permite afirmar que um desktop é mais rápido.

Para testar um aplicativo específico já aberto: `ps -C firefox -o pid,rss,%cpu,comm` (RSS em KiB por processo; `%CPU` é média desde início do processo, não taxa instantânea). Alternativamente procurar `firefox`, `nemo` ou `foot` na lista do Observatório, que mostra os 8 maiores processos por RSS. Para experimentos reproduzíveis de tempo de resposta, medir a mesma tarefa em ambas sessões, com cache quente/frio controlado e ao menos 5 repetições; não comparar somente a abertura de uma instância já em execução.

**Métricas futuras:** latência de abertura de aplicativos, FPS/composição, consumo PSS proporcional (smaps_rollup), amostragem temporal de CPU/temperatura, energia e gráficos históricos com consentimento. Nenhum resultado comparativo foi medido ou reivindicado no VAIO ainda.

## 0.6.4 — Ensaio CPU/RAM ARANDU × GNOME (opt-in)

O botão `Desempenho → Ensaio comparativo (5 medições)` abre Foot com uma medição de 5 amostras por 1 segundo. Exibe os dados no terminal; não armazena automaticamente. O módulo `benchmark.py` pode medir uma sessão, salvar um JSON privado apenas por ação explícita e comparar arquivos de sessões diferentes, sem rede nem telemetria.

```bash
# Na sessão ARANDU, salvar primeira medição (arquivo novo, exclusivo, permissão 600)
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
python3 ARANDU-DESKTOP/benchmark.py --measure --count 10 --interval 1 --save "$HOME/arandu-benchmark-arandu.json"

# Mais tarde, na sessão GNOME, nas mesmas condições:
python3 ARANDU-DESKTOP/benchmark.py --measure --count 10 --interval 1 --save "$HOME/arandu-benchmark-gnome.json"

# Comparar, a partir de qualquer sessão:
python3 ARANDU-DESKTOP/benchmark.py --compare "$HOME/arandu-benchmark-arandu.json" "$HOME/arandu-benchmark-gnome.json"
```

O comparador usa medianas de RAM estimada, CPU global e swap e calcula diferenças `GNOME – ARANDU`. **Não conclui automaticamente qual desktop é mais rápido:** RAM/CPU incluem todos os processos, inclusive navegador/serviços, e uma única medição curta é indicativa. Para precisão, repetir ensaios em repouso e com tarefas equivalentes, no mesmo hardware, evitando comparações com programas diferentes. Arquivos contêm métricas locais e etiqueta da sessão, e não devem ser enviados sem revisão. A medição termina sozinha; nenhum daemon foi instalado.

**Pendente:** validação dos novos testes e funcionamento real do botão GTK no VAIO.

## ARANDU 0.7.0 — Opy, espaço de encontro de janelas

A **Opy** é o novo seletor de janelas do ARANDU, inspirado na ideia de um espaço de encontro. O termo cultural é empregado como metáfora de organização da interface, **não como simulação de rituais ou práticas religiosas Guarani**. O desenvolvimento segue com atenção à procedência e à possibilidade de revisão com representantes culturais.

Na sessão Sway, **Alt+Tab** invoca a Opy por uma aplicação GTK4 própria (`opy.py`). A janela flutuante lista janelas abertas de verdade, exclui a própria Opy e aceita **setas**, **Enter** para focar e **Esc** para sair sem ação. Não fecha aplicativos; não monitora em segundo plano. O `Ctrl+Alt+A` segue trazendo a Semente. O recurso não opera sobre as janelas do GNOME hospedeiro.

### Ativar sem sair do ARANDU atual

```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
git pull --ff-only
python3 -m unittest discover -s ARANDU-DESKTOP/tests -q
swaymsg "bindsym Mod1+Tab exec /usr/bin/python3 $PWD/ARANDU-DESKTOP/opy.py"
```

Esse comando instala **somente o atalho da sessão atualmente aberta**, sem mudar GNOME/LightDM. Para que a Opy também abra **flutuante centralizada**, a regra `for_window` consta no template de sessão para o **próximo login ARANDU**; a ativação dinâmica de um atalho não garante toda a apresentação visual do template novo.

A barra de abas padrão do Sway ainda permanece nesta fase. Primeiro vamos validar que Opy encontra Firefox/Foot/Nemo e troca de foco corretamente; só depois consideraremos retirar/substituir a barra nativa, preservando alternativa acessível. A Opy não é uma camada layer-shell e não substitui o compositor Sway.

**Estado:** versão e testes publicados no GitHub; ainda falta o teste real no VAIO.

## 0.7.1 — Retorno temporário ao GNOME para amadurecimento

A primeira experiência no login ARANDU mostrou lacunas em captura/clipboard, fechamento sem barra de título e organização de aplicativos. **Voltar ao GNOME é a decisão de teste recomendada** até a Opy e os atalhos estarem confirmados em sessão aninhada.

Ambas as configurações Sway agora usam `default_border none` e `workspace_layout default`, removendo os títulos/abas próprios do Sway por padrão; janelas de aplicativos GTK com decoração própria podem continuar mostrando cabeçalho. `Super+T` oferece volta ao layout com abas, `Alt+Tab` abre Opy, `Super+Q` solicita fechamento da janela atual, `Super+H` move janela para o scratchpad e `Super+Shift+H` recupera. `Ctrl+Alt+A` retorna ao ARANDU e `Ctrl+Alt+Shift+Q` encerra a sessão Sway experimental.

Esses atalhos não são idênticos a uma operação de encerramento de processo: `kill` é um comando de janela do Sway, e `scratchpad` não libera memória do aplicativo. Em layouts sem abas, várias janelas podem ficar lado a lado; `Super+F` dá tela cheia à janela selecionada. Não remover atalhos de recuperação antes da validação.

### Banco de testes a partir do GNOME

```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
git pull --ff-only
bash ARANDU-DESKTOP/session/verify-essentials.sh
bash ARANDU-DESKTOP/session/start-nested.sh
```

Na janela Sway aninhada, validar `Alt+Tab`, seleção de Firefox/Foot/Nemo, `Super+Q`, `Super+H`, `Print` + colar e `Shift+Print` antes de voltar ao seletor de login ARANDU. O script de verificação é somente leitura e testes, não altera GNOME ou o login.

**Importante:** `git pull` atualiza código-fonte; sessão Sway que já estava aberta não carrega a nova configuração sozinha. Testar sessão aninhada recém-aberta. A sessão de login registrada utiliza scripts da árvore atual mas não deve ser escolhida para trabalho principal até aceitação no VAIO.

## 0.7.2 — Semente essencial: relógio, rede, bateria, Bluetooth, som e sessão

Na interface ARANDU, logo abaixo do mapa gráfico da Semente, aparecem botões próprios: **relógio** (hora local, atualizada periodicamente), **Rede**, **Bateria**, **Bluetooth**, **Som** e **Sessão**. Ao clicar nos indicadores, abre-se um painel com dados reais do Linux: `/proc/net/route` mostra apenas presença de rota IPv4 (não comprova conexão com internet); bateria consulta `/sys/class/power_supply`; Bluetooth consulta `bluetoothctl show`; volume consulta `pactl`. Recursos ausentes aparecem como indisponíveis, não inventados. O som pode ser ajustado em passos explícitos de 5%.

**Sessão → Solicitar saída → Encerrar sessão** tem diálogo de confirmação GTK4; usa `swaymsg exit` somente na sessão ARANDU Sway, preservando GNOME. É o equivalente visual à saída manual de emergência, que permanece via Ctrl+Alt+Shift+Q.

**Área de Trabalho** abre a pasta desktop configurada do usuário no Nemo. Isso permite copiar, colar, renomear e movimentar arquivos com atalhos do próprio Nemo. **Não é ainda uma superfície com ícones e arrastar/soltar diretamente sobre o papel de parede**; essa função requer integração posterior com compositor/gerenciador da área de trabalho. Cópia de texto entre aplicativos segue a área de transferência Wayland/X11; `wl-clipboard` habilita integração CLI de imagens/texto, mas não deve ser executado no GNOME/X11 para simular a sessão Sway. `Print → Ctrl+V` ainda necessita validação real dentro do ARANDU.

**Estado dos testes:** código e novos testes de contrato publicados; funcionamento da UI deve ser verificado no VAIO a partir da sessão aninhada, antes de voltar ao ARANDU como login principal. Indicadores da Semente são um primeiro painel horizontal **próximo à Semente**, não ícones embutidos no desenho SVG — a integração visual final ainda está pendente.

## 0.7.3–0.7.4 — ações essenciais e Centro de Atualizações

- A Semente disponibiliza Firefox, Nemo, Foot, Área de Trabalho (pasta Nemo) e Opy (visão experimental das janelas). Captura `Print → Ctrl+V` também é acessível por um botão explícito; recortar/copiar/colar arquivos permanece no Nemo e ainda não existe drag-and-drop sobre o papel de parede próprio.
- Rio Abertos: Focar, Recolher à Opy via scratchpad, Recuperar janela recolhida e Encerrar janela com confirmação. Identificadores sempre validados pelo Sway antes da ação. Recolher **não** libera RAM; encerrar pode solicitar salvamento dentro do programa.
- Status da Semente: gerenciadores externos autorizados de redes (`nm-connection-editor`), Bluetooth (`blueman-manager`), áudio (`pavucontrol`) e calendário (`gnome-calendar`), só quando presentes, sem instalação automática.
- **Atualizações:** botão `Atualizações`, consulta somente leitura do cache APT sob clique; contagem pode estar desatualizada. Flatpak ainda exige conferência no gerenciador oficial. `Abrir gerenciador oficial` lança MintUpdate quando instalado (fallback GNOME Software/Discover), com seus próprios controles de permissões. O ARANDU não executa apt upgrade/update nem instala pacotes sozinho.

### Comparador ARANDU × GNOME × Cinnamon

O script abaixo cria uma medição explicitamente solicitada por sessão, com 10 amostras de CPU global, memória disponível/estimada e swap. Não inicia serviços, não instala pacotes, não fecha sessões. O resultado é um arquivo JSON local, novo e restrito ao usuário:

```bash
# Na sessão GNOME do mesmo VAIO
bash ARANDU-DESKTOP/session/benchmark-desktop.sh gnome 1

# Noutra ocasião, no login ARANDU (após confirmar estabilidade)
bash ARANDU-DESKTOP/session/benchmark-desktop.sh arandu 1

# Se realmente houver uma sessão Cinnamon instalada
bash ARANDU-DESKTOP/session/benchmark-desktop.sh cinnamon 1
```

Repetir três a cinco vezes por ambiente com MESMA resolução, mesmos aplicativos e rede, tempo após login e alimentação. Evitar GNOME com navegador aberto versus ARANDU vazio. Comparar relatórios individuais:

```bash
python3 ARANDU-DESKTOP/benchmark.py --compare CAMINHO-GNOME.json CAMINHO-ARANDU.json
```

**Limites metodológicos:** essas medições observam o computador inteiro; NÃO medem a memória exclusiva da shell nem provam superioridade. Adicionar posteriormente PSS por processo, consumo de energia (medidores adequados), tempo real de login, latência de Opy/Alt+Tab, inicialização de aplicações e estabilidade de sessões. Não atribuir métricas inventadas a GNOME ou Cinnamon. Monitorar também acessibilidade, recuperação de falhas e comportamento do clipboard. A comparação não é automática entre dois desktops simultâneos: cada ambiente precisa de seu próprio login e relatório.

**Estado:** versão 0.7.4 publicada no código. Testes e usabilidade na máquina do usuário pendentes; o GNOME permanece o ambiente principal recomendado.

## 0.7.5 — Terminal ARANDU e atualização interna consentida

- Terminal ARANDU = emulador Foot maduro, configurado com `session/foot-arandu.ini`: paleta verde floresta/dourado, tipografia monoespaçada, contraste e padding. Não é um emulador proprietário reimplementado.
- `Super+Enter` nas sessões Sway inicia `session/terminal-arandu.sh` via config temporária gerada; o botão **Terminal ARANDU** também o abre.
- **Evolução → Consultar e atualizar ARANDU no Terminal** lança `session/evolve-arandu.sh --update` em uma janela do Terminal ARANDU. O script só procede em `main`, árvore limpa e após digitar exatamente **ATUALIZAR**. `git pull --ff-only origin main`, testes e registro do commit anterior; sem sudo, upgrades APT ou reiniciar GNOME.
- O comando `bash session/evolve-arandu.sh --check` consulta estado local sem rede nem alterações. Para atualizar os pacotes Linux, usar **Atualizações → Gerenciador oficial** e revisar as confirmações do Mint.
- O Git atualiza arquivos, mas **não substitui automaticamente o processo da interface ARANDU já aberto**. Para interface renovada, reiniciar a aplicação ou entrar em sessão ARANDU nova depois de validar testes, salvando trabalho.
- `.github/workflows/arandu-desktop-tests.yml` executa testes Python e validação sintática Bash em pushes. Isso não substitui teste real de sessão Sway no VAIO.
- Caminho do clone no VAIO: `~/Downloads/ARANDU-TAPE-COMPLETO`. GNOME continua como ambiente de segurança e desenvolvimento.

### Atualização recomendada a partir do GNOME

```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
git pull --ff-only
python3 -m compileall -q ARANDU-DESKTOP
python3 -m unittest discover -s ARANDU-DESKTOP/tests -v
bash ARANDU-DESKTOP/session/verify-essentials.sh
bash ARANDU-DESKTOP/session/start-nested.sh
```

A opção existente de sessão no login usa os mesmos arquivos do clone. **Não selecionar o login ARANDU como ambiente principal até validar a 0.7.5 no Sway aninhado.**

## 0.7.7 — Ontologia transversal; atualização a partir do VAIO

A Semente recolhida/expandida usa os SVG originais e `seed_presentation.py`, sem alterar o arandu-core canônico. `ontology_contract.py` mapeia algumas intenções a fontes ontológicas e rejeita ações sensíveis sem intenção/confirmação. **É um guardrail parcial**, não uma auditoria completa da AO nem prova de equivalência com a máquina de estados Rust.

**Tupã**: ChatGPT (no navegador) é a opção inicial. Outras APIs ou Ollama só funcionam mediante escolha explícita e configuração; não existe incorporação automática desta conversa nem leitura da ECA. A ponte `eca_bridge.py` permite examinar exportações experimentais JSON somente leitura, nunca a Semente oficial. `adaptation.py` observa indicadores locais sob demanda, sugere modo econômico e permite aplicar/desfazer alterações exclusivamente na apresentação GTK. O adaptador de Bluetooth lista dispositivos pareados sob clique e permite conectar/desconectar; o fone Philips depende de pareamento real no VAIO.

**Atenção:** a interface 0.7.7 e os contratos novos estão publicados, mas não foram validados na sessão gráfica VAIO. Antes de trabalho diário, validar suíte unitária completa, Sway aninhado, Opy, fechamento, saída, ChatGPT, Bluetooth, captura/clipboard, áudio e fallback para GNOME. Não chamar 0.7.7 de estável sem esses ensaios.

```bash
cd "$HOME/Downloads/ARANDU-TAPE-COMPLETO"
git pull --ff-only
python3 -m compileall -q ARANDU-DESKTOP
python3 -m unittest discover -s ARANDU-DESKTOP/tests -v
for file in ARANDU-DESKTOP/session/*.sh ARANDU-DESKTOP/session/login/*.sh; do bash -n "$file"; done
bash ARANDU-DESKTOP/session/verify-essentials.sh
# Só se tudo estiver OK:
bash ARANDU-DESKTOP/session/start-nested.sh
```

`git pull` renova arquivos no clone, não substitui janela GTK já aberta. A sessão ARANDU nativa permanece opcional, nunca padrão automaticamente. **Sem login nativo antes da verificação visual**.
