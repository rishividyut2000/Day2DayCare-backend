"""API views."""

from rest_framework import viewsets

from .models import Invoice, InvoiceItem, Package, PatientPackage, Payment, Refund
from .serializers import (
    InvoiceItemSerializer,
    InvoiceSerializer,
    PackageSerializer,
    PatientPackageSerializer,
    PaymentSerializer,
    RefundSerializer,
)


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(deleted_at__isnull=True)
    serializer_class = PackageSerializer


class PatientPackageViewSet(viewsets.ModelViewSet):
    queryset = PatientPackage.objects.filter(deleted_at__isnull=True)
    serializer_class = PatientPackageSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.filter(deleted_at__isnull=True)
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.filter(deleted_at__isnull=True)
    serializer_class = InvoiceItemSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.filter(deleted_at__isnull=True)
    serializer_class = RefundSerializer
