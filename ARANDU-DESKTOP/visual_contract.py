"""Validação da geometria responsiva sem carregar GTK4.

Fonte de verdade: arquivos SVG e geometria originais da Confluência.
"""
from layout import WIDTH, HEIGHT, SEED, paths

SCALE = 0.75


def scaled(value):
    return round(value * SCALE)


def compact_geometry():
    markers = {
        river: tuple((scaled(x), scaled(y)) for x, y in points)
        for river, points in paths().items()
    }
    return {
        "scale": SCALE,
        "size": (scaled(WIDTH), scaled(HEIGHT)),
        "seed": (scaled(SEED[0]), scaled(SEED[1])),
        "markers": markers,
    }
