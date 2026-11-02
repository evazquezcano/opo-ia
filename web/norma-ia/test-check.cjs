/* NORMA-IA: comprobaciones estáticas reproducibles, sin dependencias externas. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const path=require("node:path");
const file=path.join(__dirname,"index.html");
const h=fs.readFileSync(file,"utf8");
const checks=[];
function test(name,callback){callback();checks.push(name);}
test("HTML de una sola página",()=>{assert.match(h,/<!doctype html>/i);assert.match(h,/<main id="workspace"/);assert.match(h,/<\/html>\s*$/);});
test("Tres logotipos institucionales incrustados",()=>{assert.equal((h.match(/<img[^>]*src="data:image\/webp;base64,/g)||[]).length,3);});
test("Diecisiete comunidades y ámbitos de Ceuta y Melilla",()=>{const codes=["andalucia","aragon","asturias","baleares","canarias","cantabria","clm","cyl","cataluna","valencia","extremadura","galicia","rioja","madrid","murcia","navarra","euskadi","ceuta","melilla"];for(const code of codes){assert.ok(h.includes('["'+code+'",'),'Falta ámbito '+code)}});
test("Tres etapas y convocatoria obligatoria",()=>{for(const st of ["primaria","eso","bach"]){assert.match(h,new RegExp('<option value="'+st+'"'));}assert.match(h,/id="call-pdf"/);assert.match(h,/if\(!pdf\)/);});
test("Filtro de acceso, sin base de datos ni envío de PDFs",()=>{assert.match(h,/@alumno\\\.uned\\\.es/);assert.doesNotMatch(h,/\bfetch\s*\(\s*["']?https?:\/\/[^)]*\b(formData|pdf)/i);});
test("Normativa básica y complementaria diferenciadas",()=>{assert.match(h,/id="basic-list"/);assert.match(h,/id="extra-list"/);assert.match(h,/Normativa básica/);assert.match(h,/Normativa complementaria/);});
test("Exportación Word y PDF",()=>{assert.match(h,/id="word"/);assert.match(h,/id="pdf"/);assert.match(h,/Times New Roman/);assert.match(h,/window\.print\(\)/);assert.match(h,/Packer\.toBlob/);assert.match(h,/ExternalHyperlink/);});
test("Directorio oficial y accesos territoriales",()=>{assert.match(h,/id="education-link"/);assert.match(h,/id="rules-link"/);assert.match(h,/id="all-portals"/);assert.match(h,/die\.caib\.es\/normativa/);});
test("Comunidades no validadas bloquean la exportación",()=>{assert.match(h,/byid\("word"\)\.disabled=!configured/);assert.match(h,/byid\("pdf"\)\.disabled=!configured/);});
test("No se conserva el enlace defectuoso de la Orden 2067/2023",()=>{assert.doesNotMatch(h,/sites\/default\/files\/doc\/educacion\/univ\/orden2067_2023_bachillerato\.pdf/);assert.match(h,/docs\/assets\/2023\/06\/23\/orden2067_2023_bachillerato\.pdf/);});
test("JavaScript de la aplicación sin errores sintácticos",()=>{const scripts=[...h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(x=>x.trim());assert.equal(scripts.length,1);new vm.Script(scripts[0],{filename:"norma-ia-inline.js"});});
test("Aplicación curricular anterior conservada en su ruta",()=>{const original=path.resolve(__dirname,"..","index.html");assert.ok(fs.existsSync(original),"No se encuentra el generador curricular original")});
console.log("NORMA-IA: "+checks.length+" comprobaciones superadas.\n- "+checks.join("\n- "));
