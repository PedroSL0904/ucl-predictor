import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

sys.stdout.reconfigure(encoding='utf-8')

from src.features.builder import build_features_matrix

if __name__ == "__main__":
    df = build_features_matrix()
    print("Features preview:")
    print(df[["season", "home_team_name", "away_team_name", "elo_diff", "form_5_h", "form_5_a", "outcome"]].tail(10))
