# Espaços Vivos — adaptador experimental GNOME 46

Este laboratório é uma extensão independente com UUID `arandu-spaces-lab@arandulab`. Não está integrado ao instalador público e a construção não instala nem habilita nada. Não é a Foundation nem substitui a versão local já funcional.

## Escopo

O menu acessível na barra do GNOME usa os símbolos recuperados da Alça Viva e das flechas. Por ações explícitas, solicita ao Meta.Window maximização, minimização, posicionamento lateral e alteração de tamanho. A minimização não é um novo mecanismo de armazenamento nos Rios. A prévia amarela é passiva; largura e altura podem ser ajustadas em passos de 48 pixels lógicos e só são aplicadas após confirmação. Encerramento solicita fechamento normal à janela, com segunda confirmação explícita e identidade do alvo revalidada. O aplicativo pode solicitar salvar documentos.

Ações são bloqueadas se a Foundation estiver ativa, se a sessão não estiver permitida ou se a janela não for normal/elegível. Ações pendentes são descartadas em troca de foco, movimento/tamanho da janela, mudança de monitor, grab nativo, bloqueio, Visão Geral, Esc recebido pelo Shell, cancelamento explícito ou expiração de 20 segundos. Não mantém polling, não captura mídia, não inicia subprocesso X11, não muda decorações, não altera atalhos nem acessa núcleos privados. A prévia não participa da região de entrada.

Esta etapa contém ações por menu e uma experiência opt-in de flechas contextuais de redimensionamento. O arraste da Alça Viva e a integração com os painéis transitórios ainda não estão implementados. Os seis SVGs adicionais não foram encontrados nos pacotes históricos disponíveis; foram usados rótulos em vez de redesenhar os símbolos. O ambiente GNOME 46/X11 real precisa ser validado antes de qualquer instalação experimental. A API Meta pode recusar ou ajustar a geometria solicitada, e os testes simulados não comprovam a execução gráfica.

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

## Flechas Vivas nas oito direções — revisão de design

Ativar explicitamente no menu “Flechas Vivas · ativar nesta sessão”. O padrão é desligado a cada ativação da extensão. Uma única flecha de arco e flecha autoral, sem grafismo tradicional atribuído, aparece perto do ponteiro em qualquer lado ou canto elegível. O símbolo de 18 px lógicos está num controle de 24 px; oito orientações geradas por rotação do mesmo SVG. Norte, sul, leste e oeste alteram um eixo; diagonais alteram dois. A borda oposta permanece ancorada. A Imersão permanece em ação separada no menu; não ocupa o canto superior direito do redimensionamento.

Em repouso não existe região de entrada invisível nas bordas. Na aproximação (12 px), aparece apenas um botão pequeno e o contorno fino dourado, passivo. Na saída, ambos desaparecem. Apenas pressionar o botão e arrastar pelo menos 4 px permite uma prévia. A geometria solicitada é mostrada como contorno iluminado sem capturar cliques; liberação explícita aplica a prévia, Esc cancela e a proteção de 20 s continua valendo. O clique sem arraste não altera a janela. Durante o gesto explícito há uma captura transitória do ponteiro pelo Shell, removida ao cancelar, concluir ou desativar. Não há captura permanente, modificação da decoração ou subprocesso.

Para detectar aproximação também quando o ponteiro está em janelas de aplicativos X11, o modo experimental consulta a posição do ponteiro a cada 90 ms somente quando ativado e com janela elegível, fora do menu. Não é uma implementação inteiramente dirigida por eventos; o custo real precisa ser medido. Nenhum histórico de posição é persistido. A primeira versão só atua em janelas normais, redimensionáveis, não maximizadas e inteiramente dentro da área útil; dimensões mínimas propostas de 240 × 160 px. Restrições próprias do aplicativo podem alterar a geometria efetiva. Validar captura, acesso às bordas, conflitos com controles nativos, escalas, foco, teclado e múltiplos monitores antes de habilitar em sessão de trabalho. Não utilizar junto à Foundation ativa.

Testes adicionais: `node ARANDU-SUITE/Confluencia/spaces-lab/test-edge-geometry.mjs` e `node ARANDU-SUITE/Confluencia/spaces-lab/test-adapter.mjs`.
