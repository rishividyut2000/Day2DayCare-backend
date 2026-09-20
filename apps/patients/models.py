"""Patients, addresses, contacts, consents, documents."""

from django.db import models

from apps.common.models import BaseModel


class Patient(BaseModel):
    uhid = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    registration_source = models.CharField(max_length=50, default="walk_in")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name or self.uhid


class PatientAddress(BaseModel):
    patient = models.ForeignKey(Patient, related_name="addresses", on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=80, default="India")
    is_primary = models.BooleanField(default=False)


class PatientContact(BaseModel):
    patient = models.ForeignKey(Patient, related_name="contacts", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    relation = models.CharField(max_length=80)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)


class PatientConsent(BaseModel):
    patient = models.ForeignKey(Patient, related_name="consents", on_delete=models.CASCADE)
    consent_type = models.CharField(max_length=80)
    consent_text = models.TextField(blank=True)
    granted_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class Document(BaseModel):
    patient = models.ForeignKey(Patient, null=True, blank=True, related_name="documents", on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    storage_key = models.CharField(max_length=500)
    media_type = models.CharField(max_length=50, default="image")
    file_size = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
