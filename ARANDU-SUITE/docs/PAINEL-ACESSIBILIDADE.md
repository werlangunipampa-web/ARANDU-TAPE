# ARANDU TAPE — Painel de acessibilidade da Semente (prévia)

## Acesso

- Clique **com o botão direito** sobre a Semente para abrir ou fechar o painel.
- Alternativamente, use o menu **ARANDU TAPE → Acessibilidade · configurar na Semente**.
- O painel oferece ações de teclado com foco visível e rolagem em telas pequenas.

## Controles

| Controle | Opções | Persistência |
|---|---|---|
| Varredura | 5 s → 3,5 s → 2 s | GSettings `scan-interval-ms` |
| Medalhões | 85% → 100% → 120% | GSettings `medallion-scale` |
| Alto contraste | Ligado/desligado | GSettings `high-contrast` |
| Acionador | Super+Alt+Espaço / Super+Alt+S | Atalho GNOME `arandu-varredura-acionar` |
| Barra GNOME | Recuperar barra; ocultação suspensa no candidato | GSettings `panel-mode` |
| Restaurar padrões | 3,5s; 100%; contraste normal; Super+Alt+Espaço; barra visível | Persistente |

**Importante:** a tecla do acionador é uma combinação global definida pelo GNOME, não captura de tecla simples. O teclado ou dispositivo adaptado deve conseguir enviar essa combinação. Atalhos em conflito com outros aplicativos precisam ser reconfigurados.

O painel altera **apenas as preferências da Confluência**. Ele não altera o código da TOPBAR 6.6.1.2 e não habilita câmera, microfone ou serviços de rede.

## Segurança

A varredura continua **desligada por padrão**. Mudar sua velocidade, tamanho ou contraste não ativa aplicativos. Os modos `hidden` e `auto` não são aplicados pela Confluência neste candidato, até validação de indicadores de privacidade equivalentes. Preferências anteriores não são alteradas automaticamente. Super+Alt+B solicita recuperar a barra; se Hide Top Bar controlar a barra, é necessário resolver o conflito manualmente.

A alteração de tamanho é aplicada por escala ao medalhão individual, sem alterar as posições centrais dos rios. Em telas muito pequenas, podem existir sobreposições: avaliar visualmente.

## Validar no GNOME 46/X11

O teste anterior validou movimento e ativação de janelas. **Esta nova versão do painel ainda precisa de teste visual em sessão GNOME real.**

```bash
cd ~/Downloads/ARANDU-TAPE
git pull --ff-only
cd ARANDU-SUITE
bash instalar-tudo.sh --verificar
```

Antes de instalar, salvar os trabalhos e registrar backup da Confluência. Só instalar após a verificação do pacote e confirmar que o commit contém o painel. Depois de reiniciar o GNOME, testar abertura, rolagem, contraste, escala, atalhos e restauração.

Se a extensão falhar, consultar backups do instalador em `~/.local/share/arandu-tape-confluencia/backups/` e usar `gnome-extensions disable confluencia@arandulab` para recuperação sem afetar a TOPBAR.


## Informações da Semente

O mesmo painel oferece data e hora, atualização explícita e estado da preferência GNOME de histórico (não é indicador de câmera/microfone). Botões acessam o calendário/avisos e controles nativos do GNOME, quando a API de menu está disponível; caso contrário, usar a barra. Não copia notificações nem cria monitor residente. Esc fecha o painel; sessão bloqueada impede abertura. A equivalência gráfica e funcional ainda requer testes reais.
