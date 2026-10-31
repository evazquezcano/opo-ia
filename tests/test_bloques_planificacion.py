"""Regresión del selector de bloques sin navegador ni red."""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


class BloquesPlanificacion(unittest.TestCase):
    def test_modalidades_y_cobertura(self):
        html = (Path(__file__).resolve().parents[1]/"web"/"index.html").read_text("utf-8")
        body = re.search(r"<script>(.*?)</script>", html, re.S).group(1).rsplit("render();", 1)[0]
        code = r"""
const vm=require('vm'),fs=require('fs');
const ctx=vm.createContext({document:{getElementById:()=>({innerHTML:''})},window:{},console});
vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),ctx);
const r=q=>vm.runInContext(q,ctx);
const blocks=['A','B','C','D'].map((codigo,i)=>({codigo,texto:'Bloque '+codigo,pagina_pdf:100+i}));
r('s.normReport='+JSON.stringify({documents:[{type:'curriculum',structured:{candidatos:{bloques:blocks}}}]}));
const eq=(q,exp)=>{const got=Array.from(r(q));if(JSON.stringify(got)!==JSON.stringify(exp))throw new Error(q+': '+JSON.stringify(got))};
eq('propuestaBloques().filas[0].codigos',['A','B','C']);
r("s.blockPolicy='1'");eq('propuestaBloques().filas[1].codigos',['B']);
r("s.blockPolicy='2'");eq('propuestaBloques().filas[0].codigos',['A','B']);
r("s.blockPolicy='all'");eq('propuestaBloques().filas[0].codigos',['A','B','C','D']);
r("s.units[0].blockMode='1'");eq('propuestaBloques().filas[0].codigos',['A']);
r("s.blockPolicy='5'");eq('propuestaBloques().filas[1].codigos',['B','C','D','A']);
r("s.blockPolicy='1'");r("s.units=s.units.slice(0,2)");
if(r('propuestaBloques().pendientes.length')!==2)throw new Error('Sin aviso de bloques faltantes');
const vista=r('stepPlanning()');
if(!vista.includes('id="blockPolicy"')||!vista.includes('data-block-unit="0"'))throw new Error('Selector no incluido');
"""
        with tempfile.TemporaryDirectory() as td:
            js = Path(td)/"original.js"
            js.write_text(body, encoding="utf-8")
            test = Path(td)/"test.cjs"
            test.write_text(code, encoding="utf-8")
            proc = subprocess.run(["node", str(test), str(js)], text=True,
                                  capture_output=True, timeout=25)
        self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
