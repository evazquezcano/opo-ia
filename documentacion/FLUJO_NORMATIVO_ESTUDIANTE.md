# OPO-IA · Aportación y tratamiento de normativa por el estudiante

## Decisión de diseño (30 de octubre de 2026)

La actualización del currículo autonómico es un objetivo formativo del curso. Por ello, el estudiante debe localizar en la publicación oficial la normativa que considera aplicable, consultar sus modificaciones o correcciones y aportar la documentación. OPO-IA **no sustituye** esta búsqueda por un catálogo de documentos supuestamente siempre vigentes.

## Archivos y función diferenciada

| Espacio | Tipo de archivo | Obligatorio | Uso previsto |
|---|---|---|---|
| 1 | Decreto curricular y anexos de la etapa | Sí | Objetivos de etapa, competencias específicas, criterios de evaluación, saberes o contenidos y descriptores que procedan |
| 2 | Modificación o corrección curricular 1 | No | Revisar artículos y anexos afectados |
| 3 | Modificación o corrección curricular 2 | No | Revisar artículos y anexos afectados |
| 4 | Modificación o corrección curricular 3 | No | Revisar artículos y anexos afectados |
| 5 | Orden o decreto de evaluación | No | Determinar si regula técnicas, procedimientos, instrumentos, documentos o decisiones de evaluación |

Cada entrada puede incluir un enlace a su publicación oficial. Se consigna la fecha de consulta y la comunidad, etapa, curso y materia. No basta con la fecha ni con un enlace para certificar la vigencia: la correspondencia jurídica requiere revisión de las disposiciones.

La limitación a tres modificaciones es **un parámetro de interfaz**, no una afirmación de que las normas nunca acumulen más de tres cambios. Si existen otras modificaciones o si los anexos aparecen en documentos separados, antes de generar una programación definitiva se deberá ampliar la documentación aportada.

## Tratamiento de fuentes

1. La fuente curricular principal se usa como texto de referencia.
2. Las modificaciones se analizan por el artículo, anexo, materia y curso que efectivamente alteran. No se concatenan indiscriminadamente: una modificación puede sustituir, añadir o suprimir un fragmento.
3. La normativa de evaluación se examina por separado. No modifica por defecto la redacción ni el código de los criterios curriculares. Si su contenido modifica explícitamente el currículo, se revisa el alcance jurídico real.
4. Los elementos curriculares extraídos conservarán su redacción y sus códigos oficiales. Los códigos internos que introduzca el planificador deberán identificarse como tales.
5. OPO-IA comprobará después la cobertura **conjunta** de las UD y SA de la programación.

## Implementado ahora

- Interfaz Streamlit con las cuatro pestañas previstas (solo la primera es funcional).
- Carga de 1 PDF principal, 0–3 PDF de cambios y 0–1 PDF de evaluación.
- Reconocimiento técnico de cabecera PDF, límite de tamaño, contraseña, número de páginas y extracción de muestras de texto.
- Advertencia específica para PDF posiblemente escaneados.
- Registro de nombres, huella SHA-256, paginación, tipo documental, enlaces y observaciones.
- Ficha JSON descargable por el estudiante, sin contenido original de los PDF y sin su dirección de correo.
- Bloqueo expreso de la generación curricular definitiva.

## Pendiente

- Verificación automática fiable de referencias normativas, vigencia y alcance de modificaciones.
- Tratamiento de decretos cuyos anexos se publican en PDF separados, y normativa con más de tres cambios.
- OCR para archivos escaneados.
- Extracción íntegra por materia y curso y cotejo de todos los elementos.
- Planificación, comprobación de cobertura y exportación a Word/PDF.
- Identidad institucional definitiva y despliegue público de la aplicación.

## Privacidad y acceso

El prototipo examina los archivos **en memoria**. No escribe PDF aportados por estudiantes en el repositorio, disco de aplicación o base de datos. Streamlit recibe los PDF en el servidor de alojamiento para procesarlos. La aplicación no controla las políticas de registros o conservación técnica del proveedor.

El filtro por el sufijo \`@alumno.uned.es\` solo verifica el formato que declara quien accede: **no autentica la identidad**. Para restringir efectivamente el uso a estudiantes matriculados se necesitaría autenticación institucional.

## Fuentes de referencia

- Normativa educativa: https://blogs.uned.es/futurodocente/normativa/
- Recursos para el profesorado: https://blogs.uned.es/futurodocente/recursos/
- Documentación oficial de Streamlit: https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
