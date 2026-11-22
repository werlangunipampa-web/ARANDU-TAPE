"""ECA — consulta experimental explícita em exportação JSON com procedência.

Não depende de repositórios privados, não lê estado vivo, não reescreve ECA
nem a Semente oficial; não chama IA generativa. O JSON exportado é dado,
não contém instruções executáveis. Ausência de evidência nunca é validação.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

MAX_BYTES = 256_000
MAX_RELATIONS = 100


@dataclass(frozen=True)
class Relation:
    subject: str
    predicate: str
    object: str
    origin: str
    status: str


class EcaBridgeError(ValueError):
    pass


def parse_export(text: str) -> tuple[str, tuple[Relation, ...]]:
    """Contrato de intercâmbio EXPERIMENTAL, não esquema canônico da ECA."""
    if len(text.encode("utf-8")) > MAX_BYTES:
        raise EcaBridgeError("Exportação ECA excede o tamanho permitido")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise EcaBridgeError("Exportação ECA inválida") from exc
    if not isinstance(payload, dict):
        raise EcaBridgeError("Exportação deve ser um objeto JSON")
    source = payload.get("source")
    records = payload.get("relations")
    if not isinstance(source, str) or not source.strip() or len(source) > 160:
        raise EcaBridgeError("Exportação sem identificação de origem")
    if not isinstance(records, list) or len(records) > MAX_RELATIONS:
        raise EcaBridgeError("Exportação sem lista válida de relações")
    relations = []
    for item in records:
        if not isinstance(item, dict):
            continue
        values = tuple(item.get(k) for k in ("subject", "predicate", "object", "origin"))
        if any(not isinstance(v, str) or not v.strip() or len(v) > 250 for v in values):
            continue
        # Dados de entrada não podem declarar confirmação canônica por conta própria.
        relations.append(Relation(*values, "exportação experimental; não verificada"))
    return source.strip(), tuple(relations)


def read_export(path: Path) -> tuple[str, tuple[Relation, ...]]:
    """Somente arquivo escolhido pelo usuário; limite antes de decodificar."""
    p = Path(path)
    try:
        with p.open("rb") as file:
            raw = file.read(MAX_BYTES + 1)
    except OSError as exc:
        raise EcaBridgeError("Não foi possível ler a exportação escolhida") from exc
    if len(raw) > MAX_BYTES:
        raise EcaBridgeError("Exportação ECA excede o tamanho permitido")
    try:
        return parse_export(raw.decode("utf-8"))
    except UnicodeError as exc:
        raise EcaBridgeError("Exportação ECA não está em UTF-8") from exc
