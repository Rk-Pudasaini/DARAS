from django.contrib import admin
from .models import DigitalAddictionAssessment


@admin.register(DigitalAddictionAssessment)
class AssessmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "age",
        "gender",
        "predicted_risk",
        "created_at"
    )

    list_filter = ("predicted_risk", "gender")
    search_fields = ("student__username",)
