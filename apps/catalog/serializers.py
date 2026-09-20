"""DRF serializers."""

from rest_framework import serializers

from .models import ExerciseMaster, ExerciseMasterMedia


class ExerciseMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseMaster
        fields = [
            "id", "code", "name", "category", "body_region", "difficulty",
            "default_sets", "default_reps", "default_hold_seconds", "instructions",
            "precautions", "is_active",
        ]


class ExerciseMasterMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseMasterMedia
        fields = ["id", "exercise", "media_type", "storage_key", "duration_seconds", "sort_order"]
