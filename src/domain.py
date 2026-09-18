"""Domain entities and value objects for UCL predictor 2.0."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Tuple, List, Any


class MatchOutcome(str, Enum):
    HOME = "H"
    DRAW = "D"
    AWAY = "A"


class SafetyTier(str, Enum):
    BANQUERO = "Banquero Seguro"
    FAVORITO_RIESGO_EMPATE = "Favorito con Riesgo de Empate"
    PARIDAD = "Paridad (Alto Riesgo / Empate)"
    FIRME = "Firme"


class ConfidenceLevel(str, Enum):
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"


@dataclass
class Team:
    id: int
    name: str
    country: str
    city: str = ""
    uefa_coef: float = 0.50
    current_elo: float = 1600.0


@dataclass
class Match:
    id: int
    season: str
    stage: str
    matchday: int
    date: str
    home_team: str
    away_team: str
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    status: str = "SCHEDULED"

    @property
    def outcome(self) -> Optional[MatchOutcome]:
        if self.home_goals is None or self.away_goals is None:
            return None
        if self.home_goals > self.away_goals:
            return MatchOutcome.HOME
        elif self.home_goals < self.away_goals:
            return MatchOutcome.AWAY
        return MatchOutcome.DRAW


@dataclass
class MatchPrediction:
    home_team: str
    away_team: str
    match_date: str
    matchday: int
    stage: str
    probs: Dict[str, float]  # {"H": float, "D": float, "A": float}
    prediction: str  # "H", "D", "A"
    double_chance: str  # "1X", "X2", "12"
    double_chance_prob: float
    safety_tier: SafetyTier
    confidence: ConfidenceLevel
    lambda_home: float
    lambda_away: float
    over_under: Dict[str, float] = field(default_factory=dict)
    btts: Dict[str, float] = field(default_factory=dict)
    top_exact_scores: Dict[str, float] = field(default_factory=dict)
    travel_distance_km: float = 0.0
    travel_fatigue: float = 0.0
    edge: Optional[Dict[str, Any]] = None


@dataclass
class SwissTableEntry:
    team: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_diff(self) -> int:
        return self.goals_for - self.goals_against
