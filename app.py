"""OPO-IA · Primera versión de interfaz docente.

La pestaña Currículo es operativa para cargar y examinar PDFs.
La extracción jurídica y la generación de programaciones aún no están activadas.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from urllib.parse import urlparse

import streamlit as st

from opoia.fuentes import analizar_pdf, url_normativa_valida
from opoia.extraccion import indexar_documento, consolidar_evidencias

st.set_page_config(
    page_title="OPO-IA · Programaciones docentes",
    page_icon="📚",
    layout="wide",
)

COMUNIDADES = [
    "Andalucía", "Aragón", "Principado de Asturias", "Illes Balears",
    "Canarias", "Cantabria", "Castilla-La Mancha", "Castilla y León",
    "Cataluña", "Comunitat Valenciana", "Extremadura", "Galicia",
    "Comunidad de Madrid", "Región de Murcia", "Comunidad Foral de Navarra",
    "País Vasco", "La Rioja", "Ceuta", "Melilla",
]
CURSOS = {
    "Educación Primaria": [f"{n}.º" for n in range(1, 7)],
    "Educación Secundaria Obligatoria": [f"{n}.º" for n in range(1, 5)],
    "Bachillerato": ["1.º", "2.º"],
}

st.title("OPO-IA")
st.caption("Generador de unidades didácticas y situaciones de aprendizaje · RADTE · Futuro Docente")

with st.sidebar:
    st.header("Acceso al prototipo")
    correo = st.text_input(
        "Correo del alumnado UNED",
        placeholder="usuario@alumno.uned.es",
        help="Filtro de formato, no es un sistema de autenticación.",
    ).strip().lower()
    st.caption("El correo solo se comprueba durante esta sesión. No se guarda en el repositorio.")
    st.markdown(
        "[Normativa docente · Futuro Docente]"
        "(https://blogs.uned.es/futurodocente/normativa/)"
    )
    st.markdown(
        "[Recursos didácticos · Futuro Docente]"
        "(https://blogs.uned.es/futurodocente/recursos/)"
    )

if not correo.endswith("@alumno.uned.es") or correo == "@alumno.uned.es":
    st.info(
        "Introduce un correo con terminación @alumno.uned.es para acceder al prototipo. "
        "Este filtro no comprueba la identidad ni la matrícula."
    )
    st.stop()

tab_curriculo, tab_planificacion, tab_cobertura, tab_documentos = st.tabs(
    ["1. Currículo", "2. Planificación", "3. Cobertura", "4. Documentos"]
)

with tab_curriculo:
    st.subheader("Localización y aportación de la normativa")
    st.write(
        "Como parte del curso, debes localizar el decreto curricular oficial "
        "de tu comunidad y etapa, comprobar las modificaciones posteriores "
        "y aportar los documentos que correspondan. OPO-IA no presume que "
        "una norma descargada anteriormente continúe vigente."
    )
    st.info(
        "Solo es obligatorio el documento curricular principal. Los PDF adicionales "
        "no son necesarios si no hay modificaciones que afecten a los elementos "
        "curriculares utilizados en la programación."
    )
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        comunidad = st.selectbox("Comunidad autónoma o ciudad autónoma", COMUNIDADES)
    with c2:
        etapa = st.selectbox("Etapa", list(CURSOS))
    with c3:
        curso = st.selectbox("Curso", CURSOS[etapa])
    materia = st.text_input(
        "Materia o área",
        placeholder="Ej.: Lengua Castellana y Literatura",
    )
    fecha_consulta = st.date_input(
        "Fecha en que has consultado la normativa",
        value=date.today(),
        help="Fecha declarada de consulta; no constituye una certificación de vigencia.",
    )
    gestion_ministerial = comunidad in ("Ceuta", "Melilla")
    referencias_ministeriales = {
        "Educación Primaria": ("Orden EFP/678/2022", "https://www.boe.es/eli/es/o/2022/07/15/efp678"),
        "Educación Secundaria Obligatoria": ("Orden EFP/754/2022", "https://www.boe.es/eli/es/o/2022/07/28/efp754"),
        "Bachillerato": ("Orden EFP/755/2022", "https://www.boe.es/eli/es/o/2022/07/31/efp755"),
    }
    st.markdown("#### 1. Norma curricular principal — obligatoria")
    if gestion_ministerial:
        nombre_orden, enlace_orden = referencias_ministeriales[etapa]
        st.warning(
            f"En Ceuta y Melilla el real decreto establece las enseñanzas mínimas, "
            f"pero el currículo completo de {etapa} se regula mediante la "
            f"{nombre_orden}. Para extraer los contenidos autonómicos o ministeriales "
            "de la materia, aporta esta orden con sus anexos. "
            "El real decreto estatal por sí solo podría resultar insuficiente."
        )
        st.markdown(f"[Consultar el currículo ministerial en el BOE]({enlace_orden})")
        etiqueta_principal = "Real decreto u orden ministerial curricular (PDF)"
    else:
        st.caption(
            "Aporta el decreto curricular de tu comunidad autónoma con sus "
            "anexos completos. No se requieren otros documentos si no existe "
            "una modificación curricular que afecte a la materia."
        )
        etiqueta_principal = "Decreto curricular autonómico (PDF)"

    principal = st.file_uploader(
        etiqueta_principal,
        type=["pdf"],
        max_upload_size=35,
        key="pdf_curriculo",
    )
    url_principal = st.text_input(
        "Enlace a la publicación oficial del currículo",
        placeholder="https://…",
        key="url_curriculo",
    )

    modificaciones = []
    with st.expander("2. Modificaciones curriculares — opcionales (hasta tres PDF)", expanded=False):
        st.info(
            "**No necesitas adjuntar ningún documento adicional si no existe "
            "una modificación oficial que afecte a la programación.** "
            "Aporta una modificación o corrección únicamente si altera "
            "competencias específicas, objetivos de etapa, criterios de evaluación, "
            "descriptores operativos, bloques de contenido, saberes básicos "
            "o elementos transversales de la etapa, curso o materia."
        )
        st.caption(
            "Los tres espacios pueden quedar vacíos. Si hay más de tres modificaciones "
            "aplicables, deben revisarse todas, aunque requieran ampliar las cargas."
        )
        for numero in range(1, 4):
            st.markdown(f"**Modificación o corrección {numero}**")
            archivo = st.file_uploader(
                f"PDF de la modificación {numero}",
                type=["pdf"], max_upload_size=35,
                key=f"pdf_modificacion_{numero}",
            )
            enlace = st.text_input(
                f"Enlace oficial de la modificación {numero}",
                placeholder="https://…",
                key=f"url_modificacion_{numero}",
            )
            modificaciones.append((numero, archivo, enlace))

    with st.expander("3. Orden o decreto de evaluación — opcional", expanded=False):
        st.info(
            "**No es necesario aportar una orden o decreto de evaluación "
            "para desarrollar la programación didáctica.** Puedes adjuntarlo "
            "solo si deseas consultar aspectos específicos de evaluación "
            "regulados en esa disposición. No sustituye ni modifica por defecto "
            "los criterios de evaluación del currículo."
        )
        evaluacion = st.file_uploader(
            "Orden o decreto de evaluación (PDF)",
            type=["pdf"], max_upload_size=35,
            key="pdf_evaluacion",
        )
        url_evaluacion = st.text_input(
            "Enlace oficial de la normativa de evaluación",
            placeholder="https://…",
            key="url_evaluacion",
        )

    st.markdown("#### 4. Comprobación preliminar de los archivos")
    st.warning(
        "Leer un PDF y reconocer términos curriculares no demuestra que esté vigente, "
        "que contenga todos los anexos ni que corresponda exactamente a la materia. "
        "La revisión jurídica y curricular completa se realizará en fases posteriores."
    )

    entradas = [("Currículo principal", principal, url_principal)] if principal else []
    for numero, archivo, enlace in modificaciones:
        if archivo is not None:
            entradas.append((f"Modificación {numero}", archivo, enlace))
    if evaluacion is not None:
        entradas.append(("Normativa de evaluación", evaluacion, url_evaluacion))

    # La firma se calcula en memoria y evita reutilizar resultados de archivos cambiados.
    firma = hashlib.sha256()
    for valor in (comunidad, etapa, curso, materia, str(fecha_consulta)):
        firma.update(valor.encode("utf-8"))
        firma.update(b"\0")
    for funcion, archivo, enlace in entradas:
        firma.update(funcion.encode("utf-8"))
        firma.update(archivo.getvalue())
        firma.update(enlace.strip().encode("utf-8"))
    firma_actual = firma.hexdigest()

    if st.button(
        "Examinar la documentación aportada",
        type="primary",
        disabled=not bool(principal) or not materia.strip(),
    ):
        resultados = []
        for funcion, archivo, enlace in entradas:
            registro = analizar_pdf(archivo.getvalue(), archivo.name, funcion)
            registro["url_publicacion"] = enlace.strip()
            registro["enlace_con_formato_valido"] = url_normativa_valida(enlace)
            if not enlace.strip():
                registro["observaciones"].append(
                    "Falta registrar el enlace a la publicación normativa."
                )
            elif not registro["enlace_con_formato_valido"]:
                registro["observaciones"].append(
                    "El enlace indicado no tiene formato de URL HTTP(S)."
                )
            resultados.append(registro)

        ficha = {
            "comunidad_autonoma": comunidad,
            "etapa": etapa,
            "curso": curso,
            "materia": materia.strip(),
            "fecha_consulta_declarada": fecha_consulta.isoformat(),
            "documentos": resultados,
            "estado": "PRELIMINAR_SIN_VALIDACION_NORMATIVA",
            "curriculo_habilitado": False,
            "observacion": (
                "No certifica vigencia, anexos completos, literalidad ni cobertura "
                "curricular. Se requiere validación antes de generar."
            ),
        }
        st.session_state["ficha_fuentes"] = ficha
        st.session_state["firma_fuentes"] = firma_actual

    if st.session_state.get("firma_fuentes") == firma_actual:
        ficha = st.session_state["ficha_fuentes"]
        documentos = ficha["documentos"]
        st.markdown("#### Resultado de la lectura documental")
        st.table([
            {
                "Función": doc["funcion_documental"],
                "Archivo": doc["archivo"],
                "Páginas": doc["paginas"] or "—",
                "Lectura": doc["estado"],
                "Indicios en la muestra": ", ".join(doc["indicios_textuales"]) or "Sin coincidencias",
            }
            for doc in documentos
        ])
        for doc in documentos:
            for aviso in doc["observaciones"]:
                if doc["estado"] == "ERROR":
                    st.error(f"{doc['funcion_documental']}: {aviso}")
                else:
                    st.caption(f"{doc['funcion_documental']}: {aviso}")
        if all(doc["estado"] == "PDF_LEGIBLE" for doc in documentos):
            st.info(
                "Los archivos han superado la lectura técnica inicial. "
                "Faltan verificar su correspondencia normativa, su vigencia y sus anexos."
            )
        else:
            st.warning(
                "Algún documento requiere revisión técnica antes de intentar "
                "la extracción curricular."
            )
        st.download_button(
            "Descargar ficha documental (JSON)",
            data=json.dumps(ficha, ensure_ascii=False, indent=2),
            file_name="opo-ia-ficha-normativa.json",
            mime="application/json",
            help="Solo descarga metadatos; no contiene el contenido de los PDF ni el correo del estudiante.",
        )
    elif "ficha_fuentes" in st.session_state:
        st.info("Los documentos o datos han cambiado. Examínalos de nuevo para actualizar el resultado.")

    if not principal:
        st.caption("Para analizar los archivos, adjunta el decreto curricular principal.")
    elif not materia.strip():
        st.caption("Escribe la materia o área para continuar.")

with tab_planificacion:
    st.info(
        "Esta pestaña se conectará después con la extracción y revisión de los "
        "criterios y saberes del currículo. Todavía no genera unidades didácticas "
        "ni situaciones de aprendizaje."
    )

with tab_cobertura:
    st.info(
        "La comprobación de cobertura global se activará cuando estén identificados "
        "y verificados los criterios, competencias y saberes aplicables a la materia."
    )

with tab_documentos:
    st.info(
        "La exportación de las tablas de UD y SA a Word/PDF se implementará cuando "
        "la planificación y la comprobación de cobertura estén completas."
    )

st.divider()
st.caption(
    "OPO-IA · Prototipo docente. Los PDF se procesan en memoria durante la sesión; "
    "este código no los almacena en GitHub, bases de datos ni archivos del servidor. "
    "El alojamiento puede conservar registros técnicos sujetos a sus propias políticas."
)
