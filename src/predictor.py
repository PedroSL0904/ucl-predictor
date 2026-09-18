"""Master inference engine for UCL Predictor 2.0 with Multi-Market & Stacking."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
import joblib

from config.settings import settings
from src.domain import MatchPrediction, SafetyTier, ConfidenceLevel
from src.data.clubelo import ClubEloManager
from src.features.geo import EuropeanGeoManager
from src.models.statistical import UCLDixonColes
from src.models.calibration import TemperatureScaler
from src.models.stacking import StackingMetaLearner
from src.models.ml import FEATURE_COLS
from src.strategy.safety import compute_safety_tier, compute_confidence
from src.strategy.double_chance import compute_double_chance
from src.market.edge import ValueBettingEngine

HOSTILE_COUNTRIES = {"TUR", "SRB", "GRE", "CRO", "UKR", "ROU", "BUL", "POL"}

class UCLPredictor:
    """Master predictor combining Dixon-Coles, XGBoost, LightGBM, CatBoost, Stacking and Multi-Market derivations."""

    def __init__(self, models_dir: Optional[Path] = None):
        self.models_dir = models_dir or settings.MODELS_DIR
        self.elo_mgr = ClubEloManager()
        self.geo_mgr = EuropeanGeoManager()
        self.dixon_coles: Optional[UCLDixonColes] = None
        self.xgb_model = None
        self.lgb_model = None
        self.cat_model = None
        self.stacking_meta: Optional[StackingMetaLearner] = None
        self.scaler: Optional[TemperatureScaler] = None
        self.history_df: pd.DataFrame = pd.DataFrame()
        self._load_models()
        self._load_history()

    def _load_history(self):
        if settings.FEATURES_PATH.exists():
            df = pd.read_parquet(settings.FEATURES_PATH)
            played = df[df["home_goals"].notna() & df["away_goals"].notna()].copy()
            played["date"] = pd.to_datetime(played["date"])
            self.history_df = played[["date", "home_team_name", "away_team_name", "home_goals", "away_goals"]].sort_values("date")
        else:
            self.history_df = pd.DataFrame(columns=["date", "home_team_name", "away_team_name", "home_goals", "away_goals"])

    def _compute_dynamic_features(
        self,
        home_team: str,
        away_team: str,
        match_date: Optional[str] = None
    ) -> Dict[str, float]:
        target_date = pd.to_datetime(match_date) if match_date else pd.Timestamp.now()

        def get_team_stats(team: str):
            if self.history_df.empty:
                return 1.35, 1.35, 0.0, 1.45, 1.45, 21.0

            mask = (self.history_df["date"] < target_date) & (
                (self.history_df["home_team_name"] == team) | (self.history_df["away_team_name"] == team)
            )
            t_df = self.history_df[mask]
            if t_df.empty:
                return 1.35, 1.35, 0.0, 1.45, 1.45, 21.0

            pts_list = []
            gd_list = []
            gf_list = []
            ga_list = []
            last_date = t_df["date"].iloc[-1]

            for _, r in t_df.iterrows():
                is_home = (r["home_team_name"] == team)
                gf = float(r["home_goals"]) if is_home else float(r["away_goals"])
                ga = float(r["away_goals"]) if is_home else float(r["home_goals"])
                gd = gf - ga
                pts = 3.0 if gf > ga else (1.0 if gf == ga else 0.0)
                pts_list.append(pts)
                gd_list.append(gd)
                gf_list.append(gf)
                ga_list.append(ga)

            last3_pts = pts_list[-3:]
            last5_pts = pts_list[-5:]
            last5_gd = gd_list[-5:]
            last5_gf = gf_list[-5:]
            last5_ga = ga_list[-5:]

            form_3 = float(np.mean(last3_pts))
            form_5 = float(np.mean(last5_pts))
            gd_5 = float(np.mean(last5_gd))
            gf_5 = float(np.mean(last5_gf))
            ga_5 = float(np.mean(last5_ga))
            rest = float(min(60.0, max(1.0, (target_date - last_date).days)))

            return form_3, form_5, gd_5, gf_5, ga_5, rest

        f3_h, f5_h, gd5_h, gf5_h, ga5_h, rest_h = get_team_stats(home_team)
        f3_a, f5_a, gd5_a, gf5_a, ga5_a, rest_a = get_team_stats(away_team)

        h2h_h_w, h2h_a_w, h2h_d, h2h_tot = 0, 0, 0, 0
        if not self.history_df.empty:
            h2h_mask = (self.history_df["date"] < target_date) & (
                ((self.history_df["home_team_name"] == home_team) & (self.history_df["away_team_name"] == away_team)) |
                ((self.history_df["home_team_name"] == away_team) & (self.history_df["away_team_name"] == home_team))
            )
            h2h_df = self.history_df[h2h_mask]
            h2h_tot = len(h2h_df)
            for _, r in h2h_df.iterrows():
                is_h_home = (r["home_team_name"] == home_team)
                hg, ag = r["home_goals"], r["away_goals"]
                if hg == ag:
                    h2h_d += 1
                elif (hg > ag and is_h_home) or (ag > hg and not is_h_home):
                    h2h_h_w += 1
                else:
                    h2h_a_w += 1

        return {
            "form_3_h": f3_h, "form_3_a": f3_a,
            "form_5_h": f5_h, "form_5_a": f5_a,
            "gd_5_h": gd5_h, "gd_5_a": gd5_a,
            "gf_5_h": gf5_h, "gf_5_a": gf5_a,
            "ga_5_h": ga5_h, "ga_5_a": ga5_a,
            "rest_h": rest_h, "rest_a": rest_a,
            "rest_diff": rest_h - rest_a,
            "h2h_h_wins": h2h_h_w, "h2h_a_wins": h2h_a_w,
            "h2h_draws": h2h_d, "h2h_total": h2h_tot
        }

    def _load_models(self):
        dc_path = self.models_dir / "dixon_coles.joblib"
        xgb_path = self.models_dir / "xgb_tuned.joblib"
        lgb_path = self.models_dir / "lgbm_tuned.joblib"
        cat_path = self.models_dir / "catboost_tuned.joblib"
        stack_path = self.models_dir / "stacking_meta.joblib"
        ts_path = self.models_dir / "temperature_scaler.json"

        if dc_path.exists():
            self.dixon_coles = joblib.load(dc_path)
        if xgb_path.exists():
            self.xgb_model = joblib.load(xgb_path)
        if lgb_path.exists():
            self.lgb_model = joblib.load(lgb_path)
        if cat_path.exists():
            self.cat_model = joblib.load(cat_path)
        if stack_path.exists():
            self.stacking_meta = StackingMetaLearner.load(stack_path)
        if ts_path.exists():
            self.scaler = TemperatureScaler.load(ts_path)
        else:
            self.scaler = TemperatureScaler(temperature=1.0)

    def predict_match(
        self,
        home_team: str,
        away_team: str,
        match_date: Optional[str] = None,
        home_country: Optional[str] = None,
        away_country: Optional[str] = None,
        stage: str = "League Phase",
        matchday: int = 1,
        market_odds: Optional[Dict[str, float]] = None,
    ) -> MatchPrediction:
        """Predicts a single match across 1X2, Over/Under, BTTS, and exact scores."""
        h_canon = self.elo_mgr.canonical_name(home_team)
        a_canon = self.elo_mgr.canonical_name(away_team)

        # 1. Elo and UEFA coefficients
        h_elo = self.elo_mgr.get_elo(h_canon, match_date, home_country)
        a_elo = self.elo_mgr.get_elo(a_canon, match_date, away_country)
        elo_diff = h_elo - a_elo

        with open(settings.COEFFICIENTS_PATH, "r", encoding="utf-8") as f:
            uefa_coefs = json.load(f)
        h_coef = uefa_coefs.get(home_country, uefa_coefs.get("DEFAULT", {})).get("coef", 0.50) if home_country else 0.50
        a_coef = uefa_coefs.get(away_country, uefa_coefs.get("DEFAULT", {})).get("coef", 0.50) if away_country else 0.50
        coef_diff = h_coef - a_coef
        coef_ratio = h_coef / max(a_coef, 0.1)

        # 2. Geo & Pedigree
        dist_km = self.geo_mgr.calculate_distance_km(h_canon, a_canon)
        fatigue = self.geo_mgr.calculate_travel_fatigue(dist_km)
        h_pedigree = self.geo_mgr.get_club_pedigree(h_canon)
        a_pedigree = self.geo_mgr.get_club_pedigree(a_canon)
        pedigree_diff = h_pedigree - a_pedigree
        pedigree_ratio = h_pedigree / max(a_pedigree, 10.0)

        is_hostile = 1 if home_country in HOSTILE_COUNTRIES else 0
        is_knockout = 1 if any(k in stage.lower() for k in ["playoff", "round of 16", "quarter", "semi", "final"]) else 0

        # Direct Elo probability baseline
        from src.features.builder import elo_win_probability
        p_h_elo, p_d_elo, p_a_elo = elo_win_probability(elo_diff)

        # 3. Level-1: Dixon-Coles Prediction & Multi-Market Derivation
        if self.dixon_coles is not None:
            p_dc, score_grid, (lam_h, lam_a) = self.dixon_coles.predict_proba(
                home_team=h_canon, away_team=a_canon, home_elo=h_elo, away_elo=a_elo,
                is_hostile=(is_hostile == 1), coef_ratio=coef_ratio, travel_fatigue=fatigue
            )
            multi_markets = UCLDixonColes.derive_multi_markets(score_grid)
        else:
            p_dc = np.array([p_h_elo, p_d_elo, p_a_elo])
            lam_h, lam_a = 1.6, 1.2
            multi_markets = {
                "over_under": {"over_2_5": 0.55, "under_2_5": 0.45},
                "btts": {"yes": 0.52, "no": 0.48},
                "top_exact_scores": {"2-1": 11.0, "1-1": 10.5, "2-0": 9.5}
            }

        # 4. Level-1: Machine Learning Predictions (Dynamic causal features)
        dyn_feats = self._compute_dynamic_features(h_canon, a_canon, match_date)
        feat_dict = {
            "home_elo": h_elo, "away_elo": a_elo, "elo_diff": elo_diff,
            "home_uefa_coef": h_coef, "away_uefa_coef": a_coef,
            "coef_diff": coef_diff, "coef_ratio": coef_ratio,
            "travel_distance_km": dist_km, "travel_fatigue": fatigue,
            "home_club_pedigree": h_pedigree, "away_club_pedigree": a_pedigree,
            "pedigree_diff": pedigree_diff, "pedigree_ratio": pedigree_ratio,
            "elo_prob_h": p_h_elo, "elo_prob_d": p_d_elo, "elo_prob_a": p_a_elo,
            "form_3_h": dyn_feats["form_3_h"], "form_3_a": dyn_feats["form_3_a"],
            "form_5_h": dyn_feats["form_5_h"], "form_5_a": dyn_feats["form_5_a"],
            "gd_5_h": dyn_feats["gd_5_h"], "gd_5_a": dyn_feats["gd_5_a"],
            "gf_5_h": dyn_feats["gf_5_h"], "gf_5_a": dyn_feats["gf_5_a"],
            "ga_5_h": dyn_feats["ga_5_h"], "ga_5_a": dyn_feats["ga_5_a"],
            "rest_h": dyn_feats["rest_h"], "rest_a": dyn_feats["rest_a"], "rest_diff": dyn_feats["rest_diff"],
            "h2h_h_wins": dyn_feats["h2h_h_wins"], "h2h_a_wins": dyn_feats["h2h_a_wins"], "h2h_draws": dyn_feats["h2h_draws"], "h2h_total": dyn_feats["h2h_total"],
            "is_knockout": is_knockout, "is_hostile_venue": is_hostile, "matchday": matchday
        }
        X_df = pd.DataFrame([feat_dict])[FEATURE_COLS]

        p_xgb = self.xgb_model.predict_proba(X_df)[0] if self.xgb_model else p_dc
        p_lgb = self.lgb_model.predict_proba(X_df)[0] if self.lgb_model else p_dc
        p_cat = self.cat_model.predict_proba(X_df)[0] if self.cat_model else p_dc

        # 5. Level-2: Stacking Meta-Learner or Dynamic Blend
        if self.stacking_meta is not None:
            meta_input = np.hstack([p_dc, p_xgb, p_lgb, p_cat]).reshape(1, -1)
            raw_blend = self.stacking_meta.predict_proba(meta_input)[0]
        else:
            raw_blend = (
                settings.WEIGHT_DC * p_dc +
                settings.WEIGHT_XGB * p_xgb +
                settings.WEIGHT_LGB * p_lgb +
                settings.WEIGHT_CAT * p_cat
            )
            raw_blend = raw_blend / np.sum(raw_blend)

        # 6. Temperature Scaling Calibration
        if self.scaler:
            calibrated = self.scaler.transform(raw_blend.reshape(1, -1))[0]
        else:
            calibrated = raw_blend

        probs_dict = {
            "H": float(calibrated[0]),
            "D": float(calibrated[1]),
            "A": float(calibrated[2]),
        }

        # 7. Strategic derivatives
        pred_tag = max(probs_dict, key=probs_dict.get)
        safety = compute_safety_tier(probs_dict)
        confidence = compute_confidence(probs_dict)
        dc_tag, dc_prob = compute_double_chance(probs_dict)

        # 8. Value Betting Edge
        edge_eval = None
        if market_odds:
            edge_eval = ValueBettingEngine.evaluate_market(probs_dict, market_odds)

        return MatchPrediction(
            home_team=h_canon,
            away_team=a_canon,
            match_date=match_date or "2026-09-17",
            matchday=matchday,
            stage=stage,
            probs=probs_dict,
            prediction=pred_tag,
            double_chance=dc_tag,
            double_chance_prob=dc_prob,
            safety_tier=safety,
            confidence=confidence,
            lambda_home=lam_h,
            lambda_away=lam_a,
            over_under=multi_markets.get("over_under", {}),
            btts=multi_markets.get("btts", {}),
            top_exact_scores=multi_markets.get("top_exact_scores", {}),
            conditioned_top_scores=multi_markets.get("conditioned_top_scores", {}),
            travel_distance_km=round(dist_km, 1),
            travel_fatigue=round(fatigue, 2),
            edge=edge_eval
        )
