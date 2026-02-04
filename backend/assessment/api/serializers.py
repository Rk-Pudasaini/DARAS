from rest_framework import serializers
from assessment.models import DigitalAddictionAssessment


class AssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DigitalAddictionAssessment
        exclude = [
            "student",
            "predicted_risk",
            "created_at"
        ]
