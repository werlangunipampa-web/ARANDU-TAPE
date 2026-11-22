#!/usr/bin/env python3
"""Benchmark ARANDU: amostras finitas de CPU/RAM, arquivos somente por escolha explícita."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import statistics
import time

from performance import snapshot_mem


def cpu_ticks(text: str) -> tuple[int, int]:
    first = text.splitlines()[0].split()
    if not first or first[0] != "cpu" or len(first) < 5:
        raise ValueError("Estatística de CPU indisponível")
    values = [int(x) for x in first[1:]]
    idle = values[3] + (values[4] if len(values) > 4 else 0)
    return (sum(values), idle)


def cpu_percent(previous: tuple[int, int], current: tuple[int, int]) -> float:
    delta_total = current[0] - previous[0]
    delta_idle = current[1] - previous[1]
    if delta_total <= 0 or delta_idle < 0 or delta_idle > delta_total:
        raise ValueError("Intervalo de CPU inválido")
    return round(100 * (1 - delta_idle / delta_total), 2)


def summarize(samples: list[dict]) -> dict:
    if not samples:
        raise ValueError("Nenhuma amostra")
    result = {"count": len(samples)}
    for metric in ("ram_used_mib", "ram_available_mib", "cpu_percent", "swap_used_mib"):
        values = [float(s[metric]) for s in samples]
        result[metric] = {
            "mean": round(statistics.mean(values), 2),
            "median": round(statistics.median(values), 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
        }
    return result


def sample_session(count: int = 5, interval: float = 1.0,
                   proc_root: Path = Path("/proc"), sleep=time.sleep) -> dict:
    if not 2 <= count <= 20 or not 0.5 <= interval <= 5.0:
        raise ValueError("Amostras: 2–20; intervalo: 0,5–5 segundos")
    samples = []
    previous = cpu_ticks((proc_root / "stat").read_text())
    for _ in range(count):
        sleep(interval)
        current = cpu_ticks((proc_root / "stat").read_text())
        ram = snapshot_mem((proc_root / "meminfo").read_text())
        samples.append({
            "cpu_percent": cpu_percent(previous, current),
            "ram_used_mib": ram["used_excluding_reclaimable_mib"],
            "ram_available_mib": ram["available_mib"],
            "swap_used_mib": ram["swap_used_mib"],
        })
        previous = current
    return {
        "schema": "arandu-benchmark-v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session": os.environ.get("XDG_SESSION_DESKTOP", "desconhecida"),
        "session_type": os.environ.get("XDG_SESSION_TYPE", "desconhecido"),
        "logical_cpus": os.cpu_count(),
        "interval_seconds": interval,
        "summary": summarize(samples),
        "samples": samples,
        "limitations": (
            "Métricas do computador inteiro, não somente do desktop. "
            "MemAvailable considera cache recuperável. Comparações requerem "
            "mesmo equipamento, aplicativos, carga e condições."
        ),
    }


def read_report(path: Path) -> dict:
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("schema") != "arandu-benchmark-v1":
        raise ValueError("Relatório incompatível")
    for metric in ("ram_used_mib", "cpu_percent"):
        value = report["summary"][metric]["median"]
        if not isinstance(value, (int, float)) or not 0 <= value < 100000000:
            raise ValueError("Métrica inválida")
    return report


def compare_reports(a: dict, b: dict) -> dict:
    metrics = {}
    for key in ("ram_used_mib", "cpu_percent", "swap_used_mib"):
        av = float(a["summary"][key]["median"])
        bv = float(b["summary"][key]["median"])
        metrics[key] = {"a_median": av, "b_median": bv,
                        "b_minus_a": round(bv - av, 2)}
    return {"session_a": a.get("session"), "session_b": b.get("session"),
            "metrics": metrics,
            "warning": "Diferenças são do sistema inteiro; não provam ganho causado pelo desktop."}


def write_private_new(path: Path, content: str) -> None:
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        output.write(content + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Comparar desempenho ARANDU/GNOME sem telemetria")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--measure", action="store_true", help="Executar medição finita")
    mode.add_argument("--compare", nargs=2, metavar=("A.json", "B.json"))
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--save", type=Path, help="Gravar JSON privado somente se solicitado")
    args = parser.parse_args()
    if args.compare:
        result = compare_reports(read_report(Path(args.compare[0])),
                                 read_report(Path(args.compare[1])))
    else:
        result = sample_session(args.count, args.interval)
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.save:
        write_private_new(args.save, rendered)
        print(f"Relatório salvo em: {args.save}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
