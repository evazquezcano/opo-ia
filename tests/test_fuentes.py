"""Pruebas unitarias de lectura y clasificación técnica de PDF (sin red)."""
import unittest

import fitz

from opoia.fuentes import analizar_pdf, normalizar, url_normativa_valida


def pdf_ejemplo(texto: str | None):
    archivo = fitz.open()
    pagina = archivo.new_page()
    if texto:
        pagina.insert_text((72, 72), texto, fontsize=11)
    datos = archivo.tobytes()
    archivo.close()
    return datos


class PruebasFuentes(unittest.TestCase):
    def test_pdf_legible_y_sin_aprobacion_curricular(self):
        datos = pdf_ejemplo(
            "Decreto de educacion. Competencias especificas. "
            "Criterios de evaluacion. Saberes basicos. Anexo II. "
            "Este documento presenta la normativa del sistema escolar. "
        )
        resultado = analizar_pdf(datos, "decreto.pdf", "Decreto curricular")
        self.assertEqual(resultado["estado"], "PDF_LEGIBLE")
        self.assertEqual(resultado["paginas"], 1)
        self.assertFalse(resultado["curriculo_verificado"])
        self.assertFalse(resultado["vigencia_normativa_verificada"])
        self.assertIn("criterios de evaluación", resultado["indicios_textuales"])

    def test_pdf_con_paginas_de_imagen_requiere_ocr(self):
        resultado = analizar_pdf(pdf_ejemplo(None), "escaneado.pdf", "Decreto curricular")
        self.assertEqual(resultado["estado"], "TEXTO_NO_EXTRAIBLE")
        self.assertFalse(resultado["curriculo_verificado"])

    def test_cabecera_invalida(self):
        resultado = analizar_pdf(b"esto no es PDF", "incorrecto.pdf", "Modificación 1")
        self.assertEqual(resultado["estado"], "ERROR")

    def test_archivo_vacio(self):
        self.assertEqual(analizar_pdf(b"", "vacio.pdf", "Evaluación")["estado"], "ERROR")

    def test_limite_tamano(self):
        from unittest.mock import patch
        with patch("opoia.fuentes.MAX_BYTES", 8):
            self.assertEqual(analizar_pdf(b"%PDF-" + b"x"*20, "grande.pdf", "Currículo")["estado"], "ERROR")

    def test_normalizacion_multilingue(self):
        self.assertEqual(normalizar("Criterios de Evaluación"), "criterios de evaluacion")
        self.assertEqual(normalizar("Competències Específiques"), "competencies especifiques")

    def test_enlaces(self):
        self.assertTrue(url_normativa_valida("https://www.bocm.es/decreto.pdf"))
        self.assertFalse(url_normativa_valida("not a url"))
        self.assertFalse(url_normativa_valida(""))


if __name__ == "__main__":
    unittest.main()
