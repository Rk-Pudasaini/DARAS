from django import forms
from .models import DigitalAddictionAssessment


class AssessmentForm(forms.ModelForm):

    class Meta:
        model = DigitalAddictionAssessment
        exclude = ["student", "predicted_risk", "created_at"]

        widgets = {
            "platforms": forms.CheckboxSelectMultiple(
                choices=[
                    ("YouTube", "YouTube"),
                    ("TikTok", "TikTok"),
                    ("Instagram", "Instagram"),
                    ("Facebook", "Facebook"),
                    ("WhatsApp", "WhatsApp"),
                    ("X", "X"),
                    ("Snapchat", "Snapchat"),
                    ("Gaming", "Gaming"),
                ]
            )
        }
