from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import AssessmentForm
from ml.predictor import predict_risk

from django.shortcuts import render, get_object_or_404
from assessment.models import DigitalAddictionAssessment


@login_required
def take_assessment(request):

    # Optional: prevent resubmission
    if request.user.digitaladdictionassessment_set.exists():
        return redirect("assessment_success")

    if request.method == "POST":

        form = AssessmentForm(request.POST)

        if form.is_valid():

            assessment = form.save(commit=False)
            assessment.student = request.user

            # 🔥 ML Prediction
            assessment.predicted_risk = predict_risk(assessment)

            assessment.save()

            return redirect("assessment_success")

    else:
        form = AssessmentForm()

    return render(
        request,
        "students/use_model.html",   # ✅ IMPORTANT
        {"form": form}
    )


@login_required
def assessment_success(request):
    return render(
        request,
        "students/assessment_success.html"
    )


@login_required
def assessment_result(request, assessment_id):
    assessment = get_object_or_404(DigitalAddictionAssessment, id=assessment_id)
    return render(request, 'assessment/result.html', {'assessment': assessment})

