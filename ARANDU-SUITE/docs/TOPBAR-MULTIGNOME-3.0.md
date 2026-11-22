# ARANDU SUITE 3.0 — TOPBAR unificada (prévia experimental)

## Arquitetura

O comando `ARANDU-SUITE/instalar-tudo.sh` administra dois componentes:

- **Confluência:** Semente, três rios, medalhões e ponte de comandos assistivos.
- **ARANDU TOPBAR:** identidade visual da barra superior.

A TOPBAR continua uma extensão GNOME separada, para respeitar o carregamento e a desativação de extensões do Shell. O **instalador é único** e não pede duas instalações ao usuário.

## Seleção por versão

| GNOME Shell | TOPBAR | Ativação |
|---|---|---|
| 46 | Histórico 6.6.1.2 preservado | Como atualmente, após reiniciar o GNOME |
| 45, 47–51 | Variante ESM defensiva, experimental | Somente com `--experimental-topbar` |
| 40–44 | Sem variante TOPBAR validada | Não ativar automaticamente |
| Versões futuras | Não confirmadas | Validar antes de instalar |

A variante moderna vive em `TOPBAR/modern/`. O instalador **não modifica** o código histórico sob `TOPBAR/arandu-topbar@local/`. Uma TOPBAR já instalada é preservada no destino.

**Importante:** indicar uma versão em `metadata.json` não comprova compatibilidade. As APIs internas do GNOME podem mudar mesmo em versões que suportam módulos ES. A matriz acima indica uma estratégia de construção e testes, não uma certificação.

## Como instalar

```bash
cd ~/Downloads/ARANDU-TAPE
git pull --ff-only
cd ARANDU-SUITE
bash instalar-tudo.sh --preflight
bash instalar-tudo.sh --verificar
bash instalar-tudo.sh
```

Depois de reiniciar a sessão:

```bash
bash instalar-tudo.sh --status
```

Para **testes controlados** num GNOME moderno diferente de 46, use uma conta/sessão de teste sem TOPBAR histórica previamente instalada:

```bash
bash instalar-tudo.sh --experimental-topbar
```

Reinicie a sessão. O instalador não substitui automaticamente uma TOPBAR existente por outra variante.

## Segurança e recuperação

- Não execute como `sudo`.
- Preserve backups e dados pessoais.
- Se houver problemas, use `gnome-extensions disable arandu-topbar@local` para desligar a barra sem desinstalar a Confluência.
- Em GNOME X11 use `Alt+F2`, `r` após salvar os trabalhos; em Wayland encerre e reabra a sessão.
- A barra da Confluência pode permanecer visível em `panel-mode visible`.
- Nenhum recurso de voz/câmera é ligado automaticamente.

## Testes pendentes

Verificar GNOME 45, 47, 48, 49, 50 e 51 em sessão real, X11/Wayland quando suportado, segurança de foco, restaurar estilo do painel, teclas assistivas e retorno da barra após atualização. Esses testes são necessários antes de habilitar por padrão em outros ambientes.
