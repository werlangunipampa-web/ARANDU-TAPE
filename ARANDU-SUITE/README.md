# ARANDU TAPE — Confluência 3.2.3-beta (prévia experimental)

**Um ambiente gráfico de navegação que se adapta às possibilidades humanas.**

O **ARANDU TAPE** é um projeto experimental de interface gráfica para o **GNOME Shell** que organiza a navegação por aplicativos e janelas em torno de uma **Semente central** e três **rios visuais**. Pretende facilitar o uso cotidiano do Linux e oferecer, progressivamente, formas de interação para pessoas com diferentes limitações motoras ou comunicativas.

> **Estado do projeto:** beta experimental. A interface gráfica e uma ponte local de comandos estão implementadas; reconhecimento contínuo de voz, gestos com as mãos e rastreamento de cabeça ainda **não estão integrados** nesta versão. Não é uma solução assistiva validada para uso sem suporte.

## Como funciona

- **Memória:** itens recentes da sessão.
- **Abertos:** janelas e aplicativos abertos.
- **Frequentes:** aplicativos acessados com maior frequência.
- **Semente:** expande e recolhe os rios por ação explícita.
- **Medalhões:** representam os itens navegáveis. Selecionar um rio realça seu caminho; navegar realça o medalhão escolhido; ativá-lo solicita abrir ou focar o aplicativo.

### Repouso visual — Semente 7s / ajuda 6s

Após **6 segundos** sem interação, o medalhão de ajuda `?` perde visibilidade; após **7 segundos**, a Semente central reduz sua opacidade a cerca de **12%**. O repouso visual não deve ser confundido com o temporizador de navegação: no candidato, `navigation-idle-ms` tem padrão de 0 s, e o menu oferece 0/10/30/60 s (0 = nunca recolher por tempo). Preferências explícitas já salvas permanecem. A saída do modo de navegação ao retornar ao aplicativo continua preservada. A correção do padrão segue o [Design Core](../docs/DESIGN_CORE.md) e requer validação real. A varredura assistiva suspende esse temporizador. A ajuda pode ser solicitada pelo menu ARANDU da barra superior. A intenção é manter os controles disponíveis sem poluir a área de trabalho.

As janelas de trabalho devem ficar à frente dos rios com `floating=false`; validar o posicionamento na versão de GNOME usada. A TOPBAR histórica é um componente ornamental distinto, preservado pelo instalador. A suíte possui uma variante TOPBAR experimental para outros GNOMEs modernos, sem substituir a versão 46 em uso.

## Instalação

A partir de um clone Git ou ZIP do código-fonte, entre na pasta `ARANDU-SUITE`. Ainda não há release científica confirmada. O instalador exibe um identificador legado 2.8.2; a extensão usa 3.2.3-beta.

```bash
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
bash instalar-tudo.sh
```

Não executar com `sudo`. O instalador faz backup da Confluência instalada e não substitui a TOPBAR histórica. Na sessão GNOME X11 pode ser necessário salvar o trabalho e reiniciar o GNOME Shell com `Alt+F2`, `r`, Enter; no Wayland, normalmente é necessário encerrar a sessão e entrar novamente. Veja [instalação](docs/INSTALACAO.md).

## Painel de acessibilidade na Semente (introduzido na 3.1 beta)

Clique com o botão direito na **Semente** ou abra **ARANDU TAPE → Acessibilidade · configurar na Semente**. Ajuste velocidade da varredura (2 / 3,5 / 5 s), tamanho dos medalhões (85% / 100% / 120%), alto contraste, acionador (Super+Alt+Espaço ou Super+Alt+S) e recuperação da barra GNOME. Existe uma ação para restaurar os padrões seguros. No candidato, o painel também mostra data/hora e a preferência GNOME de histórico sob demanda, e abre os menus nativos de avisos/calendário e controles do sistema quando disponíveis. A ocultação pela Confluência está suspensa até validar indicadores equivalentes na Semente; outras extensões podem controlar a barra de modo independente.

Este painel é uma **prévia experimental**, ainda não validada visualmente na máquina de referência. Veja [manual de acessibilidade](docs/PAINEL-ACESSIBILIDADE.md).

## Navegação por teclado

| Atalho | Ação |
|---|---|
| `Super+Alt+1` | Rio Memória |
| `Super+Alt+2` | Rio Abertos |
| `Super+Alt+3` | Rio Frequentes |
| `Super+Alt+← / →` | Medalhão anterior / próximo |
| `Super+Alt+Enter` | Ativar medalhão |
| `Super+Alt+0` | Limpar seleção |
| `Super+Shift+T` | Abrir o aplicativo TAPE |
| `Super+Alt+B` | Recuperar a barra superior (quando compatível) |
| `Super+Alt+Espaço` | Iniciar varredura / confirmar medalhão (experimental) |

As setas e Enter simples só atuam quando um medalhão ARANDU está com o foco; não devem interceptar a digitação em outros programas.

## Ponte assistiva (experimental)

A Confluência expõe o método D-Bus `org.arandulab.Tape.Windows1.AssistiveCommand`, com vocabulário limitado. O utilitário `arandu-assistivo.py` transforma textos explícitos em comandos de navegação **sem capturar áudio ou vídeo**:

```bash
python3 arandu-assistivo.py memória --simular
python3 arandu-assistivo.py abertos
python3 arandu-assistivo.py próximo
python3 arandu-assistivo.py abrir
```

Um retorno `(true,)` confirma aceitação do comando pela extensão, **não comprova por si só que uma janela foi ativada**. Veja [arquitetura e acessibilidade](docs/ARQUITETURA-E-ACESSIBILIDADE.md).

## Compatibilidade e limitações

- A Confluência possui variantes de implementação para **GNOME 40–44** e **GNOME 45–51**, com validação automatizada de código. Isso **não comprova** funcionamento visual em todas as versões, distribuições ou sessões X11/Wayland.
- Os testes reais compartilhados até agora ocorreram no **Linux Mint 22.3 / GNOME 46 / X11**.
- A **ARANDU TOPBAR v6.6.1.2** é preservada no GNOME 46. A variante experimental para GNOME 45, 47–51 exige habilitação explícita e testes; veja [TOPBAR multiversão](docs/TOPBAR-MULTIGNOME-3.0.md).
- **Varredura por uma tecla** foi adicionada em caráter experimental, desligada por padrão, com confirmação explícita para ativar um programa. Reconhecimento de voz em tempo real, gestos de mãos, movimentos de cabeça e controle integral de outros aplicativos ainda não estão entregues.
- Para um sistema assistivo confiável, serão necessários calibração individual, confirmação configurável, mecanismos de pausa e testes com pessoas usuárias.

## Documentação

- [Instalação, verificação e recuperação](docs/INSTALACAO.md)
- [Arquitetura e acessibilidade](docs/ARQUITETURA-E-ACESSIBILIDADE.md)
- [Guia de comandos e solução de problemas](docs/COMANDOS-E-DIAGNOSTICO.md)
- [Estado atual e roteiro de desenvolvimento](docs/ROADMAP.md)
- [Varredura assistiva 2.9](docs/VARREDURA-2.9.md)
- [Instalador unificado e TOPBAR multiversão](docs/TOPBAR-MULTIGNOME-3.0.md)
- [Notas da versão 2.8.3](NOTAS-2.8.3.md)

## Autoria e colaboração

Projeto em desenvolvimento no ecossistema ARANDU. Antes de aceitar contribuições externas, definir licença, diretrizes de contribuição e política de privacidade. **Não presumir licença de código aberto apenas por hospedar o código no GitHub.**


Para distinguir versões, evidências e marcos futuros, consulte [estado dos componentes](../docs/ESTADO_E_VERSOES.md). Para citar e distribuir, siga a [política científica](../docs/PUBLICACAO_CIENTIFICA_ZENODO.md).
