#!/usr/bin/env python3
import json,pathlib,sys
root=pathlib.Path(__file__).resolve().parent
for folder,uuid in [('Confluencia',None),('TOPBAR/arandu-topbar@local','arandu-topbar@local')]:
    path=root/folder
    if uuid is None:
        assert (path/'instalador.py').is_file() and (path/'shell/build.py').is_file()
        print('Confluência: fonte presente')
    elif path.exists():
        data=json.loads((path/'metadata.json').read_text())
        assert data.get('uuid')==uuid and (path/'extension.js').is_file()
        print('TOPBAR: código presente; UUID validado')
    else: print('TOPBAR: ainda não incorporada; pacote parcial')
print('Verificação estática concluída; não substitui teste visual no GNOME.')
