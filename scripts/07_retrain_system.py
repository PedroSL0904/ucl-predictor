"""Automated end-to-end retraining script for UCL Predictor 2.0."""
import sys
import importlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

sys.stdout.reconfigure(encoding='utf-8')

build_db_mod = importlib.import_module("scripts.02_build_database")
build_database = build_db_mod.build_database

from src.features.builder import build_features_matrix

train_mod = importlib.import_module("scripts.04_train_models")
train_production_pipeline = train_mod.train_production_pipeline

def retrain_all():
    print("=======================================================")
    print("🔄 INITIATING FULL RE-TRAIN OF UCL PREDICTOR 2.0 🔄")
    print("=======================================================")
    
    # 1. Rebuild database
    print("\nStep 1: Refreshing database records...")
    build_database()

    # 2. Rebuild features
    print("\nStep 2: Rebuilding causal features matrix 2.0...")
    build_features_matrix()

    # 3. Re-train models with Stacking
    print("\nStep 3: Training models, Stacking meta-learner and calibrating...")
    train_production_pipeline()

    print("\n=======================================================")
    print("✅ RE-TRAINING COMPLETED SUCCESSFULLY!")
    print("=======================================================")

if __name__ == "__main__":
    retrain_all()
