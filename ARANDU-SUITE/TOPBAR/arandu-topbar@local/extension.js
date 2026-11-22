import St from 'gi://St';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Clutter from 'gi://Clutter';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

const COLORS = {
    terra: [22, 18, 14],
    mate: [14, 20, 15],
    cinza: [18, 18, 19],
};

const BAND_CLASSES = [
    'arandu-band-arandu',
    'arandu-band-yvy',
    'arandu-band-kaaguy',
    'arandu-band-tape',
    'arandu-band-trama',
];

const ACCENT_CLASSES = [
    'arandu-topbar--terra',
    'arandu-topbar--mate',
    'arandu-topbar--cinza',
];

const HEIGHT_CLASSES = [
    'arandu-topbar--compact',
    'arandu-topbar--medium',
    'arandu-topbar--tall',
];

export default class AranduTopbarExtension extends Extension {
    enable() {
        this._settings = this.getSettings('org.gnome.shell.extensions.arandu-topbar');
        this._oldStyle = Main.panel.get_style() ?? '';
        this._clock = Main.panel.statusArea?.dateMenu?.container ?? null;
        this._timeouts = [];

        this._button = new St.Button({
            style_class: 'panel-button arandu-portal-button',
            reactive: true,
            can_focus: true,
            track_hover: true,
            y_align: Clutter.ActorAlign.CENTER,
            accessible_name: 'Abrir menu de aplicativos ARANDU',
        });

        const box = new St.BoxLayout({
            style_class: 'arandu-portal-content',
            y_align: Clutter.ActorAlign.CENTER,
        });

        box.add_child(new St.Icon({
            gicon: Gio.icon_new_for_string(`${this.path}/assets/arandu-mark.svg`),
            icon_size: 18,
        }));

        box.add_child(new St.Label({
            text: 'ARANDU',
            style_class: 'arandu-portal-label',
        }));

        this._button.set_child(box);
        this._button.connect('clicked', () => this._launch());

        Main.panel._leftBox.insert_child_at_index(this._button, 1);
        this._riversButton = new St.Button({
            style_class: 'panel-button arandu-rivers-button',
            reactive: true,
            can_focus: true,
            track_hover: true,
            y_align: Clutter.ActorAlign.CENTER,
            accessible_name: 'Mostrar ou ocultar Rios ARANDU',
        });
        this._riversButton.set_child(new St.Label({
            text: '◈ RIOS',
            style_class: 'arandu-rivers-label',
        }));
        this._riversButton.connect('clicked', () => this._toggleRivers());
        Main.panel._leftBox.insert_child_at_index(this._riversButton, 2);

        this._settingsChangedId = this._settings.connect('changed', () => this._apply());

        this._apply();

        for (const ms of [1200, 3500, 8000]) {
            const id = GLib.timeout_add(GLib.PRIORITY_DEFAULT, ms, () => {
                if (this._settings)
                    this._apply();
                return GLib.SOURCE_REMOVE;
            });
            this._timeouts.push(id);
        }

        console.log('[ARANDU TOPBAR] v4.9.1 reboot persistence fix ativa');
    }

    // ARANDU abre a grade de aplicativos nativa do GNOME 46.
    _launch() {
        try {
            Main.overview.showApps();
        } catch (e) {
            console.error(`[ARANDU TOPBAR] erro no menu de aplicativos: ${e}`);
            Main.notify('ARANDU', 'Não foi possível abrir os aplicativos.');
        }
    }

    // RIOS expande/recolhe a Confluência instalada; não inicia outro aplicativo.
    // A chamada é assíncrona para não bloquear a interface do GNOME Shell.
    _toggleRivers() {
        try {
            Gio.DBus.session.call(
                'org.gnome.Shell',
                '/org/arandulab/Tape/Windows',
                'org.arandulab.Tape.Windows1',
                'AssistiveCommand',
                new GLib.Variant('(s)', ['seed:toggle']),
                new GLib.VariantType('(b)'),
                Gio.DBusCallFlags.NONE,
                3000,
                null,
                (connection, result) => {
                    try {
                        const [ok] = connection.call_finish(result).deep_unpack();
                        if (!ok) Main.notify('ARANDU RIOS', 'A Confluência não aceitou o comando.');
                    } catch (e) {
                        console.error(`[ARANDU TOPBAR] falha D-Bus em RIOS: ${e}`);
                        Main.notify('ARANDU RIOS', 'Ativa a extensão Confluência para navegar pelos rios.');
                    }
                }
            );
        } catch (e) {
            console.error(`[ARANDU TOPBAR] falha ao alternar RIOS: ${e}`);
            Main.notify('ARANDU RIOS', 'Confluência indisponível.');
        }
    }

    _removeClasses(actor, classes) {
        if (!actor) return;
        for (const c of classes)
            actor.remove_style_class_name(c);
    }

    _apply() {
        if (!this._settings) return;

        const variant = this._settings.get_string('variant');
        const accent = this._settings.get_string('accent');
        const height = this._settings.get_int('panel-height');
        const opacity = Math.max(0.72, Math.min(1.0, this._settings.get_double('panel-opacity')));
        const rgb = COLORS[accent] ?? COLORS.terra;

        this._removeClasses(Main.panel, BAND_CLASSES);
        this._removeClasses(Main.panel, ACCENT_CLASSES);
        this._removeClasses(Main.panel, HEIGHT_CLASSES);

        Main.panel.add_style_class_name('arandu-topbar');
        Main.panel.add_style_class_name(
            BAND_CLASSES.includes(`arandu-band-${variant}`)
                ? `arandu-band-${variant}`
                : 'arandu-band-arandu'
        );
        Main.panel.add_style_class_name(
            ACCENT_CLASSES.includes(`arandu-topbar--${accent}`)
                ? `arandu-topbar--${accent}`
                : 'arandu-topbar--terra'
        );
        Main.panel.add_style_class_name(
            height >= 54
                ? 'arandu-topbar--tall'
                : height >= 50
                    ? 'arandu-topbar--medium'
                    : 'arandu-topbar--compact'
        );

        const base = this._oldStyle?.trim() ?? '';
        const sep = base && !base.endsWith(';') ? '; ' : '';
        Main.panel.set_style(
            `${base}${sep}background-color: rgba(${rgb[0]},${rgb[1]},${rgb[2]},${opacity});`
        );

        if (this._clock) {
            this._removeClasses(this._clock, [
                'arandu-clock-capsule',
                'arandu-clock-capsule--terra',
                'arandu-clock-capsule--mate',
                'arandu-clock-capsule--cinza',
            ]);

            if (this._settings.get_boolean('clock-capsule')) {
                this._clock.add_style_class_name('arandu-clock-capsule');
                this._clock.add_style_class_name(`arandu-clock-capsule--${accent}`);
            }
        }

        if (this._button)
            this._button.visible = this._settings.get_boolean('portal-button');
    }

    disable() {
        if (this._settingsChangedId && this._settings)
            this._settings.disconnect(this._settingsChangedId);

        for (const id of this._timeouts ?? []) {
            try { GLib.source_remove(id); } catch (_) {}
        }
        this._timeouts = [];

        this._removeClasses(Main.panel, BAND_CLASSES);
        this._removeClasses(Main.panel, ACCENT_CLASSES);
        this._removeClasses(Main.panel, HEIGHT_CLASSES);
        Main.panel.remove_style_class_name('arandu-topbar');

        if (this._button)
            this._button.destroy();

        if (this._riversButton)
            this._riversButton.destroy();

        if (this._clock) {
            this._removeClasses(this._clock, [
                'arandu-clock-capsule',
                'arandu-clock-capsule--terra',
                'arandu-clock-capsule--mate',
                'arandu-clock-capsule--cinza',
            ]);
        }

        Main.panel.set_style(this._oldStyle);

        this._settings = null;
        this._button = null;
        this._clock = null;

        console.log('[ARANDU TOPBAR] v4.9.1 desativada');
    }
}
