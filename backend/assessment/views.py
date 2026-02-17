from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from assessment.models import DigitalAddictionAssessment

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from assessment.models import DigitalAddictionAssessment
from ml.preprocessing import preprocess_assessment# your preprocessing function
import numpy as np
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from assessment.models import DigitalAddictionAssessment
from ml.preprocessing import preprocess_assessment
import numpy as np
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from assessment.models import DigitalAddictionAssessment
from ml.preprocessing import preprocess_assessment
import numpy as np

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



@login_required
def insights_view(request):
    assessments = DigitalAddictionAssessment.objects.all()
    total_assessments = assessments.count()

    screen_weekdays_list = []
    screen_weekends_list = []
    gaming_time_list = []
    social_media_list = []

    for assessment in assessments:
        # Preprocess assessment; returns (numeric_features, encoders)
        numeric_features, _ = preprocess_assessment(assessment, fit=False)

        # Access numeric values by column name
        screen_weekdays_list.append(numeric_features["screen_time_weekdays"])
        screen_weekends_list.append(numeric_features["screen_time_weekends"])
        gaming_time_list.append(numeric_features.get("gaming_time", 0))
        social_media_list.append(numeric_features.get("social_media_time", 0))

    # Compute averages safely
    avg_screen_weekdays = round(np.mean(screen_weekdays_list), 1) if screen_weekdays_list else 0
    avg_screen_weekends = round(np.mean(screen_weekends_list), 1) if screen_weekends_list else 0
    avg_gaming_time = round(np.mean(gaming_time_list), 0) if gaming_time_list else 0
    avg_social_media_time = round(np.mean(social_media_list), 0) if social_media_list else 0

    context = {
        "total_assessments": total_assessments,
        "avg_screen_weekdays": avg_screen_weekdays,
        "avg_screen_weekends": avg_screen_weekends,
        "avg_gaming_time": avg_gaming_time,
        "avg_social_media_time": avg_social_media_time,
    }

    return render(request, "admin/insights.html", context)


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.conf import settings

# import os
# import numpy as np
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt

# from .models import DigitalAddictionAssessment
# from ml.preprocessing import preprocess_assessment


# @login_required
# def insights_view(request):
#     assessments = DigitalAddictionAssessment.objects.all()
#     total_assessments = assessments.count()

#     #print(assessments) # debugging line to check if assessments are being retrieved correctly

#     screen_weekdays_list = []
#     screen_weekends_list = []
#     gaming_time_list = []
#     social_media_list = []

#     # -------- Age group buckets --------
#     age_group_scores = {
#         "10-14": [],
#         "15-18": [],
#         "19-22": [],
#         "23-26": [],
#         "27+": [],
#     }

#     for assessment in assessments:
#         numeric_features, _ = preprocess_assessment(assessment, fit=False)

#         screen_weekdays_list.append(numeric_features.get("screen_time_weekdays", 0))
#         screen_weekends_list.append(numeric_features.get("screen_time_weekends", 0))
#         gaming_time_list.append(numeric_features.get("gaming_time", 0))
#         social_media_list.append(numeric_features.get("social_media_time", 0))

#         # -------- Age-grouped addiction score --------
#         age = numeric_features.get("age", None)
#     addiction_score = numeric_features.get("digital_addiction_score", 0)

#     # Convert pandas Series → scalar
#     if hasattr(age, "item"):
#         age = age.item()

#     if hasattr(addiction_score, "item"):
#         addiction_score = addiction_score.item()

#     if age is not None:
#         if 10 <= age <= 14:
#             age_group_scores["10-14"].append(addiction_score)
#         elif 15 <= age <= 18:
#             age_group_scores["15-18"].append(addiction_score)
#         elif 19 <= age <= 22:
#             age_group_scores["19-22"].append(addiction_score)
#         elif 23 <= age <= 26:
#             age_group_scores["23-26"].append(addiction_score)
#         else:
#             age_group_scores["27+"].append(addiction_score)

#     # -------- Compute averages safely --------
#     avg_screen_weekdays = round(np.mean(screen_weekdays_list), 1) if screen_weekdays_list else 0
#     avg_screen_weekends = round(np.mean(screen_weekends_list), 1) if screen_weekends_list else 0
#     avg_gaming_time = round(np.mean(gaming_time_list), 0) if gaming_time_list else 0
#     avg_social_media_time = round(np.mean(social_media_list), 0) if social_media_list else 0

#     age_labels = []
#     avg_scores = []

#     for label, values in age_group_scores.items():
#         age_labels.append(label)
#         avg_scores.append(round(np.mean(values), 1) if values else 0)

#     # -------- Generate Bar Chart (Python) --------
#     # -------- Generate Bar Chart (FORCE SAFE) --------
#     chart_dir = os.path.join(settings.MEDIA_ROOT, "charts")
#     os.makedirs(chart_dir, exist_ok=True)

#     chart_filename = "avg_addiction_by_age.png"
#     chart_path = os.path.join(chart_dir, chart_filename)

#     plt.clf()
#     plt.figure(figsize=(7, 4))

#     bars = plt.bar(age_labels, avg_scores, color="#3b82f6")

#     plt.title("Average Digital Addiction Score by Age Group")
#     plt.xlabel("Age Group")
#     plt.ylabel("Addiction Score")
#     plt.ylim(0, 100)

#     for bar, score in zip(bars, avg_scores):
#         plt.text(
#             bar.get_x() + bar.get_width() / 2,
#             bar.get_height() + 1,
#             f"{score}",
#             ha="center",
#             fontsize=9,
#         )

#     plt.tight_layout()
#     plt.savefig(chart_path, dpi=120)
#     plt.close("all")

#     context = {
#         "total_assessments": total_assessments,
#         "avg_screen_weekdays": avg_screen_weekdays,
#         "avg_screen_weekends": avg_screen_weekends,
#         "avg_gaming_time": avg_gaming_time,
#         "avg_social_media_time": avg_social_media_time,
#         "age_chart_url": settings.MEDIA_URL + "charts/avg_addiction_by_age.png",
#     }

#     return render(request, "admin/insights.html", context)


