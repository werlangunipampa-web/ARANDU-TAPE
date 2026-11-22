"""ARANDU Desktop — controle transversal das intenções segundo AO-0000/AO-0001.

Estas são regras DERIVADAS para adaptadores do desktop, não uma reescrita da
Constituição ontológica. Sem acesso a SeedHome, G3/G4, ECA viva ou arquivos
pessoais. Toda decisão é em memória e não cria falsa autobiografia.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# Fontes lidas em 22/11/2026:
# ARANDU-G4-PRIVATE/docs/ontology/AO-0000.md (invariantes G1)
# ARANDU-G4-PRIVATE/docs/ontology/AO-0001-PERCEPCAO-SITUADA.md (G2)
# arandu-core/docs/CONFLUENCE_SEED.md
# ARANDU-ECA-PRIVATE/README.md (ECA-001 pré-geracional)
#
# AO-0000: identidade distinta de geração e Corpo, causalidade sem relógio
# global, registros arqueológicos não são memória, autorização de nidação,
# memória bruta não é compartilhada automaticamente, legado não vira
# autobiografia. AO-0001: sinal ≠ evidência ≠ compreensão, procedência,
# nenhuma captura sensível por padrão, interpretação provisória.

PILLARS: tuple[str, ...] = (
    "informacao", "ambiente", "continuidade",
    "emergencia", "identidade", "ontologia",
)
# Eixos de engenharia, não uma declaração de axiomas completos.
@dataclass(frozen=True)
class Rule:
    pillar: str
    source: str
    purpose: str
    confirmation: bool = False
    evidence: bool = False
    forbidden: bool = False


RULES: dict[str, Rule] = {
    "navigate_rivers": Rule("continuidade", "CONFLUENCE_SEED",
                            "Revelar navegação somente por intenção"),
    "list_windows": Rule("ambiente", "AO-0001",
                         "Consultar janelas da sessão ativa sob demanda"),
    "focus_window": Rule("continuidade", "CONFLUENCE_SEED",
                         "Foco em janela real e recuperável", confirmation=True),
    "launch_app": Rule("identidade", "AO-0000",
                       "Aplicativo escolhido pela pessoa", confirmation=True),
    "close_window": Rule("continuidade", "AO-0000",
                         "Fechar janela com possibilidade de cancelar",
                         confirmation=True),
    "clipboard_capture": Rule("informacao", "AO-0001",
                              "Capturar somente sob pedido explícito"),
    "bluetooth_connect": Rule("ambiente", "AO-0001",
                              "Conectar apenas dispositivo pareado selecionado",
                              confirmation=True),
    "bluetooth_disconnect": Rule("ambiente", "AO-0001",
                                 "Desconectar dispositivo selecionado",
                                 confirmation=True),
    "read_system_status": Rule("ambiente", "AO-0001",
                               "Distinguir indicadores locais de Internet comprovada"),
    "benchmark": Rule("ambiente", "AO-0001",
                      "Medição finita do equipamento, não memória cognitiva"),
    "update_code": Rule("continuidade", "AO-0000",
                        "Atualizar com versão, origem e confirmação", confirmation=True,
                        evidence=True),
    "consult_eca_export": Rule("informacao", "ECA-001",
                               "Importação experimental com origem identificada",
                               evidence=True),
    "propose_eca_learning": Rule("emergencia", "ECA-001",
                                 "Hipótese experimental; não promoção ontológica",
                                 evidence=True),
    "propose_adaptation": Rule("ambiente", "AO-0001",
                               "Proposta reversível sem executar mudanças"),
    "apply_adaptation": Rule("continuidade", "AO-0000",
                             "Ajustar somente a interface com aprovação",
                             confirmation=True),
    "ask_generative_ai": Rule("informacao", "AO-0001",
                              "Enviar apenas texto explicitamente digitado",
                              confirmation=True),
    "read_official_seed": Rule("identidade", "AO-0000",
                               "A interface não tem acesso ao estado oficial",
                               forbidden=True),
    "modify_official_seed": Rule("identidade", "AO-0000",
                                 "Interface não modifica identidade oficial",
                                 forbidden=True),
    "promote_generation": Rule("ontologia", "AO-0000",
                               "Não promover geração via interface",
                               forbidden=True),
    "execute_ai_generated_code": Rule("emergencia", "ECA-001",
                                      "Modelo de linguagem não executa código",
                                      forbidden=True),
    "silently_collect_history": Rule("informacao", "AO-0001",
                                     "Histórico não coletado por padrão",
                                     forbidden=True),
}


@dataclass(frozen=True)
class Decision:
    allowed: bool
    why: str
    source: str = "nenhuma"
    pillar: str = "ontologia"


def decide(action: str, *, user_intent: bool = False,
           confirmation: bool = False, provenance: bool = False,
           agent: Literal["human", "generative_ai"] = "human") -> Decision:
    """Fail-closed: modelo generativo só consulta/propõe, nunca executa.

    O chamador deve confirmar também a identidade do recurso, os parâmetros,
    a validade do dispositivo e os limites específicos da operação.
    """
    rule = RULES.get(action)
    if rule is None:
        return Decision(False, "Ação desconhecida: negar por padrão")
    if rule.forbidden:
        return Decision(False, "Invariante ontológica impede esta operação",
                        rule.source, rule.pillar)
    if not user_intent:
        return Decision(False, "Ausência de solicitação humana explícita",
                        rule.source, rule.pillar)
    if agent != "human" and (rule.confirmation or
                              action in ("consult_eca_export", "propose_eca_learning")):
        return Decision(False, "IA generativa não é autoridade executora",
                        rule.source, rule.pillar)
    if rule.confirmation and not confirmation:
        return Decision(False, "Confirmação humana necessária",
                        rule.source, rule.pillar)
    if rule.evidence and not provenance:
        return Decision(False, "Procedência/evidência ausente",
                        rule.source, rule.pillar)
    return Decision(True, rule.purpose, rule.source, rule.pillar)


def validate_manifest() -> bool:
    """Todo contrato precisa de princípio, origem e finalidade verificáveis."""
    return all(r.pillar in PILLARS and bool(r.source) and bool(r.purpose)
               for r in RULES.values())
