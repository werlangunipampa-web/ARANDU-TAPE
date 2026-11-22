"""Reconhece uma frase curta em português em um processo local, aberto a pedido."""
import importlib.util
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import sys
import time

def runtime():
    v=Path(os.environ.get("XDG_DATA_HOME") or Path.home()/".local/share")/"arandu-tape-confluencia"/"voz-venv/bin/python"
    return str(v) if v.is_file() else sys.executable

def recorder():
    for executable,args in [
        ("parec",["--raw","--rate=16000","--format=s16le","--channels=1"]),
        ("arecord",["-q","-t","raw","-f","S16_LE","-c","1","-r","16000"]),
    ]:
        path=shutil.which(executable)
        if path:return [path,*args]
    return []

def recognize(model):
    if not Path(model).is_dir() or not (Path(model)/"am").is_dir():
        raise RuntimeError("Escolhe a pasta extraída do modelo Vosk em Aparência e acessibilidade.")
    if importlib.util.find_spec("vosk") is None: raise RuntimeError("Instala o Vosk conforme a seção Voz do guia.")
    rec=recorder()
    if not rec:raise RuntimeError("Instala um capturador de áudio: parec ou arecord.")
    import vosk
    vosk.SetLogLevel(-1)
    recognizer=vosk.KaldiRecognizer(vosk.Model(str(model)),16000)
    proc=subprocess.Popen(rec,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(proc.stdout,selectors.EVENT_READ);end=time.monotonic()+8.0
            while time.monotonic()<end:
                if not selector.select(.35):continue
                buf=os.read(proc.stdout.fileno(),4000)
                if not buf:raise RuntimeError("O microfone não entregou áudio. Confere a entrada de som.")
                if recognizer.AcceptWaveform(buf):
                    result=json.loads(recognizer.Result()).get("text","").strip()
                    if result:return result
        return json.loads(recognizer.FinalResult()).get("text","").strip()
    finally:
        proc.terminate()
        try:proc.wait(timeout=1)
        except subprocess.TimeoutExpired:proc.kill();proc.wait()
        proc.stdout.close()

if __name__=="__main__":
    try:print(json.dumps({"text":recognize(sys.argv[1])},ensure_ascii=False))
    except Exception as exc:print(json.dumps({"error":str(exc)},ensure_ascii=False));sys.exit(1)
