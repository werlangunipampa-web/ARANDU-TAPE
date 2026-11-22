import importlib.util
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('arandu_assistivo', HERE/'arandu-assistivo.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class TestRouter(unittest.TestCase):
    def test_voice_aliases(self):
        self.assertEqual(mod.normalize('  MEMÓRIA  '),'river:memory')
        self.assertEqual(mod.normalize('próximo'),'node:next')
        self.assertEqual(mod.normalize('ABRIR'),'node:activate')
    def test_unknown_rejected(self):
        self.assertIsNone(mod.normalize('rm -rf /'))
        self.assertIsNone(mod.normalize('abrir terminal; apagar arquivos'))
    def test_dry_run(self):
        self.assertTrue(mod.send('river:open',dry_run=True))

if __name__=='__main__':unittest.main()
