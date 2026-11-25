# Segurança / Security

## Estado do projeto

ARANDU TAPE é experimental, sem release científica aprovada ou compromisso de manutenção de versões estáveis. Use em ambiente de teste e preserve acesso ao desktop habitual. Não há SLA ou promessa de suporte a uma versão específica.

## Relato responsável

Não publique vulnerabilidades exploráveis, tokens, logs sensíveis, capturas ou conteúdo privado em issues públicas. Se a opção Security → Report a vulnerability estiver habilitada no GitHub, use-a. Caso contrário, solicite um canal privado aos mantenedores sem revelar os detalhes em público. A disponibilidade de recebimento privado ainda deve ser confirmada.

Inclua componente, SHA, versão do sistema, tipo de sessão, impacto, passos mínimos em ambiente de teste, resultado esperado e evidência sanitizada. Não teste contra instalações alheias sem autorização. Não inclua dados de usuários ou cópias dos núcleos de pesquisa.

## Princípios técnicos

- Sem privilégios administrativos para instalação de extensões de usuário; ações administrativas separadas e explícitas.
- Nenhuma execução arbitrária de código proveniente de modelos generativos ou arquivos de intercâmbio.
- Credenciais fora do Git; se expostas, revogar e rotacionar no fornecedor. Não presumir que apagar um arquivo elimina o histórico.
- Revisar árvore completa do candidato com python3 scripts/auditar-snapshot.py --ref HEAD em clone Git. A triagem é limitada a padrões e não substitui análise de dependências, histórico e código.
- Não publicar release automaticamente a partir de main. Exigir revisão humana, licença, autorização e teste do SHA candidato.
- Preservar rollback; testar instalação, desativação e recuperação antes de alterar sessão padrão.

## Security reporting (English)

This is experimental software, not a supported stable distribution. Please use GitHub private vulnerability reporting if enabled. Otherwise request a private contact channel without posting vulnerability details, secrets, or personal data publicly. Include the component, commit, environment, impact and minimal sanitized reproduction. Do not access systems without authorization. No response-time commitment is currently established.

See [privacy](docs/PRIVACIDADE.md) and [scientific release policy](docs/PUBLICACAO_CIENTIFICA_ZENODO.md).
