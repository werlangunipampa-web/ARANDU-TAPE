# ARANDU Updates — ambiente isolado de atualização

Esta pasta contém apenas o **código e as especificações do mecanismo de atualização**.
Não é uma fonte de pacotes instaláveis e não deve receber builds finais.

## Separação de responsabilidades
- `client/`: cliente local de consulta somente leitura.
- `systemd/`: unidades modelo para futura integração ao início da sessão; não habilitadas.
- `PLANO-SEGURANCA.md`: pré-requisitos de segurança e testes.
- Pacotes finais: **GitHub Releases**, após homologação, assinatura e publicação formal.
- Protótipos: ramificações de desenvolvimento; não usar `main` como canal de entrega de pacotes.

## Política atual
Consulta ao iniciar, aviso após validação de versão instalada (ainda pendente), sem download ou instalação.
O protótipo ainda não está instalado em nenhum computador por esta alteração no GitHub.
