"""Mapa ARANDU GTK4: SVG originais; escala responsiva; medalhões opcionais.

Marcadores das três vias não são janelas nem memórias inventadas.
No modo Aplicativos, cada medalhão acessível representa um AppInfo real.
"""
from __future__ import annotations

from gi.repository import Gtk, GLib
from layout import ASSETS, SEED, WIDTH, HEIGHT, paths
from visual_contract import DEFAULT_SCALE, scale_for_viewport, scaled, choose_app_slots
from core import RIVERS, NAMES

LABEL_POSITIONS = {"memory": (130, 290), "open": (770, 18), "frequent": (1040, 120)}


class RiversCanvas(Gtk.ScrolledWindow):
    def __init__(self, on_river, on_seed, on_app, on_window):
        super().__init__(hexpand=True, vexpand=False)
        self.on_river, self.on_seed, self.on_app, self.on_window = on_river, on_seed, on_app, on_window
        self.scale = DEFAULT_SCALE
        self.apps = ()
        self.marker_apps = {}
        self.marker_windows = {}
        self.mode = "rivers"
        self._fit_source = 0
        self._energy_economy = False
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        self.canvas = Gtk.Overlay()
        self.canvas.set_halign(Gtk.Align.CENTER)
        self.set_child(self.canvas)
        self.background = Gtk.Picture.new_for_filename(str(ASSETS / "rios.svg"))
        self.background.set_content_fit(Gtk.ContentFit.FILL)
        self.background.set_can_shrink(True)
        self.background.set_can_target(False)
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

        # GTK4 não oferece notify::width nos widgets; consulta discreta
        # enquanto o canvas está mapeado (sem redimensionamento contínuo).
        self.connect("map", self._on_map)
        self.connect("unmap", self._on_unmap)
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

    def _on_map(self, *_args):
        if not self._fit_source:
            self._fit_width()
            self._fit_source = GLib.timeout_add(2400 if self._energy_economy else 450,
                                                  self._fit_width)

    def _on_unmap(self, *_args):
        if self._fit_source:
            GLib.Source.remove(self._fit_source)
            self._fit_source = 0

    def set_energy_mode(self, economical: bool):
        """Reduz ciclos de geometria em economia, sem alterar janelas de terceiros."""
        economical = bool(economical)
        if economical == self._energy_economy:
            return
        self._energy_economy = economical
        if self._fit_source:
            GLib.Source.remove(self._fit_source)
            self._fit_source = GLib.timeout_add(2400 if economical else 450,
                                                  self._fit_width)
        self._fit_width()

    def _fit_width(self):
        width = self.get_width()
        if width > 0:
            # Margem: o widget sempre preserva espaço antes de sua borda.
            candidate = scale_for_viewport(max(1, width - 24), 500)
            if abs(self.scale - candidate) > 0.015:
                self._layout(candidate)
        return GLib.SOURCE_CONTINUE

    def _layout(self, scale):
        self.scale = scale
        w, h = scaled(WIDTH, scale), scaled(HEIGHT, scale)
        self.canvas.set_size_request(w, h)
        self.background.set_size_request(w, h)
        self.fixed.set_size_request(w, h)
        # Nunca combine min/max content-height na troca de escala:
        # o GTK4 pode validar o limite antigo antes do novo (GTK-CRITICAL).
        # O tamanho solicitado acompanha o canvas e evita esse conflito.
        self.set_size_request(-1, h)
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
        app = self.marker_apps.get(button)
        if self.mode == "apps" and app is not None:
            self.on_app(app)  # Seleção sem iniciar processo.
        if self.mode == "windows":
            window = self.marker_windows.get(button)
            if window is not None:
                self.on_window(window)  # Confirmação antes de alterar o foco.

    def show_compact(self):
        """Em repouso, apenas o símbolo original da Semente permanece no mapa.

        Rios, títulos e medalhões surgem mediante intenção explícita.
        O tamanho da área é preservado para não causar saltos de layout.
        """
        self.mode = "compact"
        self.marker_apps.clear()
        self.marker_windows.clear()
        # Keep the main overlay child allocated; only hide its paint.
        self.background.set_opacity(0.0)
        self.seed.set_visible(True)
        self.seed.set_tooltip_text("Abrir a Confluência: Memória, Abertos e Frequentes")
        for marker, _, _, _ in self.markers:
            marker.set_visible(False)
            marker.set_sensitive(False)
        for label in self.river_buttons.values():
            label.set_visible(False)
        self._layout(self.scale)

    def show_rivers(self):
        self.background.set_opacity(1.0)
        self.mode = "rivers"
        self.seed.set_tooltip_text("Recolher a Confluência")
        self.marker_windows.clear()
        for marker, river, _, _ in self.markers:
            self.marker_apps.pop(marker, None)
            marker.set_focusable(False)
            marker.set_sensitive(False)
            marker.set_visible(True)
            marker.set_tooltip_text(NAMES[river] + " · posição visual, sem dados")
            picture = Gtk.Picture.new_for_filename(str(ASSETS / f"{river}.svg"))
            picture.set_can_shrink(True)
            picture.set_size_request(scaled(51, self.scale), scaled(51, self.scale))
            marker.set_child(picture)
        for label in self.river_buttons.values():
            label.set_visible(True)
        self._layout(self.scale)

    def show_apps(self, apps):
        """Distribui até 15 aplicativos instalados reais, sem ler janelas."""
        self.apps = choose_app_slots(apps)
        self.background.set_opacity(1.0)
        self.mode = "apps"
        self.marker_windows.clear()
        for i, (marker, river, _, _) in enumerate(self.markers):
            app = self.apps[i] if i < len(self.apps) else None
            if app:
                self.marker_apps[marker] = app
            else:
                self.marker_apps.pop(marker, None)
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

    def show_windows(self, windows):
        """Medalhões representam somente janelas Sway verificadas, sem coleta periódica."""
        self.background.set_opacity(1.0)
        self.mode = "windows"
        self.marker_apps.clear()
        self.marker_windows.clear()
        for index, (marker, river, _, _) in enumerate(self.markers):
            item = windows[index] if index < len(windows) else None
            marker.set_visible(item is not None)
            marker.set_sensitive(item is not None)
            marker.set_focusable(item is not None)
            if item is None:
                continue
            self.marker_windows[marker] = item
            marker.set_tooltip_text(
                "Selecionar janela: " + item["title"] + " · " + item["app"])
            icon = Gtk.Picture.new_for_filename(str(ASSETS / f"{river}.svg"))
            icon.set_can_shrink(True)
            marker.set_child(icon)
        for label in self.river_buttons.values():
            label.set_visible(False)
        self._layout(self.scale)
