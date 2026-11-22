"""Instalação por usuário, com troca atômica e restauração da versão anterior."""
import argparse
import contextlib
import fcntl
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import tarfile
from datetime import datetime, timezone

SOURCE=Path(__file__).resolve().parent
NAME="arandu-tape-confluencia"
APPID="org.arandulab.Tape"
UUID="confluencia@arandulab"
DATA=Path(os.environ.get("XDG_DATA_HOME") or Path.home()/".local/share").absolute()
BASE=DATA/NAME
BIN=Path(os.environ.get("XDG_BIN_HOME") or Path.home()/".local/bin").absolute()
TARGET={"programa":BASE/"programa","atalho":DATA/"applications"/(APPID+".desktop"),
        "icone":DATA/"icons/hicolor/scalable/apps"/(APPID+".svg"),
        "comando":BIN/NAME,"extensao":DATA/"gnome-shell/extensions"/UUID}
MANIFEST=BASE/"instalacao.json"
PREVIOUS=BASE/"anterior"
BACKUPS=BASE/"backups"
VERSION="2.8.2"
DEPS="""Dependências do aplicativo:
  Debian / Ubuntu:  sudo apt install python3 python3-gi python3-cairo gir1.2-gtk-3.0 librsvg2-common libwnck-3-0
  Fedora:           sudo dnf install python3 python3-gobject python3-cairo gtk3 librsvg2 libwnck3
  Arch / Manjaro:   sudo pacman -S python python-gobject python-cairo gtk3 librsvg libwnck3
  openSUSE:         sudo zypper install python3-gobject python3-cairo typelib-1_0-Gtk-3_0 gdk-pixbuf-loader-rsvg libwnck-3-0
A instalação do Arandu usa apenas a tua conta. O guia acompanha o pacote."""
def present(p):return p.exists() or p.is_symlink()
def copy(src,dst):
    if src.is_dir():shutil.copytree(src,dst,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
    else:shutil.copy2(src,dst)
def discard(p):
    if p.is_dir() and not p.is_symlink():shutil.rmtree(p)
    elif present(p):p.unlink()
def cli(command):
    try:return subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=12,check=False)
    except (OSError,subprocess.TimeoutExpired):return None

def version():
    tool=shutil.which("gnome-shell")
    r=cli([tool,"--version"]) if tool else None
    m=re.search(r"\b(\d+)(?:\.\d+)*\b",r.stdout) if r and r.returncode==0 else None
    return int(m.group(1)) if m else 0
def gtk_ready():
    try:
        import cairo,gi
        gi.require_version("Gtk","3.0")
        from gi.repository import Gtk,Gio,GdkPixbuf
        if not hasattr(Gio,"DesktopAppInfo"):return False
        GdkPixbuf.Pixbuf.new_from_file_at_scale(str(SOURCE/"app/assets/semente.svg"),22,22,True)
        return sys.version_info>=(3,8)
    except (ImportError,ValueError,RuntimeError,OSError) as exc:print(str(exc));return False
def diagnose():
    subprocess.run(["sh",str(SOURCE/"identificar-arandu.sh")],check=True)
    print("Dependências GTK 3, Cairo e leitura de SVG:", "disponíveis" if gtk_ready() else "pendentes")
def quote_exec(path):
    s=str(path).replace("%","%%")
    # Regras combinadas de strings e de argumentos da Desktop Entry Specification.
    return '"'+''.join(("\\\\"+ch if ch in ('"','`','$') else "\\\\\\\\" if ch=="\\" else ch) for ch in s)+'"'
def desktop_entry():
    cmd=quote_exec(TARGET["comando"])
    lines=["[Desktop Entry]","Type=Application","Version=1.0","Name=Arandu Tape","GenericName=Navegação por janelas e aplicativos",
           "Comment=Memória, Abertos e Frequentes se encontram na Semente","Icon="+APPID,"Exec="+cmd,"StartupWMClass="+APPID,
           "Terminal=false","Categories=Utility;Accessibility;","Keywords=Arandu;Semente;Memória;Rios;Janelas;",
           "Actions=Memory;Open;Frequent;"]
    for k,t,r in [("Memory","Abrir Memória","memory"),("Open","Ver Abertos","open"),("Frequent","Ver Frequentes","frequent")]:
        lines+=["","[Desktop Action "+k+"]","Name="+t,"Exec="+cmd+" --rio "+r]
    return "\n".join(lines)+"\n"
def make_stage(stage,v):
    programa=stage/"programa";programa.mkdir()
    for k in ("app","shell","tests","instalar.sh","instalador.py","identificar-arandu.sh","LEIA-ME.md"):copy(SOURCE/k,programa/k)
    (stage/"atalho").write_text(desktop_entry())
    copy(SOURCE/"app/assets/semente.svg",stage/"icone")
    path=shlex.quote(str(TARGET["programa"]))
    cmd=stage/"comando"
    cmd.write_text("#!/bin/sh\nexport PYTHONDONTWRITEBYTECODE=1\ncase \"${1:-}\" in\n"
                   +
                   "  --diagnostico|--autoteste|--desinstalar|--restaurar|--ativar|--preflight|--backup|--verificar-rios) exec sh "+path+"/instalar.sh \"$@\" ;;\nesac\n"+
                   "exec "+shlex.quote(sys.executable)+" "+path+"/app/main.py \"$@\"\n")
    cmd.chmod(0o755)
    keys=["programa","atalho","icone","comando"]
    if 40<=v<=51:
        from shell.build import build
        if not shutil.which("glib-compile-schemas"):
            print("Integração do Shell pendente. Instala glib-compile-schemas e repete o instalador.")
        else:
            build(v,stage/"extensao")
            subprocess.run(["glib-compile-schemas","--strict",str(stage/"extensao/schemas")],check=True)
            keys.append("extensao")
    return keys

@contextlib.contextmanager
def locked():
    BASE.mkdir(mode=0o700,parents=True,exist_ok=True)
    with (BASE/".instalar.lock").open("a+") as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        yield

def current():
    if MANIFEST.is_file():
        value=json.loads(MANIFEST.read_text())
        if value.get("id")!=UUID:raise RuntimeError("Identidade da instalação local desconhecida.")
        return value
    return {"id":UUID,"keys":[]}
def transact(stage,keys,old,new,retain):
    paths=dict(TARGET,registro=MANIFEST)
    names=list(dict.fromkeys([*keys,*old["keys"],"registro"]))
    if any(n not in paths for n in names):raise RuntimeError("Registro de instalação inválido.")
    (stage/"registro").write_text(json.dumps(new,indent=2)+"\n")
    with contextlib.ExitStack() as stack:
        staged={};moved=[];placed=[]
        for k in names:
            target=paths[k]
            if target.is_symlink() or (k!="registro" and present(target) and k not in old["keys"]):
                raise RuntimeError("Já existe outro arquivo em "+str(target)+". A instalação foi preservada.")
            target.parent.mkdir(parents=True,exist_ok=True)
            d=Path(stack.enter_context(tempfile.TemporaryDirectory(prefix=".arandu-troca-",dir=str(target.parent))))
            staged[k]=d
            if k in keys or k=="registro":copy(stage/k,d/"novo")
        # Toda a versão nova é preparada antes da primeira alteração.
        try:
            for k in names:
                target=paths[k];d=staged[k]
                if present(target):os.replace(target,d/"antigo");moved.append(k)
                if present(d/"novo"):os.replace(d/"novo",target);placed.append(k)
            if retain and old["keys"]:
                snap=stage/"copia-anterior";snap.mkdir()
                for k in moved:copy(staged[k]/"antigo",snap/k)
                prev=stage/"copia-trocada"
                if present(PREVIOUS):os.replace(PREVIOUS,prev)
                try:os.replace(snap,PREVIOUS)
                except BaseException:
                    if present(prev):os.replace(prev,PREVIOUS)
                    raise
        except BaseException:
            for k in reversed(placed):discard(paths[k])
            for k in reversed(moved):os.replace(staged[k]/"antigo",paths[k])
            raise
def activate():
    sh=shutil.which("gnome-extensions")
    if sh:
        check=cli([sh,"enable",UUID])
        if check and check.returncode==0:
            enabled=cli([sh,"list","--enabled"])
            if enabled and UUID in enabled.stdout.splitlines():
                print("O GNOME habilitou a extensão. Abre o mapa e confere o indicador GNOME conectado.");return
    print("Para integrar as janelas, encerra a sessão e entra de novo. Em Extensões, ativa “Arandu Tape · Confluência”.")
def preflight():
    """Checks without changes. An unsupported GNOME still allows standalone mode."""
    print("Arandu Tape",VERSION,"| pré-verificação (somente leitura)")
    diagnose()
    v=version()
    print("GNOME:",v if v else "ausente", "| integração de painel:", "prevista" if 40<=v<=51 else "não oferecida")
    print("Sessão:",os.environ.get("XDG_SESSION_TYPE", "não informada"))
    print("Compilador de esquemas:","disponível" if shutil.which("glib-compile-schemas") else "ausente")
    print("Manifesto próprio:","presente" if MANIFEST.is_file() else "ausente")
    print("Extensão histórica:","preservada — não é destino do instalador")
    print("Nota: a extensão GNOME só aparece após o Shell reconhecer a instalação; pode exigir sair e entrar na sessão.")
    return 0

def backup_current():
    """Archive only managed Confluência files. Never touch historical Arandu paths."""
    with locked():
        record=current()
        keys=[k for k in record["keys"] if k in TARGET]
        if len(keys)!=len(record["keys"]):raise RuntimeError("Registro local contém destinos desconhecidos.")
        BACKUPS.mkdir(mode=0o700,parents=True,exist_ok=True)
        stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        target=BACKUPS/("confluencia-"+stamp+"-"+str(os.getpid())+".tar.gz")
        with tarfile.open(target,"w:gz",format=tarfile.PAX_FORMAT) as archive:
            for k in keys:
                if present(TARGET[k]):archive.add(TARGET[k],arcname=k,recursive=True)
            if MANIFEST.is_file():archive.add(MANIFEST,arcname="instalacao.json")
        target.chmod(0o600)
    print("Backup da edição Confluência:",target)
    return target

def verify_rivers():
    """Static and automated contracts, not a promise of GNOME graphical coverage."""
    tests=subprocess.run([sys.executable,"-m","unittest","discover","-s",str(SOURCE/"tests"),"-v"],cwd=SOURCE)
    if tests.returncode:return tests.returncode
    node=shutil.which("node")
    if not node:print("Contrato JS não executado: Node.js não encontrado.");return 2
    return subprocess.run([node,str(SOURCE/"tests/shell-contract.cjs")],cwd=SOURCE).returncode

def refresh_menu():
    tool=shutil.which("update-desktop-database")
    if tool:cli([tool,str(TARGET["atalho"].parent)])
def install():
    if not gtk_ready():print(DEPS);return 1
    v=version()
    if MANIFEST.is_file():backup_current()
    with locked():
        old=current()
        with tempfile.TemporaryDirectory(prefix=".arandu-preparo-",dir=BASE) as d:
            stage=Path(d);keys=make_stage(stage,v)
            record={"id":UUID,"version":VERSION,"keys":keys,"gnome":v}
            transact(stage,keys,old,record,True)
    refresh_menu();print("Arandu Tape instalado. Abre Atividades e procura por Arandu Tape.")
    if "extensao" in keys:activate()
    elif not v:print("O aplicativo está disponível. Em X11, libwnck3 permite navegar pelas janelas.")
    else:print("Este GNOME recebe o aplicativo independente. A integração do Shell foi preparada para 40 a 51.")
    return 0
def restore():
    with locked():
        if not (PREVIOUS/"registro").is_file():print("Não há uma instalação anterior para restaurar.");return 1
        old=current();record=json.loads((PREVIOUS/"registro").read_text())
        if record.get("id")!=UUID:raise RuntimeError("Cópia anterior inválida.")
        with tempfile.TemporaryDirectory(prefix=".arandu-restauro-",dir=BASE) as d:
            stage=Path(d)
            for k in record["keys"]:
                if k not in TARGET:raise RuntimeError("Registro inválido.")
                copy(PREVIOUS/k,stage/k)
            transact(stage,record["keys"],old,record,True)
    refresh_menu();print("Versão anterior restaurada. Reabre o aplicativo ou inicia uma nova sessão.");return 0
def remove():
    if not MANIFEST.is_file():print("Arandu Tape já está removido.");return 0
    with locked():
        old=current()
        if "extensao" in old["keys"] and shutil.which("gnome-extensions"):cli(["gnome-extensions","disable",UUID])
        # Nomes e destinos são fixos. Dados e instalação legada têm outros caminhos.
        for k in old["keys"]:
            if k not in TARGET:raise RuntimeError("Registro inválido.")
        for k in old["keys"]:discard(TARGET[k])
        discard(PREVIOUS);discard(MANIFEST)
    refresh_menu();print("Aplicativo removido. O histórico e as preferências da conta foram preservados.");return 0
def main():
    p=argparse.ArgumentParser(description="Arandu Tape · Confluência 2.8.2")
    p.add_argument("--version",action="version",version="Arandu Tape 2.8.2")
    a=p.add_mutually_exclusive_group()
    for opt in ("diagnostico","autoteste","desinstalar","restaurar","ativar","preflight","backup","verificar-rios"):a.add_argument("--"+opt,action="store_true")
    opt=p.parse_args()
    if opt.diagnostico:diagnose();return 0
    if opt.preflight:return preflight()
    if opt.backup:backup_current();return 0
    if opt.verificar_rios:return verify_rivers()
    if opt.autoteste:
        result=subprocess.run([sys.executable,"-m","unittest","discover","-s",str(SOURCE/"tests"),"-v"],cwd=SOURCE)
        node=shutil.which("node")
        if result.returncode or not node:return result.returncode
        return subprocess.run([node,str(SOURCE/"tests/shell-contract.cjs")],cwd=SOURCE).returncode
    if opt.desinstalar:return remove()
    if opt.restaurar:return restore()
    if opt.ativar:
        if not (TARGET["extensao"]/"metadata.json").is_file():print("Instala o pacote em uma sessão GNOME compatível.");return 1
        activate();return 0
    return install()
if __name__=="__main__":
    try:sys.exit(main())
    except (OSError,ValueError,RuntimeError,subprocess.CalledProcessError) as e:
        print("Instalação:",e,file=sys.stderr);sys.exit(1)
