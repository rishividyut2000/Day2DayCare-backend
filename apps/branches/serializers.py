"""DRF serializers."""

from rest_framework import serializers

from .models import AppSetting, Branch, BranchHours, Discipline, NumberingSequence


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["id", "code", "name", "description", "is_active", "created_at", "updated_at"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "id", "code", "name", "city", "state", "address", "phone", "email",
            "latitude", "longitude", "is_active", "opening_time", "closing_time",
            "created_at", "updated_at",
        ]


class BranchHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchHours
        fields = ["id", "branch", "day_of_week", "open_time", "close_time", "is_closed"]


class AppSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSetting
        fields = ["id", "key", "value", "value_type", "updated_at"]


class NumberingSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberingSequence
        fields = ["id", "entity", "prefix", "last_number", "width", "branch"]
