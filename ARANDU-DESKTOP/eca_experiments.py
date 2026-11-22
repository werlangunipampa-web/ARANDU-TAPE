"""ECA Lab — evolução cognitiva experimental sem autoexecução.

A ECA pode propor refinamentos de relações, diferenciação progressiva e
reconciliação integrativa. O experimento só avalia dados sintéticos fornecidos
explicitamente e não executa código, altera ontologia ou promove gerações.

Mudança de código/arquitetura real é uma etapa SEPARADA: proposta revisada,
sandbox, testes, relatório, aprovação humana e integração versionada.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CognitiveOperation = Literal[
    "diferenciacao_progressiva", "reconciliacao_integrativa",
    "ancoragem_subsuncor",
]
OPERATIONS = ("diferenciacao_progressiva", "reconciliacao_integrativa",
              "ancoragem_subsuncor")


@dataclass(frozen=True)
class CognitiveProposal:
    operation: CognitiveOperation
    objective: str
    concept_before: str
    concept_after: str
    evidence_origin: str
    justification: str


@dataclass(frozen=True)
class Evaluation:
    valid: bool
    reasons: tuple[str, ...]
    experimental: bool = True
    official_state_changed: bool = False
    code_executed: bool = False


def evaluate(proposal: CognitiveProposal) -> Evaluation:
    """Gate de integridade, não validação epistemológica final.

    Validade = completude estrutural e procedência declarada; confirmar
    aprendizagem significativa requer observações, instrumentos e humano.
    """
    issues = []
    if proposal.operation not in OPERATIONS:
        issues.append("Operação cognitiva desconhecida")
    for attr in ("objective", "concept_before", "concept_after",
                 "evidence_origin", "justification"):
        item = getattr(proposal, attr, None)
        if not isinstance(item, str) or not item.strip() or len(item) > 300:
            issues.append("Campo ausente ou inválido: " + attr)
    if proposal.concept_before == proposal.concept_after:
        issues.append("Não há diferenciação observável entre os conceitos")
    return Evaluation(valid=not issues, reasons=tuple(issues))


def workflow() -> tuple[str, ...]:
    """Nenhuma transição é executada: fases obrigatórias para projeto real."""
    return (
        "1. formular hipótese de aprendizagem significativa com objetivo definido",
        "2. identificar subsunçores, evidências e procedência da relação",
        "3. simular em cópia isolada sem acesso à Semente oficial",
        "4. medir resultados contra referência e testar explicações alternativas",
        "5. auditar consistência epistemológica, código, segurança e consumo",
        "6. solicitar aprovação humana explícita e registrar versão",
        "7. implantar somente por mecanismo reversível autorizado",
    )
