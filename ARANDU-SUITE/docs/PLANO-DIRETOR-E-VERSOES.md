# ARANDU — plano diretor, contrato de evolução e histórico

**Idealização e desenvolvimento:** Rafhael Brum Werlang  
**Repositório de referência:** werlangunipampa-web/ARANDU-TAPE  
**Regra:** este documento registra decisões verificáveis, pendências e limites. Não declara validação gráfica que ainda não ocorreu.

## Visão final do ARANDU

Uma camada de navegação gráfica própria, acessível e discreta no desktop GNOME, com identidade visual unificada, autonomia tecnológica e controle local pelo usuário. O sistema deve **facilitar a transição entre aplicativos sem atrapalhar digitação, clique, seleção ou produção acadêmica**.

### 1. Experiência de navegação: Semente e três Rios

- Uma **Semente** e três rios: **Memória**, **Abertos**, **Frequentes**.
- Medalhões para aplicativos e janelas, acionáveis por teclado, mouse/touchpad, toque e acessibilidade assistiva.
- Atalhos `Super+Alt+1/2/3` abrem a camada no monitor pertinente; `Super+Alt+0` cancela; teclado e acionador percorrem e confirmam.
- Na navegação, Semente e rios aparecem temporariamente à frente. Ao abrir um aplicativo, clicar **na mesma janela**, clicar em outra janela ou voltar a digitar, **a camada deve se recolher imediatamente**.
- Tempo de inatividade padrão **10 segundos**, opções 30/60/desligado. Durante **varredura assistiva**, não recolher automaticamente por tempo para não prejudicar usuários com mobilidade reduzida.
- Guia dos Rios e configurações não devem abrir automaticamente: apenas por ação deliberada.
- O modo flutuante permanente continua optativo, **desligado por padrão**.
- Em duas/três telas: seguir janela ativa (padrão), seguir ponteiro/toque, principal ou tela fixa; preservar uma única sessão de navegação/varredura. Desconexão de tela deve recuperar posição segura.
- **Validação pendente:** testar na prática retorno à mesma janela com mouse/touchpad em GNOME 46 X11, além de teclado, touchscreen e monitores extras.

### 2. TOPBAR e identidade

- TOPBAR gráfica com grafismos Arandu, Yvy, Kaaguy, Tape, Trama; paletas Terra, Mate e Cinza.
- Botão ARANDU abre grade de aplicativos GNOME; botão RIOS controla Confluência; engrenagem é a **única central de personalização**.
- Páginas: **Identidade visual**, **Semente e Rios**, **Sobre o ARANDU**.
- Identidade visual abriga os **papéis de parede originais**, quando recuperados do primeiro computador. Não recriar os originais por aproximação; não substituir wallpaper durante a instalação; permitir prévia, aplicação e restauração.
- Recuperar da versão antiga todos os controles ainda úteis, com avaliação de compatibilidade, em vez de apagar o legado.
- **Sobre o ARANDU** mostra o crédito 'Desenvolvimento: Rafhael Brum Werlang', versões locais e link para repositório. Versão instalada é diferente de versão carregada em execução.

### 3. Acessibilidade e segurança de uso

- Varredura controlada, nunca ativar aplicativos sem confirmação explícita.
- Configurar escala 85/100/120%, contraste, velocidade 2/3,5/5 s, acionador e visibilidade da barra.
- Não capturar indevidamente teclas em aplicativos; cliques fora da camada devem continuar alcançando a janela de destino.
- Sem execução automática arbitrária; configuração local persistente; acesso a dados recentes respeita opções de privacidade GNOME.
- Não destruir extensões históricas nem o trabalho anterior; backup e restauração antes de qualquer alteração.

### 4. Qualidade, instalação, evolução

- Repositório `main` como origem do código; cada mudança significativa com commit e versão, notas de alteração, testes simulados, verificação estática.
- Testar primeiro no VAIO, depois no desktop principal e em 2–3 monitores. Só chamar **estável** depois de validação manual.
- Atualizador transacional com backup de Confluência e TOPBAR, sem `sudo` e sem reinício forçado do Shell. GNOME precisa carregar a nova versão após logout/login.
- Diagnóstico `AssistiveStatus` somente leitura: seleção, varredura, camada, monitor, intervalo/timeout; não expor nomes desnecessários de janelas em logs.
- Evoluções futuras devem atualizar **este plano**, o changelog e os testes correspondentes.
- Distribuição, instalador, guia de acessibilidade e documentação no mesmo pacote.

## Histórico resumido

| Versão | Marco | Evidência/pendência |
|---|---|---|
| Confluência 3.1 beta (15) | Medallhões, guia, acessibilidade configurável, alternância da barra | Testes simulados e observações VAIO |
| 3.2.0 beta (16) | Camada temporária e 1–3 monitores | Observações de menus sobrepostos |
| 3.2.1 beta (17) | Fechamento dos painéis; detecção de foco e timer de 10 s | Instalado/testes simulados, regressões visuais relatadas |
| 3.2.2 beta (18) | Clique fora, digitação e superfície transparente | **Usuário confirmou melhoria no VAIO**; mesma janela ainda problematizada |
| **3.2.3 beta (19)** | Sinal `notify::key-focus` e botão liberado para mesma janela | **Publicada, ainda não validada no VAIO** |
| TOPBAR 6.6.1.2 | Identidade preservada, botões ARANDU/RIOS, engrenagem | Preferências TOPBAR evoluem sem alterar a versão de seu núcleo de Shell |

## Próxima validação funcional

1. `gnome-extensions info confluencia@arandulab` deve exibir **3.2.3-beta (19)** após login.
2. Na **mesma janela**: abrir Rio pelo atalho e clicar num campo editável, ou voltar a digitar. Rios devem sair instantaneamente.
3. Outra janela: clicar e garantir que o evento não é bloqueado.
4. Inatividade: 10 s; interagir com medalhão reinicia temporizador.
5. Varredura: tempo não cancela seleção.
6. Engrenagem: abrir Identidade visual / Semente e Rios / Sobre o ARANDU; confirmar crédito e versão real.
7. Confirmar ausência de Guia/configurações automáticos e não regressão dos grafismos.

## Regras de aceite

Aceitar como estável somente com testes simulados aprovados, versão GNOME carregada identificada, sessão gráfica real validada, backup verificado e nenhuma regressão em acesso assistivo.

## Trilha independente — ARANDU Desktop 0.1 (2026-11-22)

- Protótipo GTK4 autocontido em `ARANDU-DESKTOP/`. **Não substitui GNOME nem Cinnamon, não instala sessão gráfica**.
- Semente e três Rios em visual próprio, lançador explícito de aplicativos instalados, seção Sobre com crédito ao desenvolvedor.
- Rio Abertos sem provedor de janelas nesta fase, para não anunciar dados simulados como observação real.
- Memória, Frequentes e ECA inativos; nenhuma migração de identidade, coleta automática ou sincronização.
- Contrato de sessão verificável em Python, núcleo mínimo Rust com testes locais; integração entre eles ainda não implementada.
- Lançador somente de usuário `bash ARANDU-DESKTOP/rodar-arandu-desktop.sh`.
- **Status:** arquivos publicados no GitHub. Testes e execução GTK4 no Linux Mint **pendentes de validação pelo usuário**.
- Avanço posterior somente após avaliação visual, acessibilidade, comportamento ao abrir apps e medição de desempenho, com o TAPE atual intocado.


## ARANDU Desktop 0.2.0 — Confluência visual desacoplada

- Preserva `ARANDU-DESKTOP/0.1` no histórico Git e a versão funcional do GNOME/TOPBAR.
- Reutiliza **diretamente** `ARANDU-SUITE/Confluencia/app/assets/rios.svg`, `semente.svg`, `memory.svg`, `open.svg`, `frequent.svg` e `geometria.json`.
- Interface `GTK4` isolada com caminhos e Semente reais, rótulos clicáveis e marcadores visuais; motor ECA e provedor de janelas **não conectados**.
- Testes adicionais de geometria e integridade visual sem dependências externas em `ARANDU-DESKTOP/tests/test_layout.py`.
- **Status:** arquivos publicados; não houve validação visual no VAIO ainda. Verificar comportamento do layout em 1366×768, tela cheia e HiDPI antes de aceitar.
- **Próximo marco:** medalhões somente quando houver entidades reais autorizadas, renderização responsiva sem rolagem horizontal e adaptador de leitura de janelas separado do núcleo cognitivo.


## ARANDU Desktop 0.3.0 — rios adaptativos e aplicativos instalados (2026-11-22)

- **Experimento publicado, sem teste GTK real ainda:** canvas redimensionável até 100%, em tela estreita mínimo 48%, mantendo geometria original.
- Painel informativo retrátil para priorizar a Semente e os Rios; o botão Sobre preserva o crédito Rafhael Brum Werlang e a numeração.
- Até quinze medalhões ligados a `Gio.AppInfo` (aplicativos instalados), com pesquisa e **confirmação explícita** antes de iniciar. Não representam janelas abertas, memórias ou frequência de utilização.
- Medallhões sem aplicativo válido ficam indisponíveis.
- Segurança: sem alterar login/compositor/GNOME, sem coleta de uso, sem integrar ou migrar ECA.
- **Aceite pendente:** executar testes Python/Rust e abrir GTK4 no Linux Mint. Conferir escala ao reduzir/restaurar janela, seleção, pesquisa, confirmação e recolhimento. Registrar regressões antes de evoluir para provedor de janelas.


## ARANDU Desktop 0.4 — sessão experimental aninhada no Mint (2026-11-22)

- **Estado: publicada para testes, não homologada.** `ARANDU-DESKTOP/session/start-nested.sh` inicia Sway compositor Wayland **dentro de janela do GNOME X11**, com backend X11 explicitamente configurado. Requer pacote `sway` instalado e compatibilidade do hardware.
- Ainda é um **laboratório**, não há entrada ARANDU no login, compositor próprio, layer-shell nem substituição da sessão gráfica existente. A GUI cliente dentro do Sway continua o protótipo 0.3, com ID GApplication próprio para evitar acionar a janela GNOME já aberta.
- Configuração Sway temporária, criada no `mktemp` e removida ao sair; não altera `~/.config/sway`, GSettings, login, TOPBAR ou Confluência.
- **Saída segura:** `Ctrl+Alt+Shift+Q` ou `Super+Shift+Esc` enquanto a janela aninhada está focada; fechar a janela Sway também encerra o laboratório.
- Conector de janela `session/windows.py` consulta `swaymsg get_tree` apenas mediante chamada explícita; sem persistência e sem integração ainda com a interface.
- ECA/G4 não importadas, não migradas, não ativadas.
- Testes adicionados para isolamento, contrato de saída, identidade do cliente e parsing determinístico da árvore de janelas.
- **Próximo aceite:** confirmar compositor abre no VAIO; confirmar janela ARANDU está **dentro do Sway**, não apenas no GNOME; abrir outro aplicativo no Sway; saída sem encerrar GNOME; diagnóstico do driver caso incompatível.
- Após validação: extrair camada de interface em sobreposição (layer-shell em compositor compatível) e testar protocolo de foco e janelas reais **sem degradar** a Confluência GNOME.

## ARANDU Desktop 0.5 — foco em janelas reais do Sway (2026-11-22)

- **Código publicado, validação gráfica pendente no VAIO.**
- O botão `Janelas da sessão Sway` consulta explicitamente a árvore IPC do compositor aninhado e não lê janelas GNOME. A própria janela ARANDU é excluída.
- Medalhões representam janelas existentes (limite 15). Selecionar um medalhão não muda o foco: exige botão de confirmação. O `con_id` escolhido é validado novamente contra o estado atual antes do comando de foco.
- Atalho `Super+Enter` abre Foot dentro do Sway para teste; saída aninhada `Ctrl+Alt+Shift+Q`.
- **Limitação declarada:** GTK4 ARANDU continua janela cliente normal, não há overlay layer-shell nem recolhimento real sobre a janela do Foot. Ponte IPC não se conecta à Seed/ECA e não coleta histórico.
- **Aceite:** testar abertura do Foot, lista de janelas, medalhão, confirmação de foco, recusa de janela removida, retorno seguro ao GNOME. Verificar 25+ testes Python e Rust.

## ARANDU Desktop 0.5.1 — verificabilidade do foco (2026-11-22)

- O VAIO confirmou o compositor Sway aninhado com ARANDU 0.5 aberto; 25 testes Python + 2 Rust aprovados. Não há ainda teste humano confirmando comutação entre duas janelas.
- A captura exibiu somente ARANDU. Foram observados avisos do wlroots/GDK de mapeamento de superfícies, sem demonstrar falha fatal.
- Criado botão **Abrir Foot no Sway**, disponível exclusivamente quando `ARANDU_SESSION_LAB=1` e `SWAYSOCK` está presente, sem ação automática.
- A consulta de janelas lista os nomes reais no painel e os expõe em medalhões, com confirmação anterior ao foco.
- **Pendente:** abrir Foot, retornar ao ARANDU, escolher medalhão e confirmar foco; garantir que os eventos não alterem janelas do GNOME hospedeiro e sair pelo atalho do compositor.
- Em hipótese alguma publicar esse marco como sessão ARANDU de login ou compositor próprio.

## ARANDU Desktop 0.5.2 — Rios para janelas Sway, ida e volta (2026-11-22)

- Corrigida a diferença entre `Rio ABERTOS` e botão auxiliar: durante laboratório Sway, clicar **ABERTOS** agora consulta janelas efetivamente abertas, sob demanda.
- Acrescentado `Ctrl+Alt+A` na configuração temporária Sway para reencontrar a janela ARANDU sem instanciar programas.
- Acrescentada lista acessível de janelas no painel contextual; cada seleção exige confirmação explícita antes do foco.
- O estado de navegação permanece aberto enquanto a seleção estiver ativa, e `Recolher Rios` o limpa.
- **Estado:** código e testes de contrato publicados; somente a presença de duas janelas foi validada no VAIO, não a troca por medalhão nesta revisão.
- **Próximo teste:** Foot -> Ctrl+Alt+A -> ABERTOS -> selecionar Foot -> Focar -> verificar foco real -> Ctrl+Alt+A para retorno, sem modificar GNOME.
- A ECA permanece desconectada, o compositor Sway não é substituído pelo ARANDU e nenhum registro automático de histórico é autorizado.

## Desktop 0.6.1 — tela cheia, até três saídas virtuais e scratchpad (22/11/2026)

- **Meta de integração GNOME:** Semente/Rios sobre janelas, recolher sem encerrar, adaptação multi-monitor e tela cheia, sem coletar histórico ou tocar na ECA.
- `Ctrl+Alt+A` no Sway alterna `scratchpad show`; janela ARANDU passa a flutuante com regra temporária. É um **protótipo de sobreposição**, ainda sem transparência real ou layer-shell.
- `Telas do ARANDU` consulta `swaymsg get_outputs` somente mediante clique; permite mover a janela para saída cujo nome exista no compositor. `Tela cheia` é opção do cliente GTK4.
- `start-nested.sh --outputs=1|2|3` ajusta `WLR_X11_OUTPUTS` e simula **saídas virtuais**, não a detecção de monitores físicos, que permanece um requisito futuro.
- GNOME/Confluência/TOPBAR mantidos; serviços Mint (Nemo, NetworkManager, áudio etc.) são reaproveitáveis, mas uma sessão ARANDU completa ainda precisará prover integração de desktop, portais e serviços.
- **Status:** código publicado e testes preparados; validação gráfica/funcional no VAIO pendente. Não afirmar que Sway virou um compositor escrito pelo ARANDU nem que suporte físico a três telas esteja concluído.

## Desktop 0.6.2 — estabilidade do ambiente e aplicativos internos (2026-11-22)

- Após relato de dificuldade para abrir aplicativos na revisão 0.6.1, regra de scratchpad automático foi removida da configuração temporária do Sway, porque ocultar a janela principal compromete a experiência.
- ARANDU volta a iniciar **visível como uma aba normal**, com retorno direto via `Ctrl+Alt+A`; flutuação manual continua possível.
- Interface incorpora botões **Arquivos (Nemo)** e **Terminal (Foot)** dentro do próprio ARANDU, somente sob clique em sessão aninhada, com executáveis locais permitidos, sem shell e sem alteração de login.
- `Aplicativos instalados` continua disponível; seleção de medalhão não executa automaticamente por questão de validação e acessibilidade.
- Teste de aceitação: ARANDU inicia visível -> clicar Foot -> voltar com Ctrl+Alt+A -> clicar Arquivos -> verificar se janela ficou dentro do Sway -> foco via ABERTOS. Aplicativos single-instance do Mint poderão reutilizar instância no GNOME; não presumir sessão separada.
- Semente overlay layer-shell, modo desktop próprio no login, múltiplos monitores físicos e evolução da interface por ações próprias são marcos futuros; preservar GNOME e dados cognitivos.

## ARANDU Desktop — candidato a sessão opcional de login (2026-11-22)

- Criado diretório `ARANDU-DESKTOP/session/login` com configuração Sway exclusiva de sessão nativa, inicializador sem root e gerenciador opt-in `--check` / `--install` / `--remove`.
- `--install` exige sudo manual e cria apenas dois arquivos próprios: `/usr/local/bin/arandu-login-session` e `/usr/share/wayland-sessions/arandu-desktop-lab.desktop`. Não altera GNOME, LightDM, padrão de login, configurações pessoais nem instala dependências.
- `--remove` apaga apenas os dois itens marcados como gerenciados pelo ARANDU; recusa sobrescrever/apagar outros arquivos.
- Ao contrário do ensaio aninhado, a sessão real remove flags de backend X11 do wlroots e executa Sway Wayland sobre o hardware. Precisa validação específica de seat, login manager, GPU, teclado, mouse, saídas, integração GTK/Nemo e retorno ao greeter.
- Emergência: `Ctrl+Alt+Shift+Q` encerra a sessão experimental, volta ao seletor de login se compositor estiver operante. GNOME permanece outra opção.
- **Não declarar pronta nem recomendar login automático**: o código e testes contratuais não substituem o teste físico do VAIO nem provam integração de desktop completa. A Semente GUI segue GTK4, Rust segue isolado, camada layer-shell e motor de aprendizagem ainda não conectados.

## Contrato permanente — captura de tela no ARANDU (2026-11-22)

- **Print Screen:** captura PNG somente para a área de transferência Wayland (`grim - | wl-copy --type image/png`), sem gravar arquivo automaticamente; o usuário cola com Ctrl+V em ChatGPT ou outro aplicativo de sua escolha.
- **Shift + Print:** salva arquivo PNG somente por solicitação explícita.
- O contrato é mantido no código-fonte da sessão de login e do laboratório aninhado, portanto permanece após reinícios, ao contrário de atalhos adicionados manualmente com `swaymsg`.
- A opção `--check` do gerenciador do login agora verifica `grim`, `wl-copy` e ambos os atalhos; testes de regressão em `test_login_contract.py`.
- Não há armazenamento permanente de capturas na Semente, Memória, ECA ou nuvem, nem envio automático à rede. O conteúdo no clipboard permanece somente enquanto o serviço Wayland o mantiver ou até ser substituído.
- **Critério de aceite antes de publicar futuras versões:** rodar suíte de testes, inspecionar `--check`, testar fisicamente Print -> Ctrl+V no navegador e Shift+Print -> arquivo, sobretudo após alterações da configuração do compositor.
- Uma sessão já aberta com configuração antiga não recebe os novos atalhos automaticamente; deve usar `swaymsg` para habilitá-los no momento ou reiniciar a sessão ARANDU depois da atualização do Git.

## Desktop 0.6.3 — Observatório de Desempenho (22/11/2026)

- Painel `Desempenho` disponível dentro do ARANDU, leitura pontual de `/proc/meminfo`, `/proc/loadavg` e RSS dos principais processos.
- Métricas: RAM total/disponível/estimada utilizada excluindo cache recuperável, swap, carga CPU 1/5/15 min e núcleos lógicos; explicitamente **não** confundir carga média com % de CPU nem RSS somável com RAM exclusiva.
- Script `ARANDU-DESKTOP/performance.py` permite capturas JSON de sessões ARANDU/GNOME sob solicitação, com escrita apenas via `--save` e permissão 0600. Não coleta continuamente nem envia telemetria.
- Comparação legítima exige mesmas condições de máquina/carga/programas, várias repetições e medidas adicionais de tempo de resposta e PSS; nenhum benchmark comparativo foi medido ainda.
- Testes unitários acrescentados para parsing de RAM, processos e ausência de persistência automática. Execução efetiva e interface ainda requerem validação no VAIO.

## Desktop 0.6.4 — benchmark comparativo reproduzível (22/11/2026)

- Criado `ARANDU-DESKTOP/benchmark.py` com amostragem limitada a 2–20 intervalos de 0,5–5 s, RAM disponível/em uso, swap e CPU global calculada do delta de `/proc/stat`.
- Criado comparador offline de dois relatórios JSON `--compare`, que calcula diferenças de mediana sem inventar superioridade entre desktops. Identifica sessões por variável `XDG_SESSION_DESKTOP`.
- O botão `Desempenho → Ensaio comparativo (5 medições)` abre o Foot apenas sob clique e encerra a medição sozinho; não bloqueia o GTK nem grava arquivo automaticamente.
- Persistência apenas mediante `--save`: cria arquivo novo, permissionamento 0600, recusa sobrescrever. Nenhuma telemetria/rede.
- `tests/test_benchmark.py` testa CPU, medianas, segurança de arquivo, limites de coleta e disparo por GUI.
- Critério: executar todos os testes Python e coletar baselines reais nas sessões ARANDU e GNOME, sob condições equivalentes. Não declarar desempenho comprovadamente superior sem repetições.

## Desktop 0.7.0 — Opy, encontro das janelas (22/11/2026)

- `Alt+Tab` na sessão ARANDU Sway invoca `opy.py`, interface GTK4 experimental de seleção de janelas existentes: setas, Enter para focar, Esc para cancelar; seleciona apenas janelas verificadas por `swaymsg get_tree` e não encerra aplicações.
- Opy usa janela flutuante centralizada por regra temporária do Sway, não depende do GNOME Shell nem substitui o Sway; barra tabbed existente permanece até validação.
- Contratos de compatibilidade: `Ctrl+Alt+A` retorna aos Rios, Print cola captura no clipboard, Shift+Print salva PNG; nenhuma ECA, histórico de uso ou telemetria.
- **Respeito cultural:** Opy é uma referência metafórica ao encontro e à organização, não representação de cerimônia ou reprodução de práticas religiosas. Recomendada futura escuta de interlocutores Guarani para avaliar terminologia e iconografia.
- Publicados testes contratuais de teclado, exclusão da própria Opy, segurança e atalhos preservados. **Pendente:** confirmar no VAIO a abertura/centralização e troca entre Firefox, Nemo, Foot. O registro do atalho na sessão atual pode ser feito por `swaymsg`; centralização completa requer carregar nova configuração após relogin.
- Futuro: reduzir presença da barra convencional de janelas, melhorar agrupamento acessível e navegação por múltiplos monitores, sem bloquear acesso de emergência.

## Desktop 0.7.1 — plano de estabilização dos controles essenciais (22/11/2026)

- Usuário validou entrada no ARANDU pelo login e ChatGPT/Firefox, mas encontrou ausência de ação visual para fechar, dificuldade de Print/clipboard, barra de títulos/abas convencional e navegação básica ainda incompleta.
- **Decisão:** retornar temporariamente ao GNOME e testar em laboratório Sway aninhado. A opção de login ARANDU é preservada, mas não recomendada ainda como sessão principal.
- Templates do Sway agora configuram `default_border none` e `workspace_layout default`: removem decoração/abas **do Sway**, mas cabeçalhos próprios de aplicações podem permanecer. `Alt+Tab` abre Opy; `Super+T` recupera abas, `Super+Q` solicita fechar janela, `Super+H` recolhe ao scratchpad, `Super+Shift+H` recupera; `Super+F` permite maximização via tela cheia.
- Atalhos essenciais mantidos: `Ctrl+Alt+A` para retornar à Semente, `Print` para capturar ao clipboard e `Shift+Print` para arquivo, `Ctrl+Alt+Shift+Q` para saída de emergência.
- `session/verify-essentials.sh` audita dependências e executa testes sem sudo, instalações ou modificações de configuração. `tests/test_essentials_contract.py` verifica contratos em ambos templates de sessão.
- **Aceitação pendente no VAIO:** 1) login GNOME seguro, 2) laboratório Sway inicia, 3) Opy alterna Firefox ↔ Foot, 4) fechamento e recolhimento funcionam, 5) Print → Ctrl+V envia imagem ao ChatGPT, 6) salvar via Shift+Print, 7) retornar ao GNOME sem reiniciar.
- Não afirmar que Opy já substituiu totalmente a barra de janelas ou que todos os programas GTK não tenham cabeçalhos próprios. Preservar modo de reversão via `Super+T` e exit do Sway.

## Desktop 0.7.2 — serviços essenciais próximos à Semente (22/11/2026)

- Indicadores locais: relógio, estado de rota de rede, bateria, Bluetooth e áudio. Falta de dispositivo explicitamente indicada, sem inventar conectividade à Internet.
- Centro de Sessão: controle visual com confirmação para sair do Sway ARANDU; GNOME hospedeiro não é encerrado.
- Botão de Área de Trabalho abre pasta de desktop pelo Nemo; copiar/colar arquivos é inicialmente do gerenciador de arquivos, não do fundo da tela.
- Indicadores próximos à Semente nesta etapa; a integração geométrica nos medalhões originais será feita após testes de usabilidade.
- Nova proposta visual: fundo de paisagem/rio/mata em tons verdes e dourados, com Semente clara em primeiro plano e baixa interferência visual. Arte visual é conceito, não interface executada.
- Testes de contrato publicados. Pendente validação visual no VAIO e verificação completa antes de entrar novamente na sessão ARANDU.

## Desktop 0.7.5 — retorno seguro, atualização interna e Terminal ARANDU (22/11/2026)

- Semente: lançadores Firefox, Nemo, Opy, Terminal ARANDU, pasta Área de Trabalho, captura para área de transferência, ações de janela, indicadores de status, saída confirmada e Centro de Atualizações de pacotes (somente gerenciador oficial).
- Terminal ARANDU: Foot real com esquema de cores verde/dourado e atalho Super+Enter; não reimplementa PTY.
- Centro de Evolução do código: `session/evolve-arandu.sh` valida estado do repositório e exige confirmação literal antes de `git pull --ff-only`; interrompe se houver mudanças locais, não reinicia sessão e testa após atualizar.
- Comparador de desempenho `session/benchmark-desktop.sh` preservado (RAM/CPU/swap locais); próximos ensaios devem medir PSS, carga, energia e latência de Opy/Firefox/Nemo sob as mesmas condições no VAIO.
- Testes contratuais Python de segurança e funcionalidade estendidos; CI `.github/workflows/arandu-desktop-tests.yml` executa testes/sintaxe em pushes.
- **Estado real:** publicação no GitHub confirmada, principais contratos inspecionados; suíte e integração gráfica da versão 0.7.5 **ainda não confirmadas no VAIO**. Preservar GNOME e validar Sway aninhado antes de reentrar na sessão nativa.
- Pendente para fase seguinte: bloqueio seguro, energia/suspensão, notificações, superfície de desktop com drag-and-drop, impressão/scanner, gestão de monitores e interoperabilidade robusta de clipboard entre aplicativos.
