"""Templates, reminders, delivery log, follow-ups."""

from django.db import models

from apps.common.models import BaseModel
from apps.patients.models import Patient


class NotificationTemplate(BaseModel):
    code = models.CharField(max_length=80, unique=True)
    channel = models.CharField(max_length=40, default="sms")
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    is_active = models.BooleanField(default=True)


class Reminder(BaseModel):
    patient = models.ForeignKey(Patient, related_name="reminders", on_delete=models.CASCADE)
    template = models.ForeignKey(NotificationTemplate, related_name="reminders", on_delete=models.CASCADE)
    scheduled_for = models.DateTimeField()
    status = models.CharField(max_length=40, default="pending")
    channel = models.CharField(max_length=40, default="sms")


class NotificationLog(BaseModel):
    reminder = models.ForeignKey(Reminder, related_name="logs", on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=40, default="queued")
    response = models.TextField(blank=True)


class FollowUp(BaseModel):
    patient = models.ForeignKey(Patient, related_name="follow_ups", on_delete=models.CASCADE)
    follow_up_at = models.DateTimeField()
    note = models.TextField(blank=True)
    status = models.CharField(max_length=40, default="pending")


class DeviceToken(BaseModel):
    patient = models.ForeignKey(Patient, related_name="device_tokens", on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    platform = models.CharField(max_length=20, default="android")
    is_active = models.BooleanField(default=True)
