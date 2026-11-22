# ARANDU TAPE 🌿

**Ambiente gráfico de navegação adaptativa para GNOME Linux.**

O ARANDU TAPE é um projeto experimental que organiza a navegação entre aplicativos e janelas em torno de uma **Semente central** e três **rios visuais**:

- **Memória:** aplicativos e itens recentes
- **Abertos:** janelas em execução
- **Frequentes:** aplicativos usados com frequência

Cada rio possui medalhões selecionáveis. O objetivo é desenvolver um ambiente visual limpo, com diferentes formas de controle para pessoas com variadas capacidades motoras e comunicativas.

## Versão atual: ARANDU SUITE 2.8.3 (beta)

- Semente expande/recolhe os rios por ação deliberada
- Semente central entra em repouso visual após **7 segundos**
- Medalhão de ajuda `?` entra em repouso após **6 segundos**
- Rios e medalhões de aplicativos continuam visíveis enquanto expandidos
- Seleção de rios e medalhões por teclado
- Ponte local de comandos assistivos via D-Bus
- Instalador Linux com pré-verificação, verificação e backups
- TOPBAR histórica tratada como componente separado, preservada pelo instalador

**Limitações:** voz contínua, rastreamento da cabeça/pescoço, gestos de mão e controle multimodal completo ainda não estão integrados nem validados para uso assistivo autônomo. A compatibilidade gráfica entre versões GNOME e entre X11/Wayland precisa de testes.

## Instalação de desenvolvimento

Com o pacote-fonte ARANDU SUITE 2.8.3 disponível, entre na pasta `ARANDU-SUITE` e execute:

```bash
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
bash instalar-tudo.sh
```

Não execute com `sudo`. Em GNOME X11, salve os trabalhos e reinicie o Shell com `Alt+F2`, `r`, Enter. No Wayland, reinicie a sessão.

> O código e instalador serão sincronizados com este repositório. Até lá, este README é a apresentação inicial do projeto, não uma distribuição instalável pelo GitHub.

## Código aberto e direitos

Objetivo: distribuição pública de código-fonte. Antes de conceder uma licença abrangente ao pacote completo, devem ser verificadas a autoria e as licenças dos componentes gráficos e da TOPBAR incorporados.

## Projeto relacionado

[ARANDU WEB](https://github.com/werlangunipampa-web/ARANDU-WEB) — extensão acessível para Firefox.

> Tecnologia que se adapta às possibilidades humanas.
