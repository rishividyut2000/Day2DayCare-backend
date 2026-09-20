from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DocumentViewSet,
    PatientAddressViewSet,
    PatientConsentViewSet,
    PatientContactViewSet,
    PatientViewSet,
)

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"patient-addresses", PatientAddressViewSet, basename="patient-address")
router.register(r"patient-contacts", PatientContactViewSet, basename="patient-contact")
router.register(r"patient-consents", PatientConsentViewSet, basename="patient-consent")
router.register(r"documents", DocumentViewSet, basename="document")

urlpatterns = [path("", include(router.urls))]
