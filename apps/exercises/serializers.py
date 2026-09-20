"""DRF serializers."""

from rest_framework import serializers

from .models import Exercise, ExerciseCategory, ExerciseMedia


class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = ["id", "name", "description", "is_active", "created_at", "updated_at"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            "id", "category", "code", "name", "body_part", "difficulty", "default_sets",
            "default_reps", "default_hold_seconds", "instructions", "precautions", "is_active",
        ]


class ExerciseMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseMedia
        fields = ["id", "exercise", "media_type", "storage_key", "duration_seconds", "sort_order"]
