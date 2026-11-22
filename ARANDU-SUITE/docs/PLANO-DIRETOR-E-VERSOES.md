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
