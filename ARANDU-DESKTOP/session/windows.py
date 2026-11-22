"""Ponte opt-in com janelas da sessão Sway aninhada.

Sway IPC apenas mediante clique, sem observação contínua, logs nem persistência.
Foco permitido somente em ID presente numa consulta atual do próprio Sway.
Não controla o GNOME hospedeiro nem acessa Semente/ECA.
"""
import json
import os
import subprocess

OWN_APP_IDS = {"org.arandulab.DesktopSessionLab", "org.arandulab.DesktopPrototype"}


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
        identifier = current.get("id")
        if ((app_id or wm_class) and isinstance(title, str) and title
                and type(identifier) is int and identifier > 0
                and not current.get("scratchpad_state") == "fresh"):
            found.append({
                "id": identifier,
                "title": title,
                "app": str(app_id or wm_class),
            })
        for key in ("nodes", "floating_nodes"):
            for child in current.get(key) or []:
                walk(child)
    walk(node)
    return tuple(found)


def user_windows(windows):
    """Descarta a própria janela ARANDU sem inventar que há outras janelas."""
    return tuple(w for w in windows if w["app"] not in OWN_APP_IDS
                 and not w["title"].startswith("ARANDU Desktop · Laboratório"))


def _sway_socket():
    return os.environ.get("SWAYSOCK") if os.environ.get("ARANDU_SESSION_LAB") == "1" else None


def list_windows():
    """Consulta explícita; sem SWAYSOCK e flag de laboratório, não faz I/O."""
    if not _sway_socket():
        return ()
    result = subprocess.run(
        ["swaymsg", "-r", "-t", "get_tree"],
        capture_output=True, text=True, timeout=3, check=True,
    )
    return user_windows(flatten_windows(json.loads(result.stdout)))


def focus_window(identifier):
    """Solicita foco apenas se a janela ainda pertencer à sessão aninhada."""
    if not _sway_socket() or type(identifier) is not int or identifier <= 0:
        return False
    if identifier not in {w["id"] for w in list_windows()}:
        return False
    command = f"[con_id={identifier}] focus"
    result = subprocess.run(
        ["swaymsg", "-r", "-t", "command", command],
        capture_output=True, text=True, timeout=3, check=True,
    )
    answer = json.loads(result.stdout)
    return isinstance(answer, list) and bool(answer) and all(
        isinstance(part, dict) and part.get("success") is True for part in answer
    )


def hide_arandu():
    """Recolhe apenas a janela ARANDU neste Sway, sem encerrá-la.

    A regra de janela do laboratório move ARANDU para o scratchpad ao iniciar.
    Este comando move a janela de volta à área oculta depois da navegação.
    """
    if not _sway_socket():
        return False
    result = subprocess.run(
        ["swaymsg", "-r", "-t", "command",
         '[title="^ARANDU Desktop"] move scratchpad'],
        capture_output=True, text=True, timeout=3, check=True,
    )
    answer = json.loads(result.stdout)
    return isinstance(answer, list) and bool(answer) and all(
        isinstance(part, dict) and part.get("success") is True for part in answer
    )


def list_outputs():
    """Saídas ativas do Sway aninhado sob consulta, sem depender do GNOME."""
    if not _sway_socket():
        return ()
    result = subprocess.run(
        ["swaymsg", "-r", "-t", "get_outputs"],
        capture_output=True, text=True, timeout=3, check=True,
    )
    outputs = json.loads(result.stdout)
    if not isinstance(outputs, list):
        raise ValueError("Resposta de monitores inválida")
    return tuple({
        "name": item["name"],
        "focused": item.get("focused") is True,
        "width": int(item.get("rect", {}).get("width", 0)),
        "height": int(item.get("rect", {}).get("height", 0)),
    } for item in outputs if isinstance(item, dict) and item.get("active") is True
        and isinstance(item.get("name"), str) and item["name"])


def move_arandu_to_output(name):
    """Só move para uma saída enumerada pelo compositor aninhado."""
    if not _sway_socket() or not isinstance(name, str):
        return False
    valid = {item["name"] for item in list_outputs()}
    if name not in valid:
        return False
    # Evita incorporar nomes de saída em sintaxe livre; só IDs de letras/números.
    import re
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,48}", name):
        return False
    result = subprocess.run(
        ["swaymsg", "-r", "-t", "command",
         f'[title="^ARANDU Desktop"] move to output {name}'],
        capture_output=True, text=True, timeout=3, check=True,
    )
    answer = json.loads(result.stdout)
    return isinstance(answer, list) and bool(answer) and all(
        isinstance(part, dict) and part.get("success") is True for part in answer)
