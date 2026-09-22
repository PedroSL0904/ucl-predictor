# UEFA Champions League Predictor

Pronóstico probabilístico y simulador del torneo completo de la UEFA Champions League, actualizado dinámicamente conforme avanza la competición.

- **Temporada**: 2026-27
- **Progreso del Torneo**: 18 de 144 partidos computados (Jornada 1 concluida)
- **Ultima Actualizacion**: `2026-09-22 11:07 UTC`

---

## 1. Probabilidades de Titulo

Estimaciones calculadas mediante 10,000 simulaciones Monte Carlo considerando el desarrollo de la fase de liga, cruces eliminatorios y sede neutral de la final:

| Posicion | Club | Campeon | Finalista | Semifinales |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Arsenal** | **22.6%** | 35.6% | 50.4% |
| 2 | **Man City** | **17.3%** | 29.8% | 47.0% |
| 3 | **Bayern Munich** | **13.9%** | 26.2% | 44.4% |
| 4 | **Barcelona** | **11.2%** | 22.4% | 40.6% |
| 5 | **Paris SG** | **6.7%** | 13.9% | 29.1% |
| 6 | **Real Madrid** | **6.6%** | 15.8% | 32.6% |
| 7 | **Inter** | **5.3%** | 11.6% | 21.2% |
| 8 | **Liverpool** | **4.9%** | 12.3% | 27.3% |
| 9 | **Manchester United** | **3.1%** | 8.0% | 21.7% |
| 10 | **Aston Villa** | **2.2%** | 6.2% | 16.3% |
| 11 | **Dortmund** | **2.1%** | 5.6% | 16.1% |
| 12 | **Atletico** | **0.8%** | 2.5% | 9.3% |

---

## 2. Proyeccion de la Fase de Liga (36 Equipos)

Estructura de clasificacion oficial de la UEFA:
- **Puestos 1 al 8**: Clasificacion directa a Octavos de Final.
- **Puestos 9 al 24**: Ronda eliminatoria de Play-offs (Dieciseisavos de final).
- **Puestos 25 al 36**: Eliminados de la competicion.

| Pos | Club | PJ | Pts Actuales | Dif Gol | Pts Proyectados | Octavos Directos (1-8) | Play-offs (9-24) | Eliminado (25-36) | Estatus Proyectado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
|  1 | **Bayern Munich** | 1 | 3 | +5.0 | 18.5 pts | 87.2% | 12.7% | 0.1% | Octavos Directos |
|  2 | **Liverpool** | 1 | 3 | +1.0 | 17.4 pts | 76.3% | 23.2% | 0.5% | Octavos Directos |
|  3 | **Man City** | 1 | 3 | +2.0 | 16.9 pts | 71.0% | 28.1% | 0.8% | Octavos Directos |
|  4 | **Barcelona** | 1 | 3 | +4.0 | 16.6 pts | 69.0% | 30.0% | 0.9% | Octavos Directos |
|  5 | **Real Madrid** | 1 | 3 | +1.0 | 17.0 pts | 69.8% | 29.8% | 0.3% | Octavos Directos |
|  6 | **Paris SG** | 1 | 3 | +5.0 | 15.5 pts | 55.2% | 42.7% | 2.1% | Octavos Directos |
|  7 | **Dortmund** | 1 | 3 | +1.0 | 15.3 pts | 51.6% | 46.5% | 1.9% | Octavos Directos |
|  8 | **Manchester United** | 1 | 3 | +4.0 | 14.5 pts | 42.5% | 54.5% | 2.9% | Octavos Directos |
|  9 | **Aston Villa** | 1 | 3 | +1.0 | 14.8 pts | 43.7% | 52.3% | 4.0% | Play-offs |
| 10 | **Arsenal** | 1 | 3 | +1.0 | 14.5 pts | 39.5% | 56.5% | 4.0% | Play-offs |
| 11 | **Sporting** | 1 | 3 | +2.0 | 14.0 pts | 36.8% | 57.7% | 5.5% | Play-offs |
| 12 | **Atletico** | 1 | 0 | -1.0 | 13.9 pts | 34.2% | 59.6% | 6.2% | Play-offs |
| 13 | **Porto** | 1 | 0 | -2.0 | 12.5 pts | 17.5% | 70.0% | 12.4% | Play-offs |
| 14 | **Stuttgart** | 1 | 3 | +2.0 | 12.0 pts | 16.2% | 67.0% | 16.8% | Play-offs |
| 15 | **Inter** | 1 | 0 | -1.0 | 11.5 pts | 11.2% | 70.3% | 18.4% | Play-offs |
| 16 | **Lens** | 1 | 3 | +1.0 | 11.3 pts | 11.2% | 66.4% | 22.4% | Play-offs |
| 17 | **Como** | 1 | 3 | +3.0 | 11.1 pts | 12.4% | 64.4% | 23.2% | Play-offs |
| 18 | **Roma** | 1 | 1 | 0.0 | 10.9 pts | 8.0% | 66.2% | 25.9% | Play-offs |
| 19 | **Shakhtar Donetsk** | 1 | 1 | 0.0 | 10.6 pts | 7.4% | 64.4% | 28.1% | Play-offs |
| 20 | **AEK Athens** | 1 | 3 | +1.0 | 10.3 pts | 5.9% | 59.8% | 34.4% | Play-offs |
| 21 | **Real Betis** | 1 | 3 | +1.0 | 10.1 pts | 5.9% | 57.4% | 36.7% | Play-offs |
| 22 | **Club Brugge** | 1 | 0 | -1.0 | 10.2 pts | 5.1% | 60.3% | 34.5% | Play-offs |
| 23 | **RB Leipzig** | 1 | 0 | -3.0 | 10.3 pts | 5.5% | 58.8% | 35.7% | Play-offs |
| 24 | **Villarreal** | 1 | 0 | -1.0 | 9.2 pts | 2.6% | 52.4% | 45.0% | Play-offs |
| 25 | **Lille** | 1 | 0 | -1.0 | 9.1 pts | 3.0% | 50.2% | 46.8% | Eliminado |
| 26 | **Slavia Praha** | 1 | 0 | -1.0 | 8.9 pts | 2.3% | 48.9% | 48.8% | Eliminado |
| 27 | **Fenerbahce** | 1 | 1 | 0.0 | 8.9 pts | 2.4% | 47.9% | 49.6% | Eliminado |
| 28 | **Napoli** | 1 | 0 | -1.0 | 8.7 pts | 2.1% | 46.0% | 51.9% | Eliminado |
| 29 | **PSV Eindhoven** | 1 | 1 | 0.0 | 8.1 pts | 1.7% | 37.2% | 61.1% | Eliminado |
| 30 | **Bodo/Glimt** | 1 | 0 | -5.0 | 8.5 pts | 0.9% | 39.5% | 59.7% | Eliminado |
| 31 | **Galatasaray SK** | 1 | 0 | -2.0 | 6.7 pts | 0.7% | 24.0% | 75.3% | Eliminado |
| 32 | **Feyenoord** | 1 | 0 | -4.0 | 6.8 pts | 0.4% | 23.3% | 76.3% | Eliminado |
| 33 | **Viking** | 1 | 0 | -2.0 | 5.1 pts | 0.1% | 9.5% | 90.3% | Eliminado |
| 34 | **LASK** | 1 | 0 | -1.0 | 4.9 pts | 0.1% | 8.8% | 91.1% | Eliminado |
| 35 | **Slovan Bratislava** | 1 | 0 | -5.0 | 5.2 pts | 0.1% | 9.4% | 90.5% | Eliminado |
| 36 | **Sabah FC** | 1 | 0 | -4.0 | 4.1 pts | 0.1% | 4.0% | 96.0% | Eliminado |

---

## 3. Proyeccion del Cuadro Eliminatorio

### Cruces Proyectados de Play-offs (Dieciseisavos)
- **Serie 1**: Aston Villa vs Villarreal — *Pase proyectado: **Aston Villa** (61.2%)*
- **Serie 2**: Arsenal vs RB Leipzig — *Pase proyectado: **Arsenal** (81.6%)*
- **Serie 3**: Sporting vs Club Brugge — *Pase proyectado: **Sporting** (58.3%)*
- **Serie 4**: Atletico vs Real Betis — *Pase proyectado: **Atletico** (57.5%)*
- **Serie 5**: Porto vs AEK Athens — *Pase proyectado: **Porto** (72.7%)*
- **Serie 6**: Stuttgart vs Shakhtar Donetsk — *Pase proyectado: **Stuttgart** (59.7%)*
- **Serie 7**: Inter vs Roma — *Pase proyectado: **Inter** (65.2%)*
- **Serie 8**: Lens vs Como — *Pase proyectado: **Como** (52.7%)*

### Cabezas de Serie Proyectados (Octavos de Final)
Clubs clasificados directamente entre los 8 primeros: **Bayern Munich, Liverpool, Man City, Barcelona, Real Madrid, Paris SG, Dortmund, Manchester United**.

---

## 4. Pronosticos de la Proxima Jornada (Jornada 2)

Pronósticos probabilísticos detallados de los 18 encuentros programados:

| Partido | Probabilidades 1X2 | Pronostico | Marcador Probable |
| :--- | :---: | :---: | :---: |
| **Lens** vs **Sporting** | `L 19% / E 17% / V 64%` | **Visitante** | `1-2` |
| **Sabah FC** vs **Slavia Praha** | `L 10% / E 15% / V 75%` | **Visitante** | `1-2` |
| **Arsenal** vs **Lille** | `L 63% / E 18% / V 19%` | **Local** | `2-1` |
| **Atletico** vs **Manchester United** | `L 33% / E 22% / V 45%` | **Visitante** | `1-2` |
| **Inter** vs **Club Brugge** | `L 55% / E 20% / V 25%` | **Local** | `2-1` |
| **Galatasaray SK** vs **Barcelona** | `L 10% / E 13% / V 76%` | **Visitante** | `1-2` |
| **RB Leipzig** vs **PSV Eindhoven** | `L 41% / E 24% / V 35%` | **Local** | `2-1` |
| **Viking** vs **Bayern Munich** | `L 6% / E 10% / V 83%` | **Visitante** | `1-2` |
| **Villarreal** vs **Napoli** | `L 25% / E 21% / V 54%` | **Visitante** | `1-2` |
| **Feyenoord** vs **Como** | `L 19% / E 22% / V 59%` | **Visitante** | `1-2` |
| **LASK** vs **Liverpool** | `L 7% / E 11% / V 82%` | **Visitante** | `0-1` |
| **Roma** vs **Real Madrid** | `L 15% / E 16% / V 69%` | **Visitante** | `1-2` |
| **Aston Villa** vs **Fenerbahce** | `L 44% / E 20% / V 36%` | **Local** | `2-1` |
| **Shakhtar Donetsk** vs **AEK Athens** | `L 44% / E 25% / V 32%` | **Local** | `2-1` |
| **Bodo/Glimt** vs **Dortmund** | `L 13% / E 18% / V 69%` | **Visitante** | `0-2` |
| **Man City** vs **Paris SG** | `L 38% / E 21% / V 41%` | **Visitante** | `1-2` |
| **Real Betis** vs **Porto** | `L 20% / E 17% / V 63%` | **Visitante** | `1-2` |
| **Slovan Bratislava** vs **Stuttgart** | `L 14% / E 19% / V 66%` | **Visitante** | `1-3` |

---

## 5. Actualizacion del Sistema

Este repositorio actualiza todas sus proyecciones de manera continua. Cada vez que concluye una jornada y se registran los marcadores oficiales, el motor recalcula las probabilidades de victoria de cada partido restante, actualiza la tabla de posiciones simulada y proyecta de nuevo los favoritos al titulo.

