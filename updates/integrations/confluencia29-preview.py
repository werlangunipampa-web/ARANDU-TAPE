#!/usr/bin/env python3
"""Staged, fail-closed Confluencia 2.9.0 integration. DOES NOT patch live GNOME files."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

DEFAULT = Path.home()/".local/share/gnome-shell/extensions/confluencia@arandulab/extension.js"
INSERT = """        // ARANDU_UPDATE_V03_START — explicit access in Semente controls.
        // A center launcher, NOT a verified-update notification or installer.
        this.aranduUpdateButton = new St.Button({
            label: 'Atualizações ↻',
            style_class: 'arandu-seed-control',
            can_focus: true,
            reactive: true,
            accessible_name: 'Abrir Central de Atualizações ARANDU',
        });
        this.aranduUpdateButton.connect('clicked', () => {
            try {
                const app = Gio.DesktopAppInfo.new('arandu-update.desktop');
                if (app) app.launch([], null);
                else Main.notify('ARANDU', 'Central de Atualizações ainda não instalada.');
            } catch (error) {
                logError(error, 'ARANDU Update: falha ao abrir Central');
                Main.notify('ARANDU', 'Não foi possível abrir a Central de Atualizações.');
            }
        });
        this.controlBox.add_child(this.aranduUpdateButton);
        // ARANDU_UPDATE_V03_END
"""
def prepare(source):
    # Check source identity and insertion site. Never modify it if uncertain.
    if 'ARANDU_UPDATE_V03_START' in source:
        raise ValueError('integration marker already present')
    anchors = [
        "this.root.add_child(this.controlBox);",
        "this.seed=new St.Button(",
        "this.root.add_child(this.seed);",
        "this.controlBox",
        "this.buildDesktop();",
        "import Gio from 'gi://Gio';",
    ]
    missing = [a for a in anchors if a not in source]
    if missing: raise ValueError('expected Confluencia anchors absent: '+', '.join(missing))
    anchor = "this.root.add_child(this.controlBox);"
    if source.count(anchor) != 1: raise ValueError('ambiguous control box anchor')
    if not re.search(r'class TapeSession\s*\{', source): raise ValueError('unexpected extension')
    output = source.replace(anchor, anchor+"\n"+INSERT, 1)
    # Four controls can exceed the original 140px allowance. Use the
    # natural panel height to keep it inside the visible work area.
    original = "Math.round(limit(seedY-100,4,Math.max(4,h-140)))"
    if source.count(original) != 1:
        raise ValueError('unexpected position() implementation; refusing patch')
    revised = ("Math.round(limit(seedY-100,4,"
               "Math.max(4,h-Math.ceil(this.controlBox.get_preferred_height(-1)[1])-4)))")
    return output.replace(original, revised, 1)

def main():
    parser=argparse.ArgumentParser(description='Prepare a separate integration copy; never changes active extension')
    parser.add_argument('--source',type=Path,default=DEFAULT)
    parser.add_argument('--out',type=Path,default=Path.home()/".cache/arandu/update-staging/confluencia-extension.js")
    args=parser.parse_args()
    if args.source.is_symlink() or not args.source.is_file(): parser.error('source must be a regular file, not a symlink')
    if args.source.name != 'extension.js': parser.error('source must be extension.js')
    raw=args.source.read_text(encoding='utf-8')
    try: revised=prepare(raw)
    except ValueError as error: parser.error(str(error))
    if args.out.exists() or args.out.is_symlink(): parser.error('refusing to overwrite staging output')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(revised,encoding='utf-8')
    # node --check checks parsing only; no GNOME Shell execution occurs.
    if shutil.which('node'):
        # GNOME extension uses ES module imports, so check a temporary .mjs copy.
        module_copy=args.out.with_suffix('.mjs')
        try:
            module_copy.write_text(revised,encoding='utf-8')
            subprocess.run(['node','--check',str(module_copy)],check=True,timeout=10)
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired):
            args.out.unlink(missing_ok=True)
            parser.error('JavaScript syntax check failed')
        finally:
            module_copy.unlink(missing_ok=True)
    print(json.dumps({"status":"staged_not_installed","output":str(args.out),
                      "live_extension_modified":False,"installation_enabled":False},ensure_ascii=False))
if __name__=='__main__':
    main()
