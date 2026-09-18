"""Geographical distance and travel fatigue engine for European competitions."""
import math
import json
from pathlib import Path
from typing import Tuple, Optional

CONFIG_PATH = Path("C:/Users/Boutros/ucl-predictor/config/stadium_cities.json")

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates the great-circle distance between two points on Earth in kilometers."""
    r = 6371.0  # Earth's radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c

class EuropeanGeoManager:
    """Manages stadium locations, distance calculation and travel fatigue."""

    def __init__(self, config_path: Path = CONFIG_PATH):
        self.cities = {}
        self.clubs = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.cities = data.get("cities", {})
                self.clubs = data.get("clubs", {})

    def get_club_coords(self, club_name: str) -> Optional[Tuple[float, float]]:
        info = self.clubs.get(club_name)
        if not info:
            # Fallback search substring
            for c_key, c_info in self.clubs.items():
                if c_key.lower() in club_name.lower() or club_name.lower() in c_key.lower():
                    info = c_info
                    break
        if info:
            city = info.get("city")
            if city in self.cities:
                return (self.cities[city]["lat"], self.cities[city]["lon"])
        return None

    def get_club_pedigree(self, club_name: str) -> float:
        info = self.clubs.get(club_name)
        if not info:
            for c_key, c_info in self.clubs.items():
                if c_key.lower() in club_name.lower() or club_name.lower() in c_key.lower():
                    info = c_info
                    break
        if info:
            return float(info.get("pedigree", 25.0))
        return 20.0  # Default for minor clubs

    def calculate_distance_km(self, home_club: str, away_club: str) -> float:
        h_coords = self.get_club_coords(home_club)
        a_coords = self.get_club_coords(away_club)
        if h_coords and a_coords:
            return haversine_km(h_coords[0], h_coords[1], a_coords[0], a_coords[1])
        return 950.0  # Median European flight distance default

    def calculate_travel_fatigue(self, distance_km: float) -> float:
        """Returns a travel fatigue index (0.0 to 1.0).
        0.0 for domestic/short flights (< 400km), up to 1.0 for cross-continental (> 3500km).
        """
        return min(1.0, max(0.0, (distance_km - 400.0) / 3000.0))
