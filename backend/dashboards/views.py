from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# @login_required
# def student_dashboard(request):
#     if getattr(request.user, 'role', '').lower() == 'student':
#         return render(request, 'dashboards/student.html')
#     else:
#         return redirect('admin_dashboard')  # prevent admins from accessing student page

# @login_required
# def admin_dashboard(request):
#     if getattr(request.user, 'role', '').lower() == 'admin':
#         return render(request, 'dashboards/admin.html')
#     else:
#         return redirect('student_dashboard')  # prevent students from accessing admin page

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request):
    if not request.user.is_staff:
        return render(request, 'dashboards/student.html')
    return redirect('admin_dashboard')

@login_required
def use_model(request):
    return render(request, 'students/use_model.html')

@login_required
def about(request):
    return render(request, 'students/about.html')

@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        return render(request, 'dashboards/admin.html')
    return redirect('student_dashboard')

@login_required
def digital_behaviour_insights(request):
    return render(request, 'admin/insights.html')

@login_required
def metrics(request):
    return render(request, 'admin/metrics.html')









