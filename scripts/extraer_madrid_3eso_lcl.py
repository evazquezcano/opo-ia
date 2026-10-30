#!/usr/bin/env python3
"""OPO-IA: primera extracción literal por páginas, Madrid LCL 3º ESO.

Fuente: Decreto 65/2022 (BOCM 26/07/2022), anexo II.
Se utiliza el PDF original descargado en GitHub Actions.
No equiparar extracción a validación literal final ni a vigencia.
"""
import json,re,hashlib
from pathlib import Path
from datetime import datetime,timezone
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"fuentes_temporales"/"MD-eso-2022.pdf"
OUT=ROOT/"datos"/"madrid"/"eso"/"3"/"lengua-castellana-literatura"
OUT.mkdir(parents=True,exist_ok=True)
assert PDF.exists(),f"No encontrado {PDF}"
raw=PDF.read_bytes()
assert raw.startswith(b"%PDF-"),"No se ha descargado un PDF"
pdf=PdfReader(PDF,strict=False)
assert len(pdf.pages)>=180,f"PDF inesperadamente corto, páginas: {len(pdf.pages)}"
# El archivo PDF empieza en BOCM página impresa 396. PDF índice 0 -> BOCM 396.
pages={}
for printed in list(range(547,572)) + [397,398,399,400]:
    idx=printed-396
    if idx<0 or idx>=len(pdf.pages):continue
    txt=pdf.pages[idx].extract_text(extraction_mode="plain") or ""
    pages[printed]=txt
    print(f"BOCM {printed}: {len(txt)} caracteres",flush=True)
def pack(r):
    return "\n\n".join(f"=== BOCM PÁGINA {p} / PDF {p-395} ===\n{pages[p]}" for p in r if p in pages)
(OUT/"fuente_lcl_paginas_547_571.txt").write_text(pack(range(547,572)),encoding="utf-8")
(OUT/"fuente_objetivos_etapa_paginas_397_400.txt").write_text(pack(range(397,401)),encoding="utf-8")
t=pack(range(565,572))
# Identificación literal de criterio/códigos únicamente (la extracción completa se valida después).
criterion_match=re.search(r"3\s*[ºo°]\s*ESO\s*\.?\s*Criterios de evaluación",t,re.I)
contents_match=re.search(r"\bContenidos\s*\.\s*\n\s*A\s*\.\s*Las lenguas y sus hablantes",t,re.I)
assert criterion_match,"No se reconoce el encabezado 3º ESO / criterios de evaluación"
assert contents_match,"No se reconoce el inicio de contenidos de 3º ESO"
criterion_text=t[criterion_match.end():contents_match.start()]
# Evitar elementos paginadores como pies de boletín
criterion_text="\n".join(v for v in criterion_text.splitlines() if not re.search(r"^\s*(?:BOCM\s*$|BOCM-20220726-2\s*$|B\.O\.C\.M\..*|BOLETÍN OFICIAL DE LA COMUNIDAD DE MADRID\s*$|Pág\.\s*\d+\s*[—-]|MARTES 26 DE JULIO DE 2022|Pág\.\s*\d+)",v,re.I))
criterion_text=re.sub(r"\n\s*Competencia específica\s+\d+\s*\.\s*\n","\n",criterion_text)
# Unión de saltos de línea para criterios de varias líneas; código 1.1. ... 10.2.
entries=[]
pattern=re.compile(r"(?<![\d.])((?:10|[1-9])\.\d{1,2})\.\s+(?=[A-ZÁÉÍÓÚÜÑ])")
matches=list(pattern.finditer(criterion_text))
for i,m in enumerate(matches):
    end=matches[i+1].start() if i+1<len(matches) else len(criterion_text)
    literal=re.sub(r"\s+"," ",criterion_text[m.end():end]).strip()
    # El texto debe terminar en un signo de cierre, sin cabeceras de página.
    entries.append({"codigo":m.group(1),"competencia_especifica":m.group(1).split(".")[0],"texto_literal":literal,"pagina_bocm_inicio":565})
keys=[r["codigo"] for r in entries]
if len(keys)!=len(set(keys)):raise ValueError("Códigos de criterio duplicados")
expected=tuple(str(n) for n in range(1,11))
coverage=sorted(set(x["competencia_especifica"] for x in entries),key=int)
assert tuple(coverage)==expected,f"No se extrajeron las 10 competencias de criterios: {coverage}"
counts={x:sum(e["competencia_especifica"]==x for e in entries) for x in expected}
# Capturar sección de contenidos sin intentar codificar jerarquía a ciegas.
content_block=t[contents_match.end():]
content_block="\n".join(v for v in content_block.splitlines() if not re.search(r"^\s*(?:BOCM\s*$|BOCM-20220726-2\s*$|B\.O\.C\.M\..*|BOLETÍN OFICIAL DE LA COMUNIDAD DE MADRID\s*$|Pág\.\s*\d+\s*[—-]|MARTES 26 DE JULIO DE 2022)",v,re.I))
next_grade=re.search(r"(?:^|\n)\s*4\s*[ºo°]\s*ESO\s*\.",content_block,re.I)
assert next_grade,"No se encontró límite de 4º ESO; no se permite extraer un curso distinto"
content_block=content_block[:next_grade.start()]
# Se conservan las líneas y niveles tipográficos para la revisión humana de códigos internos.
(OUT/"contenidos_3eso_fuente_sin_codificar.txt").write_text(content_block.strip()+"\n",encoding="utf-8")
# Competencias específicas y descriptores: sección previa al inicio 1º ESO.
intro=pack(range(547,555))
(OUT/"competencias_descriptores_fuente.txt").write_text(intro,encoding="utf-8")
meta={
  "id":"MD-ESO-3-LCL","comunidad":"Comunidad de Madrid","etapa":"ESO",
  "curso":"3.º","materia":"Lengua Castellana y Literatura",
  "fuente":{"norma":"Decreto 65/2022, de 20 de julio","diario":"BOCM 176, 26/07/2022",
    "url":"https://www.bocm.es/boletin/CM_Orden_BOCM/2022/07/26/BOCM-20220726-2.PDF",
    "sha256":hashlib.sha256(raw).hexdigest(),"paginas_criterios":"565-567","paginas_contenidos":"567-571",
    "paginas_competencias":"547-553","hora_extraccion_utc":datetime.now(timezone.utc).isoformat()},
  "referencia_modificacion":{"norma":"Decreto 59/2024, de 12 de junio","revision_de_impacto_por_materia":"PENDIENTE"},
  "periodos_semanales":4,
  "criterios_evaluacion":entries,
  "recuento_por_competencia":counts,
  "bloques_detectados":[],
  "competencias_especificas":[],
  "descriptores_perfil_salida":[],
  "objetivos_etapa":[],
  "validacion":{"integridad_texto_criterios":"PENDIENTE_COTEJO_VISUAL","integridad_saberes":"PENDIENTE_CODIFICACION_Y_COTEJO",
      "vigencia_normativa":"PENDIENTE_COTEJO","curriculo_completo_verificado":False,
      "habilitado_para_generar":False}
}
for m in re.finditer(r"(?m)^\s*([ABCD])\.\s+([^\n]{4,130})",content_block):
    meta["bloques_detectados"].append({"bloque":m.group(1),"titulo_extraido":m.group(2).strip()})
(OUT/"extraccion_preliminar_3eso.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("EXTRACCION "+json.dumps({"numero_criterios":len(entries),"recuento":counts,"bloques":meta["bloques_detectados"],"fuente_paginas":len(pages),"habilitado":False},ensure_ascii=False),flush=True)
