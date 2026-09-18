"""De-vigorish methods for margin removal from bookmaker odds."""
from typing import Dict, Tuple
import numpy as np

def devig_multiplicative(odds_dict: Dict[str, float]) -> Dict[str, float]:
    """Simple proportional de-vigorish (normalizing inverse odds to 1.0)."""
    inv_probs = {k: 1.0 / v for k, v in odds_dict.items() if v > 1.0}
    total_margin = sum(inv_probs.values())
    if total_margin <= 0:
        return {}
    return {k: inv / total_margin for k, inv in inv_probs.items()}


def devig_shin(odds_dict: Dict[str, float], max_iter: int = 50) -> Dict[str, float]:
    """Shin (1993) model: accounts for insider trading / asymmetric information bias (longshot bias)."""
    inv_probs = [1.0 / odds_dict[k] for k in sorted(odds_dict.keys())]
    sum_inv = sum(inv_probs)
    if abs(sum_inv - 1.0) < 1e-4:
        return {k: 1.0 / odds_dict[k] for k in sorted(odds_dict.keys())}

    # Bisection search for Shin's z parameter
    z_low = 0.0
    z_high = sum_inv - 1.0
    z = (z_low + z_high) / 2.0

    for _ in range(max_iter):
        p_list = []
        for inv_p in inv_probs:
            # Shin formula for probability p_i given z and odds beta_i
            term = np.sqrt(z**2 + 4.0 * (1.0 - z) * (inv_p**2) / sum_inv) - z
            denom = 2.0 * (1.0 - z)
            p_list.append(max(0.0, term / max(denom, 1e-9)))
        
        sum_p = sum(p_list)
        if abs(sum_p - 1.0) < 1e-5:
            break
        elif sum_p > 1.0:
            z_low = z
        else:
            z_high = z
        z = (z_low + z_high) / 2.0

    # Normalize final probabilities
    total_p = sum(p_list)
    keys = sorted(odds_dict.keys())
    return {keys[i]: float(p_list[i] / total_p) for i in range(len(keys))}
