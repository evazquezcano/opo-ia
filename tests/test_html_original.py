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
            "Modificaciones o correcciones curriculares",
            "Orden o decreto de evaluación",
            "No aportes archivos adicionales",
            "normReadPdf",
            "normAnalyze",
            "INDICE_PRELIMINAR",
            "completeCurriculumVerified:false",
        ):
            with self.subTest(ancla=ancla):
                self.assertIn(ancla, codigo)

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
