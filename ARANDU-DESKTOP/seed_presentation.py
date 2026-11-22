"""Adaptador transitório da Confluência — sem mutação da Semente oficial.

Mantém a nomenclatura do arandu-core/CONFLUENCE_SEED.md, com os estados
Collapsed, Aware, Near, Expanded e Pinned. Não substitui o núcleo Rust.
Não inicia timers, sensores, coleta de uso ou consulta a ECA.
"""
from dataclasses import dataclass
from typing import Literal

State = Literal["Collapsed", "Aware", "Near", "Expanded", "Pinned"]


@dataclass
class SeedPresentation:
    state: State = "Collapsed"

    @property
    def expanded(self) -> bool:
        return self.state in ("Expanded", "Pinned")

    def approach(self, proximity: float) -> State:
        """Sinal opcional do adaptador, não lê sensores em background."""
        if not isinstance(proximity, (int, float)):
            raise ValueError("Proximidade inválida")
        if self.expanded:
            return self.state
        if proximity >= 0.75:
            self.state = "Near"
        elif proximity >= 0.25:
            self.state = "Aware"
        else:
            self.state = "Collapsed"
        return self.state

    def expand(self) -> State:
        if self.state != "Pinned":
            self.state = "Expanded"
        return self.state

    def toggle_pin(self) -> State:
        self.state = "Expanded" if self.state == "Pinned" else "Pinned"
        return self.state

    def collapse(self, force: bool = False) -> State:
        if self.state != "Pinned" or force:
            self.state = "Collapsed"
        return self.state
