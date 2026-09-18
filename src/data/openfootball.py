import re
from pathlib import Path
from typing import List, Dict, Any

STAGE_PATTERN = re.compile(r"^[\u25aa\u2022\*\-]?\s*([A-Za-z0-9\s,–\-]+)$")
DATE_PATTERN_FULL = re.compile(r"^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Za-z]+)\s+(\d{1,2})\s+(\d{4})")
DATE_PATTERN_SHORT = re.compile(r"^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Za-z]+)\s+(\d{1,2})")

MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

def parse_season_file(filepath: Path, season_name: str) -> List[Dict[str, Any]]:
    matches = []
    lines = filepath.read_text(encoding="utf-8", errors="ignore").splitlines()
    
    current_stage = "Unknown"
    current_matchday = 0
    current_date = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("="):
            continue
            
        if line.startswith("▪") or line.startswith("\u25aa"):
            current_stage = line.lstrip("▪\u25aa ").strip()
            # Extract matchday if present (e.g. "League, Matchday 1" or "Group A" or "Matchday 2")
            m_md = re.search(r"Matchday\s+(\d+)", current_stage, re.IGNORECASE)
            if m_md:
                current_matchday = int(m_md.group(1))
            elif "Playoff" in current_stage:
                current_matchday = 9
            elif "Round of 16" in current_stage:
                current_matchday = 10
            elif "Quarter" in current_stage:
                current_matchday = 11
            elif "Semi" in current_stage:
                current_matchday = 12
            elif "Final" in current_stage:
                current_matchday = 13
            continue
            
        date_full = DATE_PATTERN_FULL.match(stripped)
        if date_full:
            m_name, day, year = date_full.group(1), int(date_full.group(2)), int(date_full.group(3))
            current_date = f"{year:04d}-{MONTH_MAP[m_name]:02d}-{day:02d}"
            continue
            
        date_short = DATE_PATTERN_SHORT.match(stripped)
        if date_short:
            m_name, day = date_short.group(1), int(date_short.group(2))
            start_year = int(season_name.split("-")[0])
            m_idx = MONTH_MAP[m_name]
            actual_year = start_year + 1 if m_idx <= 7 else start_year
            current_date = f"{actual_year:04d}-{m_idx:02d}-{day:02d}"
            continue
            
        if " v " in line:
            line_clean = re.sub(r"^\s*\d{1,2}:\d{2}\s+", "", line).strip()
            parts = line_clean.split(" v ")
            if len(parts) == 2:
                home_part = parts[0].strip()
                away_and_score = parts[1].strip()
                
                home_country = ""
                hc_m = re.search(r"\(([A-Z]{3})\)$", home_part)
                if hc_m:
                    home_country = hc_m.group(1)
                    home_team = home_part[:hc_m.start()].strip()
                else:
                    home_team = home_part
                    
                score_str = away_and_score
                if "pen." in score_str:
                    pen_idx = score_str.find("pen.")
                    after_pen = score_str[pen_idx + 4:].strip()
                    match_score_m = re.search(r"(\d+)-(\d+)", after_pen)
                    if match_score_m:
                        home_goals = int(match_score_m.group(1))
                        away_goals = int(match_score_m.group(2))
                        before_pen = score_str[:pen_idx].strip()
                        shootout_m = re.search(r"\d+-\d+$", before_pen)
                        away_raw = before_pen[:shootout_m.start()].strip() if shootout_m else before_pen
                    else:
                        home_goals, away_goals = None, None
                        away_raw = away_and_score
                else:
                    score_m = re.search(r"(\d+)-(\d+)", score_str)
                    if score_m:
                        home_goals = int(score_m.group(1))
                        away_goals = int(score_m.group(2))
                        away_raw = score_str[:score_m.start()].strip()
                    else:
                        home_goals = None
                        away_goals = None
                        away_raw = score_str.strip()
                    
                away_country = ""
                ac_m = re.search(r"\(([A-Z]{3})\)$", away_raw)
                if ac_m:
                    away_country = ac_m.group(1)
                    away_team = away_raw[:ac_m.start()].strip()
                else:
                    away_team = away_raw
                    
                if home_team and away_team:
                    status = "FINISHED" if home_goals is not None else "SCHEDULED"
                    matches.append({
                        "season": season_name,
                        "stage": current_stage,
                        "matchday": current_matchday,
                        "date": current_date or f"{season_name[:4]}-09-15",
                        "home_team": home_team,
                        "home_country": home_country,
                        "away_team": away_team,
                        "away_country": away_country,
                        "home_goals": home_goals,
                        "away_goals": away_goals,
                        "status": status,
                    })
    return matches

def parse_all_seasons(raw_dir: Path) -> List[Dict[str, Any]]:
    all_matches = []
    openfootball_dir = raw_dir / "openfootball"
    for p in sorted(openfootball_dir.glob("*.txt")):
        season_name = p.stem
        m = parse_season_file(p, season_name)
        all_matches.extend(m)
    return all_matches
