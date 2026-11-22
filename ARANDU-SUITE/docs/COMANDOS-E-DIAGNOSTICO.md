# Comandos e diagnóstico

## Atalhos

`Super+Alt+1/2/3`: Memória/Abertos/Frequentes; `Super+Alt+←/→`: navegar; `Super+Alt+Enter`: ativar; `Super+Alt+0`: cancelar; `Super+Shift+T`: mapa; `Super+Alt+B`: restaurar painel quando compatível.

## Comandos de texto assistivos

```bash
python3 arandu-assistivo.py memória --simular
python3 arandu-assistivo.py abertos
python3 arandu-assistivo.py próximo
python3 arandu-assistivo.py anterior
python3 arandu-assistivo.py abrir
```

As palavras não são capturadas do microfone: devem ser passadas explicitamente pelo usuário ou por um futuro sensor. O vocabulário é restrito; não permite execução arbitrária de comandos de sistema.

## Estado da extensão

```bash
gnome-extensions info confluencia@arandulab
```

## Diagnóstico D-Bus

```bash
gdbus introspect --session --dest org.gnome.Shell \
  --object-path /org/arandulab/Tape/Windows

gdbus call --session --dest org.gnome.Shell \
  --object-path /org/arandulab/Tape/Windows \
  --method org.arandulab.Tape.Windows1.AssistiveCommand 'river:open'
```

Se responder `(true,)`, o comando foi recebido, mas verifique se a seleção mudou visualmente. Caso rios sobreponham uma janela, confira a preferência `floating` e reinicie a sessão, sem presumir que a correção seja universal.
