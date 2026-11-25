# Contribuir com ARANDU TAPE

A colaboração pública está em preparação. A licença geral e titularidade ainda precisam ser aprovadas; este guia não concede licença nem estabelece CLA/DCO. Até essa definição, prefira issues com sugestões e propostas sem código de terceiros. Não enviar material cuja redistribuição não esteja autorizada.

## Escopo

A interface gráfica pública, acessibilidade, documentação, testes e adaptadores revisados são candidatos à colaboração. Núcleos cognitivos experimentais privados, dados, credenciais e estado vivo não são parte do fluxo público. Não publicar contratos internos adicionais sem autorização.

## Fluxo técnico proposto

1. Descrever a finalidade humana, problema reproduzível, alternativa e impacto no Design Core.
2. Trabalhar em branch isolada a partir de um commit conhecido, sem alterações locais não relacionadas.
3. Registrar procedência de código, recursos gráficos e dependências; distinguir material próprio, assistido por IA e de terceiros quando conhecido. Preservar avisos. Não declarar titularidade por inferência.
4. Testar em clone Git, sem instalar serviços ou alterar sessão padrão automaticamente.
5. Abrir PR em rascunho com escopo, evidências, limitações, impacto de privacidade/acessibilidade, recuperação e versões. Marcar revisão somente após conferir.
6. Integrar após aprovação. Merge não autoriza release científica.

## Verificações

Na raiz do clone, usando as dependências apropriadas:

```bash
python3 -m compileall -q ARANDU-DESKTOP
python3 -m unittest discover -s ARANDU-DESKTOP/tests -v
python3 ARANDU-SUITE/verificar.py
python3 scripts/auditar-snapshot.py --ref HEAD
```

Para Rust, se disponível: cargo test --manifest-path ARANDU-DESKTOP/rust-core/Cargo.toml. O scanner inspeciona o commit, não mudanças ainda não commitadas. Testes reais GNOME, GTK e Sway são separados de testes de contrato.

Não afirmar desempenho superior sem comparação controlada; não declarar uma funcionalidade implementada apenas porque existe um plano ou teste simulado. Respeitar os limites culturais, evitar reproduzir materiais restritos e não tratar grafismos como autenticamente tradicionais sem evidência.

Referências: [Design Core](docs/DESIGN_CORE.md), [fundamentação](docs/FUNDAMENTACAO_PUBLICA.md), [segurança](SECURITY.md), [estado](docs/ESTADO_E_VERSOES.md).
