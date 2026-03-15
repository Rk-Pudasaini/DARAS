from django.urls import path
from frontend import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('use-model/', views.use_model, name='use_model'),
    path('digital-usage/', views.digital_usage, name='digital_usage'),
    path('risk-category/', views.risk_category, name='risk_category'),
    path('metrics/', views.metrics, name='metrics'),
    path('about/', views.about, name='about'),
]