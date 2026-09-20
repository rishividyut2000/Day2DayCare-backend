"""Shared exercise master library (public schema)."""

from django.db import models

from apps.common.models import BaseModel


class ExerciseMaster(BaseModel):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=80, blank=True)
    body_region = models.CharField(max_length=80, blank=True)
    difficulty = models.PositiveSmallIntegerField(default=1)
    default_sets = models.PositiveSmallIntegerField(default=1)
    default_reps = models.PositiveSmallIntegerField(default=10)
    default_hold_seconds = models.PositiveSmallIntegerField(default=0)
    instructions = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ExerciseMasterMedia(BaseModel):
    exercise = models.ForeignKey(ExerciseMaster, related_name="media", on_delete=models.CASCADE)
    media_type = models.CharField(max_length=20, default="video")
    storage_key = models.CharField(max_length=500)
    duration_seconds = models.PositiveIntegerField(default=0)
    sort_order = models.PositiveSmallIntegerField(default=0)
