# OPO-IA

**Generador de unidades didácticas y situaciones de aprendizaje para programaciones docentes.** Proyecto de formación asociado a RADTE y Futuro Docente (UNED).

## Estado del proyecto

**Prototipo en desarrollo.** La pestaña «Currículo» permite cargar el decreto curricular oficial, hasta tres modificaciones y una norma de evaluación. Las pestañas «Planificación», «Cobertura» y «Documentos» todavía no realizan sus funciones definitivas. El análisis de PDF es técnico y preliminar: **no certifica la vigencia normativa ni autoriza generar programaciones**.

La búsqueda de la norma y de sus posibles modificaciones corresponde al estudiante como actividad formativa del curso. El catálogo autonómico del repositorio sirve de referencia, pero no sustituye la búsqueda y verificación de las disposiciones vigentes.

## Ejecutar el prototipo con Python

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá una interfaz con cuatro pestañas. Para el acceso inicial se solicita un correo terminado en `@alumno.uned.es`; este es exclusivamente un filtro de formato, **no una autenticación**.

## Carga documental

- Decreto curricular principal (PDF obligatorio).
- Hasta tres modificaciones o correcciones curriculares (PDF opcionales).
- Orden o decreto de evaluación (PDF opcional y analizado por separado).

Los PDF se examinan en memoria y no se guardan en el repositorio. Se puede descargar una ficha JSON de procedencia y comprobaciones técnicas. Actualmente no se extrae todavía un currículo completo a partir de los documentos aportados.

## Fuentes y protocolos

- [Flujo normativo del estudiante](documentacion/FLUJO_NORMATIVO_ESTUDIANTE.md)
- [Protocolo de validación curricular](documentacion/PROTOCOLO_CURRICULAR.md)
- [Informe documental previo](datos/ESTADO_DOCUMENTAL.md)
- [Normativa educativa de Futuro Docente](https://blogs.uned.es/futurodocente/normativa/)
- [Recursos para el profesorado](https://blogs.uned.es/futurodocente/recursos/)

## Privacidad

No hay almacenamiento deliberado de documentos subidos, correos ni información personal en archivos locales o GitHub. El procesamiento de los PDF requiere enviarlos desde el navegador al servidor Streamlit; los registros y políticas del alojamiento quedan fuera del código de esta aplicación.
