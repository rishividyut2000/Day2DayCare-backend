"""DRF serializers."""

from rest_framework import serializers

from .models import DeviceToken, FollowUp, NotificationLog, NotificationTemplate, Reminder


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ["id", "code", "channel", "subject", "body", "is_active"]


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ["id", "patient", "template", "scheduled_for", "status", "channel"]


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = ["id", "reminder", "provider", "status", "response"]


class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = ["id", "patient", "follow_up_at", "note", "status"]


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ["id", "patient", "token", "platform", "is_active"]
