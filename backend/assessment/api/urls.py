from django.urls import path
from .views import PredictAssessmentView

urlpatterns = [
    path('predict/', PredictAssessmentView.as_view(), name='predict-assessment'),
]
