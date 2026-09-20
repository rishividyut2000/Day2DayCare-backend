"""Therapists, specializations, availability, time-off, service zones."""

from django.db import models

from apps.common.models import BaseModel


class Specialization(BaseModel):
    code = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Staff(BaseModel):
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    employee_code = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    designation = models.CharField(max_length=80, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name or self.employee_code


class StaffSpecialization(BaseModel):
    staff = models.ForeignKey(Staff, related_name="specializations", on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, related_name="staff_members", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("staff", "specialization")


class StaffBranch(BaseModel):
    staff = models.ForeignKey(Staff, related_name="branches", on_delete=models.CASCADE)
    branch_id = models.UUIDField(db_index=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ("staff", "branch_id")


class ServiceZone(BaseModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StaffServiceZone(BaseModel):
    staff = models.ForeignKey(Staff, related_name="service_zones", on_delete=models.CASCADE)
    zone = models.ForeignKey(ServiceZone, related_name="staff_members", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("staff", "zone")


class StaffAvailability(BaseModel):
    staff = models.ForeignKey(Staff, related_name="availability", on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("staff", "day_of_week")


class StaffTimeOff(BaseModel):
    staff = models.ForeignKey(Staff, related_name="time_off", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    reason = models.CharField(max_length=200, blank=True)
    is_approved = models.BooleanField(default=False)
