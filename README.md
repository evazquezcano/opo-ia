# OPO-IA

**Generador de unidades didácticas y situaciones de aprendizaje para programaciones docentes.** Proyecto de formación asociado a RADTE y Futuro Docente (UNED).

## Interfaz HTML aprobada

**El diseño que debe utilizarse es [web/index.html](web/index.html)**, una ampliación del [HTML original aprobado](web/referencia-original.html). Ambos conservan los mismos logotipos incrustados, colores y disposición institucional. La versión integrada mantiene cuatro pasos: Currículo, Planificación, Cobertura y Documentos.

La pestaña Currículo permite aportar una norma curricular principal obligatoria, hasta tres modificaciones relevantes opcionales y normativa de evaluación opcional. El estudiante debe localizar las disposiciones oficiales aplicables a su etapa, curso y materia.

**Estado de la extracción:** el HTML incorporado utiliza PDF.js (biblioteca cargada desde CDN al iniciar la lectura) para procesar los PDF en el navegador y localizar páginas y extractos preliminares. Esta función **no equivale** a extraer y validar literalmente todos los elementos del currículo, ni puede verificar por sí sola la vigencia o aplicar modificaciones normativas. Hasta que se completen esas fases, la generación definitiva permanece desactivada.

El programa [app.py](app.py) es una prueba técnica de lectura documental con Streamlit. **No es la interfaz visual aprobada**; cualquier integración futura deberá conservar la apariencia de `web/index.html` y el archivo original de referencia.

## Estado del proyecto

**Prototipo en desarrollo.** La pestaña «Currículo» permite cargar el decreto curricular oficial, hasta tres modificaciones y una norma de evaluación. Las pestañas «Planificación», «Cobertura» y «Documentos» todavía no realizan sus funciones definitivas. El análisis de PDF es técnico y preliminar: **no certifica la vigencia normativa ni autoriza generar programaciones**.

La búsqueda de la norma y de sus posibles modificaciones corresponde al estudiante como actividad formativa del curso. El catálogo autonómico del repositorio sirve de referencia, pero no sustituye la búsqueda y verificación de las disposiciones vigentes.

## Ejecutar el prototipo con Python

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá una interfaz con cuatro pestañas. Para el acceso inicial se solicita un correo terminado en `@alumno.uned.es`; este es exclusivamente un filtro de formato, **no una autenticación**.

## Carga documental

- Decreto curricular principal (PDF obligatorio).
- Hasta tres modificaciones o correcciones curriculares (PDF opcionales).
- Orden o decreto de evaluación (PDF opcional y analizado por separado).

Los PDF se examinan en memoria y no se guardan en el repositorio. Se puede descargar una ficha JSON de procedencia y comprobaciones técnicas. Actualmente no se extrae todavía un currículo completo a partir de los documentos aportados.

## Fuentes y protocolos

- [Flujo normativo del estudiante](documentacion/FLUJO_NORMATIVO_ESTUDIANTE.md)
- [Protocolo de validación curricular](documentacion/PROTOCOLO_CURRICULAR.md)
- [Informe documental previo](datos/ESTADO_DOCUMENTAL.md)
- [Normativa educativa de Futuro Docente](https://blogs.uned.es/futurodocente/normativa/)
- [Recursos para el profesorado](https://blogs.uned.es/futurodocente/recursos/)

## Privacidad

No hay almacenamiento deliberado de documentos subidos, correos ni información personal en archivos locales o GitHub. El procesamiento de los PDF requiere enviarlos desde el navegador al servidor Streamlit; los registros y políticas del alojamiento quedan fuera del código de esta aplicación.
