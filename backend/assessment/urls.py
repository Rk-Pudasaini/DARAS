from django.urls import path, include
from . import views
from .views import take_assessment, assessment_result   
from .api.views import PredictAssessmentView

urlpatterns = [
    path('take/', take_assessment, name='take_assessment'),

    path('use-model/', views.use_model, name='use-model'),  # Form page
    path('result/<int:assessment_id>/', views.assessment_result, name='assessment-result'),
    path('api/predict/', PredictAssessmentView.as_view(), name='predict-assessment'),
]
