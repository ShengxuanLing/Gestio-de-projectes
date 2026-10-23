# Gantt y tablero Kanban

Plan del proyecto **Smart Water UAB**. Fechas en dias naturales desde el
**06/10/2026**.

## 1. Gantt

Las barras `crit` son las de la ruta critica (holgura = 0).

```mermaid
gantt
    title Smart Water UAB - 11,67 semanas (82 dias)
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    A Mapear consumo por zona y entrevistar servicios UAB :, crit, 2026-10-06, 2026-10-21
    B Recopilar dataset historico de consumo :, crit, 2026-10-21, 2026-11-07
    C Definir KPIs y umbrales de anomalia :, crit, 2026-11-07, 2026-11-15
    D Disenar arquitectura del sistema de sensores :, 2026-10-06, 2026-10-14
    E Seleccionar y montar componentes :, 2026-10-14, 2026-10-29
    F Implementar lectura y filtrado de datos :, 2026-10-29, 2026-11-13
    G Implementar deteccion de fugas y anomalias :, crit, 2026-11-15, 2026-11-23
    H Ensamblar y documentar el prototipo :, crit, 2026-11-23, 2026-12-02
    I Disenar estructura y storyboard de la web :, 2026-10-06, 2026-10-14
    J Maquetar HTML/CSS responsive :, 2026-10-14, 2026-10-28
    K Visualizar datos (graficos de consumo) :, 2026-11-07, 2026-11-22
    L Integrar datos del prototipo en la web :, crit, 2026-12-02, 2026-12-10
    M Revisar, corregir y publicar :, crit, 2026-12-10, 2026-12-19
    N Redactar la memoria :, 2026-11-15, 2026-11-29
    O Campana de concienciacion :, 2026-11-29, 2026-12-07
    P Presentacion final y entrega :, crit, 2026-12-19, 2026-12-27
```

---

## 2. Tablero Kanban

Una tarjeta por actividad de la WBS. El flujo es `Por hacer` -> `En curso`
-> `Hecho`, y la regla del Kanban es **limitar el trabajo en curso**: pocas
tarjetas en `En curso` a la vez.

| ID | Tarea | Estado | Rol | Start | End | Predec. |
|----|-------|--------|-----|-------|-----|---------|
| A | Mapear consumo por zona y entrevistar servicios UAB | En curso | Analisis de datos | 2026-10-06 | 2026-10-21 | - |
| B | Recopilar dataset historico de consumo | Por hacer | Analisis de datos | 2026-10-21 | 2026-11-07 | A |
| C | Definir KPIs y umbrales de anomalia | Por hacer | Analisis de datos | 2026-11-07 | 2026-11-15 | B |
| D | Disenar arquitectura del sistema de sensores | Por hacer | Sensores y prototipo | 2026-10-06 | 2026-10-14 | - |
| E | Seleccionar y montar componentes | Por hacer | Sensores y prototipo | 2026-10-14 | 2026-10-29 | D |
| F | Implementar lectura y filtrado de datos | Por hacer | Sensores y prototipo | 2026-10-29 | 2026-11-13 | E |
| G | Implementar deteccion de fugas y anomalias | Por hacer | Sensores y prototipo | 2026-11-15 | 2026-11-23 | C, F |
| H | Ensamblar y documentar el prototipo | Por hacer | Sensores y prototipo | 2026-11-23 | 2026-12-02 | G |
| I | Disenar estructura y storyboard de la web | Por hacer | Desarrollo web | 2026-10-06 | 2026-10-14 | - |
| J | Maquetar HTML/CSS responsive | Por hacer | Desarrollo web | 2026-10-14 | 2026-10-28 | I |
| K | Visualizar datos (graficos de consumo) | Por hacer | Desarrollo web | 2026-11-07 | 2026-11-22 | J, B |
| L | Integrar datos del prototipo en la web | Por hacer | Desarrollo web | 2026-12-02 | 2026-12-10 | K, H |
| M | Revisar, corregir y publicar | Por hacer | Desarrollo web | 2026-12-10 | 2026-12-19 | L |
| N | Redactar la memoria | Por hacer | Documentacion | 2026-11-15 | 2026-11-29 | C |
| O | Campana de concienciacion | Por hacer | Documentacion | 2026-11-29 | 2026-12-07 | N |
| P | Presentacion final y entrega | Por hacer | Coordinacion | 2026-12-19 | 2026-12-27 | M, N, O |

---

## 3. Hitos

| Hito | Fecha | Actividad | Entregable |
|------|-------|-----------|------------|
| H2 | 2026-10-29 | E | Sistema de sensores montado |
| H1 | 2026-11-15 | C | KPIs y umbrales de anomalia definidos |
| H4 | 2026-11-22 | K | Graficos de consumo funcionando en la web |
| H3 | 2026-12-02 | H | Prototipo ensamblado y documentado |
| H5 | 2026-12-19 | M | Web revisada, corregida y publicada |
| H6 | 2026-12-27 | P | Entrega final y presentacion |

---

## 4. Importar el tablero en GitHub Projects

1. Abre <https://github.com/users/ShengxuanLing/projects/new>
2. **Projects** -> **New project** -> **Board**
3. En el board: **...** -> **Import** -> sube `docs/tablero.csv`
4. GitHub crea los campos `Status`, `Start` y `End` automaticamente.
5. Cambia la vista a **Roadmap**: las barras `Start`/`End` se convierten en el
   Gantt del proyecto.

> La columna `Assignee` no viene en el CSV a proposito: hay que rellenarla con
> el usuario de GitHub de cada miembro del grupo. El rol de cada tarea ya esta
> en la columna `Rol` y en la tabla RACI del plan de gestion.
