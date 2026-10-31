# OPO-IA · Estado de la interfaz aprobada (31/10/2026)

## Decisión confirmada por el responsable

El estudiante introduce **su correo electrónico institucional UNED como valor de acceso**, pero el campo visible se titula exclusivamente **«Contraseña»**, con entrada enmascarada, sin ejemplo visible `usuario@alumno.uned.es` ni mensajes que revelen el formato. **Advertencia técnica:** un filtro del lado del cliente no autentica al estudiante ni impide realmente accesos no autorizados; la plataforma del curso comunica la regla de entrada. No afirmar que sea una autenticación segura.

**El diseño aprobado (logotipos, CSS, colores, navegación y tarjetas) permanece intacto.** Archivo original `web/referencia-original.html`; archivo actualizado `web/index.html`. Se conservan las cuatro pestañas y el formato institucional.

## Cambios ya implementados en el HTML

- **Acceso:** «Accede con tu contraseña» y etiqueta «Contraseña», campo enmascarado, mensaje de error «Contraseña no válida». Eliminados la demostración y el texto visible de la maqueta. El código sigue comprobando el formato de correo institucional, sin almacenar deliberadamente el valor.
- **Currículo:** selección CCAA/Ceuta-Melilla, etapa, curso y materia; mantiene la norma curricular principal obligatoria con anexos y enlace directo a https://blogs.uned.es/futurodocente/normativa/. Modificaciones curriculares hasta tres y evaluación opcional, según criterios acordados. Se añaden dos cargas independientes **opcionales**: resolución de convocatoria de oposiciones y rúbricas/listas de cotejo oficiales, con enlace oficial recomendado. Se advierte de que no se necesitan para generar UD/SA y que los criterios de valoración del tribunal no equivalen a criterios curriculares de evaluación.
- **Planificación:** se preserva el número total, el reparto UD + SA, los títulos y el orden. No alterar el mecanismo existente sin petición expresa.
- **Cobertura:** lista de objetivos de etapa, competencias específicas, criterios de evaluación, bloques de contenido, saberes, descriptores y elementos transversales. Señala páginas candidatas con fuente de currículo o modificación; cuando no se detecta un elemento dice **«No identificado»** y lo detalla en un aviso. No interpreta una coincidencia documental como currículo íntegro y validado. En una sección separada figura la cobertura global UD+SA, todavía pendiente de cálculo.
- **Documentos:** selector entre **primera tabla de prueba** o **todas las tablas**, con salida Word/PDF prevista. Los botones siguen **desactivados** hasta incorporar plantillas del curso y extracción curricular válida; eliminado el JSON de configuración de la maqueta. Se ha dejado preparada la estructura del informe final: total UD/SA, recuento de competencias/criterios/saberes, % de cobertura y grado de desarrollo, sin cifras ni ponderaciones ficticias.

## Limitaciones que deben mantenerse visibles en la implementación

1. `normReadPdf` localiza indicios de encabezados y páginas en el navegador (PDF.js): todavía no efectúa una extracción **literal completa ni cotejada** de todos los criterios, competencias y saberes por curso y materia.
2. Cuando hay modificaciones, las páginas detectadas se integran **solo como evidencias** en Cobertura; no se aplican cambios de artículos o anexos sin análisis jurídico.
3. Los PDF de oposición se indexan como documentos opcionales, pero **no se ha automatizado todavía la extracción/verificación de requisitos de formato y rúbricas**.
4. No existe aún exportación real Word/PDF en el HTML.
5. El informe final está a la espera de la tabla de ponderación/desarrollo del responsable y de las plantillas originales.

## Pruebas y archivo

- Comprobación sintáctica JavaScript con Node.js: correcta.
- Prueba de navegación real con Chromium/Playwright mediante HTML inyectado: acceso válido e inválido, cuatro pestañas, seven categorías de Cobertura, selector de salida y dos botones de exportación deshabilitados, sin errores de JavaScript.
- Comparación de CSS y cinco imágenes originales incrustadas: idénticos.
- Prueba de identidad visual en GitHub Actions: `.github/workflows/verificar-prototipo-html.yml`.
- Archivo descargable del 31/10/2026: `OPO-IA_planificador_actualizado_31-10-2026.html` y ZIP con versión original y notas.

## Próximo trabajo

1. Diseñar y comprobar un parser de extracción literal del PDF que aporte el estudiante en tiempo real, con preservación de texto/códigos y alertas de faltantes.
2. Identificar jurídicamente las modificaciones pertinentes.
3. Integrar dos plantillas Word originales (UD y SA) en un motor de salida que permita primera prueba, revisión y lote completo.
4. Añadir validación de formatos de convocatorias/rúbricas y desarrollo del informe global con la tabla aportada por el responsable.

Reanudar **sobre el HTML aprobado**, sin rediseñarlo ni activar validaciones/descargas ficticias.
