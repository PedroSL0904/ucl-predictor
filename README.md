# UEFA Champions League Predictor

Pronóstico probabilístico y simulador del torneo completo de la UEFA Champions League, actualizado dinámicamente conforme avanza la competición.

- **Temporada**: 2026-27
- **Progreso del Torneo**: 18 de 144 partidos computados (Jornada 1 concluida)
- **Ultima Actualizacion**: `2026-09-24 11:16 UTC`

---

## 1. Probabilidades de Titulo

Estimaciones calculadas mediante 10,000 simulaciones Monte Carlo considerando el desarrollo de la fase de liga, cruces eliminatorios y sede neutral de la final:

| Posicion | Club | Campeon | Finalista | Semifinales |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Arsenal** | **19.7%** | 31.9% | 47.0% |
| 2 | **Man City** | **15.8%** | 28.1% | 46.4% |
| 3 | **Bayern Munich** | **14.9%** | 28.0% | 48.4% |
| 4 | **Barcelona** | **13.7%** | 24.8% | 42.4% |
| 5 | **Real Madrid** | **8.8%** | 18.9% | 37.5% |
| 6 | **Paris SG** | **5.5%** | 12.6% | 27.2% |
| 7 | **Liverpool** | **5.5%** | 12.9% | 27.6% |
| 8 | **Inter** | **4.8%** | 11.1% | 20.1% |
| 9 | **Manchester United** | **3.4%** | 8.8% | 20.7% |
| 10 | **Dortmund** | **2.7%** | 5.2% | 15.4% |
| 11 | **Aston Villa** | **1.6%** | 4.5% | 13.9% |
| 12 | **Roma** | **0.9%** | 2.1% | 6.7% |

---

## 2. Proyeccion de la Fase de Liga (36 Equipos)

Estructura de clasificacion oficial de la UEFA:
- **Puestos 1 al 8**: Clasificacion directa a Octavos de Final.
- **Puestos 9 al 24**: Ronda eliminatoria de Play-offs (Dieciseisavos de final).
- **Puestos 25 al 36**: Eliminados de la competicion.

| Pos | Club | PJ | Pts Actuales | Dif Gol | Pts Proyectados | Octavos Directos (1-8) | Play-offs (9-24) | Eliminado (25-36) | Estatus Proyectado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
|  1 | **Bayern Munich** | 1 | 3 | +5.0 | 18.8 pts | 88.9% | 11.1% | 0.1% | Octavos Directos |
|  2 | **Real Madrid** | 1 | 3 | +1.0 | 17.6 pts | 75.1% | 24.4% | 0.5% | Octavos Directos |
|  3 | **Liverpool** | 1 | 3 | +1.0 | 17.2 pts | 71.8% | 27.6% | 0.7% | Octavos Directos |
|  4 | **Barcelona** | 1 | 3 | +4.0 | 16.7 pts | 70.5% | 29.0% | 0.4% | Octavos Directos |
|  5 | **Man City** | 1 | 3 | +2.0 | 16.7 pts | 68.2% | 31.1% | 0.7% | Octavos Directos |
|  6 | **Paris SG** | 1 | 3 | +5.0 | 15.8 pts | 58.4% | 39.7% | 1.9% | Octavos Directos |
|  7 | **Dortmund** | 1 | 3 | +1.0 | 15.4 pts | 50.5% | 46.9% | 2.5% | Octavos Directos |
|  8 | **Manchester United** | 1 | 3 | +4.0 | 14.6 pts | 42.3% | 53.8% | 4.0% | Octavos Directos |
|  9 | **Sporting** | 1 | 3 | +2.0 | 14.6 pts | 41.0% | 55.9% | 3.1% | Play-offs |
| 10 | **Aston Villa** | 1 | 3 | +1.0 | 14.4 pts | 39.1% | 56.8% | 4.2% | Play-offs |
| 11 | **Atletico** | 1 | 0 | -1.0 | 14.0 pts | 34.3% | 60.1% | 5.6% | Play-offs |
| 12 | **Arsenal** | 1 | 3 | +1.0 | 14.0 pts | 32.6% | 62.0% | 5.5% | Play-offs |
| 13 | **Porto** | 1 | 0 | -2.0 | 12.7 pts | 18.9% | 68.9% | 12.2% | Play-offs |
| 14 | **Stuttgart** | 1 | 3 | +2.0 | 12.3 pts | 17.8% | 68.9% | 13.3% | Play-offs |
| 15 | **Como** | 1 | 3 | +3.0 | 11.5 pts | 15.3% | 65.3% | 19.3% | Play-offs |
| 16 | **Inter** | 1 | 0 | -1.0 | 11.7 pts | 12.7% | 69.3% | 18.1% | Play-offs |
| 17 | **Lens** | 1 | 3 | +1.0 | 11.2 pts | 10.6% | 65.7% | 23.7% | Play-offs |
| 18 | **Roma** | 1 | 1 | 0.0 | 11.0 pts | 8.6% | 67.7% | 23.8% | Play-offs |
| 19 | **Club Brugge** | 1 | 0 | -1.0 | 10.3 pts | 5.1% | 63.1% | 31.7% | Play-offs |
| 20 | **Shakhtar Donetsk** | 1 | 1 | 0.0 | 10.0 pts | 5.2% | 59.6% | 35.2% | Play-offs |
| 21 | **RB Leipzig** | 1 | 0 | -3.0 | 10.3 pts | 4.9% | 59.1% | 36.0% | Play-offs |
| 22 | **AEK Athens** | 1 | 3 | +1.0 | 10.1 pts | 5.5% | 57.2% | 37.3% | Play-offs |
| 23 | **Real Betis** | 1 | 3 | +1.0 | 9.8 pts | 5.5% | 55.2% | 39.4% | Play-offs |
| 24 | **Lille** | 1 | 0 | -1.0 | 9.4 pts | 3.8% | 55.6% | 40.6% | Play-offs |
| 25 | **Fenerbahce** | 1 | 1 | 0.0 | 9.3 pts | 3.5% | 50.5% | 46.0% | Eliminado |
| 26 | **Villarreal** | 1 | 0 | -1.0 | 9.1 pts | 2.4% | 51.6% | 46.1% | Eliminado |
| 27 | **Slavia Praha** | 1 | 0 | -1.0 | 9.0 pts | 2.2% | 51.0% | 46.8% | Eliminado |
| 28 | **Napoli** | 1 | 0 | -1.0 | 8.8 pts | 2.0% | 48.1% | 49.9% | Eliminado |
| 29 | **PSV Eindhoven** | 1 | 1 | 0.0 | 7.8 pts | 0.9% | 35.6% | 63.4% | Eliminado |
| 30 | **Bodo/Glimt** | 1 | 0 | -5.0 | 7.8 pts | 0.7% | 31.1% | 68.3% | Eliminado |
| 31 | **Galatasaray SK** | 1 | 0 | -2.0 | 7.1 pts | 0.7% | 26.7% | 72.7% | Eliminado |
| 32 | **Feyenoord** | 1 | 0 | -4.0 | 6.9 pts | 0.7% | 22.8% | 76.5% | Eliminado |
| 33 | **LASK** | 1 | 0 | -1.0 | 4.9 pts | 0.2% | 8.6% | 91.2% | Eliminado |
| 34 | **Slovan Bratislava** | 1 | 0 | -5.0 | 5.2 pts | 0.1% | 8.6% | 91.4% | Eliminado |
| 35 | **Viking** | 1 | 0 | -2.0 | 4.7 pts | 0.1% | 7.3% | 92.7% | Eliminado |
| 36 | **Sabah FC** | 1 | 0 | -4.0 | 4.0 pts | 0.0% | 4.2% | 95.8% | Eliminado |

---

## 3. Proyeccion del Cuadro Eliminatorio

### Cruces Proyectados de Play-offs (Dieciseisavos)
- **Serie 1**: Sporting vs Lille — *Pase proyectado: **Sporting** (51.0%)*
- **Serie 2**: Aston Villa vs Real Betis — *Pase proyectado: **Aston Villa** (63.6%)*
- **Serie 3**: Atletico vs AEK Athens — *Pase proyectado: **Atletico** (77.6%)*
- **Serie 4**: Arsenal vs RB Leipzig — *Pase proyectado: **Arsenal** (81.6%)*
- **Serie 5**: Porto vs Shakhtar Donetsk — *Pase proyectado: **Porto** (61.3%)*
- **Serie 6**: Stuttgart vs Club Brugge — *Pase proyectado: **Stuttgart** (52.9%)*
- **Serie 7**: Como vs Roma — *Pase proyectado: **Roma** (57.6%)*
- **Serie 8**: Inter vs Lens — *Pase proyectado: **Inter** (74.0%)*

### Cabezas de Serie Proyectados (Octavos de Final)
Clubs clasificados directamente entre los 8 primeros: **Bayern Munich, Real Madrid, Liverpool, Barcelona, Man City, Paris SG, Dortmund, Manchester United**.

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

