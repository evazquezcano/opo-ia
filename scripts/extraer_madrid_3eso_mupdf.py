#!/usr/bin/env python3
"""Segunda extracción, con PyMuPDF; controles contra roturas de palabras del PDF."""
import fitz, re, json, hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"fuentes_temporales"/"MD-eso-2022.pdf"
OUT=ROOT/"datos/madrid/eso/3/lengua-castellana-literatura"
OUT.mkdir(parents=True,exist_ok=True)
d=fitz.open(PDF)
assert len(d)>175
def page(p):
    return d[p-396].get_text("text",sort=True)
def clean_section(pages):
    lines=[]
    for p in pages:
        text=page(p)
        if p==565 and "Criterios de evaluación" not in text:
            raise ValueError("Página 565 no contiene criterios")
        lines.append(f"\n===BOCM_PAGINA_{p}===\n"+text)
    return "\n".join(lines)
critall=clean_section(range(565,572))
start=re.search(r"3\s*[º°o]\s*ESO\s*\.?\s*Criterios de evaluación\s*\.",critall,re.I)
cont=re.search(r"\bContenidos\s*\.\s*A\s*\.\s*Las lenguas y sus hablantes",critall,re.I)
end=re.search(r"4\s*[º°o]\s*ESO\s*\.?\s*Criterios de evaluación",critall,re.I)
assert start and cont and end, f"Separadores no encontrados: {bool(start)}/{bool(cont)}/{bool(end)}"
def strip_margins(s):
    lines=[]
    for l in s.splitlines():
        if re.search(r"^(?:B\.?O\.?C\.?M\.?(?:\s+Núm.*)?|BOLETÍN OFICIAL DE LA COMUNIDAD DE MADRID|===BOCM_PAGINA_|Pág\.\s*\d+|MARTES 26 DE JULIO DE 2022|BOCM-20220726-2)",l.strip(),re.I):continue
        lines.append(l.strip())
    return "\n".join(lines)
criterios=strip_margins(critall[start.end():cont.start()])
criterios=re.sub(r"(?im)^\s*Competencia específica\s+\d+\.\s*$","",criterios)
pat=re.compile(r"(?m)^\s*((?:10|[1-9])\.\d{1,2})\.\s+")
matches=list(pat.finditer(criterios))
results=[]
for i,m in enumerate(matches):
    snippet=criterios[m.end():matches[i+1].start() if i+1<len(matches) else len(criterios)]
    snippet=re.sub(r"\s+"," ",snippet).strip()
    results.append({"codigo":m.group(1),"competencia_especifica":m.group(1).split(".")[0],"texto_literal":snippet})
ids=[x["codigo"] for x in results]
assert len(ids)==31 and len(set(ids))==31,f"Esperaba 31 criterios, encontrados: {len(ids)}"
assert sorted(set(int(x.split(".")[0]) for x in ids))==list(range(1,11))
for test in ["variedades dialectales","sociolingüístico","diferentes lenguas"]:
    # solo los dos primeros se esperan en el primer criterio
    if test!="diferentes lenguas":assert test in results[0]["texto_literal"],f"Error de letras: {test} no está en 1.1"
assert results[-1]["codigo"]=="10.2"
contents=strip_margins(critall[cont.start():end.start()])
bpat=re.compile(r"(?m)^\s*([ABCD])\.\s+([^\n]+)")
blocks=[{"bloque":m.group(1),"titulo_literal":m.group(2).strip()} for m in bpat.finditer(contents)]
assert [b["bloque"] for b in blocks]==["A","B","C","D"],f"Bloques incompletos: {blocks}"
# Fuente completa con texto extraído, no edición literaria; se guardan saltos.
(OUT/"mupdf_criterios_3eso_fuente.txt").write_text(criterios,encoding="utf-8")
(OUT/"mupdf_contenidos_3eso_fuente.txt").write_text(contents,encoding="utf-8")
intro=clean_section(range(548,554))
(OUT/"mupdf_competencias_descriptores_fuente.txt").write_text(intro,encoding="utf-8")
data={
  "id":"MD-ESO-3-LCL","curso":"3º ESO","materia":"Lengua Castellana y Literatura",
  "comunidad":"Comunidad de Madrid","horas_semanales":4,
  "norma":"Decreto 65/2022, de 20 de julio (BOCM 176, anexo II)",
  "fuente_url":"https://www.bocm.es/boletin/CM_Orden_BOCM/2022/07/26/BOCM-20220726-2.PDF",
  "sha256_pdf":hashlib.sha256(PDF.read_bytes()).hexdigest(),
  "criterios":results,
  "bloques":blocks,
  "pendiente_extraccion":["competencias_especificas_literales","descriptores","objetivos_etapa","jerarquia_interna_de_saberes","cotejo_visual_integral"],
  "modificacion_2024":"El Decreto 59/2024 modifica organización bilingüe y los contenidos de Geografía e Historia, no el anexo II de LCL (revisado en BOCM).",
  "validado_para_generador":False,
  "extraccion_utc":datetime.now(timezone.utc).isoformat()
}
(OUT/"criterios_3eso_lcl_mupdf_borrador.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("VALIDACION_INICIAL "+json.dumps({"criterios":len(ids),"competencias":len(set(x["competencia_especifica"] for x in results)),"bloques":blocks,"criterio_1_1":results[0]["texto_literal"][:130],"habilitado":False},ensure_ascii=False),flush=True)
