import numpy as np
import joblib
import os

# Load model once (important for performance)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'digital_addiction_model.pkl')

model = joblib.load(MODEL_PATH)


def predict_risk(data):
    """
    Predict digital addiction risk level

    Args:
        data (dict): user input features

    Returns:
        dict: prediction result
    """

    try:
        # 1️⃣ Extract features in correct order
        features = np.array([[
            float(data['screen_time']),
            float(data['sleep_hours']),
            float(data['social_media_hours']),
            float(data['gaming_hours'])
        ]])

        # 2️⃣ Predict
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features).max()

        # 3️⃣ Map numeric output to label
        risk_map = {
            0: "Not At Risk",
            1: "Mild Risk",
            2: "Moderate Risk",
            3: "High Risk"
        }

        risk_level = risk_map.get(prediction, "Unknown")

        # 4️⃣ Return clean response
        return {
            "risk_level": risk_level,
            "prediction_score": round(float(probability), 2),
            "status": "success"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

