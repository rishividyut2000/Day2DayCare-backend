"""DRF serializers."""

from rest_framework import serializers

from .models import Document, Patient, PatientAddress, PatientConsent, PatientContact


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = [
            "id", "uhid", "first_name", "last_name", "full_name", "phone", "email",
            "gender", "date_of_birth", "is_active", "registration_source", "created_at", "updated_at",
        ]


class PatientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAddress
        fields = [
            "id", "patient", "address_line1", "address_line2", "city", "state",
            "postal_code", "country", "is_primary",
        ]


class PatientContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientContact
        fields = ["id", "patient", "name", "relation", "phone", "email", "is_primary"]


class PatientConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientConsent
        fields = ["id", "patient", "consent_type", "consent_text", "granted_at", "revoked_at", "is_active"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "patient", "file_name", "storage_key", "media_type", "file_size", "is_verified"]
