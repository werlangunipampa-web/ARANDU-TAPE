"""ARANDU — adaptação situada, reversível e mensurável.

Observação finita, proposta sem execução e alteração apenas da apresentação
do próprio ARANDU após ação humana. Nenhum ajuste de kernel, CPU governor,
dispositivos, ECA, identidade, aplicativos ou serviços. O modelo generativo
pode explicar sugestões, mas não chama apply().
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Mode = Literal["equilibrado", "economico"]


@dataclass(frozen=True)
class Snapshot:
    battery_percent: int | None
    charging: bool | None
    available_memory_percent: float | None


@dataclass(frozen=True)
class Proposal:
    mode: Mode
    rationale: str
    source: str
    requires_confirmation: bool = True


def observe(root: Path = Path("/sys/class/power_supply"),
            meminfo: Path = Path("/proc/meminfo")) -> Snapshot:
    """Sem rede e sem processos residentes; cada observação é solicitada."""
    percent = None
    charging = None
    try:
        for device in root.iterdir():
            if not device.is_dir() or (device / "type").read_text().strip() != "Battery":
                continue
            value = int((device / "capacity").read_text().strip())
            if 0 <= value <= 100:
                percent = value
            status = (device / "status").read_text().strip().lower()
            charging = status in ("charging", "full")
            break
    except (OSError, ValueError):
        pass
    available = None
    try:
        entries = {}
        for line in meminfo.read_text().splitlines():
            name, _, value = line.partition(":")
            if name in ("MemTotal", "MemAvailable"):
                entries[name] = int(value.strip().split()[0])
        if entries.get("MemTotal", 0) > 0 and "MemAvailable" in entries:
            available = round(100.0 * entries["MemAvailable"] / entries["MemTotal"], 1)
    except (OSError, ValueError, IndexError):
        pass
    return Snapshot(percent, charging, available)


def propose(snapshot: Snapshot, current: Mode = "equilibrado",
            preference: Mode | None = None) -> Proposal | None:
    """Priorização explícita do usuário precede economia sugerida."""
    if preference is not None:
        if preference not in ("equilibrado", "economico"):
            raise ValueError("Preferência de apresentação desconhecida")
        if preference != current:
            return Proposal(preference, "Preferência solicitada pela pessoa", "usuario")
        return None
    if snapshot.battery_percent is not None and snapshot.charging is False:
        if snapshot.battery_percent <= 25 and current != "economico":
            return Proposal("economico",
                            f"Bateria em {snapshot.battery_percent}% fora da tomada; "
                            "reduzir movimento e consultas de layout do ARANDU.",
                            "hardware-local")
    if snapshot.available_memory_percent is not None:
        if snapshot.available_memory_percent < 12 and current != "economico":
            return Proposal("economico",
                            "Memória disponível baixa. Reduzir somente efeitos da interface; "
                            "nenhum aplicativo será fechado automaticamente.",
                            "hardware-local")
    return None


class Adaptation:
    def __init__(self):
        self.mode: Mode = "equilibrado"
        self.previous: Mode | None = None

    def apply(self, proposal: Proposal, confirmed: bool = False) -> bool:
        if not confirmed or proposal.mode not in ("economico", "equilibrado"):
            return False
        if proposal.mode == self.mode:
            return False
        self.previous = self.mode
        self.mode = proposal.mode
        return True

    def undo(self) -> bool:
        if self.previous is None:
            return False
        self.mode, self.previous = self.previous, None
        return True
