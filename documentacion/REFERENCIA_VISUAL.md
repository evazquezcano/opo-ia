# OPO-IA — Referencia visual obligatoria

**Archivo de referencia creado previamente en el proyecto:** `OPO-IA_planificador_prototipo.html`.

**Huella SHA-256 del archivo original (30-10-2026):**
`ae0fc385eb85f5322210eac41a29791b64fe044532dba46c4ac33364ca882297`.

El usuario ha aprobado este prototipo y ha pedido conservar su apariencia. El archivo está disponible en los artefactos del chat; este documento registra sus rasgos para evitar rediseños accidentales. **Este documento no es el HTML original**.

## Estructura que se debe preservar

- Encabezado institucional con tres logotipos: OPO-IA a la izquierda; RADTE y Futuro Docente a la derecha. Subtítulo «Generador de unidades didácticas y situaciones de aprendizaje para programaciones docentes».
- Línea superior de 6 píxeles con degradado verde-azul.
- Banda principal (*hero*) verde oscuro, esquinas redondeadas, titular «Una programación anual. Dos modalidades de desarrollo.» e insignia circular «UD/SA · UN CURRÍCULO».
- Contenido centrado con anchura máxima de 1216 píxeles, fondo suave, tarjetas blancas de esquinas redondeadas y bordes discretos.
- Acceso inicial con panel introductorio y panel para correo UNED; filtro `@alumno.uned.es` sin presentarlo como autenticación efectiva.
- Diseño de dos columnas en el planificador: panel lateral de navegación a la izquierda y tarjeta principal de formulario a la derecha.
- Cuatro pasos en la misma navegación vertical, en este orden y con las denominaciones aprobadas:
  1. **Currículo** — Etapa, curso y materia.
  2. **Planificación** — Distribución UD / SA.
  3. **Cobertura** — Verificación global.
  4. **Documentos** — Plantillas y descarga.
- Pie de página con identificación OPO-IA, RADTE y Futuro Docente.
- Interacción, diseño adaptable y estados visuales del HTML original. Los tres logotipos están incrustados en ese HTML como imágenes WebP codificadas, no sustituidas por logos genéricos.

## Variables CSS originales (no sustituir por una paleta nueva)

```css
:root {
  --bg: #f2f6f4;
  --white: #fff;
  --text: #153329;
  --muted: #62746d;
  --green: #07553e;
  --green2: #08775b;
  --navy: #0c2c45;
  --blue: #176b90;
  --gold: #bb9b5a;
  --line: #dce5df;
  --soft: #eaf5ef;
  --softblue: #edf5f9;
  --warning: #865e1c;
  --warningbg: #fff7e7;
  --shadow: 0 10px 35px rgba(6,53,39,.08);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Arial, sans-serif;
}
```

## Regla de integración

Las funciones nuevas (PDF curricular obligatorio; hasta tres modificaciones pertinentes opcionales; orden/decreto de evaluación opcional; extracción sobre la marcha; planificación y exportación) deben incorporarse **dentro de las tarjetas y pasos del HTML original**. No reemplazar el frontend aprobado por la apariencia predeterminada de Streamlit ni alterar sus colores, logos, títulos y disposición.

El archivo `app.py` escrito anteriormente con controles Streamlit predeterminados es un prototipo técnico funcional, **no** el diseño visual aprobado. Se conservará o adaptará la lógica de procesamiento, pero la interfaz final debe reproducir fielmente el HTML de referencia.

**Antes de realizar cualquier cambio visual:** cotejar el resultado con `OPO-IA_planificador_prototipo.html` y sus capturas de las cuatro pestañas. El propósito de este archivo es mantener la identidad visual, no reinterpretarla.
