#!/usr/bin/env python3
"""Read-only ARANDU update check at graphical login; never installs or notifies."""
import json
import os
import pathlib
import sys
import tempfile

BASE = pathlib.Path.home() / ".local/share/arandu/updates"
sys.path.insert(0, str(BASE / "client"))
from arandu_update_check import check

def main():
    state = check()
    state["update_available"] = False
    state["notification_sent"] = False
    # A remote release is not yet a verified upgrade to the locally installed build.
    folder = pathlib.Path.home() / ".cache/arandu/updates"
    folder.mkdir(mode=0o700, parents=True, exist_ok=True)
    if folder.is_symlink():
        return 1
    fd, name = tempfile.mkstemp(prefix=".status-", suffix=".json", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        os.chmod(name, 0o600)
        os.replace(name, folder / "status.json")
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
