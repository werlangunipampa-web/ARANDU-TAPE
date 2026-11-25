"""Exercise actual GTK-independent method bodies with fake widgets."""
import ast
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from seed_presentation import SeedPresentation

def methods(path, cls, names, namespace):
    tree=ast.parse(path.read_text())
    owner=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls)
    code=ast.Module(body=[n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[])
    exec(compile(code,str(path),"exec"),namespace)
    return namespace

class SeedToggle(unittest.TestCase):
    def test_actual_toggle_roundtrip(self):
        names=("expand_seed","toggle_seed","retract","show_intro")
        funcs=methods(ROOT/"app.py","Desktop",names,{"clock_text":lambda:"12:00"})
        obj=SimpleNamespace(seed_state=SeedPresentation(),tools_revealer=Mock(),clock_button=Mock(),
                            visual=Mock(),seed_toggle=Mock(),session=Mock(),detail_revealer=Mock(),
                            clear_content=Mock(),content=Mock(),text=Mock())
        for name in names:
            setattr(obj,name,funcs[name].__get__(obj))
        obj.toggle_seed()
        self.assertTrue(obj.seed_state.expanded)
        obj.seed_toggle.set_label.assert_called_with("Recolher Semente")
        obj.tools_revealer.set_reveal_child.assert_called_with(True)
        obj.visual.show_rivers.assert_called()
        obj.toggle_seed()
        self.assertFalse(obj.seed_state.expanded)
        obj.seed_toggle.set_label.assert_called_with("Expandir Semente")
        obj.tools_revealer.set_reveal_child.assert_called_with(False)
        obj.visual.show_compact.assert_called()
        obj.detail_revealer.set_reveal_child.assert_called_with(False)
        obj.session.retract.assert_called_once()

    def test_compact_retains_overlay_allocation(self):
        funcs=methods(ROOT/"visual.py","RiversCanvas",("show_compact",),{})
        marker,label=Mock(),Mock()
        obj=SimpleNamespace(background=Mock(),seed=Mock(),markers=[(marker,"memory",0,0)],
                            river_buttons={"memory":label},marker_apps={},marker_windows={},
                            scale=.75,_layout=Mock())
        funcs["show_compact"](obj)
        obj.background.set_opacity.assert_called_once_with(0.0)
        obj.background.set_visible.assert_not_called()
        obj.seed.set_visible.assert_called_once_with(True)
        marker.set_visible.assert_called_once_with(False)
        label.set_visible.assert_called_once_with(False)

if __name__=="__main__":
    unittest.main()
