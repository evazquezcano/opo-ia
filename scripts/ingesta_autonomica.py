#!/usr/bin/env python3
"""Ingesta PROVISIONAL: evidencia de descarga, nunca verificación curricular."""
import argparse
import hashlib
import json
import pathlib
import re
import urllib.request
from datetime import datetime, timezone
from html import unescape
from urllib.parse import urlparse

ROOT=pathlib.Path(__file__).resolve().parents[1]
MAX_BYTES=45*1024*1024
HEADERS={"User-Agent":"Mozilla/5.0 (compatible; OPO-IA-research-catalog/0.2)","Accept":"application/pdf,text/html,application/xhtml+xml"}
def load_sources():
    catalog=json.loads((ROOT/"datos/catalogo_51_autonomicos.json").read_text(encoding="utf-8"))
    originals=json.loads((ROOT/"datos/fuentes_iniciales.json").read_text(encoding="utf-8"))
    unique={}
    for r in catalog["registros"]:
        k=r["url"].strip()
        unique.setdefault(k,{"url":k,"ids":[],"normas":[],"tipo":r["tipo_fuente"]})
        unique[k]["ids"].append(r["id"]); unique[k]["normas"].append(r["norma_de_referencia"])
    for r in originals:
        k=r["url"].strip()
        unique.setdefault(k,{"url":k,"ids":[],"normas":[],"tipo":"fuente_previa"})
        unique[k]["ids"].append(r["id"]);unique[k]["normas"].append(r["norma"])
    return list(unique.values()),len(catalog["registros"])
def download(r, dest):
    record={"ids":r["ids"],"normas":r["normas"],"url":r["url"],"estado":"ERROR_DESCARGA","validacion_juridica":"PENDIENTE","validacion_contenido":"PENDIENTE","habilitado_para_generar":False}
    try:
        u=urlparse(r["url"])
        if u.scheme!="https" or not u.hostname:raise ValueError("URL no HTTPS")
        with urllib.request.urlopen(urllib.request.Request(r["url"],headers=HEADERS),timeout=14) as response:
            final=response.geturl()
            if not final.startswith("https://"):raise ValueError("Redirección fuera de HTTPS")
            data=response.read(MAX_BYTES+1)
            if len(data)>MAX_BYTES:raise ValueError("Excede tamaño admitido")
            ctype=response.headers.get("Content-Type","")
        pdf=data.startswith(b"%PDF-")
        head=data[:25000].lower()
        html=(b"<html" in head or b"<!doctype html" in head)
        if not pdf and not html:raise ValueError("Respuesta distinta de PDF/HTML: "+ctype)
        extension="pdf" if pdf else "html"
        sha=hashlib.sha256(data).hexdigest()
        path=dest/(sha[:20]+"."+extension)
        path.write_bytes(data)
        record.update(estado="DESCARGADO_SIN_VALIDAR",archivo=path.name,sha256=sha,bytes=len(data),tipo_real=extension,url_final=final)
        if html:
            content=re.sub(r"<[^>]+>"," ",data.decode("utf-8",errors="replace"))
            content=unescape(content)
            normalized=" ".join(content.split()).lower()
            record["aviso"]="Puede ser portal o índice; no se asume que contiene texto íntegro"
            record["coincidencia_referencias"]=list(dict.fromkeys(x for x in r["normas"] if x.lower() in normalized))
        elif pdf:
            record["aviso"]="PDF descargado; integridad de anexos y vigencia no comprobadas"
    except Exception as err:
        record["error"]=str(err)[:400]
    return record
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--max-documentos",type=int,default=25,help="Máximo de direcciones distintas por ejecución; 0 significa todas")
    p.add_argument("--inicio",type=int,default=0,help="Índice inicial para lotes")
    args=p.parse_args()
    all_sources,entries=load_sources()
    selected=all_sources[args.inicio:] if args.max_documentos==0 else all_sources[args.inicio:args.inicio+args.max_documentos]
    output=ROOT/"resultados_ingesta"/("lote_"+str(args.inicio))
    output.mkdir(parents=True,exist_ok=True)
    results=[]
    for s in selected:
        r=download(s,output)
        results.append(r)
        print(",".join(s["ids"])+": "+r["estado"],flush=True)
    manifest={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"entradas_autonomicas":entries,"fuentes_distintas_en_catalogo":len(all_sources),"lote_inicio":args.inicio,"fuentes_comprobadas":len(results),"descargadas":sum(r["estado"]=="DESCARGADO_SIN_VALIDAR" for r in results),"curriculos_verificados":0,"documentos":results}
    (output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print("RESUMEN: "+json.dumps({k:manifest[k] for k in ["entradas_autonomicas","fuentes_distintas_en_catalogo","fuentes_comprobadas","descargadas","curriculos_verificados"]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
