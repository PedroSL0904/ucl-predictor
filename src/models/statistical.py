"""Dixon-Coles bivariate Poisson model optimized for UEFA Champions League with Multi-Market Derivations."""
from __future__ import annotations
import math
from typing import Dict, Optional, Tuple, List, Any
import numpy as np
import pandas as pd
from scipy.stats import poisson

from config.settings import settings
from src.features.strengths import compute_weighted_strengths


def dc_tau(x: int, y: int, lam_h: float, lam_a: float, rho: float) -> float:
    """Dixon & Coles (1997) low-score adjustment factor."""
    if x == 0 and y == 0:
        return 1.0 - lam_h * lam_a * rho
    if x == 0 and y == 1:
        return 1.0 + lam_h * rho
    if x == 1 and y == 0:
        return 1.0 + lam_a * rho
    if x == 1 and y == 1:
        return 1.0 - rho
    return 1.0


class UCLDixonColes:
    """Dixon-Coles Poisson model with Bayesian shrinkage, Elo inflation and draw boost."""

    def __init__(
        self,
        home_advantage: float = settings.DEFAULT_HOME_ADVANTAGE,
        elo_sigma: float = settings.DEFAULT_ELO_SIGMA,
        recency_half_life_days: float = settings.DEFAULT_RECENCY_HALF_LIFE_DAYS,
        shrinkage_matches: int = settings.DEFAULT_SHRINKAGE_MATCHES,
        rho: float = settings.DEFAULT_RHO,
        draw_boost: float = settings.DEFAULT_DRAW_BOOST,
        draw_penalty_threshold: float = settings.DEFAULT_DRAW_PENALTY_THRESHOLD,
        draw_penalty_strength: float = settings.DEFAULT_DRAW_PENALTY_STRENGTH,
        elo_gap_threshold: float = settings.DEFAULT_ELO_GAP_THRESHOLD,
        elo_gap_inflation: float = settings.DEFAULT_ELO_GAP_INFLATION,
    ):
        self.home_advantage = home_advantage
        self.elo_sigma = elo_sigma
        self.recency_half_life_days = recency_half_life_days
        self.shrinkage_matches = shrinkage_matches
        self.rho = rho
        self.draw_boost = draw_boost
        self.draw_penalty_threshold = draw_penalty_threshold
        self.draw_penalty_strength = draw_penalty_strength
        self.elo_gap_threshold = elo_gap_threshold
        self.elo_gap_inflation = elo_gap_inflation
        
        self.league_avg_home = 1.75
        self.league_avg_away = 1.33
        self.strengths: Dict[int, Dict[str, float]] = {}

    def fit(self, df: pd.DataFrame, as_of: str | None = None) -> UCLDixonColes:
        data = df.dropna(subset=["home_goals", "away_goals"]).copy()
        if len(data) == 0:
            return self

        self.league_avg_home = float(data["home_goals"].mean())
        self.league_avg_away = float(data["away_goals"].mean())
        if self.league_avg_away > 0:
            self.home_advantage = self.league_avg_home / self.league_avg_away

        self.strengths = compute_weighted_strengths(
            data,
            as_of=as_of,
            elo_sigma=self.elo_sigma,
            recency_half_life_days=self.recency_half_life_days,
            shrinkage_matches=self.shrinkage_matches,
        )
        return self

    def _lambda(
        self,
        home_id: int,
        away_id: int,
        is_hostile: bool = False,
        coef_ratio: float = 1.0,
        travel_fatigue: float = 0.0,
    ) -> Tuple[float, float]:
        h_s = self.strengths.get(int(home_id), {"attack": 1.0, "defense": 1.0})
        a_s = self.strengths.get(int(away_id), {"attack": 1.0, "defense": 1.0})

        lam_h = self.league_avg_home * h_s["attack"] * a_s["defense"]
        lam_a = self.league_avg_away * a_s["attack"] * h_s["defense"]

        # Travel fatigue penalty on away team
        if travel_fatigue > 0.4:
            lam_a *= (1.0 - 0.10 * travel_fatigue)
            lam_h *= (1.0 + 0.05 * travel_fatigue)

        # Boost home advantage in hostile atmospheres (e.g. Istanbul, Belgrade)
        if is_hostile:
            lam_h *= 1.08
            lam_a *= 0.92

        # Cross-league quality adjustment
        if coef_ratio > 1.4:
            lam_h *= 1.06
            lam_a *= 0.94
        elif coef_ratio < 0.7:
            lam_h *= 0.94
            lam_a *= 1.06

        return float(lam_h), float(lam_a)

    def _apply_elo_inflation(
        self, lam_h: float, lam_a: float, home_elo: float, away_elo: float
    ) -> Tuple[float, float]:
        elo_diff = home_elo - away_elo
        if elo_diff > self.elo_gap_threshold:
            factor = 1.0 + (math.log10(elo_diff / self.elo_gap_threshold) * self.elo_gap_inflation)
            return lam_h * factor, lam_a / factor
        elif elo_diff < -self.elo_gap_threshold:
            factor = 1.0 + (math.log10(-elo_diff / self.elo_gap_threshold) * self.elo_gap_inflation)
            return lam_h / factor, lam_a * factor
        return lam_h, lam_a

    def _apply_draw_adjustments(self, p_h: float, p_d: float, p_a: float) -> Tuple[float, float, float]:
        diff = abs(p_h - p_a)

        if diff <= self.draw_penalty_threshold and self.draw_boost > 0:
            proximity = 1.0 - (diff / max(self.draw_penalty_threshold, 1e-9))
            boost_factor = self.draw_boost * proximity
            avg_side = (p_h + p_a) * 0.5
            mass_to_move = avg_side * boost_factor
            p_h -= mass_to_move * 0.5
            p_a -= mass_to_move * 0.5
            p_d += mass_to_move
            tot = p_h + p_d + p_a
            return p_h / tot, p_d / tot, p_a / tot

        if diff > self.draw_penalty_threshold:
            excess = min(1.0, (diff - self.draw_penalty_threshold) / 0.5)
            penalty = self.draw_penalty_strength * excess
            mass = p_d * penalty
            if p_h > p_a:
                p_h += mass * 0.65
                p_a += mass * 0.35
            else:
                p_a += mass * 0.65
                p_h += mass * 0.35
            p_d *= (1.0 - penalty)
            tot = p_h + p_d + p_a
            return p_h / tot, p_d / tot, p_a / tot

        return p_h, p_d, p_a

    def predict_proba(
        self,
        home_id: int,
        away_id: int,
        home_elo: Optional[float] = None,
        away_elo: Optional[float] = None,
        is_hostile: bool = False,
        coef_ratio: float = 1.0,
        travel_fatigue: float = 0.0,
        max_goals: int = 7,
    ) -> Tuple[np.ndarray, np.ndarray, Tuple[float, float]]:
        lam_h, lam_a = self._lambda(home_id, away_id, is_hostile, coef_ratio, travel_fatigue)

        if home_elo is not None and away_elo is not None:
            lam_h, lam_a = self._apply_elo_inflation(lam_h, lam_a, home_elo, away_elo)

        score_probs = np.zeros((max_goals + 1, max_goals + 1))
        for h in range(max_goals + 1):
            for a in range(max_goals + 1):
                score_probs[h, a] = poisson.pmf(h, lam_h) * poisson.pmf(a, lam_a)

        for h in range(min(2, score_probs.shape[0])):
            for a in range(min(2, score_probs.shape[1])):
                score_probs[h, a] *= dc_tau(h, a, lam_h, lam_a, self.rho)

        tot = score_probs.sum()
        if tot > 0:
            score_probs /= tot

        prob_h = float(np.tril(score_probs, k=-1).sum())
        prob_d = float(np.diag(score_probs).sum())
        prob_a = float(np.triu(score_probs, k=1).sum())

        prob_h, prob_d, prob_a = self._apply_draw_adjustments(prob_h, prob_d, prob_a)

        return np.array([prob_h, prob_d, prob_a]), score_probs, (lam_h, lam_a)

    @staticmethod
    def derive_multi_markets(score_grid: np.ndarray) -> Dict[str, Any]:
        """Analytically derives Over/Under, BTTS and exact scores from the 2D score grid."""
        max_h, max_a = score_grid.shape

        # 1. Over / Under Lines
        over_1_5 = 0.0
        over_2_5 = 0.0
        over_3_5 = 0.0
        btts_yes = 0.0

        scores_list = []
        for h in range(max_h):
            for a in range(max_a):
                p = float(score_grid[h, a])
                tot_goals = h + a
                if tot_goals > 1.5:
                    over_1_5 += p
                if tot_goals > 2.5:
                    over_2_5 += p
                if tot_goals > 3.5:
                    over_3_5 += p
                if h >= 1 and a >= 1:
                    btts_yes += p
                scores_list.append((f"{h}-{a}", p))

        # Sort exact scores descending
        scores_list.sort(key=lambda item: item[1], reverse=True)
        top5_scores = {s: round(p * 100, 1) for s, p in scores_list[:5]}

        return {
            "over_under": {
                "over_1_5": round(over_1_5, 4),
                "under_1_5": round(1.0 - over_1_5, 4),
                "over_2_5": round(over_2_5, 4),
                "under_2_5": round(1.0 - over_2_5, 4),
                "over_3_5": round(over_3_5, 4),
                "under_3_5": round(1.0 - over_3_5, 4),
            },
            "btts": {
                "yes": round(btts_yes, 4),
                "no": round(1.0 - btts_yes, 4)
            },
            "top_exact_scores": top5_scores
        }
