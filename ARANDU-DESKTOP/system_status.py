"""Indicadores da Semente: leitura local pontual, sem dados fictícios ou telemetria."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import socket
import subprocess


def battery_status(root: Path = Path("/sys/class/power_supply")) -> str:
    try:
        batteries = [d for d in root.iterdir() if d.is_dir() and
                     (d / "type").read_text().strip() == "Battery"]
    except OSError:
        return "Sem bateria detectada"
    if not batteries:
        return "Sem bateria detectada"
    battery = batteries[0]
    try:
        percentage = int((battery / "capacity").read_text().strip())
        status = (battery / "status").read_text().strip()
        return f"Bateria {percentage}% · {status}"
    except (OSError, ValueError):
        return "Bateria indisponível"


def network_status(route_file: Path = Path("/proc/net/route")) -> str:
    # Rota padrão local não comprova conectividade com a Internet.
    try:
        lines = route_file.read_text().splitlines()[1:]
        if any(len(fields := line.split()) > 3 and
               fields[1] == "00000000" and int(fields[3], 16) & 1 for line in lines):
            return "Rede configurada · Internet não verificada"
        return "Sem rota IPv4 padrão detectada"
    except (OSError, ValueError):
        return "Rede indisponível"


def run_status(command: list[str], timeout: float = 1.5) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=timeout, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def bluetooth_status() -> str:
    output = run_status(["bluetoothctl", "show"])
    if output is None:
        return "Bluetooth indisponível"
    for line in output.splitlines():
        if line.strip().startswith("Powered:"):
            return "Bluetooth ligado" if line.split(":", 1)[1].strip().lower() == "yes" else "Bluetooth desligado"
    return "Nenhum adaptador Bluetooth detectado"


def volume_status() -> str:
    output = run_status(["pactl", "get-sink-volume", "@DEFAULT_SINK@"])
    muted = run_status(["pactl", "get-sink-mute", "@DEFAULT_SINK@"])
    if output is None:
        return "Som indisponível"
    import re
    match = re.search(r"\b(\d{1,3})%", output)
    if not match:
        return "Som sem volume informado"
    return "Som mudo" if muted and muted.endswith("yes") else f"Som {match.group(1)}%"


def clock_text() -> str:
    return datetime.now().strftime("%H:%M")


def summary() -> dict[str, str]:
    return {"clock": clock_text(), "network": network_status(),
            "battery": battery_status(), "bluetooth": bluetooth_status(),
            "sound": volume_status()}
