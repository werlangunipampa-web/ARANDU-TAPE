# ARANDU Update v0.1 — Prévia de consulta

**Status:** protótipo em `feature/arandu-update-readonly`, ainda não homologado. Não representa versão final.

## Estrutura
- `client/arandu_update_check.py`: consulta metadados de release estável no GitHub.
- `client/arandu_update_app.py`: aplicativo GTK 3 “ARANDU Atualizações”; botão “Verificar agora”.
- `client/arandu_update_startup.py`: consulta ao iniciar a sessão e grava estado somente em `~/.cache/arandu/updates/status.json`.
- `install-preview.sh`: copia os arquivos apenas para o perfil do usuário; cria lançador de aplicativo e entrada XDG Autostart.
- `systemd/`: modelo alternativo **não habilitado**; não utilizar junto com XDG Autostart.
- `PLANO-SEGURANCA.md`: requisitos para futuras operações de instalação.

## O que funciona
Consulta manual na central e verificação silenciosa ao iniciar a sessão **depois** da instalação da prévia. Consulta offline falha sem travar login. Não requer sudo.

## O que NÃO funciona ainda
- Identificar uma atualização realmente aplicável (falta inventário da versão instalada e assinatura de manifesto).
- Notificar na Semente ou enviar atualização à interface ARANDU.
- Baixar, executar ou instalar pacotes; rollback permanece apenas planejado.

Mesmo que seja encontrada uma release estável, não será anunciada como atualização disponível.
A publicação de pacotes finais continuará exclusivamente nas GitHub Releases, após homologação.

## Instalar a prévia a partir da raiz do checkout
```bash
bash updates/install-preview.sh
```
Requer Linux com Python 3, GTK 3 e `python3-gi`. Inspecione o código antes de executar. Não execute como root.

## Remoção (somente componentes específicos)
```bash
rm -f ~/.config/autostart/arandu-update-check.desktop
rm -f ~/.local/share/applications/arandu-update.desktop
rm -f ~/.local/bin/arandu-update
```
A pasta `~/.local/share/arandu/updates` e o cache podem ser removidos separadamente após confirmar que não há outros componentes dependentes.
