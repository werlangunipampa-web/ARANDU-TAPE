"""O laboratório de sessão não instala compositor nem altera GNOME."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SESSION = ROOT / "session"


class NestedSessionContract(unittest.TestCase):
    def test_files_are_present(self):
        for filename in ("start-nested.sh", "launch-arandu.sh", "sway.config.in"):
            self.assertTrue((SESSION / filename).is_file(), filename)

    def test_compositor_is_nested_x11_and_does_not_touch_login(self):
        script = (SESSION / "start-nested.sh").read_text(encoding="utf-8")
        self.assertIn("WLR_BACKENDS=x11", script)
        self.assertIn("WLR_LIBINPUT_NO_DEVICES=1", script)
        self.assertIn('sway -c "$ARANDU_SESSION_CONFIG"', script)
        # Mensagens de ajuda podem mencionar apt/sudo; comandos não podem executá-los.
        self.assertIsNone(re.search(r"(?m)^\\s*(sudo|apt|pkill|systemctl)\\b", script))
        self.assertNotIn("/usr/share/wayland-sessions", script)

    def test_emergency_exit_and_explicit_child(self):
        config = (SESSION / "sway.config.in").read_text(encoding="utf-8")
        self.assertIn("bindsym Ctrl+Alt+Shift+q exit", config)
        self.assertIn("bindsym $mod+Shift+Escape exit", config)
        self.assertEqual(config.count("__ARANDU_LAUNCHER__"), 1)
        self.assertIn("exec __ARANDU_LAUNCHER__", config)

    def test_titleless_layout_with_recovery(self):
        config = (SESSION / "sway.config.in").read_text(encoding="utf-8")
        self.assertIn("default_border none", config)
        self.assertIn("workspace_layout default", config)
        self.assertIn("bindsym $mod+t layout tabbed", config)
        self.assertIn("bindsym $mod+Tab focus next", config)
        self.assertIn("bindsym $mod+Shift+Tab focus prev", config)
        self.assertIn("bindsym $mod+q kill", config)
        self.assertIn("bindsym $mod+h move scratchpad", config)
        self.assertIn("bindsym $mod+Shift+h scratchpad show", config)

    def test_gapplication_identity_does_not_collide(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        launcher = (SESSION / "launch-arandu.sh").read_text(encoding="utf-8")
        self.assertIn("org.arandulab.DesktopSessionLab", app)
        self.assertIn("ARANDU_SESSION_LAB", launcher)
        self.assertIn("GDK_BACKEND=wayland", launcher)

    def test_foot_requires_direct_click_and_nested_session(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('terminal_btn.connect("clicked"', source)
        self.assertIn('def open_test_terminal(self):', source)
        self.assertIn('os.environ.get("SWAYSOCK")', source)
        self.assertIn('subprocess.Popen(', source)
        self.assertIn('["foot"]', source)
        self.assertNotIn('shell=True', source)

    def test_sway_can_return_to_arandu_directly(self):
        config = (SESSION / "sway.config.in").read_text(encoding="utf-8")
        self.assertIn(
            'bindsym Ctrl+Alt+a [title="^ARANDU Desktop"] focus', config
        )
        self.assertNotIn('for_window [title="^ARANDU Desktop"] floating enable', config)
        self.assertNotIn('move scratchpad, scratchpad show', config)

    def test_open_river_requests_real_windows_and_confirms_focus(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('if river == "open" and os.environ.get("ARANDU_SESSION_LAB") == "1":', app)
        self.assertIn('self.show_windows()', app)
        self.assertIn('self.session.select("open")', app)
        self.assertIn('entry.connect("clicked", lambda _button, selected=item: self.select_window(selected))', app)
        self.assertIn('focus.connect("clicked", lambda *_: self.activate_window(window["id"]))', app)
        self.assertIn('if not focus_window(identifier):', app)

    def test_focus_does_not_hide_the_app_in_scratchpad(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('self.retract()', app)
        self.assertIn('def activate_window(self, identifier):', app)
        self.assertNotIn('hide_arandu()', app)

    def test_native_launchers_are_explicit_and_allowlisted(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('quick_action("Arquivos (Nemo)", "nemo")', app)
        self.assertIn('quick_action("Terminal (Foot)", "foot")', app)
        self.assertIn('quick_action("Área de Trabalho", "desktop")', app)
        self.assertIn('quick_action("Navegador", "firefox")', app)
        self.assertIn('quick_action("Opy · Janelas", "opy")', app)
        self.assertIn('program not in ("nemo", "foot", "desktop", "firefox", "opy")', app)
        self.assertIn('path = shutil.which("nemo" if program == "desktop" else', app)
        self.assertIn('("python3" if program == "opy" else program))', app)
        self.assertIn('GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)', app)
        self.assertIn('if not Path(desktop_dir).is_dir():', app)
        self.assertIn('command.append(desktop_dir)', app)
        self.assertNotIn("shell=True", app)

    def test_virtual_outputs_one_to_three_only(self):
        script = (SESSION / "start-nested.sh").read_text(encoding="utf-8")
        self.assertIn("--outputs=1|--outputs=2|--outputs=3", script)
        self.assertIn('export WLR_X11_OUTPUTS="$OUTPUTS"', script)
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("def show_displays(self):", app)
        self.assertIn("def toggle_fullscreen(self):", app)
        self.assertIn("move_arandu_to_output(output)", app)

    def test_evolution_panel_does_not_run_updates_or_migrations(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('roadmap = Gtk.Button(label="Evolução")', app)
        self.assertIn('def show_development(self):', app)
        development = app.split('    def show_development(self):', 1)[1].split(
            '    def quick_action(', 1)[0]
        self.assertNotIn('subprocess.', development)
        self.assertNotIn('os.system(', development)
        self.assertNotIn('git pull', development)

    def test_nested_print_bindings_are_rendered(self):
        config = (SESSION / "sway.config.in").read_text()
        script = (SESSION / "start-nested.sh").read_text()
        self.assertIn('bindsym Print exec __ARANDU_CAPTURE__', config)
        self.assertIn('bindsym Shift+Print exec __ARANDU_CAPTURE_SAVE__', config)
        self.assertIn("template.replace('__ARANDU_CAPTURE__'", script)
        self.assertIn("template.replace('__ARANDU_CAPTURE_SAVE__'", script)

    def test_no_automatic_eca_connection(self):
        for name in ("start-nested.sh", "launch-arandu.sh", "sway.config.in"):
            source = (SESSION / name).read_text(encoding="utf-8")
            for sensitive in ("ARANDU-ECA-PRIVATE", "ARANDU-G4-PRIVATE", "migrate-seed"):
                self.assertNotIn(sensitive, source)


if __name__ == "__main__":
    unittest.main()
