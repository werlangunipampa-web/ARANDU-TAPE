"""ARANDU Desktop 0.1 — modelo local e verificável, sem dependências gráficas.

Não lê janelas, não coleta atividade, não altera a Semente oficial.
A lista de aplicativos instalados é obtida somente quando solicitada pela GUI.
"""
from dataclasses import dataclass, field
from typing import Literal

River = Literal["memory", "open", "frequent"]
RIVERS: tuple[River, ...] = ("memory", "open", "frequent")
NAMES = {"memory": "MEMÓRIA", "open": "ABERTOS", "frequent": "FREQUENTES"}


@dataclass
class Session:
    """Contrato de interação isolado da camada GTK."""

    active: bool = False
    river: River | None = None
    bridge_enabled: bool = False  # Nunca habilitar implicitamente a ECA.
    items: dict[str, list[str]] = field(
        default_factory=lambda: {river: [] for river in RIVERS}
    )

    def select(self, river: str) -> None:
        if river not in RIVERS:
            raise ValueError("Rio desconhecido")
        self.active = True
        self.river = river  # type: ignore[assignment]

    def retract(self) -> None:
        self.active = False
        self.river = None

    def read_items(self, river: str) -> tuple[str, ...]:
        if river not in RIVERS:
            raise ValueError("Rio desconhecido")
        return tuple(self.items[river])

    def status(self) -> dict:
        return {
            "prototype": "0.7.4",
            "active": self.active,
            "river": self.river,
            "eca": "isolated",
            "bridge_enabled": self.bridge_enabled,
            "window_provider": "not-connected",
        }
