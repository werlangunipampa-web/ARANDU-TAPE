# Protocolo proposto de pesquisa em interação humano-computador

Revisão 0.1 — 24/11/2026. Planejamento, não estudo executado ou aprovado. Complementa o protocolo de engenharia e a arquitetura pública. Nenhum participante, resultado ou tamanho amostral é inventado.

## 1. Questões e hipóteses

- Q1. A organização por Semente e Rios favorece a localização e a retomada de atividades? H1: menor esforço de navegação e melhor orientação em tarefas comparáveis.
- Q2. Controles contextuais de janela com prévia favorecem controle espacial sem aumentar ações involuntárias? H2: menor número de correções e melhor percepção de controle, sem prejuízo relevante à conclusão da tarefa.
- Q3. A revelação progressiva e a Presença Viva equilibram simplicidade e descoberta? H3: redução de poluição visual percebida sem comprometer encontrabilidade, inclusive por teclado.
- Q4. A interface essencial mantém fluidez e autonomia sem serviços de pesquisa? H4: funcionamento independente e custo computacional compatível com metas previamente especificadas.

Hipóteses podem ser refutadas. Não interpretar eficiência ou satisfação como comprovação de aprendizagem significativa.

## 2. Fases e critérios

Fase A — engenharia: testes automatizados e isolamento, execução gráfica real, recuperação, privacidade e desempenho. Usar dados fictícios, sem coleta de conteúdo pessoal. Bloquear ensaios com usuários se existirem regressões graves ou perda de controle.

Fase B — piloto de usabilidade: depois das autorizações aplicáveis, usar tarefas controladas e ambiente documentado. Identificar problemas de instrução, familiaridade, instrumentos e acessibilidade. Dados do piloto não constituem comprovação de eficácia.

Fase C — avaliação comparativa: comparar ambiente convencional e candidato ARANDU no mesmo equipamento e sob condições equivalentes. Definir antes da coleta o desfecho primário, menor efeito de interesse, estratégia amostral, inclusão, ordem das condições, análise e exclusões. Se desenho intraindividual, contrabalançar ordem e usar tarefas equivalentes para reduzir efeitos de aprendizagem. Não generalizar para todos os perfis ou compositores.

Fase D — estudo de aprendizagem de uso: se pertinente, incluir retomada em intervalo previamente definido, explicação das relações entre controles e transferência para tarefas novas. Retenção operacional não equivale necessariamente à aprendizagem significativa ausubeliana; investigação dessa teoria exige instrumentos próprios e análise interpretativa.

## 3. Tarefas e observáveis

| ID | Tarefa controlada | Observáveis |
| --- | --- | --- |
| U01 | Localizar e abrir aplicativo fictício pelo ambiente | Conclusão, tempo, tentativas, ajuda |
| U02 | Alternar entre duas tarefas e retomar a anterior | Erros de seleção, tempo, orientação |
| U03 | Encontrar documento fictício e retornar à janela | Caminho de interação, sucesso e esforço |
| U04 | Redimensionar janela até um alvo geométrico por lados e cantos | Erro geométrico, tempo, correções, eventos involuntários |
| U05 | Maximizar, recolher, recuperar e cancelar uma operação | Sucesso, perda de foco, recuperação, ações indesejadas |
| U06 | Descobrir controles contextuais e repetir por alternativa de teclado/menu | Encontrabilidade, tempo, barreiras, pedidos de ajuda |
| U07 | Retomar tarefas após intervalo definido | Retenção operacional, explicação e transferência |
| U08 | Realizar tarefas essenciais sem rede de IA nem credenciais | Sucesso e independência; medir recursos separadamente |

Tarefas precisam corresponder às funções presentes no commit avaliado. Ausência de componente é registrada como indisponibilidade, não como sucesso. Encerramento deve usar janelas descartáveis e preservar trabalho.

## 4. Medidas e análise

Adotar como estrutura de usabilidade efetividade, eficiência e satisfação, no sentido da ISO 9241-11:2018. Definir previamente o que conta como sucesso, erro, abandono, ação involuntária e ajuda. Registrar tempos apenas de tarefas definidas; para redimensionamento usar erro absoluto em pixels lógicos e registrar escala e geometria-alvo. Para desempenho técnico usar o protocolo separado, CPU/RAM/swap do sistema inteiro e medições de latência com método explícito. Não confundir taxa de atualização da prévia com taxa de quadros percebida.

Apresentar dados ausentes e falhas, medidas de tendência central e dispersão, estimativas de efeito e incerteza adequadas ao desenho e ao tamanho amostral. Uma comparação não controlada não estabelece causalidade. Definir instrumento de satisfação e esforço antes da coleta; não inventar escala validada. Relatos qualitativos podem contextualizar barreiras, estratégias e autonomia, sem identificar pessoas.

## 5. Privacidade e responsabilidade

A participação humana somente será iniciada após avaliação ética e institucional aplicável, consentimento e informação sobre finalidade, dados, duração e possibilidade de retirada. Não coletar tela, áudio, histórico, títulos de janelas, credenciais ou documentos pessoais por padrão. Usar perfil de teste e materiais fictícios; separar identificadores de resultados e controlar acesso. Definir retenção e descarte antes da coleta. Não publicar dados individuais ou núcleos reservados no Zenodo; somente materiais e resultados cuja divulgação tenha sido autorizada.

## 6. Registro de uma execução

Preencher: protocolo/versão, SHA, ambiente, data, condições, critérios, métricas, aprovação aplicável, resultado e limitações. Manter distinção entre evidência de engenharia e estudo com pessoas. Nenhum resultado apresentado neste documento.

Referências: [fundamentação pública](FUNDAMENTACAO_PUBLICA.md), [arquitetura e contribuições](ARQUITETURA_CONTRIBUICOES_CIENTIFICAS.md), [validação funcional e desempenho](VALIDACAO_FUNCIONAL_DESEMPENHO.md); ISO 9241-11:2018, https://www.iso.org/standard/63500.html.
