#!/usr/bin/env python3
"""Reintento exclusivamente de fuentes que fallaron en los dos primeros lotes.

Una descarga o la identificación del número de decreto NO acredita vigencia,
integridad de anexos, aplicabilidad por materia ni validación curricular.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from pathlib import Path
from io import BytesIO
import hashlib
import json
import re
import unicodedata

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultados_reintento"
OUT.mkdir(exist_ok=True)
IDS = {
    "AS-primaria", "AS-eso", "AS-bachillerato",
    "CV-eso",
    "RI-primaria", "RI-eso", "RI-bachillerato"
}

MAX_BYTES = 40 * 1024 * 1024
OFFICIAL_DOMAINS = {
    "www.educastur.es", "miprincipado.asturias.es",
    "www.educantabria.es", "boc.cantabria.es",
    "www.lexnavarra.navarra.es", "web.larioja.org",
    "dogv.gva.es", "www.dogv.gva.es",
}

class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.ignore = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg", "noscript"):
            self.ignore += 1
    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "noscript"):
            self.ignore = max(0, self.ignore - 1)
    def handle_data(self, data):
        if not self.ignore:
            self.parts.append(data)

def norm(s):
    s = unicodedata.normalize("NFKD", s).lower()
    s = "".join(x for x in s if not unicodedata.combining(x))
    return " ".join(s.split())

def fetch(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("La URL no utiliza HTTPS")
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; OPO-IA educational curriculum project)",
        "Accept": "application/pdf,text/html,application/xhtml+xml"})
    with urlopen(req, timeout=22) as resp:
        final = resp.geturl()
        if urlparse(final).scheme != "https":
            raise ValueError("Redirección no HTTPS")
        data = resp.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Documento superior a 40 MB")
        content_type = resp.headers.get("content-type", "")
    kind = "PDF" if data.startswith(b"%PDF-") else (
        "HTML" if (b"<html" in data[:30000].lower() or b"<!doctype html" in data[:30000].lower()) else "OTRO")
    if kind == "OTRO":
        raise ValueError("No es PDF/HTML; content-type: " + content_type)
    return data, final, kind

def extract(data, kind):
    if kind == "HTML":
        parser = TextOnly()
        parser.feed(data.decode("utf-8", errors="replace"))
        return " ".join(parser.parts)[:2500000], None, None
    reader = PdfReader(BytesIO(data), strict=False)
    n_pages = len(reader.pages)
    # Muestreo para identificar portada, norma y anexos. No es auditoría integral.
    sample = sorted(set(list(range(min(n_pages, 14))) + [n_pages//2, n_pages-1]))
    chunks, extraction_errors = [], 0
    for page in sample:
        try:
            chunks.append(reader.pages[page].extract_text() or "")
        except Exception:
            extraction_errors += 1
    return "\n".join(chunks), n_pages, extraction_errors

def process(group):
    ids = sorted(r["id"] for r in group)
    doc = group[0]
    urls = [doc["url"]]
    if doc.get("url_alternativa") and doc["url_alternativa"] not in urls:
        urls.append(doc["url_alternativa"])
    report = {
        "ids": ids, "norma_esperada": doc["norma_de_referencia"],
        "estado": "NO_DESCARGADO",
        "validacion_curricular": False,
        "documento_completo_verificado": False,
        "intentos": []}
    for url in urls:
        attempt = {"url":url}
        try:
            data, final, kind = fetch(url)
            text, pages, errors = extract(data, kind)
            match = norm(doc["norma_de_referencia"]) in norm(text)
            # Si la norma no está literalmente en texto extraído, no es verificable automáticamente.
            sha = hashlib.sha256(data).hexdigest()
            path = OUT / (sha[:20] + (".pdf" if kind == "PDF" else ".html"))
            path.write_bytes(data)
            host = (urlparse(final).hostname or "").lower()
            official = host in OFFICIAL_DOMAINS
            report.update(
                estado=("NORMA_IDENTIFICADA_PENDIENTE_REVISION" if match else "DESCARGADO_NORMA_NO_IDENTIFICADA"),
                url_efectiva=final, archivo=path.name,
                formato=kind, bytes=len(data), sha256=sha,
                dominio_institucional=official, paginas_pdf=pages,
                errores_extraccion_pdf=errors, titulo_norma_coincide=match)
            attempt.update(resultado="DESCARGADO",formato=kind,titulo_norma_coincide=match,
                           dominio_institucional=official)
            report["intentos"].append(attempt)
            # Si se descargó un HTML o una copia no oficial, también queda documentado.
            # Se continúa con la alternativa solo si no se pudo descargar la fuente principal.
            break
        except Exception as exc:
            attempt.update(resultado="ERROR",error=str(exc)[:300])
            report["intentos"].append(attempt)
    return report

def main():
    catalog = json.loads((ROOT / "datos/catalogo_51_autonomicos.json").read_text(encoding="utf-8"))
    subset = [r for r in catalog["registros"] if r["id"] in IDS]
    assert len(subset) == len(IDS), "Faltan registros de las fuentes que requieren reintento"
    groups = {}
    for r in subset:
        groups.setdefault(r["url"], []).append(r)
    reports = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(process, group) for group in groups.values()]
        for task in as_completed(futures):
            result = task.result()
            reports.append(result)
            print(",".join(result["ids"]) + ": " + result["estado"], flush=True)
    reports.sort(key=lambda r:r["ids"][0])
    summary = {
        "generado_utc":datetime.now(timezone.utc).isoformat(),
        "registros_reintentados":len(subset),
        "direcciones_unicas_reintentadas":len(groups),
        "archivos_descargados":sum(r["estado"] != "NO_DESCARGADO" for r in reports),
        "normas_identificadas_preliminarmente":sum(r["estado"] == "NORMA_IDENTIFICADA_PENDIENTE_REVISION" for r in reports),
        "fuentes_sin_descarga":sum(r["estado"] == "NO_DESCARGADO" for r in reports),
        "curriculos_verificados":0,
        "aviso":"La revisión de vigencia, anexos y materias es posterior. Cualquier documento no oficial requiere cotejo con boletín."
    }
    (OUT / "manifest.json").write_text(json.dumps({"resumen":summary,"resultados":reports},ensure_ascii=False,indent=2),encoding="utf-8")
    print("RESUMEN: " + json.dumps(summary,ensure_ascii=False),flush=True)

if __name__ == "__main__":
    main()
