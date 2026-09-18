"""Knockout phase bracket simulator for UEFA Champions League."""
from typing import Dict, List, Tuple
import numpy as np

class KnockoutSimulator:
    """Simulates 2-leg knockout ties and single-match final."""

    @staticmethod
    def simulate_two_leg_tie(
        team_a: str, team_b: str,
        prob_a_home: float, prob_b_home: float,
        rng: np.random.Generator
    ) -> str:
        """Simulates 2 legs: Leg 1 at team_b, Leg 2 at team_a."""
        # Goals leg 1
        g_b1 = int(rng.poisson(1.5 * prob_b_home))
        g_a1 = int(rng.poisson(1.2 * (1.0 - prob_b_home)))
        # Goals leg 2
        g_a2 = int(rng.poisson(1.6 * prob_a_home))
        g_b2 = int(rng.poisson(1.1 * (1.0 - prob_a_home)))

        total_a = g_a1 + g_a2
        total_b = g_b1 + g_b2

        if total_a > total_b:
            return team_a
        elif total_b > total_a:
            return team_b
        else:
            # Extra time / penalty shootout (coin flip weighted by quality)
            p_a_pen = prob_a_home / (prob_a_home + prob_b_home)
            return team_a if rng.random() < p_a_pen else team_b

    @staticmethod
    def simulate_final(team_a: str, team_b: str, elo_a: float, elo_b: float, rng: np.random.Generator) -> str:
        """Single match on neutral venue."""
        dr = elo_a - elo_b
        p_a = 1.0 / (1.0 + 10.0 ** (-dr / 400.0))
        return team_a if rng.random() < p_a else team_b
