import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import joblib

sys.stdout.reconfigure(encoding='utf-8')

from config.settings import settings
from src.models.statistical import UCLDixonColes
from src.models.calibration import TemperatureScaler
from src.models.stacking import StackingMetaLearner
from src.models.ml import prepare_xy, train_xgb, train_lgb, train_catboost, FEATURE_COLS

def rps_score(p_pred: np.ndarray, y_true: np.ndarray) -> float:
    p_cum = np.cumsum(p_pred, axis=1)
    y_cum = np.zeros_like(p_cum)
    for i, y in enumerate(y_true):
        y_cum[i, int(y):] = 1.0
    return float(np.mean(np.sum((p_cum - y_cum) ** 2, axis=1) / 2.0))

def brier_score(p_pred: np.ndarray, y_true: np.ndarray) -> float:
    y_one_hot = np.zeros_like(p_pred)
    for i, y in enumerate(y_true):
        y_one_hot[i, int(y)] = 1.0
    return float(np.mean(np.sum((p_pred - y_one_hot) ** 2, axis=1)))

def log_loss_score(p_pred: np.ndarray, y_true: np.ndarray) -> float:
    eps = 1e-7
    p_safe = np.clip(p_pred, eps, 1.0 - eps)
    y_one_hot = np.zeros_like(p_pred)
    for i, y in enumerate(y_true):
        y_one_hot[i, int(y)] = 1.0
    return float(-np.mean(np.sum(y_one_hot * np.log(p_safe), axis=1)))

def train_production_pipeline():
    print("==================================================================")
    print("🚀 TRAINING UCL PREDICTOR 2.0 (STACKING META-LEARNER & CALIBRATION)")
    print("==================================================================")
    df = pd.read_parquet(settings.FEATURES_PATH)
    
    train_mask = ~df["season"].isin(["2024-25", "2025-26"])
    test_mask = df["season"].isin(["2024-25", "2025-26"])

    df_train = df[train_mask].copy()
    df_test = df[test_mask].copy()
    print(f"Training matches: {len(df_train)} (2011 to 2024)")
    print(f"Validation matches: {len(df_test)} (2024-25 & 2025-26 Swiss Format)")

    # 1. Fit Dixon-Coles on Train
    print("\n1. Training Dixon-Coles model...")
    dc_model = UCLDixonColes()
    dc_model.fit(df_train)
    settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(dc_model, settings.MODELS_DIR / "dixon_coles.joblib")

    X_train, y_train, w_train = prepare_xy(df_train)
    X_test, y_test, _ = prepare_xy(df_test)

    # 2. Generate 5-Fold Out-Of-Fold (OOF) Level-1 Predictions for Stacking
    print("\n2. Generating 5-Fold Out-Of-Fold (OOF) Level-1 Predictions...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    oof_preds = np.zeros((len(df_train), 12))  # 3 cols each for DC, XGB, LGB, Cat

    for fold, (tr_idx, val_idx) in enumerate(kf.split(X_train, y_train), 1):
        df_tr_f = df_train.iloc[tr_idx]
        df_val_f = df_train.iloc[val_idx]
        X_tr_f, y_tr_f, w_tr_f = X_train.iloc[tr_idx], y_train[tr_idx], w_train[tr_idx] if w_train is not None else None
        X_val_f = X_train.iloc[val_idx]

        # Fold-specific Dixon-Coles for true OOF
        dc_fold = UCLDixonColes()
        dc_fold.fit(df_tr_f)
        p_dc_fold_list = []
        for _, row in df_val_f.iterrows():
            p_dc_f, _, _ = dc_fold.predict_proba(
                home_team=row["home_team_name"],
                away_team=row["away_team_name"],
                home_elo=row["home_elo"],
                away_elo=row["away_elo"],
                is_hostile=(row["is_hostile_venue"] == 1),
                coef_ratio=row["coef_ratio"],
                travel_fatigue=row.get("travel_fatigue", 0.0)
            )
            p_dc_fold_list.append(p_dc_f)
        oof_preds[val_idx, 0:3] = np.array(p_dc_fold_list)

        m_xgb = train_xgb(X_tr_f, y_tr_f, w_tr_f)
        m_lgb = train_lgb(X_tr_f, y_tr_f, w_tr_f)
        m_cat = train_catboost(X_tr_f, y_tr_f, w_tr_f)

        oof_preds[val_idx, 3:6] = m_xgb.predict_proba(X_val_f)
        oof_preds[val_idx, 6:9] = m_lgb.predict_proba(X_val_f)
        oof_preds[val_idx, 9:12] = m_cat.predict_proba(X_val_f)
        print(f"   Fold {fold}/5 completed.")

    # 3. Train Level-2 Stacking Meta-Learner on OOF
    print("\n3. Training Level-2 Stacking Meta-Learner...")
    stacking_meta = StackingMetaLearner(C=0.4).fit(oof_preds, y_train)
    stacking_meta.save(settings.MODELS_DIR / "stacking_meta.joblib")
    print("   Stacking Meta-Learner trained and saved.")

    # 4. Train final Level-1 models on full training set
    print("\n4. Fitting final Level-1 models on full training set...")
    xgb_final = train_xgb(X_train, y_train, w_train)
    lgb_final = train_lgb(X_train, y_train, w_train)
    cat_final = train_catboost(X_train, y_train, w_train)

    joblib.dump(xgb_final, settings.MODELS_DIR / "xgb_tuned.joblib")
    joblib.dump(lgb_final, settings.MODELS_DIR / "lgbm_tuned.joblib")
    joblib.dump(cat_final, settings.MODELS_DIR / "catboost_tuned.joblib")
    print("   All Level-1 models saved to models/.")

    # 5. Calibrate via Temperature Scaling on OOF predictions (zero test leakage)
    print("\n5. Calibrating probabilities via Temperature Scaling on OOF predictions...")
    oof_stacked = stacking_meta.predict_proba(oof_preds)
    scaler = TemperatureScaler().fit(oof_stacked, y_train, metric="brier")
    scaler.save(settings.MODELS_DIR / "temperature_scaler.json")
    print(f"   Optimal Calibration Temperature T = {scaler.temperature:.3f}")

    # 6. Evaluate on Unseen Validation Test Set (Swiss Stage 2024-2026)
    p_dc_test_list = []
    for _, row in df_test.iterrows():
        p_dc, _, _ = dc_model.predict_proba(
            home_team=row["home_team_name"],
            away_team=row["away_team_name"],
            home_elo=row["home_elo"],
            away_elo=row["away_elo"],
            is_hostile=(row["is_hostile_venue"] == 1),
            coef_ratio=row["coef_ratio"],
            travel_fatigue=row.get("travel_fatigue", 0.0)
        )
        p_dc_test_list.append(p_dc)
    p_dc_test = np.array(p_dc_test_list)

    p_xgb_test = xgb_final.predict_proba(X_test)
    p_lgb_test = lgb_final.predict_proba(X_test)
    p_cat_test = cat_final.predict_proba(X_test)

    # Combine into meta-matrix for test set
    meta_test = np.hstack([p_dc_test, p_xgb_test, p_lgb_test, p_cat_test])
    p_stacked = stacking_meta.predict_proba(meta_test)
    p_final = scaler.transform(p_stacked)

    # 7. Metrics calculation
    brier_ens = brier_score(p_final, y_test)
    rps_ens = rps_score(p_final, y_test)
    ll_ens = log_loss_score(p_final, y_test)
    preds = np.argmax(p_final, axis=1)
    acc_sign = float(np.mean(preds == y_test)) * 100.0

    dc_hits = 0
    for i, y in enumerate(y_test):
        ph, pd_, pa = p_final[i]
        if ph >= pa:
            if y in [0, 1]:
                dc_hits += 1
        else:
            if y in [1, 2]:
                dc_hits += 1
    dc_accuracy = (dc_hits / len(y_test)) * 100.0

    always_home_acc = float(np.mean(y_test == 0)) * 100.0

    print("\n" + "="*65)
    print("🏆 UCL PREDICTOR 2.0 OUT-OF-SAMPLE VALIDATION METRICS 🏆")
    print("="*65)
    print(f"Total Matches Evaluated:         {len(y_test)} (Formato Suizo)")
    print(f"Sign Accuracy (Acierto de Signo): {acc_sign:.2f}%  (Baseline Always-Home: {always_home_acc:.1f}%)")
    print(f"Double Chance Accuracy (1X/X2):   {dc_accuracy:.2f}%")
    print(f"Brier Score 1X2:                 {brier_ens:.4f}  (Uniform baseline: 0.6667)")
    print(f"Ranked Probability Score (RPS):  {rps_ens:.4f}")
    print(f"Log Loss:                        {ll_ens:.4f}")
    print(f"Calibrated Temperature T:        {scaler.temperature:.3f}")
    print("="*65)

if __name__ == "__main__":
    train_production_pipeline()
