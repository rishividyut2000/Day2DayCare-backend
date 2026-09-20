from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DrugMasterViewSet,
    PrescriptionItemViewSet,
    PrescriptionViewSet,
    ReferralCommissionViewSet,
    ReferralViewSet,
    ReferringDoctorViewSet,
)

router = DefaultRouter()
router.register(r"referring-doctors", ReferringDoctorViewSet, basename="referring-doctor")
router.register(r"referrals", ReferralViewSet, basename="referral")
router.register(r"referral-commissions", ReferralCommissionViewSet, basename="referral-commission")
router.register(r"drug-master", DrugMasterViewSet, basename="drug-master")
router.register(r"prescriptions", PrescriptionViewSet, basename="prescription")
router.register(r"prescription-items", PrescriptionItemViewSet, basename="prescription-item")

urlpatterns = [path("", include(router.urls))]
