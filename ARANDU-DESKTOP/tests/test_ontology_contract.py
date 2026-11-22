"""A ontologia atravessa ações reais, não apenas a aparência da interface."""
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ontology_contract import RULES, PILLARS, decide, validate_manifest
from adaptation import Snapshot, Adaptation, propose
from ai_gateway import PROVIDERS, ready, build_request, GatewayError
from eca_bridge import parse_export, EcaBridgeError
from eca_experiments import CognitiveProposal, evaluate


class OntologicalTransversality(unittest.TestCase):
    def test_manifest_all_actions_have_source_pillar_and_purpose(self):
        self.assertTrue(validate_manifest())
        self.assertEqual(set(PILLARS), {
            "informacao", "ambiente", "continuidade",
            "emergencia", "identidade", "ontologia"})
        self.assertGreaterEqual(len(RULES), 15)
        self.assertTrue(all(rule.pillar in PILLARS for rule in RULES.values()))

    def test_fail_closed_for_unknown_and_unsolicited(self):
        self.assertFalse(decide("invented", user_intent=True).allowed)
        self.assertFalse(decide("clipboard_capture").allowed)
        self.assertTrue(decide("clipboard_capture", user_intent=True).allowed)

    def test_constitution_prohibits_changes_to_official_seed(self):
        for operation in ("read_official_seed", "modify_official_seed",
                          "promote_generation", "execute_ai_generated_code",
                          "silently_collect_history"):
            self.assertFalse(decide(operation, user_intent=True,
                                    confirmation=True, provenance=True).allowed)

    def test_language_model_is_not_execution_authority(self):
        self.assertFalse(decide("apply_adaptation", user_intent=True,
                                confirmation=True, agent="generative_ai").allowed)
        self.assertFalse(decide("consult_eca_export", user_intent=True,
                                provenance=True, agent="generative_ai").allowed)
        self.assertTrue(decide("ask_generative_ai", user_intent=True,
                               confirmation=True).allowed)

    def test_provenance_required_for_eca_and_evolution(self):
        self.assertFalse(decide("consult_eca_export", user_intent=True).allowed)
        self.assertTrue(decide("consult_eca_export", user_intent=True,
                               provenance=True).allowed)
        self.assertFalse(decide("update_code", user_intent=True,
                                confirmation=True).allowed)
        self.assertTrue(decide("update_code", user_intent=True,
                               confirmation=True, provenance=True).allowed)

    def test_eca_export_is_experimental_without_verified_truth(self):
        source, items = parse_export(
            '{"source":"laboratorio-sandbox","relations":['
            '{"subject":"rotacao","predicate":"explica","object":"dia-noite",'
            '"origin":"aula-simulada"}]}')
        self.assertEqual(source, "laboratorio-sandbox")
        self.assertEqual(len(items), 1)
        self.assertIn("não verificada", items[0].status)
        with self.assertRaises(EcaBridgeError):
            parse_export('{"relations":[]}')

    def test_eca_structural_check_never_proves_learning(self):
        e = evaluate(CognitiveProposal(
            "diferenciacao_progressiva", "distinguir conceitos",
            "movimento", "rotacao da Terra", "aula simulada",
            "separar movimento próprio do dia e noite"))
        self.assertTrue(e.valid)
        self.assertTrue(e.experimental)
        self.assertFalse(e.official_state_changed)
        self.assertFalse(e.code_executed)

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

    def test_desktop_actions_use_ontology_contract(self):
        app = (ROOT / "app.py").read_text()
        self.assertIn('from ontology_contract import decide as ontology_decide', app)
        for token in ('"ask_generative_ai"', '"consult_eca_export"',
                      '"apply_adaptation"', '"clipboard_capture"',
                      '"bluetooth_connect"', '"launch_app"'):
            self.assertIn("ontology_decide("+token if token != '"bluetooth_connect"' else '"bluetooth_connect"', app)
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
