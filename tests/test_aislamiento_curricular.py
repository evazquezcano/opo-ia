"""Comprueba que la extracción documental no mezcle otras materias ni cursos."""
from pathlib import Path
import subprocess
import tempfile
import unittest

HTML = (Path(__file__).resolve().parents[1] / "web" / "index.html").read_text("utf-8")


class PruebaAislamientoCurricular(unittest.TestCase):
    def test_curso_y_materia_precisos(self):
        inicio = HTML.index("function normStructuredFromPages(pages){")
        final = HTML.index("async function normReadPdf(doc,pdfjs)", inicio)
        algoritmo = HTML[inicio:final]
        cabecera = r"""
        const normFold=x=>String(x||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').replace(/\s+/g,' ').trim();
        const s={subject:'Lengua Castellana y Literatura',grade:'3.º',stage:'ESO'};
        const pages=[
            {page:1,text:'BIOLOGÍA Y GEOLOGÍA\nCompetencias específicas.\n1. Competencia distinta.\n\n3º ESO.\nCriterios de evaluación.\n1.1. Biología, no incluir.\nContenidos.\nA. Células.\n– Membrana.'},
            {page:2,text:'LENGUA CASTELLANA Y LITERATURA\nCompetencias específicas.\n1. Conocer y valorar la diversidad lingüística.\n\n2. Comprender textos.'},
            {page:3,text:'1º ESO.\nCriterios de evaluación.\n1.1. Primer curso, excluir.\nContenidos.\nA. Contenido de primero.'},
            {page:4,text:'3º ESO.\nCriterios de evaluación.\nCompetencia específica 1.\n1.1. Reconocer y valorar las variedades lingüísticas.\n1.2. Identificar estereotipos lingüísticos.\nContenidos.\nA. Las lenguas y sus hablantes.\n– Conocimiento de las variedades lingüísticas.'},
            {page:5,text:'LENGUA EXTRANJERA\nCompetencias específicas.\n1. Otra competencia.\n3º ESO.\nCriterios de evaluación.\n1.1. Otro idioma, excluir.'}
        ];
        """
        comprobacion = r"""
        const result=normStructuredFromPages(pages);
        const c=result.candidatos;
        if(c.competencias.length!==2||c.criterios.length!==2||
           c.bloques.length!==1||c.saberes.length!==1||
           result.ambito_pdf.pagina_curso!==4) {
            throw new Error("Selección curricular incorrecta: "+JSON.stringify({
                com:c.competencias.length,crit:c.criterios.length,
                blocks:c.bloques.length,saberes:c.saberes.length,
                ambito:result.ambito_pdf
            }));
        }
        if(c.criterios.some(x=>x.texto.includes("Biología")||
            x.texto.includes("Primer curso")||x.texto.includes("Otro idioma"))){
            throw new Error("Contaminación con materias o cursos ajenos");
        }
        console.log("Selección curricular aislada correctamente");
        """
        with tempfile.TemporaryDirectory() as folder:
            ruta = Path(folder) / "verificar.js"
            ruta.write_text(cabecera + algoritmo + comprobacion, encoding="utf-8")
            result = subprocess.run(["node", str(ruta)],
                                    capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
