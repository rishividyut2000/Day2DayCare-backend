"""Treatment plans, phases, plan-exercises, revisions."""

from django.db import models

from apps.common.models import BaseModel
from apps.exercises.models import Exercise
from apps.patients.models import Patient


class TreatmentPlan(BaseModel):
    patient = models.ForeignKey(Patient, related_name="plans", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=40, default="active")
    notes = models.TextField(blank=True)


class PlanPhase(BaseModel):
    plan = models.ForeignKey(TreatmentPlan, related_name="phases", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    week_number = models.PositiveSmallIntegerField(default=1)
    objectives = models.TextField(blank=True)


class PlanExercise(BaseModel):
    plan = models.ForeignKey(TreatmentPlan, related_name="exercises", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name="plan_links", on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField(default=1)
    reps = models.PositiveSmallIntegerField(default=10)
    hold_seconds = models.PositiveSmallIntegerField(default=0)
    frequency = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)


class PlanRevision(BaseModel):
    plan = models.ForeignKey(TreatmentPlan, related_name="revisions", on_delete=models.CASCADE)
    revision_number = models.PositiveIntegerField(default=1)
    summary = models.TextField(blank=True)


class ProgressionNote(BaseModel):
    plan = models.ForeignKey(TreatmentPlan, related_name="progression_notes", on_delete=models.CASCADE)
    note = models.TextField()
    is_approved = models.BooleanField(default=False)
