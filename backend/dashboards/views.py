from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from assessment.models import DigitalAddictionAssessment
from assessment.views import create_late_night_pie_chart, create_night_phone_by_age_percentage_bar_chart, create_platform_bar_chart, generate_das_by_age_chart_interactive
from ml.preprocessing import preprocess_assessment 
import numpy as np


# ================================
# STUDENT DASHBOARD
# ================================
@login_required
def student_dashboard(request):
    # If admin accidentally lands here → redirect
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')

    return render(request, 'dashboards/student.html')


# ================================
# USE MODEL (ASSESSMENT FORM)
# ================================
@login_required
def use_model(request):
    # Only students should access assessment form
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')

    return render(request, 'students/use_model.html')


# ================================
# ABOUT PAGE (STUDENT)
# ================================
@login_required
def about(request):
    return render(request, 'students/about.html')


# ================================
# ADMIN DASHBOARD
# ================================
@login_required
def admin_dashboard(request):
    # Block non-admin users
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('student_dashboard')

    return render(request, 'dashboards/admin.html')


# ================================
# ADMIN – DIGITAL BEHAVIOUR INSIGHTS
# ================================
@login_required
def digital_behaviour_insights(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('student_dashboard')

    # Fetch all assessments
    assessments = DigitalAddictionAssessment.objects.all()
    total_assessments = assessments.count()

    screen_weekdays_list = []
    screen_weekends_list = []
    gaming_time_list = []
    social_media_list = []

    for assessment in assessments:
        numeric_features, _ = preprocess_assessment(assessment, fit=False)
        screen_weekdays_list.append(numeric_features.get("screen_time_weekdays", 0))
        screen_weekends_list.append(numeric_features.get("screen_time_weekends", 0))
        gaming_time_list.append(numeric_features.get("gaming_time", 0))           # in hours
        social_media_list.append(numeric_features.get("social_media_time", 0))     # in hours

    # Compute averages safely
    avg_screen_weekdays = round(np.mean(screen_weekdays_list), 1) if screen_weekdays_list else 0
    avg_screen_weekends = round(np.mean(screen_weekends_list), 1) if screen_weekends_list else 0
    avg_gaming_time_hours = round(np.mean(gaming_time_list), 2) if gaming_time_list else 0
    avg_social_media_time_hours = round(np.mean(social_media_list), 2) if social_media_list else 0

    # Convert hours to minutes for metric cards
    avg_gaming_time_mins = round(avg_gaming_time_hours * 60, 1)
    avg_social_media_time_mins = round(avg_social_media_time_hours * 60, 1)

    context = {
        "total_assessments": total_assessments,
        "avg_screen_weekdays": avg_screen_weekdays,
        "avg_screen_weekends": avg_screen_weekends,
        "avg_gaming_time": avg_gaming_time_mins,        # now in minutes
        "avg_social_media_time": avg_social_media_time_mins,  # now in minutes

        # Interactive chart div for DAS by age
        "das_chart_div": generate_das_by_age_chart_interactive(assessments),

        # Interactive pie chart for late night phone usage
        "pie_div": create_late_night_pie_chart(assessments),

        # Interactive bar chart for late night phone usage
        "bar_div": create_night_phone_by_age_percentage_bar_chart(assessments),

        # Bar chart for platform usage
        "platform_bar_div": create_platform_bar_chart(assessments),
    }

    return render(request, 'admin/insights.html', context)


# ================================
# ADMIN – MODEL METRICS
# ================================
@login_required
def metrics(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('student_dashboard')

    # Placeholder for ML metrics (expand later)
    context = {
        'accuracy': '92%',
        'precision': '90%',
        'recall': '89%',
        'f1_score': '89.5%',
        'model_version': 'v1.0'
    }

    return render(request, 'admin/metrics.html', context)


# ================================
# STUDENT HISTORY
# ================================
@login_required
def assessment_history_view(request):
    assessments = DigitalAddictionAssessment.objects.filter(
        student=request.user
    ).order_by("-created_at")

    return render(
        request,
        "students/history.html",
        {"assessments": assessments}
    )

@login_required
def assessment_detail_view(request, id):
    assessment = get_object_or_404(
        DigitalAddictionAssessment,
        id=id,
        student=request.user   # IMPORTANT: ownership check
    )

    # Compute DAS weighted average
    da_values = [assessment.da1, assessment.da2, assessment.da3, assessment.da4,
                 assessment.da5, assessment.da6, assessment.da7, assessment.da8]
    das_score = sum(da_values) / len(da_values)  # average
    das_score_normalized = (das_score / 5) * 100  # assuming DA1–DA8 are 0–5 Likert scale

    return render(request, 'students/details.html', {
        'assessment': assessment,
        'das_score': round(das_score_normalized, 2),
    })











