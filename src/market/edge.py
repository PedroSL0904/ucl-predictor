"""Value betting, expected value (+EV) and Fractional Kelly staking engine."""
from typing import Dict, Optional, List, Any
from src.market.devig import devig_shin, devig_multiplicative

class ValueBettingEngine:
    """Calculates expected value (+EV), edge vs market and Kelly stake sizing."""

    @staticmethod
    def calculate_kelly_stake(prob: float, decimal_odds: float, fraction: float = 0.25) -> float:
        """Fractional Kelly Criterion: f* = fraction * (b*p - q) / b."""
        if decimal_odds <= 1.0 or prob <= 0:
            return 0.0
        b = decimal_odds - 1.0
        q = 1.0 - prob
        edge_ratio = (b * prob - q) / b
        if edge_ratio <= 0:
            return 0.0
        return round(float(edge_ratio * fraction * 100.0), 2)  # as percentage of bankroll

    @staticmethod
    def evaluate_market(
        model_probs: Dict[str, float],
        market_odds: Dict[str, float],
        min_edge_threshold: float = 0.03
    ) -> Dict[str, Any]:
        """Evaluates 1X2 market for positive expected value (+EV) edges."""
        fair_probs = devig_shin(market_odds) if len(market_odds) == 3 else devig_multiplicative(market_odds)

        evaluations = {}
        has_value = False

        for outcome, m_odd in market_odds.items():
            if outcome not in model_probs or m_odd <= 1.0:
                continue

            p_model = model_probs[outcome]
            p_fair = fair_probs.get(outcome, 1.0 / m_odd)
            
            ev = (p_model * m_odd) - 1.0
            edge = p_model - p_fair
            kelly = ValueBettingEngine.calculate_kelly_stake(p_model, m_odd, fraction=0.25)

            is_value = (edge >= min_edge_threshold) and (ev > 0)
            if is_value:
                has_value = True

            evaluations[outcome] = {
                "market_odd": m_odd,
                "model_prob": round(p_model, 4),
                "fair_market_prob": round(p_fair, 4),
                "expected_value_pct": round(ev * 100.0, 2),
                "edge_pct": round(edge * 100.0, 2),
                "kelly_stake_pct": kelly,
                "is_value_bet": is_value
            }

        return {
            "has_value_bet": has_value,
            "markets": evaluations
        }
