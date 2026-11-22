"""Tela visual GTK4 dos Rios; não carrega GNOME Shell nem consulta janelas.

Os cinco pontos de cada Rio são exclusivamente marcadores gráficos nesta versão,
não simulam aplicativos nem registros de memória.
"""
from __future__ import annotations

from gi.repository import Gtk, Gdk
from layout import ASSETS, WIDTH, HEIGHT, SEED, paths
from core import RIVERS, NAMES


class RiversCanvas(Gtk.ScrolledWindow):
    def __init__(self, on_river, on_seed):
        super().__init__(hexpand=True, vexpand=False)
        self.set_min_content_height(330)
        self.set_max_content_height(510)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.canvas = Gtk.Overlay()
        self.canvas.set_size_request(WIDTH, HEIGHT)
        self.set_child(self.canvas)

        background = Gtk.Picture.new_for_filename(str(ASSETS / "rios.svg"))
        background.set_can_shrink(False)
        background.set_content_fit(Gtk.ContentFit.FILL)
        background.set_size_request(WIDTH, HEIGHT)
        self.canvas.set_child(background)

        fixed = Gtk.Fixed()
        fixed.set_size_request(WIDTH, HEIGHT)
        fixed.set_halign(Gtk.Align.FILL)
        fixed.set_valign(Gtk.Align.FILL)
        self.canvas.add_overlay(fixed)

        seed = self._icon_button("semente.svg", 148, "Semente: expandir ou recolher os rios")
        seed.connect("clicked", lambda *_: on_seed())
        fixed.put(seed, SEED[0] - 74, SEED[1] - 74)

        self.river_buttons = {}
        positions = {"memory": (130, 290), "open": (770, 18), "frequent": (1110, 120)}
        markers = paths()
        for river in RIVERS:
            # Os marcadores são decorativos, não dados reais de aplicativos.
            for index, (x, y) in enumerate(markers[river]):
                indicator = Gtk.Picture.new_for_filename(str(ASSETS / f"{river}.svg"))
                indicator.set_size_request(51, 51)
                indicator.set_can_shrink(True)
                indicator.set_tooltip_text(f"{NAMES[river]} · posição visual {index+1}, sem dados associados")
                fixed.put(indicator, x - 25, y - 25)
            label = Gtk.Button(label=NAMES[river])
            label.add_css_class("arandu-river-map")
            label.set_accessible_name(f"Abrir Rio {NAMES[river]}")
            label.connect("clicked", lambda _button, r=river: on_river(r))
            fixed.put(label, *positions[river])
            self.river_buttons[river] = label

    def _icon_button(self, filename, size, accessibility):
        button = Gtk.Button()
        button.set_accessible_name(accessibility)
        button.add_css_class("arandu-seed-image")
        picture = Gtk.Picture.new_for_filename(str(ASSETS / filename))
        picture.set_size_request(size, size)
        picture.set_can_shrink(False)
        button.set_child(picture)
        return button

    def highlight(self, river):
        for name, button in self.river_buttons.items():
            if name == river:
                button.add_css_class("arandu-river-active")
            else:
                button.remove_css_class("arandu-river-active")
