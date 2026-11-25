#!/usr/bin/env python3
"""Exercise GTK4 widgets on a disposable virtual display, not a user desktop."""
import os
from pathlib import Path
import sys
import time

if os.environ.get("ARANDU_VIRTUAL_GTK_TEST") != "1":
    raise SystemExit("Execute only in the dedicated virtual-display test environment.")
os.environ.pop("ARANDU_SESSION_LAB",None)
os.environ.pop("SWAYSOCK",None)
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import Desktop, Gtk, GLib

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def settle(seconds=.35):
    context=GLib.MainContext.default()
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        # Bound dispatch in case an event source remains continuously ready.
        for _ in range(100):
            if not context.pending():
                break
            context.iteration(False)
        time.sleep(.01)

def verify(app, expanded):
    canvas=app.visual
    require(app.seed_state.expanded==expanded,"state mismatch")
    require(canvas.mode==("rivers" if expanded else "compact"),"canvas mode mismatch")
    require(app.tools_revealer.get_reveal_child()==expanded,"tools mismatch")
    require(app.seed_toggle.get_label()==("Recolher Semente" if expanded else "Expandir Semente"),"toggle label mismatch")
    require(canvas.seed.get_mapped(),"seed not mapped")
    require(canvas.seed.get_width()>0 and canvas.seed.get_height()>0,"seed has no allocation")
    require(canvas.background.get_visible(),"main overlay child hidden")
    require(canvas.background.get_opacity()==float(expanded),"background paint mismatch")
    require(all(b.get_visible()==expanded for b in canvas.river_buttons.values()),"river labels mismatch")
    require(all(b.get_visible()==expanded for b,*_ in canvas.markers),"marker visibility mismatch")
    # GTK picking uses the actual allocation and stacking order.
    picked=canvas.seed.pick(canvas.seed.get_width()/2,canvas.seed.get_height()/2,Gtk.PickFlags.DEFAULT)
    require(picked is not None,"seed center is not targetable")
    return (canvas.seed.get_width(),canvas.seed.get_height())

def main():
    app=Desktop()
    require(app.register(None),"cannot register GTK application")
    require(not app.get_is_remote(),"unexpected existing application")
    app.activate()
    try:
        settle(.8)
        before=verify(app,False)
        app.visual.seed.emit("clicked")
        settle()
        expanded=verify(app,True)
        app.visual.seed.emit("clicked")
        settle()
        verify(app,False)
        app.seed_toggle.emit("clicked")
        settle()
        verify(app,True)
        app.seed_toggle.emit("clicked")
        settle()
        after=verify(app,False)
        require(all(v>0 for v in before+expanded+after),"invalid allocation")
        print("GTK4 virtual display: seed and alternative button round trips passed")
        return 0
    finally:
        if app.window:
            app.window.destroy()
        app.quit()

if __name__=="__main__":
    raise SystemExit(main())
