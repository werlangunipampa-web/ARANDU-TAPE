#!/usr/bin/env python3
"""ARANDU Desktop 0.2 — laboratório GTK4 independente do GNOME Shell.

É um aplicativo de prototipação, NÃO um compositor nem sessão gráfica.
Não conecta à ECA, não coleta janelas e não modifica atalhos do sistema.
"""
from __future__ import annotations

import json
import os
import subprocess
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
from session.windows import list_windows, focus_window

VERSION = "0.5.2"
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
.arandu-main {padding:16px;}
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
        super().__init__(application_id=(
                             "org.arandulab.DesktopSessionLab"
                             if os.environ.get("ARANDU_SESSION_LAB") == "1"
                             else "org.arandulab.DesktopPrototype"),
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.session = Session()
        self.window = None
        self.content = None
        self.detail_revealer = None
        self.selected_app = None
        self.selected_window = None

    def do_activate(self):
        if self.window:
            self.window.present()
            return
        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title("ARANDU Desktop · Laboratório 0.5.2")
        self.window.set_default_size(1120, 780)
        self.window.add_css_class("arandu")
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window.set_child(root)
        bar = add_style(Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16), "arandu-bar")
        bar.append(add_style(Gtk.Label(label="◈  ARANDU DESKTOP", xalign=0), "arandu-brand"))
        bar.append(add_style(Gtk.Label(label="0.5.2 · RIO ABERTOS FUNCIONAL", xalign=0), "arandu-muted"))
        spacer = Gtk.Box(hexpand=True)
        bar.append(spacer)
        about = Gtk.Button(label="Sobre")
        about.connect("clicked", self.show_about)
        bar.append(about)
        root.append(bar)

        main = add_style(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12), "arandu-main")
        main.set_hexpand(True)
        main.set_vexpand(True)
        root.append(main)
        main.append(add_style(Gtk.Label(
            label="A Semente organiza o encontro entre os Rios.", xalign=0), "arandu-title"))
        main.append(add_style(Gtk.Label(
            label="Interface independente do GNOME Shell · protótipo seguro sobre Linux Mint",
            xalign=0), "arandu-muted"))

        # Reutiliza SVG e geometria reais da Confluência, sem extensão GNOME.
        self.visual = RiversCanvas(self.select, self.toggle_seed, self.select_app, self.select_window)
        main.append(self.visual)

        self.detail_revealer = Gtk.Revealer()
        self.detail_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self.detail_revealer.set_reveal_child(False)
        self.content = add_style(Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8), "arandu-subpanel")
        self.content.set_vexpand(False)
        self.detail_revealer.set_child(self.content)
        main.append(self.detail_revealer)
        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        apps = add_style(Gtk.Button(label="Aplicativos instalados"), "arandu-action")
        apps.connect("clicked", lambda *_: self.show_apps())
        actions.append(apps)
        windows_btn = Gtk.Button(label="Janelas da sessão Sway")
        windows_btn.connect("clicked", lambda *_: self.show_windows())
        actions.append(windows_btn)
        if os.environ.get("ARANDU_SESSION_LAB") == "1":
            terminal_btn = Gtk.Button(label="Abrir Foot no Sway")
            terminal_btn.connect("clicked", lambda *_: self.open_test_terminal())
            actions.append(terminal_btn)
        retract = Gtk.Button(label="Recolher Rios")
        retract.connect("clicked", lambda *_: self.retract())
        actions.append(retract)
        toggle = Gtk.Button(label="Mostrar/ocultar informações")
        toggle.connect("clicked", lambda *_: self.detail_revealer.set_reveal_child(
            not self.detail_revealer.get_reveal_child()))
        actions.append(toggle)
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
        self.visual.show_rivers()
        self.content.append(self.text("Escolha um Rio ou abra a lista de aplicativos instalados."))
        self.content.append(self.text(
            "MEMÓRIA e FREQUENTES não coletam dados. Abertos consulta janelas "
            "da sessão Sway somente mediante ação explícita."))
        self.content.append(self.text(
            "ARANDU Seed / ECA: desconectado por padrão. Nenhuma identidade é migrada."))

    def select(self, river):
        if river == "open" and os.environ.get("ARANDU_SESSION_LAB") == "1":
            self.session.select(river)
            self.show_windows()
            return
        self.session.select(river)
        self.clear_content()
        self.visual.show_rivers()
        self.visual.highlight(river)
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text(NAMES[river], "arandu-title"))
        messages = {
            "memory": "Memória ainda não conectada. Procedência e consentimento serão obrigatórios.",
            "open": "Janelas reais disponíveis no laboratório Sway; GNOME hospedeiro não é consultado.",
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
        self.selected_app = None
        self.selected_window = None
        self.detail_revealer.set_reveal_child(False)
        self.show_intro()

    def show_apps(self):
        """Medalhões representam aplicativos instalados, não janelas abertas."""
        self.session.retract()
        self.selected_app = None
        self.clear_content()
        self.content.append(self.text(
            "APLICATIVOS INSTALADOS · seleção requer confirmação", "arandu-title"))
        self.content.append(self.text(
            "Escolhe um dos medalhões para examinar; nenhum aplicativo abre automaticamente."))
        apps = [a for a in Gio.AppInfo.get_all() if a.should_show() and a.get_name()]
        apps.sort(key=lambda a: a.get_name().casefold())
        finder = Gtk.SearchEntry()
        finder.set_placeholder_text("Pesquisar aplicativos nos medalhões")
        self.content.append(finder)
        finder.connect("search-changed", lambda entry: self.visual.show_apps(
            [a for a in apps if entry.get_text().casefold() in a.get_name().casefold()]))
        self.visual.show_apps(apps)
        self.detail_revealer.set_reveal_child(True)
        if not apps:
            self.content.append(self.text("Nenhum aplicativo disponível nesta sessão."))

    def open_test_terminal(self):
        """Só abre o Foot por solicitação explícita dentro da sessão experimental."""
        if os.environ.get("ARANDU_SESSION_LAB") != "1" or not os.environ.get("SWAYSOCK"):
            return
        try:
            subprocess.Popen(
                ["foot"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True,
            )
            self.clear_content()
            self.content.append(self.text(
                "Foot solicitado na sessão Sway. Volte ao ARANDU e clique "
                "em Janelas da sessão Sway para localizar a janela.",
                "arandu-note"))
            self.detail_revealer.set_reveal_child(True)
        except OSError as error:
            self.clear_content()
            self.content.append(self.text("Não foi possível abrir Foot: " + str(error)))
            self.detail_revealer.set_reveal_child(True)

    def show_windows(self):
        """Consulta janelas somente mediante pedido; não toca no GNOME hospedeiro."""
        self.session.select("open")
        self.selected_window = None
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("RIO DOS ABERTOS · JANELAS SWAY", "arandu-title"))
        if os.environ.get("ARANDU_SESSION_LAB") != "1":
            self.visual.show_rivers()
            self.content.append(self.text(
                "Disponível somente no laboratório Sway aninhado. "
                "Nenhuma janela do GNOME foi consultada."))
            return
        try:
            windows = list_windows()
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            self.visual.show_rivers()
            self.content.append(self.text("Não foi possível consultar Sway: " + str(error)))
            return
        self.visual.show_windows(windows)
        if not windows:
            self.content.append(self.text(
                "Nenhuma outra janela Sway encontrada. Clique em 'Abrir Foot no Sway', "
                "volte ao ARANDU e selecione ABERTOS novamente."))
        else:
            self.content.append(self.text(
                f"{len(windows)} janela(s) disponíveis. Selecione um medalhão "
                "e confirme antes de mudar o foco. Para voltar ao ARANDU, "
                "use Ctrl+Alt+A dentro do Sway."))
            for item in windows[:15]:
                self.content.append(self.text(
                    f"Medalhão · {item['title']} ({item['app']})"))

    def select_window(self, window):
        self.selected_window = window
        self.clear_content()
        self.content.append(self.text("Janela selecionada", "arandu-title"))
        self.content.append(self.text(window["title"] + " · " + window["app"]))
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=9)
        focus = Gtk.Button(label="Focar esta janela")
        focus.add_css_class("arandu-action")
        focus.connect("clicked", lambda *_: self.activate_window(window["id"]))
        row.append(focus)
        cancel = Gtk.Button(label="Cancelar")
        cancel.connect("clicked", lambda *_: self.show_windows())
        row.append(cancel)
        self.content.append(row)
        self.detail_revealer.set_reveal_child(True)

    def activate_window(self, identifier):
        try:
            if not focus_window(identifier):
                self.content.append(self.text(
                    "Janela indisponível ou foco recusado pelo compositor."))
                return
            self.retract()
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            self.content.append(self.text("Erro ao focar janela: " + str(error)))

    def select_app(self, application):
        self.selected_app = application
        self.clear_content()
        self.content.append(self.text("Aplicativo selecionado", "arandu-title"))
        self.content.append(self.text(application.get_name()))
        self.content.append(self.text(
            "Abrir apenas com confirmação explícita. Nenhum acesso à ECA."))
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=9)
        launch = Gtk.Button(label="Abrir aplicativo")
        launch.add_css_class("arandu-action")
        launch.connect("clicked", lambda *_: self.launch_app(application))
        row.append(launch)
        cancel = Gtk.Button(label="Cancelar")
        cancel.connect("clicked", lambda *_: self.show_apps())
        row.append(cancel)
        self.content.append(row)
        self.detail_revealer.set_reveal_child(True)

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
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("Sobre o ARANDU Desktop", "arandu-title"))
        self.content.append(self.text("Versão: " + VERSION + " (protótipo GTK4 · navegação local)"))
        self.content.append(self.text("Desenvolvimento: Rafhael Brum Werlang"))
        self.content.append(self.text("ARANDU TAPE, TOPBAR e ECA são projetos distintos."))
        self.content.append(self.text("Contrato de sessão:\n" +
                                      json.dumps(self.session.status(), ensure_ascii=False, indent=2)))
        self.content.append(self.text(
            "Licenciamento e distribuição: verificar as licenças do repositório antes de publicar pacotes."))


if __name__ == "__main__":
    raise SystemExit(Desktop().run(sys.argv))
