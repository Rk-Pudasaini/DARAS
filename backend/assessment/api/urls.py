from django.urls import path
from assessment.api.views import PredictAssessmentView, DigitalAddictionAssessmentDetailAPI

urlpatterns = [
    path("predict/", PredictAssessmentView.as_view(), name="predict-assessment"),
    path("<int:pk>/", DigitalAddictionAssessmentDetailAPI.as_view(), name="assessment-detail"),
]
