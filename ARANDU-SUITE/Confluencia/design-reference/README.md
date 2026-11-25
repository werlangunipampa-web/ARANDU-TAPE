# Convergência gráfica ARAPI — referência não instalada

Fonte: inventário da instalação local fornecido pelo responsável pelo projeto em 24/11/2026. Dez arquivos presentes correspondem byte a byte aos SHA-256 do manifesto; três entradas eram somente inventário. Não publicar o ZIP integral nem dados de identificação da máquina.

## Importação seletiva

| Arquivo neste diretório | SHA-256 original |
| --- | --- |
| alca-viva.svg | 9a2be5548b3eb434b1ccab427ce6e71d4fdb3a0c0d13858a967443898c236823 |
| flecha-azul.svg | 00f4d455a8fd8d20a90e55666e979d550821cbebcf01e05a48bc977b7f859ba7 |
| flecha-amarela.svg | 9f5c9898e1a697bc8a777500ebca4ac7e8c56080709efaadb9dd71c5b002a3c9 |
| ponteiro-folha.svg | 1b233d9338308bf15d1e6430a01c3bebb3c7c12f7f8b4772fad2cb9307caffb8 |
| espacos-math.mjs | 12d69e944d506ba565b0bb67fdad767eb02c0a9a39478ee8220de7cb4d140c52 |

O último arquivo foi renomeado de espacos-math.js para permitir teste ESM em Node sem alterar os bytes. Os quatro SVGs possuem apenas elementos gráficos locais. A cópia design/arandu-alca-viva.svg é idêntica à cópia Foundation e não foi duplicada. Os hashes dos blobs Git foram comparados com os originais. Titularidade, procedência e licença final ainda dependem da revisão do projeto. Não se trata de release.

## O que não foi importado

- espacos-vivos.js: adaptador GNOME 46 restrito a ARANDU_SESSION=1; depende de _seed, _opyOpen, _a93Busy, _windowActionBusy, _showHint, _hideHint e path da Foundation. A classe usa seis SVGs adicionais ausentes: imersao.svg, recolher.svg, confluencia-esquerda.svg, confluencia-direita.svg, encerrar.svg e cancelar.svg.
- O adaptador contém subprocesso Python/Xlib persistente, manipulação de decorações X11, injeção de atalhos por teclado virtual, consulta /proc/PID/cmdline para reconhecer Terminal e temporizador de 16 ms durante arraste. Requer isolamento, revisão de privilégios de ação, foco, recuperação e custo. O caminho de encerramento deliberado após prévia pode solicitar fechamento sem segundo diálogo, apesar do comentário inicial. Não importar automaticamente nem modificar a versão local.
- stylesheet.css: 84.532 bytes e 483 aberturas de bloco, incluindo estilos de outros componentes e variantes sensoriais. Sem URL externa detectada na triagem; separar somente regras necessárias e validar prioridades.
- cursor/index.theme e cursor/cursors/left_ptr: tema herda Adwaita; cabeçalho Xcursor contém imagens 24, 32, 48 e 64 px. Manter binário fora do repositório até verificar geração a partir do SVG, hotspots, compatibilidade, procedência e restauração de preferências.
- metadata.json, extension.js e semente-guardia.js da Foundation: somente hashes, sem conteúdo no pacote. Não inferir a arquitetura nem divulgar núcleos de pesquisa.

## Testes e limites

O módulo matemático é puro, não opera janelas. Seu classificador de margens é histórico: encerramento na margem inferior esquerda; não representa necessariamente a gramática mais recente. O adaptador local usa campos reais de soltura, em vez de simplesmente chamar classifyDrop. Manter o contrato Python de gestos como referência separada, sem substituir o comportamento local por inferência. O teste desta pasta verifica casos representativos, não todas as entradas ou limites; uma revisão futura deve validar dimensões mínimas, valores anômalos e identidade do alvo.

Executar da raiz: `node ARANDU-SUITE/Confluencia/design-reference/test-math.mjs`.

Esta pasta não altera instaladores, schema, extensão ativa, cursor, nem sessão. A integração executável exige análise dos recursos e interfaces gráficas mínimas faltantes, confirmação de escopo público e testes em GNOME 46/X11 real. Não remover as decorações ou indicadores nativos antes de validar recuperação.
