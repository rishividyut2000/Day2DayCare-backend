"""API views."""

from rest_framework import viewsets

from .models import (
    Appointment,
    AppointmentStatusHistory,
    Feedback,
    HomeVisit,
    HomeVisitLog,
    Modality,
    ServiceType,
    Session,
    SessionModality,
)
from .serializers import (
    AppointmentSerializer,
    AppointmentStatusHistorySerializer,
    FeedbackSerializer,
    HomeVisitLogSerializer,
    HomeVisitSerializer,
    ModalitySerializer,
    ServiceTypeSerializer,
    SessionModalitySerializer,
    SessionSerializer,
)


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.filter(deleted_at__isnull=True)
    serializer_class = ServiceTypeSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.filter(deleted_at__isnull=True)
    serializer_class = AppointmentSerializer


class AppointmentStatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = AppointmentStatusHistory.objects.filter(deleted_at__isnull=True)
    serializer_class = AppointmentStatusHistorySerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.filter(deleted_at__isnull=True)
    serializer_class = SessionSerializer


class ModalityViewSet(viewsets.ModelViewSet):
    queryset = Modality.objects.filter(deleted_at__isnull=True)
    serializer_class = ModalitySerializer


class SessionModalityViewSet(viewsets.ModelViewSet):
    queryset = SessionModality.objects.filter(deleted_at__isnull=True)
    serializer_class = SessionModalitySerializer


class HomeVisitViewSet(viewsets.ModelViewSet):
    queryset = HomeVisit.objects.filter(deleted_at__isnull=True)
    serializer_class = HomeVisitSerializer


class HomeVisitLogViewSet(viewsets.ModelViewSet):
    queryset = HomeVisitLog.objects.filter(deleted_at__isnull=True)
    serializer_class = HomeVisitLogSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.filter(deleted_at__isnull=True)
    serializer_class = FeedbackSerializer
