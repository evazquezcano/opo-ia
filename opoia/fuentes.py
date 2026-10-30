"""Lectura preliminar de PDF normativos aportados por estudiantes.

No valida vigencia, integridad de anexos ni literalidad curricular.
No guarda archivos originales ni envía su contenido a servicios externos.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from urllib.parse import urlparse

import fitz

MAX_BYTES = 35 * 1024 * 1024
MAX_PAGES = 1500

_TERMINOS = {
    "competencias específicas": (
        "competencias especificas", "competencies especifiques",
        "konpetentzia espezifikoak",
    ),
    "criterios de evaluación": (
        "criterios de evaluacion", "criterios de avaliacion",
        "criteris d'avaluacio", "criteris d’avaluacio",
        "ebaluazio irizpideak",
    ),
    "saberes o contenidos": (
        "saberes basicos", "sabers basics", "contidos",
        "contenidos", "edukiak",
    ),
    "anexos": ("anexo", "annex", "eranskina"),
    "evaluación": ("evaluacion", "avaliacion", "avaluacio", "ebaluazio"),
}


def normalizar(texto: str) -> str:
    descompuesto = unicodedata.normalize("NFKD", texto.casefold())
    return " ".join("".join(
        caracter for caracter in descompuesto
        if not unicodedata.combining(caracter)
    ).split())


def url_normativa_valida(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def analizar_pdf(datos: bytes, nombre: str, tipo: str) -> dict:
    """Obtiene metadatos y pistas textuales de un PDF sin conservar su contenido.

    Las coincidencias se buscan en una muestra, nunca se interpretan
    como prueba de que el documento contenga todos los elementos.
    """
    registro = {
        "archivo": nombre,
        "funcion_documental": tipo,
        "tamano_bytes": len(datos),
        "huella_sha256": hashlib.sha256(datos).hexdigest(),
        "paginas": None,
        "paginas_muestreadas": 0,
        "estado": "NO_EXAMINADO",
        "indicios_textuales": [],
        "observaciones": [],
        "curriculo_verificado": False,
        "vigencia_normativa_verificada": False,
    }
    if not datos:
        registro.update(estado="ERROR", observaciones=["El archivo está vacío."])
        return registro
    if len(datos) > MAX_BYTES:
        registro.update(estado="ERROR", observaciones=["El archivo supera el límite de 35 MB."])
        return registro
    if b"%PDF-" not in datos[:1024]:
        registro.update(estado="ERROR", observaciones=["El contenido no tiene cabecera PDF válida."])
        return registro

    try:
        with fitz.open(stream=datos, filetype="pdf") as documento:
            if documento.needs_pass:
                registro.update(
                    estado="ERROR",
                    observaciones=["El archivo está protegido con contraseña."]
                )
                return registro
            paginas = len(documento)
            registro["paginas"] = paginas
            if not paginas or paginas > MAX_PAGES:
                registro.update(
                    estado="ERROR",
                    observaciones=["El PDF está vacío o supera las 1.500 páginas permitidas."]
                )
                return registro

            indices = sorted({
                0, min(1, paginas - 1), min(2, paginas - 1),
                paginas // 4, paginas // 2, (3 * paginas) // 4,
                max(paginas - 2, 0), paginas - 1,
            })
            fragmentos = []
            for indice in indices:
                fragmentos.append(documento[indice].get_text("text", sort=True))
            registro["paginas_muestreadas"] = len(indices)

        texto = normalizar("\n".join(fragmentos))
        registro["indicios_textuales"] = [
            etiqueta
            for etiqueta, variantes in _TERMINOS.items()
            if any(normalizar(variante) in texto for variante in variantes)
        ]
        if len(texto) < 120:
            registro.update(
                estado="TEXTO_NO_EXTRAIBLE",
                observaciones=[
                    "La muestra apenas contiene texto seleccionable; puede ser un escaneado.",
                    "Se requerirá OCR o una versión oficial accesible antes de extraer el currículo.",
                ],
            )
        else:
            registro.update(
                estado="PDF_LEGIBLE",
                observaciones=[
                    "PDF abierto y texto extraído de una muestra de páginas.",
                    "No se ha acreditado que los anexos estén completos ni que la norma esté vigente.",
                ],
            )
    except (RuntimeError, ValueError, fitz.FileDataError) as exc:
        registro.update(
            estado="ERROR",
            observaciones=["No se ha podido leer este PDF: " + type(exc).__name__],
        )
    return registro
