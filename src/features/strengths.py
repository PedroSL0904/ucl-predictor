"""Bayesian weighted attack/defense strengths for UEFA Champions League."""
from __future__ import annotations
import numpy as np
import pandas as pd

def approx_xg_from_elo(elo_attacker: float | np.ndarray, elo_defender: float | np.ndarray,
                       base_goals: float = 1.45, elo_div: float = 400.0) -> float | np.ndarray:
    """Approximates expected goals from Elo differential."""
    return base_goals * (1.0 + 0.35 * np.tanh((elo_attacker - elo_defender) / elo_div))


def compute_weighted_strengths(
    df: pd.DataFrame,
    as_of: str | None = None,
    elo_sigma: float = 240.0,
    recency_half_life_days: float = 500.0,
    shrinkage_matches: int = 6,
    league_mean_attack: float = 1.0,
    league_mean_defense: float = 1.0,
    home_team_col: str = "home_team_name",
    away_team_col: str = "away_team_name",
    home_goals_col: str = "home_goals",
    away_goals_col: str = "away_goals",
    home_elo_col: str = "home_elo",
    away_elo_col: str = "away_elo",
    date_col: str = "date",
) -> dict[str, dict[str, float]]:
    """Calculates attack and defensive vulnerability weighting by opponent Elo and time decay."""
    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col])
    if as_of is not None:
        data = data[data[date_col] < pd.Timestamp(as_of)]
    if data.empty:
        return {}

    ref_date = data[date_col].max()
    days_ago = (ref_date - data[date_col]).dt.days.values
    w_recency = 0.5 ** (np.maximum(0, days_ago) / recency_half_life_days)

    home_elo = data[home_elo_col].values if home_elo_col in data.columns else np.full(len(data), 1600.0)
    away_elo = data[away_elo_col].values if away_elo_col in data.columns else np.full(len(data), 1600.0)

    w_h = np.exp((away_elo - home_elo) / elo_sigma) * w_recency
    w_a = np.exp((home_elo - away_elo) / elo_sigma) * w_recency

    xg_h = approx_xg_from_elo(home_elo, away_elo)
    xg_a = approx_xg_from_elo(away_elo, home_elo)

    gf_h = data[home_goals_col].values
    ga_h = data[away_goals_col].values

    home_teams = data[home_team_col].values
    away_teams = data[away_team_col].values

    team_data = {}
    for tid in set(np.concatenate([home_teams, away_teams])):
        team_data[tid] = {
            "gf_w": 0.0, "xg_f_w": 0.0,
            "ga_w": 0.0, "xg_a_w": 0.0,
            "w_sum": 0.0, "matches": 0,
        }

    for i in range(len(data)):
        ht, at = home_teams[i], away_teams[i]
        wh, wa = w_h[i], w_a[i]

        team_data[ht]["gf_w"] += gf_h[i] * wh
        team_data[ht]["xg_f_w"] += xg_h[i] * wh
        team_data[ht]["ga_w"] += ga_h[i] * wh
        team_data[ht]["xg_a_w"] += xg_a[i] * wh
        team_data[ht]["w_sum"] += wh
        team_data[ht]["matches"] += 1

        team_data[at]["gf_w"] += ga_h[i] * wa
        team_data[at]["xg_f_w"] += xg_a[i] * wa
        team_data[at]["ga_w"] += gf_h[i] * wa
        team_data[at]["xg_a_w"] += xg_h[i] * wa
        team_data[at]["w_sum"] += wa
        team_data[at]["matches"] += 1

    strengths = {}
    for tid, d in team_data.items():
        w_n = d["w_sum"]
        raw_att = d["gf_w"] / max(d["xg_f_w"], 1e-6)
        raw_def = d["ga_w"] / max(d["xg_a_w"], 1e-6)
        shrink = w_n / (w_n + shrinkage_matches) if w_n > 0 else 0.0
        att = shrink * raw_att + (1.0 - shrink) * league_mean_attack
        def_vuln = shrink * raw_def + (1.0 - shrink) * league_mean_defense
        strengths[str(tid)] = {
            "attack": float(att),
            "defense": float(def_vuln),
            "matches": int(d["matches"]),
            "weighted_matches": float(w_n),
        }

    return strengths
