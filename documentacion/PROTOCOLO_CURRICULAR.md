# Protocolo de consolidación curricular de OPO-IA

## Principio
Un enlace abierto, una descarga correcta o la identificación automática de un decreto **no** acredita un currículo completo. Ningún archivo habilita la generación de unidades hasta la revisión completa de los anexos aplicables.

## Criterios para consolidar una materia/curso
1. Comprobar la disposición y todas las modificaciones, correcciones y anexos aplicables a fecha de referencia, con enlace al diario oficial.
2. Identificar etapa, curso o ciclo, materia y, cuando proceda, modalidades, vías u optativas.
3. Transcribir literalmente objetivos de etapa, competencias específicas, criterios de evaluación y saberes básicos; identificar descriptores vinculados cuando proceda.
4. Conservar el código oficial si existe. Los códigos breves de saberes (A.1, A.2.1...) se etiquetan como **internos** cuando la norma no los proporciona; nunca se atribuyen a la disposición.
5. Revisar íntegramente anexos y tablas, incluidos documentos PDF no extraíbles y las remisiones a otras normas.
6. Contrastar la suma de criterios, competencias, bloques y saberes con el documento original.
7. Registrar versión, fecha y responsable de la verificación; marcar `curriculo_completo_verificado: true` solo con evidencia suficiente.
8. Antes de generar 8 UD + 4 SA u otra combinación, comprobar la cobertura **global** de todos los elementos pertinentes sin exigir una duplicación artificial por formato.

## Estado actual
La auditoría automática agrupa por SHA-256, identifica referencias y detecta indicios de anexos. **No valida** textos curriculares. El informe está en `datos/ESTADO_DOCUMENTAL.md`.

## Riesgos observados
- Páginas institucionales o índices que mencionan la norma, pero no contienen el anexo.
- Documentos obtenidos con referencias literales abreviadas o modificadas (posibles falsos negativos en la coincidencia).
- PDF con extracción defectuosa (por ejemplo un fichero de Primaria de Comunitat Valenciana).
- Normas y textos consolidados modificados con posterioridad a su publicación inicial.
- Artefactos de GitHub temporales: conservar metadatos no equivale a conservar los PDF de forma indefinida.

## No confundir
La validación documental, la validación curricular por materia y la comprobación global de cobertura de una programación son tres operaciones diferentes.
