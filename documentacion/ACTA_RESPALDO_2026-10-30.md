# OPO-IA — Acta de cierre y respaldo verificado (30/10/2026)

## Copias de seguridad

1. **Repositorio de trabajo:** https://github.com/evazquezcano/opo-ia
2. **Rama congelada de respaldo:** https://github.com/evazquezcano/opo-ia/tree/respaldo-integral-2026-10-30
   - Commit fijado: `707af73ddc06d22504817161ec4dce3d67e034c7`
   - ZIP de GitHub: https://github.com/evazquezcano/opo-ia/archive/refs/heads/respaldo-integral-2026-10-30.zip
3. **Release permanente con código, historial Git, registros de Actions y artefactos recuperados:**
   - https://github.com/evazquezcano/opo-ia/releases/tag/opo-ia-respaldo-2026-10-30
   - ZIP: https://github.com/evazquezcano/opo-ia/releases/download/opo-ia-respaldo-2026-10-30/OPO-IA_RESPALDO_GITHUB_2026-10-30.zip
   - Tamaño verificado por API de GitHub: **27.463.513 bytes**.
   - SHA256 declarado por GitHub: `05c0b030403aea00c81c230507b7aa5662811df88f62edad1eea4d1e313e6fb5`.
   - GitHub publica además el fichero `.zip.sha256`.
4. **ZIP local complementario de este chat:** `OPO-IA_RESGUARDO_COMPLETO_LOCAL_2026-10-30.zip`.
   - Contiene **76 archivos**, incluyendo diseños originales, versión integrada, capturas, plantillas Word, logos, catálogos, paquetes previos y material de desarrollo local.
   - Tamaño **34.156.406 bytes**, verificado mediante lectura integral ZIP.
   - SHA256: `dc92421112dbe8235a217eeaa3063d54cf8157994507c144f6eb5a4d61434dc1`.
   - Copia persistente subida a la **Biblioteca personal de ChatGPT**, ruta `/OPO-IA/OPO-IA_RESGUARDO_COMPLETO_LOCAL_2026-10-30.zip`.

El ZIP de GitHub y el ZIP local **son complementarios**. El primero contiene los resultados capturados de Actions y el historial; el segundo preserva plantillas, imágenes y materiales locales que no figuran en el repositorio.

## Documentos de reanudación

- `documentacion/MEMORIA_MAESTRA_OPO_IA_2026-10-30.md` (decisiones y trabajo pendiente).
- `documentacion/REGISTRO_EJECUCIONES_Y_ARTEFACTOS_2026-10-30.json` (inventario de 24 ejecuciones hasta la fecha).
- `documentacion/FLUJO_NORMATIVO_ESTUDIANTE.md` (cargas de PDF principales y opcionales).
- `documentacion/PROTOCOLO_CURRICULAR.md` (cotejo literal, fuentes y códigos).
- `documentacion/REFERENCIA_VISUAL.md` (apariencia que NO debe alterarse).
- `web/referencia-original.html` (diseño original intacto).
- `web/index.html` (HTML integrado que mantiene la apariencia).

## Estado y siguiente fase

- Interfaz HTML aprobada, carga de archivos e indexación preliminar de PDF implementadas.
- No hay todavía extracción literal totalmente verificada, planificación completa, cobertura final ni documentos Word/PDF acabados.
- Los decretos aportados se procesarán sobre la marcha; currículo principal obligatorio y normas modificativas/orden de evaluación opcionales con condiciones explicadas.
- La validación de currículos sigue siendo **pendiente**.
- La comprobación visual corregida terminó correctamente en el run `41121551773`, después de ajustar el propio test. No se modificó el diseño para corregirla.

**Para retomar:** leer la memoria maestra, abrir los dos HTML y continuar con la extracción literal estructurada y los controles de integridad a partir del PDF que aporte el estudiante, sin rediseñar el frontend.
