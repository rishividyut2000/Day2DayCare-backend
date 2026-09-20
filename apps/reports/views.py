"""API views."""

from rest_framework import viewsets

from .models import ReportMetric
from .serializers import ReportMetricSerializer


class ReportMetricViewSet(viewsets.ModelViewSet):
    queryset = ReportMetric.objects.filter(deleted_at__isnull=True)
    serializer_class = ReportMetricSerializer
