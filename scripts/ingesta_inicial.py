#!/usr/bin/env python3
"""Descarga documental provisional. Nunca certifica cobertura curricular."""
import csv
import hashlib
import json
import pathlib
import urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"resultados_ingesta"
OUT.mkdir(exist_ok=True)
fuentes=json.loads((ROOT/"datos/fuentes_iniciales.json").read_text(encoding="utf-8"))
registro=[]
for fuente in fuentes:
    item={"id":fuente["id"],"norma":fuente["norma"],"url":fuente["url"],"estado":"ERROR","verificado":False}
    try:
        req=urllib.request.Request(fuente["url"],headers={"User-Agent":"OPO-IA-Docentes/0.1","Accept":"application/pdf,text/html"})
        with urllib.request.urlopen(req,timeout=35) as res:
            final=res.geturl()
            if not final.startswith("https://"):
                raise ValueError("Redirección no HTTPS")
            data=res.read(80*1024*1024+1)
            if len(data)>80*1024*1024:
                raise ValueError("Documento demasiado grande")
        kind="pdf" if data.startswith(b"%PDF-") else "html" if b"<html" in data[:15000].lower() else None
        if not kind:
            raise ValueError("El contenido no parece PDF ni HTML")
        nombre=f'{fuente["id"]}.{kind}'
        (OUT/nombre).write_bytes(data)
        item.update(estado="DESCARGADO_SIN_VERIFICAR",archivo=nombre,sha256=hashlib.sha256(data).hexdigest(),tamano_bytes=len(data),url_final=final)
    except Exception as exc:
        item["error"]=str(exc)[:350]
    registro.append(item)
    print(f'{item["id"]}: {item["estado"]}',flush=True)
(OUT/"manifest.json").write_text(json.dumps({"fecha_utc":datetime.now(timezone.utc).isoformat(),"fuentes":registro,"curriculos_verificados":0},ensure_ascii=False,indent=2),encoding="utf-8")
with (OUT/"manifest.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["id","norma","url","estado","verificado","archivo","sha256","tamano_bytes","url_final","error"],extrasaction="ignore")
    w.writeheader()
    w.writerows(registro)
print(f"Descargados: {sum(x['estado']=='DESCARGADO_SIN_VERIFICAR' for x in registro)}/{len(registro)}. Verificados: 0.")
