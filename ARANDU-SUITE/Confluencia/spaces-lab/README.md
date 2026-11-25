# Espaços Vivos — adaptador experimental GNOME 46

Este laboratório é uma extensão independente com UUID `arandu-spaces-lab@arandulab`. Não está integrado ao instalador público e a construção não instala nem habilita nada. Não é a Foundation nem substitui a versão local já funcional.

## Escopo

O menu acessível na barra do GNOME usa os símbolos recuperados da Alça Viva e das flechas. Por ações explícitas, solicita ao Meta.Window maximização, minimização, posicionamento lateral e alteração de tamanho. A minimização não é um novo mecanismo de armazenamento nos Rios. A prévia amarela é passiva; largura e altura podem ser ajustadas em passos de 48 pixels lógicos e só são aplicadas após confirmação. Encerramento solicita fechamento normal à janela, com segunda confirmação explícita e identidade do alvo revalidada. O aplicativo pode solicitar salvar documentos.

Ações são bloqueadas se a Foundation estiver ativa, se a sessão não estiver permitida ou se a janela não for normal/elegível. Ações pendentes são descartadas em troca de foco, movimento/tamanho da janela, mudança de monitor, grab nativo, bloqueio, Visão Geral, Esc recebido pelo Shell, cancelamento explícito ou expiração de 20 segundos. Não mantém polling, não captura mídia, não inicia subprocesso X11, não muda decorações, não altera atalhos nem acessa núcleos privados. A prévia não participa da região de entrada.

Esta etapa é um adaptador por menu; não implementa ainda arraste da Alça, flechas que surgem por aproximação, gesto de redimensionamento contínuo ou integração com os painéis transitórios. Os seis SVGs adicionais não foram encontrados nos pacotes históricos disponíveis; foram usados rótulos em vez de redesenhar os símbolos. O ambiente GNOME 46/X11 real precisa ser validado antes de qualquer instalação experimental. A API Meta pode recusar ou ajustar a geometria solicitada, e os testes simulados não comprovam a execução gráfica.

## Construção e testes (sem instalação)

Da raiz do repositório, na branch de revisão:

```sh
node ARANDU-SUITE/Confluencia/spaces-lab/test-adapter.mjs
python3 ARANDU-SUITE/Confluencia/spaces-lab/build.py /tmp/arandu-spaces-lab
node --input-type=module --check < /tmp/arandu-spaces-lab/extension.js
```

O destino deve ser novo. O build copia três SVGs recuperados e os dois módulos puros da pasta design-reference. Não faz downloads nem inicia o GNOME.

## Validação antes de habilitar

Em uma sessão de teste separada GNOME 46, sem Foundation ativa e com arquivos descartáveis, verificar foco e elegibilidade, menu por teclado, cancelamento, confirmação da janela correta, geometria em múltiplos monitores e escalas, ausência de bloqueio de cliques, desmontagem limpa e coexistência com os indicadores nativos. Não usar em sessão de trabalho antes de validação e revisão de direitos/licença.
