import Adw from 'gi://Adw';
import Gtk from 'gi://Gtk';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
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

        // Página Sobre: versões de fato instaladas, nunca uma versão presumida.
        const aboutPage=new Adw.PreferencesPage({
            title:'Sobre o ARANDU',icon_name:'help-about-symbolic'
        });
        window.add(aboutPage);
        const credits=new Adw.PreferencesGroup({
            title:'ARANDU · Identidade e desenvolvimento',
            description:'Informações e acompanhamento da instalação atual.'
        });
        aboutPage.add(credits);
        const author=new Adw.ActionRow({
            title:'Desenvolvimento',
            subtitle:'Rafhael Brum Werlang'
        });
        credits.add(author);
        const versionOf=(uuid,fallback)=>{
            try {
                const file=Gio.File.new_for_path(GLib.build_filenamev([
                    GLib.get_user_data_dir(),'gnome-shell','extensions',uuid,'metadata.json'
                ]));
                const [ok,bytes]=file.load_contents(null);
                if(!ok)return fallback;
                const meta=JSON.parse(new TextDecoder().decode(bytes));
                const version=meta['version-name']||String(meta.version||fallback);
                const number=meta.version?' ('+meta.version+')':'';
                return version+number;
            } catch(e){return fallback;}
        };
        credits.add(new Adw.ActionRow({
            title:'ARANDU TOPBAR',
            subtitle:versionOf('arandu-topbar@local','Versão não identificada')
        }));
        credits.add(new Adw.ActionRow({
            title:'ARANDU TAPE · Confluência',
            subtitle:versionOf('confluencia@arandulab','Não instalada')
        }));
        const release=new Adw.PreferencesGroup({
            title:'Histórico e evolução',
            description:'Versões e plano diretor publicados no repositório oficial. O número mostrado indica os arquivos instalados; a versão ativa deve ser confirmada no GNOME Shell.'
        });
        aboutPage.add(release);
        const repoLink=new Gtk.LinkButton({
            label:'Abrir projeto ARANDU no GitHub',
            uri:'https://github.com/werlangunipampa-web/ARANDU-TAPE',
            halign:Gtk.Align.START,margin_top:6,margin_bottom:6
        });
        release.add(repoLink);

        // Os controles dos medalhões pertencem à Confluência, não à TOPBAR.
        // Abrimos o schema instalado da Confluência sem duplicar preferências.
        const riverPage=new Adw.PreferencesPage({
            title:'Semente e Rios',
            icon_name:'preferences-other-symbolic'
        });
        window.add(riverPage);
        const location=GLib.build_filenamev([
            GLib.get_user_data_dir(),'gnome-shell','extensions',
            'confluencia@arandulab','schemas'
        ]);
        let rivers=null;
        try {
            const source=Gio.SettingsSchemaSource.new_from_directory(
                location,Gio.SettingsSchemaSource.get_default(),false);
            const schema=source.lookup('org.gnome.shell.extensions.arandu-confluencia',true);
            if(schema)rivers=Gio.Settings.new_full(schema,null,null);
        } catch(e) {
            console.warn('[ARANDU] Confluência indisponível para preferências:',e);
        }
        if(!rivers) {
            const unavailable=new Adw.PreferencesGroup({
                title:'Confluência não encontrada',
                description:'Instala ou atualiza a extensão Confluência e reinicia a sessão para configurar os medalhões.'
            });
            riverPage.add(unavailable);
            return;
        }
        const visual=new Adw.PreferencesGroup({
            title:'Medalhões',
            description:'Preferências compartilhadas com os rios da Confluência. As mudanças são salvas automaticamente.'
        });
        riverPage.add(visual);

        // Um único modelo de configuração, sem copiar valores entre extensões.
        const selection=(group,title,key,labels,values)=>{
            const row=new Adw.ComboRow({title,model:Gtk.StringList.new(labels)});
            const current=()=>Math.max(0,values.indexOf(rivers.get_string(key)));
            row.set_selected(current());
            row.connect('notify::selected',()=>{
                const selected=row.get_selected();
                if(selected<values.length && rivers.get_string(key)!==values[selected])
                    rivers.set_string(key,values[selected]);
            });
            rivers.connect('changed::'+key,()=>{
                const index=current();
                if(row.get_selected()!==index)row.set_selected(index);
            });
            group.add(row);
            return row;
        };
        const sizeOptions=[0.85,1.0,1.2];
        const size=new Adw.ComboRow({
            title:'Tamanho dos medalhões',
            subtitle:'85%, 100% ou 120%',
            model:Gtk.StringList.new(['85% · compacto','100% · normal','120% · ampliado'])
        });
        const sizeIndex=()=>Math.max(0,sizeOptions.findIndex(v=>Math.abs(rivers.get_double('medallion-scale')-v)<0.01));
        size.set_selected(sizeIndex());
        size.connect('notify::selected',()=>{
            const index=size.get_selected();
            if(index<sizeOptions.length && Math.abs(rivers.get_double('medallion-scale')-sizeOptions[index])>0.01)
                rivers.set_double('medallion-scale',sizeOptions[index]);
        });
        rivers.connect('changed::medallion-scale',()=>{
            if(size.get_selected()!==sizeIndex())size.set_selected(sizeIndex());
        });
        visual.add(size);

        const contrast=new Adw.SwitchRow({
            title:'Alto contraste nos medalhões',
            subtitle:'Realça o medalhão selecionado durante a navegação'
        });
        visual.add(contrast);
        rivers.bind('high-contrast',contrast,'active',Gio.SettingsBindFlags.DEFAULT);

        const help=new Adw.SwitchRow({
            title:'Mostrar botão de ajuda (?)',
            subtitle:'O Guia dos Rios permanece fechado até ser solicitado'
        });
        visual.add(help);
        rivers.bind('show-help-button',help,'active',Gio.SettingsBindFlags.DEFAULT);

        const movement=new Adw.PreferencesGroup({
            title:'Navegação e acessibilidade',
            description:'O clique em um aplicativo devolve os rios ao fundo imediatamente.'
        });
        riverPage.add(movement);

        const scanOptions=[2000,3500,5000];
        const scan=new Adw.ComboRow({
            title:'Velocidade da varredura',
            model:Gtk.StringList.new(['2 segundos · rápida','3,5 segundos · normal','5 segundos · lenta'])
        });
        const scanIndex=()=>Math.max(0,scanOptions.indexOf(rivers.get_int('scan-interval-ms')));
        scan.set_selected(scanIndex());
        scan.connect('notify::selected',()=>{
            const index=scan.get_selected();
            if(index<scanOptions.length && rivers.get_int('scan-interval-ms')!==scanOptions[index])
                rivers.set_int('scan-interval-ms',scanOptions[index]);
        });
        rivers.connect('changed::scan-interval-ms',()=>{
            if(scan.get_selected()!==scanIndex())scan.set_selected(scanIndex());
        });
        movement.add(scan);

        const idleOptions=[10000,30000,60000,0];
        const idle=new Adw.ComboRow({
            title:'Recolher rios após inatividade',
            subtitle:'A varredura assistiva não é interrompida automaticamente',
            model:Gtk.StringList.new(['10 segundos','30 segundos','60 segundos','Nunca por tempo'])
        });
        const idleIndex=()=>Math.max(0,idleOptions.indexOf(rivers.get_int('navigation-idle-ms')));
        idle.set_selected(idleIndex());
        idle.connect('notify::selected',()=>{
            const index=idle.get_selected();
            if(index<idleOptions.length && rivers.get_int('navigation-idle-ms')!==idleOptions[index])
                rivers.set_int('navigation-idle-ms',idleOptions[index]);
        });
        rivers.connect('changed::navigation-idle-ms',()=>{
            if(idle.get_selected()!==idleIndex())idle.set_selected(idleIndex());
        });
        movement.add(idle);

        const float=new Adw.SwitchRow({
            title:'Semente permanentemente sobre as janelas',
            subtitle:'Desligado: os rios retornam ao fundo após navegar'
        });
        movement.add(float);
        rivers.bind('floating',float,'active',Gio.SettingsBindFlags.DEFAULT);

        const target=selection(movement,'Monitor da navegação','monitor-target',
            ['Janela ativa (recomendado)','Ponteiro ou toque','Monitor principal','Monitor fixo'],
            ['focused','pointer','primary','fixed']);
        const monitor=new Adw.SpinRow({
            title:'Número do monitor fixo',
            subtitle:'1 = primeira tela, 2 = segunda, 3 = terceira',
            adjustment:new Gtk.Adjustment({lower:1,upper:3,step_increment:1,page_increment:1,value:1})
        });
        movement.add(monitor);
        monitor.set_value(rivers.get_int('fixed-monitor-index')+1);
        monitor.connect('notify::value',()=>{
            const value=Math.round(monitor.get_value())-1;
            if(rivers.get_int('fixed-monitor-index')!==value)
                rivers.set_int('fixed-monitor-index',value);
        });
        rivers.connect('changed::fixed-monitor-index',()=>{
            const value=rivers.get_int('fixed-monitor-index')+1;
            if(Math.round(monitor.get_value())!==value)monitor.set_value(value);
        });
        const updateMonitor=()=>{monitor.sensitive=rivers.get_string('monitor-target')==='fixed';};
        target.connect('notify::selected',updateMonitor);
        updateMonitor();

        const recovery=new Adw.PreferencesGroup({
            title:'Restaurar navegação',
            description:'Não altera os grafismos nem a aparência da TOPBAR.'
        });
        riverPage.add(recovery);
        const resetRivers=new Gtk.Button({
            label:'Restaurar configurações dos rios',
            halign:Gtk.Align.START,margin_top:6,margin_bottom:6
        });
        resetRivers.connect('clicked',()=>{
            for(const key of ['medallion-scale','high-contrast','show-help-button',
                'scan-interval-ms','navigation-idle-ms','floating','monitor-target','fixed-monitor-index'])
                rivers.reset(key);
        });
        recovery.add(resetRivers);
    }
}
