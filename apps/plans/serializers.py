"""DRF serializers."""

from rest_framework import serializers

from .models import PlanExercise, PlanPhase, PlanRevision, ProgressionNote, TreatmentPlan


class TreatmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlan
        fields = ["id", "patient", "title", "status", "notes", "created_at", "updated_at"]


class PlanPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPhase
        fields = ["id", "plan", "name", "week_number", "objectives"]


class PlanExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanExercise
        fields = ["id", "plan", "exercise", "sets", "reps", "hold_seconds", "frequency", "notes"]


class PlanRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanRevision
        fields = ["id", "plan", "revision_number", "summary", "created_at"]


class ProgressionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressionNote
        fields = ["id", "plan", "note", "is_approved", "created_at", "updated_at"]
