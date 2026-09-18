from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, Float, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import settings

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    country = Column(String(3), nullable=False)
    uefa_coef = Column(Float, default=0.50)
    current_elo = Column(Float, default=1550.0)

class Fixture(Base):
    __tablename__ = "fixtures"
    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(String(10), nullable=False)
    stage = Column(String(50), nullable=False)
    matchday = Column(Integer, default=0)
    date = Column(String(10), nullable=False)
    home_team_id = Column(Integer, nullable=False)
    away_team_id = Column(Integer, nullable=False)
    home_team_name = Column(String(100), nullable=False)
    away_team_name = Column(String(100), nullable=False)
    home_country = Column(String(3), default="")
    away_country = Column(String(3), default="")
    home_goals = Column(Integer, nullable=True)
    away_goals = Column(Integer, nullable=True)
    home_elo = Column(Float, default=1500.0)
    away_elo = Column(Float, default=1500.0)
    elo_diff = Column(Float, default=0.0)
    status = Column(String(20), default="FINISHED")

def get_engine(db_path: Path = None):
    p = db_path or settings.DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{p}")

def init_db(engine = None):
    eng = engine or get_engine()
    Base.metadata.create_all(eng)
    return eng

SessionLocal = sessionmaker()
