"""Episodes, assessments, pain/ROM/strength, templates, measures."""

from django.db import models

from apps.common.models import BaseModel
from apps.patients.models import Patient


class Episode(BaseModel):
    patient = models.ForeignKey(Patient, related_name="episodes", on_delete=models.CASCADE)
    status = models.CharField(max_length=40, default="active")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    chief_complaint = models.TextField(blank=True)
    diagnosis_summary = models.TextField(blank=True)


class MedicalHistory(BaseModel):
    patient = models.ForeignKey(Patient, related_name="medical_history", on_delete=models.CASCADE)
    condition = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class BodyRegion(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)


class Joint(BaseModel):
    body_region = models.ForeignKey(BodyRegion, related_name="joints", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40, blank=True)

    class Meta:
        unique_together = ("body_region", "name")


class DiagnosisMaster(BaseModel):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
        

class Assessment(BaseModel):
    episode = models.ForeignKey(Episode, related_name="assessments", on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=60, default="initial")
    notes = models.TextField(blank=True)
    pain_overall = models.PositiveSmallIntegerField(null=True, blank=True)
    mobility_score = models.PositiveSmallIntegerField(null=True, blank=True)
    function_score = models.PositiveSmallIntegerField(null=True, blank=True)


class AssessmentPain(BaseModel):
    assessment = models.ForeignKey(Assessment, related_name="pain_data", on_delete=models.CASCADE)
    region = models.CharField(max_length=80, blank=True)
    intensity = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)


class AssessmentRom(BaseModel):
    assessment = models.ForeignKey(Assessment, related_name="rom_data", on_delete=models.CASCADE)
    joint = models.ForeignKey(Joint, null=True, blank=True, related_name="rom_records", on_delete=models.SET_NULL)
    range_value = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)


class AssessmentStrength(BaseModel):
    assessment = models.ForeignKey(Assessment, related_name="strength_data", on_delete=models.CASCADE)
    joint = models.ForeignKey(Joint, null=True, blank=True, related_name="strength_records", on_delete=models.SET_NULL)
    grade = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)


class AssessmentDiagnosis(BaseModel):
    assessment = models.ForeignKey(Assessment, related_name="diagnoses", on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(DiagnosisMaster, related_name="assessments", on_delete=models.CASCADE)
    certainty = models.CharField(max_length=40, default="primary")
