"""DRF serializers."""

from rest_framework import serializers

from .models import DrugMaster, Prescription, PrescriptionItem, Referral, ReferralCommission, ReferringDoctor


class ReferringDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferringDoctor
        fields = ["id", "name", "clinic_name", "specialty", "phone", "email", "city", "is_active"]


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ["id", "patient", "referring_doctor", "visit_type", "status", "notes", "created_at", "updated_at"]


class ReferralCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCommission
        fields = ["id", "referral", "amount", "currency", "is_paid"]


class DrugMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugMaster
        fields = ["id", "name", "strength", "dosage_form", "is_active"]


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["id", "patient", "doctor", "status", "notes", "superseded_by", "created_at", "updated_at"]


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ["id", "prescription", "item_type", "name", "dosage", "frequency", "duration_days", "instructions"]
