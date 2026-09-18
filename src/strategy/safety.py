"""Safety tier classification and confidence scoring."""
from typing import Dict
from src.domain import SafetyTier, ConfidenceLevel

def compute_safety_tier(probs: Dict[str, float]) -> SafetyTier:
    """Classifies risk level to differentiate direct singles vs double chance."""
    ph = probs.get("H", 0.33)
    pd_ = probs.get("D", 0.34)
    pa = probs.get("A", 0.33)
    max_p = max(ph, pd_, pa)
    diff_ha = abs(ph - pa)

    if max_p >= 0.60:
        return SafetyTier.BANQUERO
    elif diff_ha <= 0.08:
        return SafetyTier.PARIDAD
    elif pd_ >= 0.22:
        return SafetyTier.FAVORITO_RIESGO_EMPATE
    return SafetyTier.FIRME


def compute_confidence(probs: Dict[str, float]) -> ConfidenceLevel:
    """Calculates confidence based on maximum probability."""
    max_p = max(probs.values())
    if max_p >= 0.58:
        return ConfidenceLevel.HIGH
    elif max_p >= 0.45:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.LOW
