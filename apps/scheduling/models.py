"""Service types, appointments, sessions, home visits, feedback."""

from django.db import models

from apps.common.models import BaseModel
from apps.patients.models import Patient
from apps.staff.models import Staff


class ServiceType(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)


class Appointment(BaseModel):
    patient = models.ForeignKey(Patient, related_name="appointments", on_delete=models.CASCADE)
    therapist = models.ForeignKey(Staff, null=True, blank=True, related_name="appointments", on_delete=models.SET_NULL)
    service_type = models.ForeignKey(ServiceType, related_name="appointments", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=40, default="scheduled")
    notes = models.TextField(blank=True)


class AppointmentStatusHistory(BaseModel):
    appointment = models.ForeignKey(Appointment, related_name="status_history", on_delete=models.CASCADE)
    old_status = models.CharField(max_length=40, blank=True)
    new_status = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)


class Session(BaseModel):
    appointment = models.ForeignKey(Appointment, null=True, blank=True, related_name="sessions", on_delete=models.SET_NULL)
    patient = models.ForeignKey(Patient, related_name="session_records", on_delete=models.CASCADE)
    therapist = models.ForeignKey(Staff, null=True, blank=True, related_name="sessions", on_delete=models.SET_NULL)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)


class Modality(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)


class SessionModality(BaseModel):
    session = models.ForeignKey(Session, related_name="modalities", on_delete=models.CASCADE)
    modality = models.ForeignKey(Modality, related_name="sessions", on_delete=models.CASCADE)
    quantity = models.CharField(max_length=60, blank=True)


class HomeVisit(BaseModel):
    patient = models.ForeignKey(Patient, related_name="home_visits", on_delete=models.CASCADE)
    therapist = models.ForeignKey(Staff, null=True, blank=True, related_name="home_visits", on_delete=models.SET_NULL)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    status = models.CharField(max_length=40, default="scheduled")
    address = models.TextField(blank=True)
    travel_minutes = models.PositiveIntegerField(default=0)


class HomeVisitLog(BaseModel):
    home_visit = models.ForeignKey(HomeVisit, related_name="logs", on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)


class Feedback(BaseModel):
    patient = models.ForeignKey(Patient, related_name="feedback", on_delete=models.CASCADE)
    session = models.ForeignKey(Session, null=True, blank=True, related_name="feedback", on_delete=models.SET_NULL)
    rating = models.PositiveSmallIntegerField(default=5)
    comments = models.TextField(blank=True)
