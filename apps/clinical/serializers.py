"""DRF serializers."""

from rest_framework import serializers

from .models import (
    Assessment,
    AssessmentDiagnosis,
    AssessmentPain,
    AssessmentRom,
    AssessmentStrength,
    BodyRegion,
    DiagnosisMaster,
    Episode,
    Joint,
    MedicalHistory,
)


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "patient", "status", "start_date", "end_date", "chief_complaint", "diagnosis_summary"]


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ["id", "patient", "condition", "details", "is_active"]


class BodyRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyRegion
        fields = ["id", "name", "description"]


class JointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joint
        fields = ["id", "body_region", "name", "code"]


class DiagnosisMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisMaster
        fields = ["id", "code", "name", "description"]


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id", "episode", "assessment_type", "notes", "pain_overall",
            "mobility_score", "function_score",
        ]


class AssessmentPainSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPain
        fields = ["id", "assessment", "region", "intensity", "description"]


class AssessmentRomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentRom
        fields = ["id", "assessment", "joint", "range_value", "notes"]


class AssessmentStrengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentStrength
        fields = ["id", "assessment", "joint", "grade", "notes"]


class AssessmentDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentDiagnosis
        fields = ["id", "assessment", "diagnosis", "certainty"]
