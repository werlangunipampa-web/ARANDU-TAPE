#!/usr/bin/env python3
"""Confluencia 2.9 update-control patch. Preview default; apply/restore explicit."""
import argparse
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
LIVE = Path.home()/".local/share/gnome-shell/extensions/confluencia@arandulab/extension.js"
BACKUPS = Path.home()/".local/share/arandu/updates/backups"
MARKER = "ARANDU_UPDATE_V03_START"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def atomic_bytes(path, data, mode):
    descriptor, name = tempfile.mkstemp(prefix=".arandu-update-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def main():
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group()
    group.add_argument("--apply", action="store_true", help="Patch active extension on disk (loads on next login)")
    group.add_argument("--restore", metavar="BACKUP", type=Path, help="Restore exact backup created by this tool")
    args = p.parse_args()
    if os.geteuid() == 0:
        p.error("do not run as root")
    if LIVE.is_symlink() or not LIVE.is_file():
        p.error("extension.js missing or symlink")
    if not shutil.which("node"):
        p.error("node required for syntax validation before any update")
    old = LIVE.read_bytes()
    if args.restore:
        backup = args.restore.resolve()
        if BACKUPS.resolve() not in backup.parents or not backup.name.startswith("confluencia-") or backup.suffix != ".js":
            p.error("backup must be a named file within ARANDU backups directory")
        if backup.is_symlink() or not backup.is_file():
            p.error("backup missing or symlink")
        restored = backup.read_bytes()
        if MARKER in restored.decode("utf-8", errors="replace"):
            p.error("backup already contains update patch")
        if digest(old) == digest(restored):
            print("Already restored")
            return
        check_js(restored)
        atomic_bytes(LIVE, restored, LIVE.stat().st_mode & 0o777)
        print(json.dumps({"restored": True, "sha256": digest(restored),
                          "restart": "log out and log back in"}, ensure_ascii=False))
        return

    if MARKER.encode() in old:
        p.error("patch already installed; refusing duplicate")
    # The generator imports a pure prepare() function. No writes to LIVE.
    sys.path.insert(0, str(HERE))
    import importlib.util
    spec = importlib.util.spec_from_file_location("confluencia_preview", HERE/"confluencia29-preview.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        modified = module.prepare(old.decode("utf-8")).encode("utf-8")
    except (ValueError, UnicodeError) as exc:
        p.error("extension layout not recognized: "+str(exc))
    check_js(modified)
    diff = list(difflib.unified_diff(old.decode("utf-8").splitlines(),
                                    modified.decode("utf-8").splitlines(),
                                    fromfile="installed",tofile="candidate",lineterm=""))
    result = {"preview": not args.apply, "baseline_sha256": digest(old),
              "candidate_sha256": digest(modified), "patch_lines": len(diff),
              "live_extension_modified": False}
    if not args.apply:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\n".join(diff[:65]))
        return
    if LIVE.read_bytes() != old:
        p.error("source changed during preparation; refusing apply")
    if not (Path.home()/".local/share/applications/arandu-update.desktop").is_file():
        p.error("ARANDU Update desktop launcher not found")
    BACKUPS.mkdir(parents=True, exist_ok=True, mode=0o700)
    if BACKUPS.is_symlink():
        p.error("backup directory cannot be symlink")
    stamp=datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup=BACKUPS/("confluencia-"+stamp+".js")
    # Fail closed if backup cannot be recorded.
    with backup.open("xb") as fh:
        fh.write(old)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(backup, 0o600)
    if backup.read_bytes() != old:
        p.error("backup failed verification")
    try:
        atomic_bytes(LIVE, modified, LIVE.stat().st_mode & 0o777)
        if LIVE.read_bytes() != modified:
            raise RuntimeError("post-write checksum mismatch")
    except Exception:
        atomic_bytes(LIVE, old, LIVE.stat().st_mode & 0o777)
        raise
    result.update({"preview":False, "live_extension_modified":True,
                   "backup":str(backup), "restart":"log out and log back in"})
    print(json.dumps(result,ensure_ascii=False,indent=2))

def check_js(data):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"extension.mjs"
        path.write_bytes(data)
        subprocess.run(["node","--check",str(path)],check=True,timeout=15,
                       stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    main()
