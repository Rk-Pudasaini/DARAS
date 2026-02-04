from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from assessment.models import DigitalAddictionAssessment
from .serializers import AssessmentSerializer
import joblib
import os

# Load ML model once (replace path with your trained model)
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml', 'digital_addiction_model.pkl')
model = joblib.load(MODEL_PATH)

class PredictAssessmentView(APIView):
    """
    Receives participant form data, saves it, predicts digital addiction risk.
    """

    def post(self, request):
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the participant data first
            assessment = serializer.save()

            # Prepare features for ML model
            features = [
                assessment.study_hours,
                assessment.sleep_hours,
                assessment.social_media_hours,
                assessment.stress_level
            ]

            # Predict risk
            predicted_risk = model.predict([features])[0]

            # Save predicted risk in DB
            assessment.predicted_risk = predicted_risk
            assessment.save()

            # Return response
            return Response({
                "participant_name": assessment.participant_name,
                "predicted_risk": predicted_risk,
                "message": f"Digital addiction risk for {assessment.participant_name} is {predicted_risk}."
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
