"""Stacking Meta-Learner with Out-Of-Fold (OOF) cross-validation."""
from __future__ import annotations
from pathlib import Path
from typing import Tuple, List, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

class StackingMetaLearner:
    """Level-2 Meta-Learner combining Level-1 models (DC, XGB, LGBM, CatBoost)."""

    def __init__(self, C: float = 0.5):
        self.meta_model = LogisticRegression(
            C=C,
            max_iter=500,
            solver="lbfgs",
            random_state=42
        )

    def fit(self, meta_features: np.ndarray, y_true: np.ndarray) -> StackingMetaLearner:
        """Fits Level-2 meta-learner on Out-Of-Fold predictions."""
        self.meta_model.fit(meta_features, y_true)
        return self

    def predict_proba(self, meta_features: np.ndarray) -> np.ndarray:
        return self.meta_model.predict_proba(meta_features)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.meta_model, path)

    @classmethod
    def load(cls, path: Path) -> StackingMetaLearner:
        instance = cls()
        instance.meta_model = joblib.load(path)
        return instance
