#!/usr/bin/env python3
"""Conservative source scope gate for the FIRST scientific release. Read-only."""
import argparse
from pathlib import PurePosixPath
import re
import subprocess

# Existing public-tree paths reserved for separation/review before the first deposit.
# This is not a classification of all possible private material.
HOLD = frozenset({
    "ARANDU-DESKTOP/docs/CONTRATO-ONTOLOGICO-TRANSVERSAL.md",
    "ARANDU-DESKTOP/docs/MATRIZ-FILOSOFIA-FUNCOES.md",
    "ARANDU-DESKTOP/ontology_contract.py",
    "ARANDU-DESKTOP/eca_experiments.py",
    "ARANDU-DESKTOP/eca_bridge.py",
    "ARANDU-DESKTOP/tests/test_ontology_contract.py",
})

def blocked_paths(paths):
    found = set()
    for path in paths:
        parts = PurePosixPath(path).parts
        if path in HOLD or any(p.lower().endswith("-private") for p in parts):
            found.add(path)
    return sorted(found)

def check(commit):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use SHA integral de commit, não branch ou HEAD.")
    resolved = subprocess.check_output(
        ["git","rev-parse","--verify",commit+"^{commit}"], stderr=subprocess.PIPE
    ).decode().strip()
    if resolved != commit:
        raise ValueError("SHA não corresponde ao commit.")
    raw = subprocess.check_output(["git","ls-tree","-r","--name-only","-z",commit])
    return blocked_paths(p.decode("utf-8","strict") for p in raw.split(b"\0") if p)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit",required=True)
    args=parser.parse_args()
    try:
        blocked=check(args.commit)
    except (ValueError,UnicodeError,subprocess.CalledProcessError,OSError):
        parser.exit(2,"Não foi possível verificar o escopo do commit.\n")
    for path in blocked:
        print(f"HOLD: {path!r}")
    if blocked:
        print("DEPÓSITO BLOQUEADO: separar ou revisar formalmente o escopo antes da release.")
        return 1
    print("Nenhum caminho da lista de retenção encontrado. Revisão humana e aprovação ainda obrigatórias.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
