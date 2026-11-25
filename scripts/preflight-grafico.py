#!/usr/bin/env python3
"""Read-only graphical validation preflight. Does not install or enable extensions."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/"ARANDU-SUITE"/"Confluencia"/"spaces-lab"

def execute(args, *, cwd=ROOT, timeout=120):
    try:
        p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         text=True,errors="replace",timeout=timeout,check=False)
        return p.returncode,p.stdout
    except (OSError,subprocess.TimeoutExpired):
        return 125,""

def session_assessment(version, session, enabled, listing_ok):
    match=re.search(r"GNOME Shell\s+(\d+)(?:\.\d+)*",version)
    major=int(match.group(1)) if match else None
    # Other ARANDU extensions may also conflict; do not modify them.
    conflict=any("arandu" in name.lower() or "confluencia" in name.lower()
                 for name in enabled.splitlines())
    reasons=[]
    if major!=46: reasons.append("GNOME 46 não confirmado")
    if session!="x11": reasons.append("Sessão X11 não confirmada")
    if not listing_ok: reasons.append("Lista de extensões habilitadas indisponível")
    if conflict: reasons.append("Extensão ARANDU/Confluência ativa; usar sessão separada")
    return {"gnome_major":major,"session_type":session if session in ("x11","wayland") else "unknown",
            "arandu_extension_active":conflict if listing_ok else None,
            "isolated_session_candidate":not reasons,"session_warnings":reasons}

def preflight(commit):
    if not re.fullmatch(r"[0-9a-f]{40}",commit):
        raise ValueError("SHA integral obrigatório")
    code,head=execute(["git","rev-parse","HEAD"])
    clean,status=execute(["git","status","--porcelain","--untracked-files=all"])
    if code or head.strip()!=commit or clean or status.strip():
        raise ValueError("Usar clone separado, checkout do SHA informado e árvore limpa.")
    py=[sys.executable,"-B"]
    results={}
    def check(label,args):
        rc,_=execute(args)
        results[label]="pass" if rc==0 else "fail"
    check("source_screen",py+["scripts/auditar-snapshot.py","--ref",commit])
    check("research_scope",py+["scripts/verificar-escopo-release.py","--commit",commit])
    check("desktop_contracts",py+["-m","unittest","discover","-s","ARANDU-DESKTOP/tests","-q"])
    if shutil.which("node"):
        check("edge_geometry",["node",str(LAB/"test-edge-geometry.mjs")])
        check("adapter_mock",["node",str(LAB/"test-adapter.mjs")])
    else:
        results["edge_geometry"]=results["adapter_mock"]="not_available"
    with tempfile.TemporaryDirectory(prefix="arandu-preflight-") as tmp:
        out=Path(tmp)/"lab"
        check("lab_build",py+[str(LAB/"build.py"),str(out)])
        if results["lab_build"]=="pass" and shutil.which("node"):
            # JS file is in a temporary directory without package metadata.
            module=out/"extension.mjs"
            module.write_bytes((out/"extension.js").read_bytes())
            check("lab_syntax",["node","--check",str(module)])
        else:
            results["lab_syntax"]="not_available"
    for version in ("3.0","4.0"):
        code,_=execute(py+["-c",f"import gi; gi.require_version('Gtk','{version}'); from gi.repository import Gtk"])
        results["gtk_"+version]="pass" if code==0 else "not_available"
    if shutil.which("cffconvert"):
        check("citation",["cffconvert","--validate"])
    else:
        results["citation"]="not_available"
    _,gnome=execute(["gnome-shell","--version"],timeout=10)
    rc,enabled=execute(["gnome-extensions","list","--enabled"],timeout=10)
    session=session_assessment(gnome,os.environ.get("XDG_SESSION_TYPE",""),enabled,rc==0)
    return {"schema":"arandu-graphical-preflight-v1","commit":commit,
            "checks":results,"environment":session,
            "graphical_validation":"not_executed","publication_authorized":False}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit",required=True)
    args=parser.parse_args()
    try:
        result=preflight(args.commit)
    except ValueError as exc:
        parser.exit(2,f"Preflight interrompido: {exc}\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    required=("source_screen","research_scope","desktop_contracts","edge_geometry","adapter_mock","lab_build","lab_syntax")
    return 0 if all(result["checks"].get(k)=="pass" for k in required) else 1

if __name__=="__main__":
    raise SystemExit(main())
