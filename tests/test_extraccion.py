"""Tests de extracción indexada y separación entre normas, sin conexión externa."""
import unittest

import fitz

from opoia.extraccion import indexar_documento, consolidar_evidencias


def pdf_de_prueba(paginas):
    documento = fitz.open()
    for texto in paginas:
        pagina = documento.new_page()
        pagina.insert_text((50, 60), texto[:450], fontsize=10)
    datos = documento.tobytes()
    documento.close()
    return datos


class PruebasExtraccion(unittest.TestCase):
    def test_indice_localiza_encabezados_y_no_valida_curriculo(self):
        pdf = pdf_de_prueba([
            "Lengua Castellana y Literatura. 3 ESO. "
            "Competencias especificas de la materia. Criterios de evaluacion.",
            "Saberes basicos. Objetivos de la etapa. Descriptores operativos. "
            "Elementos transversales.",
        ])
        resultado = indexar_documento(
            pdf, "decreto.pdf", "Currículo principal",
            "Lengua Castellana y Literatura", "3.º",
        )
        self.assertEqual(resultado["estado"], "INDICE_PRELIMINAR")
        self.assertEqual(resultado["paginas_pdf"], 2)
        self.assertEqual(resultado["paginas_con_materia"], [1])
        self.assertTrue(resultado["indicios_por_elemento"]["competencias_especificas"])
        self.assertTrue(resultado["indicios_por_elemento"]["criterios_evaluacion"])
        self.assertFalse(resultado["revision_literal_completa"])
        self.assertFalse(resultado["revision_vigencia"])

    def test_modificaciones_no_se_aplican_sin_cotejo(self):
        p = indexar_documento(
            pdf_de_prueba(["Competencias especificas y saberes basicos"]),
            "principal.pdf", "Currículo principal", "Matemáticas", "2.º",
        )
        m = indexar_documento(
            pdf_de_prueba(["Correccion de los criterios de evaluacion"]),
            "modificacion.pdf", "Modificación 1", "Matemáticas", "2.º",
        )
        e = indexar_documento(
            pdf_de_prueba(["Normas de evaluacion"]),
            "evaluacion.pdf", "Normativa de evaluación", "Matemáticas", "2.º",
        )
        out = consolidar_evidencias([p, m, e])
        self.assertEqual(len(out["modificaciones"]), 1)
        self.assertEqual(len(out["evaluacion"]), 1)
        self.assertEqual(
            out["modificaciones"][0]["estado"],
            "IMPACTO_JURIDICO_PENDIENTE_DE_COTEJO",
        )
        self.assertFalse(out["curriculo_validado"])
        self.assertFalse(out["puede_generar_unidades_definitivas"])

    def test_rechaza_archivos_no_pdf(self):
        out = indexar_documento(b"<html>texto</html>", "web.pdf",
                               "Currículo principal", "Lengua", "3.º")
        self.assertEqual(out["estado"], "NO_EXTRAIBLE")

    def test_documento_esencial_obligatorio_en_consolidacion(self):
        with self.assertRaises(ValueError):
            consolidar_evidencias([{"funcion": "Modificación 1"}])
        self.assertFalse(consolidar_evidencias([])["curriculo_validado"])


if __name__ == "__main__":
    unittest.main()
