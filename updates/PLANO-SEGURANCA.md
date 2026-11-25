# ARANDU Update — fase 0 (consulta apenas)

**Status:** protótipo não implantado. Este conteúdo está na branch `feature/arandu-update-readonly`, não representa uma versão final. Nenhuma instalação está habilitada.

## Contrato
- Fonte fixa: API HTTPS de **releases/latest** do repositório `werlangunipampa-web/ARANDU-TAPE`.
- A consulta inicia com a sessão gráfica **apenas depois** da instalação e habilitação explícitas do serviço de usuário.
- Um resultado `stable_release_found` é **informativo**, não prova de autenticidade do pacote nem de compatibilidade com a máquina.
- Não usar branches, commits, ZIP do código ou prereleases como atualizações finais.
- Não baixar, extrair, executar nem substituir arquivos na fase 0.
- Não executar como root; nunca solicitar sudo; falha de rede não pode bloquear o login.
- A interface da Semente deve consumir a saída JSON e exibir aviso **apenas após** comparar uma versão local confiável com a tag remota. Esta integração ainda não foi implementada.

## Arquivos
| Arquivo | Papel |
| --- | --- |
| `updates/client/arandu_update_check.py` | Consultar metadados de release estável e emitir JSON; não instala |
| `updates/systemd/arandu-update-check.service` | Modelo de execução única em sessão gráfica; **desabilitado por padrão** |
| `updates/PLANO-SEGURANCA.md` | Critérios obrigatórios para habilitar download/instalação |

## Estados da saída
- `stable_release_found`: existe release não-draft e não-prerelease, com tag bem formada; ainda **não** é oferta validada de atualização.
- `no_stable_release`: dados retornados não descrevem release estável.
- `unavailable`: falha de rede, esquema de metadados ou validação; não tomar ação.

## Portas de segurança para a próxima etapa
1. Inventariar empacotamento real, versões instaladas, dependências, GNOME/X11/Wayland e componentes.
2. Criar um manifesto versionado e **assinado** com chaves de distribuição previamente confiadas, versão mínima e máxima compatíveis, identificador exato do pacote, URL fixa no repositório oficial e SHA-256; verificar assinatura e hash (hash isolado não autentica editor).
3. Rejeitar downgrade, caminho fora da área permitida, symlinks, arquivos com permissões perigosas, arquivos extras, travessia de diretórios e pacotes excessivos.
4. Preparar backup atômico, teste de instalação, rollback e registro auditável; não quebrar login/sessão na falha.
5. Exigir aprovação explícita do usuário para instalação; nunca usar scripts remotos via pipe ou instalar silenciosamente.
6. Testes positivos/negativos: offline, rate limit, timeout, JSON malformado, release beta, assinatura inválida, hash inválido, versão incompatível, rollback, falha de energia e sessão sem privilégios.
7. Só então integrar aviso acessível à Semente; não expor controles de instalação antes dessas verificações.

**Observação:** o README principal descreve a Suite 2.8.3 beta; não presumir que existe release final instalável.
