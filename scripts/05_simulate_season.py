"""Monte Carlo simulation of the 36-team Champions League season and bracket."""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

from config.settings import settings
from src.predictor import UCLPredictor
from src.simulation.swiss_stage import SwissStageSimulator
from src.simulation.bracket import KnockoutSimulator

def run_ucl_simulation(season: str = "2024-25", n_sims: int = 1000):
    print(f"\n=======================================================")
    print(f"🎲 SIMULATING UEFA CHAMPIONS LEAGUE ({season}) 🎲")
    print(f"Running {n_sims} Monte Carlo iterations...")
    print(f"=======================================================")

    predictor = UCLPredictor()
    df_feat = pd.read_parquet(settings.FEATURES_PATH)
    season_matches = df_feat[df_feat["season"] == season].copy()
    
    if season_matches.empty:
        print(f"No matches found for season {season}")
        return

    # Extract unique teams in this season
    teams = sorted(list(set(season_matches["home_team_name"].unique()) | set(season_matches["away_team_name"].unique())))
    print(f"Found {len(teams)} participating European clubs in {season}.")

    # Pre-calculate match probabilities for all fixtures in the season
    sim_fixtures = []
    for _, row in season_matches.iterrows():
        # Fast prediction
        h = row["home_team_name"]
        a = row["away_team_name"]
        pred = predictor.predict_match(h, a, match_date=str(row["date"])[:10])
        sim_fixtures.append({
            "home_team": h,
            "away_team": a,
            "probs": [pred.probs["H"], pred.probs["D"], pred.probs["A"]],
            "lam_h": pred.lambda_home,
            "lam_a": pred.lambda_away,
            "home_goals": row["home_goals"],
            "away_goals": row["away_goals"]
        })

    # 1. Run Swiss Stage Simulation
    swiss_sim = SwissStageSimulator(sim_fixtures, teams)
    table_df = swiss_sim.run_simulations(n_simulations=n_sims)

    print("\n" + "="*80)
    print(f"📊 PROJECTED SWISS LEAGUE TABLE ({season}) - 36 TEAMS")
    print("="*80)
    print(f"{'Pos':<4} {'Club':<26} {'Exp Pts':<10} {'Top 8 %':<12} {'Playoff %':<12} {'Elim %':<10}")
    print("-" * 80)
    for i, row in table_df.iterrows():
        status_marker = "🌟" if i < 8 else ("⚔️" if i < 24 else "❌")
        print(f"{i+1:<2} {status_marker} {row['team']:<25} {row['expected_points']:<10.1f} {row['prob_top_8']:<12.1f} {row['prob_playoff_9_24']:<12.1f} {row['prob_eliminated']:<10.1f}")
    print("-" * 80)
    print("🌟 Top 8: Direct to Round of 16 | ⚔️ 9-24: Knockout Play-offs | ❌ 25-36: Eliminated")

    # 2. Knockout & Champion Simulation
    print("\n=======================================================")
    print("🏆 SIMULATING TOURNAMENT CHAMPION ODDS 🏆")
    print("=======================================================")
    champion_counts = {t: 0 for t in teams}
    rng = np.random.default_rng(42)

    # Top contenders from Swiss Table
    top_contenders = table_df.head(16)["team"].tolist()

    for _ in range(n_sims):
        # Sample bracket from top contenders
        # Round of 16 -> QF -> SF -> Final
        current_round = top_contenders.copy()
        rng.shuffle(current_round)

        while len(current_round) > 1:
            next_round = []
            for i in range(0, len(current_round), 2):
                t1 = current_round[i]
                t2 = current_round[i+1]
                e1 = predictor.elo_mgr.get_elo(t1)
                e2 = predictor.elo_mgr.get_elo(t2)
                p1 = 1.0 / (1.0 + 10.0 ** (-(e1 - e2) / 400.0))
                winner = t1 if rng.random() < p1 else t2
                next_round.append(winner)
            current_round = next_round

        champion_counts[current_round[0]] += 1

    champ_df = pd.DataFrame([
        {"team": t, "prob_champion": round(count / n_sims * 100, 1)}
        for t, count in champion_counts.items() if count > 0
    ]).sort_values("prob_champion", ascending=False).reset_index(drop=True)

    print(f"{'Rank':<5} {'Club':<26} {'Champion Prob %':<15}")
    print("-" * 50)
    for i, row in champ_df.head(10).iterrows():
        print(f" {i+1:<4} {row['team']:<26} {row['prob_champion']:<15.1f}%")
    print("=" * 50)

if __name__ == "__main__":
    run_ucl_simulation("2024-25", 1000)
