# UEFA Champions League Predictor

Pronóstico probabilístico y simulador del torneo completo de la UEFA Champions League, actualizado dinámicamente conforme avanza la competición.

- **Temporada**: 2026-27
- **Progreso del Torneo**: 54 de 144 partidos computados (Jornada 3 concluida)
- **Ultima Actualizacion**: `2026-10-29 18:28 UTC`

---

## 1. Probabilidades de Titulo

Estimaciones calculadas mediante 10,000 simulaciones Monte Carlo considerando el desarrollo de la fase de liga, cruces eliminatorios y sede neutral de la final:

| Posicion | Club | Campeon | Finalista | Semifinales |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Arsenal** | **21.6%** | 34.1% | 48.2% |
| 2 | **Man City** | **16.2%** | 30.1% | 49.1% |
| 3 | **Barcelona** | **13.4%** | 23.6% | 41.2% |
| 4 | **Bayern Munich** | **13.4%** | 25.9% | 44.2% |
| 5 | **Paris SG** | **7.6%** | 16.4% | 34.4% |
| 6 | **Real Madrid** | **7.2%** | 16.9% | 34.5% |
| 7 | **Inter** | **6.5%** | 12.7% | 24.9% |
| 8 | **Liverpool** | **4.8%** | 12.6% | 28.4% |
| 9 | **Aston Villa** | **2.6%** | 6.9% | 19.9% |
| 10 | **Manchester United** | **2.1%** | 5.3% | 11.8% |
| 11 | **Dortmund** | **1.8%** | 4.5% | 12.8% |
| 12 | **Roma** | **0.7%** | 2.2% | 7.0% |

---

## 2. Proyeccion de la Fase de Liga (36 Equipos)

Estructura de clasificacion oficial de la UEFA:
- **Puestos 1 al 8**: Clasificacion directa a Octavos de Final.
- **Puestos 9 al 24**: Ronda eliminatoria de Play-offs (Dieciseisavos de final).
- **Puestos 25 al 36**: Eliminados de la competicion.

| Pos | Club | PJ | Pts Actuales | Dif Gol | Pts Proyectados | Octavos Directos (1-8) | Play-offs (9-24) | Eliminado (25-36) | Estatus Proyectado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
|  1 | **Paris SG** | 3 | 9 | +9.0 | 19.2 pts | 93.2% | 6.8% | 0.0% | Octavos Directos |
|  2 | **Liverpool** | 3 | 9 | +5.0 | 18.5 pts | 87.2% | 12.7% | 0.1% | Octavos Directos |
|  3 | **Real Madrid** | 3 | 9 | +5.0 | 18.5 pts | 83.8% | 16.2% | 0.0% | Octavos Directos |
|  4 | **Bayern Munich** | 3 | 5 | +5.0 | 17.0 pts | 77.8% | 22.1% | 0.1% | Octavos Directos |
|  5 | **Man City** | 3 | 6 | +4.0 | 17.1 pts | 75.4% | 24.6% | 0.1% | Octavos Directos |
|  6 | **Barcelona** | 3 | 6 | +5.0 | 16.0 pts | 62.7% | 36.8% | 0.5% | Octavos Directos |
|  7 | **Aston Villa** | 3 | 9 | +9.0 | 16.0 pts | 61.8% | 38.1% | 0.1% | Octavos Directos |
|  8 | **Arsenal** | 3 | 7 | +4.0 | 14.5 pts | 36.4% | 62.1% | 1.6% | Octavos Directos |
|  9 | **Dortmund** | 3 | 6 | +1.0 | 14.5 pts | 32.9% | 65.8% | 1.2% | Play-offs |
| 10 | **Atletico** | 3 | 4 | +1.0 | 14.2 pts | 32.8% | 64.9% | 2.4% | Play-offs |
| 11 | **Sporting** | 3 | 6 | +3.0 | 13.9 pts | 27.4% | 70.7% | 1.9% | Play-offs |
| 12 | **Stuttgart** | 3 | 7 | +5.0 | 13.6 pts | 26.0% | 69.9% | 4.1% | Play-offs |
| 13 | **Real Betis** | 3 | 9 | +3.0 | 13.8 pts | 22.4% | 76.4% | 1.2% | Play-offs |
| 14 | **Club Brugge** | 3 | 6 | +3.0 | 13.5 pts | 19.7% | 77.0% | 3.2% | Play-offs |
| 15 | **Inter** | 3 | 3 | -1.0 | 12.4 pts | 9.7% | 81.8% | 8.5% | Play-offs |
| 16 | **Roma** | 3 | 4 | +3.0 | 11.6 pts | 8.5% | 79.2% | 12.2% | Play-offs |
| 17 | **Shakhtar Donetsk** | 3 | 4 | +1.0 | 11.8 pts | 10.1% | 76.6% | 13.3% | Play-offs |
| 18 | **RB Leipzig** | 3 | 3 | -5.0 | 12.3 pts | 9.8% | 75.4% | 14.7% | Play-offs |
| 19 | **Como** | 3 | 6 | +5.0 | 11.2 pts | 7.2% | 80.0% | 12.8% | Play-offs |
| 20 | **Manchester United** | 3 | 3 | -1.0 | 11.3 pts | 6.4% | 76.0% | 17.6% | Play-offs |
| 21 | **Villarreal** | 3 | 3 | 0.0 | 11.1 pts | 5.7% | 76.4% | 17.8% | Play-offs |
| 22 | **Galatasaray SK** | 3 | 3 | -3.0 | 8.8 pts | 0.7% | 48.5% | 50.8% | Play-offs |
| 23 | **Lens** | 3 | 3 | -4.0 | 8.6 pts | 1.1% | 44.0% | 54.9% | Play-offs |
| 24 | **Napoli** | 3 | 3 | -2.0 | 8.2 pts | 0.2% | 42.0% | 57.8% | Play-offs |
| 25 | **Lille** | 3 | 0 | -6.0 | 8.0 pts | 0.1% | 43.5% | 56.5% | Eliminado |
| 26 | **Porto** | 3 | 0 | -4.0 | 7.6 pts | 0.1% | 37.3% | 62.5% | Eliminado |
| 27 | **Feyenoord** | 3 | 3 | -4.0 | 7.9 pts | 0.4% | 32.6% | 67.0% | Eliminado |
| 28 | **PSV Eindhoven** | 3 | 4 | 0.0 | 7.3 pts | 0.2% | 26.1% | 73.7% | Eliminado |
| 29 | **Slavia Praha** | 3 | 1 | -3.0 | 7.0 pts | 0.1% | 27.9% | 72.0% | Eliminado |
| 30 | **Bodo/Glimt** | 3 | 3 | -5.0 | 7.5 pts | 0.1% | 25.4% | 74.4% | Eliminado |
| 31 | **Fenerbahce** | 3 | 2 | -6.0 | 7.1 pts | 0.1% | 23.2% | 76.8% | Eliminado |
| 32 | **AEK Athens** | 3 | 3 | -5.0 | 7.0 pts | 0.0% | 22.1% | 77.8% | Eliminado |
| 33 | **LASK** | 3 | 3 | -3.0 | 6.4 pts | 0.1% | 15.8% | 84.2% | Eliminado |
| 34 | **Sabah FC** | 3 | 3 | -3.0 | 6.3 pts | 0.1% | 14.3% | 85.7% | Eliminado |
| 35 | **Viking** | 3 | 1 | -4.0 | 4.9 pts | 0.0% | 6.0% | 94.0% | Eliminado |
| 36 | **Slovan Bratislava** | 3 | 0 | -12.0 | 3.3 pts | 0.0% | 1.5% | 98.5% | Eliminado |

---

## 3. Proyeccion del Cuadro Eliminatorio

### Cruces Proyectados de Play-offs (Dieciseisavos)
- **Serie 1**: Dortmund vs Napoli — *Pase proyectado: **Dortmund** (52.2%)*
- **Serie 2**: Atletico vs Lens — *Pase proyectado: **Atletico** (57.7%)*
- **Serie 3**: Sporting vs Galatasaray SK — *Pase proyectado: **Sporting** (80.5%)*
- **Serie 4**: Stuttgart vs Villarreal — *Pase proyectado: **Villarreal** (53.3%)*
- **Serie 5**: Real Betis vs Manchester United — *Pase proyectado: **Manchester United** (67.3%)*
- **Serie 6**: Club Brugge vs Como — *Pase proyectado: **Como** (56.1%)*
- **Serie 7**: Inter vs RB Leipzig — *Pase proyectado: **Inter** (73.5%)*
- **Serie 8**: Roma vs Shakhtar Donetsk — *Pase proyectado: **Roma** (69.6%)*

### Cabezas de Serie Proyectados (Octavos de Final)
Clubs clasificados directamente entre los 8 primeros: **Paris SG, Liverpool, Real Madrid, Bayern Munich, Man City, Barcelona, Aston Villa, Arsenal**.

---

## 4. Pronosticos de la Proxima Jornada (Jornada 4)

Pronósticos probabilísticos detallados de los 18 encuentros programados:

| Partido | Probabilidades 1X2 | Pronostico | Marcador Probable |
| :--- | :---: | :---: | :---: |
| **Galatasaray SK** vs **Viking** | `L 61% / E 22% / V 17%` | **Local** | `2-1` |
| **Paris SG** vs **AEK Athens** | `L 78% / E 14% / V 8%` | **Local** | `2-0` |
| **Man City** vs **Como** | `L 69% / E 19% / V 13%` | **Local** | `2-1` |
| **Bayern Munich** vs **Roma** | `L 69% / E 18% / V 13%` | **Local** | `2-1` |
| **Dortmund** vs **Club Brugge** | `L 66% / E 20% / V 15%` | **Local** | `2-1` |
| **Napoli** vs **Manchester United** | `L 41% / E 23% / V 36%` | **Local** | `2-1` |
| **Liverpool** vs **Real Betis** | `L 69% / E 19% / V 12%` | **Local** | `2-1` |
| **Barcelona** vs **Real Madrid** | `L 41% / E 23% / V 36%` | **Local** | `2-1` |
| **Sporting** vs **Sabah FC** | `L 74% / E 14% / V 12%` | **Local** | `3-0` |
| **PSV Eindhoven** vs **Arsenal** | `L 18% / E 21% / V 61%` | **Visitante** | `1-2` |
| **Porto** vs **Slovan Bratislava** | `L 77% / E 13% / V 10%` | **Local** | `3-1` |
| **Slavia Praha** vs **Feyenoord** | `L 43% / E 21% / V 36%` | **Local** | `3-1` |
| **Inter** vs **Fenerbahce** | `L 75% / E 16% / V 9%` | **Local** | `1-0` |
| **LASK** vs **Aston Villa** | `L 27% / E 24% / V 48%` | **Visitante** | `1-2` |
| **Shakhtar Donetsk** vs **Atletico** | `L 33% / E 25% / V 41%` | **Visitante** | `1-2` |
| **RB Leipzig** vs **Lens** | `L 61% / E 23% / V 16%` | **Local** | `2-1` |
| **Lille** vs **Bodo/Glimt** | `L 64% / E 17% / V 19%` | **Local** | `3-0` |
| **Stuttgart** vs **Villarreal** | `L 35% / E 23% / V 42%` | **Visitante** | `1-2` |

---

## 5. Actualizacion del Sistema

Este repositorio actualiza todas sus proyecciones de manera continua. Cada vez que concluye una jornada y se registran los marcadores oficiales, el motor recalcula las probabilidades de victoria de cada partido restante, actualiza la tabla de posiciones simulada y proyecta de nuevo los favoritos al titulo.

