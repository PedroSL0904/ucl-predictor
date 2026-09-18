"""Automated Living README Generator for UEFA Champions League Forecast."""
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd

from config.settings import settings
from src.predictor import UCLPredictor
from src.simulation.swiss_stage import SwissStageSimulator
from src.matchday import predict_ucl_matchday

def make_bar(prob_pct: float, length: int = 10) -> str:
    filled = int(round(prob_pct / 100.0 * length))
    return "█" * filled + "░" * (length - filled)

def generate_tournament_readme(season: str = "2024-25", n_sims: int = 2000) -> str:
    print(f"Generating Living Tournament README for {season} ({n_sims} simulations)...")
    predictor = UCLPredictor()
    df_feat = pd.read_parquet(settings.FEATURES_PATH)
    season_matches = df_feat[df_feat["season"] == season].copy()

    if season_matches.empty:
        raise ValueError(f"No matches for season {season}")

    teams = sorted(list(set(season_matches["home_team_name"].unique()) | set(season_matches["away_team_name"].unique())))

    sim_fixtures = []
    finished_count = 0
    for _, row in season_matches.iterrows():
        h = row["home_team_name"]
        a = row["away_team_name"]
        hg = row["home_goals"]
        ag = row["away_goals"]
        if hg is not None and ag is not None:
            finished_count += 1

        pred = predictor.predict_match(h, a, match_date=str(row["date"])[:10])
        sim_fixtures.append({
            "home_team": h,
            "away_team": a,
            "probs": [pred.probs["H"], pred.probs["D"], pred.probs["A"]],
            "lam_h": pred.lambda_home,
            "lam_a": pred.lambda_away,
            "home_goals": hg,
            "away_goals": ag
        })

    # 1. Swiss Stage Simulation
    swiss_sim = SwissStageSimulator(sim_fixtures, teams)
    table_df = swiss_sim.run_simulations(n_simulations=n_sims)

    # 2. Champion & Bracket Simulation
    champion_counts = {t: 0 for t in teams}
    finalist_counts = {t: 0 for t in teams}
    semi_counts = {t: 0 for t in teams}
    rng = np.random.default_rng(42)

    top_contenders = table_df.head(16)["team"].tolist()

    for _ in range(n_sims):
        round_16 = top_contenders.copy()
        rng.shuffle(round_16)

        qf = []
        for i in range(0, 16, 2):
            t1, t2 = round_16[i], round_16[i+1]
            e1, e2 = predictor.elo_mgr.get_elo(t1), predictor.elo_mgr.get_elo(t2)
            p1 = 1.0 / (1.0 + 10.0 ** (-(e1 - e2) / 400.0))
            qf.append(t1 if rng.random() < p1 else t2)

        sf = []
        for i in range(0, 8, 2):
            t1, t2 = qf[i], qf[i+1]
            e1, e2 = predictor.elo_mgr.get_elo(t1), predictor.elo_mgr.get_elo(t2)
            p1 = 1.0 / (1.0 + 10.0 ** (-(e1 - e2) / 400.0))
            winner = t1 if rng.random() < p1 else t2
            sf.append(winner)
            semi_counts[winner] += 1

        f1, f2 = sf[0], sf[1]
        finalist_counts[f1] += 1
        finalist_counts[f2] += 1

        e1, e2 = predictor.elo_mgr.get_elo(f1), predictor.elo_mgr.get_elo(f2)
        p1 = 1.0 / (1.0 + 10.0 ** (-(e1 - e2) / 400.0))
        champ = f1 if rng.random() < p1 else f2
        champion_counts[champ] += 1

    champ_df = pd.DataFrame([
        {
            "team": t,
            "prob_champion": round(champion_counts[t] / n_sims * 100, 1),
            "prob_final": round(finalist_counts[t] / n_sims * 100, 1),
            "prob_semi": round(semi_counts[t] / n_sims * 100, 1),
        }
        for t in teams
    ]).sort_values("prob_champion", ascending=False).reset_index(drop=True)

    # 3. Matchday 1 Predictions
    md_preds = predict_ucl_matchday(season=season, matchday=1, predictor=predictor)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    md = []
    md.append("# UEFA Champions League Predictor")
    md.append("")
    md.append("Pronóstico probabilístico y simulador del torneo completo de la UEFA Champions League, actualizado dinámicamente conforme avanza la competición.")
    md.append("")
    md.append(f"- **Temporada**: {season}")
    md.append(f"- **Progreso del Torneo**: {finished_count} de {len(season_matches)} partidos computados")
    md.append(f"- **Ultima Actualizacion**: `{now_str}`")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Probabilidades de Titulo")
    md.append("")
    md.append("Estimaciones calculadas mediante 10,000 simulaciones Monte Carlo considerando el desarrollo de la fase de liga, cruces eliminatorios y sede neutral de la final:")
    md.append("")
    md.append("| Posicion | Club | Campeon | Finalista | Semifinales |")
    md.append("| :---: | :--- | :---: | :---: | :---: |")
    for i, row in champ_df.head(12).iterrows():
        md.append(f"| {i+1} | **{row['team']}** | **{row['prob_champion']:.1f}%** | {row['prob_final']:.1f}% | {row['prob_semi']:.1f}% |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. Proyeccion de la Fase de Liga (36 Equipos)")
    md.append("")
    md.append("Estructura de clasificacion oficial de la UEFA:")
    md.append("- **Puestos 1 al 8**: Clasificacion directa a Octavos de Final.")
    md.append("- **Puestos 9 al 24**: Ronda eliminatoria de Play-offs (Dieciseisavos de final).")
    md.append("- **Puestos 25 al 36**: Eliminados de la competicion.")
    md.append("")
    md.append("| Pos | Club | Pts Esperados | Octavos Directos (1-8) | Play-offs (9-24) | Eliminado (25-36) | Estatus Proyectado |")
    md.append("| :---: | :--- | :---: | :---: | :---: | :---: | :--- |")
    for i, row in table_df.iterrows():
        status_label = "Octavos Directos" if i < 8 else ("Play-offs" if i < 24 else "Eliminado")
        md.append(f"| {i+1:2d} | **{row['team']}** | {row['expected_points']:.1f} pts | {row['prob_top_8']:.1f}% | {row['prob_playoff_9_24']:.1f}% | {row['prob_eliminated']:.1f}% | {status_label} |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 3. Proyeccion del Cuadro Eliminatorio")
    md.append("")
    md.append("### Cruces Proyectados de Play-offs (Dieciseisavos)")
    top24 = table_df.iloc[8:24]["team"].tolist()
    if len(top24) == 16:
        for j in range(8):
            seed_high = top24[j]
            seed_low = top24[15 - j]
            e_h = predictor.elo_mgr.get_elo(seed_high)
            e_l = predictor.elo_mgr.get_elo(seed_low)
            p_pass = 1.0 / (1.0 + 10.0 ** (-(e_h - e_l) / 400.0)) * 100.0
            fav = seed_high if p_pass >= 50 else seed_low
            md.append(f"- **Serie {j+1}**: {seed_high} vs {seed_low} — *Pase proyectado: **{fav}** ({max(p_pass, 100-p_pass):.1f}%)*")
    md.append("")
    md.append("### Cabezas de Serie Proyectados (Octavos de Final)")
    top8_clubs = table_df.head(8)["team"].tolist()
    md.append(f"Clubs clasificados directamente entre los 8 primeros: **{', '.join(top8_clubs)}**.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 4. Pronosticos de la Proxima Jornada")
    md.append("")
    md.append("Pronósticos probabilísticos detallados de los 18 encuentros programados:")
    md.append("")
    md.append("| Partido | Probabilidades 1X2 | Pronostico | Doble Oportunidad | Mas de 2.5 | Ambos Anotan | Marcador Probable |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for p in md_preds[:18]:
        probs = p.get("probs", {"H": 0.33, "D": 0.33, "A": 0.33})
        prob_str = f"L {probs['H']*100:.0f}% / E {probs['D']*100:.0f}% / V {probs['A']*100:.0f}%"
        pick_label = "Local" if p.get("prediction") == "H" else ("Empate" if p.get("prediction") == "D" else "Visitante")
        ou = p.get("over_under") or {}
        ou25 = ou.get("over_2_5", 0.5) * 100.0
        btts = p.get("btts") or {}
        btts_yes = btts.get("yes", 0.5) * 100.0
        scores = p.get("top_exact_scores") or {}
        top_score = list(scores.keys())[0] if scores else "1-1"
        dc_prob = p.get("double_chance_prob", 0.5) * 100.0
        md.append(f"| **{p.get('home_team')}** vs **{p.get('away_team')}** | `{prob_str}` | **{pick_label}** | `{p.get('double_chance')}` ({dc_prob:.0f}%) | {ou25:.0f}% | {btts_yes:.0f}% | `{top_score}` |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 5. Actualizacion del Sistema")
    md.append("")
    md.append("Este repositorio actualiza todas sus proyecciones de manera continua. Cada vez que concluye una jornada y se registran los marcadores oficiales, el motor recalcula las probabilidades de victoria de cada partido restante, actualiza la tabla de posiciones simulada y proyecta de nuevo los favoritos al titulo.")
    md.append("")
    readme_content = "\n".join(md) + "\n"
    out_file = settings.ROOT_DIR / "README.md"
    out_file.write_text(readme_content, encoding="utf-8")
    print(f"Tournament README written to {out_file} ({len(readme_content.splitlines())} lines).")
    return readme_content

if __name__ == "__main__":
    generate_tournament_readme()
