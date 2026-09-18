"""Automated end-to-end retraining script for UCL Predictor 2.0."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from scripts.01_download_data import *
from scripts.02_build_database import build_database
from src.features.builder import build_features_matrix
from scripts.04_train_models import train_production_pipeline

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
