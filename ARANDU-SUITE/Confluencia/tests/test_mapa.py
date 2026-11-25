import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"app"))
sys.path.insert(0,str(BASE))
from model import Item, Store, command, frequency_items, memory_items, window_key
from shell.build import build
import instalador

class Historico(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store=Store(self.tmp.name)
        self.addCleanup(self.store.db.close)
    def test_janela_confirmada_substitui_abertura_recente(self):
        app="folhas.desktop"
        self.store.remember(Item("app:"+app,"Folhas",app),when=100)
        self.store.remember(Item(window_key(app,"Notas"),"Notas",app,win="43"),count=False,when=103)
        self.assertEqual([i.title for i in self.store.memory()],["Notas"])
        self.assertEqual(self.store.frequency()[app][0],1)
    def test_origem_antiga_so_uma_vez(self):
        names={"a.desktop":"Editor","b.desktop":"Mapas"}
        self.store.import_legacy(["b.desktop","a.desktop","sumiu.desktop"],{"a.desktop":9},names)
        self.store.import_legacy(["a.desktop"],{"a.desktop":90},names)
        self.assertEqual([i.app for i in self.store.memory()],["b.desktop","a.desktop"])
        self.assertEqual(self.store.frequency()["a.desktop"][0],9)
    def test_historico_e_preferencias_persistem(self):
        self.store.set("theme","contrast")
        self.store.remember(Item("arquivo","Campo",uri="file:///teste"),when=722)
        other=Store(self.tmp.name)
        try:self.assertEqual((other.get("theme"),other.memory()[0].stamp),("contrast",722))
        finally:other.db.close()
    def test_limpar_preserva_tema_e_rejeita_reimportacao(self):
        self.store.set("theme","focus")
        self.store.remember(Item("app:a","A","a"));self.store.clear()
        self.store.import_legacy(["a"],{"a":2},{"a":"A"})
        self.assertEqual(self.store.memory(),[]);self.assertEqual(self.store.frequency(),{})
        self.assertGreater(float(self.store.get("clear-time")),0)
        self.assertEqual(self.store.get("theme"),"focus")
    def test_memoria_resolve_janela_atual_e_unifica_documentos(self):
        old=Item("w","Nota","a",stamp=3)
        live=Item("w","Nota","a",win="12")
        doc=Item("uri:f","F",uri="file:///f",stamp=9)
        rows=memory_items([old,doc],[old],[doc],[live])
        self.assertEqual([(i.key,i.win) for i in rows],[("uri:f",""),("w","12")])
        self.assertEqual(memory_items([],[old],[],[])[0].win,"")
    def test_frequentes_somam_origens_e_ignoram_apps_removidos(self):
        top=frequency_items({"a":(2,3),"b":(2,2)},{"b":(2,4),"c":(1,3),"xx":(999,9)},
                            {"a":"Arco","b":"Brisa","c":"Campo"})
        self.assertEqual([(i.app,i.count) for i in top],[("b",4),("a",2),("c",1)])
    def test_comandos_com_e_sem_acentos(self):
        for phrase,key in [("O QUE ESTÁ ABERTO?","open"),("abrir memória","memory"),("meus frequentes","frequent"),("modo foco","focus")]:
            self.assertEqual(command(phrase),(key,""))
        self.assertEqual(command("Ir para o Relatório"),("find","relatorio"))
        self.assertEqual(command("abrir terminal"),("find","terminal"))

class Pacote(unittest.TestCase):
    def test_shell_recalcula_mapa_por_monitor(self):
        code=(BASE/'shell/implementation.js.in').read_text()
        self.assertIn('this.root.set_size(w,h)',code)
        self.assertIn('this.fabric.set_size(w,h)',code)
        self.assertIn('riverPoint(r, t)',code)
        self.assertIn('this.layoutRivers()',code)
        self.assertIn('this.repaintRivers(w,h)',code)
        self.assertIn('this.transformPoint(this.transforms[r],p)',code)
        self.assertIn('this.makeTransform',code)

    def test_recolhimento_por_tempo_desligado_por_padrao(self):
        import xml.etree.ElementTree as ET
        schema=ET.parse(BASE/'shell/org.gnome.shell.extensions.arandu-confluencia.gschema.xml')
        key=schema.find(".//key[@name='navigation-idle-ms']")
        self.assertIsNotNone(key)
        self.assertEqual(key.findtext('default'),'0')
        self.assertEqual(key.find('range').attrib,{'min':'0','max':'60000'})

    def test_variantes_de_shell_e_schema(self):
        import xml.etree.ElementTree as ET
        with tempfile.TemporaryDirectory() as tmp:
            for v in [40,44,45,46,51]:
                dst=Path(tmp)/str(v);build(v,dst)
                meta=json.loads((dst/"metadata.json").read_text());code=(dst/"extension.js").read_text()
                self.assertIn(str(v),meta["shell-version"]);self.assertEqual("__LAYOUT__" in code,False)
                self.assertEqual("export default class" in code,v>=45)
                self.assertEqual(ET.parse(next((dst/"schemas").glob("*.xml"))).find("schema").attrib["id"],meta["settings-schema"])
    def test_versao_desconhecida(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):build(52,tmp)
    def test_transacao_restaura_se_falhar_durante_troca(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);root=p/"dest";root.mkdir();stage=p/"stage";stage.mkdir()
            targets={k:root/k for k in ("programa","atalho")};manifest=root/"manifest"
            old={"id":instalador.UUID,"keys":list(targets)}
            manifest.write_text(json.dumps(old))
            for k in targets:targets[k].write_text("anterior");(stage/k).write_text("novo")
            real=instalador.os.replace;failed=False
            def interrupt(a,b):
                nonlocal failed
                if not failed and Path(b)==targets["atalho"] and Path(a).name=="novo":
                    failed=True;raise OSError("falha de teste")
                return real(a,b)
            with patch.object(instalador,"TARGET",targets),patch.object(instalador,"MANIFEST",manifest),patch.object(instalador.os,"replace",interrupt):
                with self.assertRaises(OSError):instalador.transact(stage,list(targets),old,old,False)
            self.assertTrue(failed);self.assertTrue(all(t.read_text()=="anterior" for t in targets.values()))
            self.assertEqual(json.loads(manifest.read_text()),old)
if __name__=="__main__":unittest.main()

class GeometriaConfluencia(unittest.TestCase):
    def test_tres_rios_usam_o_mesmo_inicio_e_tres_bordas(self):
        data=json.loads((BASE/'shell/rios-dinamicos.json').read_text())
        self.assertEqual(len(data['groups']),3)
        starts=[row[0] for row in data['paths']]
        self.assertTrue(all(p==[642.0,355.0] for p in starts))
        seed=(1000.0,650.0)
        edges=[(-34.0,650.0),(1130.0,-34.0),(1960.0,305.0)]
        for path,edge in zip(data['paths'],edges):
            x,y=path[0];u,v=path[-1];dx,dy=u-x,v-y
            vx,vy=edge[0]-seed[0],edge[1]-seed[1]
            den=dx*dx+dy*dy
            a=(vx*dx+vy*dy)/den;b=(vy*dx-vx*dy)/den
            e=seed[0]-a*x+b*y;f=seed[1]-b*x-a*y
            p=lambda x,y:(a*x-b*y+e,b*x+a*y+f)
            for actual,wanted in [(p(x,y),seed),(p(u,v),edge)]:
                self.assertAlmostEqual(actual[0],wanted[0],places=6)
                self.assertAlmostEqual(actual[1],wanted[1],places=6)
