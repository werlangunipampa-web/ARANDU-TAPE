# ARANDU A8.3 — Confluência discreta (compatibilidade GNOME)

**Status:** proposta em desenvolvimento; revisão e validação no GNOME 46 necessárias.

## Motivação

As faixas ornamentadas permanentes dos antigos três Rios competem com a nova Semente, a Opy e os aplicativos. A Ontologia ARANDU não exige que uma relação semântica seja representada por uma estrada visível durante todo o uso.

Na proposta A8.3, os Rios **Memória, Abertos e Frequentes** passam a ser perspectivas contextuais na Opy. Na tela em repouso, só a Semente permanece visível.

## Contrato de continuidade

A extensão histórica `confluencia@arandulab` tem dois papéis:

- a camada gráfica antiga, com faixas, medalhões e Semente;
- o serviço D-Bus `org.arandulab.Tape.Windows1`, que fornece `Snapshot` à ponte GNOME → Rust A5.

**A8.3 não pode desabilitar o serviço somente para eliminar os desenhos.**

Este patch muda unicamente a atribuição `this.root.visible` da extensão histórica, condicionando-a ao ambiente `ARANDU_SESSION=1`. No GNOME regular, a condição mantém o comportamento existente. Na sessão ARANDU, o ator raiz é oculto, mas instância, eventos, D-Bus, `Snapshot` e configurações permanecem ativos.

Esse controle de visibilidade é a primeira etapa de uma futura separação formal entre **adaptação de dados** e **representação visual**. Não é, por si só, um compositor ARANDU independente.

## Instalação e recuperação

A instalação local experimental usa o script reversível `arandu_a83_rios_discretos.py`, entregue na conversa, com `--test`, `--check`, `--apply` e `--restore`. O instalador verifica o padrão exato da versão instalada antes de editar o arquivo e guarda uma cópia integral com hashes SHA-256.

**Não execute o instalador com sudo.** A edição afeta só a extensão do usuário e requer GNOME 46/X11. Se o código local não corresponder ao padrão esperado, o instalador se recusa a aplicar. O `--restore` pode ser executado também a partir da sessão GNOME normal, como recuperação.

A integração com o núcleo Rust não é alterada por esse patch. As ações reais de janelas (Recolher, Retomar, Imersão, Confluência e Encerrar) serão implementadas em um adaptador específico somente após validar o novo contrato de referências opacas por janela.

## Testes manuais necessários

1. Na sessão ARANDU, conferir que as antigas faixas não aparecem e a Semente A8.2/Opy continua funcionando.
2. Consultar `AssistiveStatus` e executar a ponte GNOME → Rust para verificar que os dados continuam disponíveis.
3. Verificar a troca de áreas de trabalho, a grade de aplicativos, o relógio e Energia.
4. Entrar no GNOME normal e confirmar que o comportamento antigo não foi alterado.
5. Executar `--restore` e confirmar reaparecimento das faixas na sessão ARANDU.

## Filosofia

A relação é maior do que sua representação gráfica. O Rio continua existindo como navegação, memória e retomada de uma atividade, mesmo quando o desenho se recolhe. O usuário é quem decide quando visualizar relações e quando trabalhar com a tela livre.

Documentação relacionada: [ARANDU Core — ADR A8.3](https://github.com/werlangunipampa-web/arandu-core/blob/a8/filosofia-espacos-vivos/docs/design/ADR_A8_3_RIOS_DISCRETOS_ESPACOS_VIVOS.md).
