



import os
import joblib
import numpy as np
from pathlib import Path

from django.conf import settings
from ml.preprocessing import preprocess_assessment

# Load pipeline ONCE (VERY IMPORTANT)
# --------------------------------------
MODEL_PATH = os.path.join(settings.BASE_DIR, "ml", "logistic_regression.pkl")


if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("ML pipeline not found.")

pipeline = joblib.load(MODEL_PATH)




# -------------------------------------------------
# Core Prediction Function
# -------------------------------------------------

# -------------------------------------------------
# Core Prediction Function
# -------------------------------------------------
def predict_risk(instance, df=None):
    """
    Returns ONLY the predicted class.
    
    Args:
        instance : DigitalAddictionAssessment model instance
        df       : preprocessed DataFrame (optional)
    """
    from ml.preprocessing import preprocess_assessment

    # Preprocess if not provided
    if df is None:
        df, _ = preprocess_assessment(instance)

    # Prevent label leakage
    if "y" in df.columns:
        df = df.drop(columns=["y"])

    # Predict class
    pred_class = pipeline.predict(df)[0]

    risk_map = {
        0: "Not at Risk",
        1: "Mild",
        2: "Moderate",
        3: "Severe"
    }

    return risk_map.get(int(pred_class), "Unknown")


# --------------------------------------------------
# Prediction + Confidence
# --------------------------------------------------
def predict_risk_with_confidence(instance, df=None):
    """
    Returns predicted risk label and confidence score.
    
    Args:
        instance : DigitalAddictionAssessment model instance
        df       : preprocessed DataFrame (optional)
        
    Returns:
        (risk_label: str, confidence_score: float | None)
    """
    from ml.preprocessing import preprocess_assessment

    # Use provided DataFrame or preprocess
    if df is None:
        df, _ = preprocess_assessment(instance)
    
    # Drop label column if present
    if "y" in df.columns:
        df = df.drop(columns=["y"])

    # Ensure feature order matches the trained model
    if hasattr(pipeline, "feature_names_in_"):
        df = df.reindex(columns=pipeline.feature_names_in_, fill_value=0)

    # Predict
    pred_class = pipeline.predict(df)[0]

    # Map to risk label
    risk_map = {
        0: "Not at Risk",
        1: "Mild",
        2: "Moderate",
        3: "Severe"
    }
    risk_label = risk_map.get(int(pred_class), "Unknown")

    # Get confidence score if available
    if hasattr(pipeline, "predict_proba"):
        probability = pipeline.predict_proba(df).max()
        probability = round(float(probability), 3)
    else:
        probability = None

    return risk_label, probability

