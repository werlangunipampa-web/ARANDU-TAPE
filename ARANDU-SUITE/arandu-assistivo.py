#!/usr/bin/env python3
"""ARANDU: ponte local e explícita para comandos assistivos (sem captura de mídia)."""
import argparse
import json
import subprocess
import sys

INTERFACE = 'org.arandulab.Tape.Windows1'
PATH = '/org/arandulab/Tape/Windows'
COMMANDS = {
    'memoria': 'river:memory', 'memória': 'river:memory',
    'abertos': 'river:open', 'frequentes': 'river:frequent',
    'próximo': 'node:next', 'proximo': 'node:next',
    'anterior': 'node:previous', 'abrir': 'node:activate',
    'ativar': 'node:activate', 'cancelar': 'node:cancel',
    'expandir': 'seed:expand', 'recolher': 'seed:collapse',
}
COMMANDS.update({v:v for v in list(COMMANDS.values())})

def normalize(text):
    """Vocabulário estrito: impede comandos não autorizados."""
    return COMMANDS.get(text.strip().lower())

def send(command, *, dry_run=False):
    if dry_run:
        print(json.dumps({'mode':'simulation','command':command},ensure_ascii=False))
        return True
    # Não usa shell=True; envia comando limitado ao DBus da própria sessão do usuário.
    try:
        r=subprocess.run(['gdbus','call','--session','--dest',
            'org.gnome.Shell','--object-path',PATH,
            '--method',INTERFACE+'.AssistiveCommand',command],
            timeout=5,capture_output=True,text=True,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        print(f'Conexão indisponível: {exc}',file=sys.stderr);return False
    if r.returncode:
        print(r.stderr.strip() or 'ARANDU não respondeu.',file=sys.stderr);return False
    if '(true,)' not in r.stdout.lower():
        print('Comando não aceito pelo ARANDU.',file=sys.stderr);return False
    return True

def main():
    p=argparse.ArgumentParser(description='Ponte assistiva local do ARANDU')
    p.add_argument('command',help='Memória, Abertos, Frequentes, próximo, anterior, abrir, cancelar, expandir, recolher')
    p.add_argument('--simular',action='store_true',help='Mostra comando sem acionar GNOME')
    args=p.parse_args()
    command=normalize(args.command)
    if not command:
        p.error('Comando desconhecido. Consulta a ajuda para comandos válidos.')
    return 0 if send(command,dry_run=args.simular) else 1
if __name__=='__main__':sys.exit(main())
