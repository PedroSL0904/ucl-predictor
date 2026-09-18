# AGENTS.md - Guía de Operación y Arquitectura Técnica: `ucl-predictor`

## Contexto Técnico
* **Nombre del Repositorio**: `ucl-predictor`
* **Ruta Local**: `C:\Users\Boutros\ucl-predictor`
* **Entorno Python**: `C:\Users\Boutros\liga-mx-predictor\.venv\Scripts\python.exe`
* **Framework de Testing**: `pytest` (`& "C:\Users\Boutros\liga-mx-predictor\.venv\Scripts\pytest.exe" tests\test_ucl.py -q`)
* **Propósito**: Predicción probabilística calibrada de partidos de UEFA Champions League, simulación Monte Carlo de la fase de liga suiza (36 equipos) y bracket de eliminatorias, y optimización de portafolios de quiniela y apuestas (sencillas y dobles 1X/X2).

---

## Archivos Críticos
* `src/predictor.py`: Orquestador principal de inferencia (`UCLPredictor`). Carga los 4 modelos y el TemperatureScaler.
* `src/models/statistical.py`: Dixon-Coles Poisson bivariado con Bayesian shrinkage, corrección $\tau(x,y;\rho=-0.10)$, inflación por gap de Elo y draw boost.
* `src/models/ml.py`: Entrenadores de XGBoost, LightGBM y CatBoost con class_weight balanceado.
* `src/models/calibration.py`: `TemperatureScaler` que optimiza $T$ sobre validación ($T=0.653$).
* `src/data/clubelo.py`: Resolutor canónico de clubes europeos y lookup causal de Elo por fecha.
* `src/data/openfootball.py`: Parser de fixtures y resultados de UCL de openfootball.
* `src/simulation/swiss_stage.py`: Simulador Monte Carlo de la tabla única de 36 equipos.
* `src/simulation/bracket.py`: Simulador de eliminatorias ida y vuelta y final única.
* `src/strategy/safety.py`: Clasificador de Safety Tiers (Banquero Seguro, Favorito con Riesgo de Empate, Paridad).
* `src/strategy/double_chance.py`: Cálculo de Doble Oportunidad (`1X`, `X2`, `12`).
* `src/strategy/portfolio.py`: Generador de portafolio de 3 boletos complementarios (Base, Empates, Sorpresas).
* `config/settings.py`: Parámetros globales y rutas del proyecto.
* `config/uefa_coefficients.json`: Factores de fuerza y calidad por liga doméstica.

---

## Convenciones
* **Ejecución**: Ejecutar scripts siempre como `python -m scripts.NN_script` desde `C:\Users\Boutros\ucl-predictor`.
* **Causalidad**: NUNCA usar datos de partidos futuros para calcular features o ratings de partidos pasados.
* **Codificación**: UTF-8 explícito en lecturas y escrituras de archivos.
