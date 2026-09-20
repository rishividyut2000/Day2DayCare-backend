"""DRF serializers."""

from rest_framework import serializers

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


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["id", "name", "duration_minutes", "is_active"]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id", "patient", "therapist", "service_type", "start_at", "end_at", "status", "notes"]


class AppointmentStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentStatusHistory
        fields = ["id", "appointment", "old_status", "new_status", "notes"]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["id", "appointment", "patient", "therapist", "start_at", "end_at", "notes", "completed"]


class ModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Modality
        fields = ["id", "name", "is_active"]


class SessionModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionModality
        fields = ["id", "session", "modality", "quantity"]


class HomeVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeVisit
        fields = ["id", "patient", "therapist", "scheduled_start", "scheduled_end", "status", "address", "travel_minutes"]


class HomeVisitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeVisitLog
        fields = ["id", "home_visit", "started_at", "ended_at", "notes"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "patient", "session", "rating", "comments"]
