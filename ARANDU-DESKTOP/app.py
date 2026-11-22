#!/usr/bin/env python3
"""ARANDU Desktop 0.1 — laboratório GTK4 independente do GNOME Shell.

É um aplicativo de prototipação, NÃO um compositor nem sessão gráfica.
Não conecta à ECA, não coleta janelas e não modifica atalhos do sistema.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from core import Session, NAMES, RIVERS

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, Gio, Gdk
except (ImportError, ValueError) as error:
    print("GTK4 não disponível. Instale python3-gi e gir1.2-gtk-4.0.", file=sys.stderr)
    print(error, file=sys.stderr)
    raise SystemExit(2)

from visual import RiversCanvas

VERSION = "0.2.0"
CSS = """
window.arandu { background:#14221d; color:#e9eee7; }
.arandu-bar {background:#1a2e26; padding:12px 18px;}
.arandu-brand {color:#c7e5cd;font-weight:800;font-size:17px;letter-spacing:2px;}
.arandu-muted {color:#adc0b3;font-size:12px;}
.arandu-title {font-size:25px;font-weight:700;color:#f2e4c6;}
.arandu-seed {
 min-width:178px;min-height:178px;border-radius:100px;
 background:#274739;color:#d9edca;border:2px solid #b9ad84;
 font-size:24px;font-weight:800;
}
.arandu-river {
 min-width:142px;min-height:48px;background:#315342;color:#eef4e9;
 border:1px solid #82a78a;border-radius:18px;font-weight:700;
}
.arandu-river:hover,.arandu-seed:hover {background:#426c56;}
.arandu-main {padding:26px;}
.arandu-subpanel {background:#1c3128;padding:18px;border-radius:16px;}
.arandu-action {background:#506d54;color:#fff;border-radius:10px;padding:10px;}
.arandu-note {color:#cfdbcf;font-size:13px;}
.arandu-seed-image {padding:0;background:transparent;border:0;box-shadow:none;}
.arandu-seed-image:hover {background:rgba(181,174,111,.10);}
.arandu-river-map {
 background:rgba(20,34,29,.94);color:#ebdfb6;
 border:1px solid #c6b27c;border-radius:11px;
 font-weight:800;font-size:12px;padding:7px 12px;
}
.arandu-river-active {background:#516f54;border-color:#eff0bd;}
entry {background:#f7f7f4;color:#14221d;}
"""

def add_style(widget, name):
    widget.add_css_class(name)
    return widget


class Desktop(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.arandulab.DesktopPrototype",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.session = Session()
        self.window = None
        self.content = None

    def do_activate(self):
        if self.window:
            self.window.present()
            return
        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title("ARANDU Desktop · Laboratório 0.2")
        self.window.set_default_size(1180, 800)
        self.window.add_css_class("arandu")
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window.set_child(root)
        bar = add_style(Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16), "arandu-bar")
        bar.append(add_style(Gtk.Label(label="◈  ARANDU DESKTOP", xalign=0), "arandu-brand"))
        bar.append(add_style(Gtk.Label(label="0.2.0 · ARQUITETURA VISUAL INDEPENDENTE", xalign=0), "arandu-muted"))
        spacer = Gtk.Box(hexpand=True)
        bar.append(spacer)
        about = Gtk.Button(label="Sobre")
        about.connect("clicked", self.show_about)
        bar.append(about)
        root.append(bar)

        main = add_style(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=19), "arandu-main")
        main.set_hexpand(True)
        main.set_vexpand(True)
        root.append(main)
        main.append(add_style(Gtk.Label(
            label="A Semente organiza o encontro entre os Rios.", xalign=0), "arandu-title"))
        main.append(add_style(Gtk.Label(
            label="Interface independente do GNOME Shell · protótipo seguro sobre Linux Mint",
            xalign=0), "arandu-muted"))

        # Reutiliza SVG e geometria reais da Confluência, sem extensão GNOME.
        self.visual = RiversCanvas(self.select, self.toggle_seed)
        main.append(self.visual)

        self.content = add_style(Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10), "arandu-subpanel")
        self.content.set_vexpand(True)
        main.append(self.content)
        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        apps = add_style(Gtk.Button(label="Aplicativos instalados"), "arandu-action")
        apps.connect("clicked", lambda *_: self.show_apps())
        actions.append(apps)
        retract = Gtk.Button(label="Recolher Rios")
        retract.connect("clicked", lambda *_: self.retract())
        actions.append(retract)
        main.append(actions)

        controller = Gtk.EventControllerKey.new()
        controller.connect("key-pressed", self.on_key)
        self.window.add_controller(controller)
        self.show_intro()
        self.window.present()

    def clear_content(self):
        while self.content.get_first_child():
            self.content.remove(self.content.get_first_child())

    def text(self, label, style="arandu-note"):
        return add_style(Gtk.Label(label=label, xalign=0, wrap=True), style)

    def show_intro(self):
        self.clear_content()
        self.content.append(self.text("Escolha um Rio ou abra a lista de aplicativos instalados."))
        self.content.append(self.text(
            "MEMÓRIA e FREQUENTES não coletam dados nesta versão. "
            "ABERTOS aguarda um adaptador de janelas independente do GNOME."))
        self.content.append(self.text(
            "ARANDU Seed / ECA: desconectado por padrão. Nenhuma identidade é migrada."))

    def select(self, river):
        self.session.select(river)
        self.clear_content()
        self.visual.highlight(river)
        self.content.append(self.text(NAMES[river], "arandu-title"))
        messages = {
            "memory": "Memória ainda não conectada. Procedência e consentimento serão obrigatórios.",
            "open": "Leitura de janelas ainda não implementada. Não confundir aplicativos instalados com janelas abertas.",
            "frequent": "Frequência de uso desativada. O protótipo não monitora os seus aplicativos.",
        }
        self.content.append(self.text(messages[river]))

    def toggle_seed(self):
        if self.session.active:
            self.retract()
        else:
            self.select("open")

    def retract(self):
        self.session.retract()
        self.visual.highlight(None)
        self.show_intro()

    def show_apps(self):
        self.session.retract()
        self.visual.highlight(None)
        self.clear_content()
        self.content.append(self.text("Aplicativos instalados · execução somente após clique",
                                      "arandu-title"))
        search = Gtk.SearchEntry()
        search.set_placeholder_text("Filtrar aplicativos por nome")
        self.content.append(search)
        scroll = Gtk.ScrolledWindow(vexpand=True)
        listing = Gtk.ListBox()
        listing.set_selection_mode(Gtk.SelectionMode.NONE)
        scroll.set_child(listing)
        self.content.append(scroll)
        apps = [a for a in Gio.AppInfo.get_all() if a.should_show() and a.get_name()]
        apps.sort(key=lambda a: a.get_name().casefold())

        def refill(query=""):
            while listing.get_first_child():
                listing.remove(listing.get_first_child())
            matches = [a for a in apps if query.casefold() in a.get_name().casefold()]
            for application in matches[:120]:
                row = Gtk.ListBoxRow()
                button = Gtk.Button(label=application.get_name(), halign=Gtk.Align.FILL)
                button.connect("clicked", lambda _b, a=application: self.launch_app(a))
                row.set_child(button)
                listing.append(row)
            if len(matches)>120:
                listing.append(self.text("Exibindo 120 resultados. Refine a pesquisa."))
        search.connect("search-changed", lambda entry: refill(entry.get_text()))
        refill()

    def launch_app(self, application):
        try:
            application.launch([], None)
            self.retract()
        except Exception as error:
            self.clear_content()
            self.content.append(self.text("Falha ao iniciar aplicativo: " + str(error)))

    def on_key(self, _controller, keyval, _keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.retract()
            return True
        # Apenas teclas na janela ARANDU; não registra atalhos globais.
        return False

    def show_about(self, *_args):
        self.clear_content()
        self.content.append(self.text("Sobre o ARANDU Desktop", "arandu-title"))
        self.content.append(self.text("Versão: " + VERSION + " (protótipo GTK4 com SVG originais)"))
        self.content.append(self.text("Desenvolvimento: Rafhael Brum Werlang"))
        self.content.append(self.text("ARANDU TAPE, TOPBAR e ECA são projetos distintos."))
        self.content.append(self.text("Contrato de sessão:\n" +
                                      json.dumps(self.session.status(), ensure_ascii=False, indent=2)))
        self.content.append(self.text(
            "Licenciamento e distribuição: verificar as licenças do repositório antes de publicar pacotes."))


if __name__ == "__main__":
    raise SystemExit(Desktop().run(sys.argv))
