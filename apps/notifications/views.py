"""API views."""

from rest_framework import viewsets

from .models import DeviceToken, FollowUp, NotificationLog, NotificationTemplate, Reminder
from .serializers import (
    DeviceTokenSerializer,
    FollowUpSerializer,
    NotificationLogSerializer,
    NotificationTemplateSerializer,
    ReminderSerializer,
)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.filter(deleted_at__isnull=True)
    serializer_class = NotificationTemplateSerializer


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.filter(deleted_at__isnull=True)
    serializer_class = ReminderSerializer


class NotificationLogViewSet(viewsets.ModelViewSet):
    queryset = NotificationLog.objects.filter(deleted_at__isnull=True)
    serializer_class = NotificationLogSerializer


class FollowUpViewSet(viewsets.ModelViewSet):
    queryset = FollowUp.objects.filter(deleted_at__isnull=True)
    serializer_class = FollowUpSerializer


class DeviceTokenViewSet(viewsets.ModelViewSet):
    queryset = DeviceToken.objects.filter(deleted_at__isnull=True)
    serializer_class = DeviceTokenSerializer
