#!/usr/bin/env python3
"""Opy — encontro visual das janelas abertas no compositor Sway.

Metáfora de acolhimento/organização, sem representar práticas rituais.
Não salva histórico, não encerra programas e não acessa a ECA.
"""
from __future__ import annotations

import os
import sys
import subprocess

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, Gio, Gdk
except (ImportError, ValueError) as exc:
    raise SystemExit(f"Opy: GTK4 indisponível: {exc}") from exc

from session.windows import list_windows, focus_window


def available():
    return os.environ.get("ARANDU_SESSION_LAB") == "1" and bool(os.environ.get("SWAYSOCK"))


CSS = """
window.opy {background:#152820;color:#f1ecdc;}
.opy-heading {font-size:28px;font-weight:800;color:#e6ce96;}
.opy-subtitle {font-size:13px;color:#b9cfb8;}
.opy-row {padding:13px 18px;border-radius:12px;background:#233e30;
          color:#f0f3e7;border:1px solid #55785c;}
.opy-row:hover,.opy-row:focus {background:#416149;}
.opy-footer {font-size:12px;color:#afc6ae;}
"""


class Opy(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.arandulab.OpySwitcher",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = None
        self.rows = []
        self.selected = 0
        self.message = None
        self.list_box = None

    def do_activate(self):
        if not available():
            print("Opy: disponível somente na sessão Sway ARANDU.", file=sys.stderr)
            self.quit()
            return
        if self.window is None:
            self.create_window()
        self.refresh()
        self.window.present()

    def create_window(self):
        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title("Opy · Encontro das janelas")
        self.window.set_default_size(660, 460)
        self.window.add_css_class("opy")
        css = Gtk.CssProvider()
        css.load_from_data(CSS.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        layout.set_margin_top(18)
        layout.set_margin_bottom(18)
        layout.set_margin_start(20)
        layout.set_margin_end(20)
        self.window.set_child(layout)
        heading = Gtk.Label(label="OPY  ·  Encontro das Janelas", xalign=0)
        heading.add_css_class("opy-heading")
        layout.append(heading)
        intro = Gtk.Label(label="Escolha um fluxo aberto. A Semente permanece acessível por Ctrl+Alt+A.", xalign=0)
        intro.add_css_class("opy-subtitle")
        intro.set_wrap(True)
        layout.append(intro)
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        layout.append(scrolled)
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.list_box.connect("row-activated", self.on_activate_row)
        scrolled.set_child(self.list_box)
        self.message = Gtk.Label(xalign=0, wrap=True)
        self.message.add_css_class("opy-footer")
        layout.append(self.message)
        footer = Gtk.Label(label="↑ / ↓ selecionar · Enter abrir · Esc voltar · Alt+Tab reencontrar", xalign=0)
        footer.add_css_class("opy-footer")
        layout.append(footer)
        keys = Gtk.EventControllerKey.new()
        keys.connect("key-pressed", self.on_key)
        self.window.add_controller(keys)

    def refresh(self):
        self.rows = []
        while self.list_box.get_first_child():
            self.list_box.remove(self.list_box.get_first_child())
        try:
            windows = list_windows()[:30]
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            self.message.set_text("Opy não conseguiu consultar o Sway: " + str(error))
            return
        for item in windows:
            row = Gtk.ListBoxRow()
            title = item["title"].replace("\n", " ").strip()[:100]
            label = Gtk.Label(
                label=f"{item['app']}  ·  {title}",
                xalign=0, wrap=True)
            label.add_css_class("opy-row")
            row.set_child(label)
            row.set_activatable(True)
            row.set_selectable(True)
            self.list_box.append(row)
            self.rows.append(item)
        self.message.set_text(
            f"{len(self.rows)} janela(s) encontradas. Opy não fecha aplicativos."
            if self.rows else "Nenhuma janela aberta encontrada. Ctrl+Alt+A retorna à Semente.")
        if self.rows:
            self.list_box.select_row(self.list_box.get_row_at_index(0))

    def on_activate_row(self, _list_box, row):
        index = row.get_index()
        if 0 <= index < len(self.rows):
            try:
                success = focus_window(self.rows[index]["id"])
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
                self.message.set_text("Não foi possível focar: " + str(error))
                return
            if success:
                self.window.close()
            else:
                self.message.set_text("Janela mudou ou foi encerrada. Abra Opy novamente.")

    def on_key(self, _controller, keyval, _keycode, _state):
        if keyval == Gdk.KEY_Escape:
            self.window.close()
            return True
        if keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            row = self.list_box.get_selected_row()
            if row is not None:
                self.on_activate_row(self.list_box, row)
            return True
        if keyval in (Gdk.KEY_Down, Gdk.KEY_Up) and self.rows:
            row = self.list_box.get_selected_row()
            current = row.get_index() if row else 0
            direction = 1 if keyval == Gdk.KEY_Down else -1
            target = self.list_box.get_row_at_index((current + direction) % len(self.rows))
            self.list_box.select_row(target)
            return True
        return False


if __name__ == "__main__":
    raise SystemExit(Opy().run(sys.argv))
