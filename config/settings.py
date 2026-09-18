"""Configuration management for ucl-predictor."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent
    CONFIG_DIR: Path = ROOT_DIR / "config"
    DATA_DIR: Path = ROOT_DIR / "data"
    RAW_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    MODELS_DIR: Path = ROOT_DIR / "models"
    
    DB_PATH: Path = PROCESSED_DIR / "ucl.db"
    FEATURES_PATH: Path = PROCESSED_DIR / "features.parquet"
    COEFFICIENTS_PATH: Path = CONFIG_DIR / "uefa_coefficients.json"
    
    # Statistical model defaults
    DEFAULT_HOME_ADVANTAGE: float = 1.28
    DEFAULT_ELO_SIGMA: float = 240.0
    DEFAULT_RECENCY_HALF_LIFE_DAYS: float = 500.0
    DEFAULT_SHRINKAGE_MATCHES: int = 6
    DEFAULT_RHO: float = -0.10
    DEFAULT_DRAW_BOOST: float = 0.06
    DEFAULT_DRAW_PENALTY_THRESHOLD: float = 0.08
    DEFAULT_DRAW_PENALTY_STRENGTH: float = 0.06
    DEFAULT_ELO_GAP_THRESHOLD: float = 80.0
    DEFAULT_ELO_GAP_INFLATION: float = 0.28
    
    # Ensemble weights
    WEIGHT_DC: float = 0.40
    WEIGHT_XGB: float = 0.30
    WEIGHT_LGB: float = 0.15
    WEIGHT_CAT: float = 0.15
    
    # API Keys (optional)
    ODDS_API_KEY: str = os.getenv("ODDS_API_KEY", "")
    BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY", "")

settings = Settings()
