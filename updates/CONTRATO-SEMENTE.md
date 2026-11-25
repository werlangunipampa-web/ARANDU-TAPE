# Contrato Semente ↔ ARANDU Update v0.1

A Semente **não** chama o GitHub, instala pacotes, executa shell ou solicita senha.
O verificador iniciado na sessão grava um JSON em `~/.cache/arandu/updates/status.json`.
O adaptador `client/semente_bridge.py` interpreta esse JSON e produz uma resposta segura.

## Interface pública
```json
{
  "schema": 1,
  "component": "arandu-update",
  "indicator": "hidden",
  "message": "",
  "action": "open-center",
  "install_enabled": false,
  "release_verified": false
}
```

`indicator` admite `hidden` e `informational` nesta fase. 
`informational` significa apenas release estável anunciada remotamente, **não** atualização disponível, verificada ou compatível.

## Regras de interface
- A Semente lê o estado **somente quando seu módulo de integração tiver sido testado**. É obrigatório inspecionar primeiro o código real de `confluencia@arandulab` e respeitar a Alça Viva, Rios, acessibilidade e privacidade.
- Indicador deve ser pequeno, discreto e acionado apenas por solicitação/estado realmente importante; falhas de consulta não geram alerta persistente.
- A única ação inicial é abrir o aplicativo desktop `arandu-update.desktop`, por método seguro do shell (sem shell string executável ou privilégios).
- Nenhum popup automático, atualização aplicada, permissão administrativa ou controle de instalação.
- Futuramente: mostrar “atualização disponível” somente após comparar versão local confiável, assinatura do manifesto, versão mínima suportada, canal, hash, compatibilidade e elegibilidade de instalação.
- Evitar processos permanentes, polling curto e rede dentro da thread de UI do GNOME Shell.

## Pendências
1. Inspecionar a extensão Semente efetivamente instalada e seu código de origem.
2. Testar adaptador, acessibilidade, fallback e sessão X11/Wayland.
3. Introduzir versão local assinada e verificar autenticidade/compatibilidade.
4. Implementar sinal visual nativo e abertura da Central.
