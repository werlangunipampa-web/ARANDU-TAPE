# ARANDU — Matriz de coerência filosófica, interface e funcionalidade
**Proposta de engenharia para revisão humana — 22/11/2026**  
**Idealização e desenvolvimento:** Rafhael Brum Werlang

## Hierarquia de fontes

Este documento **não altera a ontologia canônica**, nem é um manifesto substitutivo. Seu propósito é derivar contratos verificáveis de interface/desktop de fontes existentes:

1. Manifesto inicial *Computação Germinativa*, no arquivo **Arandu AVE.pdf**, capítulo “Por que o mundo precisa de um novo paradigma de sistema operacional?” — uso necessário de recursos, compreensão do hardware, adaptação, cooperação, regeneração tecnológica.
2. **ARANDU-Tape-diretrizes-da-sessao-grafica.md** — Semente e três Rios, semântica de navegação, ECA de leitura, acessibilidade e medições.
3. **A0_AUDITORIA_FUNDACIONAL.md** — limites de escrita na Semente, papéis core/adapters, procedimentos de consentimento e recuperação.
4. **arandu-core/docs/CONFLUENCE_SEED.md** — estados `Collapsed`, `Aware`, `Near`, `Expanded`, `Pinned`, tempo lógico monotônico, não recolher durante atividade.
5. **ARANDU-SUITE/docs/PLANO-DIRETOR-E-VERSOES.md** — regras reais da Confluência: recolhimento e foco, modo assistivo sem timeout, 2–3 telas, GNOME fallback.

**Lacuna:** a totalidade da ontologia canônica RDF/Turtle não foi lida/auditada nesta etapa. Os itens abaixo são **contratos propostos** e não axiomas ontológicos.

## Princípios de projeto não negociáveis

- A pessoa permanece no comando, com cancelamento, acessibilidade e configuração previsível.
- A Semente/Confluência só revela complexidade mediante intenção ou evento pertinente; não decorar a tela com botões persistentes desnecessários.
- O core de navegação recebe **intenções** e devolve estados; hardware, compositor, voz, câmera e teclado ficam em adaptadores.
- Não coletar históricos, microfone, câmera, clipboard ou hábitos silenciosamente; distinção estrita entre frequência operacional e memória cognitiva.
- ECA não é requisito para login ou funcionamento básico; só consulta experimental com procedência e autorização, sem escrita no estado oficial.
- Desligamento de serviço, economia de energia e modo sem animação devem preservar funções essenciais.
- Nenhum indicador deve inventar conectividade, bateria, som ou dispositivo; estados desconhecidos devem ser explícitos.
- GNOME/Mint preservado; sem mudança automática da sessão padrão; evolução do Git exige confirmação e testes.
- Metas de velocidade/consumo são hipóteses sujeitas a medição no VAIO, nunca afirmações de vitória sobre GNOME/Cinnamon.

## Mapa de correspondência entre filosofia, ação e teste

| Princípio / fonte | Expressão gráfica e funcional | Estratégia técnica inicial | Contrato de aceite |
|---|---|---|---|
| Complexidade sob demanda / ConfluenceState | Semente compacta em repouso; Rios expandidos por intenção; controles contextuais sem barra tradicional permanente | Core Rust Confluência ou adaptador fiel à máquina de estados; eventos abstratos | Testar estados Collapsed/Aware/Near/Expanded/Pinned, recolhimento sem perda de foco; exceção assistiva |
| Memória e relações / ECA | Rio Memória retoma tarefas recentes quando usuário autorizar; sugestões de relações exibem origem e grau de validação | Adaptador somente leitura, não blocking; sem acoplamento a GNOME | Sem ECA, navegação funciona; sem fonte/evidência, UI declara indisponível |
| Abertos / Confluência | Rio Abertos lista janelas reais | Sway IPC ou compositor-adapter | Foco verificável, cancela com Esc, nenhum nome de janela persistido |
| Opy / extensão de navegação | Lugar de encontro/contextualização das janelas abertas; não substitui a semântica do Rio Abertos | Visão gráfica das janelas consultadas ao abrir, sem monitoramento contínuo; teclado/miniaturas futuras | Alt+Tab, Enter, Esc; recuperação; sem fecha automaticamente |
| Frequentes / diretrizes | Ordenação local de atalhos sob opt-in; nunca interpretação psicológica do usuário | Dados somente mediante autorização, exportação/limpeza pelo usuário | Desligar monitoramento restaura comportamento neutro |
| Economia de energia / manifesto | Modo essencial: mínimo de efeitos, nenhum polling de dispositivos inativos; animações opcionais | Eventos D-Bus para rede/energia onde possível; amostragem limitada e suspensa | Comparar CPU em repouso, energia e memória em VAIO com perfis equivalentes |
| Adaptação ao indivíduo / manifesto | Preferências explicitamente controláveis: escala, contrastes, entradas e disposição contextual | Configuração local reversível, exportável, sem mudança automatizada não solicitada | A pessoa entende, desfaz e desliga cada adaptação |
| Acessibilidade / diretrizes | Mesma intenção via teclado, mouse, acionador, voz ou gesto — sem obrigar sensores | NavigationIntent desacoplado do dispositivo | Operar sem mouse, foco visível, varredura sem timeout, cancelar sempre |
| Centro da Semente / usabilidade | Relógio, rede, bateria, Bluetooth, áudio, calendário, sessão e atualizações revelados quando apropriado | Serviços maduros Linux (UPower, NetworkManager, BlueZ, PipeWire/PulseAudio, atualização oficial) | Indicadores verdadeiros, controles funcionam, ausência de hardware é clara |
| Clipboard / autonomia | Ctrl+C/X/V entre apps e arquivos; Print captura PNG para colar sem gravar | Wayland clipboard/portais, Nemo e XDG | Texto/arquivo/imagem colam no destino; consentimento para coleta |
| Área de trabalho / autonomia | Superfície funcional com arquivos, pastas e arrastar-soltar (futuro), sem confundir com pasta Nemo | Adaptador próprio em etapa posterior, aproveitando serviços XDG | Transferências testadas, desfazer/recuperar, sem perda de dados |
| Gestão de janelas / experiência | Recolher, recuperar, encerrar com pedido claro; sem perder o caminho de volta | Sway IPC + Opy, botão visível e atalho; modo recuperável | Teclado, mouse e Opy; GNOME fallback validado |
| Sessão / identidade | Menu sair, bloquear, suspender/reiniciar com confirmação e salvamento | Gerenciador de sessão, logind/Polkit/portais; NÃO executar comandos destrutivos diretos sem contexto | Sair não perde tarefas sem aviso; bloqueio funciona com segurança |
| Terminal / autonomia tecnológica | Terminal ARANDU de alto contraste, real, responsivo, com comandos normais | Foot temático sobre Sway | Copy/paste, resize, unicode, Bash, saída/recuperação |
| Atualizações / governança | Sistema e apps pelo gerenciador oficial; código ARANDU com consentimento, verificação e atualização reversível | MintUpdate, git fast-forward, testes e registro do commit anterior | Sem sudo automático; falha no teste não esconde regressão; rollback ensaiado |
| Observatório / sustentabilidade | Desempenho acessível sob demanda, comparação entre ambientes no VAIO | /proc, benchmark finito, PSS/latência/energia futuros | Medidas comparáveis, ambiente/carga controlados, sem telemetria |
| Cultura Guarani / contexto | Nomes e grafismos com contexto, sem simulação ou apropriação de rituais | Revisão de terminologia por interlocutores Guarani | Distinção de inspiração técnica de práticas/termos tradicionais verificada |

## Contradições detectadas na interface experimental (corrigir progressivamente)

1. Muitos botões permanentemente expostos sob a Semente: **não refletem** a regra `Collapsed → Expanded`. Migrar para menu compacto contextual, preservando acesso por teclado.
2. A Opy por enquanto é um listador GTK de janelas, **não** uma visão com miniaturas nem substituto validado para a barra/tabbed do Sway.
3. A abertura exige clique e confirmação no catálogo alfabético: seguro para acessibilidade, porém excessivamente custoso para usuários que desejam um único gesto. Implementar perfis de confirmação sem quebrar varredura assistiva nem segurança.
4. O relógio é amostrado a cada 30 segundos, sem modo de energia; preferir agendamento em fronteira de minuto e atualização por eventos.
5. Memória/Frequentes ainda não têm dados autorizados reais; não simulá-los nem mascarar com interface cognitiva.
6. A aplicação GTK ainda não integra formalmente a máquina de estados Rust do `arandu-core`. Evitar duplicação do núcleo e verificar diferenças de semântica entre contratos.
7. O comparador mede recursos globais do computador; ainda não mede causalidade/eficiência exclusiva do desktop, PSS, consumo elétrico ou latência de interação.
8. A tela ilustrativa de referência é **visão artística**, não layout funcional implementado nem descrição literal de cultura Guarani.
9. O documento README da suíte contém trechos históricos desatualizados; evitar confundir versões documentais com código em execução.

## Próximas revisões por prioridade

**R0 — indispensável para voltar ao login nativo:** todos os testes Python/CI e Sway real; captura/clipboard texto, arquivos e PNG; Opy e foco; gerenciamento de janelas; saída confirmada; terminal; fallback GNOME.

**R1 — semanticamente fiel:** Semente compacta ligada à máquina de estados; indicadores por evento; Centro de Sessão seguro; Abertos/Opy não redundantes; perfis de acessibilidade.

**R2 — recursos sustentáveis:** relatório RAM/PSS/CPU/energia/latência e modo economia adaptativo consentido; arquivo de baseline GNOME/ARANDU.

**R3 — pesquisa avançada:** ECA somente leitura, diferenciação progressiva/reconciliação integrativa com procedência, validação humana e nenhuma migração automática.

## Governança de desenvolvimento

Cada nova função declara explicitamente: **princípio**, **intenção de uso**, **serviço Linux/adaptador**, **permissões necessárias**, **comportamento na ausência do serviço**, **impacto energético**, **teste de regressão** e **ação de reversão**.

Este texto é uma **matriz de trabalho derivada dos documentos recuperados**, sujeita à revisão humana e à validação contra a ontologia canônica.
