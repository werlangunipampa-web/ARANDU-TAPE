"""Catálogo GIO, instantâneos do GNOME e navegação EWMH em sessões X11."""
import ctypes as C
from ctypes.util import find_library
from pathlib import Path
import json
import os
import time
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, Gio, GLib
from model import APP_ID, Item, plain, window_key

BUS = "org.gnome.Shell"
PATH = "/org/arandulab/Tape/Windows"
IFACE = "org.arandulab.Tape.Windows1"
def own(app):
    return plain(app).replace(".desktop","") in (plain(APP_ID),"arandu-tape-confluencia")

class Catalog:
    def __init__(self):
        self.refresh()
    def refresh(self):
        self.apps={}; self.names={}; self.alias={}; ranks={}
        for info in Gio.AppInfo.get_all():
            ident=info.get_id()
            if not ident or own(ident) or not info.should_show(): continue
            self.apps[ident]=info; self.names[ident]=info.get_display_name() or info.get_name() or ident
            stem=ident[:-8] if ident.endswith(".desktop") else ident
            wm=info.get_startup_wm_class() if isinstance(info,Gio.DesktopAppInfo) else None
            exe=os.path.basename(info.get_executable() or "")
            # O ID de um editor tem prioridade sobre o executável compartilhado com suas preferências.
            for name,score in [(stem,6),(stem.rsplit(".",1)[-1],5),(wm,4),(self.names[ident],3),(exe,1)]:
                if name and score>ranks.get(plain(name),0):
                    self.alias[plain(name)]=ident
                    ranks[plain(name)]=score
    def match(self, *values):
        for val in values:
            key=plain(val or "")
            if key in self.alias: return self.alias[key]
        return ""
    def items(self):
        return sorted((Item("app:"+k,v,k,detail="Aplicativo instalado") for k,v in self.names.items()),key=lambda i:plain(i.title))

class Link:
    """O serviço é publicado somente pela extensão na sessão gráfica."""
    def __init__(self):
        try: self.bus=Gio.bus_get_sync(Gio.BusType.SESSION,None)
        except GLib.Error: self.bus=None
    def call(self, name, args=None):
        if not self.bus: raise RuntimeError("Barramento de sessão indisponível.")
        result=self.bus.call_sync(BUS,PATH,IFACE,name,args,None,
                                  Gio.DBusCallFlags.NO_AUTO_START,550,None)
        values=result.unpack()
        return values[0] if values else None
    def snapshot(self):
        v=json.loads(self.call("Snapshot"))
        wins=[Item(window_key(w["app"],w["title"]),w["title"],w["app"],win=str(w["id"]),detail=w.get("where","")) for w in v["windows"]]
        mem=[Item(window_key(w["app"],w["title"]),w["title"],w["app"],stamp=w["ts"]) for w in v["recent"]]
        freq={a:(n,t) for a,n,t in v["frequency"]}
        return wins,mem,freq

class _GList(C.Structure): pass
_GList._fields_=[("data",C.c_void_p),("next",C.POINTER(_GList)),("prev",C.POINTER(_GList))]

class XWindows:
    """Usa a API C de libwnck3 mesmo quando a distribuição omite seu typelib."""
    def __init__(self, catalog):
        self.catalog=catalog
        self.lib=None; self.screen=None
        display=Gdk.Display.get_default()
        if not display or "x11" not in display.__gtype__.name.lower():return
        name=find_library("wnck-3")
        if not name:return
        lib=C.CDLL(name)
        p=C.c_void_p; s=C.c_char_p; n=C.c_int; t=C.c_uint32
        signatures={
            "screen_get_default":(p,[]),"screen_force_update":(None,[p]),
            "screen_get_windows_stacked":(C.POINTER(_GList),[p]),"screen_get_active_window":(p,[p]),
            "window_get_xid":(C.c_ulong,[p]),"window_get_name":(s,[p]),
            "window_get_class_group_name":(s,[p]),"window_get_class_instance_name":(s,[p]),
            "window_is_skip_tasklist":(n,[p]),"window_get_window_type":(n,[p]),
            "window_get_workspace":(p,[p]),"workspace_get_number":(n,[p]),
            "workspace_activate":(None,[p,t]),"window_activate":(None,[p,t]),
        }
        for func,(ret,args) in signatures.items():
            f=getattr(lib,"wnck_"+func);f.restype=ret;f.argtypes=args;setattr(self,func,f)
        self.lib=lib;self.screen=self.screen_get_default()
    def _windows(self):
        self.screen_force_update(self.screen)
        current=self.screen_get_windows_stacked(self.screen)
        while current:
            w=current.contents.data
            if not self.window_is_skip_tasklist(w) and self.window_get_window_type(w) in (0,3):
                yield w
            current=current.contents.next
    def snapshot(self):
        out=[];active=None
        def decode(v):return (v or b"").decode("utf-8","replace")
        windows=list(self._windows())
        focus=self.screen_get_active_window(self.screen)
        for w in reversed(windows):
            group=decode(self.window_get_class_group_name(w));inst=decode(self.window_get_class_instance_name(w))
            if own(group) or own(inst): continue
            app=self.catalog.match(group,inst)
            title=decode(self.window_get_name(w)) or group or "Janela"
            xid=str(self.window_get_xid(w));space=self.window_get_workspace(w)
            location=("Área de trabalho "+str(self.workspace_get_number(space)+1)) if space else "Todas as áreas"
            item=Item(window_key(app or group,title),title,app,win=xid,detail=location)
            out.append(item)
            if w==focus:active=item
        return out,active
    def activate(self, item, window):
        from gi.repository import GdkX11
        stamp=Gtk.get_current_event_time() or GdkX11.x11_get_server_time(window.get_window())
        for w in self._windows():
            if str(self.window_get_xid(w))==item.win:
                space=self.window_get_workspace(w)
                if space:self.workspace_activate(space,stamp)
                self.window_activate(w,stamp);return True
        return False

def recent_documents(since):
    manager=Gtk.RecentManager.get_default()
    out=[]
    for info in manager.get_items():
        if info.get_private_hint() or not info.is_local() or info.get_modified()<=since:continue
        file=Gio.File.new_for_uri(info.get_uri())
        if not file.query_exists(None):continue
        uri=file.get_uri()
        out.append(Item("uri:"+uri,info.get_display_name(),uri=uri,detail="Arquivo recente",stamp=info.get_modified()))
    return sorted(out,key=lambda x:x.stamp,reverse=True)[:45]

def privacy_enabled():
    source=Gio.SettingsSchemaSource.get_default()
    schema=source.lookup("org.gnome.desktop.privacy",True) if source else None
    if schema and schema.has_key("remember-recent-files"):
        return Gio.Settings.new_full(schema,None,None).get_boolean("remember-recent-files")
    return True

def import_previous(store,cat):
    if store.get("legacy-imported"):return
    sid="org.gnome.shell.extensions.arandu-tape"
    parent=Gio.SettingsSchemaSource.get_default()
    sources=[]
    for base in [GLib.get_user_data_dir(),*GLib.get_system_data_dirs()]:
        path=Path(base)/"gnome-shell/extensions/arandu-tape@arandulab/schemas"
        if (path/"gschemas.compiled").is_file():
            try:sources.append(Gio.SettingsSchemaSource.new_from_directory(str(path),parent,False))
            except GLib.Error:pass
    if parent:sources.append(parent)
    for src in sources:
        schema=src.lookup(sid,True)
        if not schema:continue
        prefs=Gio.Settings.new_full(schema,None,None); ids=[];counts={}
        for name in ("recent-apps","recent-ids"):
            if schema.has_key(name):ids.extend(prefs.get_strv(name))
        if schema.has_key("usage-stats"):
            for val in prefs.get_strv("usage-stats"):
                k,sep,n=val.rpartition("|")
                if sep and n.isdecimal(): counts[k]=int(n)
        if schema.has_key("usage-json"):
            try:
                data=json.loads(prefs.get_string("usage-json"))
                if isinstance(data,dict):counts.update(data)
            except (TypeError,ValueError):pass
        store.import_legacy(ids,counts,cat.names);return

class Desktop:
    def __init__(self,store):
        self.store=store;self.catalog=Catalog();self.link=Link();self.x=XWindows(self.catalog)
        self.mode="limited";self.next_probe=0;self.last=None;self.recent=[];self.freq={}
        self.wins=[];self.docs=[];self.last_docs=0;self.last_launched={}
        if privacy_enabled(): import_previous(store,self.catalog)
    def refresh(self):
        import model
        now=time.monotonic(); allowed=privacy_enabled()
        if now>=self.next_probe:
            try:
                self.wins,self.recent,self.freq=self.link.snapshot()
                self.mode="shell";self.next_probe=now
            except (GLib.Error,RuntimeError,ValueError,KeyError,TypeError):
                self.mode="x11" if self.x.screen else "limited"
                self.recent=[];self.freq={};self.next_probe=now+8
        if self.mode=="x11":
            self.wins,active=self.x.snapshot()
            if active and active.win!=self.last and allowed:
                single=(time.monotonic()-self.last_launched.pop(active.app,-100))>=12
                self.store.remember(active,count=single)
            self.last=active.win if active else None
        elif self.mode=="limited":self.wins=[]
        if allowed and now-self.last_docs>5:
            self.docs=recent_documents(float(self.store.get("clear-time","0")))
            self.last_docs=now
        own_memory=self.store.memory() if allowed else []
        return {
            "memory":model.memory_items(own_memory,self.recent if allowed else [],self.docs if allowed else [],self.wins),
            "open":self.wins,
            "frequent":model.frequency_items(self.store.frequency(),self.freq,self.catalog.names) if allowed else [],
        }
    def open(self,item,window):
        if item.win:
            if self.mode=="shell":
                if self.link.call("Activate",GLib.Variant("(s)",(item.win,))):return
            elif self.mode=="x11" and self.x.activate(item,window):return
            raise RuntimeError("Essa janela já foi fechada. Atualiza o rio e tenta novamente.")
        if item.uri:
            f=Gio.File.new_for_uri(item.uri)
            if not f.query_exists(None):raise RuntimeError("O arquivo foi movido ou excluído.")
            Gio.AppInfo.launch_default_for_uri(item.uri,window.get_display().get_app_launch_context())
        elif item.app in self.catalog.apps:
            w=next((w for w in self.wins if w.app==item.app and
                    (not item.key.startswith("win:") or w.title==item.title)),None)
            if w:
                self.open(w,window)
                return
            self.catalog.apps[item.app].launch([],window.get_display().get_app_launch_context())
        else:raise RuntimeError("Esta janela foi fechada e seu aplicativo não está no catálogo.")
        if privacy_enabled() and (item.uri or self.mode!="shell"):
            self.store.remember(item)
            if item.app:self.last_launched[item.app]=time.monotonic()
    def clear(self):
        if self.mode=="shell": self.link.call("Clear")
        self.store.clear();self.docs=[];self.recent=[];self.freq={};self.last_docs=0
