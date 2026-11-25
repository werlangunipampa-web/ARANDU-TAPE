# Semente Adaptativa — sinais nativos GNOME

Revisão experimental, 24/11/2026. Este adaptador não é uma autoridade de privacidade nem um substituto certificado dos indicadores do sistema.

## Implementação

A Semente observa, por sinais de mudança de propriedade, os atores de indicação disponíveis na barra do GNOME. Não abre dispositivos, captura mídia, lê texto de notificações, altera permissões ou cria um processo residente. A etiqueta não é interativa e permanece visível na superfície da Semente enquanto houver sinal reconhecido; impede o repouso visual da Semente. A sessão bloqueada não apresenta a etiqueta. O candidato posterior usa addTopChrome quando a API e o sinal de sessão estão disponíveis, sem região de entrada ou reserva de espaço. A etiqueta fica independente dos Rios, inclusive em tela cheia, em condições normais de sessão; é ocultada na Visão Geral e no bloqueio. Se a API faltar, permanece na camada anterior. A visibilidade efetiva ainda depende de validação real, portanto a barra nativa continua indispensável.

| Sinal | Fonte interna verificada em GNOME 46.0 | Interpretação |
| --- | --- | --- |
| Câmera | quickSettings._camera._indicator | GNOME apresenta sinal de câmera |
| Microfone | quickSettings._volumeInput._indicator | GNOME apresenta sinal de entrada de áudio |
| Gravação GNOME | statusArea.screenRecording | Indicador de screencast nativo visível |
| Captura remota | quickSettings._remoteAccess._indicator | Indicador remoto de gravação visível |
| Compartilhamento | statusArea.screenSharing | Indicador nativo de compartilhamento visível |
| Avisos / Não perturbe | dateMenu._indicator, visibilidade e icon_name | Sinal nativo agregado, sem contagem ou conteúdo |

Não inferir que um dispositivo está desligado a partir de ausência de indicador. Uma fonte inexistente ou incompatível é desconhecida. O indicador de Não perturbe não significa notificação nova. No GNOME 46, o indicador de compartilhamento é deliberadamente limitado ao Wayland; X11 não oferece cobertura completa de compartilhamento. Outras versões/distribuições podem usar propriedades diferentes. Não anunciar suporte universal.

## Aceite

Verificar no GNOME 46 real: ativar/desativar cada fonte por aplicativos de teste consentidos; comparar simultaneamente a indicação nativa com a da Semente; distinguir Não perturbe de avisos; verificar sessão bloqueada, recolhimento, mudança de monitor, sobreposição por janelas e desativação da extensão. Testar ausência de fonte e fallback. Nenhuma captura ou dado real precisa ser compartilhado.

A etiqueta escolhe a posição preferida ou o canto com menor sobreposição à janela focada, com desempate por distância da Semente. Se a janela cobre a área inteira, a etiqueta continua compacta dentro da área útil; não modifica o tamanho ou foco da janela. Reposicionamento por eventos de foco, movimento, tamanho e monitor; sem polling. O arraste e a posição persistida da Semente principal permanecem intactos. A próxima etapa requer validar a camada no Mint, acesso por teclado à Semente e a cobertura dos sinais. Não ocultar a barra nativa com base nesta revisão.

## Referências técnicas

- GNOME Shell 46.0: https://github.com/GNOME/gnome-shell/blob/46.0/js/ui/panel.js
- https://github.com/GNOME/gnome-shell/blob/46.0/js/ui/status/camera.js
- https://github.com/GNOME/gnome-shell/blob/46.0/js/ui/status/volume.js
- https://github.com/GNOME/gnome-shell/blob/46.0/js/ui/status/remoteAccess.js
- https://github.com/GNOME/gnome-shell/blob/46.0/js/ui/dateMenu.js

Referência complementar: https://gjs.guide/extensions/upgrading/gnome-shell-46.html .

As propriedades são internas e não constituem contrato estável entre versões. O código do ARANDU apenas observa valores e não reproduz a implementação do GNOME.

- GNOME Shell 46.0, API de camadas: https://github.com/GNOME/gnome-shell/blob/46.0/js/ui/layout.js
