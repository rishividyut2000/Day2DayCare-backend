"""DRF serializers."""

from rest_framework import serializers

from .models import ReportMetric


class ReportMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportMetric
        fields = ["id", "name", "description", "query_sql", "is_active"]
