from rest_framework import serializers
from assessment.models import DigitalAddictionAssessment

class DigitalAddictionAssessmentSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DigitalAddictionAssessment
        fields = [
            "student",
            "institute",
            "age",
            "gender",
            "da1","da2","da3","da4","da5","da6","da7","da8",
            "primary_device",
            "own_smartphone",
            "mobile_data",
            "screen_weekdays",
            "screen_weekends",
            "night_phone_use",
            "notif_per_hour",
            "social_time",
            "gaming_time",
            "platforms",
            "self_rated_da",
            "predicted_risk",
            "risk_confidence"
        ]
        read_only_fields = ["predicted_risk", "risk_confidence"]

    # ------------------------------
    # FIELD VALIDATIONS
    # ------------------------------
    def validate_age(self, value):
        if not 15 <= value <= 45:
            raise serializers.ValidationError("Age must be between 15 and 45.")
        return value

    def validate_gender(self, value):
        if value not in ["Male", "Female"]:
            raise serializers.ValidationError("Gender must be Male or Female.")
        return value

    def validate_da_field(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("DA fields must be between 1 and 5.")
        return value

    # Dynamically add da1-da8 validators
    for i in range(1, 9):
        locals()[f'validate_da{i}'] = lambda self, value, i=i: self.validate_da_field(value)

    def validate_choice_field(self, value, allowed, field_name):
        if value not in allowed:
            raise serializers.ValidationError(f"{field_name} must be one of {allowed}.")
        return value

    def validate_primary_device(self, value):
        return self.validate_choice_field(value, ["Smartphone", "Laptop", "Tablet"], "Primary device")

    def validate_own_smartphone(self, value):
        return self.validate_choice_field(value, ["Yes", "No"], "Own smartphone")

    def validate_mobile_data(self, value):
        return self.validate_choice_field(value, ["Always", "Sometimes", "Rarely", "No"], "Mobile data")

    def validate_screen_weekdays(self, value):
        return self.validate_choice_field(value, ["<2h","2–3h","3–4h","4–6h",">6h"], "Weekday screen time")

    def validate_screen_weekends(self, value):
        return self.validate_choice_field(value, ["<2h","2–3h","3–4h","4–6h",">6h"], "Weekend screen time")

    def validate_night_phone_use(self, value):
        return self.validate_choice_field(value, ["Never","<30m","30–60m","1–2h",">2h"], "Night phone use")

    def validate_notif_per_hour(self, value):
        return self.validate_choice_field(value, ["<5 times","5–10 times","11–20 times",">20 times"], "Notifications per hour")

    def validate_social_time(self, value):
        return self.validate_choice_field(value, ["<1h","1–2h","2–3h","3–4h",">4h"], "Social media time")

    def validate_gaming_time(self, value):
        return self.validate_choice_field(value, ["None","<30m","30–60m","1–2h",">2h"], "Gaming time")

    def validate_platforms(self, value):
        allowed = {"YouTube","TikTok","Instagram","Facebook","WhatsApp","X/Twitter","Snapchat","Gaming"}
        if not isinstance(value, list):
            raise serializers.ValidationError("Platforms must be a list.")
        invalid = [p for p in value if p not in allowed]
        if invalid:
            raise serializers.ValidationError(f"Invalid platforms: {invalid}")
        return value

    def validate_self_rated_da(self, value):
        return self.validate_choice_field(value, ["not_at_risk","mild","moderate","severe"], "Self-rated DA")

    # --------------------------------------------------
    # CREATE
    # Automatically attach logged-in student & assign platforms
    # --------------------------------------------------
    def create(self, validated_data):
        # Attach logged-in student
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["student"] = request.user

        # Platforms (list) is already in validated_data, no need to pop
        instance = super().create(validated_data)

        return instance
