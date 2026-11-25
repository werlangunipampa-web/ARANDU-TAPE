# ARANDU TAPE — Privacidade e tratamento de dados

Revisão 0.1 — 24/11/2026. Descrição técnica preliminar do código público, não certificação de conformidade legal. Abrange Confluência GTK3/GNOME e Desktop GTK4/Sway; não abrange serviços de pesquisa privados.

## Dados e escolhas

| Componente | Dados e finalidade | Controle e armazenamento |
| --- | --- | --- |
| Confluência GNOME | Identificadores de aplicativos, títulos de janelas recentes, frequência e horários; navegação | Preferência GNOME de lembrar arquivos recentes; GSettings da extensão; até 80 registros recentes e 180 entradas de frequência no código examinado |
| Mapa GTK3 | Itens recentes, identificadores, títulos, URI de arquivos, horário, contagens e preferências | Banco local mapa.sqlite3 em $XDG_STATE_HOME/arandu-tape-confluencia ou ~/.local/state/arandu-tape-confluencia; arquivo criado/ajustado com modo 0600; limites de 160 recentes e 240 frequências |
| Documentos recentes | Metadados fornecidos pelo gerenciador de recentes GTK, filtrados pelo código | Preferência de privacidade GNOME; não equivale a acesso ao conteúdo integral do arquivo |
| Desktop GTK4 | Consulta de aplicativos e janelas da sessão autorizada; indicadores de hardware, Bluetooth e desempenho sob demanda | Adaptadores locais; não confundir com o histórico persistente do GTK3 |
| Voz no mapa GTK3 | Frase curta solicitada pela pessoa, captura por parec ou arecord, reconhecimento Vosk local | Modelo instalado separadamente; janela de leitura de áudio de até cerca de 8 s após inicialização; comando para encerrar; não há gravação de áudio em arquivo no código examinado |
| Captura no laboratório Sway | Imagem de tela solicitada | grim para clipboard Wayland por padrão; modo --save grava imagem em pasta de imagens |
| Tupã | Pergunta digitada, identificador de modelo, instrução de sistema do projeto | Ollama em localhost ou API externa escolhida; ChatGPT abre no navegador, sem incorporar automaticamente a conversa; credenciais opcionais por variáveis de ambiente |

O histórico da Confluência é local, mas pode conter informações pessoais, títulos e caminhos sensíveis. Não é memória cognitiva. A preferência de recentes do GNOME controla a coleta e apresentação conforme os adaptadores atuais; desativá-la não é garantia de apagar registros já persistidos. O código não estabelece prazo de retenção temporal geral. Limites de quantidade não equivalem a prazo de eliminação.

## Controle pelo usuário

- Nas preferências de privacidade do GNOME, desative o registro de arquivos recentes se não desejar essa funcionalidade.
- No mapa GTK3, use Aparência e acessibilidade → Limpar histórico e confirme. O aplicativo limpa seu banco de recentes/frequências e solicita limpeza da extensão quando conectada. Isso não apaga arquivos originais, registros de outros aplicativos, backups nem necessariamente todos os vestígios físicos do SQLite.
- Não compartilhe banco de dados, saídas D-Bus contendo janelas, capturas ou logs sem remover dados pessoais. Não os inclua em issues ou releases.
- Não configure microfone ou modelo de voz se não quiser usar essa entrada. O código contém reconhecimento curto iniciado por ação, não escuta contínua; indicadores de captura persistentes ainda precisam de validação.
- Selecione IA desligada quando não quiser usar fornecedores. Consultas externas enviam o texto digitado e a instrução de sistema ao fornecedor escolhido; autenticação, metadados de rede, custos e retenção dependem desse serviço. A opção store=false em uma chamada não garante ausência total de retenção. Não digite segredos ou dados sensíveis.
- O ARANDU não deve compartilhar automaticamente histórico, clipboard, arquivos ou estado dos núcleos de pesquisa com a IA.

## Pendências de privacidade

Confirmar comportamento em sessão bloqueada, limpeza em todos os adaptadores, permissões de diretórios existentes, dados de backups, indicação de microfone e compartilhamento, dependências externas e ausência de tráfego não solicitado. Uma preferência dedicada de histórico, independente da configuração GNOME, e retenção configurável são propostas a avaliar. A substituição dos indicadores do sistema pela Semente só será permitida com equivalência comprovada.

Fontes no código: [model.py](../ARANDU-SUITE/Confluencia/app/model.py), [desktop.py](../ARANDU-SUITE/Confluencia/app/desktop.py), [voice.py](../ARANDU-SUITE/Confluencia/app/voice.py), [Shell](../ARANDU-SUITE/Confluencia/shell/implementation.js.in), [gateway](../ARANDU-DESKTOP/ai_gateway.py), [captura](../ARANDU-DESKTOP/session/capture-screen.sh). Consulte [segurança](../SECURITY.md).

## Etapa de transição dos indicadores

A Semente no candidato consulta data/hora e a preferência GNOME de histórico ao abrir ou atualizar seu painel. Abre, por ação explícita, os menus nativos de calendário/avisos e configurações rápidas quando disponíveis, sem copiar textos de notificações. A revisão seguinte observa passivamente os indicadores nativos de câmera, microfone, gravação e compartilhamento quando disponíveis. Isso não fornece estado independente dos dispositivos; ausência de sinal significa estado desconhecido. Consulte [sinais da Semente](SEMENTE_SINAIS_GNOME.md). A ocultação pela Confluência está suspensa; não altera Hide Top Bar nem garante o estado de extensões externas. O acesso é bloqueado quando a sessão não está autorizada. Testar indicadores reais antes de substituir a barra.
