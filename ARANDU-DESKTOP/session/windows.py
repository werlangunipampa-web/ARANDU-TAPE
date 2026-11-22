"""Observação opt-in e somente leitura das janelas do compositor ARANDU Lab.

Não importa GNOME Shell, não registra frequência, não toca em memória ECA.
Chame list_windows() explicitamente; nunca executa ao iniciar.
"""
import json
import os
import subprocess


def flatten_windows(node):
    if not isinstance(node, dict):
        return ()
    found = []
    def walk(current):
        if not isinstance(current, dict):
            return
        app_id = current.get("app_id")
        props = current.get("window_properties") or {}
        wm_class = props.get("class")
        title = current.get("name")
        if (app_id or wm_class) and title and isinstance(current.get("id"), int):
            found.append({
                "id": current["id"],
                "title": str(title),
                "app": str(app_id or wm_class),
            })
        for key in ("nodes", "floating_nodes"):
            for child in current.get(key) or []:
                walk(child)
    walk(node)
    return tuple(found)


def list_windows():
    """Somente quando solicitado; nenhum histórico/persistência. Requires SWAYSOCK."""
    if not os.environ.get("SWAYSOCK"):
        return ()
    result = subprocess.run(
        ["swaymsg", "-r", "-t", "get_tree"],
        capture_output=True, text=True, timeout=3, check=True,
    )
    return flatten_windows(json.loads(result.stdout))
