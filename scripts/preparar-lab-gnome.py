#!/usr/bin/env python3
"""Stage ONLY the independent Spaces Lab in an explicitly designated test account."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import shutil

ROOT=Path(__file__).resolve().parents[1]
UUID="arandu-spaces-lab@arandulab"

def run(*args):
    return subprocess.check_output(args,cwd=ROOT,text=True,stderr=subprocess.PIPE,timeout=30).strip()

def conflicts(names):
    return any("arandu" in s.lower() or "confluencia" in s.lower() for s in names.splitlines())

def validate(commit):
    if not re.fullmatch(r"[0-9a-f]{40}",commit) or run("git","rev-parse","HEAD")!=commit:
        raise ValueError("Checkout deve corresponder ao SHA integral.")
    if run("git","status","--porcelain","--untracked-files=all"):
        raise ValueError("Árvore de trabalho não está limpa.")
    if os.geteuid()==0:
        raise ValueError("Não executar como root.")
    if os.environ.get("XDG_SESSION_TYPE")!="x11" or not re.match(r"GNOME Shell 46(?:\.|\s|$)",run("gnome-shell","--version")):
        raise ValueError("Exige sessão de teste GNOME 46/X11.")
    if conflicts(run("gnome-extensions","list")):
        raise ValueError("Extensão ARANDU/Confluência instalada nesta conta. Use outra conta de teste.")
    subprocess.run([sys.executable,"-B","scripts/auditar-snapshot.py","--ref",commit],cwd=ROOT,check=True)
    subprocess.run([sys.executable,"-B","scripts/verificar-escopo-release.py","--commit",commit],cwd=ROOT,check=True)

def stage(commit):
    validate(commit)
    parent=Path.home()/".local/share/gnome-shell/extensions"
    target=parent/UUID
    # Refuse symlinked ancestors; no writes to another installation.
    for path in (Path.home()/".local",Path.home()/".local/share",parent.parent,parent,target):
        if path.is_symlink():
            raise ValueError("Caminho simbólico recusado.")
    if target.exists():
        raise ValueError("Laboratório já existente; não sobrescrever.")
    with tempfile.TemporaryDirectory(prefix="arandu-lab-build-") as tmp:
        built=Path(tmp)/UUID
        subprocess.run([sys.executable,"-B",str(ROOT/"ARANDU-SUITE/Confluencia/spaces-lab/build.py"),str(built)],check=True)
        parent.mkdir(parents=True,exist_ok=True)
        # copytree refuses an existing destination. No automatic cleanup of user files.
        shutil.copytree(built,target,dirs_exist_ok=False)
    print("Laboratório preparado, NÃO habilitado. SHA:",commit)
    print("Saia e entre novamente somente nesta conta de teste para o GNOME reconhecer a extensão.")
    print("Habilitação explícita: gnome-extensions enable "+UUID)
    print("Recuperação: gnome-extensions disable "+UUID)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit",required=True)
    parser.add_argument("--confirm-test-account",action="store_true")
    args=parser.parse_args()
    if not args.confirm_test_account:
        parser.error("Confirme somente em conta de teste separada com --confirm-test-account.")
    try:
        stage(args.commit)
    except (OSError,ValueError,subprocess.SubprocessError) as exc:
        parser.exit(2,"Preparação recusada ou interrompida. Nenhuma habilitação automática. "+str(exc)+"\n")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
