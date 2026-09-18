# UEFA Champions League Predictor

Pronóstico probabilístico y simulador del torneo completo de la UEFA Champions League, actualizado dinámicamente conforme avanza la competición.

- **Temporada**: 2026-27
- **Progreso del Torneo**: 18 de 144 partidos computados (Jornada 1 concluida)
- **Ultima Actualizacion**: `2026-09-17 23:13 UTC`

---

## 1. Probabilidades de Titulo

Estimaciones calculadas mediante 10,000 simulaciones Monte Carlo considerando el desarrollo de la fase de liga, cruces eliminatorios y sede neutral de la final:

| Posicion | Club | Campeon | Finalista | Semifinales |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Arsenal** | **17.0%** | 25.3% | 48.4% |
| 2 | **Man City** | **13.1%** | 21.2% | 42.2% |
| 3 | **Barcelona** | **11.5%** | 19.5% | 37.2% |
| 4 | **Bayern Munich** | **11.2%** | 19.6% | 39.3% |
| 5 | **Inter** | **8.2%** | 16.9% | 33.1% |
| 6 | **Real Madrid** | **7.8%** | 15.2% | 31.1% |
| 7 | **Paris SG** | **7.0%** | 14.8% | 29.6% |
| 8 | **Liverpool** | **5.9%** | 12.7% | 26.6% |
| 9 | **Aston Villa** | **5.2%** | 10.8% | 21.4% |
| 10 | **Dortmund** | **3.4%** | 9.0% | 20.4% |
| 11 | **Roma** | **3.1%** | 9.3% | 18.5% |
| 12 | **Porto** | **1.6%** | 5.2% | 10.2% |

---

## 2. Proyeccion de la Fase de Liga (36 Equipos)

Estructura de clasificacion oficial de la UEFA:
- **Puestos 1 al 8**: Clasificacion directa a Octavos de Final.
- **Puestos 9 al 24**: Ronda eliminatoria de Play-offs (Dieciseisavos de final).
- **Puestos 25 al 36**: Eliminados de la competicion.

| Pos | Club | PJ | Pts Actuales | Dif Gol | Pts Proyectados | Octavos Directos (1-8) | Play-offs (9-24) | Eliminado (25-36) | Estatus Proyectado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
|  1 | **Man City** | 1 | 3 | +2.0 | 18.2 pts | 86.1% | 13.6% | 0.3% | Octavos Directos |
|  2 | **Liverpool** | 1 | 3 | +1.0 | 17.0 pts | 77.0% | 22.7% | 0.3% | Octavos Directos |
|  3 | **Barcelona** | 1 | 3 | +4.0 | 16.1 pts | 69.2% | 29.5% | 1.3% | Octavos Directos |
|  4 | **Bayern Munich** | 1 | 3 | +5.0 | 15.8 pts | 66.0% | 31.9% | 2.0% | Octavos Directos |
|  5 | **Aston Villa** | 1 | 3 | +1.0 | 15.9 pts | 64.5% | 34.0% | 1.6% | Octavos Directos |
|  6 | **Arsenal** | 1 | 3 | +1.0 | 15.5 pts | 59.2% | 38.6% | 2.2% | Octavos Directos |
|  7 | **Dortmund** | 1 | 3 | +1.0 | 15.1 pts | 53.6% | 42.9% | 3.5% | Octavos Directos |
|  8 | **Real Madrid** | 1 | 3 | +1.0 | 14.9 pts | 51.6% | 45.1% | 3.2% | Octavos Directos |
|  9 | **Paris SG** | 1 | 3 | +5.0 | 13.9 pts | 43.2% | 51.5% | 5.2% | Play-offs |
| 10 | **Lens** | 1 | 3 | +1.0 | 13.9 pts | 39.0% | 53.4% | 7.6% | Play-offs |
| 11 | **Como** | 1 | 3 | +3.0 | 12.5 pts | 25.7% | 62.8% | 11.6% | Play-offs |
| 12 | **Inter** | 1 | 0 | -1.0 | 11.8 pts | 16.7% | 65.3% | 18.0% | Play-offs |
| 13 | **Porto** | 1 | 0 | -2.0 | 11.9 pts | 18.4% | 61.6% | 20.1% | Play-offs |
| 14 | **Roma** | 1 | 1 | 0.0 | 11.5 pts | 17.4% | 60.6% | 21.9% | Play-offs |
| 15 | **Stuttgart** | 1 | 3 | +2.0 | 11.1 pts | 15.1% | 59.6% | 25.3% | Play-offs |
| 16 | **Real Betis** | 1 | 3 | +1.0 | 10.5 pts | 8.3% | 58.6% | 33.1% | Play-offs |
| 17 | **Villarreal** | 1 | 0 | -1.0 | 10.3 pts | 7.9% | 59.5% | 32.6% | Play-offs |
| 18 | **Shakhtar Donetsk** | 1 | 1 | 0.0 | 10.3 pts | 7.8% | 58.7% | 33.5% | Play-offs |
| 19 | **Manchester United** | 1 | 3 | +4.0 | 10.1 pts | 7.8% | 58.3% | 33.9% | Play-offs |
| 20 | **RB Leipzig** | 1 | 0 | -3.0 | 10.2 pts | 8.3% | 54.8% | 36.9% | Play-offs |
| 21 | **AEK Athens** | 1 | 3 | +1.0 | 10.1 pts | 7.5% | 53.4% | 39.1% | Play-offs |
| 22 | **Sporting** | 1 | 3 | +2.0 | 9.7 pts | 6.1% | 52.8% | 41.0% | Play-offs |
| 23 | **Club Brugge** | 1 | 0 | -1.0 | 9.6 pts | 5.4% | 54.4% | 40.2% | Play-offs |
| 24 | **Napoli** | 1 | 0 | -1.0 | 9.6 pts | 6.2% | 50.9% | 42.9% | Play-offs |
| 25 | **PSV Eindhoven** | 1 | 1 | 0.0 | 9.2 pts | 5.3% | 45.9% | 48.9% | Eliminado |
| 26 | **Lille** | 1 | 0 | -1.0 | 9.1 pts | 4.8% | 46.7% | 48.5% | Eliminado |
| 27 | **Slovan Bratislava** | 1 | 0 | -5.0 | 9.5 pts | 4.8% | 47.4% | 47.9% | Eliminado |
| 28 | **Bodo/Glimt** | 1 | 0 | -5.0 | 8.9 pts | 3.4% | 41.3% | 55.3% | Eliminado |
| 29 | **Atletico** | 1 | 0 | -1.0 | 8.5 pts | 3.1% | 39.6% | 57.3% | Eliminado |
| 30 | **Fenerbahce** | 1 | 1 | 0.0 | 7.7 pts | 1.6% | 32.2% | 66.1% | Eliminado |
| 31 | **Slavia Praha** | 1 | 0 | -1.0 | 7.7 pts | 2.0% | 32.1% | 65.8% | Eliminado |
| 32 | **Feyenoord** | 1 | 0 | -4.0 | 7.8 pts | 1.9% | 30.8% | 67.3% | Eliminado |
| 33 | **Galatasaray SK** | 1 | 0 | -2.0 | 7.6 pts | 2.1% | 30.7% | 67.2% | Eliminado |
| 34 | **Sabah FC** | 1 | 0 | -4.0 | 7.8 pts | 1.6% | 31.0% | 67.4% | Eliminado |
| 35 | **Viking** | 1 | 0 | -2.0 | 7.2 pts | 0.7% | 27.4% | 72.0% | Eliminado |
| 36 | **LASK** | 1 | 0 | -1.0 | 6.5 pts | 0.5% | 20.2% | 79.2% | Eliminado |

---

## 3. Proyeccion del Cuadro Eliminatorio

### Cruces Proyectados de Play-offs (Dieciseisavos)
- **Serie 1**: Paris SG vs Napoli — *Pase proyectado: **Paris SG** (62.5%)*
- **Serie 2**: Lens vs Club Brugge — *Pase proyectado: **Lens** (53.5%)*
- **Serie 3**: Como vs Sporting — *Pase proyectado: **Como** (79.0%)*
- **Serie 4**: Inter vs AEK Athens — *Pase proyectado: **Inter** (88.4%)*
- **Serie 5**: Porto vs RB Leipzig — *Pase proyectado: **Porto** (50.5%)*
- **Serie 6**: Roma vs Manchester United — *Pase proyectado: **Roma** (83.7%)*
- **Serie 7**: Stuttgart vs Shakhtar Donetsk — *Pase proyectado: **Stuttgart** (76.8%)*
- **Serie 8**: Real Betis vs Villarreal — *Pase proyectado: **Villarreal** (55.1%)*

### Cabezas de Serie Proyectados (Octavos de Final)
Clubs clasificados directamente entre los 8 primeros: **Man City, Liverpool, Barcelona, Bayern Munich, Aston Villa, Arsenal, Dortmund, Real Madrid**.

---

## 4. Pronosticos de la Proxima Jornada (Jornada 2)

Pronósticos probabilísticos detallados de los 18 encuentros programados:

| Partido | Probabilidades 1X2 | Pronostico | Marcador Probable |
| :--- | :---: | :---: | :---: |
| **Lens** vs **Sporting** | `L 62% / E 20% / V 18%` | **Local** | `2-1` |
| **Sabah FC** vs **Slavia Praha** | `L 48% / E 24% / V 28%` | **Local** | `2-1` |
| **Arsenal** vs **Lille** | `L 73% / E 16% / V 11%` | **Local** | `2-1` |
| **Atletico** vs **Manchester United** | `L 55% / E 22% / V 23%` | **Local** | `2-1` |
| **Inter** vs **Club Brugge** | `L 71% / E 17% / V 12%` | **Local** | `2-1` |
| **Galatasaray SK** vs **Barcelona** | `L 26% / E 23% / V 51%` | **Visitante** | `1-2` |
| **RB Leipzig** vs **PSV Eindhoven** | `L 56% / E 22% / V 22%` | **Local** | `2-1` |
| **Viking** vs **Bayern Munich** | `L 18% / E 23% / V 59%` | **Visitante** | `1-2` |
| **Villarreal** vs **Napoli** | `L 46% / E 23% / V 31%` | **Local** | `2-1` |
| **Feyenoord** vs **Como** | `L 43% / E 23% / V 33%` | **Local** | `2-1` |
| **LASK** vs **Liverpool** | `L 22% / E 22% / V 56%` | **Visitante** | `1-2` |
| **Roma** vs **Real Madrid** | `L 32% / E 25% / V 43%` | **Visitante** | `1-2` |
| **Aston Villa** vs **Fenerbahce** | `L 66% / E 19% / V 15%` | **Local** | `2-1` |
| **Shakhtar Donetsk** vs **AEK Athens** | `L 54% / E 22% / V 24%` | **Local** | `2-1` |
| **Bodo/Glimt** vs **Dortmund** | `L 30% / E 24% / V 47%` | **Visitante** | `1-2` |
| **Man City** vs **Paris SG** | `L 61% / E 20% / V 19%` | **Local** | `2-1` |
| **Real Betis** vs **Porto** | `L 30% / E 24% / V 46%` | **Visitante** | `1-2` |
| **Slovan Bratislava** vs **Stuttgart** | `L 37% / E 24% / V 38%` | **Visitante** | `1-2` |

---

## 5. Actualizacion del Sistema

Este repositorio actualiza todas sus proyecciones de manera continua. Cada vez que concluye una jornada y se registran los marcadores oficiales, el motor recalcula las probabilidades de victoria de cada partido restante, actualiza la tabla de posiciones simulada y proyecta de nuevo los favoritos al titulo.

