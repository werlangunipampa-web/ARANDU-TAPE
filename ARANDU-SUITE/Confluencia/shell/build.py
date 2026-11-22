"""Monta o formato de extensão apropriado para a versão do GNOME Shell."""
from pathlib import Path
import json
import shutil
import sys
ROOT=Path(__file__).resolve().parent
MODERN="""import Clutter from 'gi://Clutter';
import GLib from 'gi://GLib';
import Gio from 'gi://Gio';
import Meta from 'gi://Meta';
import Shell from 'gi://Shell';
import St from 'gi://St';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
"""
MODERN_END="""export default class Confluencia extends Extension {
    enable() {
        this.session=new TapeSession(this.path,this.getSettings());
        try {this.session.start();} catch(e){this.session.stop();this.session=null;throw e;}
    }
    disable() {if(this.session)this.session.stop();this.session=null;}
}
"""
LEGACY="""const {Clutter,GLib,Gio,Meta,Shell,St}=imports.gi;
const Main=imports.ui.main;
const PanelMenu=imports.ui.panelMenu;
const ExtensionUtils=imports.misc.extensionUtils;
"""
LEGACY_END="""function init() {
    let session=null;
    return {
        enable() {
            session=new TapeSession(ExtensionUtils.getCurrentExtension().path,ExtensionUtils.getSettings());
            try {session.start();} catch(e){session.stop();session=null;throw e;}
        },
        disable() {if(session)session.stop();session=null;}
    };
}
"""
UUID="confluencia@arandulab"
def build(version,destination):
    modern=version>=45
    if not 40<=version<=51:raise ValueError("Integração fornecida para GNOME Shell 40 a 51.")
    assets=ROOT.parent/"app/assets"; d=Path(destination)
    (d/"schemas").mkdir(parents=True,exist_ok=True);(d/"assets").mkdir(exist_ok=True)
    info={"uuid":UUID,"name":"Arandu Tape · Confluência","description":"Semente e três rios de navegação da sessão gráfica.",
          "shell-version":list(map(str,range(45,52) if modern else range(40,45))),
          "settings-schema":"org.gnome.shell.extensions.arandu-confluencia","version":16,"version-name":"3.2.0-beta"}
    (d/"metadata.json").write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n")
    src=(ROOT/"implementation.js.in").read_text().replace("__LAYOUT__",(assets/"geometria.json").read_text().strip())
    src=src.replace("__DYNAMIC_RIVERS__",(ROOT/"rios-dinamicos.json").read_text())
    (d/"extension.js").write_text((MODERN if modern else LEGACY)+src+(MODERN_END if modern else LEGACY_END))
    shutil.copy2(ROOT/"style.css",d/"stylesheet.css")
    for schema in ROOT.glob("*.gschema.xml"):shutil.copy2(schema,d/"schemas")
    for name in ("semente","rios","memory","open","frequent"):
        shutil.copy2(assets/(name+".svg"),d/"assets")
if __name__=="__main__":build(int(sys.argv[1]),sys.argv[2])
