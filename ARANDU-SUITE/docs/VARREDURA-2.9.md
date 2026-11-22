# ARANDU TAPE 2.9.0 beta — Varredura assistiva

## Objetivo

A varredura opcional percorre **medalhões de aplicativos** sem mouse. É uma etapa para pessoas que utilizam um único acionador (tecla, botão adaptado ou dispositivo capaz de emitir uma tecla).

**Importante:** nenhum aplicativo é aberto pelo temporizador. A abertura acontece somente com uma confirmação explícita.

## Como funciona

1. Abra os rios e selecione o rio desejado (Memória, Abertos ou Frequentes).
2. Pressione **Super + Alt + Espaço** para iniciar a varredura; o medalhão selecionado ganha contorno dourado.
3. O foco avança automaticamente a cada 3,5 segundos, sem abrir aplicativos.
4. Pressione **Super + Alt + Espaço** novamente para parar e ativar o medalhão selecionado.
5. Use **Super + Alt + 0** para cancelar a seleção e parar a varredura.

A função também está no menu da Confluência da barra superior, em *Varredura assistiva: iniciar/parar*. O menu para apenas a varredura; a confirmação utiliza a combinação de teclas ou a ponte assistiva.

## Ponte assistiva D-Bus

Os comandos continuam restritos a um vocabulário fechado:

- `scan:start` — começa a percorrer os medalhões.
- `scan:stop` — para sem abrir aplicativo.
- `scan:switch` — inicia, ou confirma a seleção quando a varredura está ativa.

Exemplo para testar:

```bash
gdbus call --session \
  --dest org.gnome.Shell \
  --object-path /org/arandulab/Tape/Windows \
  --method org.arandulab.Tape.Windows1.AssistiveCommand \
  'scan:start'
```

Para cancelar sem abrir:

```bash
gdbus call --session \
  --dest org.gnome.Shell \
  --object-path /org/arandulab/Tape/Windows \
  --method org.arandulab.Tape.Windows1.AssistiveCommand \
  'scan:stop'
```

## Velocidade adaptável

O intervalo pode ser ajustado de 2 a 5 segundos usando GSettings, por exemplo 5 segundos:

```bash
SCHEMA_DIR="$HOME/.local/share/gnome-shell/extensions/confluencia@arandulab/schemas"
SCHEMA="org.gnome.shell.extensions.arandu-confluencia"
gsettings --schemadir "$SCHEMA_DIR" set "$SCHEMA" scan-interval-ms 5000
```

A nova velocidade é aplicada na próxima vez que a varredura é iniciada. Evite intervalos muito rápidos sem calibração com o usuário.

## Limitações e segurança

- Não liga câmera nem microfone.
- Não é reconhecimento de voz, gestos ou cabeça.
- Não substitui testes com usuários de tecnologia assistiva.
- A varredura é desligada ao recolher os rios, cancelar seleção ou desativar a extensão.
- Em sessão GNOME bloqueada, os comandos não devem operar.
- Compatibilidade com GNOME/Wayland precisa de testes de campo.

## Atualização e retorno

Para instalar ou atualizar, consulte [INSTALAR.md](../../INSTALAR.md) e use o instalador do repositório. A TOPBAR histórica não deve ser modificada. Teste primeiro em GNOME 46/X11.

## Diagnóstico de estado — complemento 3.0

A ponte D-Bus oferece `AssistiveStatus`, operação **somente leitura**.
Ela permite inspecionar a seleção sem abrir nem fechar aplicativos.

```bash
gdbus call --session \
  --dest org.gnome.Shell \
  --object-path /org/arandulab/Tape/Windows \
  --method org.arandulab.Tape.Windows1.AssistiveStatus
```

O resultado é uma string JSON com `scanning`, `river`, `index`,
`selected` e `intervalMs`. Quando a sessão está bloqueada, retorna apenas
`available:false` e `scanning:false`, sem expor seleção ou janelas.

**Teste da confirmação:** selecione primeiro um aplicativo de teste, inicie
`scan:start` e, quando chegar ao medalhão desejado, use `scan:switch`.
Depois consulte `AssistiveStatus`, confirme `scanning:false` e observe se
a janela correta assumiu o foco. A resposta `true` não comprova,
isoladamente, que o aplicativo ficou em primeiro plano.
