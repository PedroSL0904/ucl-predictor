# UEFA Champions League Predictor

Pronóstico probabilístico y simulador del torneo completo de la UEFA Champions League, actualizado dinámicamente conforme avanza la competición.

- **Temporada**: 2026-27
- **Progreso del Torneo**: 36 de 144 partidos computados (Jornada 2 concluida)
- **Ultima Actualizacion**: `2026-10-22 11:18 UTC`

---

## 1. Probabilidades de Titulo

Estimaciones calculadas mediante 10,000 simulaciones Monte Carlo considerando el desarrollo de la fase de liga, cruces eliminatorios y sede neutral de la final:

| Posicion | Club | Campeon | Finalista | Semifinales |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Arsenal** | **22.2%** | 36.1% | 52.4% |
| 2 | **Bayern Munich** | **14.6%** | 26.6% | 45.5% |
| 3 | **Man City** | **14.6%** | 25.3% | 41.4% |
| 4 | **Barcelona** | **14.5%** | 27.0% | 45.4% |
| 5 | **Real Madrid** | **8.5%** | 17.3% | 35.9% |
| 6 | **Paris SG** | **7.0%** | 15.0% | 32.5% |
| 7 | **Liverpool** | **4.5%** | 11.8% | 29.6% |
| 8 | **Inter** | **4.5%** | 8.6% | 16.4% |
| 9 | **Manchester United** | **3.2%** | 7.6% | 16.4% |
| 10 | **Aston Villa** | **2.1%** | 7.0% | 18.6% |
| 11 | **Dortmund** | **1.3%** | 4.2% | 10.8% |
| 12 | **Atletico** | **0.9%** | 3.2% | 10.2% |

---

## 2. Proyeccion de la Fase de Liga (36 Equipos)

Estructura de clasificacion oficial de la UEFA:
- **Puestos 1 al 8**: Clasificacion directa a Octavos de Final.
- **Puestos 9 al 24**: Ronda eliminatoria de Play-offs (Dieciseisavos de final).
- **Puestos 25 al 36**: Eliminados de la competicion.

| Pos | Club | PJ | Pts Actuales | Dif Gol | Pts Proyectados | Octavos Directos (1-8) | Play-offs (9-24) | Eliminado (25-36) | Estatus Proyectado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
|  1 | **Liverpool** | 2 | 6 | +4.0 | 18.1 pts | 82.5% | 17.4% | 0.1% | Octavos Directos |
|  2 | **Paris SG** | 2 | 6 | +7.0 | 17.8 pts | 79.7% | 20.2% | 0.1% | Octavos Directos |
|  3 | **Real Madrid** | 2 | 6 | +2.0 | 18.1 pts | 79.4% | 20.6% | 0.0% | Octavos Directos |
|  4 | **Bayern Munich** | 2 | 4 | +5.0 | 17.1 pts | 75.1% | 24.6% | 0.3% | Octavos Directos |
|  5 | **Barcelona** | 2 | 6 | +7.0 | 16.8 pts | 71.2% | 28.7% | 0.1% | Octavos Directos |
|  6 | **Aston Villa** | 2 | 6 | +7.0 | 15.9 pts | 59.2% | 40.2% | 0.6% | Octavos Directos |
|  7 | **Sporting** | 2 | 6 | +4.0 | 16.0 pts | 56.6% | 42.5% | 0.9% | Octavos Directos |
|  8 | **Arsenal** | 2 | 6 | +4.0 | 15.4 pts | 47.9% | 51.1% | 1.0% | Octavos Directos |
|  9 | **Man City** | 2 | 3 | 0.0 | 15.4 pts | 49.4% | 49.1% | 1.5% | Play-offs |
| 10 | **Atletico** | 2 | 3 | +1.0 | 15.2 pts | 47.5% | 50.7% | 1.8% | Play-offs |
| 11 | **Dortmund** | 2 | 3 | 0.0 | 13.1 pts | 21.6% | 70.5% | 7.8% | Play-offs |
| 12 | **Manchester United** | 2 | 3 | +2.0 | 12.9 pts | 20.5% | 71.2% | 8.2% | Play-offs |
| 13 | **Club Brugge** | 2 | 3 | 0.0 | 12.9 pts | 15.2% | 76.1% | 8.6% | Play-offs |
| 14 | **Stuttgart** | 2 | 6 | +5.0 | 12.5 pts | 16.6% | 74.3% | 9.2% | Play-offs |
| 15 | **Villarreal** | 2 | 3 | +1.0 | 12.4 pts | 14.5% | 75.4% | 10.0% | Play-offs |
| 16 | **RB Leipzig** | 2 | 3 | -2.0 | 12.6 pts | 12.8% | 74.1% | 13.2% | Play-offs |
| 17 | **Shakhtar Donetsk** | 2 | 4 | +2.0 | 12.2 pts | 14.2% | 73.9% | 11.9% | Play-offs |
| 18 | **Real Betis** | 2 | 6 | +2.0 | 11.7 pts | 10.1% | 72.6% | 17.3% | Play-offs |
| 19 | **Lens** | 2 | 3 | -1.0 | 10.7 pts | 4.7% | 69.3% | 26.0% | Play-offs |
| 20 | **Roma** | 2 | 1 | -1.0 | 10.4 pts | 4.0% | 66.0% | 29.9% | Play-offs |
| 21 | **Inter** | 2 | 0 | -2.0 | 10.2 pts | 3.4% | 66.7% | 29.9% | Play-offs |
| 22 | **Porto** | 2 | 0 | -3.0 | 10.3 pts | 3.0% | 66.8% | 30.1% | Play-offs |
| 23 | **Bodo/Glimt** | 2 | 3 | -4.0 | 10.4 pts | 2.8% | 60.7% | 36.5% | Play-offs |
| 24 | **Como** | 2 | 3 | +2.0 | 9.3 pts | 3.0% | 55.9% | 41.1% | Play-offs |
| 25 | **Lille** | 2 | 0 | -4.0 | 8.8 pts | 1.0% | 48.2% | 50.7% | Eliminado |
| 26 | **Feyenoord** | 2 | 3 | -3.0 | 8.9 pts | 1.3% | 43.0% | 55.7% | Eliminado |
| 27 | **AEK Athens** | 2 | 3 | -1.0 | 8.2 pts | 0.8% | 38.2% | 61.0% | Eliminado |
| 28 | **Napoli** | 2 | 0 | -3.0 | 7.2 pts | 0.4% | 28.3% | 71.3% | Eliminado |
| 29 | **Sabah FC** | 2 | 3 | -2.0 | 7.8 pts | 0.7% | 27.6% | 71.8% | Eliminado |
| 30 | **PSV Eindhoven** | 2 | 1 | -1.0 | 6.6 pts | 0.4% | 22.7% | 76.8% | Eliminado |
| 31 | **Viking** | 2 | 1 | -2.0 | 6.7 pts | 0.4% | 21.1% | 78.5% | Eliminado |
| 32 | **Slavia Praha** | 2 | 0 | -3.0 | 6.3 pts | 0.1% | 19.8% | 80.2% | Eliminado |
| 33 | **Galatasaray SK** | 2 | 0 | -5.0 | 5.6 pts | 0.1% | 13.2% | 86.8% | Eliminado |
| 34 | **Fenerbahce** | 2 | 1 | -6.0 | 5.7 pts | 0.1% | 10.9% | 88.9% | Eliminado |
| 35 | **LASK** | 2 | 0 | -4.0 | 4.3 pts | 0.0% | 4.8% | 95.2% | Eliminado |
| 36 | **Slovan Bratislava** | 2 | 0 | -8.0 | 3.9 pts | 0.0% | 3.2% | 96.8% | Eliminado |

---

## 3. Proyeccion del Cuadro Eliminatorio

### Cruces Proyectados de Play-offs (Dieciseisavos)
- **Serie 1**: Man City vs Como — *Pase proyectado: **Man City** (76.8%)*
- **Serie 2**: Atletico vs Bodo/Glimt — *Pase proyectado: **Atletico** (76.3%)*
- **Serie 3**: Dortmund vs Porto — *Pase proyectado: **Dortmund** (60.9%)*
- **Serie 4**: Manchester United vs Inter — *Pase proyectado: **Inter** (57.8%)*
- **Serie 5**: Club Brugge vs Roma — *Pase proyectado: **Roma** (63.5%)*
- **Serie 6**: Stuttgart vs Lens — *Pase proyectado: **Lens** (50.6%)*
- **Serie 7**: Villarreal vs Real Betis — *Pase proyectado: **Villarreal** (52.5%)*
- **Serie 8**: RB Leipzig vs Shakhtar Donetsk — *Pase proyectado: **RB Leipzig** (60.8%)*

### Cabezas de Serie Proyectados (Octavos de Final)
Clubs clasificados directamente entre los 8 primeros: **Liverpool, Paris SG, Real Madrid, Bayern Munich, Barcelona, Aston Villa, Sporting, Arsenal**.

---

## 4. Pronosticos de la Proxima Jornada (Jornada 3)

Pronósticos probabilísticos detallados de los 18 encuentros programados:

| Partido | Probabilidades 1X2 | Pronostico | Marcador Probable |
| :--- | :---: | :---: | :---: |
| **Club Brugge** vs **Slavia Praha** | `L 64% / E 21% / V 15%` | **Local** | `2-1` |
| **Roma** vs **Villarreal** | `L 54% / E 24% / V 22%` | **Local** | `2-1` |
| **Real Betis** vs **Sporting** | `L 26% / E 21% / V 54%` | **Visitante** | `1-2` |
| **Real Madrid** vs **RB Leipzig** | `L 74% / E 15% / V 11%` | **Local** | `3-1` |
| **Bodo/Glimt** vs **Lens** | `L 30% / E 28% / V 42%` | **Visitante** | `0-2` |
| **Manchester United** vs **Man City** | `L 30% / E 23% / V 47%` | **Visitante** | `1-2` |
| **Barcelona** vs **Stuttgart** | `L 67% / E 20% / V 14%` | **Local** | `2-1` |
| **Liverpool** vs **Fenerbahce** | `L 78% / E 14% / V 8%` | **Local** | `2-0` |
| **Porto** vs **Como** | `L 45% / E 26% / V 29%` | **Local** | `2-1` |
| **Dortmund** vs **Feyenoord** | `L 71% / E 17% / V 12%` | **Local** | `2-1` |
| **Napoli** vs **Paris SG** | `L 17% / E 17% / V 66%` | **Visitante** | `1-2` |
| **PSV Eindhoven** vs **Lille** | `L 44% / E 26% / V 30%` | **Local** | `2-1` |
| **Aston Villa** vs **AEK Athens** | `L 66% / E 18% / V 16%` | **Local** | `2-1` |
| **Bayern Munich** vs **Inter** | `L 61% / E 20% / V 19%` | **Local** | `2-1` |
| **Arsenal** vs **Shakhtar Donetsk** | `L 75% / E 15% / V 10%` | **Local** | `2-0` |
| **Slovan Bratislava** vs **Atletico** | `L 13% / E 18% / V 69%` | **Visitante** | `1-3` |
| **LASK** vs **Sabah FC** | `L 44% / E 24% / V 32%` | **Local** | `2-0` |
| **Viking** vs **Galatasaray SK** | `L 30% / E 21% / V 49%` | **Visitante** | `1-2` |

---

## 5. Actualizacion del Sistema

Este repositorio actualiza todas sus proyecciones de manera continua. Cada vez que concluye una jornada y se registran los marcadores oficiales, el motor recalcula las probabilidades de victoria de cada partido restante, actualiza la tabla de posiciones simulada y proyecta de nuevo los favoritos al titulo.

