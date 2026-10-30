#!/usr/bin/env python3
"""Auditoría preliminar de metadatos de fuentes, no validación jurídica."""
import json, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
doc=json.loads((root/"datos/catalogo_51_autonomicos.json").read_text(encoding="utf-8"))
rows=doc["registros"]
assert len(rows)==51
assert len(set(r["id"] for r in rows))==51
stages=("primaria","eso","bachillerato")
regions={r["id"].split("-")[0] for r in rows}
assert len(regions)==17
for code in regions:
    assert {r["etapa"] for r in rows if r["id"].startswith(code+"-")}==set(stages)
for r in rows:
    assert r["url"].startswith("https://")
    assert r.get("habilitado_para_generar") is False
    assert r.get("curriculo_materia_verificado") is False
print("Catálogo: 51 entradas de 17 comunidades, tres etapas y ningún currículo habilitado sin validación.")
