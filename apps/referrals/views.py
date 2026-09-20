"""API views."""

from rest_framework import viewsets

from .models import DrugMaster, Prescription, PrescriptionItem, Referral, ReferralCommission, ReferringDoctor
from .serializers import (
    DrugMasterSerializer,
    PrescriptionItemSerializer,
    PrescriptionSerializer,
    ReferralCommissionSerializer,
    ReferralSerializer,
    ReferringDoctorSerializer,
)


class ReferringDoctorViewSet(viewsets.ModelViewSet):
    queryset = ReferringDoctor.objects.filter(deleted_at__isnull=True)
    serializer_class = ReferringDoctorSerializer


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.filter(deleted_at__isnull=True)
    serializer_class = ReferralSerializer


class ReferralCommissionViewSet(viewsets.ModelViewSet):
    queryset = ReferralCommission.objects.filter(deleted_at__isnull=True)
    serializer_class = ReferralCommissionSerializer


class DrugMasterViewSet(viewsets.ModelViewSet):
    queryset = DrugMaster.objects.filter(deleted_at__isnull=True)
    serializer_class = DrugMasterSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.filter(deleted_at__isnull=True)
    serializer_class = PrescriptionSerializer


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.filter(deleted_at__isnull=True)
    serializer_class = PrescriptionItemSerializer
