"""Knockout phase bracket simulator for UEFA Champions League."""
from typing import Dict, List, Tuple, Callable, Any
import numpy as np

class KnockoutSimulator:
    """Simulates 2-leg knockout ties and single-match final according to official UEFA format."""

    @staticmethod
    def calc_home_prob(elo_home: float, elo_away: float, home_advantage: float = 65.0) -> float:
        dr = (elo_home - elo_away) + home_advantage
        return 1.0 / (1.0 + 10.0 ** (-dr / 400.0))

    @classmethod
    def simulate_two_leg_tie(
        cls,
        team_a: str, team_b: str,
        elo_a: float, elo_b: float,
        rng: np.random.Generator
    ) -> str:
        """
        Simulates a 2-leg tie. Team A is the seeded team:
        - Leg 1: Team B is at home (Team A away)
        - Leg 2: Team A is at home (Team B away)
        """
        prob_b_home = cls.calc_home_prob(elo_b, elo_a)
        prob_a_home = cls.calc_home_prob(elo_a, elo_b)

        # Leg 1 (at Team B)
        g_b1 = int(rng.poisson(1.5 * prob_b_home))
        g_a1 = int(rng.poisson(1.2 * (1.0 - prob_b_home)))

        # Leg 2 (at Team A)
        g_a2 = int(rng.poisson(1.6 * prob_a_home))
        g_b2 = int(rng.poisson(1.1 * (1.0 - prob_a_home)))

        total_a = g_a1 + g_a2
        total_b = g_b1 + g_b2

        if total_a > total_b:
            return team_a
        elif total_b > total_a:
            return team_b
        else:
            # Extra time / penalty shootout (weighted by overall team Elo)
            dr = elo_a - elo_b
            p_a_pen = 1.0 / (1.0 + 10.0 ** (-dr / 400.0))
            return team_a if rng.random() < p_a_pen else team_b

    @staticmethod
    def simulate_final(team_a: str, team_b: str, elo_a: float, elo_b: float, rng: np.random.Generator) -> str:
        """Single match on neutral venue."""
        dr = elo_a - elo_b
        p_a = 1.0 / (1.0 + 10.0 ** (-dr / 400.0))
        return team_a if rng.random() < p_a else team_b

    @classmethod
    def simulate_knockout_bracket(
        cls,
        ranked_teams: List[str],
        elo_lookup: Callable[[str], float],
        rng: np.random.Generator
    ) -> Dict[str, Any]:
        """
        Simulates full UEFA Champions League knockout stages from Swiss stage ranks:
        1. Ranks 1-8: Direct to Round of 16 (Seeded)
        2. Ranks 9-24: Play-off ties (9-16 seeded vs 17-24 unseeded)
        3. Round of 16: Top 8 seeds vs 8 Play-off winners
        4. Quarter-finals (2-leg ties)
        5. Semi-finals (2-leg ties)
        6. Final (neutral single match)
        """
        top8 = ranked_teams[:8]
        po_seeds = ranked_teams[8:16]      # Ranks 9 to 16
        po_unseeds = ranked_teams[16:24]   # Ranks 17 to 24

        # 1. Knockout Play-offs (9-24)
        po_winners = []
        for i in range(8):
            seed = po_seeds[i]
            unseed = po_unseeds[7 - i]  # E.g. 9th vs 24th, 10th vs 23rd
            w = cls.simulate_two_leg_tie(seed, unseed, elo_lookup(seed), elo_lookup(unseed), rng)
            po_winners.append(w)

        # 2. Round of 16: Official UEFA seeded bracket tree
        # Half A: Seeds 1 vs PO, 8 vs PO, 4 vs PO, 5 vs PO
        # Half B: Seeds 2 vs PO, 7 vs PO, 3 vs PO, 6 vs PO
        bracket_seeds = [
            top8[0],  # Seed 1
            top8[7],  # Seed 8
            top8[3],  # Seed 4
            top8[4],  # Seed 5
            top8[1],  # Seed 2
            top8[6],  # Seed 7
            top8[2],  # Seed 3
            top8[5],  # Seed 6
        ]

        r16_participants = top8 + po_winners
        shuffled_po_winners = po_winners.copy()
        rng.shuffle(shuffled_po_winners)

        qf_participants = []
        for i in range(8):
            top_seed = bracket_seeds[i]
            po_opponent = shuffled_po_winners[i]
            w = cls.simulate_two_leg_tie(top_seed, po_opponent, elo_lookup(top_seed), elo_lookup(po_opponent), rng)
            qf_participants.append(w)

        # 3. Quarter-finals (8 teams, 2-legged ties)
        # Match 0: QF1 (Winner 1 vs Winner 8)
        # Match 1: QF2 (Winner 4 vs Winner 5)
        # Match 2: QF3 (Winner 2 vs Winner 7)
        # Match 3: QF4 (Winner 3 vs Winner 6)
        sf_participants = []
        for i in range(0, 8, 2):
            t1, t2 = qf_participants[i], qf_participants[i+1]
            w = cls.simulate_two_leg_tie(t1, t2, elo_lookup(t1), elo_lookup(t2), rng)
            sf_participants.append(w)

        # 4. Semi-finals (4 teams, 2-legged ties)
        # SF1: Winner QF1 vs Winner QF2 (Path A)
        # SF2: Winner QF3 vs Winner QF4 (Path B)
        finalists = []
        for i in range(0, 4, 2):
            t1, t2 = sf_participants[i], sf_participants[i+1]
            w = cls.simulate_two_leg_tie(t1, t2, elo_lookup(t1), elo_lookup(t2), rng)
            finalists.append(w)

        # 5. Final (neutral venue single match)
        f1, f2 = finalists[0], finalists[1]
        champ = cls.simulate_final(f1, f2, elo_lookup(f1), elo_lookup(f2), rng)

        return {
            "playoffs": ranked_teams[8:24],
            "r16": r16_participants,
            "qf": qf_participants,
            "sf": sf_participants,
            "finalists": finalists,
            "champion": champ
        }
