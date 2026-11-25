#!/usr/bin/env python3
"""Build a separate GNOME 46 lab directory. Never installs or enables it."""
from pathlib import Path
import shutil
import sys

root = Path(__file__).resolve().parent
ref = root.parent / "design-reference"
if len(sys.argv) != 2:
    raise SystemExit("Uso: python3 build.py NOVO_DIRETORIO")
out = Path(sys.argv[1]).expanduser()
if out.exists() or out.is_symlink():
    raise SystemExit("Destino deve ser novo; nenhum arquivo será substituído.")
out.mkdir(parents=True)
for name in ("extension.js", "metadata.json", "stylesheet.css"):
    shutil.copyfile(root / name, out / name)
for name in ("window-intent-gate.mjs", "espacos-math.mjs"):
    # GJS uses ES module imports. Keep the module suffix in the package.
    shutil.copyfile(ref / name, out / name)
(out / "assets").mkdir()
for name in ("alca-viva.svg", "flecha-azul.svg", "flecha-amarela.svg"):
    shutil.copyfile(ref / name, out / "assets" / name)
print("Laboratório construído (não instalado):", out)
