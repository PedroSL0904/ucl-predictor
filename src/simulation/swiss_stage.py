"""Monte Carlo simulation of the 36-team UEFA Champions League Swiss Stage."""
from __future__ import annotations
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd

class SwissStageSimulator:
    """Simulates the 36-team single league table across N Monte Carlo iterations."""

    def __init__(self, fixtures: List[Dict[str, Any]], teams: List[str]):
        self.fixtures = fixtures
        self.teams = teams

    def simulate_one_season(self, rng: np.random.Generator) -> Dict[str, Dict[str, int]]:
        table = {
            t: {"points": 0, "gf": 0, "ga": 0, "gd": 0, "won": 0, "drawn": 0, "lost": 0}
            for t in self.teams
        }

        for f in self.fixtures:
            h = f["home_team"]
            a = f["away_team"]
            
            # If match is already finished with actual goals, use real result
            if f.get("home_goals") is not None and f.get("away_goals") is not None:
                hg = f["home_goals"]
                ag = f["away_goals"]
            else:
                probs = f.get("probs", [0.45, 0.22, 0.33])
                # Sample 1X2 outcome
                outcome = rng.choice(["H", "D", "A"], p=probs)
                if outcome == "H":
                    hg = int(rng.poisson(f.get("lam_h", 1.8)))
                    ag = int(rng.poisson(f.get("lam_a", 1.0)))
                    if hg <= ag:
                        hg = ag + 1
                elif outcome == "A":
                    hg = int(rng.poisson(f.get("lam_h", 1.0)))
                    ag = int(rng.poisson(f.get("lam_a", 1.8)))
                    if ag <= hg:
                        ag = hg + 1
                else:  # Draw
                    goals = int(rng.choice([0, 1, 2, 3], p=[0.25, 0.50, 0.20, 0.05]))
                    hg = goals
                    ag = goals

            # Update table
            if h in table and a in table:
                table[h]["gf"] += hg
                table[h]["ga"] += ag
                table[h]["gd"] += (hg - ag)
                table[a]["gf"] += ag
                table[a]["ga"] += hg
                table[a]["gd"] += (ag - hg)

                if hg > ag:
                    table[h]["points"] += 3
                    table[h]["won"] += 1
                    table[a]["lost"] += 1
                elif hg == ag:
                    table[h]["points"] += 1
                    table[a]["points"] += 1
                    table[h]["drawn"] += 1
                    table[a]["drawn"] += 1
                else:
                    table[a]["points"] += 3
                    table[a]["won"] += 1
                    table[h]["lost"] += 1

        return table

    def run_simulations(self, n_simulations: int = 1000, seed: int = 42) -> pd.DataFrame:
        rng = np.random.default_rng(seed)
        
        top8_counts = {t: 0 for t in self.teams}
        playoff_counts = {t: 0 for t in self.teams}
        elim_counts = {t: 0 for t in self.teams}
        pts_accum = {t: [] for t in self.teams}
        rank_accum = {t: [] for t in self.teams}

        for _ in range(n_simulations):
            table = self.simulate_one_season(rng)
            # Sort by points desc, then goal difference desc, then goals for desc
            ranked = sorted(
                table.items(),
                key=lambda item: (item[1]["points"], item[1]["gd"], item[1]["gf"]),
                reverse=True
            )

            for rank_idx, (team, stats) in enumerate(ranked, 1):
                pts_accum[team].append(stats["points"])
                rank_accum[team].append(rank_idx)

                if rank_idx <= 8:
                    top8_counts[team] += 1
                elif rank_idx <= 24:
                    playoff_counts[team] += 1
                else:
                    elim_counts[team] += 1

        current_stats = {
            t: {"pj": 0, "points": 0, "gf": 0, "ga": 0, "gd": 0}
            for t in self.teams
        }
        for f in self.fixtures:
            if f.get("home_goals") is not None and f.get("away_goals") is not None:
                h, a = f["home_team"], f["away_team"]
                hg, ag = f["home_goals"], f["away_goals"]
                if h in current_stats and a in current_stats:
                    current_stats[h]["pj"] += 1
                    current_stats[a]["pj"] += 1
                    current_stats[h]["gf"] += hg
                    current_stats[h]["ga"] += ag
                    current_stats[h]["gd"] += (hg - ag)
                    current_stats[a]["gf"] += ag
                    current_stats[a]["ga"] += hg
                    current_stats[a]["gd"] += (ag - hg)
                    if hg > ag:
                        current_stats[h]["points"] += 3
                    elif hg == ag:
                        current_stats[h]["points"] += 1
                        current_stats[a]["points"] += 1
                    else:
                        current_stats[a]["points"] += 3

        summary = []
        for t in self.teams:
            avg_pts = np.mean(pts_accum[t]) if pts_accum[t] else 0.0
            avg_rank = np.mean(rank_accum[t]) if rank_accum[t] else 18.0
            summary.append({
                "team": t,
                "current_pj": current_stats[t]["pj"],
                "current_points": current_stats[t]["points"],
                "current_gd": current_stats[t]["gd"],
                "projected_rank": round(float(avg_rank), 1),
                "expected_points": round(float(avg_pts), 1),
                "prob_top_8": round(top8_counts[t] / n_simulations * 100, 1),
                "prob_playoff_9_24": round(playoff_counts[t] / n_simulations * 100, 1),
                "prob_eliminated": round(elim_counts[t] / n_simulations * 100, 1)
            })

        df_res = pd.DataFrame(summary).sort_values("projected_rank", ascending=True).reset_index(drop=True)
        return df_res
