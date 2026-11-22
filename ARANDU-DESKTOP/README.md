# ARANDU Desktop 0.5 — janelas reais do Sway, sessão experimental

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
