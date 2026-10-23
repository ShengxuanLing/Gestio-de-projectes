# -*- coding: utf-8 -*-
"""Crea una Issue por cada actividad de la WBS en GitHub.

Las Issues son la fuente de verdad del tablero: el CSV de
docs/tablero.csv se importa despues en GitHub Projects y las Issues se
anaden al board desde la propia vista.

Uso:  python docs/_seed_issues.py
"""

import csv
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "ShengxuanLing/Trabajo_Gesti-projectes"
CSV_PATH = os.path.join(BASE, "docs", "tablero.csv")

DESCRIPTION = """Actividad **{id}** de la WBS del proyecto Smart Water UAB.

| | |
|---|---|
| **Estado** | {status} |
| **Rol** | {rol} |
| **Ventana** | {start} -> {end} |
| **Horas estimadas** | {horas} h |
| **Predecesoras** | {pred} |
| **Ruta critica** | {crit} |

**Regla del 100 %.** Esta actividad es un entregable del plan: describe
del trabajo, y solo del trabajo.

**Dependencias:** {pred_long}

---

Fuentes del plan

- Tablero completo: `docs/TABLERO-KANBAN.md`
- Plan de gestion (WBS + PERT + Gantt): `docs/PLAN-DE-GESTION.md`
"""


def gh(*args):
    return subprocess.run(
        ["gh"] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def main():
    with open(CSV_PATH, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    for row in rows:
        title = row["Title"]
        act_id = title.split(" - ", 1)[0]
        pred = row["Predecesoras"].strip()
        is_crit = row["Labels"] == "critica"

        pred_long = (
            "ninguna: es una actividad de arranque."
            if not pred
            else "depende de " + ", ".join(pred) + "."
        )

        body = DESCRIPTION.format(
            id=act_id,
            status=row["Status"],
            rol=row["Rol"],
            start=row["Start"],
            end=row["End"],
            horas=row["Horas"],
            pred=pred or "-",
            pred_long=pred_long,
            crit="**si**" if is_crit else "no",
        )

        res = gh(
            "issue", "create",
            "--repo", REPO,
            "--title", title,
            "--body", body,
            "--label", row["Labels"],
        )
        if res.returncode != 0:
            print("FAIL %s: %s" % (act_id, res.stderr.strip()[:200]))
        else:
            print("ok   %s -> %s" % (act_id, res.stdout.strip()))

    print("--- labels ---")
    for label, desc in (
        ("critica", "Actividad en la ruta critica (holgura = 0)"),
        ("con-holgura", "Actividad con holgura"),
        ("wbs", "Actividad de la WBS"),
    ):
        res = gh("label", "create", label, "--repo", REPO,
                 "--description", desc, "--color", "0e8a16", "--force")
        print(("ok   " if res.returncode == 0 else "skip ") + label)


if __name__ == "__main__":
    main()
