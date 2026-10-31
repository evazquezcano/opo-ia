# OPO-IA — MEMORIA MAESTRA DE CONTINUIDAD Y RESGUARDO

**Fecha de corte:** 31 de octubre de 2026. **Proyecto:** GENERADORES OPO_IA. **Subproyecto activo:** generador de unidades didácticas (UD) y situaciones de aprendizaje (SA) para programaciones docentes. **Chat de continuación:** «Generador 2». No confundir con el desarrollo ulterior del segundo generador de actividades y tareas DUA.

## 1. PUNTO DE REANUDACIÓN INEQUÍVOCO

La versión vigente y de referencia para TODAS las próximas modificaciones es:

`01_VERSION_ACTUAL/OPO-IA_planificador_simplificado_informe_final_2026-10-31.html`

**No** partir del anterior HTML `web/index.html` del repositorio sin incorporar esta versión: la versión actual se ha guardado por separado bajo `/respaldo/2026-10-31/`, sin sobrescribir el frontend público anterior. Esta copia es el punto de partida actual. Los HTML en `02_VERSIONES_ANTERIORES` son históricos para comparar cambios y recuperar funciones, no la interfaz de partida actual.

**COPIA EXTERNA VERIFICADA DE LA VERSIÓN VIGENTE:** https://github.com/evazquezcano/opo-ia/blob/main/respaldo/2026-10-31/OPO-IA_planificador_simplificado_informe_final_2026-10-31.html
**Commit que incorporó la copia:** https://github.com/evazquezcano/opo-ia/commit/b921bb463ad82a09b9aa74f76d46744e8c8a11d8
**SHA de objeto Git del HTML:** `f016780585c29878b2c3b7e31d98c8fd24e990ce`. La copia GitHub es exacta según el hash Git contrastado con archivo local.

Repositorio público de desarrollo: https://github.com/evazquezcano/opo-ia
Referencia visual original en el repositorio: https://github.com/evazquezcano/opo-ia/blob/main/web/referencia-original.html
Memoria original 30/10: https://github.com/evazquezcano/opo-ia/blob/main/documentacion/MEMORIA_MAESTRA_OPO_IA_2026-10-30.md
Protocolo de bloques y plantilla 31/10: https://github.com/evazquezcano/opo-ia/blob/main/documentacion/PLANIFICACION_BLOQUES_Y_PLANTILLA_UD_2026-10-31.md

## 2. PROPÓSITO Y MARCO

OPO-IA permitirá que estudiantes que preparan oposiciones docentes elaboren una programación anual de UD y SA con currículo autonómico vigente aportado por cada estudiante, planifiquen contenido y sesiones, generen tablas editables Word y PDF conforme a las plantillas originales del curso y obtengan una matriz final de cobertura curricular por UD/SA. Ámbitos: Primaria, ESO y Bachillerato; selección de CCAA, Ceuta y Melilla, curso y materia.

**Identidad visual intocable salvo petición expresa:** HTML original (`web/referencia-original.html`) con cabecera OPO-IA, RADTE y UNED Futuro Docente, cinco imágenes incrustadas, paleta verde/blanco/dorado, cuatro pestañas y una barra lateral. Mantener el CSS, logotipos, diseño, orden y tratamiento institucional. HTML autónomo sin imponer aspecto Streamlit.

## 3. DECISIONES VIGENTES SOBRE LA INTERFAZ (31/10, ÚLTIMA ITERACIÓN)

### Currículo

- Seleccionar territorio, etapa, curso y materia/área.
- Cargar **un PDF curricular oficial principal obligatorio**. El estudiante busca la disposición en https://blogs.uned.es/futurodocente/normativa/.
- Convocatoria de oposiciones y rúbricas/listas de cotejo: documentaciones **opcionales** y separadas de criterios de evaluación curriculares.
- Se retiraron, por simplificación, controles independientes para PDF de modificaciones y orden de evaluación (podrían seguir siendo necesarios en verificación jurídica de vigencia, pero no mostrarlos en interfaz sin nueva decisión).
- El campo inicial lleva únicamente la etiqueta «Contraseña»: actualmente verifica el formato del correo institucional oculto. **NO es autenticación real**; no presentarlo como seguridad.
- Lectura del currículo en navegador mediante PDF.js, con extracción de candidatos, códigos y páginas. **NO está validada la extracción literal, exhaustiva ni jurídicamente actualizada**. No confundir detección de fragmentos con integridad curricular.

### Planificación: simplicidad como requisito prioritario

- El estudiante determina el total de piezas que exige su convocatoria (p. ej., 12), cuántas son UD y cuántas SA; UD+SA=total. Puede asignar títulos/ejes temáticos, nº de sesiones y evaluación.
- Selecciona **cuántos bloques de contenido quiere trabajar por unidad**, con opciones «Automático», «Todos» o 1, 2, 3... hasta los bloques **realmente identificados en su materia/curso**. NO poner máximo universal cinco bloques. El resultado automático es orientativo.
- La secuenciación por bloques permanece en modo automático; si el estudiante desea definir personalmente qué bloques aparecen en cada unidad, puede activar **una opción voluntaria** inicialmente oculta. Conservar títulos y orden al modificar preferencias.
- Decide **en cuántas UD/SA se incorporarán ODS/sostenibilidad** y **en cuántas se incorporarán elementos transversales**. El motor distribuye esas incorporaciones equitativamente entre las evaluaciones existentes y procura una por evaluación cuando son tres, priorizando UD cuando sea posible.
- **NO mostrar** registro manual completo por unidad de objetivos de etapa, competencias específicas, descriptores, criterios, saberes o bloques detallados, ni campos de «registro de elementos», ni configuración didáctica extensa para el checklist. Esas relaciones se calculan **internamente** a partir del inventario normativo y las tablas generadas. Solo dejar los parámetros sencillos solicitados.

### Cobertura: simplificada

- Mostrar el **inventario de elementos encontrados** en la documentación curricular: objetivos de etapa, competencias específicas, criterios de evaluación, descriptores de salida, bloques, saberes y transversales, con **recuentos** y páginas candidatas.
- NO exponer al estudiante panel de «Cobertura conjunta / checklist», estados técnicos de asignaciones, ni detalles de registros internos de elementos. Dicho cálculo se reservará para el informe final.
- Si la extracción de un elemento es parcial o dudosa, advertirlo; no atribuir integridad o cobertura verificadas a coincidencias de texto.

### Documentos e informe final

- Ofrecer elección de generar una **primera tabla UD/SA de prueba** o **todas las tablas** de la programación.
- Word editable y PDF de las tablas usando **las dos plantillas originales** del curso, conservando sus estilos, celdas, bordes, códigos oficiales, métodos seleccionados, sesiones y una página A4 por tabla, cuando sea factible sin alterar datos.
- **Estado real en el HTML actual:** la exportación automática de UD/SA a Word/PDF a partir de las plantillas originales sigue **PENDIENTE**; mantener botones desactivados o advertencia veraz. Las UD Word de piloto se confeccionaron/filtraron por separado, como pruebas.
- **Informe final descargable por separado en Word y PDF**. Debe aparecer después de generar la programación completa y no llenar la pestaña Planificación de registros manuales.
- La tabla general (referencia visual: `04_REFERENCIAS/2_tabla_resumen_unidades_para_programacion.png`) tendrá una fila por cada UD o SA, con nombre, evaluación, nº de sesiones, % temporal, bloques y saberes, criterios de evaluación, relación con SA, transversalidad/sostenibilidad, actividad complementaria cuando proceda, competencias específicas y descriptores; una sección posterior indicará el detalle por categoría y las UD/SA donde aparece cada elemento.
- Checklist general con recuentos de: objetivos de etapa trabajados, competencias específicas, todos los descriptores del perfil de salida vinculados, bloques, todos los saberes básicos, todos los criterios de evaluación, transversales y sostenibilidad/ODS. Distinguir curricularmente **obligatorios** de transversales/ODS **decididos pedagógicamente**.
- Calcular cobertura de cada elemento mediante unión de TODAS las UD y SA, no exigiendo duplicar cobertura en ambos formatos. **No mostrar 100 % ficticios:** 100 % solo cuando inventario completo y asignación individual verificable; asignar bloque no demuestra cubrir todos sus contenidos, ni una competencia garantiza automáticamente la realización de todos sus descriptores.
- «Trabajado en planificación» es distinto de «adquirido/conseguido por el alumnado»; el informe no acredita logro empírico.

## 4. EVALUACIÓN Y NORMATIVA

- Conservar identificadores oficiales: objetivos de etapa a), b)... cuando así aparezcan; competencias específicas con su número; criterios con decimal; bloques con letra; saberes con texto literal. Los códigos artificiales A.1 etc. solamente como referencias **internas de planificador** (nunca códigos oficiales falsos).
- Distinguir técnicas (observación sistemática y análisis de producciones, inicialmente), procedimientos, instrumentos y agentes/modalidades (heteroevaluación, coevaluación, evaluación entre iguales). Ampliación pendiente de la tipología que aporte el responsable.
- Verificar las normas en https://blogs.uned.es/futurodocente/normativa/ y recursos en https://blogs.uned.es/futurodocente/recursos/ cuando sea necesario; el catálogo antiguo 17 CCAA × 3 etapas es **orientativo**, no fuente automáticamente vigente.
- Piloto curricular: Madrid, Lengua Castellana y Literatura de 3.º de ESO, Decreto 65/2022; inventario preliminar de 10 CE, 31 criterios, cuatro bloques, 76 relaciones descriptores/CE. **No tiene validación curricular completa.**

## 5. PRUEBAS Y ARTEFACTOS RECUPERABLES

- El HTML actual fue comprobado en navegador Chromium mediante escenarios sintéticos y revisión de JavaScript, manteniendo estilo visual y logotipos. Probada configuración de 12 piezas y 7 bloques sintéticos (no significa que ese sea un currículo real).
- Ensayada la distribución de 3 incorporaciones de ODS entre 3 evaluaciones; se conserva la selección voluntaria y la asignación de bloques al reordenar.
- Comprobada generación del informe Word de prueba con tabla global y matriz/checklist, sin atribuirles vigencia ni cobertura normativa completa. PDF directo condicionado a carga de biblioteca de navegador y alternativa imprimir a PDF.
- Probada **por separado** la supresión en un DOCX real de UD de filas y apartados no seleccionados, eliminando metodologías/agrupamientos sin uso y conservando una página A4. **NO implica exportador UD/SA integrado.**
- Los archivos fuente, imagen de referencia, pilotos, scripts de transformación y pruebas se incluyen en este ZIP. La copia integral del 30/10 con base del repositorio se incluye como ZIP histórico anidado.

## 6. DECISIONES QUE NO DEBEN PERDERSE

- Última revisión: priorizar la **simplicidad** de la experiencia estudiantil. El motor inteligente hace la distribución curricular; el estudiante no cumplimenta matrices gigantes ni registra a mano todos los elementos.
- El estudiante conserva control de número total, proporción UD/SA, sesiones, evaluación, títulos/ejes temáticos, modalidad de bloques y número de intervenciones ODS/transversalidad.
- La distribución temática de ODS y elementos transversales se reparte equilibradamente entre evaluaciones, sin garantía artificial de progresión adecuada si no está programada efectivamente.
- El informe curricular está al final, apartado Documentos, no en Planificación ni en Cobertura.
- La trazabilidad es individual: cada competencia/criterio/saber/descriptor/objetivo debe enlazar con una o más UD/SA. El hecho de aparecer en el PDF o asignar genéricamente un bloque no es suficiente para cobertura.
- Los PDF curriculares pueden tener estructuras diferentes; extracción transversal debe basarse en documentos reales y verificaciones por materia/curso, no reglas codificadas para un único decreto.

## 7. TAREAS PENDIENTES ANTES DE PRODUCTO DEFINITIVO

1. Validar extracción literal y completa con PDF oficiales completos de varias materias, cursos y etapas, incluidos todos los bloques y saberes; comprobar jurídicamente modificaciones y ámbito de vigencia.
2. Construir inventario curricular estructurado estable con códigos oficiales, texto literal y relaciones verificadas CE–criterios–descriptores–saberes; identificación de transversales cuando proceda.
3. Generar **internamente** distribución completa y temáticamente coherente de todos los elementos entre las UD/SA previstas y auditar cobertura real, avisando de lagunas sin inventar 100 %.
4. Integrar exportación real de tablas UD/SA a DOCX y PDF desde las plantillas originales (incluida la plantilla SA aún no localizada en este respaldo), conservando una página A4 cuando sea viable; eliminar filas/opciones no seleccionadas.
5. Vincular el informe final a **las tablas realmente generadas**, no solo a propuestas/candidatos de extracción; DOCX/PDF descargables con nomenclatura y trazabilidad de criterios/descriptores/saberes.
6. Revisar aspectos de seguridad del filtro de entrada y la eventual publicación web; filtro de formato de correo no constituye autenticación.
7. Documentar pruebas en browser y repositorio y publicar versión definitiva solo tras contrastar condiciones anteriores.

## 8. CÓMO REANUDAR EN OTRO CHAT

Copiar la siguiente instrucción en un nuevo chat y adjuntar este ZIP si es necesario:

«Continúa el proyecto OPO-IA de generación de unidades didácticas y situaciones de aprendizaje. Usa la MEMORIA_MAESTRA_CONTINUIDAD_2026-10-31.md del respaldo de 31/10/2026 y la versión actual `OPO-IA_planificador_simplificado_informe_final_2026-10-31.html`, **no** versiones anteriores del repositorio. Respeta la identidad visual y la simplificación de las pestañas. Los documentos de GitHub son antecedentes; las decisiones más recientes están en esta memoria. Antes de proponer cambios, revisa funcionalidades existentes y pendientes; no digas que el motor curricular o el exportador Word de UD/SA ya están finalizados.»

Guardar copia personal del ZIP. Si se agota un chat, la ruta más fiable es aportar el ZIP a uno nuevo; adicionalmente verificar las memorias y fuente original en el repositorio GitHub. Fecha del corte y sumas SHA-256 en MANIFEST_SHA256.json.
