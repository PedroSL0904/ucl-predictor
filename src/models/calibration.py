"""Temperature scaling for multi-class probability calibration."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional
import numpy as np
from scipy.optimize import minimize_scalar

class TemperatureScaler:
    """Calibrates 3-way 1X2 probabilities using Temperature Scaling."""

    def __init__(self, temperature: float = 1.0):
        self.temperature = float(temperature)

    def fit(self, probs: np.ndarray, y_true: np.ndarray, metric: str = "brier") -> TemperatureScaler:
        """Finds optimal temperature T to minimize validation Brier score or Log Loss."""
        # Convert y_true (0, 1, 2) to one-hot
        y_one_hot = np.zeros((len(y_true), 3))
        for i, val in enumerate(y_true):
            if not np.isnan(val):
                y_one_hot[i, int(val)] = 1.0

        eps = 1e-7
        clipped = np.clip(probs, eps, 1.0 - eps)
        log_probs = np.log(clipped)

        def objective(t: float) -> float:
            scaled_logits = log_probs / max(t, 0.1)
            # Softmax
            exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=1, keepdims=True))
            p_scaled = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

            if metric == "brier":
                return float(np.mean(np.sum((p_scaled - y_one_hot) ** 2, axis=1)))
            else:  # log loss
                p_safe = np.clip(p_scaled, eps, 1.0 - eps)
                return float(-np.mean(np.sum(y_one_hot * np.log(p_safe), axis=1)))

        res = minimize_scalar(objective, bounds=(0.3, 2.5), method="bounded")
        self.temperature = float(res.x)
        return self

    def transform(self, probs: np.ndarray) -> np.ndarray:
        """Scales probabilities with learned temperature."""
        if abs(self.temperature - 1.0) < 1e-4:
            return probs
            
        eps = 1e-7
        clipped = np.clip(probs, eps, 1.0 - eps)
        log_probs = np.log(clipped)
        scaled_logits = log_probs / max(self.temperature, 0.1)
        exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"temperature": self.temperature}, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> TemperatureScaler:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return cls(temperature=data.get("temperature", 1.0))
