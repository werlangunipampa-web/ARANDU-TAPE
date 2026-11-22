#!/usr/bin/env python3
"""Observatório ARANDU: leitura local opt-in de /proc, sem coleta contínua."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from datetime import datetime, timezone


def memory_kib(text: str) -> dict[str, int]:
    data = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].endswith(":"):
            try:
                data[parts[0][:-1]] = int(parts[1])
            except ValueError:
                pass
    return data


def snapshot_mem(meminfo: str) -> dict:
    values = memory_kib(meminfo)
    total = values["MemTotal"]
    available = values["MemAvailable"]
    return {
        "total_mib": round(total / 1024, 1),
        "available_mib": round(available / 1024, 1),
        "used_excluding_reclaimable_mib": round((total - available) / 1024, 1),
        "swap_used_mib": round((values.get("SwapTotal", 0) - values.get("SwapFree", 0)) / 1024, 1),
    }


def process_info(pid: int, proc_root: Path = Path("/proc")) -> dict | None:
    base = proc_root / str(pid)
    try:
        statm = (base / "status").read_text()
        info = memory_kib(statm)
        name = next((line.split(":", 1)[1].strip() for line in statm.splitlines()
                     if line.startswith("Name:")), "desconhecido")
        rss = info.get("VmRSS", 0)
        return {"pid": pid, "name": name[:48], "rss_mib": round(rss / 1024, 1)}
    except (OSError, ValueError):
        return None


def collect(proc_root: Path = Path("/proc"), limit: int = 12) -> dict:
    mem = snapshot_mem((proc_root / "meminfo").read_text())
    processes = []
    for child in proc_root.iterdir():
        if child.name.isdecimal():
            item = process_info(int(child.name), proc_root)
            if item is not None:
                processes.append(item)
    processes.sort(key=lambda x: x["rss_mib"], reverse=True)
    try:
        one, five, fifteen, *_ = (proc_root / "loadavg").read_text().split()
        loads = {"one_min": float(one), "five_min": float(five),
                 "fifteen_min": float(fifteen)}
    except (OSError, ValueError):
        loads = None
    return {
        "schema": 1,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_desktop": os.environ.get("XDG_SESSION_DESKTOP", "desconhecido"),
        "session_type": os.environ.get("XDG_SESSION_TYPE", "desconhecido"),
        "memory": mem,
        "load_average": loads,
        "logical_cpus": os.cpu_count(),
        "load_note": "Load average mede tarefas em espera/execução; NÃO é porcentagem de CPU.",
        "top_processes": processes[:limit],
        "process_rss_note": "RSS por processo pode compartilhar páginas; não somar como total único.",
        "comparison_note": "Comparar sessões com mesmo hardware, uptime, aplicativos e condições.",
    }


def main():
    parser = argparse.ArgumentParser(description="Métricas locais ARANDU /proc")
    parser.add_argument("--save", type=Path, help="Salvar JSON somente quando solicitado")
    parser.add_argument("--top", type=int, default=12, help="Quantidade de processos, 1..30")
    args = parser.parse_args()
    if not 1 <= args.top <= 30:
        parser.error("--top deve estar entre 1 e 30")
    output = json.dumps(collect(limit=args.top), ensure_ascii=False, indent=2)
    if args.save:
        path = args.save.expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(output + "\n")
        print(f"Relatório salvo: {path}")
    else:
        print(output)


if __name__ == "__main__":
    main()
