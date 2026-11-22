"""Mapa ARANDU GTK4: SVG originais; escala responsiva; medalhões opcionais.

Marcadores das três vias não são janelas nem memórias inventadas.
No modo Aplicativos, cada medalhão acessível representa um AppInfo real.
"""
from __future__ import annotations

from gi.repository import Gtk, GLib
from layout import ASSETS, SEED, WIDTH, HEIGHT, paths
from visual_contract import DEFAULT_SCALE, scale_for_viewport, scaled, choose_app_slots
from core import RIVERS, NAMES

LABEL_POSITIONS = {"memory": (130, 290), "open": (770, 18), "frequent": (1110, 120)}


class RiversCanvas(Gtk.ScrolledWindow):
    def __init__(self, on_river, on_seed, on_app):
        super().__init__(hexpand=True, vexpand=False)
        self.on_river, self.on_seed, self.on_app = on_river, on_seed, on_app
        self.scale = DEFAULT_SCALE
        self.apps = ()
        self.mode = "rivers"
        self._refresh_scheduled = False
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        self.canvas = Gtk.Overlay()
        self.canvas.set_halign(Gtk.Align.CENTER)
        self.set_child(self.canvas)
        self.background = Gtk.Picture.new_for_filename(str(ASSETS / "rios.svg"))
        self.background.set_content_fit(Gtk.ContentFit.FILL)
        self.background.set_can_shrink(True)
        self.canvas.set_child(self.background)
        self.fixed = Gtk.Fixed()
        self.fixed.set_halign(Gtk.Align.FILL)
        self.fixed.set_valign(Gtk.Align.FILL)
        self.canvas.add_overlay(self.fixed)
        self.seed = self._icon_button("semente.svg", "Semente: abrir ou recolher rios")
        self.seed.connect("clicked", lambda *_: self.on_seed())
        self.fixed.put(self.seed, 0, 0)
        self.river_buttons = {}
        self.markers = []
        points = paths()
        for river in RIVERS:
            for x, y in points[river]:
                marker = Gtk.Button()
                marker.add_css_class("arandu-seed-image")
                marker.set_focusable(False)
                marker.connect("clicked", self._click_marker)
                self.fixed.put(marker, 0, 0)
                self.markers.append((marker, river, x, y))
            label = Gtk.Button(label=NAMES[river])
            label.add_css_class("arandu-river-map")
            label.connect("clicked", lambda _b, name=river: self.on_river(name))
            self.fixed.put(label, 0, 0)
            self.river_buttons[river] = label

        self.connect("notify::width", self._on_width)
        self._layout(self.scale)
        self.show_rivers()

    def _icon_button(self, filename, hint):
        button = Gtk.Button()
        button.set_tooltip_text(hint)
        button.add_css_class("arandu-seed-image")
        picture = Gtk.Picture.new_for_filename(str(ASSETS / filename))
        picture.set_can_shrink(True)
        button.set_child(picture)
        return button

    def _on_width(self, *_args):
        if self._refresh_scheduled:
            return
        self._refresh_scheduled = True
        GLib.idle_add(self._fit_width)

    def _fit_width(self):
        self._refresh_scheduled = False
        width = self.get_width()
        if width > 0:
            # Margem: o widget sempre preserva espaço antes de sua borda.
            candidate = scale_for_viewport(max(1, width - 24), 500)
            if abs(self.scale - candidate) > 0.015:
                self._layout(candidate)
        return GLib.SOURCE_REMOVE

    def _layout(self, scale):
        self.scale = scale
        w, h = scaled(WIDTH, scale), scaled(HEIGHT, scale)
        self.canvas.set_size_request(w, h)
        self.background.set_size_request(w, h)
        self.fixed.set_size_request(w, h)
        self.set_min_content_height(h)
        self.set_max_content_height(h)
        size = scaled(148, scale)
        self.seed.set_size_request(size, size)
        self.seed.get_child().set_size_request(size, size)
        self.fixed.move(self.seed, scaled(SEED[0]-74,scale), scaled(SEED[1]-74,scale))
        for marker, river, x, y in self.markers:
            edge = scaled(51,scale)
            marker.set_size_request(edge,edge)
            self.fixed.move(marker, scaled(x-25,scale), scaled(y-25,scale))
            if marker.get_child():
                marker.get_child().set_size_request(edge,edge)
        for river, label in self.river_buttons.items():
            x, y = LABEL_POSITIONS[river]
            self.fixed.move(label,scaled(x,scale),scaled(y,scale))

    def _click_marker(self, button):
        app = getattr(button, "_arandu_app", None)
        if self.mode == "apps" and app is not None:
            self.on_app(app)  # Apenas seleciona; não inicia processo.

    def show_rivers(self):
        self.mode = "rivers"
        for marker, river, _, _ in self.markers:
            marker._arandu_app = None
            marker.set_focusable(False)
            marker.set_sensitive(False)
            marker.set_visible(True)
            marker.set_tooltip_text(NAMES[river] + " · posição visual, sem dados")
            marker.set_child(Gtk.Picture.new_for_filename(str(ASSETS / f"{river}.svg")))
        for label in self.river_buttons.values():
            label.set_visible(True)

    def show_apps(self, apps):
        """Distribui até 15 aplicativos instalados reais, sem ler janelas."""
        self.apps = choose_app_slots(apps)
        self.mode = "apps"
        for i, (marker, river, _, _) in enumerate(self.markers):
            app = self.apps[i] if i < len(self.apps) else None
            marker._arandu_app = app
            marker.set_sensitive(app is not None)
            marker.set_focusable(app is not None)
            marker.set_visible(app is not None)
            if app:
                name = app.get_name()
                marker.set_tooltip_text("Selecionar aplicativo: " + name)
                icon = app.get_icon()
                if icon:
                    marker.set_child(Gtk.Image.new_from_gicon(icon))
                else:
                    marker.set_child(Gtk.Picture.new_for_filename(str(ASSETS / f"{river}.svg")))
        for label in self.river_buttons.values():
            label.set_visible(False)
        self._layout(self.scale)

    def highlight(self, river):
        if self.mode != "rivers":
            return
        for name, button in self.river_buttons.items():
            if name == river:
                button.add_css_class("arandu-river-active")
            else:
                button.remove_css_class("arandu-river-active")
