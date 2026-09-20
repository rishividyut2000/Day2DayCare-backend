"""API views."""

from rest_framework import viewsets

from .models import AppSetting, Branch, BranchHours, Discipline, NumberingSequence
from .serializers import (
    AppSettingSerializer,
    BranchHoursSerializer,
    BranchSerializer,
    DisciplineSerializer,
    NumberingSequenceSerializer,
)


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.filter(deleted_at__isnull=True)
    serializer_class = DisciplineSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.filter(deleted_at__isnull=True)
    serializer_class = BranchSerializer


class BranchHoursViewSet(viewsets.ModelViewSet):
    queryset = BranchHours.objects.filter(deleted_at__isnull=True)
    serializer_class = BranchHoursSerializer


class AppSettingViewSet(viewsets.ModelViewSet):
    queryset = AppSetting.objects.filter(deleted_at__isnull=True)
    serializer_class = AppSettingSerializer


class NumberingSequenceViewSet(viewsets.ModelViewSet):
    queryset = NumberingSequence.objects.filter(deleted_at__isnull=True)
    serializer_class = NumberingSequenceSerializer
