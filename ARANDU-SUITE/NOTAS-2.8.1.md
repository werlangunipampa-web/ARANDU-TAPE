# ARANDU SUITE 2.8.1 — Repouso dos medalhões

- Os três rios permanecem expandidos até a pessoa recolher pela Semente.
- Medalhões de aplicativos e `?` ficam visualmente em repouso após 7 segundos sem interação.
- Navegação pelo teclado ou pela ponte D-Bus restaura os medalhões e preserva a seleção.
- O botão `?` obedece à preferência persistente `show-help-button`; se foi desligado na 2.8.0, reative-o via menu da Confluência ou pelo GSettings.
- A Semente mantém seu repouso independente de 30 segundos quando os rios estão recolhidos.
- A TOPBAR histórica só é instalada quando ausente; jamais é sobrescrita.
- Extensão oferecida somente para GNOME Shell 40–51. Os builds GNOME 40–44 e 45–51 usam entradas JavaScript distintas. Isso **não constitui certificação** de todas as versões/sessões; testar em X11 e Wayland.
- `floating=false` permite a camada de área de trabalho no GNOME compatível; em certos shells a superfície pode ficar atrás do wallpaper ou de outras camadas. O teste visual é obrigatório.
- Sem ligar microfone ou câmera automaticamente.
