import json
import unicodedata
from pathlib import Path
from typing import Dict, Optional, Tuple
import pandas as pd

from config.settings import settings

def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")

TEAM_ALIASES = {
    "real madrid cf": "Real Madrid",
    "real madrid": "Real Madrid",
    "fc barcelona": "Barcelona",
    "barcelona": "Barcelona",
    "club atletico de madrid": "Atletico",
    "atletico madrid": "Atletico",
    "atletico": "Atletico",
    "sevilla fc": "Sevilla",
    "sevilla": "Sevilla",
    "valencia cf": "Valencia",
    "villarreal cf": "Villarreal",
    "real sociedad": "Sociedad",
    "athletic club": "Athletic Bilbao",
    "girona fc": "Girona",
    "malaga cf": "Malaga",
    
    "manchester city fc": "Man City",
    "manchester city": "Man City",
    "man city": "Man City",
    "manchester united fc": "Manchester United",
    "manchester united": "Manchester United",
    "man united": "Manchester United",
    "liverpool fc": "Liverpool",
    "liverpool": "Liverpool",
    "arsenal fc": "Arsenal",
    "arsenal": "Arsenal",
    "chelsea fc": "Chelsea",
    "chelsea": "Chelsea",
    "tottenham hotspur fc": "Tottenham",
    "tottenham hotspur": "Tottenham",
    "tottenham": "Tottenham",
    "aston villa fc": "Aston Villa",
    "aston villa": "Aston Villa",
    "newcastle united fc": "Newcastle",
    "leicester city fc": "Leicester",
    "como": "Como",
    "como 1907": "Como",
    "sabah fc": "Sabah FC",
    "sabah futbol klubu": "Sabah FC",
    "sabah": "Sabah FC",
    "viking": "Viking",
    "viking fk": "Viking",
    "bodo/glimt": "Bodo/Glimt",
    "fk bodo/glimt": "Bodo/Glimt",
    "bodø/glimt": "Bodo/Glimt",
    "fk bodø/glimt": "Bodo/Glimt",
    "aek athens": "AEK Athens",
    "aek athens fc": "AEK Athens",
    "aek": "AEK Athens",
    "lask": "LASK",
    "lask linz": "LASK",
    "real betis": "Real Betis",
    "real betis balompie": "Real Betis",
    "betis": "Real Betis",
    "club brujas": "Club Brugge",
    "sporting lisboa": "Sporting",
    "slavia praga": "Slavia Praha",
    "atletico madrid": "Atletico",
    "atletico de madrid": "Atletico",
    "club atletico de madrid": "Atletico",
    "villarreal cf": "Villarreal",
    "villarreal": "Villarreal",
    "fenerbahçe": "Fenerbahce",
    "fenerbahce": "Fenerbahce",
    "fenerbahçe sk": "Fenerbahce",
    "fenerbahce sk": "Fenerbahce",
    "newcastle united fc": "Newcastle",
    "leicester city fc": "Leicester",
    
    "fc bayern munchen": "Bayern Munich",
    "bayern munchen": "Bayern Munich",
    "fc bayern": "Bayern Munich",
    "bayern munich": "Bayern Munich",
    "borussia dortmund": "Dortmund",
    "dortmund": "Dortmund",
    "rb leipzig": "RB Leipzig",
    "bayer 04 leverkusen": "Leverkusen",
    "bayer leverkusen": "Leverkusen",
    "leverkusen": "Leverkusen",
    "vfb stuttgart": "Stuttgart",
    "stuttgart": "Stuttgart",
    "eintracht frankfurt": "Frankfurt",
    "bor monchengladbach": "M'gladbach",
    "vfl wolfsburg": "Wolfsburg",
    "fc schalke 04": "Schalke",
    "tsg 1899 hoffenheim": "Hoffenheim",
    "1 fc union berlin": "Union Berlin",
    
    "juventus fc": "Juventus",
    "juventus": "Juventus",
    "fc internazionale milano": "Inter",
    "inter milan": "Inter",
    "inter": "Inter",
    "ac milan": "Milan",
    "milan": "Milan",
    "ssc napoli": "Napoli",
    "napoli": "Napoli",
    "as roma": "Roma",
    "roma": "Roma",
    "ss lazio": "Lazio",
    "lazio": "Lazio",
    "atalanta bc": "Atalanta",
    "atalanta": "Atalanta",
    "bologna fc 1909": "Bologna",
    "bologna": "Bologna",
    
    "paris saint-germain fc": "Paris SG",
    "paris saint-germain": "Paris SG",
    "paris sg": "Paris SG",
    "psg": "Paris SG",
    "as monaco fc": "Monaco",
    "as monaco": "Monaco",
    "monaco": "Monaco",
    "olympique de marseille": "Marseille",
    "marseille": "Marseille",
    "olympique lyonnais": "Lyon",
    "lyon": "Lyon",
    "losc lille": "Lille",
    "lille osc": "Lille",
    "lille": "Lille",
    "stade rennais": "Rennes",
    "stade brestois 29": "Brest",
    "brest": "Brest",
    "rc lens": "Lens",
    
    "afc ajax": "Ajax",
    "ajax": "Ajax",
    "psv": "PSV Eindhoven",
    "psv eindhoven": "PSV Eindhoven",
    "feyenoord rotterdam": "Feyenoord",
    "feyenoord": "Feyenoord",
    "az alkmaar": "AZ Alkmaar",
    
    "sport lisboa e benfica": "Benfica",
    "benfica": "Benfica",
    "fc porto": "Porto",
    "porto": "Porto",
    "sporting cp": "Sporting",
    "sporting clube de portugal": "Sporting",
    "sporting": "Sporting",
    "sc braga": "Braga",
    
    "club brugge kv": "Club Brugge",
    "club brugge": "Club Brugge",
    "rsc anderlecht": "Anderlecht",
    "kaa gent": "Gent",
    "krc genk": "Genk",
    "royal antwerp fc": "Antwerp",
    "r union saint-gilloise": "Union SG",
    
    "celtic fc": "Celtic",
    "celtic": "Celtic",
    "rangers fc": "Rangers",
    "galatasaray": "Galatasaray",
    "fenerbahce": "Fenerbahce",
    "besiktas": "Besiktas",
    "olympiacos fc": "Olympiakos",
    "paok fc": "PAOK",
    "panathinaikos fc": "Panathinaikos",
    "fc red bull salzburg": "Salzburg",
    "salzburg": "Salzburg",
    "sk sturm graz": "Sturm Graz",
    "sturm graz": "Sturm Graz",
    "fk shakhtar donetsk": "Shakhtar Donetsk",
    "shakhtar donetsk": "Shakhtar Donetsk",
    "shakhtar": "Shakhtar Donetsk",
    "dynamo kyiv": "Dynamo Kyiv",
    "dinamo kiev": "Dynamo Kyiv",
    "fk crvena zvezda": "Crvena Zvezda",
    "crvena zvezda": "Crvena Zvezda",
    "red star": "Crvena Zvezda",
    "gnk dinamo zagreb": "Dinamo Zagreb",
    "dinamo zagreb": "Dinamo Zagreb",
    "ac sparta praha": "Sparta Praha",
    "sparta praha": "Sparta Praha",
    "sk slavia praha": "Slavia Praha",
    "slavia praha": "Slavia Praha",
    "viktoria plzen": "Viktoria Plzen",
    "bsc young boys": "Young Boys",
    "young boys": "Young Boys",
    "fc basel 1893": "Basel",
    "basel": "Basel",
    "fc kobenhavn": "FC Kobenhavn",
    "copenhagen": "FC Kobenhavn",
    "sk slovan bratislava": "Slovan Bratislava",
    "slovan bratislava": "Slovan Bratislava"
}


CANONICAL_TO_CSV = {
    "atletico": "ath madrid",
    "sporting": "sp lisbon",
    "manchester united": "man united",
    "real betis": "betis",
    "bodo/glimt": "bodoe glimt",
    "bayern munich": "bayern munich",
    "psv eindhoven": "psv eindhoven",
    "inter": "inter",
    "juventus": "juventus",
    "lille": "lille",
    "porto": "porto",
    "real madrid": "real madrid",
    "barcelona": "barcelona",
    "villarreal": "villarreal",
    "como": "como",
    "viking": "viking",
    "lask": "lask",
    "lens": "lens",
    "roma": "roma",
    "napoli": "napoli",
    "arsenal": "arsenal",
    "man city": "man city",
    "liverpool": "liverpool",
    "dortmund": "dortmund",
    "leverkusen": "leverkusen",
    "rb leipzig": "rb leipzig",
    "stuttgart": "stuttgart",
    "aston villa": "aston villa",
    "paris sg": "paris sg",
    "monaco": "monaco",
    "feyenoord": "feyenoord",
    "celtic": "celtic",
    "club brugge": "club brugge",
    "bologna": "bologna",
    "girona": "girona",
    "brest": "brest",
    "atalanta": "atalanta",
    "milan": "milan",
    "benfica": "benfica",
    "galatasaray": "galatasaray",
}

CALIBRATED_FALLBACK_ELOS = {
    "shakhtar donetsk": 1690.0,
    "slavia praha": 1680.0,
    "sparta praha": 1650.0,
    "dinamo zagreb": 1620.0,
    "crvena zvezda": 1610.0,
    "aek athens": 1600.0,
    "young boys": 1590.0,
    "slovan bratislava": 1510.0,
    "sabah fc": 1460.0,
}


class ClubEloManager:
    """Manages European Elo ratings with date-aware lookups and UEFA-coef fallback."""

    def __init__(self, elo_csv_path: Optional[Path] = None):
        self.elo_path = elo_csv_path or (settings.RAW_DIR / "EloRatings.csv")
        self.uefa_coefs = self._load_uefa_coefs()
        self.elo_cache: Dict[str, pd.DataFrame] = {}
        self.current_ratings: Dict[str, float] = {}
        self._load_elo_database()

    def _load_uefa_coefs(self) -> Dict[str, float]:
        if settings.COEFFICIENTS_PATH.exists():
            with open(settings.COEFFICIENTS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {k: v["coef"] for k, v in data.items()}
        return {"DEFAULT": 0.35}

    def _load_elo_database(self):
        if not self.elo_path.exists():
            return
        df = pd.read_csv(self.elo_path)
        df["date"] = pd.to_datetime(df["date"])
        raw_groups = {}
        for club, group in df.groupby("club"):
            normalized_club = strip_accents(club.lower()).strip()
            sorted_grp = group.sort_values("date")
            raw_groups[normalized_club] = sorted_grp
            self.elo_cache[normalized_club] = sorted_grp
            self.current_ratings[normalized_club] = float(sorted_grp.iloc[-1]["elo"])

        # Map canonical aliases directly into elo_cache and current_ratings
        for canon_name, csv_name in CANONICAL_TO_CSV.items():
            csv_norm = strip_accents(csv_name.lower()).strip()
            if csv_norm in raw_groups:
                grp = raw_groups[csv_norm]
                self.elo_cache[canon_name] = grp
                self.current_ratings[canon_name] = float(grp.iloc[-1]["elo"])

    def canonical_name(self, raw_name: str) -> str:
        clean = strip_accents(raw_name).lower().strip()
        if clean in TEAM_ALIASES:
            return TEAM_ALIASES[clean]
        # Remove common prefixes/suffixes
        s = clean.replace(" fc", "").replace("fc ", "").replace("cf ", "").replace(" cf", "").strip()
        if s in TEAM_ALIASES:
            return TEAM_ALIASES[s]
        return raw_name.strip()

    def get_base_elo_by_country(self, country: str) -> float:
        coef = self.uefa_coefs.get(country, self.uefa_coefs.get("DEFAULT", 0.35))
        return 1380.0 + 400.0 * coef

    def get_elo(self, team_name: str, match_date: Optional[str] = None, country: Optional[str] = None) -> float:
        c_name = self.canonical_name(team_name)
        norm_key = strip_accents(c_name).lower().strip()

        # 1. Check dynamic Elo cache (historical CSV)
        if norm_key in self.elo_cache:
            history = self.elo_cache[norm_key]
            if match_date is not None:
                dt = pd.to_datetime(match_date)
                past = history[history["date"] <= dt]
                if not past.empty:
                    return float(past.iloc[-1]["elo"])
            return float(history.iloc[-1]["elo"])

        # 2. Check calibrated fallback for unlisted leagues
        if norm_key in CALIBRATED_FALLBACK_ELOS:
            return float(CALIBRATED_FALLBACK_ELOS[norm_key])

        # 3. Check current ratings dictionary
        if norm_key in self.current_ratings:
            return self.current_ratings[norm_key]

        # 4. Fallback to UEFA country coefficient baseline
        if country:
            return self.get_base_elo_by_country(country)

        return 1550.0
