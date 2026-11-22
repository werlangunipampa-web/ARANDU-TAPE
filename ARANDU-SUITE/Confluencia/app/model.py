"""Histórico, preferências e comandos do Arandu Tape. Todos os dados são locais."""
from dataclasses import dataclass
from pathlib import Path
import os
import sqlite3
import time
import unicodedata

APP_ID = "org.arandulab.Tape"
RIVERS = ("memory", "open", "frequent")
NAMES = {"memory": "Memória", "open": "Abertos", "frequent": "Frequentes"}
SUBS = {"memory": "Por onde tu passaste", "open": "O que está ativo agora", "frequent": "O que tu mais usas"}
THEMES = {"paper": "Papel", "focus": "Luz suave", "contrast": "Alto contraste"}

def plain(value):
    return "".join(c for c in unicodedata.normalize("NFD", str(value).casefold())
                   if not unicodedata.combining(c)).strip()

@dataclass(frozen=True)
class Item:
    key: str
    title: str
    app: str = ""
    uri: str = ""
    win: str = ""
    detail: str = ""
    stamp: float = 0
    count: int = 0

def display_title(title):
    if title.startswith(("/", "~/")):
        return title.rstrip("/").rsplit("/", 1)[-1] or title
    return title

def window_key(app, title):
    return "win:" + app + "\n" + title

def unique(items, key=lambda x: x.key):
    seen = set()
    for item in items:
        ident = key(item)
        if ident not in seen:
            seen.add(ident)
            yield item

class Store:
    def __init__(self, directory=None):
        folder = Path(directory or os.environ.get("XDG_STATE_HOME") or Path.home()/".local/state") / "arandu-tape-confluencia"
        folder.mkdir(parents=True, mode=0o700, exist_ok=True)
        path = folder / "mapa.sqlite3"
        self.db = sqlite3.connect(str(path), timeout=4)
        os.chmod(path, 0o600)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS pref(k TEXT PRIMARY KEY, val TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS recent(k TEXT PRIMARY KEY, title TEXT, app TEXT, uri TEXT, ts REAL);
            CREATE TABLE IF NOT EXISTS freq(app TEXT PRIMARY KEY, total INTEGER, ts REAL);
        """)
    def get(self, k, default=""):
        row = self.db.execute("SELECT val FROM pref WHERE k=?", (k,)).fetchone()
        return row[0] if row else default

    def set(self, k, val):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO pref VALUES(?,?)", (k, str(val)))

    def remember(self, item, count=True, when=None):
        ts = time.time() if when is None else when
        with self.db:
            if item.win and item.app:
                self.db.execute("DELETE FROM recent WHERE k=? AND ts>=?", ("app:"+item.app, ts-12))
            self.db.execute("INSERT OR REPLACE INTO recent VALUES(?,?,?,?,?)",
                            (item.key, item.title, item.app, item.uri, ts))
            if item.app and count:
                self.db.execute("""INSERT INTO freq VALUES(?,1,?) ON CONFLICT(app)
                                   DO UPDATE SET total=total+1,ts=excluded.ts""", (item.app, ts))
            self.db.execute("DELETE FROM recent WHERE k IN (SELECT k FROM recent ORDER BY ts DESC LIMIT -1 OFFSET 160)")
            self.db.execute("DELETE FROM freq WHERE app IN (SELECT app FROM freq ORDER BY total DESC,ts DESC LIMIT -1 OFFSET 240)")

    def memory(self):
        return [Item(k,t,a,u,stamp=s) for k,t,a,u,s in self.db.execute("SELECT * FROM recent ORDER BY ts DESC")]

    def frequency(self):
        return {a:(n,t) for a,n,t in self.db.execute("SELECT * FROM freq")}

    def import_legacy(self, ids, counts, catalog):
        if self.get("legacy-imported"): return
        with self.db:
            now = time.time()-60
            for i, ident in enumerate(ids[:50]):
                if ident in catalog:
                    self.db.execute("INSERT OR IGNORE INTO recent VALUES(?,?,?,?,?)",
                                    ("app:"+ident,catalog[ident],ident,"",now-i))
            for ident, count in counts.items():
                if ident in catalog and type(count) is int and 0 < count < 10**9:
                    self.db.execute("INSERT OR IGNORE INTO freq VALUES(?,?,?)",(ident,count,0))
            self.db.execute("INSERT OR REPLACE INTO pref VALUES('legacy-imported','1')")

    def clear(self):
        with self.db:
            self.db.execute("DELETE FROM recent")
            self.db.execute("DELETE FROM freq")
            self.db.execute("INSERT OR REPLACE INTO pref VALUES('clear-time',?)",(str(time.time()),))
            self.db.execute("INSERT OR REPLACE INTO pref VALUES('legacy-imported','1')")

def memory_items(own, bridge, documents, opened, limit=50):
    live = {i.key:i for i in opened}
    ordered = sorted([*own,*bridge,*documents], key=lambda i:i.stamp, reverse=True)
    result=[]; seen=set()
    for i in ordered:
        if i.key in seen: continue
        seen.add(i.key)
        if i.key.startswith("app:") and any(j.app == i.app and abs(j.stamp-i.stamp)<12 for j in result):
            continue
        if i.win or i.key in live:
            now=live.get(i.key)
            i=Item(i.key,i.title,i.app,i.uri,now.win if now else "",i.detail,i.stamp,i.count)
        result.append(i)
        if len(result)>=limit:break
    return result

def frequency_items(local, bridge, catalog):
    out=[]
    for app in set(local)|set(bridge):
        if app not in catalog: continue
        n1,t1=local.get(app,(0,0)); n2,t2=bridge.get(app,(0,0))
        out.append(Item("app:"+app,catalog[app],app,detail="Aplicativo",count=n1+n2,stamp=max(t1,t2)))
    return sorted(out,key=lambda i:(-i.count,-i.stamp,plain(i.title)))

def command(text):
    value=" ".join(plain(text).strip(" ?!.").split())
    fixed={
        "abrir memoria":"memory","memoria":"memory", "ultimas janelas":"memory",
        "o que esta aberto":"open","abertos":"open","abrir abertos":"open",
        "meus frequentes":"frequent","frequentes":"frequent","abrir frequentes":"frequent",
        "semente":"seed","abrir semente":"seed","aproximar":"expand",
        "modo foco":"focus","luz suave":"focus","alto contraste":"contrast",
        "modo claro":"paper","papel":"paper","centralizar":"center",
        "abrir aplicativos":"apps","aplicativos":"apps","comandos":"commands",
    }
    if value in fixed: return fixed[value],""
    for prefix in ("ir para o ","ir para a ","ir para ","abrir "):
        if value.startswith(prefix): return "find",value[len(prefix):].strip()
    return "find",value
