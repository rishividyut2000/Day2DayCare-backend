"""API views."""

from rest_framework import viewsets

from .models import PlanExercise, PlanPhase, PlanRevision, ProgressionNote, TreatmentPlan
from .serializers import (
    PlanExerciseSerializer,
    PlanPhaseSerializer,
    PlanRevisionSerializer,
    ProgressionNoteSerializer,
    TreatmentPlanSerializer,
)


class TreatmentPlanViewSet(viewsets.ModelViewSet):
    queryset = TreatmentPlan.objects.filter(deleted_at__isnull=True)
    serializer_class = TreatmentPlanSerializer


class PlanPhaseViewSet(viewsets.ModelViewSet):
    queryset = PlanPhase.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanPhaseSerializer


class PlanExerciseViewSet(viewsets.ModelViewSet):
    queryset = PlanExercise.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanExerciseSerializer


class PlanRevisionViewSet(viewsets.ModelViewSet):
    queryset = PlanRevision.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanRevisionSerializer


class ProgressionNoteViewSet(viewsets.ModelViewSet):
    queryset = ProgressionNote.objects.filter(deleted_at__isnull=True)
    serializer_class = ProgressionNoteSerializer
