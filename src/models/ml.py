"""Machine Learning model trainers (XGBoost, LightGBM, CatBoost) for UCL 2.0."""
from __future__ import annotations
from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd
from sklearn.utils.class_weight import compute_sample_weight
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier

FEATURE_COLS = [
    "home_elo", "away_elo", "elo_diff",
    "home_uefa_coef", "away_uefa_coef", "coef_diff", "coef_ratio",
    "travel_distance_km", "travel_fatigue",
    "home_club_pedigree", "away_club_pedigree", "pedigree_diff", "pedigree_ratio",
    "elo_prob_h", "elo_prob_d", "elo_prob_a",
    "form_3_h", "form_3_a",
    "form_5_h", "form_5_a",
    "gd_5_h", "gd_5_a",
    "gf_5_h", "gf_5_a",
    "ga_5_h", "ga_5_a",
    "rest_h", "rest_a", "rest_diff",
    "h2h_h_wins", "h2h_a_wins", "h2h_draws", "h2h_total",
    "is_knockout", "is_hostile_venue", "matchday"
]

def prepare_xy(df: pd.DataFrame, use_sample_weight: bool = False) -> Tuple[pd.DataFrame, np.ndarray, Optional[np.ndarray]]:
    clean = df.dropna(subset=["target"]).copy()
    X = clean[FEATURE_COLS].copy()
    y = clean["target"].astype(int).values
    sample_weights = compute_sample_weight(class_weight="balanced", y=y) if use_sample_weight else None
    return X, y, sample_weights

def train_xgb(X_train: pd.DataFrame, y_train: np.ndarray, sample_weights: Optional[np.ndarray] = None) -> xgb.XGBClassifier:
    model = xgb.XGBClassifier(
        n_estimators=180,
        max_depth=4,
        learning_rate=0.035,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="multi:softprob",
        num_class=3,
        random_state=42,
        eval_metric="mlogloss"
    )
    model.fit(X_train, y_train, sample_weight=sample_weights)
    return model

def train_lgb(X_train: pd.DataFrame, y_train: np.ndarray, sample_weights: Optional[np.ndarray] = None) -> lgb.LGBMClassifier:
    model = lgb.LGBMClassifier(
        n_estimators=170,
        max_depth=4,
        learning_rate=0.035,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="multiclass",
        num_class=3,
        random_state=42,
        verbosity=-1
    )
    model.fit(X_train, y_train, sample_weight=sample_weights)
    return model

def train_catboost(X_train: pd.DataFrame, y_train: np.ndarray, sample_weights: Optional[np.ndarray] = None) -> CatBoostClassifier:
    model = CatBoostClassifier(
        iterations=200,
        depth=4,
        learning_rate=0.035,
        loss_function="MultiClass",
        random_seed=42,
        verbose=False
    )
    model.fit(X_train, y_train, sample_weight=sample_weights)
    return model
