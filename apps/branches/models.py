"""Branches, disciplines, clinic settings, numbering sequences."""

from django.db import models

from apps.common.models import BaseModel


class Discipline(BaseModel):
    code = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Branch(BaseModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BranchHours(BaseModel):
    branch = models.ForeignKey(Branch, related_name="hours", on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField()
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("branch", "day_of_week")


class AppSetting(BaseModel):
    key = models.CharField(max_length=100)
    value = models.TextField(blank=True)
    value_type = models.CharField(max_length=20, default="string")

    class Meta:
        unique_together = ("key",)

    def __str__(self):
        return self.key


class NumberingSequence(BaseModel):
    entity = models.CharField(max_length=80)
    prefix = models.CharField(max_length=30, blank=True)
    last_number = models.PositiveIntegerField(default=0)
    width = models.PositiveSmallIntegerField(default=6)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "branch")

    def __str__(self):
        return f"{self.entity}:{self.last_number}"
