#!/usr/bin/env python3
"""Consolidación provisional de los documentos recuperados por GitHub Actions.

Agrupa por SHA-256 y registra evidencias de identidad documental.
Nunca habilita curricularmente una comunidad, etapa, curso o materia.
Los textos legales deben verificarse íntegramente y cotejarse con versiones vigentes.
"""
import argparse, csv, hashlib, json, re, unicodedata
from collections import defaultdict, Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

class ExtractorHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections=[]; self.ignored=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript','svg'):self.ignored+=1
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript','svg'):self.ignored=max(0,self.ignored-1)
    def handle_data(self,v):
        if not self.ignored:self.sections.append(v)

def norm(t):
    t=unicodedata.normalize('NFKD', t or '').lower()
    t=''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', t).strip()

def classify(blob):
    if blob.startswith(b'%PDF-'):return 'PDF'
    if b'<html' in blob[:30000].lower() or b'<!doctype html' in blob[:30000].lower():return 'HTML'
    return 'DESCONOCIDO'

def examine(path,expected):
    raw=path.read_bytes()
    typ=classify(raw)
    result={'tipo':typ,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'revision_integral_anexos':False,'validez_juridica_confirmada':False,
            'habilitado_para_generar':False}
    try:
        if typ=='PDF':
            reader=PdfReader(BytesIO(raw),strict=False)
            n=len(reader.pages)
            result['paginas']=n
            if n<1:raise ValueError('PDF sin páginas')
            pages=sorted(set(list(range(min(n,12)))+[n//4,n//2,3*n//4,n-1]))
            pieces=[]
            for pg in pages:
                pieces.append(reader.pages[pg].extract_text() or '')
            result['paginas_muestreadas']=len(pages)
            content='\n'.join(pieces)
        elif typ=='HTML':
            parser=ExtractorHTML()
            parser.feed(raw.decode('utf-8',errors='replace'))
            content=' '.join(parser.sections)[:3000000]
        else:
            raise ValueError('No es PDF ni HTML')
        sample=norm(content)
        result['normas_esperadas_identificadas']=[n for n in sorted(set(expected)) if norm(n) in sample]
        result['indicio_anexos']=bool(re.search(r'\banexos?\b',sample))
        result['indicio_competencias_especificas']=bool(re.search(r'competencias especificas|competencies especifiques|konpetentzia espezifiko',sample))
        result['indicio_criterios_evaluacion']=bool(re.search(r'criterios de evaluacion|criteris d.avaluacio|ebaluazio irizpide',sample))
        result['indicio_saberes_basicos']=bool(re.search(r'saberes basicos|sabers basics|contidos|contenidos',sample))
        result['muestra_caracteres']=len(sample)
        result['estado']='IDENTIDAD_PRELIMINAR' if result['normas_esperadas_identificadas'] else 'DESCARGA_NO_IDENTIFICADA'
    except Exception as e:
        result['estado']='ERROR_EXTRACCION'
        result['error']=str(e)[:200]
    return result

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument('base',help='Carpeta con artefactos de GitHub ya descargados')
    args=arg.parse_args()
    base=Path(args.base)
    manifests=list(base.rglob('manifest.json'))
    all_records=[];missing=[]
    for manifest in manifests:
        source=json.loads(manifest.read_text(encoding='utf-8'))
        records=source.get('fuentes') or source.get('documentos') or source.get('resultados') or []
        for item in records:
            file=item.get('archivo')
            if not file:continue
            p=manifest.parent/file
            if not p.is_file():
                missing.append({'manifest':str(manifest.relative_to(base)),'archivo':file});continue
            ids=item.get('ids') or ([item['id']] if item.get('id') else [])
            norms=item.get('normas') or ([item['norma']] if item.get('norma') else ([item['norma_esperada']] if item.get('norma_esperada') else []))
            if isinstance(norms,str):norms=[norms]
            all_records.append({'path':p,'ids':ids,'normas':norms,'url':item.get('url') or item.get('url_efectiva') or '',
                                'lote':str(manifest.relative_to(base))})
    byhash={}
    for row in all_records:
        sha=hashlib.sha256(row['path'].read_bytes()).hexdigest()
        if sha not in byhash:
            byhash[sha]={'path':row['path'],'ids':set(),'normas':set(),'urls':set(),'lotes':set()}
        found=byhash[sha]
        found['ids'].update(row['ids']);found['normas'].update(row['normas'])
        if row['url']:found['urls'].add(row['url'])
        found['lotes'].add(row['lote'])
    documents=[]
    for sha,data in sorted(byhash.items()):
        info=examine(data['path'],data['normas'])
        info.update({
            'identificador_documental':sha[:16],
            'identificadores_de_curriculo':sorted(data['ids']),
            'normas_esperadas':sorted(data['normas']),
            'urls_de_origen':sorted(data['urls']),
            'lotes':sorted(data['lotes'])
        })
        documents.append(info)
        print(info['identificador_documental']+': '+info['estado'],flush=True)
    count=Counter(r['estado'] for r in documents)
    result={
        'fecha_utc':datetime.now(timezone.utc).isoformat(),
        'manifiestos_procesados':len(manifests),
        'referencias_documentales_recuperadas':len(all_records),
        'documentos_unicos_por_sha256':len(documents),
        'documentos_con_identificacion_preliminar':count.get('IDENTIDAD_PRELIMINAR',0),
        'documentos_descargados_sin_identificacion':count.get('DESCARGA_NO_IDENTIFICADA',0),
        'documentos_con_error_extraccion':count.get('ERROR_EXTRACCION',0),
        'faltantes_en_archivos':len(missing),
        'registros_autonomicos_catalogados':51,
        'curriculos_completamente_verificados':0,
        'materias_habilitadas_para_generar':0,
        'alerta':'Documento descargado o norma identificada NO implica anexos completos, vigencia ni cobertura curricular. Requiere comprobación humana íntegra por materia y curso.',
        'procedencia':'GitHub Actions: descargas de lotes y reintentos.'
    }
    report={'resumen':result,'documentos':documents,'faltantes':missing}
    out=ROOT/'datos'
    out.mkdir(exist_ok=True)
    (out/'estado_documental.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    md=['# OPO-IA — Estado documental preliminar','',
        'Fecha UTC: '+result['fecha_utc'],'',
        '| Indicador | Resultado |','|---|---:|']
    for k,label in [
        ('manifiestos_procesados','Manifiestos examinados'),
        ('referencias_documentales_recuperadas','Registros recuperados (incluye duplicados)'),
        ('documentos_unicos_por_sha256','Archivos distintos por huella SHA-256'),
        ('documentos_con_identificacion_preliminar','Archivos con coincidencia preliminar de norma'),
        ('documentos_descargados_sin_identificacion','Archivos sin identificación preliminar'),
        ('documentos_con_error_extraccion','Errores de extracción'),
        ('faltantes_en_archivos','Archivos no localizados en artefactos'),
        ('curriculos_completamente_verificados','Currículos completos validados'),
        ('materias_habilitadas_para_generar','Materias habilitadas')]:
        md.append('| '+label+' | '+str(result[k])+' |')
    md+=['','**Advertencia:** '+result['alerta'],'',
         'Esta tabla resume una comprobación automática por muestreo y no constituye una auditoría de vigencia ni de contenido curricular íntegro.',
         'Los documentos PDF/HTML originales permanecen en artefactos temporales de GitHub Actions; el registro JSON sí se conserva en el repositorio.']
    (out/'ESTADO_DOCUMENTAL.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print('CONSOLIDACION '+json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':
    main()
