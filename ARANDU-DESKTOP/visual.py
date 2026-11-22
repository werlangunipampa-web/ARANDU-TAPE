"""Tela visual GTK4 dos Rios; não carrega GNOME Shell nem consulta janelas.

Os cinco pontos de cada Rio são exclusivamente marcadores gráficos nesta versão,
não simulam aplicativos nem registros de memória.
"""
from __future__ import annotations

from gi.repository import Gtk
from layout import ASSETS, SEED, paths
from visual_contract import SCALE, scaled, compact_geometry
from core import RIVERS, NAMES


# Escala determinística: preserva cada coordenada original no mesmo sistema de referência.
# 1200x500 -> 900x375, cabendo na sessão de teste do VAIO sem cortar a Semente.
CANVAS_WIDTH, CANVAS_HEIGHT = compact_geometry()["size"]


class RiversCanvas(Gtk.ScrolledWindow):
    def __init__(self, on_river, on_seed):
        super().__init__(hexpand=True, vexpand=False)
        self.set_min_content_height(CANVAS_HEIGHT)
        self.set_max_content_height(CANVAS_HEIGHT)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.canvas = Gtk.Overlay()
        self.canvas.set_size_request(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.canvas.set_halign(Gtk.Align.CENTER)
        self.set_child(self.canvas)

        background = Gtk.Picture.new_for_filename(str(ASSETS / "rios.svg"))
        background.set_can_shrink(True)
        background.set_content_fit(Gtk.ContentFit.FILL)
        background.set_size_request(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.canvas.set_child(background)

        fixed = Gtk.Fixed()
        fixed.set_size_request(CANVAS_WIDTH, CANVAS_HEIGHT)
        fixed.set_halign(Gtk.Align.FILL)
        fixed.set_valign(Gtk.Align.FILL)
        self.canvas.add_overlay(fixed)

        seed_size = scaled(148)
        seed = self._icon_button("semente.svg", seed_size, "Semente: expandir ou recolher os rios")
        seed.connect("clicked", lambda *_: on_seed())
        fixed.put(seed, scaled(SEED[0] - 74), scaled(SEED[1] - 74))

        self.river_buttons = {}
        positions = {"memory": (130, 290), "open": (770, 18), "frequent": (1110, 120)}
        markers = paths()
        for river in RIVERS:
            # Os marcadores são decorativos, não dados reais de aplicativos.
            for index, (x, y) in enumerate(markers[river]):
                indicator = Gtk.Picture.new_for_filename(str(ASSETS / f"{river}.svg"))
                indicator.set_size_request(scaled(51), scaled(51))
                indicator.set_can_shrink(True)
                indicator.set_tooltip_text(f"{NAMES[river]} · posição visual {index+1}, sem dados associados")
                fixed.put(indicator, scaled(x - 25), scaled(y - 25))
            label = Gtk.Button(label=NAMES[river])
            label.add_css_class("arandu-river-map")
            label.set_tooltip_text(f"Abrir Rio {NAMES[river]}")
            label.connect("clicked", lambda _button, r=river: on_river(r))
            fixed.put(label, scaled(positions[river][0]), scaled(positions[river][1]))
            self.river_buttons[river] = label

    def _icon_button(self, filename, size, accessibility):
        button = Gtk.Button()
        button.set_tooltip_text(accessibility)
        button.add_css_class("arandu-seed-image")
        picture = Gtk.Picture.new_for_filename(str(ASSETS / filename))
        picture.set_size_request(size, size)
        picture.set_can_shrink(True)
        button.set_child(picture)
        return button

    def highlight(self, river):
        for name, button in self.river_buttons.items():
            if name == river:
                button.add_css_class("arandu-river-active")
            else:
                button.remove_css_class("arandu-river-active")
