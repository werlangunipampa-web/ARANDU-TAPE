# Evidência de pré-validação local do candidato científico

Registro sanitizado do relatório de terminal fornecido pelo responsável durante a preparação do primeiro depósito. O relatório foi produzido no clone separado de revisão. Não incluir prompt do terminal, hostname, nome de usuário ou caminhos pessoais.

Commit avaliado: `716cfaa91b3ba01d3725efec4cf88e0d809921bb`.

| Verificação local | Resultado informado |
| --- | --- |
| Triagem do código-fonte | pass |
| Barreira de escopo de pesquisa | pass |
| Contratos Desktop | pass |
| Geometria de bordas | pass |
| Simulação do adaptador | pass |
| Build temporário do laboratório | pass |
| Sintaxe do laboratório | pass |
| GTK 3.0 | pass |
| GTK 4.0 | pass |
| cffconvert local | not_available |

Ambiente: GNOME Shell 46, X11. Extensão ARANDU/Confluência ativa: sim. Sessão candidata ao teste isolado: não. A advertência de conflito foi emitida como esperado. Não desativar a instalação em uso para produzir esta evidência.

O relatório local tem `graphical_validation: not_executed` e `publication_authorized: false`. O resultado comprova a execução das verificações informadas pelo responsável, não a execução visual das extensões, desempenho comparativo ou ausência absoluta de conteúdo reservado.

## Evidência automatizada complementar

No mesmo head, as duas suítes concluíram com sucesso: [Desktop](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45537918250) e [Suite](https://github.com/werlangunipampa-web/ARANDU-TAPE/actions/runs/45537918086). O log Desktop confirma CFF 1.2.0 válido, 114 testes Python aprovados e triagem de 181 entradas, zero indicadores bloqueantes e sete referências de pesquisa para revisão no merge de CI `c093e52b0fedbf45511276bd21219b200a23d0a5`. O validador bibliográfico não estava instalado localmente, mas a evidência CI para esse head está disponível.

## Próximo ensaio

Testar primeiro o aplicativo GTK4 independente no clone de revisão, sem modo de sessão Sway. Não iniciar se outra instância do protótipo GTK4 estiver aberta, pois o identificador de aplicação pode encaminhar a ativação à instância anterior. Usar somente ações de apresentação, dados fictícios e fechamento normal; não clicar em atualização, captura, configuração de dispositivos ou envio de IA durante o ensaio básico.

O laboratório de extensão GNOME deve permanecer desabilitado na sessão atual. Os ensaios F01–F08 exigem sessão de teste separada GNOME 46/X11, sem as extensões ARANDU/Confluência ativas. Todos os ensaios gráficos continuam não executados neste registro.

Este documento foi acrescentado após o SHA avaliado; o head final precisará de nova validação e revisão. Não constitui autorização de depósito.

## Primeiro ensaio visual GTK4 — relato do responsável

No clone do candidato de pré-validação, o responsável informou: abertura normal, três Rios visíveis, medalhões responsivos, cabeçalho sem sobreposição, painel Sobre funcional e encerramento sem interferência na sessão principal. A expansão/recolhimento da Semente ficou **não confirmada**. Seis de sete verificações confirmadas; não presumir causa nem reprovação de um mecanismo específico. O ensaio não valida as extensões GNOME.

Correções propostas após o relato: preservar a alocação do filho principal do Gtk.Overlay, ocultando apenas sua pintura quando recolhido (fundo não interativo), e acrescentar controle acessível explícito de alternância no protótipo GTK4, com rótulo sincronizado. Não alterar a dimensão da Semente nem a instalação local. Testes simulados exercitam os corpos reais dos métodos. Reteste visual obrigatório; não marcar o item como aprovado antes do relato. O botão adicional é uma alternativa de diagnóstico/acessibilidade do protótipo, não alteração automática da gramática gráfica definitiva.

## Reteste visual da Semente — confirmado pelo responsável

Após a atualização do clone de revisão e a correção intermediária, o responsável confirmou os quatro critérios: primeiro clique na Semente expande os Rios; segundo clique recolhe; botão alternativo funciona; Esc recolhe. Os seis critérios positivos do primeiro ensaio e a confirmação posterior da Semente fornecem evidência dos sete critérios originais em dois ensaios. Não foi registrado SHA explícito na saída deste reteste; a correção encontra-se a partir dos commits 4dd64e22b9b9e2b48e8a37fb06d071492d0d868d e 99299011a6ea363a1f5fac40f57da27761fedbf9. Não atribuir o reteste a um SHA exato sem confirmação. O ensaio não comprova expansão geométrica do símbolo em si, desempenho, compatibilidade com todas as escalas ou funcionamento das extensões GNOME. Não confundir o botão alternativo do protótipo com a gramática definitiva do ambiente.

Próximos ensaios: teste do laboratório GNOME 46/X11 em sessão separada, sem outras extensões ARANDU ativas, conforme F01–F08; manter a instalação principal intacta. Registrar SHA e resultados antes de qualquer aceite final.
