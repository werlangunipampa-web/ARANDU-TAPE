#!/usr/bin/env python3
"""ARANDU Desktop 0.2 — laboratório GTK4 independente do GNOME Shell.

É um aplicativo de prototipação, NÃO um compositor nem sessão gráfica.
Não conecta à ECA, não coleta janelas e não modifica atalhos do sistema.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from core import Session, NAMES, RIVERS
from performance import collect
from system_status import summary, clock_text, network_status, battery_status, bluetooth_status, volume_status

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, Gio, Gdk, GLib
except (ImportError, ValueError) as error:
    print("GTK4 não disponível. Instale python3-gi e gir1.2-gtk-4.0.", file=sys.stderr)
    print(error, file=sys.stderr)
    raise SystemExit(2)

from visual import RiversCanvas
from session.windows import list_windows, focus_window, list_outputs, move_arandu_to_output, window_action, show_scratchpad

VERSION = "0.7.3"
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
        self.window.set_title("ARANDU Desktop · Laboratório 0.7.3")
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
        bar.append(add_style(Gtk.Label(label="0.7.3 · FUNDAMENTOS", xalign=0), "arandu-muted"))
        spacer = Gtk.Box(hexpand=True)
        bar.append(spacer)
        performance = Gtk.Button(label="Desempenho")
        performance.connect("clicked", lambda *_: self.show_performance())
        bar.append(performance)
        roadmap = Gtk.Button(label="Evolução")
        roadmap.connect("clicked", lambda *_: self.show_development())
        bar.append(roadmap)
        about = Gtk.Button(label="Sobre")
        about.connect("clicked", self.show_about)
        bar.append(about)
        root.append(bar)

        main = add_style(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12), "arandu-main")
        main.set_hexpand(True)
        main.set_vexpand(True)
        root.append(main)
        if os.environ.get("ARANDU_SESSION_LAB") == "1":
            quick = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            quick.append(self.quick_action("Arquivos (Nemo)", "nemo"))
            quick.append(self.quick_action("Terminal (Foot)", "foot"))
            quick.append(self.quick_action("Área de Trabalho", "desktop"))
            quick.append(self.quick_action("Navegador", "firefox"))
            quick.append(self.quick_action("Opy · Janelas", "opy"))
            main.append(quick)
        main.append(add_style(Gtk.Label(
            label="A Semente organiza o encontro entre os Rios.", xalign=0), "arandu-title"))
        main.append(add_style(Gtk.Label(
            label="Interface independente do GNOME Shell · protótipo seguro sobre Linux Mint",
            xalign=0), "arandu-muted"))

        # Reutiliza SVG e geometria reais da Confluência, sem extensão GNOME.
        self.visual = RiversCanvas(self.select, self.toggle_seed, self.select_app, self.select_window)
        main.append(self.visual)
        # Indicadores ao pé da Semente, substituindo progressivamente a barra superior.
        self.seed_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.seed_status.set_halign(Gtk.Align.CENTER)
        self.clock_button = Gtk.Button(label="--:--")
        self.clock_button.set_tooltip_text("Relógio da Semente")
        self.clock_button.connect("clicked", lambda *_: self.show_seed_status())
        self.seed_status.append(self.clock_button)
        for label, callback in (
            ("Rede", lambda: self.show_seed_status()),
            ("Bateria", lambda: self.show_seed_status()),
            ("Bluetooth", lambda: self.show_seed_status()),
            ("Som", lambda: self.show_seed_status()),
            ("Sessão", lambda: self.show_session_menu()),
        ):
            button = Gtk.Button(label=label)
            button.connect("clicked", lambda _b, cb=callback: cb())
            self.seed_status.append(button)
        main.append(self.seed_status)
        self.clock_button.set_label(clock_text())
        GLib.timeout_add_seconds(30, self.update_seed_clock)

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
            capture_button = Gtk.Button(label="Capturar → Colar")
            capture_button.connect("clicked", lambda *_: self.capture_to_clipboard())
            actions.append(capture_button)
            clipboard_button = Gtk.Button(label="Área de transferência")
            clipboard_button.connect("clicked", lambda *_: self.show_clipboard_help())
            actions.append(clipboard_button)
        if os.environ.get("ARANDU_SESSION_LAB") == "1":
            displays = Gtk.Button(label="Telas do ARANDU")
            displays.connect("clicked", lambda *_: self.show_displays())
            actions.append(displays)
            fullscreen = Gtk.Button(label="Tela cheia")
            fullscreen.connect("clicked", lambda *_: self.toggle_fullscreen())
            actions.append(fullscreen)
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

    def update_seed_clock(self):
        if self.window is None:
            return False
        self.clock_button.set_label(clock_text())
        return True

    def show_seed_status(self):
        """Consulta status somente por solicitação; não rastreia conectividade remota."""
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("SEMENTE · ESTADO DO AMBIENTE", "arandu-title"))
        for name, value in (
            ("Hora", clock_text()),
            ("Rede", network_status()),
            ("Energia", battery_status()),
            ("Bluetooth", bluetooth_status()),
            ("Áudio", volume_status()),
        ):
            self.content.append(self.text(f"{name}: {value}"))
        if os.environ.get("ARANDU_SESSION_LAB") == "1":
            for label, volume in (("Diminuir som", "-5%"), ("Aumentar som", "+5%")):
                button = Gtk.Button(label=label)
                button.connect("clicked", lambda _b, amount=volume: self.adjust_volume(amount))
                self.content.append(button)
        if os.environ.get("ARANDU_SESSION_LAB") == "1":
            for label, program in (
                ("Gerenciar redes", "nm-connection-editor"),
                ("Gerenciar Bluetooth", "blueman-manager"),
                ("Mixer de som", "pavucontrol"),
                ("Calendário", "gnome-calendar"),
            ):
                button = Gtk.Button(label=label)
                button.connect("clicked", lambda _b, app=program: self.launch_system_tool(app))
                self.content.append(button)
        refresh = Gtk.Button(label="Atualizar indicadores")
        refresh.connect("clicked", lambda *_: self.show_seed_status())
        self.content.append(refresh)

    def adjust_volume(self, amount):
        """Altera volume no máximo 5 pontos sob clique explícito."""
        if os.environ.get("ARANDU_SESSION_LAB") != "1" or amount not in ("+5%", "-5%"):
            return
        try:
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", amount],
                           check=True, timeout=3, capture_output=True)
            self.show_seed_status()
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            self.content.append(self.text("Não foi possível ajustar o áudio."))

    def capture_to_clipboard(self):
        """Captura só após clique; processo externo termina sozinho, sem histórico."""
        if os.environ.get("ARANDU_SESSION_LAB") != "1" or not os.environ.get("SWAYSOCK"):
            return
        target = Path(__file__).resolve().parent / "session" / "capture-screen.sh"
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        try:
            # Execução em subprocesso evita travar a GUI durante captura.
            subprocess.Popen(
                ["/bin/bash", str(target), "--clipboard"],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, close_fds=True, start_new_session=True,
            )
            self.content.append(self.text(
                "Captura solicitada. Use Ctrl+V no aplicativo de destino. "
                "Se não colar, verifique grim e wl-clipboard."))
        except OSError as error:
            self.content.append(self.text("Captura indisponível: " + str(error)))

    def show_clipboard_help(self):
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("SEMENTE · COPIAR E COLAR", "arandu-title"))
        for instruction in (
            "Texto: Ctrl+C para copiar, Ctrl+V para colar; Ctrl+X para recortar.",
            "Arquivos: use Nemo, com Ctrl+C/Ctrl+X/Ctrl+V entre pastas.",
            "Imagem da tela: Print copia PNG no Wayland; Ctrl+V cola no destino.",
            "Alt+Tab abre Opy para alternar entre aplicativos.",
            "Clipboard pertence à sessão: não é gravado na Memória ou ECA.",
            "Arrastar e soltar sobre o fundo ARANDU ainda não foi implementado.",
        ):
            self.content.append(self.text(instruction))

    def launch_system_tool(self, name):
        """Abre somente controles gráficos conhecidos, se instalados; sem sudo."""
        allowed = ("nm-connection-editor", "blueman-manager",
                   "pavucontrol", "gnome-calendar")
        if name not in allowed or os.environ.get("ARANDU_SESSION_LAB") != "1" or not os.environ.get("SWAYSOCK"):
            return
        binary = shutil.which(name)
        if not binary:
            self.content.append(self.text(
                name + " não está instalado. Nada foi instalado automaticamente."))
            return
        try:
            subprocess.Popen(
                [binary], stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                close_fds=True, start_new_session=True,
            )
        except OSError as error:
            self.content.append(self.text("Não foi possível abrir controle: " + str(error)))

    def show_session_menu(self):
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("SEMENTE · SESSÃO", "arandu-title"))
        if os.environ.get("ARANDU_SESSION_LAB") != "1" or not os.environ.get("SWAYSOCK"):
            self.content.append(self.text("Sair do ARANDU só está disponível na sessão própria."))
            return
        self.content.append(self.text(
            "Encerrar sessão fecha os aplicativos desta sessão. Salve documentos primeiro."))
        button = Gtk.Button(label="Solicitar saída do ARANDU")
        button.connect("clicked", lambda *_: self.confirm_logout())
        self.content.append(button)

    def confirm_logout(self):
        """Dupla ação: diálogo e confirmação para não derrubar a sessão por acidente."""
        if os.environ.get("ARANDU_SESSION_LAB") != "1" or not os.environ.get("SWAYSOCK"):
            return
        dialog = Gtk.MessageDialog(
            transient_for=self.window, modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.NONE,
            text="Encerrar a sessão ARANDU?",
        )
        dialog.set_secondary_text("Aplicativos serão fechados. Salve seu trabalho antes de continuar.")
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.add_button("Encerrar sessão", Gtk.ResponseType.ACCEPT)
        dialog.set_default_response(Gtk.ResponseType.CANCEL)
        dialog.connect("response", self.finish_logout)
        dialog.present()

    def finish_logout(self, dialog, response):
        dialog.destroy()
        if response != Gtk.ResponseType.ACCEPT:
            return
        try:
            subprocess.run(["swaymsg", "-t", "command", "exit"],
                           timeout=3, check=True, capture_output=True)
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            self.show_session_menu()
            self.content.append(self.text("Não foi possível encerrar a sessão."))

    def show_performance(self):
        """Fotografia local sob clique; nenhuma amostragem contínua."""
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("OBSERVATÓRIO · USO ATUAL", "arandu-title"))
        try:
            report = collect(limit=8)
            mem = report["memory"]
            self.content.append(self.text(
                f'RAM disponível: {mem["available_mib"]:.1f} MiB / '
                f'{mem["total_mib"]:.1f} MiB'))
            self.content.append(self.text(
                f'RAM em uso (estimada, sem cache recuperável): '
                f'{mem["used_excluding_reclaimable_mib"]:.1f} MiB'))
            self.content.append(self.text(
                f'Swap em uso: {mem["swap_used_mib"]:.1f} MiB'))
            load = report["load_average"]
            if load:
                self.content.append(self.text(
                    f'Carga CPU (1/5/15 min): {load["one_min"]:.2f} / '
                    f'{load["five_min"]:.2f} / {load["fifteen_min"]:.2f} '
                    f'(CPUs lógicas: {report["logical_cpus"] or "?"})'))
            self.content.append(self.text(
                "Carga não é % de CPU. Maiores processos por RSS:"))
            for item in report["top_processes"]:
                self.content.append(self.text(
                    f'{item["name"]} · PID {item["pid"]} · '
                    f'{item["rss_mib"]:.1f} MiB RSS'))
            self.content.append(self.text(
                "Comparação GNOME × ARANDU: usar a mesma máquina, aplicativos "
                "e condições. Esta leitura não mede o consumo isolado da interface."))
        except (OSError, KeyError, ValueError) as error:
            self.content.append(self.text("Leitura indisponível: " + str(error)))
        refresh = Gtk.Button(label="Medir novamente")
        refresh.connect("clicked", lambda *_: self.show_performance())
        self.content.append(refresh)
        if os.environ.get("ARANDU_SESSION_LAB") == "1":
            benchmark = Gtk.Button(label="Ensaio comparativo (5 medições)")
            benchmark.connect("clicked", lambda *_: self.start_benchmark())
            self.content.append(benchmark)
        self.content.append(self.text(
            "Os relatórios de outras sessões só podem ser comparados após medi-las "
            "na mesma máquina. Ensaio de CPU/RAM mede o sistema todo."))

    def start_benchmark(self):
        """Inicia uma medição finita em Foot, somente por clique, sem shell."""
        if os.environ.get("ARANDU_SESSION_LAB") != "1":
            return
        target = Path(__file__).resolve().parent / "benchmark.py"
        if not target.is_file():
            self.content.append(self.text("Módulo de benchmark indisponível."))
            return
        try:
            subprocess.Popen(
                ["foot", "-e", sys.executable, str(target), "--measure",
                 "--count", "5", "--interval", "1"],
                stdin=subprocess.DEVNULL,
                close_fds=True, start_new_session=True,
            )
            self.content.append(self.text(
                "Ensaio iniciado no Foot: cinco amostras, "
                "sem gravar automaticamente resultados."))
        except OSError as error:
            self.content.append(self.text("Não foi possível abrir o ensaio: " + str(error)))

    def show_development(self):
        """Painel local de estado; nenhuma atualização automática de código."""
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("EVOLUÇÃO DO ARANDU · " + VERSION, "arandu-title"))
        for line in (
            "Atual: iniciar com janelas visíveis; abrir Nemo e Foot por dentro do ambiente.",
            "Disponível: Rios, Semente, aplicativos instalados, ABERTOS e até 3 saídas virtuais.",
            "Em teste: foco entre janelas, saída para tela cheia, integração Nemo no Sway.",
            "Próximo: shell gráfico sobreposto e retrátil, navegação acessível e controles de sessão.",
            "Futuro: login ARANDU opcional, compositor integrado, múltiplas telas físicas.",
            "ECA e motor de aprendizagem: isolados até auditoria e autorização.",
            "O código é atualizado pelo GitHub fora desta sessão; este painel não executa git nem instala nada.",
        ):
            self.content.append(self.text(line))

    def quick_action(self, label, program):
        button = add_style(Gtk.Button(label=label), "arandu-action")
        button.connect("clicked", lambda *_: self.launch_known(program))
        return button

    def launch_known(self, program):
        """Abre aplicativos locais conhecidos no Sway, nunca comandos arbitrários."""
        if os.environ.get("ARANDU_SESSION_LAB") != "1" or not os.environ.get("SWAYSOCK"):
            return
        if program not in ("nemo", "foot", "desktop", "firefox", "opy"):
            return
        path = shutil.which("nemo" if program == "desktop" else
                            ("python3" if program == "opy" else program))
        if not path:
            self.clear_content()
            self.content.append(self.text(f"{program} não encontrado no Mint."))
            self.detail_revealer.set_reveal_child(True)
            return
        try:
            command = [path]
            if program == "opy":
                command.append(str(Path(__file__).resolve().parent / "opy.py"))
            if program == "desktop":
                desktop_dir = (GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)
                               or str(Path.home() / "Área de Trabalho"))
                if not Path(desktop_dir).is_dir():
                    desktop_dir = str(Path.home())
                command.append(desktop_dir)
            subprocess.Popen(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                start_new_session=True,
            )
            self.retract()
        except OSError as error:
            self.clear_content()
            self.content.append(self.text(f"Falha ao abrir {program}: {error}"))
            self.detail_revealer.set_reveal_child(True)

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

    def toggle_fullscreen(self):
        """Tela cheia opcional do cliente ARANDU; o Sway segue sendo o compositor."""
        if os.environ.get("ARANDU_SESSION_LAB") != "1":
            return
        if self.window.is_fullscreen():
            self.window.unfullscreen()
        else:
            self.window.fullscreen()

    def show_displays(self):
        """Permite escolher uma saída real/virtual retornada pelo Sway."""
        self.clear_content()
        self.detail_revealer.set_reveal_child(True)
        self.content.append(self.text("MONITORES DA SESSÃO SWAY", "arandu-title"))
        try:
            outputs = list_outputs()
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            self.content.append(self.text("Falha ao consultar monitores: " + str(error)))
            return
        if not outputs:
            self.content.append(self.text("Nenhuma saída Sway disponível neste modo."))
        for output in outputs:
            name = output["name"]
            dimensions = f'{output["width"]} × {output["height"]}'
            description = f'{name} · {dimensions}'
            if output["focused"]:
                description += " · ativa"
            button = Gtk.Button(label="Mover Semente para " + description)
            button.set_halign(Gtk.Align.START)
            button.connect("clicked", lambda _b, target=name: self.move_display(target))
            self.content.append(button)
        self.content.append(self.text(
            "As saídas virtuais representam janelas do Sway aninhado; "
            "não equivalem necessariamente aos monitores físicos do VAIO."))

    def move_display(self, output):
        try:
            if not move_arandu_to_output(output):
                self.content.append(self.text("Saída indisponível ou movimentação recusada."))
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            self.content.append(self.text("Falha ao mover ARANDU: " + str(error)))

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
        restore = Gtk.Button(label="Recuperar janela recolhida")
        restore.connect("clicked", lambda *_: self.restore_recollected())
        self.content.append(restore)
        if not windows:
            self.content.append(self.text(
                "Nenhuma outra janela Sway encontrada. Clique em 'Abrir Foot no Sway', "
                "volte ao ARANDU e selecione ABERTOS novamente."))
        else:
            self.content.append(self.text(
                f"{len(windows)} janela(s) disponíveis. Selecione um medalhão "
                "e confirme antes de mudar o foco. Para voltar ao ARANDU, "
                "use Ctrl+Alt+A dentro do Sway."))
            # Lista acessível acompanha os medalhões sem executar ações automaticamente.
            for item in windows[:15]:
                entry = Gtk.Button(label=f"Selecionar · {item['title']} ({item['app']})")
                entry.set_halign(Gtk.Align.START)
                entry.connect("clicked", lambda _button, selected=item: self.select_window(selected))
                self.content.append(entry)

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
        reclaim = Gtk.Button(label="Recolher à Opy")
        reclaim.connect("clicked", lambda *_: self.act_on_window(window["id"], "recolher"))
        row.append(reclaim)
        close = Gtk.Button(label="Encerrar janela")
        close.connect("clicked", lambda *_: self.confirm_close_window(window))
        row.append(close)
        cancel = Gtk.Button(label="Cancelar")
        cancel.connect("clicked", lambda *_: self.show_windows())
        row.append(cancel)
        self.content.append(row)
        self.detail_revealer.set_reveal_child(True)

    def act_on_window(self, identifier, action):
        try:
            if window_action(identifier, action):
                self.show_windows()
            else:
                self.content.append(self.text("Ação indisponível. Atualize a Opy."))
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            self.content.append(self.text("Não foi possível agir sobre a janela: " + str(error)))

    def confirm_close_window(self, window):
        dialog = Gtk.MessageDialog(
            transient_for=self.window, modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.NONE,
            text="Encerrar esta janela?",
        )
        dialog.set_secondary_text(window["title"][:150] +
                                  "\\nO aplicativo poderá pedir para salvar documentos.")
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.add_button("Encerrar janela", Gtk.ResponseType.ACCEPT)
        dialog.set_default_response(Gtk.ResponseType.CANCEL)
        dialog.connect("response", self.finish_close_window, window["id"])
        dialog.present()

    def finish_close_window(self, dialog, response, identifier):
        dialog.destroy()
        if response == Gtk.ResponseType.ACCEPT:
            self.act_on_window(identifier, "encerrar")

    def restore_recollected(self):
        try:
            if show_scratchpad():
                self.retract()
            else:
                self.content.append(self.text("Nenhuma janela recolhida para recuperar."))
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            self.content.append(self.text("Falha ao recuperar janela: " + str(error)))

    def activate_window(self, identifier):
        try:
            if not focus_window(identifier):
                self.content.append(self.text(
                    "Janela indisponível ou foco recusado pelo compositor."))
                return
            self.retract()
            # O ARANDU continua vivo em outra aba, recuperável por Ctrl+Alt+A.
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
