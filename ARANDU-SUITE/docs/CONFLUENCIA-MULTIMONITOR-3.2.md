# ARANDU TAPE 3.2 beta — Confluência temporária e múltiplos monitores

## Objetivo

A Semente e os três rios formam **uma única camada temporária** de navegação. O ARANDU retorna à área de trabalho após a escolha, não fica sobre as janelas de trabalho.

## Fluxo previsto

1. Pressionar `Super+Alt+1/2/3` escolhe o rio e eleva **Semente, rios e medalhões juntos** sobre as janelas.
2. Navegar por teclado, acionador assistivo ou toque. Não há temporizador que descarte a escolha.
3. Confirmar um medalhão abre/focaliza a janela; a camada volta ao desktop.
4. `Super+Alt+0` cancela e retorna a camada ao desktop.
5. Quando a varredura é iniciada com um rio já selecionado, a camada é reativada.
6. Quando a extensão está configurada em modo flutuante permanente (`floating=true`), respeita-se essa escolha explícita; o retorno ao desktop requer `floating=false`.

## Monitores

O destino padrão é o **monitor da janela ativa**. Se ele não existir ou tiver sido desconectado, a Confluência usa o monitor principal disponível. Os monitores do GNOME são identificados por índices a partir de zero; o menu mostra 1, 2, 3 para o usuário.

No menu Confluência do painel GNOME existem seleções:
- **Acompanhar janela ativa** (padrão);
- **Acompanhar ponteiro/toque**, via posição do último ponteiro reportada pelo Shell;
- **Monitor principal**;
- **Monitor fixo 1/2/3** (com fallback seguro se não estiver conectado).

Somente uma Confluência e uma varredura existem por sessão, inclusive com 2 ou 3 telas. A troca de monitores ajusta a área de trabalho, posiciona a Semente e recalcula os rios. O modo de navegação conserva o monitor escolhido até terminar, evitando saltos inesperados enquanto o foco muda.

**Limitações:** o modo `pointer` usa as coordenadas do ponteiro fornecidas pelo GNOME; ainda não distingue diretamente qual dedo tocou qual monitor touchscreen. O modo `fixed` guarda índice de saída, não a identidade física/EDID do monitor — trocar cabos pode alterar os índices.

## Atualização integrada do VAIO GNOME 46/X11

O pacote inclui `ARANDU-SUITE/atualizar-vaio-3.2.sh`, que:
1. Valida a versão GNOME 46/X11;
2. Executa testes e verificação do pacote;
3. Faz backup das duas novas extensões;
4. Atualiza a Confluência com o instalador transacional;
5. Aplica as duas atualizações pendentes da TOPBAR (**botão ARANDU abre aplicativos, RIOS controla Confluência e engrenagem abre preferências gráficas**) copiando somente `extension.js` e `prefs.js`;
6. Preserva CSS, grafismos, preferências e as antigas extensões desativadas.

**Nunca executar com sudo.** Salvar os trabalhos e sair/entrar na sessão antes de validar na interface. Não reabilitar `arandu-lab@local` ou `arandu-tape@arandulab` enquanto as novas extensões estiverem ativas.

### Confirmação visual e recuperação

Testar com 1 monitor e 2–3 monitores:
- Atalhos 1/2/3 mostram Semente+rio em primeiro plano;
- Seleção por toque e por teclado;
- Ativação retorna para a janela;
- Cancelamento retorna ao fundo;
- Destino acompanha janela ativa e monitor fixo;
- Desconectar monitor migra a interface ao principal;
- Engrenagem TOPBAR abre preferências e grafismos;
- Super+Alt+H alterna a barra e Super+Alt+B recupera.

Se houver erro ou regressão, desativar apenas a Confluência ou TOPBAR afetada e restaurar seu arquivo a partir do backup criado em `~/ARANDU-BACKUP-INTEGRADO-*/`. As versões antigas não foram apagadas.

**Status:** código publicado e testes simulados adicionados, mas não foi feita validação visual no VAIO ou com três monitores reais. Não tratar essa beta como versão estável.
