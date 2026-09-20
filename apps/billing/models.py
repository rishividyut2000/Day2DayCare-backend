"""Packages, patient packages, invoices, payments, refunds."""

from django.db import models

from apps.common.models import BaseModel
from apps.patients.models import Patient


class Package(BaseModel):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=150)
    package_type = models.CharField(max_length=40, default="single")
    validity_days = models.PositiveIntegerField(default=30)
    session_count = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="INR")
    is_active = models.BooleanField(default=True)


class PatientPackage(BaseModel):
    patient = models.ForeignKey(Patient, related_name="packages", on_delete=models.CASCADE)
    package = models.ForeignKey(Package, related_name="assignments", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    sessions_included = models.PositiveIntegerField(default=0)
    sessions_used = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=40, default="active")


class Invoice(BaseModel):
    patient = models.ForeignKey(Patient, related_name="invoices", on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=40, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="INR")
    status = models.CharField(max_length=40, default="draft")


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class Payment(BaseModel):
    invoice = models.ForeignKey(Invoice, related_name="payments", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=40, default="cash")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=40, default="success")


class Refund(BaseModel):
    invoice = models.ForeignKey(Invoice, related_name="refunds", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=40, default="requested")
