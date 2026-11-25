"""Public action authorization and independent desktop behavior."""
import ast
import pathlib
import sys
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from action_contract import RULES, decide
from adaptation import Snapshot, Adaptation, propose
from ai_gateway import PROVIDERS, ready, build_request, GatewayError

class PublicActionContract(unittest.TestCase):
    def test_all_operations_require_human_intent(self):
        for action,rule in RULES.items():
            with self.subTest(action=action):
                self.assertFalse(decide(action).allowed)
                self.assertFalse(decide(action,user_intent=True,confirmation=True,provenance=True,agent="generative_ai").allowed)
                self.assertFalse(decide(action,user_intent=1,confirmation=True,provenance=True).allowed)
                self.assertTrue(decide(action,user_intent=True,confirmation=True,provenance=True).allowed)
                if rule.confirmation:
                    self.assertFalse(decide(action,user_intent=True,provenance=True).allowed)
                if rule.provenance:
                    self.assertFalse(decide(action,user_intent=True,confirmation=True).allowed)

    def test_unknown_and_invalid_actions_are_denied(self):
        for action in ("invented","execute_ai_generated_code","consult_eca_export","modify_official_seed",None,[]):
            self.assertFalse(decide(action,user_intent=True,confirmation=True,provenance=True).allowed)

    def test_no_research_import_or_export_reader(self):
        tree=ast.parse((ROOT/"app.py").read_text())
        imports={n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}
        imports.update(a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names)
        self.assertNotIn("ontology_contract",imports)
        self.assertNotIn("eca_bridge",imports)
        self.assertNotIn("eca_experiments",imports)
        self.assertNotIn("show_eca",{n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)})
        self.assertNotIn("preview_eca",{n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)})

    def test_adaptation_suggests_only_and_requires_confirmation(self):
        snapshot = Snapshot(15, False, 9)
        proposal = propose(snapshot)
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal.mode, "economico")
        engine = Adaptation()
        self.assertFalse(engine.apply(proposal))
        self.assertEqual(engine.mode, "equilibrado")
        self.assertTrue(engine.apply(proposal, confirmed=True))
        self.assertEqual(engine.mode, "economico")
        self.assertTrue(engine.undo())
        self.assertEqual(engine.mode, "equilibrado")

    def test_tupa_default_chatgpt_is_browser_not_implicit_api(self):
        self.assertIn("chatgpt", PROVIDERS)
        valid, message = ready("chatgpt", "")
        self.assertFalse(valid)
        self.assertIn("navegador", message)
        with self.assertRaises(GatewayError):
            build_request("chatgpt", "", "olá")

    def test_desktop_actions_use_public_contract(self):
        app = (ROOT / "app.py").read_text()
        self.assertIn('from action_contract import decide as action_decide', app)
        for token in ('"ask_generative_ai"', '"apply_adaptation"', '"clipboard_capture"',
                      '"bluetooth_connect"', '"launch_app"'):
            self.assertIn("action_decide("+token if token != '"bluetooth_connect"' else '"bluetooth_connect"', app)
        self.assertIn("def show_tupa(self):", app)
        self.assertIn("def show_adaptation(self):", app)
        self.assertIn("def show_bluetooth(self):", app)
        self.assertIn("Gio.AppInfo.launch_default_for_uri(\"https://chatgpt.com/\"", app)
        self.assertIn("self.visual.set_energy_mode(economical)", app)

    def test_original_seed_states_remain(self):
        from seed_presentation import SeedPresentation
        state = SeedPresentation()
        self.assertEqual(state.state, "Collapsed")
        self.assertEqual(state.expand(), "Expanded")
        self.assertEqual(state.toggle_pin(), "Pinned")
        self.assertEqual(state.collapse(), "Pinned")
        self.assertEqual(state.collapse(force=True), "Collapsed")


if __name__ == "__main__":
    unittest.main()
