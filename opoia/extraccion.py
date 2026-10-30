"""Índice de evidencias de normativa curricular a partir de PDF aportados.

El resultado es un índice de páginas y extractos **sin validación jurídica**.
No mezcla automáticamente las modificaciones con el texto principal.
No registra archivos, texto íntegro ni metadatos en disco o bases de datos.
"""
from __future__ import annotations

import re
import unicodedata

import fitz

from .fuentes import MAX_BYTES, MAX_PAGES, normalizar

TERMINOS = {
    "objetivos_etapa": ("objetivos de la etapa", "objetivos", "objetivos da etapa", "objectius"),
    "competencias_especificas": (
        "competencias especificas", "competencies especifiques",
        "competencias específicas", "konpetentzia espezifiko",
    ),
    "criterios_evaluacion": (
        "criterios de evaluacion", "criteris d'avaluacio", "criteris d’avaluacio",
        "criterios de avaliacion", "ebaluazio irizpide",
    ),
    "saberes_contenidos": (
        "saberes basicos", "sabers basics", "contenidos", "contidos",
        "edukiak",
    ),
    "descriptores_operativos": ("descriptores operativos", "descriptors operatius"),
    "elementos_transversales": (
        "elementos transversales", "elementos transversais", "elements transversals",
        "contenidos transversales",
    ),
}
MAX_RESULTS_PER_CATEGORY = 12
MAX_EXTRACT_LENGTH = 340


def _palabras_materia(materia: str) -> list[str]:
    """Palabras de materia sin atribuirse capacidad para reconocer sinónimos."""
    return [w for w in re.findall(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+", normalizar(materia)) if len(w) > 3]


def _extracto(lineas: list[str], numero: int) -> str:
    principio = max(0, numero - 1)
    fin = min(len(lineas), numero + 3)
    return re.sub(r"\s+", " ", " ".join(lineas[principio:fin]))[:MAX_EXTRACT_LENGTH]


def indexar_documento(datos: bytes, nombre: str, funcion: str, materia: str, curso: str) -> dict:
    """Indexa el PDF completo página a página, sin atribuir integridad o vigencia.

    Solo persiste como salida el índice de evidencias (extractos breves) y conteos.
    """
    out = {
        "archivo": nombre,
        "funcion": funcion,
        "paginas_pdf": 0,
        "paginas_con_texto": 0,
        "paginas_con_materia": [],
        "indicios_por_elemento": {clave: [] for clave in TERMINOS},
        "fragmentos_de_curso": [],
        "estado": "NO_EXTRAIBLE",
        "advertencias": [],
        "revision_literal_completa": False,
        "revision_vigencia": False,
        "cambios_juridicos_aplicados": False,
    }
    if not datos.startswith(b"%PDF-") or len(datos) > MAX_BYTES:
        out["advertencias"].append("El archivo no es un PDF válido o excede el tamaño admitido.")
        return out
    palabras = _palabras_materia(materia)
    numero_curso = re.search(r"\d+", curso)
    curso_regex = None
    if numero_curso:
        n = re.escape(numero_curso.group())
        curso_regex = re.compile(rf"\b{n}\s*(?:º|°|o|\.º|\.o)?\s*(?:curso|eso|bachillerato|primaria)?\b", re.I)
    try:
        with fitz.open(stream=datos, filetype="pdf") as documento:
            if documento.needs_pass:
                out["advertencias"].append("PDF protegido con contraseña.")
                return out
            if len(documento) > MAX_PAGES:
                out["advertencias"].append("PDF superior a 1.500 páginas.")
                return out
            out["paginas_pdf"] = len(documento)
            for i, pagina in enumerate(documento):
                texto = pagina.get_text("text", sort=True)
                if not texto.strip():
                    continue
                out["paginas_con_texto"] += 1
                normal = normalizar(texto)
                palabras_en_pagina = bool(palabras) and all(p in normal for p in palabras)
                if palabras_en_pagina and len(out["paginas_con_materia"]) < 80:
                    out["paginas_con_materia"].append(i + 1)
                lineas = texto.splitlines()
                for indice, linea in enumerate(lineas):
                    normal_linea = normalizar(linea)
                    if not normal_linea:
                        continue
                    if curso_regex and curso_regex.search(linea):
                        if len(out["fragmentos_de_curso"]) < 15:
                            out["fragmentos_de_curso"].append({
                                "pagina_pdf": i + 1,
                                "extracto": _extracto(lineas, indice),
                            })
                    for clave, variaciones in TERMINOS.items():
                        entradas = out["indicios_por_elemento"][clave]
                        if len(entradas) >= MAX_RESULTS_PER_CATEGORY:
                            continue
                        if any(normalizar(variacion) in normal_linea for variacion in variaciones):
                            entradas.append({
                                "pagina_pdf": i + 1,
                                "extracto": _extracto(lineas, indice),
                                "coincidencia_de_materia_en_pagina": palabras_en_pagina,
                            })
            out["estado"] = (
                "INDICE_PRELIMINAR"
                if out["paginas_con_texto"] else "PDF_SIN_TEXTO_EXTRAIBLE"
            )
            if out["estado"] == "PDF_SIN_TEXTO_EXTRAIBLE":
                out["advertencias"].append(
                    "No se encontró texto seleccionable; necesita OCR o una publicación accesible."
                )
            if not out["paginas_con_materia"]:
                out["advertencias"].append(
                    "No se ha localizado la denominación completa de la materia en una página. "
                    "Esto no demuestra que el currículo esté ausente."
                )
            out["advertencias"].append(
                "Este índice identifica páginas candidatas; no acredita la extracción "
                "literal completa, las modificaciones aplicables ni la vigencia."
            )
    except (ValueError, RuntimeError, fitz.FileDataError) as exc:
        out["estado"] = "ERROR"
        out["advertencias"].append("Error de apertura o lectura: " + type(exc).__name__)
    return out


def consolidar_evidencias(indices: list[dict]) -> dict:
    """Resume las fuentes sin alterar ni reemplazar jurídicamente texto alguno."""
    if not indices:
        return {
            "estado": "SIN_DOCUMENTO_PRINCIPAL",
            "fuentes": [],
            "pendiente": ["Aportar documento curricular principal"],
            "curriculo_validado": False,
        }
    if indices[0]["funcion"] != "Currículo principal":
        raise ValueError("La primera entrada debe ser el currículo principal")
    principales = indices[0]
    enmiendas = [i for i in indices[1:] if i["funcion"].startswith("Modificación")]
    evaluacion = [i for i in indices[1:] if i["funcion"] == "Normativa de evaluación"]
    categorias = list(TERMINOS)
    return {
        "estado": "INDICE_DE_EVIDENCIAS_PARA_COTEJO",
        "fuentes": [x["archivo"] for x in indices],
        "principal": {
            "archivo": principales["archivo"],
            "elementos_localizados": {
                key: len(principales["indicios_por_elemento"].get(key, []))
                for key in categorias
            },
            "paginas_candidatas_de_materia": principales["paginas_con_materia"],
        },
        "modificaciones": [
            {
                "archivo": e["archivo"],
                "posibles_elementos_afectados": [
                    key for key in categorias if e["indicios_por_elemento"].get(key)
                ],
                "estado": "IMPACTO_JURIDICO_PENDIENTE_DE_COTEJO",
            }
            for e in enmiendas
        ],
        "evaluacion": [
            {"archivo": e["archivo"], "estado": "CONSULTA_SEPARADA_OPCIONAL"}
            for e in evaluacion
        ],
        "pendiente": [
            "Identificar límites exactos de la materia y curso en los anexos",
            "Verificar y transcribir literalmente todos los elementos curriculares",
            "Cotejar modificaciones y correcciones y aplicar solo los cambios pertinentes",
            "Revisar el alcance temporal y la vigencia de la norma",
            "Comprobar la cobertura conjunta antes de generar UD y SA",
        ],
        "curriculo_validado": False,
        "puede_generar_unidades_definitivas": False,
    }
