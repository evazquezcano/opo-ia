#!/usr/bin/env python3
"""Comprobación preliminar de identidad normativa y presencia de anexos.

Nunca activa la generación: comprobar páginas no equivale a revisión jurídica
ni a extracción exacta del currículo por materia y curso.
"""
import json,sys,re,hashlib,unicodedata
from html.parser import HTMLParser
from pathlib import Path
from io import BytesIO
from pypdf import PdfReader

def norm(t):
    t=unicodedata.normalize("NFKD",t or "")
    return re.sub(r"\s+"," ","".join(ch for ch in t.lower() if not unicodedata.combining(ch)))

class Plain(HTMLParser):
    def __init__(self): super().__init__();self.chunks=[];self.block=False
    def handle_data(self,txt):self.chunks.append(txt)
def analyze(path,norma):
    bs=path.read_bytes()
    typ="pdf" if bs.startswith(b"%PDF-") else "html" if b"<html" in bs[:30000].lower() else "otro"
    ans={"archivo":path.name,"tipo":typ,"sha256":hashlib.sha256(bs).hexdigest(),"bytes":len(bs),
         "identificacion_norma":False,"indicio_de_anexos":False,
         "indicio_competencias":False,"indicio_criterios":False,"indicio_saberes":False,
         "verificado_curricularmente":False}
    if typ=="pdf":
        reader=PdfReader(BytesIO(bs),strict=False)
        n=len(reader.pages)
        ans["paginas"]=n
        if not n:return ans
        # Muestreo preliminar: inicio, cuarto, centro y final; NO cobertura integral.
        nums=sorted(set(list(range(min(n,8)))+[n//4,n//2,3*n//4,n-1]))
        text="\n".join((reader.pages[i].extract_text() or "") for i in nums)
        ans["paginas_muestreadas"]=nums
    elif typ=="html":
        p=Plain();p.feed(bs.decode("utf-8",errors="replace"))
        text=" ".join(p.chunks)[:2500000]
    else:
        ans["incidencia"]="No es PDF ni HTML"
        return ans
    txt=norm(text); name=norm(norma)
    ans["identificacion_norma"]=name in txt
    ans["indicio_de_anexos"]=bool(re.search(r"\banexos?\s+(i|ii|iii|iv|1|2)\b|\banexo\b",txt))
    ans["indicio_competencias"]="competencias especificas" in txt or "competencies especifiques" in txt
    ans["indicio_criterios"]="criterios de evaluacion" in txt or "criteris d'avaluacio" in txt or "criteris d’avaluacio" in txt
    ans["indicio_saberes"]="saberes basicos" in txt or "sabers basics" in txt or "continguts" in txt
    ans["texto_muestreado_caracteres"]=len(txt)
    ans["aviso"]="Indicios preliminares. Verificar íntegramente anexos, versiones y aplicación por materia."
    return ans

def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("documentos_normativos")
    reports=[]
    for manifest in sorted(root.rglob("manifest.json")):
        obj=json.loads(manifest.read_text(encoding="utf-8"))
        records=obj.get("documentos") or obj.get("fuentes") or obj.get("resultados") or []
        for r in records:
            file_name=r.get("archivo")
            if not file_name:continue
            file=manifest.parent/file_name
            if not file.exists():
                reports.append({"ids":r.get("ids") or [r.get("id")],"incidencia":"Archivo no encontrado","archivo":file_name})
                continue
            norma=r.get("norma_esperada") or r.get("norma") or (r.get("normas") or [""])[0]
            try:
                val=analyze(file,norma)
                val["ids"]=r.get("ids") or [r.get("id")]
                val["norma_esperada"]=norma
                reports.append(val)
            except Exception as ex:
                reports.append({"ids":r.get("ids") or [r.get("id")],"archivo":file_name,"incidencia":str(ex)[:200],"verificado_curricularmente":False})
    out=Path("resultados_auditoria");out.mkdir(exist_ok=True)
    summary={"registros_documentales_analizados":len(reports),
             "normas_identificadas_en_muestra":sum(bool(r.get("identificacion_norma")) for r in reports),
             "indicios_de_anexos":sum(bool(r.get("indicio_de_anexos")) for r in reports),
             "curriculos_verificados":0,
             "nota":"Indicios exploratorios sobre muestras; se requiere revisión íntegra de los anexos."}
    (out/"auditoria_preliminar.json").write_text(json.dumps({"resumen":summary,"documentos":reports},ensure_ascii=False,indent=2),encoding="utf-8")
    print("AUDITORIA_PRELIMINAR "+json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=="__main__": main()
