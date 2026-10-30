#!/usr/bin/env python3
"""Prepara inventario legible de un respaldo de GitHub Actions y del repositorio."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

root = Path("export_github")
runs = json.loads((root / "acciones" / "ejecuciones.json").read_text(encoding="utf-8"))
all_runs = runs.get("workflow_runs", [])
ids = [str(r["id"]) for r in all_runs]
(root / "acciones" / "run_ids.txt").write_text("\n".join(ids)+"\n", encoding="utf-8")
info = {
    "nombre": "OPO-IA – Respaldo integral de repositorio y artefactos",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "repositorio": os.environ.get("GITHUB_REPOSITORY"),
    "commit": os.environ.get("GITHUB_SHA"),
    "cantidad_ejecuciones_registradas": len(ids),
    "ejecuciones": [
        {
            "id": r["id"], "workflow": r.get("name"), "estado": r.get("status"),
            "resultado": r.get("conclusion"), "url": r.get("html_url"),
            "fecha": r.get("created_at"),
        } for r in all_runs
    ],
    "advertencia": (
        "GitHub Actions puede tener errores por ejecución. Los currículos no "
        "están completamente verificados. La descarga no equivale a validación."
    )
}
(root / "MANIFIESTO_GITHUB.json").write_text(
    json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
print("Ejecuciones inventariadas:",len(ids))
