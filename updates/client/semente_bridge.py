#!/usr/bin/env python3
"""ARANDU Update -> Semente bridge. Read-only, fail-closed and no execution."""
import json
import pathlib
import re

STATUS = pathlib.Path.home() / ".cache/arandu/updates/status.json"
MAX_SIZE = 16 * 1024
TAG = re.compile(r"^v?([0-9]+)\.([0-9]+)\.([0-9]+)$")

def semver(value):
    if not isinstance(value, str):
        return None
    match = TAG.fullmatch(value)
    return tuple(int(x) for x in match.groups()) if match else None

def view(status, installed_version=None):
    """Interface contract; never offer install without verified signed metadata."""
    base = {"schema": 1, "component": "arandu-update", "indicator": "hidden",
            "message": "", "action": "open-center", "install_enabled": False,
            "release_verified": False}
    if not isinstance(status, dict):
        return base
    state = status.get("status")
    if state == "unavailable":
        return base
    if state == "no_stable_release":
        return base
    remote = semver(status.get("version"))
    local = semver(installed_version)
    # No reliable installed-version inventory, signing or compatibility yet.
    # Never label a remote release as available update.
    if state == "stable_release_found" and remote is not None:
        base["indicator"] = "informational"
        base["message"] = "Existe uma publicação estável no GitHub; compatibilidade ainda não verificada."
    return base

def read_status(path=STATUS):
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_SIZE:
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None

if __name__ == "__main__":
    print(json.dumps(view(read_status()), ensure_ascii=False, sort_keys=True))
