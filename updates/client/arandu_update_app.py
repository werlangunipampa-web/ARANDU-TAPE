#!/usr/bin/env python3
"""ARANDU Update v0.1 — read-only GTK3 app, no installation capability."""
import json
import pathlib
import subprocess
import sys
import threading

BASE = pathlib.Path.home() / ".local/share/arandu/updates"
sys.path.insert(0, str(BASE / "client"))
try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import GLib, Gtk
except (ImportError, ValueError) as exc:
    print("ARANDU Update requer python3-gi e GTK 3: " + str(exc), file=sys.stderr)
    raise SystemExit(2)
from arandu_update_check import check

class UpdateWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ARANDU • Atualizações")
        self.set_default_size(500, 300)
        self.set_border_width(24)
        self.set_position(Gtk.WindowPosition.CENTER)
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        self.add(layout)
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>ARANDU Update</span>")
        title.set_xalign(0)
        layout.pack_start(title, False, False, 0)
        subtitle = Gtk.Label(label="Atualizações oficiais do ARANDU TAPE")
        subtitle.set_xalign(0)
        layout.pack_start(subtitle, False, False, 0)
        self.status = Gtk.Label(label="Consulta ainda não realizada")
        self.status.set_xalign(0)
        self.status.set_line_wrap(True)
        self.status.set_selectable(True)
        layout.pack_start(self.status, True, True, 0)
        self.action = Gtk.Button(label="Verificar agora")
        self.action.connect("clicked", self.refresh)
        layout.pack_start(self.action, False, False, 0)
        note = Gtk.Label(label="Prévia de leitura: não baixa, não instala e não altera o sistema.")
        note.set_xalign(0)
        note.set_line_wrap(True)
        layout.pack_start(note, False, False, 0)
        self.connect("destroy", Gtk.main_quit)

    def refresh(self, *_args):
        self.action.set_sensitive(False)
        self.status.set_text("Consultando versões finais no GitHub…")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            result = check()
        except Exception:
            result = {"status": "unavailable", "reason": "unexpected_error"}
        GLib.idle_add(self._render, result)

    def _render(self, result):
        state = result.get("status")
        if state == "stable_release_found":
            msg = ("Release estável encontrada: " + result["version"] +
                   "\nA disponibilidade de uma atualização ainda NÃO foi confirmada. " +
                   "A versão local, a assinatura e a compatibilidade precisam ser verificadas.")
        elif state == "no_stable_release":
            msg = "Nenhuma release final validável foi retornada. A versão beta não será oferecida."
        else:
            msg = "Não foi possível consultar o GitHub agora. O ARANDU continuará funcionando normalmente."
        self.status.set_text(msg)
        self.action.set_sensitive(True)
        return False

if __name__ == "__main__":
    window = UpdateWindow()
    window.show_all()
    Gtk.main()
