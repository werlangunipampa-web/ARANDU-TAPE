# Estado, versões e evidências

**Referência:** candidato à primeira publicação científica, revisão iniciada em 24/11/2026 (Brasília). Não é uma release.

## Identificadores independentes

| Componente | Identificador verificado | Fonte no repositório |
| --- | --- | --- |
| Suíte GNOME | 3.2.3 beta | [instalar-tudo.sh](../ARANDU-SUITE/instalar-tudo.sh) |
| Extensão Confluência | 3.2.3-beta, versão interna 19 | [shell/build.py](../ARANDU-SUITE/Confluencia/shell/build.py) |
| Instalador Confluência | 2.8.2 (legado) | [instalador.py](../ARANDU-SUITE/Confluencia/instalador.py) |
| TOPBAR histórica | 6.6.1.2, versão 6612 | [metadata.json](../ARANDU-SUITE/TOPBAR/arandu-topbar@local/metadata.json) |
| TOPBAR moderna | versão 6613 (experimental) | [metadata.json](../ARANDU-SUITE/TOPBAR/modern/metadata.json) |
| Desktop GTK4 | 0.7.7 | [app.py](../ARANDU-DESKTOP/app.py) |
| Crate Rust local | 0.1.0 | [Cargo.toml](../ARANDU-DESKTOP/rust-core/Cargo.toml) |

Números históricos de scripts, tutoriais e notas não representam a versão global. Não renomear uma versão já distribuída nem inferir que um script local não sincronizado está no repositório. Alça Viva e outras mudanças locais só devem ser anunciadas como entregues quando a implementação correspondente estiver identificada no snapshot público e validada.

## Matriz de compatibilidade

| Ambiente | Estado |
| --- | --- |
| Linux Mint 22.3, GNOME 46/X11 | Referência de testes históricos; validar o candidato atual na máquina |
| GNOME 40–44 | Variante legada Confluência; sem garantia visual |
| GNOME 45–51 | Variante ES modules Confluência; CI constrói 46/47; sem garantia visual em toda a faixa |
| GNOME Wayland | Verificação específica pendente |
| TOPBAR | GNOME 46 histórico; variante moderna experimental com ativação explícita nos demais GNOMEs previstos |
| GTK4 sobre GNOME/Cinnamon | Aplicação independente das APIs do Shell; validar execução real em cada ambiente |
| Sway aninhado | Laboratório opcional iniciado a partir de X11; compositor de terceiros, não compositor ARANDU |
| Login ARANDU/Sway | Ensaio separado; não recomendado como sessão principal antes de validar recuperação |

## Evidência de validação

O PR #3, no head `a6b0c1f27a6f7ac05438dc887e8573b396ae7112`, teve dois workflows bem-sucedidos: [Desktop](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45517623750) e [Suite](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45517623653). O log Desktop registra 100 testes aprovados e triagem de 137 entradas, zero indicadores bloqueantes e dez caminhos para revisão de pesquisa no commit de merge de CI `b9c9d5b78e008639fd0bd4a8b4583fb727d2704b`. Isso vale para aquela execução, não para alterações posteriores. Não comprova ausência de segredos, segurança integral ou funcionamento visual.

## Critérios de atualização

Toda versão candidata precisa de SHA, escopo, testes executados, limitações, instruções e reversão. A release científica só é publicada após revisão de direitos, autorização de divulgação, teste real e CI do candidato. O DOI da versão deve corresponder exatamente ao snapshot depositado.
