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

def generate_tournament_readme(season: str = "2026-27", n_sims: int = 2000) -> str:
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
        if pd.notna(hg) and pd.notna(ag):
            finished_count += 1

        pred = predictor.predict_match(h, a, match_date=str(row["date"])[:10])
        sim_fixtures.append({
            "home_team": h,
            "away_team": a,
            "probs": [pred.probs["H"], pred.probs["D"], pred.probs["A"]],
            "lam_h": pred.lambda_home,
            "lam_a": pred.lambda_away,
            "home_goals": hg if pd.notna(hg) else None,
            "away_goals": ag if pd.notna(ag) else None
        })

    # 1 & 2. Full Tournament Simulation (Swiss Phase + Official UEFA Bracket)
    swiss_sim = SwissStageSimulator(sim_fixtures, teams)
    table_df, champ_df = swiss_sim.run_full_tournament_simulations(
        elo_lookup=lambda t: predictor.elo_mgr.get_elo(t),
        n_simulations=n_sims,
        seed=42
    )

    # 3. Next Matchday Predictions (Upcoming unplayed round)
    md_preds = predict_ucl_matchday(season=season, matchday=None, predictor=predictor)
    next_md = md_preds[0]["matchday"] if md_preds else 2

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    md = []
    md.append("# UEFA Champions League Predictor")
    md.append("")
    md.append("Pronóstico probabilístico y simulador del torneo completo de la UEFA Champions League, actualizado dinámicamente conforme avanza la competición.")
    md.append("")
    md.append(f"- **Temporada**: {season}")
    md.append(f"- **Progreso del Torneo**: {finished_count} de {len(season_matches)} partidos computados (Jornada 1 concluida)")
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
    md.append("| Pos | Club | PJ | Pts Actuales | Dif Gol | Pts Proyectados | Octavos Directos (1-8) | Play-offs (9-24) | Eliminado (25-36) | Estatus Proyectado |")
    md.append("| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")
    for i, row in table_df.iterrows():
        status_label = "Octavos Directos" if i < 8 else ("Play-offs" if i < 24 else "Eliminado")
        gd_str = f"+{row['current_gd']}" if row['current_gd'] > 0 else f"{row['current_gd']}"
        md.append(f"| {i+1:2d} | **{row['team']}** | {row['current_pj']} | {row['current_points']} | {gd_str} | {row['expected_points']:.1f} pts | {row['prob_top_8']:.1f}% | {row['prob_playoff_9_24']:.1f}% | {row['prob_eliminated']:.1f}% | {status_label} |")
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
    md.append(f"## 4. Pronosticos de la Proxima Jornada (Jornada {next_md})")
    md.append("")
    md.append("Pronósticos probabilísticos detallados de los 18 encuentros programados:")
    md.append("")
    md.append("| Partido | Probabilidades 1X2 | Pronostico | Marcador Probable |")
    md.append("| :--- | :---: | :---: | :---: |")
    for p in md_preds[:18]:
        probs = p.get("probs", {"H": 0.33, "D": 0.33, "A": 0.33})
        prob_str = f"L {probs['H']*100:.0f}% / E {probs['D']*100:.0f}% / V {probs['A']*100:.0f}%"
        pick_label = "Local" if p.get("prediction") == "H" else ("Empate" if p.get("prediction") == "D" else "Visitante")
        pred = p.get("prediction", "H")
        cond_scores = p.get("conditioned_top_scores") or {}
        top_score = cond_scores.get(pred)
        if not top_score:
            top_score = "2-1" if pred == "H" else ("1-2" if pred == "A" else "1-1")
        md.append(f"| **{p.get('home_team')}** vs **{p.get('away_team')}** | `{prob_str}` | **{pick_label}** | `{top_score}` |")
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
