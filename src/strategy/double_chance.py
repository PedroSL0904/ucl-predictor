"""Mathematical Double Chance selection for UEFA Champions League."""
from typing import Dict, Tuple

def compute_double_chance(probs: Dict[str, float]) -> Tuple[str, float]:
    """Calculates optimal Double Chance coverage.

    - Home favorite (p_H >= p_A): '1X' with coverage p_H + p_D.
    - Away favorite (p_A > p_H): 'X2' with coverage p_D + p_A.
    - Close match with low draw risk (p_D < 0.17): '12' with coverage p_H + p_A.
    """
    ph = probs.get("H", 0.33)
    pd_ = probs.get("D", 0.34)
    pa = probs.get("A", 0.33)

    if pd_ < 0.17 and abs(ph - pa) < 0.08:
        return "12", ph + pa
    elif ph >= pa:
        return "1X", ph + pd_
    else:
        return "X2", pd_ + pa
