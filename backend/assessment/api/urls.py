from django.urls import path
from assessment.api.views import PredictAssessmentView, DigitalAddictionAssessmentDetailAPI, AssessmentHistoryAPIView

urlpatterns = [
    path("predict/", PredictAssessmentView.as_view(), name="predict-assessment"),
    path("<int:pk>/", DigitalAddictionAssessmentDetailAPI.as_view(), name="assessment-detail"),
    path("api/assessments/history/", AssessmentHistoryAPIView.as_view(), name="assessment-history-api"),
]
