import Adw from 'gi://Adw';
import Gtk from 'gi://Gtk';
import Gio from 'gi://Gio';
import {ExtensionPreferences} from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';

// Preferências isoladas do GNOME Shell; não alteram as extensões históricas.
export default class AranduTopbarPreferences extends ExtensionPreferences {
    fillPreferencesWindow(window) {
        const settings=this.getSettings('org.gnome.shell.extensions.arandu-topbar');
        const page=new Adw.PreferencesPage({title:'Identidade visual',icon_name:'preferences-desktop-theme-symbolic'});
        window.add(page);
        window.set_default_size(540,620);

        const appearance=new Adw.PreferencesGroup({
            title:'Grafismos e identidade',
            description:'Escolha a composição gráfica aplicada à barra superior.'
        });
        page.add(appearance);

        const combo=(title,key,labels,values)=>{
            const model=Gtk.StringList.new(labels);
            const row=new Adw.ComboRow({title,model});
            const index=Math.max(0,values.indexOf(settings.get_string(key)));
            row.set_selected(index);
            row.connect('notify::selected',()=>{
                const selected=row.get_selected();
                if(selected<values.length)settings.set_string(key,values[selected]);
            });
            appearance.add(row);
            return row;
        };

        const variantRow=combo('Grafismo','variant',
            ['Arandu','Yvy','Kaaguy','Tape','Trama'],
            ['arandu','yvy','kaaguy','tape','trama']);
        const accentRow=combo('Paleta de cores','accent',
            ['Terra','Mate','Cinza'],
            ['terra','mate','cinza']);

        const panel=new Adw.PreferencesGroup({
            title:'Aparência da TOPBAR',
            description:'Alterações são salvas automaticamente para este usuário.'
        });
        page.add(panel);

        const height=new Adw.SpinRow({
            title:'Altura da barra (px)',
            adjustment:new Gtk.Adjustment({lower:46,upper:58,step_increment:1,page_increment:2,value:50})
        });
        panel.add(height);
        settings.bind('panel-height',height,'value',Gio.SettingsBindFlags.DEFAULT);

        const opacity=new Adw.SpinRow({
            title:'Opacidade (%)',
            adjustment:new Gtk.Adjustment({lower:72,upper:100,step_increment:1,page_increment:5,value:96}),
            digits:0
        });
        panel.add(opacity);
        // Adaptador explícito: o armazenamento usa fração entre 0,72 e 1.
        opacity.set_value(Math.round(settings.get_double('panel-opacity')*100));
        opacity.connect('notify::value',()=>settings.set_double('panel-opacity',opacity.get_value()/100));
        settings.connect('changed::panel-opacity',()=>{
            const value=Math.round(settings.get_double('panel-opacity')*100);
            if(Math.round(opacity.get_value())!==value)opacity.set_value(value);
        });

        const capsule=new Adw.SwitchRow({title:'Cápsula do relógio'});
        panel.add(capsule);
        settings.bind('clock-capsule',capsule,'active',Gio.SettingsBindFlags.DEFAULT);

        const portal=new Adw.SwitchRow({
            title:'Mostrar botão ARANDU',
            subtitle:'Abre a grade de aplicativos do GNOME'
        });
        panel.add(portal);
        settings.bind('portal-button',portal,'active',Gio.SettingsBindFlags.DEFAULT);

        const restore=new Adw.PreferencesGroup({
            title:'Recuperação',
            description:'Restaurar apenas as preferências visuais da TOPBAR.'
        });
        page.add(restore);
        const reset=new Gtk.Button({label:'Restaurar aparência padrão',halign:Gtk.Align.START,margin_top:6,margin_bottom:6});
        reset.connect('clicked',()=>{
            for(const key of ['variant','accent','panel-height','panel-opacity','clock-capsule','portal-button'])
                settings.reset(key);
            variantRow.set_selected(0);
            accentRow.set_selected(0);
        });
        restore.add(reset);

        settings.connect('changed::variant',()=>{
            const index=Math.max(0,['arandu','yvy','kaaguy','tape','trama'].indexOf(settings.get_string('variant')));
            if(variantRow.get_selected()!==index)variantRow.set_selected(index);
        });
        settings.connect('changed::accent',()=>{
            const index=Math.max(0,['terra','mate','cinza'].indexOf(settings.get_string('accent')));
            if(accentRow.get_selected()!==index)accentRow.set_selected(index);
        });
    }
}
