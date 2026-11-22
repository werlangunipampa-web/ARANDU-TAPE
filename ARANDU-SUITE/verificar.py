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
modern=root/'TOPBAR/modern'
if not (modern/'extension.js').is_file() or not (modern/'metadata.json').is_file():
    raise SystemExit('TOPBAR moderna ausente do pacote')
manifest=json.loads((modern/'metadata.json').read_text())
assert manifest.get('uuid')=='arandu-topbar@local'
assert manifest.get('settings-schema')=='org.gnome.shell.extensions.arandu-topbar'
assert '45' in manifest.get('shell-version',[]) and '51' in manifest.get('shell-version',[])
assert (root/'TOPBAR/arandu-topbar@local/metadata.json').is_file()
historical=json.loads((root/'TOPBAR/arandu-topbar@local/metadata.json').read_text())
assert historical.get('shell-version')==['46'], 'TOPBAR 46 histórica alterada'
print('TOPBAR: histórico GNOME 46 preservado; variante moderna encontrada')
print('Verificação estática concluída; não substitui teste visual no GNOME.')
