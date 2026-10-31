# OPO-IA — Lectura curricular en navegador y simplificación de la pantalla (31/10/2026)

## Cambios solicitados y ejecutados

- Entrada: el estudiante escribe su correo institucional UNED en el campo **«Contraseña»**, que permanece enmascarado. Se añade un botón accesible para mostrarlo u ocultarlo, sin revelar la pauta en la pantalla. **No constituye un sistema de autenticación segura**.
- Currículo: únicamente se muestra la carga **obligatoria** del PDF curricular autonómico o, en el ámbito de gestión ministerial de Ceuta y Melilla, su orden curricular. Se retiran de esta interfaz los formularios de modificaciones y normativa de evaluación.
- Se mantienen como **opcionales** la resolución de convocatoria de oposiciones y las rúbricas/listas de cotejo, cuya función no debe confundirse con los criterios curriculares.
- Se corrigió la construcción incorrecta del identificador HTML de `normAnalyze`, que impedía registrar el evento de pulsación del botón de lectura. Antes figuraba `id="normAnalyze ${...}` y ahora `id="normAnalyze" ${...}`.
- Tras cargar el PDF y pulsar «Examinar» se analiza su texto mediante PDF.js dentro del navegador. Se producen indicios por página y se enumeran candidatos de competencias, criterios, contenidos o saberes, bloques, objetivos, descriptores y elementos transversales, conservando el texto reconocido, su código candidato y página del PDF.
- Se agregó la posibilidad de detectar saberes con enumeración por guiones sin asignarles códigos oficiales ficticios; especialmente pertinente para decretos que no codifican cada contenido.
- Cobertura: se ofrecen indicadores de candidatos reconocidos, sin falsificar porcentajes ni checks verdes. La generación de UD/SA, Word y PDF sigue pendiente de verificar la extracción y las plantillas.
- El CSS y las cinco imágenes originales se conservan intactos. `web/referencia-original.html` **no se altera**.

## Límite importante de la extracción

La extracción **ya se ejecuta bajo demanda** cuando el usuario pulsa el botón tras subir el PDF, pero por ahora es una **recuperación preliminar de candidatos textuales**, no una transcripción oficial completa ni una certificación de vigencia. El esquema de numeración de Madrid (por ejemplo criterios `1.1.`) está contemplado, así como la búsqueda de encabezados de materia y curso. Si una sección tiene un formato distinto, es escaneada o el parser no la reconoce, aparecerá como no identificada. Podría mezclar elementos de otros cursos o materias y los candidatos requieren cotejo y revisión. No se puede afirmar que todos los elementos hayan sido extraídos.

PDF.js se descarga en el navegador desde un CDN al usar el lector. Si el navegador no tiene acceso a Internet o está bloqueado, se informa del fallo. Los PDF aportados no se envían deliberadamente a un servidor de OPO-IA; el procesamiento se efectúa en el navegador.

## Verificaciones y recuperación

- La prueba en Chromium con archivo sintético y sustituto controlado de PDF.js comprueba el botón de visualización de contraseña, acceso, selección del PDF, extracción de códigos `1.1` y paso a Cobertura.
- No se ha probado el **PDF exacto de Madrid que el estudiante utilizó**, que no estaba disponible como archivo en el proyecto; no se debe afirmar que todas sus secciones queden correctamente extraídas.
- Las pruebas automáticas de identidad visual de GitHub Actions incluyen comprobación de CSS, logos y sintaxis JavaScript.
- Código de la interfaz: `web/index.html` (archivo definitivo de esta revisión en GitHub).
- Original visual intacto: `web/referencia-original.html`.
- Paquete de recuperación distribuido al usuario: `OPO-IA_revision_31-10-2026.zip`, que contiene nuevo HTML, original y notas.

## Próximo trabajo

1. Validar la extracción con varios **PDF oficiales reales y completos** de Madrid y otras comunidades, y comprobar la delimitación exacta de materia/curso y la captación de todos los elementos, incluidos los repartidos en páginas contiguas.
2. Corregir heurísticas falsas y desarrollar la revisión literal por conjuntos, manteniendo el aviso de incertidumbre cuando no sea posible certificar integridad.
3. Integrar la comprobación opcional de requisitos formales de convocatoria y rúbricas.
4. Con las plantillas de UD/SA aportadas por el responsable, generar la primera tabla Word/PDF para inspección antes del lote completo; después calcular la cobertura curricular conjunta de todas las UD y SA.

**Nota histórica:** `documentacion/FLUJO_NORMATIVO_ESTUDIANTE.md` recoge una fase anterior en la que se plantearon documentos opcionales de modificación/evaluación. Para la interfaz actual debe prevalecer esta especificación fechada el **31/10/2026**.
