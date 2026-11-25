"""Public desktop action authorization. No research runtime or external IO."""
from dataclasses import dataclass
from types import MappingProxyType

@dataclass(frozen=True)
class Rule:
    purpose: str
    confirmation: bool = False
    provenance: bool = False

RULES = MappingProxyType({
    "navigate_rivers": Rule("Navegação solicitada"),
    "list_windows": Rule("Consulta de janelas sob demanda"),
    "focus_window": Rule("Foco em janela escolhida", True),
    "launch_app": Rule("Abrir aplicativo escolhido", True),
    "close_window": Rule("Fechar janela com confirmação", True),
    "clipboard_capture": Rule("Captura solicitada explicitamente"),
    "bluetooth_connect": Rule("Conectar dispositivo escolhido", True),
    "bluetooth_disconnect": Rule("Desconectar dispositivo escolhido", True),
    "read_system_status": Rule("Consultar indicadores locais"),
    "benchmark": Rule("Medição finita solicitada"),
    "update_code": Rule("Atualizar código com origem e confirmação", True, True),
    "propose_adaptation": Rule("Proposta de ajuste de apresentação"),
    "apply_adaptation": Rule("Ajustar apresentação com confirmação", True),
    "ask_generative_ai": Rule("Enviar texto digitado ao fornecedor escolhido", True),
})

@dataclass(frozen=True)
class Decision:
    allowed: bool
    why: str

def decide(action: str, *, user_intent: bool=False, confirmation: bool=False,
           provenance: bool=False, agent: str="human") -> Decision:
    """Pure allowlist. Caller still validates target, arguments and actual consent."""
    if not isinstance(action, str) or action not in RULES:
        return Decision(False, "Operação não disponível nesta interface")
    if agent != "human":
        return Decision(False, "Ação reservada à pessoa")
    if user_intent is not True:
        return Decision(False, "Solicitação humana explícita necessária")
    rule=RULES[action]
    if rule.confirmation and confirmation is not True:
        return Decision(False, "Confirmação humana necessária")
    if rule.provenance and provenance is not True:
        return Decision(False, "Procedência necessária")
    return Decision(True, rule.purpose)
