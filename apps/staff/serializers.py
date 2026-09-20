"""DRF serializers."""

from rest_framework import serializers

from .models import ServiceZone, Specialization, Staff, StaffAvailability, StaffTimeOff


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["id", "code", "name", "description", "is_active", "created_at", "updated_at"]


class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Staff
        fields = [
            "id", "employee_code", "first_name", "last_name", "full_name", "phone",
            "email", "designation", "gender", "is_active", "is_admin", "created_at", "updated_at",
        ]


class ServiceZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceZone
        fields = ["id", "code", "name", "city", "latitude", "longitude", "is_active", "created_at", "updated_at"]


class StaffAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAvailability
        fields = ["id", "staff", "day_of_week", "start_time", "end_time", "is_available"]


class StaffTimeOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTimeOff
        fields = ["id", "staff", "start_at", "end_at", "reason", "is_approved"]
