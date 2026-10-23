# -*- coding: utf-8 -*-
"""Genera docs/PLAN-DE-GESTION.md, docs/TABLERO-KANBAN.md y docs/tablero.csv
desde la red PERT. Ejecutar:  python docs/_build_docs.py"""

import csv
import datetime
import io
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = datetime.date(2026, 10, 6)

# ID: (nombre, predecesoras, a, m, b)   duraciones en semanas
A = {
    "A": ("Mapear consumo por zona y entrevistar servicios UAB", [], 1, 2, 4),
    "B": ("Recopilar dataset historico de consumo", ["A"], 1, 2, 5),
    "C": ("Definir KPIs y umbrales de anomalia", ["B"], 1, 1, 2),
    "D": ("Disenar arquitectura del sistema de sensores", [], 1, 1, 2),
    "E": ("Seleccionar y montar componentes", ["D"], 1, 2, 4),
    "F": ("Implementar lectura y filtrado de datos", ["E"], 2, 2, 3),
    "G": ("Implementar deteccion de fugas y anomalias", ["C", "F"], 1, 1, 2),
    "H": ("Ensamblar y documentar el prototipo", ["G"], 1, 1, 3),
    "I": ("Disenar estructura y storyboard de la web", [], 1, 1, 2),
    "J": ("Maquetar HTML/CSS responsive", ["I"], 1, 2, 3),
    "K": ("Visualizar datos (graficos de consumo)", ["J", "B"], 1, 2, 4),
    "L": ("Integrar datos del prototipo en la web", ["K", "H"], 1, 1, 2),
    "M": ("Revisar, corregir y publicar", ["L"], 1, 1, 2),
    "N": ("Redactar la memoria", ["C"], 1, 2, 3),
    "O": ("Campana de concienciacion", ["N"], 1, 1, 2),
    "P": ("Presentacion final y entrega", ["M", "N", "O"], 1, 1, 2),
}

ROLE = {
    "A": "Analisis de datos", "B": "Analisis de datos", "C": "Analisis de datos",
    "D": "Sensores y prototipo", "E": "Sensores y prototyping" if False else "Sensores y prototipo",
    "F": "Sensores y prototipo", "G": "Sensores y prototipo", "H": "Sensores y prototipo",
    "I": "Desarrollo web", "J": "Desarrollo web", "K": "Desarrollo web",
    "L": "Desarrollo web", "M": "Desarrollo web",
    "N": "Documentacion", "O": "Documentacion", "P": "Coordinacion",
}

te = {k: (v[2] + 4 * v[3] + v[4]) / 6 for k, v in A.items()}
var = {k: ((v[4] - v[2]) / 6) ** 2 for k, v in A.items()}

succ = {k: [] for k in A}
for k, v in A.items():
    for p in v[1]:
        succ[p].append(k)

order, seen = [], set()


def visit(n):
    if n in seen:
        return
    seen.add(n)
    for p in A[n][1]:
        visit(p)
    order.append(n)


for n in A:
    visit(n)

ES, EF = {}, {}
for n in order:
    ES[n] = max([EF[p] for p in A[n][1]], default=0.0)
    EF[n] = ES[n] + te[n]
T = max(EF.values())

LF, LS = {}, {}
for n in reversed(order):
    LF[n] = min([LS[s] for s in succ[n]], default=T)
    LS[n] = LF[n] - te[n]

fl = {n: LS[n] - ES[n] for n in A}
crit = [n for n in order if abs(fl[n]) < 1e-9]
sig = math.sqrt(sum(var[n] for n in crit))


def DT(weeks):
    return (START + datetime.timedelta(days=int(round(weeks * 7)))).isoformat()


def DD(weeks):
    return int(round(weeks * 7))


def es(x):
    return ("%.2f" % x).replace(".", ",")


def cdf(pl):
    return 0.5 * (1 + math.erf(((pl - T) / sig) / math.sqrt(2)))


STATE = {n: ("En curso" if n == "A" else "Por hacer") for n in order}

MILESTONES = [
    ("H1", "C", "KPIs y umbrales de anomalia definidos"),
    ("H2", "E", "Sistema de sensores montado"),
    ("H3", "H", "Prototipo ensamblado y documentado"),
    ("H4", "K", "Graficos de consumo funcionando en la web"),
    ("H5", "M", "Web revisada, corregida y publicada"),
    ("H6", "P", "Entrega final y presentacion"),
]
MILESTONES.sort(key=lambda x: EF[x[1]])


def write_plan():
    P = []
    p = P.append
    p("# Plan de gestion - Smart Water UAB")
    p("")
    p("Gestion inteligente del agua en el campus de la UAB.")
    p("")
    p("| | |")
    p("|---|---|")
    p("| **Enfoque** | Opcion 1 - Campus UAB |")
    p("| **Sector** | Gestion del agua (ODS 6 y ODS 11) |")
    p("| **Inicio** | 06/10/2026 |")
    p("| **Fin previsto** | %s |" % (START + datetime.timedelta(days=82)).strftime("%d/%m/%Y"))
    p("| **Duracion PERT** | %s semanas |" % es(T))
    p("| **Ruta critica** | %s |" % " -> ".join(crit))
    p("")
    p("> **Unidades.** La red PERT esta en *semanas*. El Gantt esta en *dias")
    p("> naturales*: %s semanas x 7 = 82 dias." % es(T))
    p("")
    p("---")
    p("")
    p("## 1. WBS y red PERT")
    p("")
    p("Regla del 100 %: cada paquete de trabajo es un entregable, y las letras A-P")
    p("son las actividades de la red. No hay trabajo fuera de esta estructura.")
    p("")
    p("### 1.1 Actividades, duraciones y predecesoras")
    p("")
    p("| ID | Actividad | Predec. | a | m | b | te | o2 |")
    p("|----|-----------|---------|---|---|---|----|----|")
    for n in order:
        nm, _, a_, m_, b_ = A[n]
        p("| %s | %s | %s | %d | %d | %d | %s | %s |"
          % (n, nm, ", ".join(A[n][1]) if A[n][1] else "-", a_, m_, b_, es(te[n]), es(var[n])))
    p("")
    p("```")
    p("te = (a + 4*m + b) / 6")
    p("o2 = ((b - a) / 6)^2")
    p("```")
    p("")
    p("### 1.2 ES, EF, LS, LF y holguras")
    p("")
    p("| ID | te | ES | EF | LS | LF | Holgura |")
    p("|----|----|----|----|----|----|---------|")
    for n in order:
        star = "**" + es(fl[n]) + "**" if abs(fl[n]) < 1e-9 else es(fl[n])
        p("| %s | %s | %s | %s | %s | %s | %s |"
          % (n, es(te[n]), es(ES[n]), es(EF[n]), es(LS[n]), es(LF[n]), star))
    p("")
    p("**Lectura de la red:**")
    p("")
    p("- **Duracion: %s semanas.** sigma = %s sem. P(T <= 12) = %s %% y P(T <= 11) = %s %%."
      % (es(T), es(sig), es(cdf(12) * 100), es(cdf(11) * 100)))
    p("- **Ruta critica: %s.** Ocho actividades; cualquier retraso ahi retrasa la entrega." % " -> ".join(crit))
    p("- **B es la actividad mas incierta** (o2 = %s, la mayor de la red): depende de que datos"
      % es(var["B"]))
    p("  publicen o faciliten los servicios de la UAB. Atacar esa incertidumbre es lo")
    p("  primero que conviene hacer.")
    p("- **I y J tienen 2,83 semanas de holgura:** la web puede absorber un retraso del")
    p("  prototipo sin mover la fecha de entrega.")
    p("- **D, E y F tienen solo 0,17 semanas de holgura.** Aunque no son criticas, G depende")
    p("  de F y F casi no puede moverse: 2 dias de retraso en F ya retrasan la entrega.")
    p("- **Ruta critica alternativa: D -> E -> F -> G -> H -> L -> M -> P = 11,50 sem,** solo")
    p("  0,17 semanas por detras. Si el bloque de sensores se atrasa, esta ruta manda.")
    p("")
    p("### 1.3 Probabilidad de plazo")
    p("")
    p("| Plazo | z | P(T <= plazo) |")
    p("|-------|---|--------------|")
    for pl in (11, 12, 13):
        p("| %d sem | %s | %s %% |" % (pl, es((pl - T) / sig), es(cdf(pl) * 100)))
    p("")
    p("```")
    p("P(T <= plazo) = DISTR.NORM.ESTAND((plazo - T) / sigma)")
    p("```")
    p("")
    p("---")
    p("")
    p("## 2. Gantt")
    p("")
    p("Dias naturales desde el 06/10/2026. Barras `###` = ruta critica; `---` = con holgura.")
    p("")
    p("| ID | Actividad | Ini | Fin | Dur | Barra |")
    p("|----|-----------|-----|-----|-----|-------|")
    for n in order:
        d0, d1 = DD(ES[n]), DD(EF[n])
        p("| %s | %s | S%d | E%d | %d | %s |"
          % (n, A[n][0], d0, d1, d1 - d0, ("###" if n in crit else "---") * (d1 - d0)))
    p("")
    p("S0 = 06/10/2026. Total: 82 dias naturales.")
    p("")
    p("---")
    p("")
    p("## 3. Hitos")
    p("")
    p("| Hito | Fecha | Actividad | Entregable |")
    p("|------|-------|-----------|------------|")
    for h, n, ent in MILESTONES:
        p("| %s | %s | %s | %s |" % (h, DT(EF[n]), n, ent))
    p("")
    p("---")
    p("")
    p("## 4. Plantilla Excel (formulas)")
    p("")
    p("Para replicar esta red en una hoja de calculo:")
    p("")
    p("```")
    p("=SI.ERROR((A2+4*M2+B2)/6;\"\")          <- te")
    p("=((B2-A2)/6)^2                          <- o2")
    p("=MAX(EF de las predecesoras)            <- ES   (ida)")
    p("=ES2+te2                                <- EF   (ida)")
    p("=MIN(LS de las sucesoras)               <- LF   (vuelta)")
    p("=LF2-te2                                <- LS   (vuelta)")
    p("=LS2-ES2                                <- holgura; 0 = critica")
    p("=DISTR.NORM.ESTAND((plazo-T)/sigma)    <- P(T <= plazo)")
    p("```")
    p("")
    p("---")
    p("")
    p("## 5. Reparto de roles y RACI")
    p("")
    p("| Actividades | R (responsable) | A (aprueba) | C (consulta) | I (informado) |")
    p("|-------------|-----------------|-------------|---------------|---------------|")
    p("| A, B, C | Analisis de datos | Coordinacion | Servicios UAB | Todo el grupo |")
    p("| D, E, F, G, H | Sensores y prototipo | Coordinacion | Analisis de datos | Todo el grupo |")
    p("| I, J, K, L, M | Desarrollo web | Coordinacion | Analisis de datos | Todo el grupo |")
    p("| N, O | Documentacion y comunicacion | Coordinacion | Todo el grupo | Tutor/a |")
    p("| P | Coordinacion | Tutor/a | Todo el grupo | Tutor/a |")
    p("")
    p("> Los **roles** estan asignados por paquete de trabajo. Al repartir el rol")
    p("> *Coordinacion* entre una persona concreta, esa persona queda como")
    p("> responsable de las 16 actividades de la red en el tablero.")
    p("")
    open(os.path.join(BASE, "docs", "PLAN-DE-GESTION.md"), "w", encoding="utf-8").write("\n".join(P))


def write_kanban():
    M = []
    m = M.append
    m("# Gantt y tablero Kanban")
    m("")
    m("Plan del proyecto **Smart Water UAB**. Fechas en dias naturales desde el")
    m("**06/10/2026**.")
    m("")
    m("## 1. Gantt")
    m("")
    m("Las barras `crit` son las de la ruta critica (holgura = 0).")
    m("")
    m("```mermaid")
    m("gantt")
    m("    title Smart Water UAB - %s semanas (82 dias)" % es(T))
    m("    dateFormat  YYYY-MM-DD")
    m("    axisFormat  %d/%m")
    m("")
    for n in order:
        tag = ", crit" if n in crit else ""
        m("    %s %s :%s, %s, %s" % (n, A[n][0], tag, DT(ES[n]), DT(EF[n])))
    m("```")
    m("")
    m("---")
    m("")
    m("## 2. Tablero Kanban")
    m("")
    m("Una tarjeta por actividad de la WBS. El flujo es `Por hacer` -> `En curso`")
    m("-> `Hecho`, y la regla del Kanban es **limitar el trabajo en curso**: pocas")
    m("tarjetas en `En curso` a la vez.")
    m("")
    m("| ID | Tarea | Estado | Rol | Start | End | Predec. |")
    m("|----|-------|--------|-----|-------|-----|---------|")
    for n in order:
        m("| %s | %s | %s | %s | %s | %s | %s |"
          % (n, A[n][0], STATE[n], ROLE[n], DT(ES[n]), DT(EF[n]),
             ", ".join(A[n][1]) if A[n][1] else "-"))
    m("")
    m("---")
    m("")
    m("## 3. Hitos")
    m("")
    m("| Hito | Fecha | Actividad | Entregable |")
    m("|------|-------|-----------|------------|")
    for h, n, ent in MILESTONES:
        m("| %s | %s | %s | %s |" % (h, DT(EF[n]), n, ent))
    m("")
    m("---")
    m("")
    m("## 4. Importar el tablero en GitHub Projects")
    m("")
    m("1. Abre <https://github.com/users/ShengxuanLing/projects/new>")
    m("2. **Projects** -> **New project** -> **Board**")
    m("3. En el board: **...** -> **Import** -> sube `docs/tablero.csv`")
    m("4. GitHub crea los campos `Status`, `Start` y `End` automaticamente.")
    m("5. Cambia la vista a **Roadmap**: las barras `Start`/`End` se convierten en el")
    m("   Gantt del proyecto.")
    m("")
    m("> La columna `Assignee` no viene en el CSV a proposito: hay que rellenarla con")
    m("> el usuario de GitHub de cada miembro del grupo. El rol de cada tarea ya esta")
    m("> en la columna `Rol` y en la tabla RACI del plan de gestion.")
    m("")
    open(os.path.join(BASE, "docs", "TABLERO-KANBAN.md"), "w", encoding="utf-8").write("\n".join(M))


def write_csv():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["Title", "Status", "Start", "End", "Labels", "Rol", "Predecesoras", "Horas"])
    for n in order:
        w.writerow([
            "%s - %s" % (n, A[n][0]),
            STATE[n],
            DT(ES[n]),
            DT(EF[n]),
            "critica" if n in crit else "con-holgura",
            ROLE[n],
            " ".join(A[n][1]),
            "%g" % round(te[n] * 40),
        ])
    path = os.path.join(BASE, "docs", "tablero.csv")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "docs"), exist_ok=True)
    write_plan()
    write_kanban()
    write_csv()
    print("OK plan=%s crit=%s sig=%s" % (es(T), "-".join(crit), es(sig)))
    for h, n, _ in MILESTONES:
        print("  %s %s %s" % (h, DT(EF[n]), n))
