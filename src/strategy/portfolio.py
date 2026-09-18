"""Multi-ticket quiniela and betting portfolio optimization."""
from typing import List, Dict, Any
from src.strategy.safety import compute_safety_tier
from src.strategy.double_chance import compute_double_chance

def generate_ucl_portfolio(match_predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generates a 3-ticket complementary portfolio:
    1. Base Ticket (Solid Favorites & Math Projections)
    2. Draws Ticket (Covers Tactical Draws in Parity matches)
    3. Surprises Ticket (Underdogs with Value / High upset potential)
    """
    base_picks = []
    draw_picks = []
    surprise_picks = []

    for pred in match_predictions:
        p = pred["probs"]
        ph, pd_, pa = p.get("H", 0.33), p.get("D", 0.34), p.get("A", 0.33)
        tier = compute_safety_tier(p)
        dc_tag, dc_prob = compute_double_chance(p)

        # 1. Base Pick
        if tier == "Banquero Seguro":
            base_pick = "H" if ph >= pa else "A"
        elif tier == "Paridad (Alto Riesgo / Empate)":
            base_pick = "D" if pd_ >= 0.25 else ("H" if ph >= pa else "A")
        elif tier == "Favorito con Riesgo de Empate":
            # For base ticket, take the favorite, but flag for double
            base_pick = "H" if ph >= pa else "A"
        else:
            base_pick = max(p, key=p.get)
        base_picks.append(base_pick)

        # 2. Draw Ticket: Prioritize D in any parity or high draw match
        if tier in ["Paridad (Alto Riesgo / Empate)", "Favorito con Riesgo de Empate"] or pd_ >= 0.23:
            draw_pick = "D"
        else:
            draw_pick = base_pick
        draw_picks.append(draw_pick)

        # 3. Surprise Ticket: Underdog pick if favorite is vulnerable
        if tier == "Banquero Seguro":
            surprise_pick = base_pick  # Keep solid banker
        else:
            # Pick the other side or underdog
            if ph >= pa:
                surprise_pick = "A" if pa > 0.18 else "D"
            else:
                surprise_pick = "H" if ph > 0.18 else "D"
        surprise_picks.append(surprise_pick)

    return {
        "ticket_base": base_picks,
        "ticket_draws": draw_picks,
        "ticket_surprises": surprise_picks,
        "matches": [f"{m['home_team']} vs {m['away_team']}" for m in match_predictions]
    }
