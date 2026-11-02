# NORMA-IA — MEMORIA MAESTRA DE CONTINUIDAD Y RESTAURACIÓN

**Fecha de corte documental:** 2 de noviembre de 2026.  
**Proyecto:** GENERADORES OPO_IA.  
**Herramienta:** NORMA-IA · Generador de normativa básica y complementaria para programaciones docentes.  
**Repositorio operativo:** https://github.com/evazquezcano/opo-ia  
**Rama:** main.  
**Interfaz actual:** `web/norma-ia/index.html`.  
**Generador anterior protegido:** `web/index.html`.  
**Referencia de diseño anterior protegida:** `web/referencia-original.html`.  
**Informe jurídico territorial:** `documentacion/NORMA_IA_AUDITORIA_JURIDICA_2026-11-02.md`.  
**Matriz jurídica por referencia y ámbito:** `documentacion/NORMA_IA_MANIFIESTO_FUENTES_2026-11-02.json`.  
**Registro histórico de especificaciones y decisiones:** `documentacion/NORMA_IA_ESPECIFICACION_2026-11-02.md`.  
**Pruebas:** `web/norma-ia/test-check.cjs`.  
**Publicación:** `.github/workflows/publicar-herramientas.yml`.  
**Control de integridad:** `.github/workflows/norma-ia-integridad.yml`.

## 1. Instrucción de continuidad prioritaria

La memoria se entrega para poder continuar la elaboración de NORMA-IA en otra conversación sin reconstruir decisiones. **Antes de modificar nada, comprobar el estado real del repositorio, leer esta memoria, el manifiesto de fuentes, el registro histórico y el HTML vigente.** El repositorio prevalece sobre las descripciones históricas si se han producido cambios posteriores. No alterar el generador curricular OPO-IA ni su referencia visual. Conservar los tres logotipos institucionales, los colores y la maquetación aprobados. No presentar una referencia como jurídicamente validada por el solo hecho de que se haya identificado una publicación o de que una URL responda.

## 2. Propósito exacto

Generador web sencillo, preferentemente en una sola página, destinado al alumnado que prepara oposiciones docentes. El usuario selecciona uno de los 17 territorios autonómicos o el ámbito del Ministerio (Ceuta y Melilla) y una de tres etapas: Primaria, ESO o Bachillerato. La aplicación ofrece solo dos bloques de normativa:
- **Normativa básica**, destinada al epígrafe inicial de la programación didáctica.
- **Normativa complementaria**, destinada a las referencias finales y a fundamentar apartados posteriores de la programación: evaluación, organización, inclusión, convivencia, optativas, metodología y demás regulación aplicable.

La selección debe corresponder a normas pertinentes y vigentes en el territorio, etapa y, cuando proceda, tipo de centro. No es suficiente con enumerar toda norma históricamente publicada.

## 3. Datos de entrada y flujo

- Selector de comunidad/autonomía y ámbito explícito del Ministerio, Ceuta y Melilla.
- Etapa educativa: Educación Primaria, Educación Secundaria Obligatoria, Bachillerato.
- La subida de convocatoria de oposiciones **es opcional**, igual que el enlace oficial. La herramienta debe producir resultados sin ambos. Actualmente estos documentos se registran solo como referencia declarativa; **no se interpretan automáticamente ni modifican la selección normativa**.
- Pantalla inicial con acceso de apariencia institucional UNED. Campo «Contraseña» con icono de ojo accesible para mostrar/ocultar. Filtro de formato del correo `@alumno.uned.es`; no es autenticación real. Evitar conservar correo o archivos.
- Tras acceder, formulario sencillo; al consultar, resultados en pantalla en orden básico → complementario, cada norma con rango, año, título completo y enlace a su disposición individual.
- Exportación a Word editable DOCX y PDF (mediante impresión del navegador). Fuente Times New Roman 12, interlineado sencillo, texto justificado, A4, referencias jurídicas adaptadas a APA 7. No se ha certificado cumplimiento APA 7 norma a norma ni realizado prueba real final en navegador de ambos formatos.
- Un único enlace al PDF original del directorio de portales oficiales, no dos cajones de accesos independientes. Documento: https://drive.google.com/file/d/1tXqvzFR6vMdVxGmNcdtSDeaH-CJpp6kO/view?usp=sharing.
- Fuentes generales del proyecto: https://blogs.uned.es/futurodocente/normativa/ y https://blogs.uned.es/futurodocente/recursos/.

## 4. Diseño y arquitectura

Aplicación HTML/CSS/JS autocontenida en `web/norma-ia/index.html`, en el mismo repositorio que el primer generador pero en ruta independiente. Cabecera «UNED · Futuro Docente / OPO-IA», marca NORMA-IA, tres logos institucionales embebidos WebP, portada institucional verde, dos tarjetas de acceso y sistema visual similar al generador anterior. Biblioteca externa docx.js para descargar documentos editables; PDF mediante hoja de impresión (guardar como PDF); no backend de consulta jurídica, ni base de datos, ni autenticación real. Los PDF de convocatoria no se envían deliberadamente a un servidor, y la aplicación no ejecuta extracción.

## 5. Reglas jurídicas acordadas

1. Mostrar «Ley Orgánica», «Real Decreto», «Decreto», «Decreto Foral», «Decret», «Orden», «Orden Foral», «Resolución», «Instrucciones», etc. y año, nunca el código interno («O1994S», «D65»).
2. Citar LOMLOE (Ley Orgánica 3/2020). No duplicar la LOE como entrada separada, conforme a la decisión editorial del usuario, aunque debe reconocerse que la Ley Orgánica 2/2006 modificada sigue siendo la norma de educación vigente.
3. No listar los reales decretos estatales de enseñanzas mínimas 157/2022, 217/2022 y 243/2022 como referencias autónomas en las 17 selecciones autonómicas; sí en el ámbito ministerial cuando corresponda a la etapa.
4. No listar las órdenes generales estatales de junio de 1994 en ninguna selección.
5. Aplicación supletoria del RD 83/1996: solo cuando una norma autonómica de organización no desplace su aplicación y en los extremos pertinentes. El artículo adicional primero del propio RD indica esa supletoriedad. Los casos no resueltos deben marcarse «pendiente de comprobación», nunca «vigencia autonómica certificada».
6. Priorizar enlaces **individuales** a BOE, boletines autonómicos y registros oficiales de normativa consolidada; no enlazar simplemente un portal general cuando se pueda enlazar la disposición.
7. Para normas modificadas, atender a la modificación efectiva y a las disposiciones transitorias y derogatorias; las instrucciones de inicio de curso deben corresponder al curso de referencia.
8. Las categorías mínimas de auditoría: currículo; desarrollo organizativo y funcional/reglamento orgánico; evaluación y promoción/titulación; inclusión/atención a las diferencias individuales; convivencia; instrucciones anuales; normas de oferta optativa/programas u otros apartados relevantes; correcciones, sustituciones y derogaciones.
9. Conservar incertidumbre explícita. Una norma identificada no demuestra que todos sus artículos estén vigentes ni que el repertorio de una comunidad esté completo.

## 6. Estado de la auditoría jurídica del 02/11/2026

**El proyecto NO tiene certificación jurídica integral.** El manifiesto guardado contiene **129 entradas normativas** extraídas del código y una matriz de **60 selecciones territoriales/etapa** (51 autonómicas más 9 del ámbito del Ministerio/Ceuta/Melilla). Se han identificado disposiciones curriculares principales para 17 autonomías × 3 etapas y al menos una complementaria por selección. **Solo un subconjunto de publicaciones tiene contraste individual de identidad y publicación; no existe un expediente documental de vigencia exhaustiva para las 129 entradas**. El manifiesto etiqueta explícitamente las demás como pendientes de cotejo.

Hallazgos verificados especialmente relevantes:
- RD 83/1996: disposición adicional primera reconoce su supletoriedad cuando no existe normativa propia; su aplicación no puede extrapolarse automáticamente.
- Navarra: Decreto Foral 14/2026 sustituye los viejos reglamentos de 1997; Orden Foral 36/2026 regula Primaria; Orden Foral 40/2026 ESO y Bachillerato.
- Illes Balears: decretos de currículo 41, 42 y 43/2025 sustituyen los de 2022; reglamento orgánico propio Decret 4/2023.
- Galicia: reglamentos orgánicos autonómicos Decretos 374/1996 (Primaria) y 324/1996 (Secundaria), con afectaciones posteriores.
- Andalucía: reglamentos orgánicos Decretos 328/2010 y 327/2010; órdenes de currículo y evaluación de 30/05/2023, sujetas a modificaciones posteriores.
- Canarias: reglamento orgánico 81/2010 y currículo de ESO y Bachillerato en un mismo Decreto 30/2023.
- Castilla-La Mancha: Decreto 82/2022 de ESO modificado por Decreto 31/2024 y Decreto 83/2022 de Bachillerato modificado por Decreto 19/2024; órdenes de funcionamiento 118/2022 y 121/2022.
- Cataluña: Decret 175/2022 de educación básica modificado por Decret 480/2024; Decret 171/2022 de Bachillerato modificado además por Decret 103/2026 (DOGC 9704, 09/07/2026).
- La Rioja: Decreto 42/2022 de ESO y Decreto 43/2022 de Bachillerato modificados por Decreto 30/2025 (BOR 126, 03/07/2025); nuevo Decreto 43/2025 inclusión y normativa de convivencia y PADI de 2025.
- Comunitat Valenciana: deben analizarse conjuntamente el Decreto 96/2026 (Primaria, modifica 106/2022), el 66/2024 (ESO, modifica 107/2022) y el 103/2026 (Bachillerato, modifica 108/2022). **No están todos los textos de modificación incorporados en el listado exportable**, por lo que hay advertencia expresa de selección provisional. Distinguir el Decreto 103/2026 valenciano (26 de junio) del Decret 103/2026 catalán (7 de julio).
- Ministerial: Orden EFP/678/2022 para Primaria, EFP/754/2022 ESO, EFP/755/2022 Bachillerato y sus RD de mínimos correspondientes. La Orden EFP/755/2022 está modificada por la EFP/824/2023 según análisis consolidado del BOE.

**Pendencias de auditoría**: cotejo individual y fechado de las 129 referencias; comprobación oficial de cada URL, rango, fecha y título literal; exhaustividad de evaluación/inclusión/convivencia/organización/instrucciones en cada una de las 51 combinaciones; supletoriedad del RD 83/1996; correcciones y derogaciones; condiciones de titularidad y especialidad; efectos de cambios 2026. No confundir la cobertura técnica de selectores con la jurídica.

## 7. Verificaciones técnicas, despliegue y alertas

- Tests de `web/norma-ia/test-check.cjs`: 20 comprobaciones reproducidas en entorno JavaScript simulado sobre acceso, tres logotipos, 20 ámbitos (17 + Ceuta/Melilla + selector ministerial), tres etapas, consulta sin convocatoria, normas excluidas, Word/PDF, revisión territorial y ROC autonómicos. Estas pruebas no equivalen a pruebas visuales ni a auditoría jurídica.
- GitHub Pages Source se configuró manualmente a «GitHub Actions» por el propietario, comprobado mediante captura.
- Workflow `.github/workflows/publicar-herramientas.yml`: empaqueta `web/index.html` como página anterior y `web/norma-ia/index.html` como aplicación NORMA-IA. Página prevista https://evazquezcano.github.io/opo-ia/web/norma-ia/.
- **Incidencia detectada y corregida el 02/11/2026:** las primeras ejecuciones de Pages e integridad fallaban porque una aserción conservaba el texto antiguo «Documento incompleto» y la aplicación ya decía «Repertorio en revisión jurídica». Se actualizó la aserción (commit 89bbec00a4a23aa140d4de28e9d0bd5676b7f575). **Verificación posterior:** GitHub Actions confirmó éxito del control de integridad [ejecución 41515214305](https://github.com/evazquezcano/opo-ia/actions/runs/41515214305) y de la publicación [ejecución 41515214303](https://github.com/evazquezcano/opo-ia/actions/runs/41515214303). La consulta externa desde el navegador del usuario sigue pendiente; el servicio de consulta web de esta sesión no pudo abrir el dominio de Pages.
- El enlace de previsualización raw.githack mostró una advertencia intermedia del proxy; no se desea utilizarlo como enlace definitivo.
- No afirmar accesibilidad pública del sitio si no se ha contrastado la ejecución de Pages.
- No se han validado aún las descargas DOCX y PDF en un navegador real, ni su conformidad editorial/visual completa.

## 8. Copia de seguridad y metodología de trabajo

El código fuente vive en GitHub, no solo en la memoria de una conversación. El usuario solicitó expresamente respaldar la totalidad del proyecto: conservar HTML, tests, workflows, memoria, manifiesto normativo, fuentes y decisiones. La instantánea de continuidad se guardará en una rama de archivo propia tras incorporar este documento y el informe jurídico. Consultar la rama `archivo/norma-ia-2026-11-02` cuando esté confirmada en GitHub. El PDF original de portales figura también como adjunto original de la conversación y está enlazado desde la aplicación.

**Bucle obligatorio para futuras sesiones:** identificar la siguiente tarea → consultar fuentes oficiales → modificar UNA parte → pruebas de sintaxis y comportamiento → corregir fallos → ejecutar y verificar GitHub Actions → comprobar sitio → actualizar matriz legal y memoria maestra → continuar. Realizar directamente las operaciones de GitHub cuando sea posible; solicitar intervención humana únicamente ante decisión fundamental o control externo imposible de ejecutar. No trabajar de modo asíncrono sin una automatización explícita.

**Regla de cierre:** NORMA-IA solo se podrá presentar como proyecto jurídicamente cerrado cuando las 51 combinaciones autonómicas y el ámbito ministerial cuenten con inventario exhaustivo, cotejado y vigente con fuentes oficiales, los documentos Word y PDF hayan sido probados, los hipervínculos sean correctos y el despliegue público esté comprobado.
