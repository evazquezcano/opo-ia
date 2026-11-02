# NORMA-IA · Especificación y registro de validación (02/11/2026)

## Ubicación y continuidad
- Aplicación: `web/norma-ia/index.html`.
- Repositorio: https://github.com/evazquezcano/opo-ia (rama `main`).
- Aplicación anterior conservada: `web/index.html`; referencia visual protegida: `web/referencia-original.html`.
- Nombre: **NORMA-IA · Generador de normativa para programaciones docentes**.
- Diseño de una sola página: la identidad institucional OPO-IA, logos e identidad cromática proceden del HTML original (tres imágenes WebP incrustadas).
- Filtro de entrada: formato `@alumno.uned.es` en campo «Contraseña», con opción mostrar/ocultar. **No es un sistema de autenticación ni de control real de acceso**. No se ha introducido base de datos, cuenta ni procesamiento remoto de los PDF.

## Funcionalidades implementadas
1. Selección de las 17 comunidades autónomas, Ceuta y Melilla, y Educación Primaria / ESO / Bachillerato.
2. Convocatoria PDF aportada por el estudiante (obligatoria); enlace opcional. Se valida selección, nombre/extensión y sintaxis del enlace. **La convocatoria no se interpreta automáticamente y su contenido no altera la selección normativa**.
3. Dos salidas separadas: A. referencias de normativa básica (epígrafe 1); B. normativa complementaria para referencias finales.
4. Word `.docx`: Times New Roman 12, interlineado sencillo, justificado, A4 con márgenes de 2,54 cm, sangría francesa para referencias, URLs como hipervínculos.
5. PDF: impresión nativa del navegador con los mismos estilos; en el diálogo elegir «Guardar como PDF». Es una exportación por impresión, no la generación inmediata de un archivo desde JavaScript.
6. Dos enlaces contextuales al portal de educación y al repositorio normativo principal de cada territorio, además de repositorios auxiliares y directorio descargable como PDF mediante impresión.
7. Sin almacenamiento deliberado del identificador ni de la convocatoria. Los scripts externos se limitan a la biblioteca de Word (docx.js); si falla su carga, la exportación DOCX informa del error.
8. Mismo diseño institucional, sin alterar la aplicación curricular previa.

## Corpus y alcance de la versión inicial
- **Conjunto estatal**: LOE, LOMLOE y reales decretos de enseñanzas mínimas de Primaria (157/2022), ESO (217/2022) y Bachillerato (243/2022).
- **Piloto autonómico**: Comunidad de Madrid en las tres etapas. Normativa de currículo, reglamentos orgánicos estatales supletorios, órdenes de organización y evaluación, atención a diferencias individuales, instrucciones de inicio de curso 2026-2027, convivencia y otras disposiciones vinculadas a la etapa.
- **Resto de territorios**: portales oficiales localizables y referencias estatales visibles, pero **sin exportación**, hasta que se verifique íntegramente la normativa autonómica aplicable.
- Ninguna combinación se presenta como repertorio íntegro de toda la normativa vigente. Las vigencias están sujetas a reformas, derogaciones, correcciones y normativa sectorial. Las normas supletorias de 1994/1996 deben comprobarse a la luz del desarrollo autonómico.

## Fuentes consultadas para el piloto Madrid
- https://www.comunidad.madrid/educacion/regulacion-educacion-primaria
- https://www.comunidad.madrid/educacion/regulacion-educacion-secundaria-obligatoria
- https://www.comunidad.madrid/educacion/regulacion-bachillerato
- https://www.comunidad.madrid/educacion/ambito-general-comienzo-curso-admision-alumnos-consejos-escolares
- https://www.educa2.madrid.org/web/sginspeccioneducativa/normativa-en-vigor
- https://www.boe.es/eli/es/rd/1996/01/26/82/con
- https://www.boe.es/eli/es/rd/1996/01/26/83/con
- https://www.boe.es/eli/es/o/1994/06/29/%281%29/con
- https://www.boe.es/eli/es/o/1994/06/29/%282%29/con

Directorio de portales: documento del usuario «Portales oficiales de normativa educativa», dos páginas, revisión 24/10/2026; contiene repositorios oficiales estatales y autonómicos. La aplicación conserva los enlaces, pero no reproduce el diseño del PDF original.

## Limitaciones técnicas y editoriales
- GitHub almacena el archivo HTML. La **publicación mediante GitHub Pages no está acreditada**; exige configurar el origen de Pages en el repositorio, si no se había habilitado.
- No existe servicio web que detecte automáticamente normas sobrevenidas ni derogaciones; para la cobertura territorial total se requiere una base jurídica revisada y fechada por comunidad y etapa.
- Las referencias se presentan en formato jurídico compatible con APA 7 en español (título de norma, publicación oficial y URL). Antes de su publicación académica deben adaptarse al formato concreto exigido por tribunal o convocatoria, especialmente cuando la norma enlaza a un portal índice y no a un documento individual.
- La lista complementaria del piloto es **selección inicial**, no inventario exhaustivo; convendría filtrar por especialidad, tipo de centro, programa y convocatoria.
- La aplicación de las instrucciones de inicio de curso depende del curso de referencia y de la titularidad del centro.

## Próximas acciones para una edición completa
1. Comprobar documentalmente las 51 combinaciones de comunidades autónomas por Primaria, ESO y Bachillerato, además de Ceuta y Melilla (órdenes ministeriales de currículo).
2. Registrar por norma: título literal, rango, número, fecha, diario oficial, URL oficial directa, materia afectada, fecha de consulta, modificaciones y estado de vigencia.
3. Construir la matriz de sustitución o supletoriedad de los reglamentos de 1996 y de las órdenes de 1994 por cada comunidad y tipo de centro.
4. Verificar las instrucciones del curso 2026-2027 y actualizarlas cada curso, así como desarrollar un protocolo de comprobación de convocatorias aportadas.
5. Ejecutar pruebas funcionales reales en navegador, especialmente Word, PDF, compatibilidad móvil, enlaces y cambios de comunidad; el fichero supera la comprobación sintáctica del JavaScript en GitHub.
6. Publicar la ruta HTML mediante GitHub Pages sin alterar la aplicación original.

## Criterio de aceptación
Una comunidad/etapa solo se habilita para exportación cuando sus fuentes se han cotejado y tiene verificados currículo, organización, evaluación, diversidad/inclusión e instrucciones aplicables, con anotación expresa del estado del reglamento orgánico y normas sustitutorias.
