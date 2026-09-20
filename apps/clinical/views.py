"""API views."""

from rest_framework import viewsets

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
from .serializers import (
    AssessmentDiagnosisSerializer,
    AssessmentPainSerializer,
    AssessmentRomSerializer,
    AssessmentSerializer,
    AssessmentStrengthSerializer,
    BodyRegionSerializer,
    DiagnosisMasterSerializer,
    EpisodeSerializer,
    JointSerializer,
    MedicalHistorySerializer,
)


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.filter(deleted_at__isnull=True)
    serializer_class = EpisodeSerializer


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.filter(deleted_at__isnull=True)
    serializer_class = MedicalHistorySerializer


class BodyRegionViewSet(viewsets.ModelViewSet):
    queryset = BodyRegion.objects.filter(deleted_at__isnull=True)
    serializer_class = BodyRegionSerializer


class JointViewSet(viewsets.ModelViewSet):
    queryset = Joint.objects.filter(deleted_at__isnull=True)
    serializer_class = JointSerializer


class DiagnosisMasterViewSet(viewsets.ModelViewSet):
    queryset = DiagnosisMaster.objects.filter(deleted_at__isnull=True)
    serializer_class = DiagnosisMasterSerializer


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.filter(deleted_at__isnull=True)
    serializer_class = AssessmentSerializer


class AssessmentPainViewSet(viewsets.ModelViewSet):
    queryset = AssessmentPain.objects.filter(deleted_at__isnull=True)
    serializer_class = AssessmentPainSerializer


class AssessmentRomViewSet(viewsets.ModelViewSet):
    queryset = AssessmentRom.objects.filter(deleted_at__isnull=True)
    serializer_class = AssessmentRomSerializer


class AssessmentStrengthViewSet(viewsets.ModelViewSet):
    queryset = AssessmentStrength.objects.filter(deleted_at__isnull=True)
    serializer_class = AssessmentStrengthSerializer


class AssessmentDiagnosisViewSet(viewsets.ModelViewSet):
    queryset = AssessmentDiagnosis.objects.filter(deleted_at__isnull=True)
    serializer_class = AssessmentDiagnosisSerializer
