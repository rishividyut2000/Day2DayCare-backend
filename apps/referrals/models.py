"""Referring doctors, referrals, immutable prescriptions."""

from django.db import models

from apps.common.models import BaseModel
from apps.patients.models import Patient


class ReferringDoctor(BaseModel):
    name = models.CharField(max_length=150)
    clinic_name = models.CharField(max_length=150, blank=True)
    specialty = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Referral(BaseModel):
    patient = models.ForeignKey(Patient, related_name="referrals", on_delete=models.CASCADE)
    referring_doctor = models.ForeignKey(ReferringDoctor, related_name="referrals", on_delete=models.CASCADE)
    visit_type = models.CharField(max_length=40, default="walk_in")
    status = models.CharField(max_length=40, default="pending")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Referral #{self.id}"


class ReferralCommission(BaseModel):
    referral = models.ForeignKey(Referral, related_name="commissions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="INR")
    is_paid = models.BooleanField(default=False)


class DrugMaster(BaseModel):
    name = models.CharField(max_length=200)
    strength = models.CharField(max_length=80, blank=True)
    dosage_form = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)


class Prescription(BaseModel):
    patient = models.ForeignKey(Patient, related_name="prescriptions", on_delete=models.CASCADE)
    doctor = models.ForeignKey(ReferringDoctor, null=True, blank=True, related_name="prescriptions", on_delete=models.SET_NULL)
    status = models.CharField(max_length=40, default="active")
    notes = models.TextField(blank=True)
    superseded_by = models.ForeignKey("self", null=True, blank=True, related_name="supersedes", on_delete=models.SET_NULL)


class PrescriptionItem(BaseModel):
    prescription = models.ForeignKey(Prescription, related_name="items", on_delete=models.CASCADE)
    item_type = models.CharField(max_length=40, default="medication")
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=80, blank=True)
    frequency = models.CharField(max_length=80, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    instructions = models.TextField(blank=True)
