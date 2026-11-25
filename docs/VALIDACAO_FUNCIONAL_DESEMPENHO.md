# Protocolo de validação funcional e de desempenho

Revisão 0.1 — 24/11/2026. Protocolo de aceite para o candidato à primeira publicação científica. Não contém resultados de testes reais ainda não executados.

## 1. Preparação segura

Usar clone Git separado, com árvore limpa e SHA identificado. Não substituir uma instalação ARANDU em uso, não executar instalador com sudo, não alterar a sessão padrão. Salvar o trabalho e preservar GNOME/Cinnamon funcional como caminho de recuperação. Testar a suíte GNOME em perfil de teste ou ambiente isolado, e GTK4/Sway inicialmente em sessão aninhada. O PR de documentação e correções não constitui release.

Registrar distribuição, kernel, GNOME, tipo de sessão, resolução/escala, quantidade de monitores, CPU/RAM, commit e componentes instalados. Não publicar nome de usuário, hostname, dados de janelas, credenciais ou capturas privadas.

## 2. Triagem antes de instalar

Na raiz do clone:

```bash
git status --short --branch
git rev-parse HEAD
python3 -m compileall -q ARANDU-DESKTOP
python3 -m unittest discover -s ARANDU-DESKTOP/tests -v
python3 ARANDU-SUITE/verificar.py
python3 scripts/auditar-snapshot.py --ref HEAD
bash ARANDU-DESKTOP/session/verify-essentials.sh
```

A verificação de dependências opcionais pode indicar itens pendentes fora do laboratório Sway. A CI também testa contratos Shell. Se houver falha de segurança, compilação ou teste aplicável, parar e registrar; não instalar automaticamente. Nenhum comando acima valida por si só uma sessão gráfica.

## 3. Aceite em GNOME 46/X11 (Linux Mint)

| ID | Ensaio | Resultado esperado |
| --- | --- | --- |
| G01 | Abrir e recolher Semente e Rios por ação explícita | Navegação previsível; sem fechar aplicativos |
| G02 | Selecionar Rio e aguardar mais de 10 s com temporizador desligado | Nenhum recolhimento por mero tempo; repouso visual distinto |
| G03 | Escolher 10 s no menu e repetir; restaurar opção nunca recolher por tempo | Temporizador opcional funciona; preferência respeitada |
| G04 | Ativar medalhão, clicar fora e retornar ao aplicativo | Foco correto; cliques e digitação não interceptados |
| G05 | Alternar Rios, percorrer medalhões, confirmar/cancelar pelo teclado | Foco visível, sem ativações involuntárias |
| G06 | Varredura experimental e intervalo configurável | Nenhuma abertura por timer; cancelamento funciona |
| G07 | Arrastar Semente, cobrir/descobrir sua posição com janela, testar botão compacto, opt-out, múltiplos monitores e escalas | Âncora preservada, clique limitado ao botão, retorno explícito aos Rios, sem deslocamento sob o ponteiro durante cobertura, sem sobreposição evitável nem perda de controle; verificar tela cheia e bloqueio |
| G08 | Abrir mapa GTK3, alternar temas e dimensões | Paisagem procedural legível e sem erro |
| G09 | Desativar histórico e testar limpeza em perfil sem dados reais | Controles e limites correspondem à política de privacidade |
| G10 | Abrir painel da Semente; conferir hora/histórico; abrir avisos e controles GNOME; Esc; testar sessão bloqueada e conflito de extensão | Acesso sob demanda, fallback honesto, nenhuma ocultação pela Confluência nem perda de indicadores essenciais; validar separadamente câmera, microfone e compartilhamento |
| G11 | Desativar extensão e recuperar desktop habitual | Sessão permanece utilizável |

Verificar Alça Viva, flechas de Imersão/redimensionamento, Folha Digital, Opy e Cabeçalho Vivo somente quando a implementação correspondente estiver presente e identificada no candidato; ausência é pendência, não aprovação. A aproximação nunca deve executar ação. Não ocultar permanentemente indicadores originais de privacidade sem substituição comprovada.

## 4. Aceite em GTK4/Sway

Abrir o protótipo GTK4 sem mudar o login. Testar Semente, navegação, Opy, informações do sistema, Terminal ARANDU, atualização apenas sob consentimento e saída/recuperação. No laboratório Sway aninhado, testar foco e janelas com dados sintéticos. Manter IA desligada durante o ensaio básico; nenhuma dependência de núcleos privados. Testar recursos de captura somente com conteúdo fictício. Opy e componentes GTK4 têm escopo distinto do Shell GNOME.

## 5. Desempenho comparável

Medir no mesmo equipamento, resolução, fonte de alimentação, perfil energético e carga de aplicativos. Primeiro GNOME sem a extensão ARANDU ativa; depois GNOME com a extensão. Manter o restante das extensões e condições equivalentes. Em cada fase aguardar estabilização, repetir no mínimo três vezes e registrar se há atualizações ou processos concorrentes.

```bash
python3 ARANDU-DESKTOP/benchmark.py --measure --count 10 --interval 1
```

O utilitário existente mede CPU, RAM e swap do computador inteiro, não o consumo exclusivo do ARANDU. Opcionalmente salvar em arquivo privado novo com --save CAMINHO; não enviar automaticamente. Para comparar dois relatórios:

```bash
python3 ARANDU-DESKTOP/benchmark.py --compare A.json B.json
```

Complementar, em ensaios separados, com tempo de abertura de aplicativo, resposta da Semente, arraste, alternância dos Rios e tempo de recuperação. Registrar mediana de repetições e condições de medição; não alegar melhoria causal com base em uma única amostra. Sway aninhado não equivale a uma sessão independente para comparar consumo.

## 6. Registro de aceite

| ID | Ambiente/SHA | Status | Evidência sanitizada | Observação |
| --- | --- | --- | --- | --- |
| G01–G11 | A preencher | Não executado | — | — |
| GTK4/Sway | A preencher | Não executado | — | — |
| Desempenho | A preencher | Não executado | — | — |

Estados: aprovado, reprovado, não executado, não aplicável com justificativa. Bloquear release científica em caso de regressão grave, perda de dados, falha de recuperação, ações involuntárias ou indicadores de privacidade comprometidos. Fixar critérios quantitativos de desempenho antes de declarar metas atingidas. Direitos, licença e revisão de divulgação permanecem portões independentes.

Referências: [Design Core](DESIGN_CORE.md), [Acessibilidade](ACESSIBILIDADE.md), [Privacidade](PRIVACIDADE.md), [Estado e versões](ESTADO_E_VERSOES.md), [Política Zenodo](PUBLICACAO_CIENTIFICA_ZENODO.md).

## Complemento: Cabeçalho Vivo e gestos

Confirmar a reserva superior de 52 px lógicos em Desktop, mapa e Opy, sem sobreposição do conteúdo ou dos controles existentes; testar dimensões menores, escala e teclado. Fechar a Opy deve fechar somente sua interface. O classificador Python de gestos ainda não está ligado a janelas reais. Registrar Alça Viva, flechas gráficas e Folha Digital como não executados até localizar/sincronizar a implementação autorizada. Não substituir as decorações nativas por gestos não validados. Testar prévia, cancelamento, liberação explícita, identidade do alvo, confirmação de encerramento e reserva inferior em revisão posterior.

## Complemento: aceite específico do laboratório Espaços Vivos

Executar somente em GNOME 46 de teste, sem Foundation ativa e com janelas descartáveis. Habilitar as Flechas Vivas voluntariamente; verificar o retorno ao modo desligado ao reiniciar a extensão.

| ID | Ensaio | Critério de aceite |
| --- | --- | --- |
| F01 | Aproximar e afastar de cada um dos oito lados/cantos | Somente controle pertinente; nenhuma ação automática, nenhum clique capturado fora do controle |
| F02 | Permanecer na zona da flecha e depois sair | Crescimento localizado, retorno ao repouso, símbolo nítido na escala testada; sem cintilação ou temporizador residual |
| F03 | Arrastar em oito direções, inclusive para dentro, e soltar | Borda oposta ancorada; prévia coincide com geometria solicitada, respeitadas restrições da janela; interior transparente e contorno de 1 px |
| F04 | Aproximar-se da Flecha Mestre, clicar e repetir junto ao canto NE | Maximização por clique explícito; distinção inequívoca de redimensionamento; nenhum disparo por aproximação |
| F05 | Esc, troca de foco, grab nativo, bloqueio, desativação, mudança de monitor durante gesto | Intenção cancelada, prévia e controles ocultos, captura de ponteiro liberada |
| F06 | Redimensionar em escalas e monitores distintos; testar janelas inelegíveis | Sem controle fora da área útil ou sobre janela indevida; caminhos nativos disponíveis |
| F07 | Usar o menu por teclado e testar redução de movimento/contraste | Alternativas compreensíveis e foco visível; se redução de animação ainda não respeitada, registrar pendência |
| F08 | Comparar repouso desativado, repouso habilitado e arraste | Registrar medições em condições equivalentes; sem meta numérica inventada nem afirmação de melhoria sem dados |

Status inicial de F01–F08: **não executados no ambiente gráfico real**. Testes simulados cobrem parte dos contratos, mas não contam como aprovação desses ensaios. Registrar separadamente candidato público e instalação local. Não publicar capturas que contenham documentos, títulos de janelas ou informações pessoais.

O estudo comparativo com participantes é tratado separadamente em [PROTOCOLO_PESQUISA_INTERACAO.md](PROTOCOLO_PESQUISA_INTERACAO.md).

## Pré-teste local sem instalação

Em clone novo da branch de revisão, com árvore limpa e SHA integral identificado:

```bash
/usr/bin/python3 -B scripts/preflight-grafico.py --commit "$(git rev-parse HEAD)"
```

O pré-teste executa triagem, barreira de escopo, testes Python, geometria/mocks JavaScript, build temporário e sintaxe, verifica presença de GTK3/GTK4 e CFF quando disponível e consulta somente a versão GNOME, tipo de sessão e existência de extensão ARANDU/Confluência ativa. Não exibe UUIDs de outras extensões, nome de usuário, hostname, credenciais ou saída bruta de comandos. Não instala, habilita, desabilita ou modifica extensões, não executa a GUI nem acessa serviços de pesquisa. O diretório temporário do build é descartado. O status isolated_session_candidate é uma triagem, não prova de isolamento completo; se houver conflito, não testar o laboratório na sessão corrente. Resultado graphical_validation permanece not_executed. Código de saída informa testes técnicos obrigatórios, não autorização para habilitar nem publicar. Dependências ausentes devem ser registradas, não instaladas automaticamente.
