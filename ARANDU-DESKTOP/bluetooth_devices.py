"""Adaptador Bluetooth local da Semente: consulta sob demanda, sem vigilância.

Pareamento novo é responsabilidade do gerenciador gráfico BlueZ/Blueman.
Conectar/desconectar requer clique explícito e dispositivo pareado verificado.
"""
from __future__ import annotations

import re
import shutil
import subprocess

MAC = re.compile(r"^[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}$")
DEVICE = re.compile(r"^Device\s+([0-9A-Fa-f:]{17})\s+(.+)$")


def _run(args: list[str], timeout: float = 4) -> tuple[bool, str]:
    if not shutil.which("bluetoothctl"):
        return False, "bluetoothctl não instalado"
    try:
        result = subprocess.run(["bluetoothctl", *args], capture_output=True,
                                text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return False, "Bluetooth indisponível ou operação excedeu o tempo"
    message = (result.stdout or "") + "\n" + (result.stderr or "")
    return result.returncode == 0, message.strip()[:1200]


def parse_devices(output: str) -> tuple[dict[str, str], ...]:
    devices = []
    seen = set()
    for line in output.splitlines():
        match = DEVICE.match(line.strip())
        if match is None:
            continue
        address, name = match.groups()
        if not MAC.fullmatch(address) or address.upper() in seen:
            continue
        seen.add(address.upper())
        devices.append({"address": address.upper(), "name": name[:120].strip()})
    return tuple(devices[:20])


def paired_devices() -> tuple[dict[str, str | bool], ...]:
    """Lista pareados reais; não confunde vizinhos detectados com autorizados."""
    ok, listing = _run(["devices", "Paired"])
    if not ok:
        # BlueZ antigo não suporta o filtro e expõe 'paired-devices'.
        ok, listing = _run(["paired-devices"])
    if not ok:
        return ()
    results = []
    for item in parse_devices(listing):
        info_ok, details = _run(["info", item["address"]], timeout=2)
        connected = False
        if info_ok:
            connected = any(line.strip() == "Connected: yes"
                            for line in details.splitlines())
        results.append({**item, "connected": connected})
    return tuple(results)


def device_action(address: str, action: str) -> tuple[bool, str]:
    """Pareado novamente conferido imediatamente antes de qualquer operação."""
    if action not in ("connect", "disconnect") or not isinstance(address, str):
        return False, "Operação recusada"
    if MAC.fullmatch(address) is None:
        return False, "Endereço Bluetooth inválido"
    normalized = address.upper()
    if normalized not in {item["address"] for item in paired_devices()}:
        return False, "Dispositivo não pareado; use o gerenciador Bluetooth"
    ok, message = _run([action, normalized], timeout=16)
    if ok and ("successful" in message.lower() or
               "connection successful" in message.lower() or
               "disconnection successful" in message.lower()):
        return True, "Conectado" if action == "connect" else "Desconectado"
    if not ok:
        return False, "Falha ao " + ("conectar" if action == "connect" else "desconectar") + ": " + message[:280]
    return False, "Não houve confirmação de sucesso: " + message[:280]


def pairing_manager() -> list[str] | None:
    """Caminho gráfico disponível, sem modificação de serviços ou pacotes."""
    found = shutil.which("blueman-manager")
    if found:
        return [found]
    found = shutil.which("gnome-control-center")
    if found:
        return [found, "bluetooth"]
    return None
