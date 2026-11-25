# ARANDU TAPE

[English](README.en.md)

**Navegação gráfica adaptativa para Linux, com foco em acessibilidade, autonomia e aprendizagem significativa.**

O ARANDU TAPE é um projeto experimental que organiza a interação entre aplicativos e janelas por uma **Semente central** e três **Rios**: Memória (itens recentes), Abertos (janelas da sessão) e Frequentes (aplicativos usados com frequência). Os medalhões oferecem pontos de navegação por ponteiro e teclado. O projeto busca uma interface discreta, reversível e adaptável às necessidades humanas.

**Estado:** código de desenvolvimento público; não é uma distribuição estável, um compositor próprio ou uma tecnologia assistiva validada para uso autônomo. Não há release científica ou DOI confirmado neste momento.

## Componentes e versões

| Componente | Identificação no código | Escopo |
| --- | --- | --- |
| ARANDU SUITE / Confluência | 3.2.3-beta | Extensão e aplicação GTK3 para GNOME Shell |
| ARANDU TOPBAR | 6.6.1.2 (6612); variante experimental 6613 | Identidade visual do painel |
| ARANDU Desktop | 0.7.7 | Protótipo GTK4; laboratório opcional com Sway |
| Instalador Confluência | 2.8.2 (identificador legado) | Instalação no perfil de usuário |

As versões são independentes. A versão do instalador e os números antigos em notas históricas não identificam a versão atual de todos os componentes. Uma futura release científica identificará o snapshot completo pelo commit Git. Consulte a [matriz de versões e evidências](docs/ESTADO_E_VERSOES.md).

## Começar com segurança

- **GNOME / Linux Mint:** [guia de instalação e recuperação](INSTALAR.md) e [manual Confluência](ARANDU-SUITE/README.md).
- **Protótipo GTK4:** [manual ARANDU Desktop](ARANDU-DESKTOP/README.md). A execução normal não substitui a sessão gráfica.
- **Laboratório Sway:** [guia experimental](ARANDU-DESKTOP/session/README.md). Testar aninhado antes de considerar o login experimental.

Prefira um clone Git para testes completos e rastreabilidade. O ZIP de código-fonte não equivale a um instalador assinado. Use os comandos de pré-verificação e backup antes de instalar; não execute o instalador de usuário com sudo.

## Documentação e pesquisa

- [Índice de documentação](docs/README.md)
- [Design Core e identidade visual](docs/DESIGN_CORE.md)
- [Fundamentação filosófica e pedagógica pública](docs/FUNDAMENTACAO_PUBLICA.md)
- [Arquitetura e acessibilidade](ARANDU-SUITE/docs/ARQUITETURA-E-ACESSIBILIDADE.md)
- [Guia de acessibilidade](docs/ACESSIBILIDADE.md)
- [Privacidade](docs/PRIVACIDADE.md) · [Segurança](SECURITY.md) · [Contribuição](CONTRIBUTING.md)
- [Histórico de mudanças](CHANGELOG.md)
- [Roteiro de evolução](ARANDU-SUITE/docs/ROADMAP.md)
- [Política de publicação científica e Zenodo](docs/PUBLICACAO_CIENTIFICA_ZENODO.md)

A interface gráfica pública deve funcionar sem depender dos núcleos de pesquisa privados. O desenvolvimento é orientado por acessibilidade, privacidade, adaptação reversível e aprendizagem significativa. Integrações experimentais não implicam validação científica do motor cognitivo.

## Citação, direitos e colaboração

Metadados de citação: [CITATION.cff](CITATION.cff). Desenvolvimento identificado no projeto: Rafhael Brum Werlang; autoria, contribuições e titularidade permanecem sujeitos à revisão documental. Ao citar o código em desenvolvimento, identifique o commit consultado. Após a publicação científica, prefira o DOI da versão arquivada.

A disponibilidade pública do código não constitui concessão automática de licença. Licenciamento definitivo e direitos dos recursos incorporados estão em revisão. Não publique dados pessoais, credenciais, estado vivo ou conteúdo dos núcleos privados. Veja a [auditoria](docs/AUDITORIA_PRELIMINAR_DOI.md).

## Projeto relacionado

[ARANDU WEB](https://github.com/werlangunipampa-web/ARANDU-WEB) — projeto separado para Firefox.

> Tecnologia que se adapta às possibilidades humanas.
