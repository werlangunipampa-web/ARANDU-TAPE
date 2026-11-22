# Relatório de validação manual — ARANDU TAPE

**Ambiente relatado:** Linux Mint 22.3, GNOME Shell 46.0, X11.
**Componentes:** Confluência 2.9.0 (14) e TOPBAR histórica 6.6.1.2 (6612).
**Condição:** Testes manuais relatados pelo usuário do projeto; não substituem auditoria independente.

## Resultados confirmados na máquina de referência

- `gnome-extensions info`: ambas extensões marcadas `ACTIVE`.
- Ponte D-Bus: `river:open`, `scan:start` e `scan:stop` retornaram `(true,)`.
- O usuário observou o contorno dourado percorrendo os medalhões automaticamente.
- O usuário confirmou que a segunda pressão do acionador de teclado parou a varredura e abriu a janela destacada.
- `AssistiveStatus` passou a retornar o estado JSON esperado, incluindo `available:true`, `scanning:false` e `intervalMs:3500`.
- `panel-mode visible` foi confirmado após ajuste manual.

## Limitações

- Não há validação de dispositivos acionadores físicos nem estudos com pessoas com deficiência.
- A varredura foi observada somente no GNOME 46/X11, não em outras versões ou Wayland.
- A TOPBAR moderna 45–51 é experimental; a TOPBAR 6.6.1.2 é declarada para GNOME 46.
- O modo da barra mudou entre `auto`, `hidden` e `visible` em testes anteriores; a origem das mudanças ainda não foi confirmada.
- A janela do terminal fechou inesperadamente durante uma instalação; não foi possível determinar a causa.
- Para nova máquina, executar preflight e verificação estática antes de instalar.

## Instalação em outro computador

```bash
git clone https://github.com/werlangunipampa-web/ARANDU-TAPE.git
cd ARANDU-TAPE/ARANDU-SUITE
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
```

Somente em sessão com GNOME 46 e após revisar os avisos do preflight:

```bash
bash instalar-tudo.sh
```

A instalação destina-se ao usuário atual; não executar com `sudo`. Depois de salvar os trabalhos, iniciar uma nova sessão GNOME e conferir `bash instalar-tudo.sh --status`.

A versão publicada no repositório `main` é um estado de desenvolvimento; conferir o commit antes de copiar instruções ou atribuir numeração de versão estável.
