"""Geometria nativa da Confluência reutilizada sem importar código do GNOME."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "ARANDU-SUITE" / "Confluencia" / "app" / "assets"
WIDTH, HEIGHT = 1200, 500
SEED = (642.0, 355.0)


def paths():
    data = json.loads((ASSETS / "geometria.json").read_text(encoding="utf-8"))
    expected = ("memory", "open", "frequent")
    for river in expected:
        points = data.get(river)
        if not isinstance(points, list) or len(points) != 5:
            raise ValueError(f"Geometria incompleta: {river}")
        for pair in points:
            if len(pair) != 2 or not all(isinstance(v, (float, int)) for v in pair):
                raise ValueError(f"Coordenadas inválidas: {river}")
    return {river: tuple(tuple(float(x) for x in point) for point in data[river])
            for river in expected}


def assets_exist():
    return all((ASSETS / filename).is_file() for filename in
               ("rios.svg", "semente.svg", "memory.svg", "open.svg", "frequent.svg"))
