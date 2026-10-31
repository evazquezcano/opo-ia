# OPO-IA — Revisión de interfaz acordada (31/10/2026)

**Origen:** revisión con el responsable del proyecto de las cuatro pestañas del HTML aprobado.  
**Estado:** especificación de implementación; no sustituye a `web/index.html` ni al HTML original. **No modificar apariencia, logotipos, colores, distribución y navegación aprobadas.**

## 0. Acceso al planificador

- Redactar el encabezado como **«Accede con tu contraseña»** y etiquetar el control **«Contraseña»**. No mostrar la cadena de ejemplo `usuario@alumno.uned.es`, ni explicar al visitante cómo deducir la clave.
- Retirar de la versión definitiva la etiqueta «Maqueta funcional», avisos internos de prototipo y acceso a demostración.
- **Decisión pendiente para implementar sin inducir a error:** ¿el usuario escribirá su correo institucional en el campo oculto «Contraseña», como filtro no seguro, o recibirá una clave específica del curso? Un correo introducido como contraseña no autentica la identidad y puede adivinarse; si se requiere restricción real, la comprobación debe ser de servidor y no un secreto incrustado en el HTML público.
- No guardar contraseñas ni correos en el repositorio, en el navegador o en archivos de sesión por defecto.

## 1. Currículo (primera pestaña)

- Preservar comunidad autónoma o Ceuta/Melilla, etapa (Primaria, ESO, Bachillerato), curso (1.º–6.º, 1.º–4.º, 1.º–2.º), materia/área.
- Hacer claramente visible el **PDF de la norma curricular principal** como único documento obligatorio. Enlace a la página del curso con normativa oficial: https://blogs.uned.es/futurodocente/normativa/.
- Conservar hasta tres documentos modificativos opcionales *solo* cuando afecten al contenido curricular y, también opcional, una orden/decreto de evaluación (sin exigirla para elaborar UD/SA).
- Añadir **«Documentación de la convocatoria de oposiciones (opcional)»** con dos entradas diferenciadas:
  1. Resolución o convocatoria de oposiciones en PDF.
  2. Rúbricas o listas de cotejo publicadas por la administración competente (permitir PDF, en principio).
- Mensaje visible: «Estos documentos son opcionales y no son necesarios para generar la unidad didáctica o situación de aprendizaje. Si se aportan, permitirán comprobar los requisitos formales de presentación y los aspectos evaluados por el tribunal».
- **Diferenciar** los criterios de calificación/rúbricas de la oposición de los **criterios de evaluación curriculares** (no son intercambiables).
- El lector de documentos debe tratar estas dos nuevas fuentes como documentación de formato/verificación, nunca como reemplazo de los contenidos curriculares.
- Conservar aclaración territorial: Ceuta y Melilla utilizan órdenes ministeriales que desarrollan los reales decretos estatales.

## 2. Planificación

- Conservar diseño y cálculos actuales: número total de piezas, reparto UD+SA cuya suma sea exactamente el total, secuencia y orden editable.
- Permitir asignar título a cada pieza, como ahora.
- El total indicado debe poder cotejarse con la convocatoria cuando el estudiante la aporte; sin convocatoria, el usuario introduce el exigido en sus bases y se advierte de que no ha sido verificado automáticamente.

## 3. Cobertura

- Añadir un primer bloque **«Integridad de la documentación curricular»** con lista de verificación:
  - Objetivos de etapa.
  - Competencias específicas.
  - Criterios de evaluación.
  - Saberes básicos/contenidos y bloques.
  - Descriptores operativos y perfil de salida, cuando corresponda.
  - Elementos transversales aplicables.
- Estados prudentes por ítem: «Identificado», «No identificado», «Pendiente de verificación literal» (la mera detección de palabras o títulos **no** autoriza un check verde de integridad completa).
- Advertencia específica automática «No se ha identificado en los documentos aportados: X», sin afirmar que un elemento no exista si el extractor no ha podido leerlo.
- Mantener un segundo bloque distinto **«Cobertura conjunta de la programación»**: criterios, competencias y contenidos efectivamente asignados a la unión de TODAS las UD y SA. La progresión temática se revisa dentro de la planificación, no como elemento que se extrae del PDF.
- Calcular porcentajes reales como `n.º elementos distintos asignados / n.º elementos curriculares verificados`, cuando existan denominadores y asignaciones reales. **Nunca mostrar 100 % ni check verde artificial por un PDF legible.**

## 4. Documentos

- Utilizar las plantillas originales del curso para UD/SA, que el responsable facilitará y validará, no reinterpretarlas como tablas nuevas.
- Permitir dos modalidades: **«Generar y descargar una tabla de prueba»** (primera UD o SA de la secuencia) y **«Generar y descargar todas las tablas»** (n.º dinámico, 12, 13, 14, o el total configurado).
- Exportación **Word (.docx)** y **PDF**. Word editable para modificar después tipografía, tamaño, diseño y contenido.
- Retirar de la interfaz estudiantil la opción **«Descargar configuración de la maqueta (.json)»**; se puede conservar JSON interno para funcionamiento o depuración, pero no ofrecerlo como salida de usuario.
- Incorporar al final **«Informe resumen de cobertura y desarrollo»**, con contadores únicos de competencias específicas, criterios de evaluación, saberes básicos (cuando corresponda) y porcentaje de asignación entre todas las UD y SA.
- La estructura exacta del informe y la tabla de ponderaciones/desarrollo **quedan pendientes de la plantilla/tabla que proporcionará el responsable**. Hasta entonces no inventar ponderaciones ni porcentajes de «desarrollo» semántico. Distinguir cobertura cuantitativa de grado de desarrollo.
- Mostrar siempre estado real de las funcionalidades; no botones que aparenten descargar Word/PDF si el generador no está implementado.

## Dependencias y siguiente iteración

1. Resolver la modalidad exacta de acceso: correo como clave disfrazada vs contraseña real de curso.
2. Ajustar textos y controles de carga de la primera pestaña y el acceso, sin modificar CSS ni branding.
3. Adaptar las dos comprobaciones de la pestaña Cobertura y el diseño funcional de Documentos con estados pendientes veraces.
4. Implementar extracción literal bajo demanda de la normativa aportada, aplicando cambios oficiales con trazabilidad y verificación.
5. Con las dos plantillas del curso y la tabla de informe final, generar Word/PDF y validar la primera tabla de prueba antes del lote total.

**Implementación futura:** siempre basarse en `web/referencia-original.html` y `web/index.html`, respaldados en GitHub; no pasar a interfaz Streamlit predeterminada.
