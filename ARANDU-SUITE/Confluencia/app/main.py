#!/usr/bin/env python3
from pathlib import Path
import json
import os
import signal
import subprocess
import sys
import threading

if "--version" in sys.argv:
    print("Arandu Tape 2.1.0 · Confluência");sys.exit(0)

import gi
gi.require_version("Gtk","3.0")
gi.require_version("Gdk","3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GLib, Pango
from model import APP_ID, RIVERS, NAMES, SUBS, THEMES, Item, Store, command, plain, unique, display_title
from desktop import Desktop, privacy_enabled
from mapview import ASSETS, MapView, PALETTES
import voice

ROOT=Path(__file__).resolve().parent
COMMANDS=[
    ("Abrir memória","Últimas janelas e arquivos","memory","document-open-recent-symbolic"),
    ("O que está aberto?","Trazer uma janela ao primeiro plano","open","focus-windows-symbolic"),
    ("Meus frequentes","Aplicativos mais usados","frequent","starred-symbolic"),
    ("Abrir aplicativos","Ver os aplicativos instalados","apps","view-app-grid-symbolic"),
    ("Modo foco","Ativar o tema Luz suave","focus","weather-clear-night-symbolic"),
    ("Alto contraste","Aumentar o contraste da interface","contrast","preferences-desktop-accessibility-symbolic"),
    ("Modo claro","Voltar ao tema Papel","paper","weather-clear-symbolic"),
    ("Centralizar","Restaurar a posição da Semente","center","zoom-fit-best-symbolic"),
]
GLYPHS={"memory":"memory","open":"open","frequent":"frequent"}
EMPTY={"memory":"Abre um aplicativo ou um arquivo para começar a tua memória.",
       "open":"As janelas aparecem aqui quando um aplicativo está aberto.",
       "frequent":"Os aplicativos ganham lugar neste rio conforme tu os usas."}
MODES={"shell":"GNOME conectado","x11":"Janelas conectadas · X11","limited":"Aguardando integração de janelas"}
def box(orientation=Gtk.Orientation.HORIZONTAL,spacing=0):return Gtk.Box(orientation=orientation,spacing=spacing)
def styled(widget,name):
    widget.get_style_context().add_class(name);return widget
def label(text,cls=None):
    l=Gtk.Label(label=text,xalign=0)
    if cls:styled(l,cls)
    return l
def ellipsis(widget):
    widget.set_ellipsize(Pango.EllipsizeMode.END);widget.set_max_width_chars(32);return widget
def button(label_text=None,icon=None,tip=None):
    b=Gtk.Button();b.set_relief(Gtk.ReliefStyle.NONE)
    row=box(spacing=7)
    if icon:row.pack_start(Gtk.Image.new_from_icon_name(icon,Gtk.IconSize.BUTTON),False,False,0)
    if label_text:row.pack_start(label(label_text),False,False,0)
    row.set_halign(Gtk.Align.CENTER);b.add(row)
    if tip:b.set_tooltip_text(tip);b.get_accessible().set_name(tip)
    return b
def padding(widget,n):
    for side in ("top","bottom","start","end"):getattr(widget,"set_margin_"+side)(n)
def svg_image(name,n):
    return Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(str(ASSETS/name),n,n,True))
def set_children(widget,children):
    for w in widget.get_children():w.destroy()
    for w in children:widget.add(w)
def theme_css(mode,large):
    bg,ink,muted,gold,line,plate=PALETTES[mode]
    chrome={"paper":"#fcfaf4","focus":"#36362f","contrast":"#161a17"}[mode]
    border={"paper":"#d7cebc","focus":"#706951","contrast":"#c3b992"}[mode]
    hover={"paper":"#eee8d9","focus":"#48473a","contrast":"#373c31"}[mode]
    scale=1.23 if large else 1.
    return f"""
    window.tape, .tape dialog, .surface, .surface viewport, .rlist, .rlist row, .tape popover, .prefs {{background-color:{bg};color:{ink};}}
    .surface label, .prefs label, .tape headerbar label, .tape popover label {{color:{ink};}}
    .surface label, .prefs label, .tape popover label {{font-size:{round(13*scale)}px;}}
    headerbar.top {{background-image:none;background-color:{chrome};border-bottom:1px solid {border};box-shadow:none;color:{ink};min-height:48px;padding:0 10px;}}
    .top button, .surface button, .prefs button, .tape popover button {{color:{ink};background-image:none;text-shadow:none;box-shadow:none;}}
    .top button:hover, .flatbtn:hover, .foot button:hover, .prefs button:hover {{background-color:{hover};}}
    .top .brand {{font-size:{round(15*scale)}px;letter-spacing:3px;font-weight:600;}}
    .top .brand-sub {{font-size:{round(10*scale)}px;letter-spacing:1px;color:{muted};}}
    .top .searchbutton, .soft, .prefs button.choice {{background-color:{plate};border:1px solid {border};border-radius:7px;}}
    .top .searchbutton {{padding:4px 11px;}}
    .rail {{background-color:{chrome};border-top:1px solid {border};padding:10px 14px;}}
    button.rivercard {{background-color:transparent;border-radius:7px;padding:8px 12px;border:1px solid transparent;}}
    button.rivercard:hover, button.rivercard:focus {{background-color:{hover};border-color:{border};}}
    .rivercard .rivername {{font-family:Georgia,serif;font-size:{round(21*scale)}px;}}
    .surface .sub, .surface .foot-label, .prefs .sub, .tape popover .sub {{color:{muted};font-size:{round(11*scale)}px;}}
    .surface .count {{color:{gold};font-weight:bold;font-size:{round(12*scale)}px;}}
    .foot {{background-color:{chrome};border-top:1px solid {border};padding:3px 16px;}}
    .foot button {{font-size:{round(11*scale)}px;min-height:24px;padding:0 6px;}}
    .foot .dot {{color:{gold};}}
    button.hotspot {{background:transparent;border:1px solid transparent;padding:0;min-width:0;min-height:0;border-radius:22px;box-shadow:none;}}
    button.hotspot:hover {{background-color:alpha({gold},.09);}}
    button.hotspot:focus {{outline:2px solid {gold};outline-offset:-2px;background-color:alpha({gold},.11);}}
    .tape button:focus, .prefs button:focus {{outline-color:{gold};}}
    .surface .heading, .prefs .heading {{font-family:Georgia,serif;font-size:{round(27*scale)}px;color:{ink};}}
    .surface .list-title {{font-size:{round(14*scale)}px;font-weight:600;}}
    .rlist row {{border-bottom:1px solid {border};padding:7px 12px;}}
    .rlist row:hover, .rlist row:selected, .rlist row:focus {{background-color:{hover};}}
    .surface entry, .prefs entry {{background:{chrome};color:{ink};border:1px solid {border};border-radius:8px;padding:7px 10px;caret-color:{ink};}}
    .prefs button:checked {{background:{ink};border-color:{gold};color:{bg};}}
    .prefs button:checked label {{color:{bg};}}
    .toast {{background:#2c342d;color:#fff3db;border-radius:7px;padding:8px 14px;}}
    .surface .toast label {{color:#fff3db;}}
    """

class Window(Gtk.ApplicationWindow):
    def __init__(self,app):
        super().__init__(application=app,title="Arandu Tape")
        self.set_icon_from_file(str(ASSETS/"semente.svg"));styled(self,"tape")
        self.store=Store();self.desktop=Desktop(self.store)
        self.theme=self.store.get("theme","paper")
        if self.theme not in THEMES:self.theme="paper"
        self.large=self.store.get("large")=="1";self.data={r:[] for r in RIVERS}
        self.page="map";self.filter="";self.list_sig=None;self.shortway=None;self.pop=None
        self.voice_proc=None;self.toast_id=0;self.destroying=False
        self.css=Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(self.get_screen(),self.css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.style()
        display=self.get_display();monitor=display.get_primary_monitor() or display.get_monitor(0)
        area=monitor.get_workarea() if monitor else None
        self.set_default_size(min(1190,area.width-32) if area else 1190,
                              min(730,area.height-42) if area else 730)
        self.set_size_request(560,410)
        head=styled(Gtk.HeaderBar(),"top");head.set_show_close_button(True)
        head.set_size_request(-1, 52) # Reserva de layout; controles nativos preservados.
        self.set_titlebar(head);brand=box(spacing=9);brand.pack_start(svg_image("marca.svg",38),False,False,0)
        words=box(Gtk.Orientation.VERTICAL,1)
        words.set_valign(Gtk.Align.CENTER)
        words.pack_start(label("ARANDU TAPE","brand"),False,False,0)
        brand.pack_start(words,False,False,0)
        head.pack_start(brand);head.set_custom_title(Gtk.Label(label=""))
        settings=button(icon="preferences-system-symbolic",tip="Aparência e acessibilidade")
        settings.connect("clicked",lambda *_:self.preferences());head.pack_end(settings)
        self.search_btn=styled(button("Buscar","system-search-symbolic","Buscar aplicativos, janelas e comandos (Ctrl+K)"),"searchbutton")
        self.search_btn.connect("clicked",lambda *_:self.show_page("search"));head.pack_end(self.search_btn)
        self.root=styled(box(Gtk.Orientation.VERTICAL),"surface");self.add(self.root)
        self.overlay=Gtk.Overlay();self.root.pack_start(self.overlay,True,True,0)
        self.stack=Gtk.Stack();self.overlay.add(self.stack)
        self.map_page=box(Gtk.Orientation.VERTICAL);self.stack.add_named(self.map_page,"map")
        self.map=MapView(self);self.map_page.pack_start(self.map,True,True,0)
        rail=styled(box(spacing=1),"rail");rail.set_homogeneous(True);self.map_page.pack_end(rail,False,False,0)
        self.card_labels={}
        for river in RIVERS:
            b=styled(Gtk.Button(),"rivercard");b.set_relief(Gtk.ReliefStyle.NONE);b.connect("clicked",lambda _,r=river:self.show_page(r))
            b.get_accessible().set_name("Ver todos em "+NAMES[river])
            cells=box(spacing=10);cells.pack_start(svg_image(GLYPHS[river]+".svg",38),False,False,0)
            words=box(Gtk.Orientation.VERTICAL,3)
            titleline=box(spacing=8);titleline.pack_start(label(NAMES[river],"rivername"),False,False,0)
            count=label("0","count");titleline.pack_start(count,False,False,0);words.pack_start(titleline,False,False,0)
            detail=ellipsis(label(SUBS[river],"sub"));words.pack_start(detail,False,False,0)
            cells.pack_start(words,True,True,0);cells.pack_end(label("›","count"),False,False,3)
            b.add(cells);rail.pack_start(b,True,True,0);self.card_labels[river]=(count,detail)
        self.detail=box(Gtk.Orientation.VERTICAL,9);padding(self.detail,16);self.stack.add_named(self.detail,"detail")
        top=box(spacing=11);self.detail.pack_start(top,False,False,0)
        self.back=button(icon="go-previous-symbolic",tip="Voltar ao mapa (Esc)");self.back.connect("clicked",lambda *_:self.show_page("map"))
        top.pack_start(self.back,False,False,0);self.title_label=label("","heading");top.pack_start(self.title_label,True,True,0)
        self.file_button=styled(button("Abrir arquivo","document-open-symbolic"),"soft")
        self.file_button.connect("clicked",lambda *_:self.choose_file());top.pack_end(self.file_button,False,False,0)
        self.audio=styled(button("Ouvir comando","audio-input-microphone-symbolic"),"soft");self.audio.connect("clicked",lambda *_:self.listen())
        top.pack_end(self.audio,False,False,0)
        self.entry=Gtk.SearchEntry();self.entry.connect("search-changed",self._changed);self.entry.connect("activate",self._entry_activate)
        self.detail.pack_start(self.entry,False,False,0);self.explain=label("","sub");self.explain.set_line_wrap(True);self.detail.pack_start(self.explain,False,False,0)
        scroll=Gtk.ScrolledWindow();scroll.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC);self.detail.pack_start(scroll,True,True,0)
        self.rows=styled(Gtk.ListBox(),"rlist");self.rows.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.rows.connect("row-activated",lambda _,row: self.run_row(row));scroll.add(self.rows)
        self.empty_box=box(Gtk.Orientation.VERTICAL,12);padding(self.empty_box,20)
        self.empty=label("","sub");self.empty.set_line_wrap(True);self.empty_box.pack_start(self.empty,False,False,0)
        self.empty_action=styled(button("Escolher aplicativo","view-app-grid-symbolic"),"soft");self.empty_action.set_halign(Gtk.Align.START)
        self.empty_action.connect("clicked",lambda *_:self.show_page("apps"));self.empty_box.pack_start(self.empty_action,False,False,0)
        self.rows.set_placeholder(self.empty_box)
        foot=styled(box(spacing=7),"foot");self.root.pack_end(foot,False,False,0)
        foot.pack_start(label("●","dot"),False,False,0);self.status=label("Conectando…","foot-label");foot.pack_start(self.status,True,True,0)
        apps=button("Aplicativos","view-app-grid-symbolic");apps.connect("clicked",lambda *_:self.show_page("apps"));foot.pack_end(apps,False,False,0)
        commands=button("Comandos","input-keyboard-symbolic");commands.connect("clicked",lambda *_:self.show_page("commands"));foot.pack_end(commands,False,False,0)
        self.toast=styled(box(spacing=6),"toast");self.toast_label=label("");self.toast_label.set_line_wrap(True);self.toast.add(self.toast_label)
        self.toast.set_halign(Gtk.Align.CENTER);self.toast.set_valign(Gtk.Align.END);self.toast.set_margin_bottom(10)
        self.overlay.add_overlay(self.toast);self.overlay.set_overlay_pass_through(self.toast,True)
        self.connect("key-press-event",self._key);self.connect("destroy",self._destroy)
        self.connect("map-event",lambda *_:self.update(force=True) and False)
        try:self.catalog_monitor=Gio.AppInfoMonitor.get();self.catalog_handler=self.catalog_monitor.connect("changed",self._catalog_change)
        except (AttributeError,GLib.Error):self.catalog_monitor=None
        self.show_all();self.toast.set_no_show_all(True);self.toast.hide()
        self.show_page("map");self.update(force=True);self.timer=GLib.timeout_add(1000,self.update)
    def style(self):
        self.css.load_from_data(theme_css(self.theme,self.large).encode())
    def notify(self,msg):
        if self.destroying:return
        self.toast_label.set_text(msg);self.toast.show_all();self.toast.show()
        if self.toast_id:GLib.source_remove(self.toast_id)
        self.toast_id=GLib.timeout_add(5100,self._hide_toast)
    def _hide_toast(self):
        self.toast_id=0;self.toast.hide();return False
    def _destroy(self,*_):
        self.destroying=True
        if getattr(self,"timer",0):GLib.source_remove(self.timer)
        if self.toast_id:GLib.source_remove(self.toast_id)
        if self.catalog_monitor:self.catalog_monitor.disconnect(self.catalog_handler)
        self.stop_voice();self.store.db.close()
    def _catalog_change(self,*_):
        self.desktop.catalog.refresh();self.update(force=True)
    def update(self,force=False):
        if self.destroying:return False
        new=self.desktop.refresh()
        if new!=self.data or force:
            self.data=new
            for r,(count,detail) in self.card_labels.items():
                count.set_text(str(len(new[r])));detail.set_text(display_title(new[r][0].title) if new[r] else SUBS[r])
            if self.page=="map":self.map.invalidate()
            else:self.render_rows()
        self.status.set_text(MODES[self.desktop.mode]);return True
    def show_page(self,page):
        if page not in (*RIVERS,"map","apps","search","commands"):page="map"
        self.page=page;self.list_sig=None
        if self.pop:self.pop.popdown()
        if page=="map":
            self.stack.set_visible_child_name("map");self.map.invalidate()
            if "seed" in self.map.buttons:self.map.buttons["seed"].grab_focus()
            return
        self.stack.set_visible_child_name("detail")
        self.title_label.set_text(NAMES.get(page,{"apps":"Aplicativos","search":"Buscar","commands":"Comandos"}.get(page,"")))
        self.audio.set_visible(page in ("search","commands"));self.file_button.set_visible(page in ("memory","apps","search"))
        self.entry.set_placeholder_text("Digita um comando ou um nome…" if page in ("commands","search") else "Filtrar por nome…")
        self.entry.set_text("");self.render_rows();self.entry.grab_focus()
    def _changed(self,*_):
        if self.page!="map":self.render_rows()
    def rows_data(self):
        q=plain(self.entry.get_text())
        choices=[]
        if self.page in RIVERS:
            choices=[(i,None) for i in self.data[self.page]]
        elif self.page=="apps":
            choices=[(i,None) for i in self.desktop.catalog.items()]
        else:
            if self.page=="search":
                people=list(unique([*self.data["open"],*self.data["memory"],*self.desktop.catalog.items()]))
                choices.extend((i,None) for i in people)
            cmds=[(Item("cmd:"+a,t,detail=d),a) for t,d,a,icon in COMMANDS]
            choices=(cmds+choices) if q or self.page=="commands" else choices+cmds
        return [(i,act) for i,act in choices if not q or q in plain(i.title+" "+i.app+" "+i.detail)]
    def render_rows(self):
        if self.page=="map":return
        candidates=self.rows_data();sig=(self.page,self.entry.get_text(),tuple((i,act) for i,act in candidates),self.desktop.mode)
        if self.list_sig==sig:return
        self.list_sig=sig;prev=self.rows.get_selected_row();oldkey=prev.item.key if prev else None
        for child in self.rows.get_children():child.destroy()
        for item,act in candidates:
            row=Gtk.ListBoxRow();row.item=item;row.action=act
            band=box(spacing=12);info=self.desktop.catalog.apps.get(item.app)
            gicon=info.get_icon() if info else None
            if gicon:icon=Gtk.Image.new_from_gicon(gicon,Gtk.IconSize.LARGE_TOOLBAR)
            else:
                choice=next((c[3] for c in COMMANDS if c[2]==act),None) or ("text-x-generic-symbolic" if item.uri else "focus-windows-symbolic")
                icon=Gtk.Image.new_from_icon_name(choice,Gtk.IconSize.LARGE_TOOLBAR)
            icon.set_size_request(32,30);band.pack_start(icon,False,False,0)
            col=box(Gtk.Orientation.VERTICAL,2);col.pack_start(ellipsis(label(display_title(item.title),"list-title")),False,False,0)
            detail=item.detail or self.desktop.catalog.names.get(item.app) or "Janela recente"
            if item.count:detail=f"{item.count} acesso"+("s" if item.count!=1 else "")
            col.pack_start(ellipsis(label(detail,"sub")),False,False,0);band.pack_start(col,True,True,0)
            band.pack_end(label("›","count"),False,False,5);row.add(band);self.rows.add(row)
            if item.key==oldkey:self.rows.select_row(row)
        self.rows.show_all()
        tips={"memory":"Retoma uma janela ou reabre um arquivo recente.",
              "open":"Seleciona uma janela para trazê-la à frente.","frequent":"Os primeiros da lista ficam mais perto da Semente.",
              "apps":"Aplicativos disponíveis nesta máquina.","search":"Busca nos teus rios, aplicativos e comandos.",
              "commands":"Ctrl+1, 2 e 3 abrem os rios. Usa as setas nos medalhões, Enter para abrir e Esc para voltar."}
        message=tips[self.page]
        if self.page=="open" and self.desktop.mode=="limited":message="Para ver janelas no Wayland, ativa Arandu Tape · Confluência no app Extensões do GNOME."
        if self.page in ("memory","frequent") and not privacy_enabled():message="O histórico está pausado nas preferências de privacidade do GNOME."
        self.explain.set_text(message)
        self.empty.set_text("Nenhum resultado para esta busca." if self.entry.get_text() else EMPTY.get(self.page,"Nenhum item disponível."))
        self.empty_action.set_visible(self.page in RIVERS);self.empty_box.show();self.empty.show()
    def run_row(self,row):
        if row.action:self.run_action(row.action)
        else:self.activate_item(row.item)
    def activate_item(self,item):
        try:
            self.desktop.open(item,self);self.update(force=True)
            if not item.win:self.notify("Abrindo "+item.title)
        except (GLib.Error,RuntimeError,OSError) as exc:self.notify(str(exc));self.update(force=True)
    def _entry_activate(self,*_):
        q=self.entry.get_text()
        if self.page in ("search","commands") and q:
            action,arg=command(q)
            if action!="find" or any(plain(q).startswith(p) for p in ("abrir ","ir para ")):
                return self.run_action(action,arg)
        row=self.rows.get_selected_row() or self.rows.get_row_at_index(0)
        if row:self.run_row(row)
    def run_action(self,act,arg=""):
        if act in (*RIVERS,"apps","commands"):self.show_page(act)
        elif act=="find":
            self.show_page("search");self.entry.set_text(arg);self.render_rows()
            matches=self.rows_data();exact=[i for i,a in matches if not a and plain(i.title)==arg]
            if len(exact)==1:self.activate_item(exact[0])
            elif len(matches)==1 and matches[0][1] is None:self.activate_item(matches[0][0])
        elif act in THEMES:self.set_theme(act);self.show_page("map")
        elif act=="center":self.map.center();self.show_page("map")
        elif act in ("seed","expand"):
            self.show_page("map");self.seed_panel(self.map.buttons.get("seed",self.search_btn))
    def set_theme(self,t):
        self.theme=t;self.store.set("theme",t);self.style();self.map.invalidate()
    def seed_panel(self,anchor):
        if self.pop:self.pop.destroy()
        self.pop=Gtk.Popover.new(anchor);col=box(Gtk.Orientation.VERTICAL,3);padding(col,12)
        col.pack_start(label("Semente","heading"),False,False,0)
        for r in RIVERS:
            b=button(NAMES[r]+"   ·   "+str(len(self.data[r])));b.connect("clicked",lambda _,g=r:self.show_page(g));col.pack_start(b,False,False,0)
        recenter=button("Centralizar mapa","zoom-fit-best-symbolic");recenter.connect("clicked",lambda *_:self.run_action("center"));col.pack_start(recenter,False,False,0)
        self.pop.add(col);self.pop.show_all();self.pop.popup()
    def _key(self,win,e):
        k=Gdk.keyval_to_lower(e.keyval);ctrl=e.state&Gdk.ModifierType.CONTROL_MASK
        if ctrl and k in (Gdk.KEY_1,Gdk.KEY_2,Gdk.KEY_3):self.show_page(RIVERS[k-Gdk.KEY_1]);return True
        if ctrl and k==Gdk.KEY_k:self.show_page("search");return True
        if k==Gdk.KEY_Escape:
            if self.voice_proc:self.stop_voice();self.notify("Escuta encerrada.")
            elif self.pop and self.pop.get_visible():self.pop.popdown()
            else:self.show_page("map")
            return True
        if k==Gdk.KEY_slash and self.page=="map":self.show_page("commands");return True
        if k==Gdk.KEY_F1:self.show_page("commands");return True
        return False
    def choose_file(self):
        dlg=Gtk.FileChooserNative.new("Escolher arquivo",self,Gtk.FileChooserAction.OPEN,"Abrir","Cancelar")
        if dlg.run()==Gtk.ResponseType.ACCEPT:
            f=dlg.get_file()
            if f:
                u=f.get_uri();self.activate_item(Item("uri:"+u,f.get_basename() or u,uri=u,detail="Arquivo"))
        dlg.destroy()
    def preferences(self):
        d=Gtk.Dialog(title="Aparência e acessibilidade",transient_for=self,modal=True,destroy_with_parent=True)
        styled(d,"prefs");d.add_button("Concluir",Gtk.ResponseType.CLOSE);d.set_default_size(480,340)
        body=d.get_content_area();padding(body,18);body.set_spacing(9)
        body.add(label("Aparência","heading"));choices=box(spacing=6);buttons=[]
        for k,title in THEMES.items():
            b=Gtk.RadioButton.new_with_label_from_widget(buttons[0] if buttons else None,title)
            b.set_mode(False);styled(b,"choice");buttons.append(b);choices.add(b);b.set_active(k==self.theme)
            b.connect("toggled",lambda w,t=k:w.get_active() and self.set_theme(t))
        body.add(choices)
        row=box(spacing=8);row.pack_start(label("Baixa visão · ampliar texto e medalhões"),True,True,0)
        sw=Gtk.Switch();sw.set_active(self.large);sw.connect("notify::active",self._large);row.pack_end(sw,False,False,0);body.add(row)
        body.add(Gtk.Separator());body.add(label("Voz em português","list-title"))
        model_path=self.store.get("voice-model");desc=label(Path(model_path).name if model_path else "Escolhe um modelo Vosk instalado para ouvir comandos locais.","sub");desc.set_line_wrap(True);body.add(desc)
        f=button("Escolher pasta do modelo","folder-open-symbolic");body.add(f)
        def model_folder(*_):
            fd=Gtk.FileChooserNative.new("Modelo de voz em português",d,Gtk.FileChooserAction.SELECT_FOLDER,"Escolher","Cancelar")
            if fd.run()==Gtk.ResponseType.ACCEPT:
                p=fd.get_filename()
                if p and (Path(p)/"am").is_dir():self.store.set("voice-model",p);desc.set_text(Path(p).name)
                else:desc.set_text("Escolhe a pasta extraída que contém o diretório am.")
            fd.destroy()
        f.connect("clicked",model_folder)
        body.add(Gtk.Separator());tools=box(spacing=8);body.add(tools)
        reset=button("Centralizar mapa","zoom-fit-best-symbolic");reset.connect("clicked",lambda *_:self.map.center());tools.add(reset)
        clear=button("Limpar histórico","edit-clear-all-symbolic");clear.connect("clicked",lambda *_:self.clear_history(d));tools.add(clear)
        d.show_all();d.run();d.destroy()
    def _large(self,widget,*_):
        self.large=widget.get_active();self.store.set("large",int(self.large));self.style();self.map.invalidate()
    def clear_history(self,parent):
        d=Gtk.MessageDialog(transient_for=parent,modal=True,message_type=Gtk.MessageType.QUESTION,
                            buttons=Gtk.ButtonsType.CANCEL,text="Limpar Memória e Frequentes?")
        d.format_secondary_text("Os registros do Arandu serão apagados. Os arquivos pessoais continuarão na máquina.")
        d.add_button("Limpar",Gtk.ResponseType.OK);reply=d.run();d.destroy()
        if reply==Gtk.ResponseType.OK:
            try:self.desktop.clear();self.update(force=True)
            except (GLib.Error,RuntimeError) as exc:self.notify(str(exc))
    def stop_voice(self):
        proc=self.voice_proc;self.voice_proc=None
        if proc and proc.poll() is None:
            try:os.killpg(proc.pid,signal.SIGTERM)
            except ProcessLookupError:pass
        if not self.destroying:self.audio.set_sensitive(True)
    def listen(self):
        if self.voice_proc:return
        model=self.store.get("voice-model")
        if not model:
            self.preferences();model=self.store.get("voice-model")
            if not model:return
        try:
            p=subprocess.Popen([voice.runtime(),str(ROOT/"voice.py"),model],stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL,start_new_session=True,text=True)
        except OSError as exc:self.notify(str(exc));return
        self.voice_proc=p;self.audio.set_sensitive(False);self.notify("Ouvindo um comando… Esc encerra a escuta.")
        def worker():
            try:
                out,_=p.communicate(timeout=30);value=json.loads(out or "{}")
            except subprocess.TimeoutExpired:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
                p.communicate();value={"error":"O reconhecimento excedeu o tempo disponível."}
            except (ValueError,OSError):value={"error":"O reconhecimento foi interrompido."}
            GLib.idle_add(finish,value)
        def finish(value):
            if self.destroying or self.voice_proc is not p:return False
            self.voice_proc=None;self.audio.set_sensitive(True);q=value.get("text","")
            if q:self.run_action(*command(q));self.notify("Reconhecido: "+q)
            else:self.notify(value.get("error","Nenhum comando reconhecido."))
            return False
        threading.Thread(target=worker,daemon=True).start()

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.HANDLES_OPEN)
        self.win=None
    def do_activate(self):
        if not self.win:
            self.win=Window(self)
            self.win.connect("destroy",lambda *_:setattr(self,"win",None))
        self.win.present()
    def do_open(self,files,n_files,hint):
        self.activate()
        if files and files[0].get_uri_scheme()=="arandu-tape":
            self.win.show_page(files[0].get_basename())

def main():
    import argparse
    parser=argparse.ArgumentParser(prog="arandu-tape-confluencia")
    parser.add_argument("--rio",choices=(*RIVERS,"map","apps","commands","search"))
    args=parser.parse_args()
    GLib.set_prgname(APP_ID);GLib.set_application_name("Arandu Tape")
    app=Application()
    argv=[sys.argv[0]]
    if args.rio:argv.append("arandu-tape:///"+args.rio)
    return app.run(argv)

if __name__=="__main__":sys.exit(main())
