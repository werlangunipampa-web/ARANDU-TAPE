"""Pure, experimental intent classifier for Alça Viva; no window operations.

Coordinates are logical pixels relative to the start of a dedicated handle drag.
An adapter must bind a valid window at press, cancel on focus loss, distinguish
panels from windows, confirm closing and revalidate target on release.
"""
from math import isfinite

MIN_TRAVEL = 48
MIN_DIAGONAL = 32
AXIS_RATIO = 2.0
HEADER_MIN_HEIGHT = 52
RESIZE_PREVIEW_MIN = 12


def classify_handle(dx, dy, *, released=False, cancelled=False, target="window"):
    """Classify only a completed deliberate drag; never execute any action."""
    if not released or cancelled or target not in ("window", "panel"):
        return None
    if any(type(v) not in (int, float) or not isfinite(v) for v in (dx, dy)):
        return None
    ax, ay = abs(dx), abs(dy)
    # Separate vertical and diagonal zones; ambiguous angles do nothing.
    if ay >= MIN_TRAVEL and ay >= AXIS_RATIO * ax:
        if target == "panel":
            return "recolher_painel" if dy > 0 else None
        return "imersao" if dy < 0 else "recolher_ao_rio"
    if dy <= -MIN_DIAGONAL and ax >= MIN_DIAGONAL and 0.67 <= ax / ay <= 1.5:
        return "solicitar_encerramento" if target == "window" else "fechar_painel"
    return None


def corner_intent(corner, *, activated=False, preview=False, cancelled=False):
    """Hover only reveals controls. Resize requires a preview and confirmation."""
    if cancelled or not activated:
        return None
    if corner == "upper_right":
        return "imersao"
    if corner == "lower_right" and preview:
        return "confirmar_redimensionamento"
    return None
