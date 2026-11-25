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
for name in ("extension.js", "metadata.json", "stylesheet.css", "edge-geometry.mjs"):
    shutil.copyfile(root / name, out / name)
for name in ("window-intent-gate.mjs", "espacos-math.mjs"):
    # GJS uses ES module imports. Keep the module suffix in the package.
    shutil.copyfile(ref / name, out / name)
(out / "assets").mkdir()
for name in ("alca-viva.svg", "flecha-azul.svg", "flecha-amarela.svg"):
    shutil.copyfile(ref / name, out / "assets" / name)
# One author-designed bow and arrow, rotated toward each resizing direction.
for direction, angle in zip(("n", "ne", "e", "se", "s", "sw", "w", "nw"), range(0, 360, 45)):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<g transform="rotate({angle} 16 16)" fill="none" stroke-linecap="round" stroke-linejoin="round">
<path d="M5 16 Q16 2 27 16" stroke="#D7BB7C" stroke-width="1.8"/>
<path d="M5 16 L16 23 L27 16" stroke="#9E926D" stroke-width="0.9"/>
<path d="M16 27 V5 M12 10 L16 5 L20 10" stroke="#E6BA59" stroke-width="1.8"/>
<path d="M13 24 L16 27 L19 24" stroke="#D7BB7C" stroke-width="1.2"/>
</g></svg>"""
    (out / "assets" / f"arco-{direction}.svg").write_text(svg, encoding="utf-8")
print("Laboratório construído (não instalado):", out)
