# OPO-IA — Memoria maestra y punto de reanudación

**Corte del proyecto:** 30 de octubre de 2026, 21:11 h (Europe/Madrid).  
**Repositorio:** https://github.com/evazquezcano/opo-ia  
**Rama principal:** `main`. Repositorio público, cuenta `evazquezcano`.

## Instrucción de continuidad para sesiones futuras

Este documento prevalece como **resumen operacional y de decisiones del proyecto**. Antes de trabajar, comprobar el estado real del repositorio y abrir `web/index.html`, `web/referencia-original.html`, `documentacion/FLUJO_NORMATIVO_ESTUDIANTE.md`, `documentacion/PROTOCOLO_CURRICULAR.md`, `datos/ESTADO_DOCUMENTAL.md` y `README.md`. No atribuir validación curricular a fuentes descargadas o a la lectura textual de PDF.

**Protocolo de trabajo acordado:** realizar una acción de desarrollo cada vez, verificar su resultado y terminar preguntando «¿Quieres que avance con la siguiente?». El usuario prefiere que el asistente realice directamente las operaciones de GitHub siempre que sea posible, sin instrucciones innecesarias para que las ejecute manualmente.

## Objetivo y diseño

Construir **OPO-IA**, generador para estudiantes de un curso de formación docente que elabora la programación anual de unidades didácticas (UD) y situaciones de aprendizaje (SA), incluyendo tablas Word/PDF ajustadas a las plantillas originales suministradas. Cuatro pestañas: **Currículo, Planificación, Cobertura, Documentos**.

**Proteger el diseño visual aprobado:** `web/referencia-original.html` es la copia INTACTA del prototipo; `web/index.html` es la versión integrada, manteniendo colores, logotipos incrustados OPO-IA/RADTE/Futuro Docente, encabezado, tarjetas, menú vertical y pie de página. NO sustituir su interfaz por la estética predeterminada de Streamlit. La copia HTML original exacta y los logos PNG, las dos plantillas DOCX y las versiones preliminares están también en el ZIP local de respaldo.

El acceso `@alumno.uned.es` es **filtro de formato, no autenticación**; sin conservación deliberada de correos ni de PDF de estudiantes. Sin dominio de pago.

## Decisión normativa FINAL (prioritaria frente a desarrollos anteriores)

El **estudiante localiza y aporta el currículo aplicable** para su comunidad, etapa, curso y materia. Se **extrae sobre la marcha**, al subir la documentación, por sesión. El catálogo de 17 CCAA × 3 etapas sirve como apoyo, **no se debe mantener como fuente permanentemente vigente ni utilizarlo por defecto como currículo validado**.

Documentos:
1. Un PDF principal OBLIGATORIO: decreto curricular de la comunidad autónoma, con anexos.
2. Hasta tres PDF adicionales OPCIONALES, únicamente si modificaciones oficiales afectan a competencias específicas, objetivos de etapa, descriptores operativos, criterios de evaluación, bloques, saberes/contenidos o elementos transversales. **Sin cambios curriculares relevantes, NO subir nada más**.
3. Orden/decreto de evaluación OPCIONAL, **no necesario para desarrollar la programación**. Puede consultarse más adelante para procedimientos, instrumentos o documentos de evaluación. No altera automáticamente criterios curriculares.
4. **Ceuta y Melilla:** el currículo completo del ámbito de gestión ministerial se establece en **órdenes ministeriales**, mientras los reales decretos estatales fijan enseñanzas mínimas. El HTML advierte de ello. Revisar orden aplicable de Primaria, ESO o Bachillerato; evitar aceptar un real decreto de mínimos como único documento suficiente.

La búsqueda, selección y comprobación de posibles modificaciones es parte de la actividad formativa del estudiante. La aplicación no inventa vigencia jurídica ni aplica cambios con coincidencias léxicas.

## Funciones ya implementadas

- El prototipo HTML original y su integración con cargas de PDF, hasta 3 modificaciones, evaluación opcional, índices preliminares de página usando PDF.js. El navegador necesita acceso a CDN para cargar PDF.js.
- Interfaz de prueba técnica `app.py` en Streamlit con las mismas fuentes documentales, guardando metadatos en memoria y permitiendo descargar índices en JSON; NO es el frontend final aprobado.
- `opoia/fuentes.py`: lectura de PDF, cabecera, contraseña, tamaño, páginas, texto preliminar.
- `opoia/extraccion.py`: indexación completa de páginas, localización de fragmentos de elementos curriculares, separación de principal/modificaciones/evaluación sin efectuar sustituciones normativas.
- Catálogo autonómico `datos/catalogo_51_autonomicos.json`, 51 entradas (17 CCAA × 3), **fuentes candidatas NO verificadas**. Los 7 enlaces finales de Asturias/La Rioja/Valencia quedaron sin descarga en último reintento.
- Descargas, reintentos, consolidación por SHA256 y auditoría preliminar de normas.
- Piloto de Lengua Castellana y Literatura de 3.º ESO Madrid: 31 criterios, 10 competencias y sus descriptores (76 relaciones), bloques A/B/C/D, extractores mejorados PyMuPDF, documentación de página y archivos JSON. Aún requiere cotejo total, codificación de contenidos y objetivos, versiones vigentes. **NO está validado ni habilitado**.

## Situación real, sin confundir prototipo con producto terminado

- `web/index.html` es el frontend elegido, con carga de archivos e índice documental provisional, pero aún **NO realiza extracción literal estructurada y verificada de TODOS los elementos curriculares**; necesita validación por materia/curso, cotejo de modificaciones y control de integridad.
- La planificación completa y la exportación definitiva Word/PDF conforme a plantillas NO están terminadas.
- El check verde global solo se habilitará tras la cobertura conjunta de TODAS las UD+SA.
- La app web no está desplegada públicamente. GitHub tiene código y GitHub Actions; Streamlit sirve como prototipo técnico, no como frontend final.
- Las descargas de PDF, aunque el workflow diga SUCCESS, no equivalen a currículos jurídicamente verificados.
- El informe documental previo agrupó 50 referencias en 42 archivos distintos (por SHA256): 34 con norma preliminarmente identificada, 7 sin identificación preliminar y 1 con error de extracción; 0 currículos totalmente validados.

## Requisitos de planificación y salida

- Planificación anual configurable: número total de UD/SA (p. ej., 12 = 8 UD + 4 SA), sesiones por unidad, fechas, horas por semana, distribución de evaluaciones, progresión de contenidos, metodologías.
- Comprobar una sola vez la **cobertura curricular combinada** de UD+SA (criterios, competencias, saberes, bloques, objetivos y descriptores); no exigir que cada formato cubra por separado todo.
- Documentos editables Word y PDF, una sola página DIN A4 por unidad o SA, fuente y estructura originales de las plantillas: `tabla SA programacion.docx` y `tabla UD programacion_EJEMPLO CON BLOQUES DE CONTENIDO ACORTADOS.docx`.
- Códigos oficiales de criterios, competencias y objetivos; los subcódigos internos de saberes A.1/A.2.1... diferenciados expresamente de los oficiales; objetivos didácticos muy breves (hasta cuatro), temporalización por sesión, ODS y elementos metodológicos/evaluativos pertinentes.
- Referencias de apoyo: https://blogs.uned.es/futurodocente/normativa/ y https://blogs.uned.es/futurodocente/recursos/.

## Histórico de ejecuciones clave (enlaces estables)

| Run ID | Finalidad | Observación |
|---|---|---|
| 41109001469 | Descarga inicial de documentos | 9/11 descargas |
| 41110399643 | Primer lote autonómico | 19/25 fuentes descargadas |
| 41112770540 | Segundo lote autonómico | 18/21 fuentes descargadas |
| 41113624931 | Auditoría estructural catálogo | 51 entradas, 17 CCAA × 3 etapas |
| 41114023140 | Primer reintento selectivo | 4/11 direcciones recuperadas |
| 41114860790 | Auditoría documental preliminar | 41 registros, 31 coincidencias y 24 indicios de anexos |
| 41114911967 | Reintento de 7 fuentes restantes | 0/7 |
| 41115404626 | Consolidación del corpus | 42 archivos únicos, 34 con identificación preliminar |
| 41115953393 | Extracción Madrid LCL 3.º ESO | 31 criterios |
| 41116180934 | Reextracción con PyMuPDF | mejor legibilidad |
| 41118154388 | Pruebas de interfaz Streamlit | OK |
| 41118890543 | Pruebas ampliadas Streamlit | OK |
| 41120762371 | Prueba visual HTML inicial | fallo en el test de regex/ancla; **no suponía un cambio del diseño**; corregido posteriormente |

Todos los enlaces: `https://github.com/evazquezcano/opo-ia/actions/runs/ID`. Los artefactos de GitHub Actions caducan (habitualmente 30 días), de ahí la **copia consolidada de seguridad** en GitHub Releases y el ZIP local entregado al usuario. Reanudar comprobando ejecuciones nuevas y estado actualizado de los tests.

## Próxima acción acordada

Desarrollar **la extracción literal y estructurada en el momento de subir el decreto**. Vincularla con el HTML visual aprobado, conservar literalidad/códigos, distinguir normativa principal/modificaciones y advertir cualquier laguna sin presentar la extracción como automáticamente válida. Probar con PDF oficial completo por etapa, materia y curso. Después avanzar con planificación, cobertura y exportación.

## Recuperación

1. Abrir `README.md` y este archivo; verificar último commit en `main`.
2. Recuperar los archivos del repositorio `git clone https://github.com/evazquezcano/opo-ia.git`.
3. Buscar en las **Releases de GitHub** la copia integral fechada 30-10-2026 con código, historial de Git, resultados y registros de Actions.
4. Conservar adicionalmente el ZIP descargable de esta conversación, que contiene originales y plantillas Word.
5. Nunca declarar «validado» un documento o etapa sin cotejar íntegramente las fuentes normativas.
