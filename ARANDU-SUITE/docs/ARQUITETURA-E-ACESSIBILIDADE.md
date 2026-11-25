# Arquitetura e visão assistiva

## Princípio

**Adaptar o ambiente gráfico às capacidades de cada pessoa**, não exigir que todas naveguem de uma única maneira.

## Componentes atuais

1. **Confluência / GNOME Shell:** desenha Semente, rios Memória, Abertos e Frequentes, medalhões, foco visual e ativação.
2. **ARANDU TAPE / GTK:** aplicativo complementar de navegação.
3. **Ponte assistiva local:** traduz um conjunto limitado de comandos explícitos para D-Bus na sessão GNOME.
4. **TOPBAR histórica:** ornamento opcional separado, preservado.

O método D-Bus `org.arandulab.Tape.Windows1.AssistiveCommand` aceita tokens como `river:memory`, `river:open`, `river:frequent`, `node:next`, `node:previous`, `node:activate`, `node:cancel`, `seed:expand`, `seed:collapse` e `seed:toggle`. A interface devolve um booleano de aceitação; isso não garante sucesso do efeito final.

## Modalidades experimentais e planejadas

- **Voz:** o mapa GTK3 possui reconhecimento local experimental de frase curta por Vosk, sob ação explícita e com modelo/gravador instalados. Voz contínua e controle multimodal completo não estão validados.
- **Cabeça / pescoço:** movimentos pequenos calibrados, tolerância a tremores e seleção por permanência.
- **Mãos:** gestos configuráveis captados por webcam.
- **Acionador:** varredura experimental de medalhões com velocidade regulável e confirmação por combinação de teclas. Não equivale a suporte universal de qualquer tecla ou dispositivo.
- **Combinação:** selecionar por movimento e confirmar pela voz ou tecla.

Todas deverão acionar o mesmo conjunto de intenções, sem recriar diferentes interfaces.

## Requisitos de segurança e autonomia

Processamento local quando possível; câmera e microfone desligados por padrão; início/parada explícitos; indicador de captura; configuração por usuário; prevenção de ativações acidentais; pausa de emergência; alternativa de entrada quando sensor falhar; logs mínimos e sem gravação de mídia por padrão.

## Estado de validação

A ponte D-Bus e a extensão responderam em sessão GNOME 46 X11; os testes da interface por teclado/ativação e as camadas gráficas ainda exigem validação de ponta a ponta. Não apresentar o protótipo como ferramenta assistiva clinicamente validada.


Consulte [guia de acessibilidade](../../docs/ACESSIBILIDADE.md) e [privacidade](../../docs/PRIVACIDADE.md) para distinguir recursos existentes, requisitos e metas.
