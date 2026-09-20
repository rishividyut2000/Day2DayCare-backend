"""API views."""

from rest_framework import viewsets

from .models import Document, Patient, PatientAddress, PatientConsent, PatientContact
from .serializers import (
    DocumentSerializer,
    PatientAddressSerializer,
    PatientConsentSerializer,
    PatientContactSerializer,
    PatientSerializer,
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(deleted_at__isnull=True)
    serializer_class = PatientSerializer


class PatientAddressViewSet(viewsets.ModelViewSet):
    queryset = PatientAddress.objects.filter(deleted_at__isnull=True)
    serializer_class = PatientAddressSerializer


class PatientContactViewSet(viewsets.ModelViewSet):
    queryset = PatientContact.objects.filter(deleted_at__isnull=True)
    serializer_class = PatientContactSerializer


class PatientConsentViewSet(viewsets.ModelViewSet):
    queryset = PatientConsent.objects.filter(deleted_at__isnull=True)
    serializer_class = PatientConsentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(deleted_at__isnull=True)
    serializer_class = DocumentSerializer
