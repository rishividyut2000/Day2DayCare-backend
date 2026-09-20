"""Materialised views and reporting endpoints."""

from django.db import models

from apps.common.models import BaseModel


class ReportMetric(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    query_sql = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
