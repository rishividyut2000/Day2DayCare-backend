"""API views."""

from rest_framework import viewsets

from .models import ServiceZone, Specialization, Staff, StaffAvailability, StaffTimeOff
from .serializers import (
    ServiceZoneSerializer,
    SpecializationSerializer,
    StaffAvailabilitySerializer,
    StaffSerializer,
    StaffTimeOffSerializer,
)


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.filter(deleted_at__isnull=True)
    serializer_class = SpecializationSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.filter(deleted_at__isnull=True)
    serializer_class = StaffSerializer


class ServiceZoneViewSet(viewsets.ModelViewSet):
    queryset = ServiceZone.objects.filter(deleted_at__isnull=True)
    serializer_class = ServiceZoneSerializer


class StaffAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = StaffAvailability.objects.filter(deleted_at__isnull=True)
    serializer_class = StaffAvailabilitySerializer


class StaffTimeOffViewSet(viewsets.ModelViewSet):
    queryset = StaffTimeOff.objects.filter(deleted_at__isnull=True)
    serializer_class = StaffTimeOffSerializer
