# ARANDU SUITE 2.8 — Ponte multimodal experimental

Esta atualização introduz `AssistiveCommand` no serviço D-Bus da Confluência, mantendo a mesma seleção visual dos rios e medalhões. Não instala capturadores automáticos de câmera ou microfone.

## Contrato de comandos

`river:memory`, `river:open`, `river:frequent`, `node:next`, `node:previous`, `node:activate`, `node:cancel`, `seed:expand`, `seed:collapse`, `seed:toggle`.

O programa `arandu-assistivo.py` mapeia textos curtos em português para essas ações. Por exemplo:

```bash
python3 arandu-assistivo.py memória --simular
python3 arandu-assistivo.py abertos
python3 arandu-assistivo.py próximo
python3 arandu-assistivo.py abrir
```

A execução real pressupõe a extensão Confluência 2.8 ACTIVE na sessão GNOME. Este programa é uma *ponte de comandos*, não um reconhecedor de fala. Um futuro reconhecedor de voz local poderá enviar textos confirmados a esta ponte; o ARANDU HEAD deverá enviar direções calibradas ao mesmo contrato. Entrada desconhecida é rejeitada. Não há execução arbitrária de programas por textos externos.

## Limitações

- A captura de voz, o rastreamento de cabeça e mãos, varredura automática, controle completo dentro de outros aplicativos e testes com usuários ainda não foram integrados.
- O teste D-Bus em GNOME real e a compatibilidade Wayland são pendentes.
- O reconhecimento de comandos por voz não deve ativar aplicativos involuntariamente. Recomenda-se uma etapa de confirmação configurável.
- TOPBAR histórica preservada; não instalar com sudo.

## Segurança

Câmera e microfone permanecem desligados por padrão. O componente não coleta nem transmite frames ou áudios. Fazer backup e testar a partir da Confluência já funcional.
