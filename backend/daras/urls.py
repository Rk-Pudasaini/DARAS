from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from assessment.views import assessment_result_page

def root_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('dashboards/', include('dashboards.urls')),
    
    # Assessment HTML pages
    path('assessment/', include('assessment.urls')),

    # API routes
    path('api/assessment/', include('assessment.api.urls')),

    # Result page
    path('students/assessment_result/<int:pk>/', assessment_result_page, name='assessment-result-page'),
]

