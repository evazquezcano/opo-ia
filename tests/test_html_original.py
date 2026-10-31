"""Protege la apariencia del prototipo HTML aprobado y el esquema de carga."""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1] / "web"
ORIGINAL = (BASE / "referencia-original.html").read_text(encoding="utf-8")
CURRENT = (BASE / "index.html").read_text(encoding="utf-8")


def style(html):
    return re.search(r"<style>(.*?)</style>", html, re.S).group(1)


def inline_logos(html):
    return re.findall(r'<img\b[^>]*\bsrc="(data:image/[^"]+)"', html, re.I | re.S)


def script(html):
    return re.search(r"<script>(.*?)</script>", html, re.S).group(1)


class AparienciaOriginal(unittest.TestCase):
    def test_los_cinco_logos_embebidos_son_identicos(self):
        original = inline_logos(ORIGINAL)
        actual = inline_logos(CURRENT)
        self.assertEqual(len(original), 5)
        self.assertEqual(original, actual)

    def test_estilos_originales_preservados(self):
        self.assertTrue(style(CURRENT).startswith(style(ORIGINAL)))

    def test_misma_identidad_visual_y_pestanas(self):
        for nombre in (
            "Una programación anual. Dos modalidades de desarrollo.",
            "Currículo", "Planificación", "Cobertura", "Documentos",
            "RADTE", "Futuro Docente"
        ):
            with self.subTest(nombre=nombre):
                self.assertIn(nombre, CURRENT)

    def test_los_documentos_extra_son_opcionales(self):
        codigo = script(CURRENT)
        for ancla in (
            "normFileBlock('curriculum'",
            "Convocatoria y criterios del proceso selectivo",
            "normFileBlock('call'",
            "normFileBlock('rubric'",
            "normReadPdf",
            "normAnalyze",
            "EXTRACCION_PRELIMINAR",
            "completeCurriculumVerified:false",
        ):
            with self.subTest(ancla=ancla):
                self.assertIn(ancla, codigo)

    def test_acceso_sin_pista_del_correo(self):
        codigo = script(CURRENT)
        self.assertIn("Accede con tu contraseña", codigo)
        self.assertIn('type="password"', codigo)
        self.assertNotIn("usuario@alumno.uned.es", CURRENT)
        self.assertNotIn("demoBtn", codigo)
        self.assertIn('id="toggleSecret"', codigo)
        self.assertIn('Mostrar contraseña', codigo)
        self.assertIn('Ocultar contraseña', codigo)
        self.assertNotIn('id="norm-modifications"', codigo)
        self.assertNotIn('id="norm-evaluation"', codigo)
        self.assertIn('id="normAnalyze"', codigo)
        self.assertIn('normStructuredFromPages', codigo)
        self.assertIn('const bullet=line.raw.match', codigo)
        self.assertIn("Contraseña no válida.", codigo)
        # La comprobación del dominio subsiste en el código, NO es autenticación segura.
        self.assertIn("@alumno\\.uned\\.es", codigo)

    def test_convocatoria_y_rubricas_opcionales(self):
        codigo = script(CURRENT)
        for ancla in (
            "Normativa · Futuro Docente (UNED)",
            "Convocatoria y criterios del proceso selectivo",
            "normFileBlock('call'",
            "normFileBlock('rubric'",
            "No es necesario aportar estos documentos",
        ):
            self.assertIn(ancla, codigo)

    def test_cobertura_y_documentos_sin_datos_inventados(self):
        codigo = script(CURRENT)
        for ancla in (
            "No se ha identificado automáticamente",
            "Indicio localizado · sin verificar",
            "Cobertura conjunta de la programación",
            "Informe final de cobertura curricular",
            "input[name=exportScope]",
            "Primera tabla de prueba",
            "Todas las tablas de la programación",
            "Descargar",
        ):
            self.assertIn(ancla, codigo)
        self.assertNotIn("exportConfig", codigo)
        self.assertIn("No calculable todavía", codigo)

    def test_sintaxis_javascript(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "prototipo.js"
            archivo.write_text(script(CURRENT), encoding="utf-8")
            salida = subprocess.run(
                ["node", "--check", str(archivo)],
                capture_output=True, text=True,
            )
        self.assertEqual(salida.returncode, 0, salida.stderr)


if __name__ == "__main__":
    unittest.main()
