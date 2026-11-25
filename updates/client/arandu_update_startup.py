#!/usr/bin/env python3
"""Session-start check. Never announces availability without a trusted local version."""
import json
import pathlib
import sys

BASE = pathlib.Path.home() / ".local/share/arandu/updates"
sys.path.insert(0, str(BASE / "client"))
from arandu_update_check import check

def main():
    state = check()
    # Do not notify on a remote release alone: installed version and signature
    # validation are not implemented yet. A local status may be consumed by UI.
    state["update_available"] = False
    state["notification_sent"] = False
    # No automatic writes, notifications or execution in preview mode.
    print(json.dumps(state, ensure_ascii=False, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
