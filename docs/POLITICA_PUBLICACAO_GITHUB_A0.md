# ARANDU — Política de publicação e continuidade no GitHub

**Marco:** A0 — Fundação do ARANDU Desktop  
**Diretriz:** código e documentação destinados à distribuição devem ser acessíveis publicamente, versionados e auditáveis.

## Repositórios públicos existentes
- [ARANDU TAPE](https://github.com/werlangunipampa-web/ARANDU-TAPE): experiência gráfica, Confluência, Três Rios e documentação de instalação.
- [arandu-core](https://github.com/werlangunipampa-web/arandu-core): núcleo Rust portável, contratos, geometria e testes.

## Procedimento obrigatório para entregas
1. Trabalhar em branch de desenvolvimento; não publicar código não testado na branch principal.
2. Executar testes e revisão de segurança, licenças, privacidade e dados sensíveis.
3. Enviar commits rastreáveis com finalidade, versão e mudanças.
4. Abrir pull request com resultados dos testes e plano de reversão.
5. Após aprovação, integrar na branch principal e, quando apropriado, criar release com notas de versão e verificações de integridade.
6. Conferir se o commit e os artefatos realmente ficaram disponíveis no GitHub. Um arquivo criado apenas na conversa ou máquina local **não** está sincronizado automaticamente.
7. Manter documentação de instalação e changelog coerentes com a versão efetivamente publicada.

## Proteção da Semente e da pesquisa
- Não publicar `seed_id` reais, memória viva, estado interno pessoal, chaves, tokens, registros de usuários, dados privados ou backups.
- Repositórios experimentais privados (G4, ECA, AVE e arquivos históricos) **não** devem ser tornados públicos automaticamente.
- Publicar apenas especificações, exemplos sintéticos e implementações explicitamente revisadas para divulgação.
- A integração gráfica deve consumir interfaces autorizadas, inicialmente somente leitura, e nunca importar estado vivo da Semente para repositórios públicos.
- A publicação de conceitos da ontologia exige comparação com os manifestos originais e revisão de procedência e direitos culturais.
- A licença declarada de cada componente deve ser conferida; acesso público não substitui uma licença de uso e redistribuição.

## Meta operacional
GitHub como referência pública para código distribuível, histórico de decisões, testes e releases. Atualizações devem ocorrer em cada marco validado, não em intervalos automáticos que publiquem conteúdo sem revisão.

**Estado:** esta política documenta o processo; não constitui, por si só, automação de sincronização do computador com GitHub.
