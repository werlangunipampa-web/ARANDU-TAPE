"""Mapa vetorial e controles GTK acessíveis. A arte e sua geometria são as mesmas no Shell."""
import functools
import io
import json
import math
from pathlib import Path
import random
import sys
import zlib
import cairo
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Atk
from model import NAMES, RIVERS, display_title

ASSETS=Path(__file__).resolve().parent/"assets"
NODES=json.loads((ASSETS/"geometria.json").read_text())
PALETTES={
    "paper":("#f8f5ed","#282e29","#655f52","#976c36","#9f8e6c","#f4ecdb"),
    "focus":("#302f2a","#eee1c8","#d1c3a6","#e1ba80","#a4997f","#3c3a32"),
    "contrast":("#101311","#fffdfa","#f4efdf","#ffe399","#d2c28f","#232823"),
}
DESC={"memory":"Últimos passos","open":"Nesta sessão","frequent":"Mais usados"}

def color(cr,hexcode,alpha=1):
    vals=[int(hexcode[n:n+2],16)/255 for n in (1,3,5)]
    cr.set_source_rgba(*vals,alpha)

def ring(cr,x,y,r,ink,width=1,alpha=1,dash=None):
    cr.save();cr.new_path();cr.set_line_width(width);color(cr,ink,alpha)
    if dash:cr.set_dash(dash)
    cr.arc(x,y,r,0,math.tau);cr.stroke();cr.restore()

def diamond(cr,x,y,r,ink,alpha=1):
    cr.new_path();cr.move_to(x,y-r);cr.line_to(x+r,y);cr.line_to(x,y+r);cr.line_to(x-r,y);cr.close_path();color(cr,ink,alpha);cr.stroke()

def rounded(cr,x,y,w,h,r):
    r=min(r,w/2,h/2);cr.new_sub_path()
    for cx,cy,a in [(x+w-r,y+r,-90),(x+w-r,y+h-r,0),(x+r,y+h-r,90),(x+r,y+r,180)]:
        cr.arc(cx,cy,r,math.radians(a),math.radians(a+90))
    cr.close_path()

def text_at(cr,x,y,text,size,ink,bold=False,serif=False,italic=False,spacing=0,align="left"):
    cr.save()
    cr.select_font_face("DejaVu Serif" if serif else "DejaVu Sans",
                        cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size);color(cr,ink)
    width=cr.text_extents(text)[4] + max(0,len(text)-1)*spacing
    start=x-width/2 if align=="center" else x
    cr.move_to(start,y)
    if spacing:
        for ch in text:
            cr.show_text(ch);cr.rel_move_to(spacing,0)
    else:cr.show_text(text)
    cr.restore();return width

@functools.lru_cache(maxsize=80)
def art(name,w,h):
    p=GdkPixbuf.Pixbuf.new_from_file_at_scale(str(ASSETS/name),max(1,w),max(1,h),False)
    return pix_surface(p)

def pix_surface(p):
    ok,data=p.save_to_bufferv("png",[],[])
    return cairo.ImageSurface.create_from_png(io.BytesIO(data))

def paint(cr,s,x,y,w,h):
    cr.save();cr.translate(x,y);cr.scale(w/s.get_width(),h/s.get_height())
    cr.set_source_surface(s,0,0);cr.paint();cr.restore()

def draw_landscape(cr, x, y, w, h):
    """Vinheta vetorial procedural ARANDU; sem fotografia ou textura externa."""
    cr.save()
    cr.translate(x, y)
    cr.scale(w, h)
    sky = cairo.LinearGradient(0, 0, 0, 1)
    sky.add_color_stop_rgb(0, .20, .32, .29)
    sky.add_color_stop_rgb(.65, .67, .66, .47)
    sky.add_color_stop_rgb(1, .87, .78, .55)
    cr.set_source(sky)
    cr.rectangle(0, 0, 1, 1)
    cr.fill()
    color(cr, "#e9d4a0", .75)
    cr.arc(.74, .25, .09, 0, math.tau)
    cr.fill()
    for ink, start, points in (
        ("#526b57", .50, ((.15,.36,.32,.37,.48,.55),(.70,.76,.84,.29,1,.46))),
        ("#354e42", .68, ((.18,.44,.37,.61,.55,.69),(.75,.75,.83,.49,1,.56))),
        ("#263f35", .82, ((.20,.68,.32,.67,.53,.80),(.71,.91,.85,.65,1,.73))),
    ):
        cr.move_to(0, start)
        for curve in points:
            cr.curve_to(*curve)
        cr.line_to(1, 1)
        cr.line_to(0, 1)
        cr.close_path()
        color(cr, ink)
        cr.fill()
    cr.move_to(.52, .66)
    cr.curve_to(.45,.75,.78,.77,.66,.86)
    cr.curve_to(.57,.92,.39,.95,.31,1)
    cr.line_to(.53,1)
    cr.curve_to(.60,.96,.82,.91,.81,.86)
    cr.curve_to(.80,.77,.49,.74,.52,.66)
    cr.close_path()
    color(cr, "#b9b58a", .85)
    cr.fill()
    cr.restore()


def icon_kind(item, group, n):
    if not item:return group
    motifs={
        "memory":("flower","woven","frequent","memory","diamond"),
        "open":("open","flower","woven","frequent","diamond"),
        "frequent":("woven","diamond","frequent","memory","flower"),
    }
    # Um glifo estável identifica o item. O pequeno selo conserva o ícone real do aplicativo.
    return motifs[group][zlib.crc32((item.app or item.title).encode("utf-8")+item.key.encode("utf-8"))%5]


def paper(cr,w,h,pal,theme):
    bg,fg,muted,gold,line,plate=pal
    color(cr,bg);cr.paint()
    if theme=="contrast":return
    if theme=="paper":
        surface=art("papel-e1.svg",1200,675)
        cr.save();cr.scale(w/surface.get_width(),h/surface.get_height())
        cr.set_source_surface(surface,0,0);cr.paint_with_alpha(.54);cr.restore()
    # Linhas de relevo discretas em dois cantos, como num mapa gravado.
    for side in (0,1):
        cr.save()
        if side:cr.translate(w,h);cr.rotate(math.pi)
        color(cr,line,.13 if theme=="paper" else .12);cr.set_line_width(.65)
        for k in range(17):
            px=-w*.06;py=h*(.70+k*.014)
            cr.move_to(px,py)
            cr.curve_to(w*.034,py-h*.08,w*.063,py+h*.09,w*.078,py+h*.133)
            cr.curve_to(w*.106,py+h*.23,w*.19,py+h*.089,w*.27,py+h*.30);cr.stroke()
        cr.restore()
    rng=random.Random(96)
    color(cr,line,.12 if theme=="paper" else .11)
    for _ in range(min(3900,w*h//125)):
        x=rng.random()*w;y=rng.random()*h
        cr.rectangle(x,y,.7+rng.random()*.7,.65)
    cr.fill()

def to_pixbuf(surface):
    surface.flush();raw=bytes(surface.get_data());rgba=bytearray(len(raw))
    if sys.byteorder=="little":
        rgba[0::4]=raw[2::4];rgba[1::4]=raw[1::4];rgba[2::4]=raw[0::4];rgba[3::4]=raw[3::4]
    else:
        rgba[0::4]=raw[1::4];rgba[1::4]=raw[2::4];rgba[2::4]=raw[3::4];rgba[3::4]=raw[0::4]
    return GdkPixbuf.Pixbuf.new_from_bytes(GLib.Bytes.new(bytes(rgba)),GdkPixbuf.Colorspace.RGB,True,8,
                                          surface.get_width(),surface.get_height(),surface.get_stride())

class FlexibleImage(Gtk.Image):
    def do_get_preferred_width(self):return 1,1
    def do_get_preferred_height(self):return 1,1

class Hotspots(Gtk.Fixed):
    def do_get_preferred_width(self):return 1,1
    def do_get_preferred_height(self):return 1,1

class MapView(Gtk.Overlay):
    def __init__(self, host):
        super().__init__()
        self.host=host;self.image=FlexibleImage();self.add(self.image)
        self.layer=Hotspots();self.add_overlay(self.layer)
        self.buttons={};self.pending=0;self.last_size=None;self.drag=None;self.moved=False
        self.dx,self.dy=(self.read_offset(k) for k in ("map-x","map-y"))
        self.points={};self.items={};self.icons={};self.pin_focus=None
        self.set_hexpand(True);self.set_vexpand(True)
        self.get_accessible().set_name("Mapa dos três rios")
        self.connect("size-allocate",self._resize)
        self.connect("destroy",self._destroy)
    def read_offset(self,k):
        try:return max(-.18,min(.18,float(self.host.store.get(k,"0"))))
        except ValueError:return 0
    def _destroy(self,*_):
        if self.pending:GLib.source_remove(self.pending);self.pending=0
    def _resize(self,widget,a):
        size=(a.width,a.height)
        if size!=self.last_size:self.last_size=size;self.invalidate()
    def invalidate(self):
        if not self.pending:self.pending=GLib.idle_add(self.render)
    def center(self):
        self.dx=self.dy=0;self.host.store.set("map-x","0");self.host.store.set("map-y","0");self.invalidate()
    def node_icon(self,item,n):
        remote=self.host.desktop.catalog.apps.get(item.app)
        icon=remote.get_icon() if remote else None
        if not icon:
            icon=GioIcon("text-x-generic" if item.uri else "preferences-system-windows")
        key=(icon.to_string(),n)
        if key not in self.icons:
            try:
                theme=Gtk.IconTheme.get_default()
                obj=theme.lookup_by_gicon(icon,n,Gtk.IconLookupFlags.FORCE_SIZE)
                self.icons[key]=pix_surface(obj.load_icon()) if obj else None
            except GLib.Error:self.icons[key]=None
        return self.icons[key]
    def add_zone(self,areas,key,rect,name,item=None):
        areas[key]=(rect,name,item)
    def sync(self,areas):
        for key in self.buttons.keys()-areas.keys():
            self.buttons.pop(key).destroy()
        for key,(rect,name,item) in areas.items():
            if key not in self.buttons:
                b=Gtk.Button();b.set_relief(Gtk.ReliefStyle.NONE);b.get_style_context().add_class("hotspot")
                b.connect("clicked",self._click,key);b.connect("query-tooltip",self._tip,key)
                b.set_has_tooltip(True)
                if key=="seed":
                    for ev,cb in [("button-press-event",self._press),("motion-notify-event",self._motion),("button-release-event",self._release)]:b.connect(ev,cb)
                    b.add_events(Gdk.EventMask.POINTER_MOTION_MASK|Gdk.EventMask.BUTTON_RELEASE_MASK|Gdk.EventMask.BUTTON_PRESS_MASK)
                b.connect("key-press-event",self._nav,key)
                self.buttons[key]=b;self.layer.put(b,0,0);b.show()
            b=self.buttons[key];b.get_accessible().set_name(name)
            x,y,w,h=map(round,rect)
            b.set_size_request(max(1,w),max(1,h));self.layer.move(b,x,y)
        self.items={k:v[2] for k,v in areas.items()}
        self.points={k:(r[0][0]+r[0][2]/2,r[0][1]+r[0][3]/2) for k,r in areas.items()}
    def _nav(self,b,e,key):
        keys={Gdk.KEY_Left:(-1,0),Gdk.KEY_Right:(1,0),Gdk.KEY_Up:(0,-1),Gdk.KEY_Down:(0,1)}
        if e.keyval not in keys or key not in self.points:return False
        dx,dy=keys[e.keyval];x,y=self.points[key];opts=[]
        for k,(x2,y2) in self.points.items():
            forward=(x2-x)*dx+(y2-y)*dy
            if forward>2:opts.append((math.hypot(x2-x,y2-y)+abs((x2-x)*dy-(y2-y)*dx)*2,k))
        if opts:self.buttons[min(opts)[1]].grab_focus()
        return True
    def _click(self,b,key):
        if key=="seed" and self.moved:self.moved=False;return
        if key=="seed":return self.host.seed_panel(b)
        group=key.split(".")[0];item=self.items.get(key)
        if item:self.host.activate_item(item)
        else:self.host.show_page(group)
    def _tip(self,b,x,y,keyboard,tip,key):
        if key=="seed":s="Semente · abrir a confluência\nArrasta para mover o mapa."
        else:
            group=key.split(".")[0];item=self.items.get(key)
            if item:s=display_title(item.title)+"\n"+(item.detail or self.host.desktop.catalog.names.get(item.app,"Abrir"))
            else:s=NAMES[group]+"\n"+"\n".join(display_title(i.title) for i in self.host.data.get(group,[])[:3])
        tip.set_text(s.strip());return True
    def _press(self,b,e):
        if e.button==1:
            self.moved=False;self.drag=(e.x_root,e.y_root,self.dx,self.dy)
        return False
    def _motion(self,b,e):
        if not self.drag or not e.state & Gdk.ModifierType.BUTTON1_MASK:return False
        x,y,dx,dy=self.drag
        if math.hypot(e.x_root-x,e.y_root-y)>5:self.moved=True
        if self.moved:
            self.dx=max(-.18,min(.18,dx+(e.x_root-x)/max(1,self.get_allocated_width())))
            self.dy=max(-.20,min(.16,dy+(e.y_root-y)/max(1,self.get_allocated_height())))
            self.invalidate()
        return False
    def _release(self,b,e):
        if self.drag and self.moved:
            self.host.store.set("map-x",round(self.dx,4));self.host.store.set("map-y",round(self.dy,4))
        self.drag=None;return False
    def render(self):
        self.pending=0;w=self.get_allocated_width();h=self.get_allocated_height()
        if w<80 or h<80:return False
        surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,w,h);cr=cairo.Context(surface)
        pal=PALETTES[self.host.theme];bg,fg,muted,gold,line,plate=pal
        sx=w/1200;sy=h/500;s=max(.70,min(1.35,sx,sy))
        large=self.host.large; type_scale=1.17 if large else 1.
        paper(cr,w,h,pal,self.host.theme)
        # Vinheta procedural, com o título e o chamado de cada rio.
        hx=max(24,40*s);top=max(23,38*s)
        text_at(cr,hx,top,"MAPA DOS RIOS",9.3*s*type_scale,gold,True,spacing=2*s)
        fs=min(42*s, max(24,w*.038))*type_scale
        text_at(cr,hx,top+fs*1.29,"Navegação que",fs,fg,serif=True)
        prefix=text_at(cr,hx,top+fs*2.38,"nasce da ",fs,fg,serif=True)
        text_at(cr,hx+prefix,top+fs*2.38,"essência.",fs,gold,serif=True,italic=True)
        if w>=880 and h>=310 and not large:
            px=.374*w;py=top-8*s;pw=min(164*s,w*.145);ph=pw*.58
            cr.save();rounded(cr,px,py,pw,ph,8*s);cr.clip()
            draw_landscape(cr,px,py,pw,ph);cr.restore()
            rounded(cr,px,py,pw,ph,8*s);color(cr,line,.56);cr.set_line_width(.9);cr.stroke()
        offx=self.dx*w;offy=self.dy*h
        def point(x,y):return x*sx+offx,y*sy+offy
        paint(cr,art("rios.svg",1200,500),offx,offy,w,h)
        seedx,seedy=point(642,355)
        diameter=min(179*s,156*sy)* (1.07 if large else 1)
        for mul,alpha,width,dash in [(0.67,.52,.75,[2,5]),(.61,.55,.85,None),(.57,.68,.65,None)]:
            ring(cr,seedx,seedy,diameter*mul,line,width,alpha,dash)
        for k in range(12):
            ang=k*math.tau/12;rad=diameter*.612
            x=seedx+math.cos(ang)*rad;y=seedy+math.sin(ang)*rad
            if k%3==0:diamond(cr,x,y,2.7*s,gold,.8)
        self.draw_medal(cr,"semente",seedx,seedy,diameter)
        areas={};self.add_zone(areas,"seed",(seedx-diameter/2,seedy-diameter/2,diameter,diameter),"Semente. Abrir confluência ou arrastar")
        ty=seedy+diameter*.72
        if ty<h-10:
            text_at(cr,seedx,ty,"SEMENTE",12*s*type_scale,fg,True,spacing=2.4*s,align="center")
            if ty+18*s<h-3:text_at(cr,seedx,ty+18*s,"Confluência",11*s*type_scale,muted,align="center")
        for river in RIVERS:
            slots=NODES[river];vals=self.host.data.get(river,[])
            cap=3 if (w<850 or large or h<330) else 5
            if river=="open" and h<425:cap=min(3,cap)
            vals=vals[:cap]
            indices={0:[2],1:[2],2:[1,3],3:[0,2,4],4:[0,1,3,4],5:list(range(5))}[len(vals)]
            for j,idx in enumerate(indices):
                item=vals[j] if vals else None;x,y=point(*slots[idx])
                d=min(64*s,68*sx,(63 if cap==5 and river=="open" else 78)*sy)
                if large:d*=1.08
                self.draw_medal(cr,icon_kind(item,river,j),x,y,d)
                if item:
                    badge=d*.32;bx=x+d*.31;by=y+d*.31
                    color(cr,"#272c28");cr.arc(bx,by,badge*.64,0,math.tau);cr.fill()
                    ring(cr,bx,by,badge*.64,"#cbb68e",.85)
                    pic=self.node_icon(item,max(16,round(badge)))
                    if pic:paint(cr,pic,bx-badge/2,by-badge/2,badge,badge)
                if y+d/2>0 and x+d/2>0 and x-d/2<w and y-d/2<h:
                    self.add_zone(areas,river+"."+str(j),(x-d/2,y-d/2,d,d),item.title if item else "Explorar "+NAMES[river],item)
        for group,x,y in [("memory",218,277),("open",894,57),("frequent",977,175)]:
            cx,cy=point(x,y);bh=(37 if h<330 else 45)*s*type_scale;bw=(125 if group=="frequent" else 115)*s*type_scale
            cx=min(w-bw/2-5,max(bw/2+5,cx));cy=max(bh/2+3,min(h-bh/2-2,cy))
            rounded(cr,cx-bw/2,cy-bh/2,bw,bh,9*s);color(cr,plate,.96);cr.fill_preserve();color(cr,line,.8);cr.set_line_width(.8);cr.stroke()
            c={"memory":gold,"open":muted,"frequent":"#3f655a" if self.host.theme=="paper" else "#b8d9c7"}[group]
            text_at(cr,cx,cy-1*s,NAMES[group].upper(),10.6*s*type_scale,c,True,spacing=1*s,align="center")
            text_at(cr,cx,cy+13*s*type_scale,DESC[group],9.7*s*type_scale,muted,align="center")
            self.add_zone(areas,group,(cx-bw/2,cy-bh/2,bw,bh),"Expandir rio "+NAMES[group])
        self.image.set_from_pixbuf(to_pixbuf(surface));self.sync(areas)
        return False
    @staticmethod
    def draw_medal(cr,name,x,y,d):
        sh=cairo.RadialGradient(x,y+d*.10,d*.22,x,y+d*.10,d*.58)
        sh.add_color_stop_rgba(0,0,0,0,.32);sh.add_color_stop_rgba(.7,0,0,0,.16);sh.add_color_stop_rgba(1,0,0,0,0)
        cr.set_source(sh);cr.new_path();cr.arc(x,y+d*.10,d*.58,0,math.tau);cr.fill()
        paint(cr,art(name+".svg",256,256),x-d/2,y-d/2,d,d)

def GioIcon(name):
    from gi.repository import Gio
    return Gio.ThemedIcon.new(name)
