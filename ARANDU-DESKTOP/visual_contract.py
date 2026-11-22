"""Contratos puros da geometria e dos medalhões, independentes de GTK e GNOME."""
from layout import WIDTH, HEIGHT, SEED, paths

DEFAULT_SCALE = 0.75
MIN_SCALE = 0.48
MAX_SCALE = 1.0


def scale_for_viewport(width, height=500):
    """Maior escala proporcional que cabe na área oferecida, sem ampliar além de 100%."""
    if width <= 0 or height <= 0:
        return DEFAULT_SCALE
    return max(MIN_SCALE, min(MAX_SCALE, width / WIDTH, height / HEIGHT))


def scaled(value, scale=DEFAULT_SCALE):
    return round(value * scale)


def compact_geometry(scale=DEFAULT_SCALE):
    markers = {
        river: tuple((scaled(x, scale), scaled(y, scale)) for x, y in points)
        for river, points in paths().items()
    }
    return {
        "scale": scale,
        "size": (scaled(WIDTH, scale), scaled(HEIGHT, scale)),
        "seed": (scaled(SEED[0], scale), scaled(SEED[1], scale)),
        "markers": markers,
    }


def choose_app_slots(applications, limit=15):
    """Seleciona somente aplicativos fornecidos pelo usuário, nunca janelas inferidas."""
    if limit < 0:
        raise ValueError("Limite inválido")
    return tuple(applications[:limit])
