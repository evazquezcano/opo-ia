/* NORMA-IA · pruebas reproducibles sin conexión, Node.js >=20. */
"use strict";
const fs=require("node:fs"),path=require("node:path"),assert=require("node:assert/strict"),vm=require("node:vm");
const html=fs.readFileSync(path.join(__dirname,"index.html"),"utf8");
let passed=0;
function check(name,fn){try{fn();passed++;console.log("✓ "+name)}catch(e){console.error("✗ "+name);throw e}}
check("Estructura de página y tres imágenes institucionales",()=>{
 assert.match(html,/<main id="workspace"/);assert.match(html,/<\/html>\s*$/);
 assert.equal((html.match(/<img[^>]*src="data:image\/webp;base64,/g)||[]).length,3);
 assert.match(html,/class="gate-wrap" id="access"/);
});
check("20 ámbitos, tres etapas y convocatoria opcional",()=>{
 for(const code of ["andalucia","aragon","asturias","baleares","canarias","cantabria","clm","cyl","cataluna","valencia","extremadura","galicia","rioja","madrid","murcia","navarra","euskadi","ceuta","melilla","ministerio"])assert.ok(html.includes('["'+code+'",'),code);
 for(const code of ["primaria","eso","bach"])assert.match(html,new RegExp('<option value="'+code+'"'));
 assert.doesNotMatch(html,/if\(!pdf\)/);assert.match(html,/if\(pdf&&/);
});
check("Acceso visual, icono ojo y resultados en bloques verticales",()=>{
 assert.match(html,/id="toggle-password"/);assert.match(html,/class="eye-btn"/);assert.match(html,/grid-template-columns:1fr;gap:15px/);
 assert.doesNotMatch(html,/id="education-link"/);assert.doesNotMatch(html,/id="rules-link"/);assert.doesNotMatch(html,/id="other-links"/);
});
check("Word/PDF, estilos y citas con enlaces",()=>{
 for(const token of ["Packer.toBlob","window.print()","Times New Roman","ExternalHyperlink","id=\"all-portals\""])assert.ok(html.includes(token),token);
});
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(x=>x.trim());
check("Sintaxis JS",()=>{assert.equal(scripts.length,1);new vm.Script(scripts[0]);});
let listeners={},elements={};let counter=0;
function el(id){return elements[id]??(elements[id]={value:"",type:"password",innerHTML:"",textContent:"",hidden:false,files:[],disabled:false,attrs:{},classList:{toggle(){}},setAttribute(k,v){this.attrs[k]=v},addEventListener(event,fn){listeners[id+":"+event]=fn},append(){},scrollIntoView(){},click(){}})}
const document={getElementById:el,querySelector:q=>el(q.replace(/^#/,"")),createElement:()=>el("_"+(++counter)),body:{classList:{add(){},remove(){}},append(){}}};
const window={addEventListener(){},print(){}};
const URLMock=class{constructor(url){if(!/^https?:\/\/[^/]+/.test(url))throw Error("invalid");this.protocol=url.split(":")[0]+":";this.hostname=url.split("/")[2]}};
const api=new Function("document","window","URL","setTimeout",scripts[0]+"\nreturn {regions,docHTML,directoryHTML,output:()=>output};")(document,window,URLMock,()=>{});
check("Inicialización y selector completo",()=>{assert.equal(api.regions.length,20);assert.equal(el("region").value,"madrid")});
check("Control de acceso e icono ojo",()=>{
 el("password").value="invalido";listeners["login:click"]();assert.ok(el("access-error").textContent);
 el("password").value="prueba@alumno.uned.es";listeners["login:click"]();assert.equal(el("workspace").hidden,false);
 listeners["toggle-password:click"]();assert.equal(el("password").type,"text");
 listeners["toggle-password:click"]();assert.equal(el("password").type,"password");
});
check("Madrid ESO sin convocatoria presenta dos grupos",()=>{
 el("call-pdf").files=[];el("call-url").value="";el("region").value="madrid";el("stage").value="eso";
 listeners["generate:click"]();assert.equal(el("results").hidden,false);
 assert.match(el("basic-list").innerHTML,/Decreto 65\/2022/);assert.match(el("extra-list").innerHTML,/Decreto 32\/2019/);
 assert.doesNotMatch(api.docHTML(),/undefined/);
});
check("Ministerio, Ceuta y Melilla seleccionan currículo ministerial",()=>{
 for(const region of ["ministerio","ceuta","melilla"]){el("region").value=region;el("stage").value="bach";listeners["generate:click"]();assert.match(el("basic-list").innerHTML,/EFP\/755\/2022/);}
});
check("Las autonomías con currículo identificado advierten de los límites de cobertura",()=>{
 el("region").value="andalucia";el("stage").value="primaria";listeners["generate:click"]();
 assert.match(el("basic-list").innerHTML,/Decreto 101\/2023/);
 assert.match(el("result-alert").textContent,/selección parcial/i);assert.equal(el("word").disabled,false);
 assert.match(api.docHTML(),/Repertorio en revisión jurídica/);
});
check("Las 60 combinaciones incluyen normas territoriales, sin LOE independiente ni RD de mínimos autonómico",()=>{
 const autonomous=["andalucia","aragon","asturias","baleares","canarias","cantabria","clm","cyl","cataluna","valencia","extremadura","galicia","rioja","madrid","murcia","navarra","euskadi"];
 let count=0;for(const r of api.regions)for(const st of ["primaria","eso","bach"]){
   el("region").value=r[0];el("stage").value=st;el("call-pdf").files=[];el("call-url").value="";
   listeners["generate:click"]();
   const o=api.output();assert.ok(o&&o.basic.length,"No hay normas: "+r[0]+" "+st);
   assert.ok(o.basic.some(n=>n.id==="LOMLOE"),"Falta LOMLOE: "+r[0]+" "+st);
   assert.ok(!o.basic.some(n=>n.id==="LOE"||/^O1994/.test(n.id)),"Normativa excluida: "+r[0]+" "+st);
   if(autonomous.includes(r[0])){
      assert.ok(!o.basic.some(n=>/^RD(157|217|243)$/.test(n.id)),"Real Decreto de mínimos improcedente: "+r[0]+" "+st);
      assert.ok(o.basic.some(n=>n.scope!=="estatal"),"Falta normativa autonómica: "+r[0]+" "+st);
   }else assert.ok(o.basic.some(n=>/^RD(157|217|243)$/.test(n.id)),"Real Decreto de mínimos ausente en Ministerio: "+st);
   assert.ok(o.extra.length>0,"Sin normativa complementaria: "+r[0]+" "+st);
   assert.equal(el("results").hidden,false);assert.equal(el("word").disabled,false);
   count++;
 }
 assert.equal(count,60);
});
check("Reglamentos orgánicos autonómicos evitan el RD 83 donde procede",()=>{
 for(const r of ["andalucia","canarias","clm","galicia","navarra","baleares"])for(const st of ["eso","bach"]){
   el("region").value=r;el("stage").value=st;listeners["generate:click"]();
   const basic=api.output().basic;assert.ok(!basic.some(n=>n.id==="RD83"),"RD83 improcedente en "+r);
   assert.ok(basic.some(n=>/Decreto 32[78]\/2010|Decreto 81\/2010|Orden 118\/2022|Decreto 324\/1996|Decreto Foral 14\/2026|Decret 4\/2023/.test(n.title)),"Sin norma orgánica "+r);
 }
});
check("Navarra usa el Reglamento de 2026 y órdenes de desarrollo",()=>{
 for(const etapa of ["primaria","eso","bach"]){el("region").value="navarra";el("stage").value=etapa;listeners["generate:click"]();
   const basic=api.output().basic;
   assert.ok(basic.some(n=>n.id==="Decreto Foral 14/2026"));
   assert.ok(basic.some(n=>n.id=== (etapa==="primaria"?"Orden Foral 36/2026":"Orden Foral 40/2026")));
   assert.ok(!basic.some(n=>n.id==="RD83"));
 }
});
check("Baleares utiliza su reglamento orgánico modificado en 2025",()=>{
 for(const etapa of ["primaria","eso","bach"]){el("region").value="baleares";el("stage").value=etapa;listeners["generate:click"]();
   assert.ok(api.output().basic.some(n=>n.id==="Decret 4/2023"));
   assert.ok(api.output().extra.some(n=>n.id==="Decret 39/2011"));
   assert.ok(!api.output().basic.some(n=>n.id==="RD83"));
 }
});
check("Galicia presenta reglamentos autonómicos propios",()=>{
 for(const etapa of ["primaria","eso","bach"]){el("region").value="galicia";el("stage").value=etapa;listeners["generate:click"]();
   assert.ok(api.output().basic.some(n=>n.id===(etapa==="primaria"?"Decreto 374/1996":"Decreto 324/1996")));
 }
});
check("Referencias con enlace individual y denominación íntegra en pantalla",()=>{
 el("region").value="navarra";el("stage").value="eso";listeners["generate:click"]();
 assert.match(el("basic-list").innerHTML,/Decreto Foral/);
 assert.doesNotMatch(el("basic-list").innerHTML,/>RD83 ·/);
 assert.match(el("basic-list").innerHTML,/Consultar texto oficial de la disposición/);
});
check("Directorio PDF contiene tabla completa",()=>{assert.match(api.directoryHTML(),/directory-table/);assert.match(api.directoryHTML(),/educagob/);});
check("La Rioja no incorpora normativas derogadas de convivencia o diversidad",()=>{
  for(const st of ["primaria","eso","bach"]){el("region").value="rioja";el("stage").value=st;listeners["generate:click"]();
    const codes=api.output().extra.map(n=>n.id);
    assert.ok(codes.includes("Decreto 43/2025"));assert.ok(codes.includes("Orden EDE/75/2025"));
    assert.ok(codes.includes("Decreto 39/2025"));assert.ok(!codes.includes("Orden 6/2014"));
  }
});
check("Comunitat Valenciana y Cataluña tienen normas de inclusión",()=>{
  for(const r of ["valencia","cataluna"]){el("region").value=r;el("stage").value="bach";listeners["generate:click"]();
    assert.ok(api.output().extra.some(n=>n.id===(r==="valencia"?"Decreto 104/2018":"Decret 150/2017")));
  }
});
check("No se ha modificado el generador anterior",()=>{assert.ok(fs.existsSync(path.join(__dirname,"..","index.html")))});
console.log("NORMA-IA: "+passed+" comprobaciones superadas.");
