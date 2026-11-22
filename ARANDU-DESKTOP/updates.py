"""Centro de Atualizações: leitura pontual do cache local, sem instalar pacotes.

Ações potencialmente privilegiadas pertencem ao gerenciador oficial do Mint.
"""
from __future__ import annotations
import shutil
import subprocess


def _read(command: list[str], timeout: int = 8):
    if not shutil.which(command[0]):
        return None, "Ferramenta não instalada"
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None, "Consulta indisponível"
    if result.returncode != 0:
        return None, "Consulta indisponível"
    return result.stdout, None


def apt_cached_updates():
    """Cache APT somente leitura, não faz apt update nem toca na configuração."""
    raw, error = _read(["apt", "list", "--upgradable"])
    if error:
        return {"available": None, "detail": error}
    lines = [x for x in raw.splitlines() if x.strip() and
             not x.startswith("Listing...") and not x.startswith("Listando...")]
    return {"available": len(lines), "detail": "Cache APT local; pode estar desatualizado"}


def flatpak_updates():
    """Flatpak remote-ls consulta fontes remotas, portanto não é executado aqui.

    Consulta opcional de atualização fica sob gestão do atualizador oficial.
    """
    return {"available": None, "detail": (
        "Flatpak: verificar pelo Gerenciador de Atualizações. "
        "Não foram consultadas fontes remotas.")}


def snapshot_updates():
    return {"apt": apt_cached_updates(), "flatpak": flatpak_updates()}


def official_updater():
    """Escolha explícita e fixa de gerenciador gráfico instalado."""
    for executable in ("mintupdate", "gnome-software", "plasma-discover"):
        path = shutil.which(executable)
        if path:
            return path
    return None
