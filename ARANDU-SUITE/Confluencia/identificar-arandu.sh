#!/bin/sh
# Leitura local, sem privilégios administrativos. Pode ser usado antes de instalar o aplicativo.
set -eu
py=/usr/bin/python3
if [ ! -x "$py" ]; then py=python3; fi
"$py" - <<'PY'
import json, os, platform, shutil, subprocess
from pathlib import Path

def run(args):
    if not shutil.which(args[0]): return None
    try:
        result=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                              universal_newlines=True,timeout=6)
        return result.stdout.strip() if result.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):return None
def clean(value):
    return str(value).replace("\n"," ").replace("\r"," ")[:160]

osname="Linux"
try:
    for line in Path("/etc/os-release").read_text().splitlines():
        if line.startswith("PRETTY_NAME="):osname=line.split("=",1)[1].strip('"')
except OSError:pass
print("Arandu Tape | Inventário local")
print("Sistema:",clean(osname),"·",platform.machine())
print("Desktop:",clean(os.getenv("XDG_CURRENT_DESKTOP") or "não informado"))
print("Sessão:",clean(os.getenv("XDG_SESSION_TYPE") or ("wayland" if os.getenv("WAYLAND_DISPLAY") else "x11" if os.getenv("DISPLAY") else "não informada")))
print("Shell:",run(["gnome-shell","--version"]) or "GNOME Shell não encontrado")
active=run(["gnome-extensions","list","--enabled"])
enabled=set(active.splitlines()) if active is not None else None
user=Path(os.getenv("XDG_DATA_HOME") or Path.home()/".local/share")
roots=[(user,"usuário")]+[(Path(d),"sistema") for d in (os.getenv("XDG_DATA_DIRS") or "/usr/local/share:/usr/share").split(":") if d]
seen=set()
for base,scope in roots:
    folder=base/"gnome-shell/extensions"
    for entry in sorted(folder.glob("*/metadata.json")):
        try: data=json.loads(entry.read_text())
        except (ValueError,OSError):continue
        uid=str(data.get("uuid",entry.parent.name))
        name=str(data.get("name",""))
        if "arandu" not in (uid+" "+name).casefold():continue
        shadowed=uid in seen
        state="cópia secundária" if shadowed else ("ativada" if uid in enabled else "desativada") if enabled is not None else "ativação não consultável"
        seen.add(uid)
        ver=data.get("version-name") or data.get("version","não informada")
        versions=data.get("shell-version",[])
        print(f"Extensão ({scope}): {clean(name)} | {clean(uid)} | versão {clean(ver)} | {state} | GNOME {clean(', '.join(map(str,versions)))}")
if not seen:print("Extensões Arandu: nenhuma encontrada nos diretórios padrão.")
for name in ("arandu-riversctl","arandu-center","arandu-hub","arandu-tape","arandu-tape-confluencia"):
    if shutil.which(name) or (Path.home()/".local/bin"/name).is_file():print("Comando presente:",name)
print("Edição Confluência:", "instalada" if (user/"arandu-tape-confluencia/instalacao.json").is_file() else "ainda não instalada")
PY
