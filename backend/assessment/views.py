from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from assessment.models import DigitalAddictionAssessment


@login_required
def assessment_result_page(request, pk):
    assessment = get_object_or_404(
        DigitalAddictionAssessment,
        pk=pk,
        student=request.user
    )

    return render(
        request,
        "students/assessment_result.html",
        {"assessment": assessment}
    )


