"""DRF serializers."""

from rest_framework import serializers

from .models import Invoice, InvoiceItem, Package, PatientPackage, Payment, Refund


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "id", "code", "name", "package_type", "validity_days", "session_count",
            "price", "currency", "is_active",
        ]


class PatientPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPackage
        fields = [
            "id", "patient", "package", "start_date", "end_date", "sessions_included",
            "sessions_used", "status",
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id", "patient", "invoice_number", "total_amount", "tax_amount",
            "discount_amount", "currency", "status",
        ]


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["id", "invoice", "description", "quantity", "unit_price", "amount"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "invoice", "payment_method", "amount", "reference", "status"]


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ["id", "invoice", "amount", "reason", "status"]
