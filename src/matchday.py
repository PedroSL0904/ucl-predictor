"""Matchday predictor and output formatter for UEFA Champions League."""
from typing import List, Dict, Any, Optional
import pandas as pd
from config.settings import settings
from src.predictor import UCLPredictor
from src.strategy.portfolio import generate_ucl_portfolio

def predict_ucl_matchday(
    season: str = "2026-27",
    matchday: Optional[int] = None,
    predictor: Optional[UCLPredictor] = None
) -> List[Dict[str, Any]]:
    pred_engine = predictor or UCLPredictor()
    df_feat = pd.read_parquet(settings.FEATURES_PATH)
    
    if matchday is None:
        unplayed = df_feat[(df_feat["season"] == season) & (df_feat["home_goals"].isna())]
        target_md = int(unplayed["matchday"].min()) if not unplayed.empty else 1
    else:
        target_md = matchday

    matches_df = df_feat[(df_feat["season"] == season) & (df_feat["matchday"] == target_md)].copy()
    if matches_df.empty:
        matches_df = df_feat[df_feat["season"] == season].head(18).copy()

    results = []
    for _, row in matches_df.iterrows():
        h = row["home_team_name"]
        a = row["away_team_name"]
        m_date = str(row["date"])[:10]
        p = pred_engine.predict_match(
            home_team=h,
            away_team=a,
            match_date=m_date,
            stage=row["stage"],
            matchday=row["matchday"]
        )
        results.append({
            "season": season,
            "matchday": row["matchday"],
            "stage": row["stage"],
            "date": m_date,
            "home_team": h,
            "away_team": a,
            "probs": p.probs,
            "prediction": p.prediction,
            "double_chance": p.double_chance,
            "double_chance_prob": p.double_chance_prob,
            "safety_tier": p.safety_tier.value,
            "confidence": p.confidence.value,
            "lambda_home": p.lambda_home,
            "lambda_away": p.lambda_away,
            "over_under": p.over_under,
            "btts": p.btts,
            "top_exact_scores": p.top_exact_scores,
            "travel_distance_km": p.travel_distance_km,
            "travel_fatigue": p.travel_fatigue,
            "actual_home_goals": row["home_goals"],
            "actual_away_goals": row["away_goals"],
            "actual_outcome": row["outcome"]
        })
    return results


def format_matchday_predictions(predictions: List[Dict[str, Any]], format_type: str = "detailed") -> str:
    if not predictions:
        return "No matches found."

    lines = []
    if format_type == "compact":
        lines.append("="*60)
        lines.append(f"🇪🇺 UCL QUINIELA - MATCHDAY {predictions[0]['matchday']} ({predictions[0]['season']})")
        lines.append("="*60)
        for i, p in enumerate(predictions, 1):
            tag_name = {"H": "Local (1)", "D": "Empate (X)", "A": "Visita (2)"}.get(p["prediction"], p["prediction"])
            lines.append(f"{i:2d}. {p['home_team']} vs {p['away_team']:<20} -> {p['prediction']} [{p['double_chance']}]")
        lines.append("="*60)

    elif format_type == "detailed":
        lines.append("="*95)
        lines.append(f"🏆 UEFA CHAMPIONS LEAGUE - PRONÓSTICOS DETALLADOS (Jornada {predictions[0]['matchday']})")
        lines.append("="*95)
        for i, p in enumerate(predictions, 1):
            probs = p["probs"]
            actual_str = ""
            if p.get("actual_home_goals") is not None and p.get("actual_away_goals") is not None:
                hit = "✅" if p["prediction"] == p["actual_outcome"] else ("🛡️" if (
                    (p["double_chance"] == "1X" and p["actual_outcome"] in ["H", "D"]) or
                    (p["double_chance"] == "X2" and p["actual_outcome"] in ["D", "A"]) or
                    (p["double_chance"] == "12" and p["actual_outcome"] in ["H", "A"])
                ) else "❌")
                actual_str = f" | Real: {int(p['actual_home_goals'])}-{int(p['actual_away_goals'])} ({p['actual_outcome']}) {hit}"

            lines.append(
                f"{i:2d}. {p['home_team']:<22} vs {p['away_team']:<22} "
                f"| 1X2: [{probs['H']*100:4.1f}% / {probs['D']*100:4.1f}% / {probs['A']*100:4.1f}%] "
                f"| Pick: {p['prediction']} | DC: {p['double_chance']:<2} ({p['double_chance_prob']*100:4.1f}%) "
                f"| [{p['safety_tier']}]"
                f"{actual_str}"
            )
        lines.append("="*95)

    elif format_type == "portfolio":
        lines.append("="*75)
        lines.append(f"💼 PORTAFOLIO DE APUESTAS & QUINIELA (3 BOLETOS COMPLEMENTARIOS)")
        lines.append("="*75)
        port = generate_ucl_portfolio(predictions)
        lines.append(f"{'#':<3} {'Partido':<40} {'Boleto Base':<12} {'Boleto Empates':<15} {'Boleto Sorpresa':<15}")
        lines.append("-" * 75)
        for i in range(len(predictions)):
            m = port["matches"][i]
            b = port["ticket_base"][i]
            d = port["ticket_draws"][i]
            s = port["ticket_surprises"][i]
            lines.append(f"{i+1:<3} {m:<40} {b:<12} {d:<15} {s:<15}")
        lines.append("="*75)
        lines.append("💡 Estrategia: Boleto Base para máxima probabilidad, Empates para absorber duelos tácticos, y Sorpresa para capturar momios altos.")

    return "\n".join(lines)
