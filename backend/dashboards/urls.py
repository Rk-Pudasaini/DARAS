from django.urls import path
from .views import admin_dashboard, student_dashboard
from . import views


urlpatterns = [
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('student/', student_dashboard, name='student_dashboard'),

     # Student pages
    path('student/use-model/', views.use_model, name='use_model'),
    path('student/about/', views.about, name='about'),

     # Admin pages
    path('admin/insights/', views.digital_behaviour_insights, name='insights'),
    path('admin/metrics/', views.metrics, name='metrics'),
]


