import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from sqlalchemy.orm import sessionmaker

sys.stdout.reconfigure(encoding='utf-8')

from config.settings import settings
from src.data.db import init_db, Team, Fixture
from src.data.openfootball import parse_all_seasons
from src.data.clubelo import ClubEloManager

def build_database():
    print("Initializing SQLite database at:", settings.DB_PATH)
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing rows to ensure idempotence
    session.query(Fixture).delete()
    session.query(Team).delete()
    session.commit()

    elo_mgr = ClubEloManager()
    with open(settings.COEFFICIENTS_PATH, "r", encoding="utf-8") as f:
        uefa_coefs = json.load(f)

    # 1. Parse raw openfootball matches
    raw_matches = parse_all_seasons(settings.RAW_DIR)
    print(f"Parsed {len(raw_matches)} raw match entries from openfootball.")

    # Sort matches chronologically so Elo lookups and updates are strictly causal
    raw_matches = sorted(raw_matches, key=lambda m: (m["date"], m["season"]))

    team_name_to_id = {}
    team_records = {}

    # Register teams
    for m in raw_matches:
        h_canon = elo_mgr.canonical_name(m["home_team"])
        a_canon = elo_mgr.canonical_name(m["away_team"])
        
        for name, country in [(h_canon, m["home_country"]), (a_canon, m["away_country"])]:
            if name not in team_records:
                coef = uefa_coefs.get(country, uefa_coefs.get("DEFAULT", {})).get("coef", 0.35)
                base_elo = elo_mgr.get_elo(name, None, country)
                team_records[name] = {
                    "name": name,
                    "country": country,
                    "uefa_coef": coef,
                    "current_elo": base_elo
                }

    for name, data in sorted(team_records.items()):
        t = Team(
            name=name,
            country=data["country"],
            uefa_coef=data["uefa_coef"],
            current_elo=data["current_elo"]
        )
        session.add(t)
    session.commit()

    # Reload team IDs
    for t in session.query(Team).all():
        team_name_to_id[t.name] = t.id

    print(f"Registered {len(team_name_to_id)} unique European clubs in database.")

    # 2. Insert fixtures with pre-match Elo ratings
    fixtures_to_insert = []
    for m in raw_matches:
        h_canon = elo_mgr.canonical_name(m["home_team"])
        a_canon = elo_mgr.canonical_name(m["away_team"])
        h_id = team_name_to_id[h_canon]
        a_id = team_name_to_id[a_canon]

        m_date = m["date"]
        h_elo = elo_mgr.get_elo(h_canon, m_date, m["home_country"])
        a_elo = elo_mgr.get_elo(a_canon, m_date, m["away_country"])
        elo_diff = h_elo - a_elo

        fix = Fixture(
            season=m["season"],
            stage=m["stage"],
            matchday=m["matchday"],
            date=m_date,
            home_team_id=h_id,
            away_team_id=a_id,
            home_team_name=h_canon,
            away_team_name=a_canon,
            home_country=m["home_country"],
            away_country=m["away_country"],
            home_goals=m["home_goals"],
            away_goals=m["away_goals"],
            home_elo=h_elo,
            away_elo=a_elo,
            elo_diff=elo_diff,
            status=m["status"]
        )
        fixtures_to_insert.append(fix)

    session.bulk_save_objects(fixtures_to_insert)
    session.commit()

    # 3. Validation & Statistical Summary
    total_fixtures = session.query(Fixture).count()
    finished = session.query(Fixture).filter(Fixture.status == "FINISHED").all()
    
    home_wins = sum(1 for f in finished if f.home_goals > f.away_goals)
    draws = sum(1 for f in finished if f.home_goals == f.away_goals)
    away_wins = sum(1 for f in finished if f.home_goals < f.away_goals)
    total_goals = sum((f.home_goals + f.away_goals) for f in finished)
    avg_goals = total_goals / len(finished) if finished else 0.0

    print("\n" + "="*50)
    print("🏆 UCL DATABASE POPULATION COMPLETE 🏆")
    print(f"Total fixtures saved: {total_fixtures}")
    print(f"Finished matches: {len(finished)}")
    print(f"Average goals per match: {avg_goals:.2f}")
    print(f"Outcome Distribution: Home: {home_wins/len(finished)*100:.1f}%, Draw: {draws/len(finished)*100:.1f}%, Away: {away_wins/len(finished)*100:.1f}%")
    print("="*50)

    # Top 10 clubs by Elo in UCL history
    print("\nTop 10 European Clubs by Latest Elo in UCL:")
    top_clubs = session.query(Team).order_by(Team.current_elo.desc()).limit(10).all()
    for i, c in enumerate(top_clubs, 1):
        print(f"  {i}. {c.name} ({c.country}): {c.current_elo:.1f} Elo (UEFA Coef: {c.uefa_coef})")

if __name__ == "__main__":
    build_database()
