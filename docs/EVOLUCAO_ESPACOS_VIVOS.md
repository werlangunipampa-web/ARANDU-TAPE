# Registro de evolução dos Espaços Vivos — novembro de 2026

## Delimitação da evidência

O desenvolvimento possui duas linhas: o laboratório público GNOME 46, contido neste repositório, e os ajustes incrementais da Foundation instalada no ambiente ARAPI. A segunda linha não é automaticamente parte da primeira release científica. Não publicar o módulo Foundation inteiro nem os arquivos privados de pesquisa. Não declarar que o snapshot público reproduz integralmente a instalação local.

## Candidato público

Snapshot de evidência: `c8e16cd4f8a510e1625eb35c434253a591a8ec4b`.

- Oito direções de redimensionamento com ancoragem da borda oposta, símbolos vetoriais autorais de arco e flecha e prévia passiva.
- Flecha Mestre azul abaixo do canto superior direito, com ação explícita de maximização e alternativa por menu.
- Laboratório GNOME 46 separado, ativação voluntária, proteção contra concorrência com a Foundation, sem alteração de decoração nativa.
- Testes automatizados concluídos com sucesso: [Desktop](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45533919228) e [Suite](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45533919455).
- A verificação é de contratos, simulação e construção; não substitui teste de execução real. O laboratório público ainda usa consulta de aproximação de 90 ms quando habilitado. Não atribuir a ele a implementação ou o desempenho dos patches locais.

## Evolução local — registro técnico sem incorporar código privado

| Ajuste | Mudança de projeto | Evidência |
| --- | --- | --- |
| Nove Flechas Vivas | Oito direções de redimensionamento e Flecha Mestre, reaproveitando o mecanismo gráfico local | 4 testes offline do patch |
| Contorno Vivo | Linha de 1 px, interior transparente, sem halo ou preenchimento dourado | 4 testes offline; retorno positivo do responsável sobre o contorno |
| Movimento Suave | Eventos de movimento e reaproveitamento do ciclo existente; deduplicação de solicitações de geometria, sem interpolação atrasada do ponteiro | 4 testes offline |
| Presença Viva | Controle dourado de 18 para 32 px; Mestre de 20 para 34 px; espera de 180 ms e transição de 150 ms | 4 testes offline; retorno positivo sobre o efeito, com observação de perda de nitidez |
| Nitidez Viva | SVG renderizado no tamanho final de 24/26 px do ícone e escala animada de 0,5 a 1, evitando ampliar a pequena textura | 4 testes offline; nitidez final ainda não confirmada |

Os valores são parâmetros experimentais dos patches locais, não uma avaliação ergonômica validada. A transição visual não deve alterar a geometria da janela, disparar operação por aproximação ou acrescentar atraso de arraste. A evolução local preserva o desenho das flechas, o mecanismo existente da Alça Viva e a reversibilidade dos ajustes. Não há medição de desempenho comparativa neste registro.

Foram executados novamente os cinco comandos --test, totalizando 20 testes offline aprovados. Esses testes não comprovam a aplicação de todos os patches na máquina do responsável, nem equivalência com o candidato público. As observações do responsável são evidência qualitativa informal de uso local, não estudo de usuários.

## Diretrizes de convergência

1. Interior da janela e da prévia sempre transparentes; contorno fino sem preenchimento nem halo difuso.
2. Presença pequena por aproximação e crescimento localizado após permanência, sem autoexecução; manter alternativa acessível por teclado/menu.
3. SVG nítido no tamanho final, compatível com escalas de tela; conferir antes de declarar resolução corrigida.
4. Medir fluidez, latência, uso de CPU/RAM e conflitos de entrada no ambiente real. Preservar Semente, Alça Viva, Rios, avisos e controle nativo.
5. Portar somente implementação pública revisada e independente. Atualizar testes e documentar a diferença de comportamento até a convergência.
6. Se as melhorias locais não forem integradas ao commit aprovado, excluir suas alegações funcionais do resumo Zenodo e das notas da release.

Este documento registra a evolução de design e os limites da evidência; não concede licença, não autoriza depósito e não constitui nova release.
