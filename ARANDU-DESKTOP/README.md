# ARANDU Desktop 0.1 — primeiro protótipo independente

**Desenvolvimento:** Rafhael Brum Werlang  
**Origem:** ARANDU TAPE / Linux Mint / GNOME 46, com preservação da interface existente.

## O que é hoje

Uma **aplicação GTK4 própria** para testar a linguagem visual da Semente, os três Rios (Memória, Abertos, Frequentes), o botão de aplicativos instalados e as informações de autoria. Funciona **sobre** GNOME ou Cinnamon, mas **não depende das APIs internas do GNOME Shell**.

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
