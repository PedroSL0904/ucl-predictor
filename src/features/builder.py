"""Causal feature engineering pipeline for UEFA Champions League 2.0."""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from config.settings import settings
from src.features.strengths import compute_weighted_strengths
from src.features.geo import EuropeanGeoManager

HOSTILE_COUNTRIES = {"TUR", "SRB", "GRE", "CRO", "UKR", "ROU", "BUL", "POL"}

def elo_win_probability(elo_diff: float, home_advantage: float = 65.0) -> Tuple[float, float, float]:
    dr = elo_diff + home_advantage
    e_home = 1.0 / (1.0 + 10.0 ** (-dr / 400.0))
    p_draw = max(0.14, 0.26 * np.exp(- (dr / 350.0) ** 2))
    p_home = e_home * (1.0 - p_draw)
    p_away = (1.0 - e_home) * (1.0 - p_draw)
    total = p_home + p_draw + p_away
    return float(p_home / total), float(p_draw / total), float(p_away / total)


def build_features_matrix(db_path: Optional[Path] = None, save_path: Optional[Path] = None) -> pd.DataFrame:
    engine = create_engine(f"sqlite:///{db_path or settings.DB_PATH}")
    df_fix = pd.read_sql_query("SELECT * FROM fixtures ORDER BY date ASC, id ASC", engine)
    df_teams = pd.read_sql_query("SELECT * FROM teams", engine).set_index("id")

    df_fix["date"] = pd.to_datetime(df_fix["date"])
    
    geo_mgr = EuropeanGeoManager()
    team_history: Dict[int, List[Dict]] = {tid: [] for tid in df_teams.index}
    h2h_history: Dict[tuple, List[str]] = {}

    feature_rows = []

    for idx, row in df_fix.iterrows():
        mid = row["id"]
        m_date = row["date"]
        hid = row["home_team_id"]
        aid = row["away_team_id"]
        h_name = row["home_team_name"]
        a_name = row["away_team_name"]

        h_elo = row["home_elo"]
        a_elo = row["away_elo"]
        elo_diff = h_elo - a_elo

        h_coef = df_teams.loc[hid, "uefa_coef"] if hid in df_teams.index else 0.50
        a_coef = df_teams.loc[aid, "uefa_coef"] if aid in df_teams.index else 0.50
        coef_diff = h_coef - a_coef
        coef_ratio = h_coef / max(a_coef, 0.1)

        # Geo distance and travel fatigue
        dist_km = geo_mgr.calculate_distance_km(h_name, a_name)
        fatigue = geo_mgr.calculate_travel_fatigue(dist_km)

        # Club individual UEFA Pedigree
        h_pedigree = geo_mgr.get_club_pedigree(h_name)
        a_pedigree = geo_mgr.get_club_pedigree(a_name)
        pedigree_diff = h_pedigree - a_pedigree
        pedigree_ratio = h_pedigree / max(a_pedigree, 10.0)

        p_h_elo, p_d_elo, p_a_elo = elo_win_probability(elo_diff)

        # Rolling causal form for home team (last 3, 5 matches)
        h_past = team_history[hid]
        if h_past:
            h_last3 = h_past[-3:]
            h_last5 = h_past[-5:]
            form_3_h = sum(m["pts"] for m in h_last3) / len(h_last3)
            form_5_h = sum(m["pts"] for m in h_last5) / len(h_last5)
            gd_5_h = sum(m["gd"] for m in h_last5) / len(h_last5)
            gf_5_h = sum(m["gf"] for m in h_last5) / len(h_last5)
            ga_5_h = sum(m["ga"] for m in h_last5) / len(h_last5)
            rest_h = min(60, (m_date - h_past[-1]["date"]).days)
        else:
            form_3_h, form_5_h, gd_5_h, gf_5_h, ga_5_h = 1.35, 1.35, 0.0, 1.45, 1.45
            rest_h = 21

        # Rolling causal form for away team (last 3, 5 matches)
        a_past = team_history[aid]
        if a_past:
            a_last3 = a_past[-3:]
            a_last5 = a_past[-5:]
            form_3_a = sum(m["pts"] for m in a_last3) / len(a_last3)
            form_5_a = sum(m["pts"] for m in a_last5) / len(a_last5)
            gd_5_a = sum(m["gd"] for m in a_last5) / len(a_last5)
            gf_5_a = sum(m["gf"] for m in a_last5) / len(a_last5)
            ga_5_a = sum(m["ga"] for m in a_last5) / len(a_last5)
            rest_a = min(60, (m_date - a_past[-1]["date"]).days)
        else:
            form_3_a, form_5_a, gd_5_a, gf_5_a, ga_5_a = 1.35, 1.35, 0.0, 1.45, 1.45
            rest_a = 21

        # Head to Head causal
        pair_key = (min(hid, aid), max(hid, aid))
        h2h_list = h2h_history.get(pair_key, [])
        if h2h_list:
            h2h_total = len(h2h_list)
            if hid < aid:
                h2h_h_wins = sum(1 for res in h2h_list if res == "first_win")
                h2h_a_wins = sum(1 for res in h2h_list if res == "second_win")
            else:
                h2h_h_wins = sum(1 for res in h2h_list if res == "second_win")
                h2h_a_wins = sum(1 for res in h2h_list if res == "first_win")
            h2h_draws = sum(1 for res in h2h_list if res == "draw")
        else:
            h2h_total = 0
            h2h_h_wins = 0
            h2h_a_wins = 0
            h2h_draws = 0

        stage_str = str(row["stage"]).lower()
        is_knockout = 1 if any(k in stage_str for k in ["playoff", "round of 16", "quarter", "semi", "final"]) else 0
        h_country = row["home_country"]
        is_hostile = 1 if h_country in HOSTILE_COUNTRIES else 0

        hg = row["home_goals"]
        ag = row["away_goals"]
        if hg is not None and ag is not None:
            if hg > ag:
                outcome = "H"
                target_code = 0
            elif hg == ag:
                outcome = "D"
                target_code = 1
            else:
                outcome = "A"
                target_code = 2
        else:
            outcome = None
            target_code = None

        feature_rows.append({
            "fixture_id": mid,
            "season": row["season"],
            "stage": row["stage"],
            "matchday": row["matchday"],
            "date": m_date,
            "home_team_id": hid,
            "away_team_id": aid,
            "home_team_name": h_name,
            "away_team_name": a_name,
            "home_elo": h_elo,
            "away_elo": a_elo,
            "elo_diff": elo_diff,
            "home_uefa_coef": h_coef,
            "away_uefa_coef": a_coef,
            "coef_diff": coef_diff,
            "coef_ratio": coef_ratio,
            "travel_distance_km": dist_km,
            "travel_fatigue": fatigue,
            "home_club_pedigree": h_pedigree,
            "away_club_pedigree": a_pedigree,
            "pedigree_diff": pedigree_diff,
            "pedigree_ratio": pedigree_ratio,
            "elo_prob_h": p_h_elo,
            "elo_prob_d": p_d_elo,
            "elo_prob_a": p_a_elo,
            "form_3_h": form_3_h,
            "form_3_a": form_3_a,
            "form_5_h": form_5_h,
            "form_5_a": form_5_a,
            "gd_5_h": gd_5_h,
            "gd_5_a": gd_5_a,
            "gf_5_h": gf_5_h,
            "gf_5_a": gf_5_a,
            "ga_5_h": ga_5_h,
            "ga_5_a": ga_5_a,
            "rest_h": rest_h,
            "rest_a": rest_a,
            "rest_diff": rest_h - rest_a,
            "h2h_h_wins": h2h_h_wins,
            "h2h_a_wins": h2h_a_wins,
            "h2h_draws": h2h_draws,
            "h2h_total": h2h_total,
            "is_knockout": is_knockout,
            "is_hostile_venue": is_hostile,
            "home_goals": hg,
            "away_goals": ag,
            "outcome": outcome,
            "target": target_code
        })

        if hg is not None and ag is not None:
            if hg > ag:
                h_pts, a_pts = 3, 0
                res_key = "first_win" if hid < aid else "second_win"
            elif hg == ag:
                h_pts, a_pts = 1, 1
                res_key = "draw"
            else:
                h_pts, a_pts = 0, 3
                res_key = "second_win" if hid < aid else "first_win"

            team_history[hid].append({
                "date": m_date, "pts": h_pts, "gf": hg, "ga": ag, "gd": hg - ag
            })
            team_history[aid].append({
                "date": m_date, "pts": a_pts, "gf": ag, "ga": hg, "gd": ag - hg
            })
            if pair_key not in h2h_history:
                h2h_history[pair_key] = []
            h2h_history[pair_key].append(res_key)

    features_df = pd.DataFrame(feature_rows)
    out_path = save_path or settings.FEATURES_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    features_df.to_parquet(out_path, index=False)
    print(f"Features 2.0 matrix built: {features_df.shape[0]} rows, {features_df.shape[1]} columns.")
    return features_df
