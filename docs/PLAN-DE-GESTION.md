# Plan de gestion - Smart Water UAB

Gestion inteligente del agua en el campus de la UAB.

| | |
|---|---|
| **Enfoque** | Opcion 1 - Campus UAB |
| **Sector** | Gestion del agua (ODS 6 y ODS 11) |
| **Inicio** | 06/10/2026 |
| **Fin previsto** | 27/12/2026 |
| **Duracion PERT** | 11,67 semanas |
| **Ruta critica** | A -> B -> C -> G -> H -> L -> M -> P |

> **Unidades.** La red PERT esta en *semanas*. El Gantt esta en *dias
> naturales*: 11,67 semanas x 7 = 82 dias.

---

## 1. WBS y red PERT

Regla del 100 %: cada paquete de trabajo es un entregable, y las letras A-P
son las actividades de la red. No hay trabajo fuera de esta estructura.

### 1.1 Actividades, duraciones y predecesoras

| ID | Actividad | Predec. | a | m | b | te | o2 |
|----|-----------|---------|---|---|---|----|----|
| A | Mapear consumo por zona y entrevistar servicios UAB | - | 1 | 2 | 4 | 2,17 | 0,25 |
| B | Recopilar dataset historico de consumo | A | 1 | 2 | 5 | 2,33 | 0,44 |
| C | Definir KPIs y umbrales de anomalia | B | 1 | 1 | 2 | 1,17 | 0,03 |
| D | Disenar arquitectura del sistema de sensores | - | 1 | 1 | 2 | 1,17 | 0,03 |
| E | Seleccionar y montar componentes | D | 1 | 2 | 4 | 2,17 | 0,25 |
| F | Implementar lectura y filtrado de datos | E | 2 | 2 | 3 | 2,17 | 0,03 |
| G | Implementar deteccion de fugas y anomalias | C, F | 1 | 1 | 2 | 1,17 | 0,03 |
| H | Ensamblar y documentar el prototipo | G | 1 | 1 | 3 | 1,33 | 0,11 |
| I | Disenar estructura y storyboard de la web | - | 1 | 1 | 2 | 1,17 | 0,03 |
| J | Maquetar HTML/CSS responsive | I | 1 | 2 | 3 | 2,00 | 0,11 |
| K | Visualizar datos (graficos de consumo) | J, B | 1 | 2 | 4 | 2,17 | 0,25 |
| L | Integrar datos del prototipo en la web | K, H | 1 | 1 | 2 | 1,17 | 0,03 |
| M | Revisar, corregir y publicar | L | 1 | 1 | 2 | 1,17 | 0,03 |
| N | Redactar la memoria | C | 1 | 2 | 3 | 2,00 | 0,11 |
| O | Campana de concienciacion | N | 1 | 1 | 2 | 1,17 | 0,03 |
| P | Presentacion final y entrega | M, N, O | 1 | 1 | 2 | 1,17 | 0,03 |

```
te = (a + 4*m + b) / 6
o2 = ((b - a) / 6)^2
```

### 1.2 ES, EF, LS, LF y holguras

| ID | te | ES | EF | LS | LF | Holgura |
|----|----|----|----|----|----|---------|
| A | 2,17 | 0,00 | 2,17 | 0,00 | 2,17 | **0,00** |
| B | 2,33 | 2,17 | 4,50 | 2,17 | 4,50 | **0,00** |
| C | 1,17 | 4,50 | 5,67 | 4,50 | 5,67 | **0,00** |
| D | 1,17 | 0,00 | 1,17 | 0,17 | 1,33 | 0,17 |
| E | 2,17 | 1,17 | 3,33 | 1,33 | 3,50 | 0,17 |
| F | 2,17 | 3,33 | 5,50 | 3,50 | 5,67 | 0,17 |
| G | 1,17 | 5,67 | 6,83 | 5,67 | 6,83 | **0,00** |
| H | 1,33 | 6,83 | 8,17 | 6,83 | 8,17 | **0,00** |
| I | 1,17 | 0,00 | 1,17 | 2,83 | 4,00 | 2,83 |
| J | 2,00 | 1,17 | 3,17 | 4,00 | 6,00 | 2,83 |
| K | 2,17 | 4,50 | 6,67 | 6,00 | 8,17 | 1,50 |
| L | 1,17 | 8,17 | 9,33 | 8,17 | 9,33 | **0,00** |
| M | 1,17 | 9,33 | 10,50 | 9,33 | 10,50 | **0,00** |
| N | 2,00 | 5,67 | 7,67 | 7,33 | 9,33 | 1,67 |
| O | 1,17 | 7,67 | 8,83 | 9,33 | 10,50 | 1,67 |
| P | 1,17 | 10,50 | 11,67 | 10,50 | 11,67 | **0,00** |

**Lectura de la red:**

- **Duracion: 11,67 semanas.** sigma = 0,97 sem. P(T <= 12) = 63,42 % y P(T <= 11) = 24,64 %.
- **Ruta critica: A -> B -> C -> G -> H -> L -> M -> P.** Ocho actividades; cualquier retraso ahi retrasa la entrega.
- **B es la actividad mas incierta** (o2 = 0,44, la mayor de la red): depende de que datos
  publicen o faciliten los servicios de la UAB. Atacar esa incertidumbre es lo
  primero que conviene hacer.
- **I y J tienen 2,83 semanas de holgura:** la web puede absorber un retraso del
  prototipo sin mover la fecha de entrega.
- **D, E y F tienen solo 0,17 semanas de holgura.** Aunque no son criticas, G depende
  de F y F casi no puede moverse: 2 dias de retraso en F ya retrasan la entrega.
- **Ruta critica alternativa: D -> E -> F -> G -> H -> L -> M -> P = 11,50 sem,** solo
  0,17 semanas por detras. Si el bloque de sensores se atrasa, esta ruta manda.

### 1.3 Probabilidad de plazo

| Plazo | z | P(T <= plazo) |
|-------|---|--------------|
| 11 sem | -0,69 | 24,64 % |
| 12 sem | 0,34 | 63,42 % |
| 13 sem | 1,37 | 91,50 % |

```
P(T <= plazo) = DISTR.NORM.ESTAND((plazo - T) / sigma)
```

---

## 2. Gantt

Dias naturales desde el 06/10/2026. Barras `###` = ruta critica; `---` = con holgura.

| ID | Actividad | Ini | Fin | Dur | Barra |
|----|-----------|-----|-----|-----|-------|
| A | Mapear consumo por zona y entrevistar servicios UAB | S0 | E15 | 15 | ############################################# |
| B | Recopilar dataset historico de consumo | S15 | E32 | 17 | ################################################### |
| C | Definir KPIs y umbrales de anomalia | S32 | E40 | 8 | ######################## |
| D | Disenar arquitectura del sistema de sensores | S0 | E8 | 8 | ------------------------ |
| E | Seleccionar y montar componentes | S8 | E23 | 15 | --------------------------------------------- |
| F | Implementar lectura y filtrado de datos | S23 | E38 | 15 | --------------------------------------------- |
| G | Implementar deteccion de fugas y anomalias | S40 | E48 | 8 | ######################## |
| H | Ensamblar y documentar el prototipo | S48 | E57 | 9 | ########################### |
| I | Disenar estructura y storyboard de la web | S0 | E8 | 8 | ------------------------ |
| J | Maquetar HTML/CSS responsive | S8 | E22 | 14 | ------------------------------------------ |
| K | Visualizar datos (graficos de consumo) | S32 | E47 | 15 | --------------------------------------------- |
| L | Integrar datos del prototipo en la web | S57 | E65 | 8 | ######################## |
| M | Revisar, corregir y publicar | S65 | E74 | 9 | ########################### |
| N | Redactar la memoria | S40 | E54 | 14 | ------------------------------------------ |
| O | Campana de concienciacion | S54 | E62 | 8 | ------------------------ |
| P | Presentacion final y entrega | S74 | E82 | 8 | ######################## |

S0 = 06/10/2026. Total: 82 dias naturales.

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

## 4. Plantilla Excel (formulas)

Para replicar esta red en una hoja de calculo:

```
=SI.ERROR((A2+4*M2+B2)/6;"")          <- te
=((B2-A2)/6)^2                          <- o2
=MAX(EF de las predecesoras)            <- ES   (ida)
=ES2+te2                                <- EF   (ida)
=MIN(LS de las sucesoras)               <- LF   (vuelta)
=LF2-te2                                <- LS   (vuelta)
=LS2-ES2                                <- holgura; 0 = critica
=DISTR.NORM.ESTAND((plazo-T)/sigma)    <- P(T <= plazo)
```

---

## 5. Reparto de roles y RACI

| Actividades | R (responsable) | A (aprueba) | C (consulta) | I (informado) |
|-------------|-----------------|-------------|---------------|---------------|
| A, B, C | Analisis de datos | Coordinacion | Servicios UAB | Todo el grupo |
| D, E, F, G, H | Sensores y prototipo | Coordinacion | Analisis de datos | Todo el grupo |
| I, J, K, L, M | Desarrollo web | Coordinacion | Analisis de datos | Todo el grupo |
| N, O | Documentacion y comunicacion | Coordinacion | Todo el grupo | Tutor/a |
| P | Coordinacion | Tutor/a | Todo el grupo | Tutor/a |

> Los **roles** estan asignados por paquete de trabajo. Al repartir el rol
> *Coordinacion* entre una persona concreta, esa persona queda como
> responsable de las 16 actividades de la red en el tablero.
