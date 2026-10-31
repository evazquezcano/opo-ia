# OPO-IA — Prueba piloto con el Decreto 65/2022 de Madrid (31/10/2026)

## Documento de entrada y selección

- PDF facilitado por el responsable: `Decreto_Curriculo_65_2022_secundaria.PDF`, 6.346.788 bytes, 321 páginas y texto seleccionable en las 321.
- SHA-256 del archivo recibido: `fba12d2dd0a19cb11cd670a922213aac5acdfb82db774dea187ed481430ffb53`.
- Ámbito: Comunidad de Madrid, Educación Secundaria Obligatoria, **3.º curso**, **Lengua Castellana y Literatura**.
- Norma: Decreto 65/2022, de 20 de julio, BOCM de 26/07/2022.
- Localización en este PDF: materia desde p. 151 hasta el comienzo de p. 183 (BOCM p. 546–578); criterios de 3.º ESO desde p. 170 (BOCM p. 565) y contenidos desde p. 172. Objetivos de etapa en el artículo 13, p. 8–9.
- **No se ha establecido aquí la vigencia de una posible versión consolidada ni cotejado modificaciones posteriores**; es una prueba de extracción del archivo concreto.

## Hallazgo que justificó corregir el código

El extractor de la versión anterior utilizaba un margen de 24 páginas alrededor de cualquier mención de la materia y mantenía un estado de contexto que continuaba entre materias. Al aplicarlo al PDF completo devolvía **100 candidatos de competencias y 100 de criterios**, incluyendo criterios de Biología y Geología, Ciencias de la Computación y otras materias. **Era un error de selección curricular**, no un problema de legibilidad del PDF. No debe utilizarse esa versión anterior para pilotar.

## Cambio aplicado en `web/index.html`

1. Delimitación de la sección de la materia mediante su título en mayúsculas y la siguiente cabecera de materia.
2. Localización explícita del curso dentro de dicha sección.
3. Diferenciación entre las competencias específicas de materia (comunes al apartado) y los criterios/contenidos del curso seleccionado.
4. Reconocimiento de bloques y viñetas de contenidos, sin convertir los códigos internos en códigos oficiales.
5. Extracción de objetivos de etapa del artículo 13 y menciones de descriptores dentro de las competencias de la materia.
6. En Cobertura, las páginas mostradas proceden ahora de elementos acotados a la materia y el curso, no de coincidencias generales del decreto.

## Resultado preliminar del piloto

| Categoría | Número de elementos candidatos |
|---|---:|
| Competencias específicas | **10** |
| Criterios de evaluación de 3.º ESO | **31** |
| Bloques de contenido | **4** (A, B, C, D) |
| Objetivos de etapa | **12** |
| Fragmentos candidatos de contenidos | 60 |
| Descriptores únicos mencionados | 27 |
| Referencia a contenidos transversales | 1 |

Los 60 fragmentos de contenidos no son el conjunto de saberes completamente delimitado ni equivalen al número oficial de saberes; quedan pendientes de verificar su organización jerárquica y los subelementos sin viñeta. Los 27 descriptores son **códigos únicos**, no el número de relaciones entre competencias y descriptores, que requiere otro cálculo.

Los 31 códigos de criterios obtenidos, todos localizados en el apartado de 3.º ESO, son:
`1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 7.1, 7.2, 7.3, 8.1, 8.2, 8.3, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.1, 10.2`.

## Pruebas realizadas

- Apertura integral del documento y extracción de texto con **PyMuPDF** (321 de 321 páginas).
- Ejecución en **Node.js** de `normStructuredFromPages` contra las 321 páginas de texto reales; 10 competencias, 31 criterios, 4 bloques y 12 objetivos.
- Pruebas adicionales con la misma norma para 1.º, 2.º y 4.º ESO en Lengua Castellana y Literatura y 3.º de ESO en Física y Química, para detectar mezcla de ámbitos.
- Simulación funcional en **Chromium/Playwright**: acceso, selección de comunidad/etapa/curso/materia, carga del PDF real, botón de analizar, resultados y pantalla Cobertura, **sin errores JS**. En este entorno se sustituyó el motor PDF.js por un lector simulado que alimentó la aplicación con el texto de las 321 páginas leído del PDF real. Por ello, este resultado no demuestra que la **descarga de PDF.js desde CDN** funcione en todas las redes/ordenadores.
- Comparación de CSS y las cinco imágenes WebP incrustadas con el HTML anterior: **idénticos**. No se ha alterado el diseño aprobado.

## Para realizar el piloto el responsable

Abrir `web/index.html` o la copia HTML descargada. Introducir correo UNED en el campo «Contraseña», seleccionar **Comunidad de Madrid → ESO → 3.º → Lengua Castellana y Literatura**, aportar el PDF original del decreto y pulsar «Examinar PDF y localizar elementos curriculares». Comprobar resultados y pasar a «Cobertura».

El navegador deberá poder acceder a PDF.js mediante CDN. Ante un mensaje de biblioteca no disponible, revisar la conexión/red y comunicar el error. No se necesita aportar convocatoria, rúbricas ni otra norma para este piloto.

## Pendiente antes de pasar a las tablas

- Comprobar el comportamiento del lector PDF.js **real** en el equipo del estudiante con este mismo PDF de 321 páginas.
- Cotejar íntegramente la literalidad de los 31 criterios y 10 competencias, además de los apartados de contenidos, descriptores y objetivos.
- Comprobar las modificaciones normativas aplicables y vigencia actual.
- Implementar cobertura real UD+SA y Word/PDF conforme a las plantillas del curso, con prueba de primera tabla previa a la generación del lote.

El PDF subido por el usuario **no se incorpora automáticamente al repositorio público**; se conserva solo su identificador SHA-256 y la referencia de la prueba.
